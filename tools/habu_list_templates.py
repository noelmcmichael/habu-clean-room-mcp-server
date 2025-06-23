"""
Habu List Templates Tool
Returns available clean room questions (templates) from the Habu API
"""
import httpx
import json
import os
from typing import List, Dict, Any
from config.habu_config import habu_config
from tools.mock_data import mock_data

async def habu_list_templates() -> str:
    """
    Lists all available clean room questions (templates) from the Habu API.
    
    Returns:
        str: JSON string containing template information
    """
    # Check if mock mode is enabled
    use_mock = os.getenv("HABU_USE_MOCK_DATA", "false").lower() == "true"
    
    if use_mock:
        templates = mock_data.get_mock_templates()
        return json.dumps({
            "status": "success",
            "count": len(templates),
            "templates": templates,
            "summary": f"Found {len(templates)} query templates available for analysis (MOCK MODE)",
            "mock_mode": True
        }, indent=2)
    
    try:
        headers = await habu_config.get_auth_headers()
        
        async with httpx.AsyncClient() as client:
            # First get cleanrooms, then get questions for each cleanroom
            response = await client.get(
                f"{habu_config.base_url}/cleanrooms",
                headers=headers,
                timeout=30.0
            )
            
            if response.status_code == 401:
                # Token might be expired, reset and retry
                habu_config.reset_token()
                headers = await habu_config.get_auth_headers()
                response = await client.get(
                    f"{habu_config.base_url}/cleanrooms",
                    headers=headers,
                    timeout=30.0
                )
            
            response.raise_for_status()
            cleanrooms_data = response.json()
            
            # Get all questions from all cleanrooms
            all_templates = []
            
            if isinstance(cleanrooms_data, list):
                for cleanroom in cleanrooms_data:
                    cleanroom_id = cleanroom.get("id")
                    if cleanroom_id:
                        # Get questions for this cleanroom
                        questions_response = await client.get(
                            f"{habu_config.base_url}/cleanrooms/{cleanroom_id}/cleanroom-questions",
                            headers=headers,
                            timeout=30.0
                        )
                        if questions_response.status_code == 200:
                            questions_data = questions_response.json()
                            if isinstance(questions_data, list):
                                for question in questions_data:
                                    template_summary = {
                                        "id": question.get("id"),
                                        "name": question.get("name"),
                                        "description": question.get("description", ""),
                                        "category": question.get("category", "general"),
                                        "question_type": question.get("questionType", "unknown"),
                                        "cleanroom_id": cleanroom_id,
                                        "cleanroom_name": cleanroom.get("name", "Unknown"),
                                        "status": question.get("status"),
                                        "created_on": question.get("createdOn")
                                    }
                                    all_templates.append(template_summary)
            
            # Create a structured summary for the LLM agent
            if all_templates:
                categories = set(t.get('category', 'general') for t in all_templates)
                summary = {
                    "status": "success",
                    "count": len(all_templates),
                    "templates": all_templates,
                    "summary": f"Found {len(all_templates)} query templates across {len(cleanrooms_data) if isinstance(cleanrooms_data, list) else 0} cleanrooms. Categories: {', '.join(categories)}"
                }
            else:
                summary = {
                    "status": "success",
                    "count": 0,
                    "templates": [],
                    "summary": f"No query templates found. You have {len(cleanrooms_data) if isinstance(cleanrooms_data, list) else 0} cleanrooms available."
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