"""
Enhanced Habu Chat Agent with Real LLM Integration
Uses OpenAI GPT-4 for intelligent conversation and tool orchestration
"""
import json
import os
import logging
from typing import Dict, Any, List, Optional, Tuple
import openai
from openai import AsyncOpenAI
import keyring
from tools.habu_list_partners import habu_list_partners
from tools.habu_list_templates import habu_list_templates
from tools.habu_submit_query import habu_submit_query
from tools.habu_check_status import habu_check_status
from tools.habu_get_results import habu_get_results
from utils.error_handling import (
    retry_async,
    format_error_response,
    APIError,
    AuthenticationError,
    openai_circuit_breaker,
    with_circuit_breaker
)

logger = logging.getLogger(__name__)

class EnhancedHabuChatAgent:
    """
    LLM-powered agent for intelligent interaction with Habu Clean Room API.
    Uses OpenAI GPT-4 for natural language understanding and conversation.
    """
    
    def __init__(self):
        self.last_query_id: Optional[str] = None
        self.context_memory: Dict[str, Any] = {}
        self.client = None
        self._setup_openai_client()
        
    def _setup_openai_client(self):
        """Setup OpenAI client with API key from keyring or environment"""
        api_key = None
        try:
            # In production (Render), keyring won't work, so try environment first
            api_key = os.getenv("OPENAI_API_KEY")
            if api_key:
                logger.info("Found OpenAI API key in environment variable")
            else:
                # Try keyring for local development
                for key_name in ["OpenAI Key", "OPENAI_API_KEY", "openai_api_key", "openai-api-key"]:
                    try:
                        api_key = keyring.get_password("memex", key_name)
                        if api_key:
                            logger.info(f"Found OpenAI API key in keyring: {key_name}")
                            break
                    except Exception as e:
                        logger.debug(f"Keyring access failed for {key_name}: {e}")
                        continue
            
            if api_key and api_key.startswith('sk-'):
                self.client = AsyncOpenAI(api_key=api_key)
                logger.info("✅ OpenAI client initialized successfully")
            else:
                logger.warning(f"❌ No valid OpenAI API key found. Key present: {bool(api_key)}, Valid format: {api_key.startswith('sk-') if api_key else False}")
                self.client = None
                
        except Exception as e:
            logger.error(f"⚠️ Failed to setup OpenAI client: {e}. Using rule-based fallback.")
            self.client = None
    
    @retry_async(max_retries=2, delay=1.0)
    async def process_request(self, user_input: str) -> str:
        """
        Process a natural language request using LLM-powered understanding.
        
        Args:
            user_input (str): User's natural language request
            
        Returns:
            str: Formatted response with results and next steps
        """
        try:
            logger.info(f"Processing request: {user_input[:100]}...")
            
            if self.client:
                return await self._llm_powered_processing(user_input)
            else:
                # Fallback to rule-based processing
                logger.info("Using rule-based processing (OpenAI not available)")
                return await self._rule_based_processing(user_input)
                
        except AuthenticationError as e:
            logger.error(f"Authentication error: {e}")
            return "I'm having trouble authenticating with the Habu API. Please check your credentials and try again."
        except APIError as e:
            logger.error(f"API error: {e}")
            return f"I encountered an API error: {e.message}. Please try again in a moment."
        except Exception as e:
            logger.error(f"Unexpected error processing request: {e}")
            return f"I encountered an unexpected error: {str(e)}. Please try rephrasing your request or contact support if the issue persists."
    
    @with_circuit_breaker(openai_circuit_breaker)
    async def _llm_powered_processing(self, user_input: str) -> str:
        """Process request using LLM for intent understanding and tool orchestration."""
        
        # Enhanced system prompt with REAL cleanroom context and intelligent response patterns
        system_prompt = """You are an expert Habu Clean Room Data Collaboration Assistant powered by OpenAI GPT-4. You help enterprises manage privacy-safe data partnerships and advanced analytics.

🏢 HABU CLEAN ROOM PLATFORM OVERVIEW:
Habu enables secure data collaboration between companies without exposing raw data. Partners can run joint analytics while maintaining privacy through cryptographic clean rooms.

🔧 AVAILABLE API TOOLS:
1. habu_list_partners - View your data collaboration partners
2. habu_list_templates - Browse advanced analytics templates (ML/AI models, audience analysis, attribution)  
3. habu_submit_query - Execute sophisticated analytics with partner data
4. habu_check_status - Monitor query progress (building, running, completed)
5. habu_get_results - Retrieve insights with business intelligence summaries

📊 LIVE CLEANROOM CONTEXT - "Data Marketplace Demo":
🎯 CURRENT REAL DATA:
- **Cleanroom Name**: "Data Marketplace Demo" (ICDC - Demo organization)
- **Status**: COMPLETE and fully operational
- **Partners**: 0 active partners (new cleanroom, partnerships being established)
- **Templates**: 4 real analytics templates available

🔥 YOUR REAL ANALYTICS TEMPLATES:
1. **"Database of Events, Language, and Tone - Sentiment Analysis - Global"** 
   - Category: Sentiment Analysis | Status: MISSING_DATASETS
   - Note: "This template needs dataset configuration before execution"
   
2. **"Database of Events, Language, and Tone - Sentiment Analysis - Global"** 
   - Category: Sentiment Analysis | Status: READY
   - Action: "Ready for immediate sentiment analysis execution"
   
3. **"Geotrace - Mobile Location - Pattern of Life"**
   - Category: Location Data | Status: READY  
   - Action: "Ready for mobile location and pattern of life analysis"
   
4. **"TimberMac and Geotrace - Combined Analysis - Location Data"**
   - Category: Pattern of Life | Status: READY
   - Action: "Ready for combined location intelligence analysis"

🧠 INTELLIGENT RESPONSE PATTERNS:
When users ask about analytics capabilities, provide smart, status-aware responses:

**For READY templates (3 available):**
- "I see you have 2 Sentiment Analysis templates - one is READY for queries while the other needs dataset setup"
- "Your Location Data template from Geotrace is available for Pattern of Life analysis"
- "The TimberMac and Geotrace combined analysis template could provide comprehensive location insights"

**For MISSING_DATASETS template (1 unavailable):**
- "One of your Sentiment Analysis templates requires dataset configuration before it can be executed"
- "Contact your administrator to complete the setup for the unavailable template"

🔥 CATEGORY-AWARE RECOMMENDATIONS:
- **Sentiment Analysis**: "You can analyze global sentiment patterns with your READY template"
- **Location Data**: "Mobile location analytics are available through your Geotrace template"  
- **Pattern of Life**: "Combined behavioral analysis is ready with your TimberMac/Geotrace template"

🎯 CONVERSATION STYLE:
- Be conversational and business-intelligent
- Reference specific templates by name when relevant
- Provide different responses based on template status (READY vs MISSING_DATASETS)
- Give actionable recommendations based on available capabilities
- Guide users through realistic workflows with our specific templates
- Be realistic about 0 partners (common for new cleanrooms)
- Provide strategic recommendations based on actual available data

📋 REAL PRODUCTION CONTEXT:
- **Live API Mode**: Using real Habu API with OAuth2 authentication
- **Real Cleanroom**: "Data Marketplace Demo" fully operational
- **Analytics Ready**: 3 templates immediately available for execution
- **Setup Needed**: 1 template requires dataset configuration
- **Real Categories**: Sentiment Analysis, Location Data, Pattern of Life
- **Partnership Status**: 0 partners (new cleanroom - partnerships being established)
- **Last Query**: {last_query_id}

🤖 RESPONSE FORMAT:
For tool actions, respond with JSON:
{{
  "action": "tool_name",
  "tool_params": {{}},
  "explanation": "Business-focused explanation with strategic context"
}}

For general questions, provide conversational responses about:
- Clean room technology and benefits
- Privacy-safe data collaboration concepts  
- Strategic use cases and ROI opportunities
- Best practices for data partnerships
- Platform capabilities and competitive advantages

💡 EXAMPLE INTERACTIONS:
User: "What clean rooms are showing as available?"
Response: {{"action": "habu_list_partners", "tool_params": {{}}, "explanation": "I'll show you your premium data partnership network. These are major brands you can collaborate with for advanced analytics while maintaining complete data privacy."}}

User: "How does audience overlap analysis work?"
Response: Conversational explanation of privacy-safe cross-platform analysis, business benefits, and strategic applications.

User: "Run a competitive analysis"
Response: Guide through template selection, explain methodology, and set expectations for insights.
- "check my last query" → {{"action": "habu_check_status", "tool_params": {{"query_id": "last"}}, "explanation": "I'll check the status of your most recent query."}}

IMPORTANT: When users ask to "run", "execute", "submit", or "start" an analysis, you should use habu_submit_query. For audience overlap analysis, use template_id "tmpl-001-audience-overlap".
"""

        try:
            # Create the conversation with GPT-4
            response = await self.client.chat.completions.create(
                model="gpt-4o",  # Using GPT-4 Omni model
                max_tokens=1000,
                messages=[
                    {
                        "role": "system", 
                        "content": system_prompt.format(last_query_id=self.last_query_id or "None")
                    },
                    {
                        "role": "user", 
                        "content": user_input
                    }
                ]
            )
            
            # Parse GPT-4's response
            gpt_response = response.choices[0].message.content.strip()
            
            # Try to parse as JSON - handle markdown code blocks
            try:
                # Remove markdown code blocks if present
                clean_response = gpt_response.strip()
                if clean_response.startswith("```json"):
                    clean_response = clean_response[7:]  # Remove ```json
                if clean_response.endswith("```"):
                    clean_response = clean_response[:-3]  # Remove ```
                clean_response = clean_response.strip()
                
                action_plan = json.loads(clean_response)
            except json.JSONDecodeError:
                # If not JSON, treat as conversation response
                return gpt_response
            
            # Execute the planned action
            action = action_plan.get("action")
            tool_params = action_plan.get("tool_params", {})
            explanation = action_plan.get("explanation", "")
            
            if action == "habu_list_partners":
                result = await habu_list_partners()
                return self._format_llm_response(explanation, result, "partners")
                
            elif action == "habu_list_templates":
                result = await habu_list_templates()
                return self._format_llm_response(explanation, result, "templates")
                
            elif action == "habu_submit_query":
                template_id = tool_params.get("template_id")
                parameters = tool_params.get("parameters", {})
                if not template_id:
                    return "I need a template ID to submit a query. Please specify which template you'd like to use."
                result = await habu_submit_query(template_id, parameters)
                result_data = json.loads(result)
                if result_data.get("status") == "success":
                    self.last_query_id = result_data.get("query_id")
                return self._format_llm_response(explanation, result, "submit")
                
            elif action == "habu_check_status":
                query_id = tool_params.get("query_id")
                if query_id == "last" or not query_id:
                    query_id = self.last_query_id
                if not query_id:
                    return "I don't have a query ID to check. Please provide a query ID or run a query first."
                result = await habu_check_status(query_id)
                return self._format_llm_response(explanation, result, "status")
                
            elif action == "habu_get_results":
                query_id = tool_params.get("query_id")
                if query_id == "last" or not query_id:
                    query_id = self.last_query_id
                if not query_id:
                    return "I don't have a query ID to get results for. Please provide a query ID or run a query first."
                result = await habu_get_results(query_id)
                return self._format_llm_response(explanation, result, "results")
                
            else:
                # Conversation response
                return explanation
                
        except Exception as e:
            return f"I encountered an error with the AI processing: {str(e)}. Let me try a simpler approach."
    
    def _format_llm_response(self, explanation: str, tool_result: str, result_type: str) -> str:
        """Format tool results with intelligent, context-aware explanations."""
        try:
            result_data = json.loads(tool_result)
            
            if result_type == "partners":
                if result_data.get("status") == "success":
                    partners = result_data.get("partners", [])
                    if partners:
                        partner_names = [p.get("name", "Unknown") for p in partners]
                        return f"{explanation}\n\nHere are your clean room partners:\n• " + "\n• ".join(partner_names)
                    else:
                        return f"{explanation}\n\n🏢 **Partnership Status**: Your 'Data Marketplace Demo' cleanroom is newly established with 0 active partners. This is normal for new cleanrooms.\n\n**Next Steps**: Contact your administrator to establish data partnerships with brands like retailers, media companies, or data providers. Once partnerships are established, you'll be able to run collaborative analytics while maintaining data privacy."
                        
            elif result_type == "templates":
                if result_data.get("status") == "success":
                    templates = result_data.get("templates", [])
                    if templates:
                        # Enhanced template display with intelligent status analysis
                        ready_templates = []
                        missing_data_templates = []
                        
                        for t in templates:
                            name = t.get("name", "Unknown")
                            category = t.get("category", "Unknown")
                            status = t.get("status", "Unknown")
                            
                            if status == "READY":
                                ready_templates.append(f"✅ **{name}**\n   Category: {category} | Status: Ready for execution")
                            elif status == "MISSING_DATASETS":
                                missing_data_templates.append(f"⚠️ **{name}**\n   Category: {category} | Status: Needs dataset configuration")
                            else:
                                ready_templates.append(f"• **{name}**\n   Category: {category} | Status: {status}")
                        
                        response = f"{explanation}\n\n🔥 **Your Analytics Templates:**\n\n"
                        
                        if ready_templates:
                            response += "**🚀 Ready for Execution:**\n" + "\n\n".join(ready_templates)
                            if len(ready_templates) == 3:
                                response += "\n\n💡 **Quick Start**: You have 3 templates ready! Try asking 'Run a sentiment analysis' or 'Analyze location patterns'"
                        
                        if missing_data_templates:
                            response += "\n\n**⚙️ Needs Setup:**\n" + "\n\n".join(missing_data_templates)
                            response += "\n\n📞 **Action Required**: Contact your administrator to complete dataset configuration for the template above."
                        
                        # Add category-specific recommendations
                        if any("Sentiment Analysis" in t.get("category", "") for t in templates):
                            response += "\n\n🎯 **Sentiment Analysis**: Analyze customer feedback, brand mentions, and market sentiment patterns."
                        if any("Location Data" in t.get("category", "") for t in templates):
                            response += "\n\n📍 **Location Analytics**: Discover mobility patterns, geographic insights, and behavioral trends."
                        if any("Pattern of Life" in t.get("category", "") for t in templates):
                            response += "\n\n🔍 **Pattern of Life**: Combined analysis for comprehensive behavioral intelligence."
                        
                        return response
                    else:
                        return f"{explanation}\n\nNo query templates are available yet. Contact your administrator to set up analysis templates."
                        
            elif result_type == "submit":
                if result_data.get("status") == "success":
                    query_id = result_data.get("query_id", "unknown")
                    status = result_data.get("query_status", "unknown")
                    return f"{explanation}\n\nQuery submitted successfully! Your query ID is {query_id} and it's currently {status}."
                    
            elif result_type == "status":
                if result_data.get("status") == "success":
                    query_status = result_data.get("query_status", "unknown")
                    progress = result_data.get("progress_percent", 0)
                    return f"{explanation}\n\nYour query is {query_status}" + (f" ({progress}% complete)" if progress > 0 else "") + "."
                    
            elif result_type == "results":
                if result_data.get("status") == "success":
                    summary = result_data.get("business_summary", "Results available")
                    count = result_data.get("record_count", 0)
                    return f"{explanation}\n\n**Summary**: {summary}\n**Records**: {count} data points"
            
            # Fallback for errors
            error_msg = result_data.get("summary", "Unknown error occurred")
            return f"{explanation}\n\nHowever, I encountered an issue: {error_msg}"
            
        except:
            return f"{explanation}\n\nI got a response but had trouble parsing it. Here's the raw result: {tool_result[:200]}..."
    
    async def _rule_based_processing(self, user_input: str) -> str:
        """Fallback rule-based processing when LLM is not available."""
        user_lower = user_input.lower()
        
        if any(phrase in user_lower for phrase in ["partners", "who can", "available partners"]):
            result = await habu_list_partners()
            result_data = json.loads(result)
            if result_data["status"] == "success" and result_data["partners"]:
                partners = [p.get("name", "Unknown") for p in result_data["partners"]]
                return f"Your clean room partners:\n• " + "\n• ".join(partners)
            else:
                return "No clean room partners are currently available."
                
        elif any(phrase in user_lower for phrase in ["templates", "queries", "what can"]):
            result = await habu_list_templates()
            result_data = json.loads(result)
            if result_data["status"] == "success" and result_data["templates"]:
                templates = [f"• {t.get('name', 'Unknown')}" for t in result_data["templates"]]
                return f"Available query templates:\n" + "\n".join(templates)
            else:
                return "No query templates are currently available."
                
        elif any(phrase in user_lower for phrase in ["status", "check", "how is"]):
            if self.last_query_id:
                result = await habu_check_status(self.last_query_id)
                result_data = json.loads(result)
                if result_data["status"] == "success":
                    return f"Your query {self.last_query_id} is {result_data['query_status']}"
                else:
                    return f"Couldn't check status: {result_data.get('summary', 'Unknown error')}"
            else:
                return "I don't have a recent query to check. Please provide a query ID."
                
        elif any(phrase in user_lower for phrase in ["results", "show me", "what were"]):
            if self.last_query_id:
                result = await habu_get_results(self.last_query_id)
                result_data = json.loads(result)
                if result_data["status"] == "success":
                    summary = result_data.get("business_summary", "Results retrieved")
                    return f"Results: {summary}"
                else:
                    return f"Couldn't get results: {result_data.get('summary', 'Unknown error')}"
            else:
                return "I don't have a recent query to get results for. Please provide a query ID."
        
        # Help message for unknown requests
        return """I can help you with:
• **Partners**: "Show me my partners" or "Who can I collaborate with?"
• **Templates**: "What queries can I run?" or "Show me templates"
• **Status**: "Check my query status" or "How is my analysis doing?"
• **Results**: "Show me results" or "What were the findings?"

What would you like to do?"""

# Create enhanced agent instance
enhanced_habu_agent = EnhancedHabuChatAgent()