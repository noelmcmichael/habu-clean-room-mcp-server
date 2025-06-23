"""
Habu List Templates Tool
Returns available clean room query templates from the Habu API
"""
import httpx
import json
from typing import List, Dict, Any
from config.habu_config import habu_config

async def habu_list_templates() -> str:
    """
    Lists all available clean room query templates from the Habu API.
    
    Returns:
        str: JSON string containing template information
    """
    try:
        headers = await habu_config.get_auth_headers()
        
        async with httpx.AsyncClient() as client:
            # Using the Habu API endpoint for listing query templates
            response = await client.get(
                f"{habu_config.base_url}/templates",
                headers=headers,
                timeout=30.0
            )
            
            if response.status_code == 401:
                # Token might be expired, reset and retry
                habu_config.reset_token()
                headers = await habu_config.get_auth_headers()
                response = await client.get(
                    f"{habu_config.base_url}/templates",
                    headers=headers,
                    timeout=30.0
                )
            
            response.raise_for_status()
            templates_data = response.json()
            
            # Format the response for better readability
            if isinstance(templates_data, dict) and "templates" in templates_data:
                templates = templates_data["templates"]
            elif isinstance(templates_data, list):
                templates = templates_data
            else:
                templates = templates_data
            
            # Create a structured summary for the LLM agent
            if templates:
                template_summaries = []
                for template in (templates if isinstance(templates, list) else [templates]):
                    template_summary = {
                        "id": template.get("id"),
                        "name": template.get("name"),
                        "description": template.get("description"),
                        "category": template.get("category", "general"),
                        "parameters": template.get("parameters", [])
                    }
                    template_summaries.append(template_summary)
                
                summary = {
                    "status": "success",
                    "count": len(template_summaries),
                    "templates": template_summaries,
                    "summary": f"Found {len(template_summaries)} query templates. Available categories: {', '.join(set(t.get('category', 'general') for t in template_summaries))}"
                }
            else:
                summary = {
                    "status": "success",
                    "count": 0,
                    "templates": [],
                    "summary": "No query templates are currently available."
                }
            
            return json.dumps(summary, indent=2)
            
    except httpx.HTTPStatusError as e:
        error_msg = f"HTTP error {e.response.status_code}: {e.response.text}"
        return json.dumps({
            "status": "error",
            "error": error_msg,
            "summary": f"Failed to retrieve templates from Habu API: {error_msg}"
        })
    except Exception as e:
        error_msg = str(e)
        return json.dumps({
            "status": "error",
            "error": error_msg,
            "summary": f"An error occurred while fetching templates: {error_msg}"
        })