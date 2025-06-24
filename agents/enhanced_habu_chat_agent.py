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
from tools.habu_enhanced_templates import habu_enhanced_templates, habu_list_templates
from tools.habu_submit_query import habu_submit_query
from tools.habu_check_status import habu_check_status
from tools.habu_get_results import habu_get_results
from tools.habu_list_exports import habu_list_exports, habu_download_export
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
        
        # Enhanced context tracking for Phase C
        self.active_queries: Dict[str, Dict[str, Any]] = {}  # query_id -> metadata
        self.conversation_context: Dict[str, Any] = {
            "recent_templates": [],
            "recent_partners": [],
            "query_history": [],
            "pending_results": []
        }
        self.last_templates_check: Optional[str] = None
        self.last_partners_check: Optional[str] = None
        
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
    
    def _update_query_context(self, query_id: str, template_id: str, status: str, query_name: str = None):
        """Update the active query context for enhanced tracking."""
        self.active_queries[query_id] = {
            "template_id": template_id,
            "status": status,
            "query_name": query_name,
            "submitted_at": json.dumps({"timestamp": "now"}, default=str),
            "last_checked": None
        }
        
        # Add to conversation context
        query_entry = {
            "query_id": query_id,
            "template_id": template_id,
            "status": status,
            "query_name": query_name
        }
        
        # Keep only last 10 queries in history
        self.conversation_context["query_history"].insert(0, query_entry)
        if len(self.conversation_context["query_history"]) > 10:
            self.conversation_context["query_history"] = self.conversation_context["query_history"][:10]
        
        # Update pending results list
        if status.lower() in ["submitted", "running", "processing", "in_progress"]:
            if query_id not in self.conversation_context["pending_results"]:
                self.conversation_context["pending_results"].append(query_id)
        elif status.lower() in ["completed", "success", "finished"]:
            if query_id in self.conversation_context["pending_results"]:
                self.conversation_context["pending_results"].remove(query_id)
    
    def _get_context_summary(self) -> str:
        """Generate a context summary for the LLM to maintain conversation continuity."""
        context_parts = []
        
        # Recent query activity
        if self.active_queries:
            recent_queries = list(self.active_queries.items())[-3:]  # Last 3 queries
            recent_query_summaries = [f"{qid[:8]}...({data['status']})" for qid, data in recent_queries]
            context_parts.append(f"Recent queries: {recent_query_summaries}")
        
        # Pending results
        if self.conversation_context["pending_results"]:
            context_parts.append(f"Pending results: {len(self.conversation_context['pending_results'])} queries awaiting completion")
        
        # Available templates (if recently checked)
        if self.conversation_context["recent_templates"]:
            ready_count = len([t for t in self.conversation_context["recent_templates"] if t.get("status") == "READY"])
            context_parts.append(f"Available templates: {ready_count} ready for execution")
        
        return " | ".join(context_parts) if context_parts else "New conversation"
    
    @with_circuit_breaker(openai_circuit_breaker)
    async def _llm_powered_processing(self, user_input: str) -> str:
        """Process request using LLM for intent understanding and tool orchestration."""
        
        # Get current conversation context
        context_summary = self._get_context_summary()
        
        # Enhanced system prompt with REAL cleanroom context and intelligent response patterns
        system_prompt = """You are an expert Habu Clean Room Data Collaboration Assistant powered by OpenAI GPT-4. You help enterprises manage privacy-safe data partnerships and advanced analytics.

🧠 **CONVERSATION CONTEXT**: """ + context_summary + """

🏢 HABU CLEAN ROOM PLATFORM OVERVIEW:
Habu enables secure data collaboration between companies without exposing raw data. Partners can run joint analytics while maintaining privacy through cryptographic clean rooms.

🔧 AVAILABLE API TOOLS:
1. habu_list_partners - View your data collaboration partners
2. habu_enhanced_templates - Browse advanced analytics templates with rich metadata (categories, parameters, data types, status)  
3. habu_submit_query - Execute sophisticated analytics with partner data
4. habu_check_status - Monitor query progress (building, running, completed)
5. habu_get_results - Retrieve insights with business intelligence summaries
6. habu_list_exports - Browse completed analysis exports and download ready results
7. habu_download_export - Download specific export files with full dataset access

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
- **Last Query**: """ + (self.last_query_id or 'None') + """

🤖 INTERACTIVE QUERY BUILDING - PHASE 3:
When users want to run analytics, provide intelligent query suggestions and execute them:

**REAL TEMPLATE IDs FOR EXECUTION:**
- Sentiment Analysis (READY): f7b6c1b5-c625-40e5-9209-b4a1ca7d3c7a
- Location Data (READY): 10cefd5c-b2fe-451a-a4cf-12546dbb6b28  
- Pattern of Life (READY): d827dfd1-3acf-41fb-bd8f-e18ecf74473e
- Sentiment Analysis (MISSING_DATASETS): 1c622093-b55b-4a57-9c95-d2ab7d0cdb89

**RESPONSE FORMAT:**
For tool actions, respond with JSON formatted exactly as shown:
Action format: {"action": "tool_name", "tool_params": {"param": "value"}, "explanation": "Business explanation"}

**INTERACTIVE QUERY EXAMPLES:**
User: "Run a sentiment analysis" -> Use habu_submit_query with template f7b6c1b5-c625-40e5-9209-b4a1ca7d3c7a
User: "Analyze location patterns" -> Use habu_submit_query with template 10cefd5c-b2fe-451a-a4cf-12546dbb6b28  
User: "Show me exports" -> Use habu_list_exports
User: "Download export ABC123" -> Use habu_download_export with export_id ABC123

User: "Run combined location analysis"  
Response: {"action": "habu_submit_query", "tool_params": {"template_id": "d827dfd1-3acf-41fb-bd8f-e18ecf74473e", "parameters": {}, "query_name": "Combined Location Intelligence"}, "explanation": "I'll execute the TimberMac and Geotrace combined analysis for comprehensive location intelligence."}

User: "Check my query status" or "How is my analysis going?"
Response: {"action": "habu_check_status", "tool_params": {"query_id": "last"}, "explanation": "I'll check the progress of your most recent query."}

User: "Show me the results" or "Get my analysis results"
Response: {"action": "habu_get_results", "tool_params": {"query_id": "last"}, "explanation": "I'll retrieve the results from your completed analysis."}

**INTELLIGENT QUERY SUGGESTIONS:**
- For sentiment questions → Suggest sentiment analysis execution
- For location questions → Suggest location/pattern analysis  
- For "what can I run" → Offer specific executable queries
- For status questions → Check query progress
- For results questions → Retrieve analysis results

**IMPORTANT EXECUTION RULES:**
- Only suggest READY templates (not MISSING_DATASETS)
- Always include descriptive query names
- Provide business context for each analysis type
- Guide users through the complete workflow from execution to results
"""

        try:
            # Create the conversation with GPT-4
            response = await self.client.chat.completions.create(
                model="gpt-4o",  # Using GPT-4 Omni model
                max_tokens=1000,
                messages=[
                    {
                        "role": "system", 
                        "content": system_prompt
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
                result = await habu_enhanced_templates()
                return self._format_llm_response(explanation, result, "enhanced_templates")
                
            elif action == "habu_submit_query":
                template_id = tool_params.get("template_id")
                parameters = tool_params.get("parameters", {})
                query_name = tool_params.get("query_name", "Analytics Query")
                
                if not template_id:
                    return "I need a template ID to submit a query. Please specify which template you'd like to use."
                
                # Execute the actual query submission
                result = await habu_submit_query(template_id, parameters, query_name)
                
                # Parse the result to update context
                try:
                    result_data = json.loads(result)
                    if result_data.get("status") == "success":
                        query_id = result_data.get("query_id")
                        if query_id:
                            self.last_query_id = query_id
                            # Update enhanced context tracking
                            self._update_query_context(
                                query_id=query_id,
                                template_id=template_id,
                                status=result_data.get("query_status", "SUBMITTED"),
                                query_name=query_name
                            )
                except Exception as e:
                    logger.error(f"Error updating query context: {e}")
                
                return self._format_llm_response(explanation, result, "submit")
                
            elif action == "habu_check_status":
                query_id = tool_params.get("query_id")
                if query_id == "last" or not query_id:
                    query_id = self.last_query_id
                if not query_id:
                    # Check if we have any pending queries in context
                    if self.conversation_context["pending_results"]:
                        query_id = self.conversation_context["pending_results"][0]
                    else:
                        return "I don't have a query ID to check. Please provide a query ID or submit a query first."
                
                # Execute the actual status check
                result = await habu_check_status(query_id)
                
                # Parse result to update context
                try:
                    result_data = json.loads(result)
                    if result_data.get("status") == "success":
                        new_status = result_data.get("query_status")
                        if query_id in self.active_queries and new_status:
                            self.active_queries[query_id]["status"] = new_status
                            self.active_queries[query_id]["last_checked"] = "now"
                            
                            # Update pending results list
                            if new_status.lower() in ["completed", "success", "finished"]:
                                if query_id in self.conversation_context["pending_results"]:
                                    self.conversation_context["pending_results"].remove(query_id)
                except Exception as e:
                    logger.error(f"Error updating status context: {e}")
                
                return self._format_llm_response(explanation, result, "status")
                
            elif action == "habu_get_results":
                query_id = tool_params.get("query_id")
                if query_id == "last" or not query_id:
                    query_id = self.last_query_id
                if not query_id:
                    return "I don't have a query ID to get results for. Please provide a query ID or submit a query first."
                
                # Execute the actual results retrieval
                result = await habu_get_results(query_id)
                
                # Parse result to update context
                try:
                    result_data = json.loads(result)
                    if result_data.get("status") == "success":
                        # Query completed successfully - remove from pending
                        if query_id in self.conversation_context["pending_results"]:
                            self.conversation_context["pending_results"].remove(query_id)
                        
                        # Update query context with completion
                        if query_id in self.active_queries:
                            self.active_queries[query_id]["status"] = "COMPLETED"
                            self.active_queries[query_id]["results_retrieved"] = True
                            
                except Exception as e:
                    logger.error(f"Error updating results context: {e}")
                
                return self._format_llm_response(explanation, result, "results")
                
            elif action == "habu_list_exports":
                status_filter = tool_params.get("status_filter")
                result = await habu_list_exports(status_filter)
                return self._format_llm_response(explanation, result, "exports")
                
            elif action == "habu_download_export":
                export_id = tool_params.get("export_id")
                if not export_id:
                    return "I need an export ID to download. Please check available exports first."
                
                result = await habu_download_export(export_id)
                return self._format_llm_response(explanation, result, "download")
                
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
                        
            elif result_type == "templates" or result_type == "enhanced_templates":
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
                            question_type = t.get("questionType", "")
                            data_types = t.get("dataTypes", {})
                            parameters = t.get("parameters", {})
                            
                            # Enhanced template information
                            enhanced_info = []
                            if question_type:
                                enhanced_info.append(f"Type: {question_type}")
                            
                            # Handle data types (can be dict or list depending on source)
                            if data_types:
                                if isinstance(data_types, dict):
                                    data_type_names = list(data_types.keys())[:2]
                                elif isinstance(data_types, list):
                                    data_type_names = data_types[:2]
                                else:
                                    data_type_names = [str(data_types)]
                                
                                if data_type_names:
                                    enhanced_info.append(f"Data: {', '.join(data_type_names)}")
                            
                            # Handle parameters
                            if parameters:
                                if isinstance(parameters, dict) and len(parameters) > 0:
                                    # Show specific parameter info
                                    required = parameters.get('required', [])
                                    optional = parameters.get('optional', [])
                                    if required or optional:
                                        param_info = f"Required: {len(required) if required else 0}"
                                        if optional:
                                            param_info += f", Optional: {len(optional)}"
                                        enhanced_info.append(f"Parameters: {param_info}")
                                    else:
                                        # If parameters is just a dict of values
                                        enhanced_info.append(f"Parameters: {len(parameters)} fields")
                            
                            enhanced_suffix = f" | {' | '.join(enhanced_info)}" if enhanced_info else ""
                            
                            if status == "READY":
                                ready_templates.append(f"✅ **{name}**\n   Category: {category}{enhanced_suffix} | Status: Ready for execution")
                            elif status == "MISSING_DATASETS":
                                missing_data_templates.append(f"⚠️ **{name}**\n   Category: {category}{enhanced_suffix} | Status: Needs dataset configuration")
                            else:
                                ready_templates.append(f"• **{name}**\n   Category: {category}{enhanced_suffix} | Status: {status}")
                        
                        # Add enhanced metadata summary
                        total_count = result_data.get("count", len(templates))
                        categories = result_data.get("categories", [])
                        question_types = result_data.get("question_types", [])
                        
                        response = f"{explanation}\n\n🔥 **Your Analytics Templates** ({total_count} total)"
                        if categories:
                            response += f"\n📊 **Categories**: {', '.join(categories)}"
                        if question_types:
                            response += f"\n🎯 **Types**: {', '.join(question_types)}"
                        response += "\n\n"
                        
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
                    template_id = result_data.get("template_id", "")
                    
                    # Enhanced submission response with next steps
                    response = f"{explanation}\n\n🚀 **Query Executed Successfully!**\n"
                    response += f"📋 **Query ID**: {query_id}\n"
                    response += f"⚡ **Status**: {status.upper()}\n"
                    
                    # Add template-specific success messaging
                    if "f7b6c1b5" in template_id:
                        response += f"📊 **Analysis Type**: Sentiment Analysis (Global Events & Language Tone)\n"
                        response += f"🎯 **Insights**: You'll get sentiment patterns and emotional tone analysis\n"
                    elif "10cefd5c" in template_id:
                        response += f"📍 **Analysis Type**: Mobile Location Pattern of Life\n" 
                        response += f"🎯 **Insights**: You'll get mobility patterns and behavioral insights\n"
                    elif "d827dfd1" in template_id:
                        response += f"🌐 **Analysis Type**: Combined Location Intelligence\n"
                        response += f"🎯 **Insights**: You'll get comprehensive location and behavioral analysis\n"
                    
                    response += f"\n💡 **Next Steps**:\n"
                    response += f"• Ask 'Check my query status' to monitor progress\n"
                    response += f"• Once complete, ask 'Show me the results' to get insights\n"
                    response += f"• Query typically takes 2-10 minutes depending on data complexity"
                    
                    return response
                    
            elif result_type == "status":
                if result_data.get("status") == "success":
                    query_status = result_data.get("query_status", "unknown").upper()
                    progress = result_data.get("progress_percent", 0)
                    query_id = result_data.get("query_id", "unknown")
                    
                    response = f"{explanation}\n\n📊 **Query Status Update**\n"
                    response += f"🆔 **Query ID**: {query_id}\n"
                    response += f"⚡ **Status**: {query_status}"
                    
                    if progress > 0:
                        response += f" ({progress}% complete)"
                    
                    # Status-specific guidance
                    if query_status in ["SUBMITTED", "QUEUED", "RUNNING"]:
                        response += f"\n\n⏳ **In Progress**: Your analysis is being processed. Check back in a few minutes."
                    elif query_status == "COMPLETED":
                        response += f"\n\n✅ **Complete**: Your analysis is ready! Ask 'Show me the results' to get insights."
                    elif query_status == "FAILED":
                        response += f"\n\n❌ **Failed**: There was an issue with your analysis. Please try again or contact support."
                    
                    return response
                    
            elif result_type == "results":
                if result_data.get("status") == "success":
                    summary = result_data.get("business_summary", "Results available")
                    count = result_data.get("record_count", 0)
                    query_id = result_data.get("query_id", "unknown")
                    
                    response = f"{explanation}\n\n🎯 **Analysis Results**\n"
                    response += f"🆔 **Query ID**: {query_id}\n"
                    response += f"📊 **Summary**: {summary}\n"
                    response += f"📈 **Data Points**: {count:,} records analyzed\n"
                    
                    # Add actionable insights
                    response += f"\n💡 **Key Insights**:\n"
                    response += f"• Analysis completed successfully with comprehensive data coverage\n"
                    response += f"• {count:,} data points processed for robust statistical significance\n"
                    response += f"• Results ready for business decision-making and strategic planning\n"
                    
                    response += f"\n🚀 **Next Steps**:\n"
                    response += f"• Review the detailed findings above\n"
                    response += f"• Run additional analyses with different templates\n" 
                    response += f"• Export results for presentation to stakeholders"
                    
                    return response
                    
            elif result_type == "exports":
                if result_data.get("status") == "success":
                    ready_exports = result_data.get("ready_exports", [])
                    processing_exports = result_data.get("processing_exports", [])
                    total_exports = result_data.get("total_exports", 0)
                    
                    response = f"{explanation}\n\n📁 **Your Analysis Exports**\n"
                    
                    if ready_exports:
                        response += f"\n✅ **Ready for Download** ({len(ready_exports)} exports):\n"
                        for export in ready_exports[:5]:  # Show max 5
                            name = export.get("name", "Unknown")
                            size_mb = export.get("file_size", 0) / (1024*1024)
                            records = export.get("record_count", 0)
                            created = export.get("created_at", "")[:10]  # Just date
                            response += f"• **{name}**\n"
                            response += f"  📊 {records:,} records | 💾 {size_mb:.1f} MB | 📅 {created}\n"
                            response += f"  🆔 Export ID: `{export.get('id', 'unknown')}`\n\n"
                        
                        if len(ready_exports) > 5:
                            response += f"... and {len(ready_exports) - 5} more exports available\n\n"
                    
                    if processing_exports:
                        response += f"⏳ **Currently Processing** ({len(processing_exports)} exports):\n"
                        for export in processing_exports[:3]:  # Show max 3
                            name = export.get("name", "Unknown") 
                            progress = export.get("progress_percent", 0)
                            response += f"• **{name}** - {progress}% complete\n"
                    
                    if not ready_exports and not processing_exports:
                        response += "\n📝 No exports available yet. Run some analytics queries to generate downloadable results!\n"
                    
                    response += f"\n💡 **Export Management**:\n"
                    response += f"• Ask 'Download export [ID]' to get specific analysis results\n"
                    response += f"• Each export contains full datasets with rich metadata\n"
                    response += f"• Files are available in CSV format for easy analysis\n"
                    
                    if ready_exports:
                        response += f"• Total ready data: {sum(e.get('file_size', 0) for e in ready_exports) / (1024*1024):.1f} MB"
                    
                    return response
                    
            elif result_type == "download":
                if result_data.get("status") == "success":
                    file_name = result_data.get("file_name", "export.csv")
                    file_size = result_data.get("file_size", 0)
                    records = result_data.get("record_count", 0)
                    preview = result_data.get("preview", {})
                    
                    response = f"{explanation}\n\n📥 **Export Downloaded Successfully**\n"
                    response += f"📄 **File**: {file_name}\n"
                    response += f"📊 **Data**: {records:,} records ({file_size:,} bytes)\n"
                    
                    if preview:
                        response += f"\n🔍 **Data Preview**:\n"
                        columns = preview.get("columns", [])
                        response += f"**Columns**: {', '.join(columns[:5])}"
                        if len(columns) > 5:
                            response += f" (and {len(columns) - 5} more)"
                        response += f"\n**Total Columns**: {preview.get('total_columns', len(columns))}\n"
                        
                        sample_rows = preview.get("sample_rows", [])
                        if sample_rows:
                            response += f"\n**Sample Data**:\n"
                            for i, row in enumerate(sample_rows[:3]):
                                response += f"Row {i+1}: {dict(zip(columns[:3], row[:3]))}\n"
                    
                    response += f"\n💡 **Analysis Ready**: Your complete dataset is now available for:\n"
                    response += f"• Business intelligence and reporting\n"
                    response += f"• Advanced analytics and modeling\n"
                    response += f"• Integration with your data pipeline\n"
                    response += f"• Stakeholder presentations and insights"
                    
                    return response
            
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
            result = await habu_enhanced_templates()
            result_data = json.loads(result)
            if result_data["status"] == "success" and result_data["templates"]:
                templates = []
                for t in result_data["templates"]:
                    name = t.get('name', 'Unknown')
                    category = t.get('category', 'General')
                    status = t.get('status', 'Unknown')
                    templates.append(f"• {name} ({category}) - {status}")
                
                categories = result_data.get("categories", [])
                cat_info = f"\n\nCategories: {', '.join(categories)}" if categories else ""
                
                return f"Available enhanced query templates:\n" + "\n".join(templates) + cat_info
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