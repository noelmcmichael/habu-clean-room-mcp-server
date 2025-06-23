"""
Habu List Partners Tool
Returns a list of clean room partners available through the Habu API
"""
import httpx
import json
from typing import List, Dict, Any
from config.habu_config import habu_config

async def habu_list_partners() -> str:
    """
    Lists all available clean room partners from the Habu API.
    
    Returns:
        str: JSON string containing partner information
    """
    try:
        headers = await habu_config.get_auth_headers()
        
        async with httpx.AsyncClient() as client:
            # Using the Habu API endpoint for listing partners
            response = await client.get(
                f"{habu_config.base_url}/partners",
                headers=headers,
                timeout=30.0
            )
            
            if response.status_code == 401:
                # Token might be expired, reset and retry
                habu_config.reset_token()
                headers = await habu_config.get_auth_headers()
                response = await client.get(
                    f"{habu_config.base_url}/partners",
                    headers=headers,
                    timeout=30.0
                )
            
            response.raise_for_status()
            partners_data = response.json()
            
            # Format the response for better readability
            if isinstance(partners_data, dict) and "partners" in partners_data:
                partners = partners_data["partners"]
            elif isinstance(partners_data, list):
                partners = partners_data
            else:
                partners = partners_data
            
            # Create a summary for the LLM agent
            if partners:
                summary = {
                    "status": "success",
                    "count": len(partners) if isinstance(partners, list) else 1,
                    "partners": partners,
                    "summary": f"Found {len(partners) if isinstance(partners, list) else 1} clean room partners available for collaboration."
                }
            else:
                summary = {
                    "status": "success",
                    "count": 0,
                    "partners": [],
                    "summary": "No clean room partners are currently available."
                }
            
            return json.dumps(summary, indent=2)
            
    except httpx.HTTPStatusError as e:
        error_msg = f"HTTP error {e.response.status_code}: {e.response.text}"
        return json.dumps({
            "status": "error",
            "error": error_msg,
            "summary": f"Failed to retrieve partners from Habu API: {error_msg}"
        })
    except Exception as e:
        error_msg = str(e)
        return json.dumps({
            "status": "error", 
            "error": error_msg,
            "summary": f"An error occurred while fetching partners: {error_msg}"
        })