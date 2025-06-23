"""
Habu Chat Agent
LLM-driven agent for intelligent interaction with Habu Clean Room API
Orchestrates tool calls and provides conversational interface
"""
import json
import re
from typing import Dict, Any, List, Optional, Tuple
from tools.habu_list_partners import habu_list_partners
from tools.habu_list_templates import habu_list_templates
from tools.habu_submit_query import habu_submit_query
from tools.habu_check_status import habu_check_status
from tools.habu_get_results import habu_get_results

class HabuChatAgent:
    """
    Intelligent agent for processing natural language requests
    and orchestrating Habu API tool calls.
    """
    
    def __init__(self):
        self.last_query_id: Optional[str] = None
        self.context_memory: Dict[str, Any] = {}
        
    async def process_request(self, user_input: str) -> str:
        """
        Process a natural language request and orchestrate appropriate tool calls.
        
        Args:
            user_input (str): User's natural language request
            
        Returns:
            str: Formatted response with results and next steps
        """
        try:
            # Parse intent from user input
            intent, entities = self._parse_intent(user_input.lower())
            
            # Route to appropriate workflow
            if intent == "list_partners":
                return await self._handle_list_partners()
            elif intent == "list_templates":
                return await self._handle_list_templates()
            elif intent == "submit_query":
                return await self._handle_submit_query(entities)
            elif intent == "check_status":
                return await self._handle_check_status(entities)
            elif intent == "get_results":
                return await self._handle_get_results(entities)
            elif intent == "full_workflow":
                return await self._handle_full_workflow(entities)
            else:
                return self._handle_unknown_intent(user_input)
                
        except Exception as e:
            return f"I encountered an error processing your request: {str(e)}. Please try rephrasing your request or contact support."
    
    def _parse_intent(self, user_input: str) -> Tuple[str, Dict[str, Any]]:
        """
        Parse user intent and extract entities from natural language input.
        
        Args:
            user_input (str): Lowercase user input
            
        Returns:
            Tuple[str, Dict[str, Any]]: Intent and extracted entities
        """
        entities = {}
        
        # Intent patterns
        if any(phrase in user_input for phrase in ["list partners", "show partners", "what partners", "available partners", "my clean room partners", "list my partners"]):
            return "list_partners", entities
            
        if any(phrase in user_input for phrase in ["list templates", "show templates", "what templates", "available templates", "templates are available", "query templates"]):
            return "list_templates", entities
            
        if any(phrase in user_input for phrase in ["check status", "query status", "how is", "progress"]):
            # Extract query ID if mentioned
            query_id_match = re.search(r'query[_\s]*id[_\s]*:?[_\s]*([a-zA-Z0-9\-]+)', user_input)
            if query_id_match:
                entities["query_id"] = query_id_match.group(1)
            elif self.last_query_id:
                entities["query_id"] = self.last_query_id
            return "check_status", entities
            
        if any(phrase in user_input for phrase in ["get results", "show results", "results", "what were the results"]):
            # Extract query ID if mentioned
            query_id_match = re.search(r'query[_\s]*id[_\s]*:?[_\s]*([a-zA-Z0-9\-]+)', user_input)
            if query_id_match:
                entities["query_id"] = query_id_match.group(1)
            elif self.last_query_id:
                entities["query_id"] = self.last_query_id
            return "get_results", entities
        
        # Full workflow patterns (run analysis, overlap analysis, etc.)
        if any(phrase in user_input for phrase in ["run", "analyze", "analysis", "overlap", "audience overlap", "execute query"]):
            # Extract partner names
            partners = self._extract_partners(user_input)
            if partners:
                entities["partners"] = partners
            
            # Extract template hints
            if "overlap" in user_input:
                entities["template_hint"] = "overlap"
            elif "audience" in user_input:
                entities["template_hint"] = "audience"
                
            return "full_workflow", entities
        
        # Direct query submission
        if any(phrase in user_input for phrase in ["submit query", "run query", "execute template"]):
            # Extract template ID
            template_id_match = re.search(r'template[_\s]*id[_\s]*:?[_\s]*([a-zA-Z0-9\-]+)', user_input)
            if template_id_match:
                entities["template_id"] = template_id_match.group(1)
            return "submit_query", entities
        
        return "unknown", entities
    
    def _extract_partners(self, user_input: str) -> List[str]:
        """Extract partner names from user input."""
        # Common partner name patterns
        partner_patterns = [
            r'\b(meta|facebook)\b',
            r'\b(amazon|aws)\b',
            r'\b(google|gcp)\b',
            r'\b(microsoft|azure)\b',
            r'\b(apple)\b',
            r'\b(netflix)\b',
            r'\b(spotify)\b',
            r'\b(uber)\b',
            r'\b(airbnb)\b'
        ]
        
        partners = []
        for pattern in partner_patterns:
            matches = re.findall(pattern, user_input, re.IGNORECASE)
            partners.extend([match.title() for match in matches])
        
        return list(set(partners))  # Remove duplicates
    
    async def _handle_list_partners(self) -> str:
        """Handle partner listing request."""
        result = await habu_list_partners()
        result_data = json.loads(result)
        
        if result_data["status"] == "success":
            partners = result_data.get("partners", [])
            if partners:
                partner_list = "\n".join([f"• {partner.get('name', 'Unknown')}" for partner in partners])
                return f"Here are your available clean room partners:\n\n{partner_list}\n\nYou can run analyses with any of these partners. Just let me know what type of analysis you'd like to perform!"
            else:
                return "No clean room partners are currently available. Please contact your administrator to set up partner connections."
        else:
            return f"I couldn't retrieve your partners: {result_data.get('summary', 'Unknown error')}"
    
    async def _handle_list_templates(self) -> str:
        """Handle template listing request."""
        result = await habu_list_templates()
        result_data = json.loads(result)
        
        if result_data["status"] == "success":
            templates = result_data.get("templates", [])
            if templates:
                template_list = []
                for template in templates:
                    name = template.get("name", "Unknown")
                    desc = template.get("description", "No description")
                    template_list.append(f"• **{name}**: {desc}")
                
                template_str = "\n".join(template_list)
                return f"Here are your available query templates:\n\n{template_str}\n\nTo run an analysis, just tell me what you want to analyze and I'll help you choose the right template!"
            else:
                return "No query templates are currently available. Please contact your administrator to set up query templates."
        else:
            return f"I couldn't retrieve your templates: {result_data.get('summary', 'Unknown error')}"
    
    async def _handle_submit_query(self, entities: Dict[str, Any]) -> str:
        """Handle direct query submission."""
        template_id = entities.get("template_id")
        if not template_id:
            return "I need a template ID to submit a query. Please specify the template you'd like to use."
        
        # For now, use empty parameters - this could be enhanced to parse parameters from input
        parameters = entities.get("parameters", {})
        
        result = await habu_submit_query(template_id, parameters)
        result_data = json.loads(result)
        
        if result_data["status"] == "success":
            query_id = result_data["query_id"]
            self.last_query_id = query_id
            return f"Query submitted successfully! Query ID: {query_id}\n\nI'll monitor the progress for you. The query is now {result_data['query_status']}."
        else:
            return f"Failed to submit query: {result_data.get('summary', 'Unknown error')}"
    
    async def _handle_check_status(self, entities: Dict[str, Any]) -> str:
        """Handle status check request."""
        query_id = entities.get("query_id")
        if not query_id:
            return "I need a query ID to check status. Please provide the query ID or run a query first."
        
        result = await habu_check_status(query_id)
        result_data = json.loads(result)
        
        if result_data["status"] == "success":
            status = result_data["query_status"]
            progress = result_data.get("progress_percent", 0)
            next_actions = result_data.get("next_actions", [])
            
            status_msg = f"Query {query_id} is {status}"
            if progress > 0:
                status_msg += f" ({progress}% complete)"
            
            if next_actions:
                status_msg += f"\n\n{next_actions[0]}"
            
            return status_msg
        else:
            return f"Failed to check query status: {result_data.get('summary', 'Unknown error')}"
    
    async def _handle_get_results(self, entities: Dict[str, Any]) -> str:
        """Handle results retrieval request."""
        query_id = entities.get("query_id")
        if not query_id:
            return "I need a query ID to get results. Please provide the query ID or run a query first."
        
        result = await habu_get_results(query_id)
        result_data = json.loads(result)
        
        if result_data["status"] == "success":
            business_summary = result_data.get("business_summary", "Results retrieved successfully")
            record_count = result_data.get("record_count", 0)
            
            return f"Results for query {query_id}:\n\n**Summary**: {business_summary}\n\n**Records**: {record_count} data points retrieved\n\nThe full results are available in the detailed response if you need more specific information."
        else:
            return f"Failed to retrieve results: {result_data.get('summary', 'Unknown error')}"
    
    async def _handle_full_workflow(self, entities: Dict[str, Any]) -> str:
        """Handle complete workflow from partners to results."""
        # This would be a more complex workflow that:
        # 1. Lists partners if needed
        # 2. Finds appropriate template
        # 3. Submits query
        # 4. Monitors status
        # 5. Retrieves results
        
        partners = entities.get("partners", [])
        template_hint = entities.get("template_hint")
        
        workflow_msg = f"I'll help you run a clean room analysis"
        if partners:
            workflow_msg += f" involving {', '.join(partners)}"
        if template_hint:
            workflow_msg += f" focusing on {template_hint}"
        
        workflow_msg += ".\n\nLet me start by checking your available templates and partners..."
        
        # For MVP, guide user through manual steps
        return workflow_msg + "\n\nTo complete this analysis:\n1. First, let me show you available partners with 'list partners'\n2. Then we'll look at templates with 'list templates'\n3. Finally, we'll submit the right query for your analysis"
    
    def _handle_unknown_intent(self, user_input: str) -> str:
        """Handle unknown or unclear requests."""
        return f"""I'm not sure how to help with that request. Here's what I can do:

• **List partners**: "Show me available partners" or "List partners"
• **List templates**: "What templates are available?" or "List templates"  
• **Run analysis**: "Run audience overlap between Meta and Amazon"
• **Check status**: "Check status of query [query_id]" or "How is my last query doing?"
• **Get results**: "Show me the results" or "Get results for query [query_id]"

What would you like to do?"""

# Global agent instance
habu_agent = HabuChatAgent()