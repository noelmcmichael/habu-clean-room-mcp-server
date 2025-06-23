"""
Habu Submit Query Tool
Submits a clean room query using a template ID and parameters
"""
import httpx
import json
from typing import Dict, Any, Optional
from config.habu_config import habu_config

async def habu_submit_query(template_id: str, parameters: Dict[str, Any], query_name: Optional[str] = None) -> str:
    """
    Submits a clean room query to the Habu API using a template.
    
    Args:
        template_id (str): The ID of the query template to use
        parameters (Dict[str, Any]): Parameters required by the template
        query_name (str, optional): Custom name for the query
    
    Returns:
        str: JSON string containing query submission result and query ID
    """
    try:
        headers = await habu_config.get_auth_headers()
        
        # Prepare the query payload
        query_payload = {
            "template_id": template_id,
            "parameters": parameters
        }
        
        if query_name:
            query_payload["name"] = query_name
        
        async with httpx.AsyncClient() as client:
            # Submit the query to the Habu API
            response = await client.post(
                f"{habu_config.base_url}/queries",
                headers=headers,
                json=query_payload,
                timeout=30.0
            )
            
            if response.status_code == 401:
                # Token might be expired, reset and retry
                habu_config.reset_token()
                headers = await habu_config.get_auth_headers()
                response = await client.post(
                    f"{habu_config.base_url}/queries",
                    headers=headers,
                    json=query_payload,
                    timeout=30.0
                )
            
            response.raise_for_status()
            query_result = response.json()
            
            # Extract key information from the response
            query_id = query_result.get("query_id") or query_result.get("id")
            status = query_result.get("status", "submitted")
            
            summary = {
                "status": "success",
                "query_id": query_id,
                "query_status": status,
                "template_id": template_id,
                "parameters_used": parameters,
                "submission_result": query_result,
                "summary": f"Query successfully submitted with ID: {query_id}. Status: {status}. Use habu_check_status to monitor progress."
            }
            
            return json.dumps(summary, indent=2)
            
    except httpx.HTTPStatusError as e:
        error_msg = f"HTTP error {e.response.status_code}: {e.response.text}"
        return json.dumps({
            "status": "error",
            "error": error_msg,
            "template_id": template_id,
            "parameters": parameters,
            "summary": f"Failed to submit query: {error_msg}"
        })
    except Exception as e:
        error_msg = str(e)
        return json.dumps({
            "status": "error",
            "error": error_msg,
            "template_id": template_id,
            "parameters": parameters,
            "summary": f"An error occurred while submitting query: {error_msg}"
        })