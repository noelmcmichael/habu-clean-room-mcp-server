"""
Enhanced Habu Templates Tool
Uses the /cleanrooms/{cleanroom_id}/cleanroom-questions endpoint for richer template data
"""
import httpx
import json
import os
from typing import List, Dict, Any
from config.habu_config import habu_config
from tools.mock_data import mock_data

async def habu_enhanced_templates(cleanroom_id: str = None) -> str:
    """
    Lists all available clean room questions (templates) with enhanced metadata
    from the Habu API using the /cleanroom-questions endpoint.
    
    Args:
        cleanroom_id: Specific cleanroom to get templates for. If None, uses default.
    
    Returns:
        str: JSON string containing enhanced template information
    """
    # Check if mock mode is enabled
    use_mock = os.getenv("HABU_USE_MOCK_DATA", "false").lower() == "true"
    
    if use_mock:
        templates = mock_data.get_mock_templates()
        # Enhance mock data with additional fields that real API provides
        enhanced_templates = []
        for template in templates:
            enhanced_template = {
                **template,
                "displayId": f"CRQ-{template['id'][:6]}",
                "questionType": "ANALYTICAL",
                "category": "Data Analysis",
                "createdOn": "2024-01-01T00:00:00Z",
                "status": "ACTIVE",
                "dataTypes": ["string", "number", "date"],
                "parameters": {
                    "required": ["date_range", "metric"],
                    "optional": ["segment", "filter"]
                },
                "dimension": "standard"
            }
            enhanced_templates.append(enhanced_template)
            
        return json.dumps({
            "status": "success",
            "count": len(enhanced_templates),
            "templates": enhanced_templates,
            "summary": f"Found {len(enhanced_templates)} enhanced query templates with detailed metadata (MOCK MODE)",
            "categories": list(set(t.get('category', 'general') for t in enhanced_templates)),
            "question_types": list(set(t.get('questionType', 'unknown') for t in enhanced_templates)),
            "mock_mode": True
        }, indent=2)
    
    try:
        headers = await habu_config.get_auth_headers()
        
        async with httpx.AsyncClient() as client:
            # If no cleanroom_id provided, get the first available cleanroom
            if not cleanroom_id:
                cleanrooms_response = await client.get(
                    f"{habu_config.base_url}/cleanrooms",
                    headers=headers,
                    timeout=30.0
                )
                
                if cleanrooms_response.status_code == 401:
                    habu_config.reset_token()
                    headers = await habu_config.get_auth_headers()
                    cleanrooms_response = await client.get(
                        f"{habu_config.base_url}/cleanrooms",
                        headers=headers,
                        timeout=30.0
                    )
                
                cleanrooms_response.raise_for_status()
                cleanrooms_data = cleanrooms_response.json()
                
                if isinstance(cleanrooms_data, list) and cleanrooms_data:
                    cleanroom_id = cleanrooms_data[0].get("id")
                else:
                    return json.dumps({
                        "status": "error",
                        "error": "No cleanrooms available",
                        "summary": "No cleanrooms found to retrieve templates from"
                    })
            
            # Get enhanced templates using the cleanroom-questions endpoint
            response = await client.get(
                f"{habu_config.base_url}/cleanrooms/{cleanroom_id}/cleanroom-questions",
                headers=headers,
                timeout=30.0
            )
            
            if response.status_code == 401:
                habu_config.reset_token()
                headers = await habu_config.get_auth_headers()
                response = await client.get(
                    f"{habu_config.base_url}/cleanrooms/{cleanroom_id}/cleanroom-questions",
                    headers=headers,
                    timeout=30.0
                )
            
            response.raise_for_status()
            templates_data = response.json()
            
            # Process and structure the enhanced template data
            enhanced_templates = []
            categories = set()
            question_types = set()
            
            if isinstance(templates_data, list):
                for template in templates_data:
                    # Extract and structure the enhanced fields
                    enhanced_template = {
                        "id": template.get("id"),
                        "name": template.get("name"),
                        "displayId": template.get("displayId"),
                        "description": template.get("description", ""),
                        "category": template.get("category", "general"),
                        "questionType": template.get("questionType", "unknown"),
                        "status": template.get("status"),
                        "createdOn": template.get("createdOn"),
                        "dataTypes": template.get("dataTypes", []),
                        "parameters": template.get("parameters", {}),
                        "dimension": template.get("dimension"),
                        "cleanroom_id": cleanroom_id,
                        # Additional computed fields for better LLM understanding
                        "is_active": template.get("status") == "ACTIVE",
                        "parameter_count": len(template.get("parameters", {})),
                        "supported_data_types": len(template.get("dataTypes", [])),
                    }
                    
                    enhanced_templates.append(enhanced_template)
                    categories.add(template.get("category", "general"))
                    question_types.add(template.get("questionType", "unknown"))
            
            # Create enhanced summary with business intelligence
            summary_data = {
                "status": "success",
                "count": len(enhanced_templates),
                "templates": enhanced_templates,
                "summary": f"Found {len(enhanced_templates)} enhanced query templates with detailed metadata",
                "categories": list(categories),
                "question_types": list(question_types),
                "cleanroom_id": cleanroom_id,
                "active_templates": len([t for t in enhanced_templates if t.get("is_active")]),
                "enhancement_features": {
                    "parameter_metadata": True,
                    "data_type_specifications": True,
                    "categorization": True,
                    "status_tracking": True,
                    "display_ids": True
                }
            }
            
            return json.dumps(summary_data, indent=2)
            
    except httpx.HTTPStatusError as e:
        error_msg = f"HTTP error {e.response.status_code}: {e.response.text}"
        return json.dumps({
            "status": "error",
            "error": error_msg,
            "summary": f"Failed to retrieve enhanced templates from Habu API: {error_msg}",
            "cleanroom_id": cleanroom_id
        })
    except Exception as e:
        error_msg = str(e)
        return json.dumps({
            "status": "error",
            "error": error_msg,
            "summary": f"An error occurred while fetching enhanced templates: {error_msg}",
            "cleanroom_id": cleanroom_id
        })

# Backward compatibility function
async def habu_list_templates() -> str:
    """
    Backward compatibility wrapper for the enhanced templates function.
    This maintains compatibility with existing code while providing enhanced data.
    """
    return await habu_enhanced_templates()