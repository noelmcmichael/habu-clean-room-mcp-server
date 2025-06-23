"""
Habu Check Status Tool
Checks the processing status of a previously submitted query
"""
import httpx
import json
import os
from typing import Dict, Any
from config.habu_config import habu_config
from tools.mock_data import mock_data

async def habu_check_status(query_id: str) -> str:
    """
    Checks the processing status of a clean room query.
    
    Args:
        query_id (str): The ID of the query to check
    
    Returns:
        str: JSON string containing query status information
    """
    # Check if mock mode is enabled
    use_mock = os.getenv("HABU_USE_MOCK_DATA", "false").lower() == "true"
    
    if use_mock:
        result = mock_data.check_mock_query_status(query_id)
        return json.dumps(result, indent=2)
    
    try:
        headers = await habu_config.get_auth_headers()
        
        async with httpx.AsyncClient() as client:
            # Check query status via the Habu API
            response = await client.get(
                f"{habu_config.base_url}/queries/{query_id}",
                headers=headers,
                timeout=30.0
            )
            
            if response.status_code == 401:
                # Token might be expired, reset and retry
                habu_config.reset_token()
                headers = await habu_config.get_auth_headers()
                response = await client.get(
                    f"{habu_config.base_url}/queries/{query_id}",
                    headers=headers,
                    timeout=30.0
                )
            
            response.raise_for_status()
            status_data = response.json()
            
            # Extract status information
            status = status_data.get("status", "unknown")
            progress = status_data.get("progress", 0)
            created_at = status_data.get("created_at")
            updated_at = status_data.get("updated_at")
            error_message = status_data.get("error_message")
            
            # Determine next actions based on status
            next_actions = []
            if status.lower() in ["completed", "success", "finished"]:
                next_actions.append("Use habu_get_results to retrieve query results")
            elif status.lower() in ["running", "processing", "in_progress"]:
                next_actions.append("Query is still processing. Check again later.")
            elif status.lower() in ["failed", "error"]:
                next_actions.append("Query failed. Check error details and consider resubmitting.")
            else:
                next_actions.append("Status unclear. Monitor or contact support.")
            
            summary = {
                "status": "success",
                "query_id": query_id,
                "query_status": status,
                "progress_percent": progress,
                "created_at": created_at,
                "updated_at": updated_at,
                "error_message": error_message,
                "full_status_data": status_data,
                "next_actions": next_actions,
                "summary": f"Query {query_id} status: {status} ({progress}% complete). {next_actions[0] if next_actions else ''}"
            }
            
            return json.dumps(summary, indent=2)
            
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            error_msg = f"Query {query_id} not found"
        else:
            error_msg = f"HTTP error {e.response.status_code}: {e.response.text}"
        
        return json.dumps({
            "status": "error",
            "error": error_msg,
            "query_id": query_id,
            "summary": f"Failed to check status for query {query_id}: {error_msg}"
        })
    except Exception as e:
        error_msg = str(e)
        return json.dumps({
            "status": "error",
            "error": error_msg,
            "query_id": query_id,
            "summary": f"An error occurred while checking query status: {error_msg}"
        })