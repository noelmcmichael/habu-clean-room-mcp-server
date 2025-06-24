"""
Habu List Partners Tool
Returns a list of clean room partners available through the Habu API
"""
import httpx
import json
import os
import logging
from typing import List, Dict, Any
from config.habu_config import habu_config
from utils.error_handling import (
    retry_async, 
    format_error_response, 
    APIError, 
    NetworkError,
    habu_api_circuit_breaker,
    with_circuit_breaker
)

logger = logging.getLogger(__name__)

@retry_async(max_retries=3, delay=1.0)
@with_circuit_breaker(habu_api_circuit_breaker)
async def habu_list_partners() -> str:
    """
    Lists all available clean room partners from the Habu API.
    
    Returns:
        str: JSON string containing partner information
    """
    # Check if mock mode is enabled
    
    try:
        logger.info("Fetching partners from Habu API")
        headers = await habu_config.get_auth_headers()
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            # First get cleanrooms, then get partners for each cleanroom
            response = await client.get(
                f"{habu_config.base_url}/cleanrooms",
                headers=headers,
                timeout=30.0
            )
            
            if response.status_code == 401:
                logger.warning("Authentication failed, refreshing token")
                # Token might be expired, reset and retry
                habu_config.reset_token()
                headers = await habu_config.get_auth_headers()
                response = await client.get(
                    f"{habu_config.base_url}/cleanrooms",
                    headers=headers
                )
            
            response.raise_for_status()
            cleanrooms_data = response.json()
            
            # Get all partners from all cleanrooms
            all_partners = []
            
            if isinstance(cleanrooms_data, list):
                for cleanroom in cleanrooms_data:
                    cleanroom_id = cleanroom.get("id")
                    if cleanroom_id:
                        # Get partners for this cleanroom
                        partner_response = await client.get(
                            f"{habu_config.base_url}/cleanrooms/{cleanroom_id}/partners",
                            headers=headers,
                            timeout=30.0
                        )
                        if partner_response.status_code == 200:
                            partners_data = partner_response.json()
                            if isinstance(partners_data, list):
                                for partner in partners_data:
                                    partner["cleanroom_id"] = cleanroom_id
                                    partner["cleanroom_name"] = cleanroom.get("name", "Unknown")
                                all_partners.extend(partners_data)
            
            # Create a summary for the LLM agent
            if all_partners:
                summary = {
                    "status": "success",
                    "count": len(all_partners),
                    "partners": all_partners,
                    "summary": f"Found {len(all_partners)} clean room partners across {len(cleanrooms_data) if isinstance(cleanrooms_data, list) else 0} cleanrooms."
                }
            else:
                summary = {
                    "status": "success",
                    "count": 0,
                    "partners": [],
                    "summary": f"No clean room partners found. You have {len(cleanrooms_data) if isinstance(cleanrooms_data, list) else 0} cleanrooms available."
                }
            
            logger.info(f"Successfully retrieved {len(all_partners)} partners")
            return json.dumps(summary, indent=2)
            
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error fetching partners: {e.response.status_code}")
        error = APIError(f"HTTP error {e.response.status_code}: {e.response.text}", e.response.status_code)
        return format_error_response(error)
    except httpx.TimeoutException as e:
        logger.error("Timeout fetching partners from Habu API")
        error = NetworkError("Request timeout while fetching partners")
        return format_error_response(error)
    except Exception as e:
        logger.error(f"Unexpected error fetching partners: {e}")
        error = APIError(f"An error occurred while fetching partners: {str(e)}")
        return format_error_response(error)