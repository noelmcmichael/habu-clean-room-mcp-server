"""
Habu List Exports Tool
Lists available exports and completed query results from the Habu Exports section
This is a key integration for Phase C enhanced context-aware chat
"""
import httpx
import json
import os
from typing import Dict, Any, List, Optional
from config.habu_config import habu_config
from tools.mock_data import mock_data

async def habu_list_exports(status_filter: Optional[str] = None) -> str:
    """
    Lists available exports from the Habu platform's Exports section.
    This provides access to completed query results that can be downloaded.
    
    Args:
        status_filter (str, optional): Filter by export status ("READY", "PROCESSING", "FAILED")
    
    Returns:
        str: JSON string containing available exports and their metadata
    """
    # Check if mock mode is enabled
    use_mock = os.getenv("HABU_USE_MOCK_DATA", "false").lower() == "true"
    
    if use_mock:
        result = mock_data.list_mock_exports(status_filter)
        return json.dumps(result, indent=2)
    
    try:
        headers = await habu_config.get_auth_headers()
        
        # Build query parameters
        params = {}
        if status_filter:
            params["status"] = status_filter
        
        async with httpx.AsyncClient() as client:
            # List exports from the Habu API
            response = await client.get(
                f"{habu_config.base_url}/exports",
                headers=headers,
                params=params,
                timeout=30.0
            )
            
            if response.status_code == 401:
                # Token might be expired, reset and retry
                habu_config.reset_token()
                headers = await habu_config.get_auth_headers()
                response = await client.get(
                    f"{habu_config.base_url}/exports",
                    headers=headers,
                    params=params,
                    timeout=30.0
                )
            
            response.raise_for_status()
            exports_data = response.json()
            
            # Parse and organize export information
            exports = exports_data if isinstance(exports_data, list) else exports_data.get("exports", [])
            
            # Categorize exports by status
            ready_exports = []
            processing_exports = []
            failed_exports = []
            
            for export in exports:
                export_id = export.get("id", "unknown")
                name = export.get("name") or export.get("query_name", "Unnamed Export")
                status = export.get("status", "unknown").upper()
                created_at = export.get("created_at")
                size = export.get("file_size") or export.get("size")
                download_url = export.get("download_url")
                query_id = export.get("query_id")
                
                export_info = {
                    "export_id": export_id,
                    "name": name,
                    "status": status,
                    "created_at": created_at,
                    "file_size": size,
                    "download_url": download_url,
                    "query_id": query_id,
                    "metadata": export
                }
                
                if status == "READY":
                    ready_exports.append(export_info)
                elif status in ["PROCESSING", "BUILDING", "RUNNING"]:
                    processing_exports.append(export_info)
                elif status in ["FAILED", "ERROR"]:
                    failed_exports.append(export_info)
            
            # Generate business-friendly summary
            summary_parts = []
            if ready_exports:
                summary_parts.append(f"{len(ready_exports)} exports ready for download")
            if processing_exports:
                summary_parts.append(f"{len(processing_exports)} exports in progress")
            if failed_exports:
                summary_parts.append(f"{len(failed_exports)} failed exports")
            
            summary_text = " | ".join(summary_parts) if summary_parts else "No exports available"
            
            # Prepare response
            result = {
                "status": "success",
                "total_exports": len(exports),
                "ready_exports": ready_exports,
                "processing_exports": processing_exports,
                "failed_exports": failed_exports,
                "summary": summary_text,
                "business_summary": _generate_exports_summary(ready_exports, processing_exports)
            }
            
            return json.dumps(result, indent=2)
            
    except httpx.HTTPStatusError as e:
        error_msg = f"HTTP error {e.response.status_code}: {e.response.text}"
        return json.dumps({
            "status": "error",
            "error": error_msg,
            "summary": f"Failed to list exports: {error_msg}"
        })
    except Exception as e:
        error_msg = str(e)
        return json.dumps({
            "status": "error",
            "error": error_msg,
            "summary": f"An error occurred while listing exports: {error_msg}"
        })

async def habu_download_export(export_id: str, save_path: Optional[str] = None) -> str:
    """
    Downloads an export file from the Habu platform.
    
    Args:
        export_id (str): The ID of the export to download
        save_path (str, optional): Local path to save the file
    
    Returns:
        str: JSON string containing download result and file information
    """
    # Check if mock mode is enabled
    use_mock = os.getenv("HABU_USE_MOCK_DATA", "false").lower() == "true"
    
    if use_mock:
        result = mock_data.download_mock_export(export_id)
        return json.dumps(result, indent=2)
    
    try:
        headers = await habu_config.get_auth_headers()
        
        async with httpx.AsyncClient() as client:
            # Get export metadata first
            response = await client.get(
                f"{habu_config.base_url}/exports/{export_id}",
                headers=headers,
                timeout=30.0
            )
            
            if response.status_code == 401:
                # Token might be expired, reset and retry
                habu_config.reset_token()
                headers = await habu_config.get_auth_headers()
                response = await client.get(
                    f"{habu_config.base_url}/exports/{export_id}",
                    headers=headers,
                    timeout=30.0
                )
            
            response.raise_for_status()
            export_data = response.json()
            
            # Check if export is ready for download
            status = export_data.get("status", "").upper()
            if status != "READY":
                return json.dumps({
                    "status": "error",
                    "error": f"Export is not ready for download. Current status: {status}",
                    "export_id": export_id,
                    "current_status": status
                })
            
            download_url = export_data.get("download_url")
            if not download_url:
                # Try direct download endpoint
                download_url = f"{habu_config.base_url}/exports/{export_id}/download"
            
            # Download the file (for now, just return metadata - actual download would be large)
            file_size = export_data.get("file_size") or export_data.get("size", "unknown")
            file_name = export_data.get("name") or f"export_{export_id}.csv"
            
            result = {
                "status": "success",
                "export_id": export_id,
                "file_name": file_name,
                "file_size": file_size,
                "download_url": download_url,
                "export_metadata": export_data,
                "summary": f"Export {export_id} is ready for download ({file_size} bytes)"
            }
            
            return json.dumps(result, indent=2)
            
    except httpx.HTTPStatusError as e:
        error_msg = f"HTTP error {e.response.status_code}: {e.response.text}"
        return json.dumps({
            "status": "error",
            "error": error_msg,
            "export_id": export_id,
            "summary": f"Failed to download export {export_id}: {error_msg}"
        })
    except Exception as e:
        error_msg = str(e)
        return json.dumps({
            "status": "error",
            "error": error_msg,
            "export_id": export_id,
            "summary": f"An error occurred while downloading export: {error_msg}"
        })

def _generate_exports_summary(ready_exports: List[Dict], processing_exports: List[Dict]) -> str:
    """
    Generate a business-friendly summary of available exports.
    
    Args:
        ready_exports: List of ready export dictionaries
        processing_exports: List of processing export dictionaries
    
    Returns:
        str: Human-readable summary of export status
    """
    if not ready_exports and not processing_exports:
        return "No exports are currently available. Run some analytics queries to generate exportable results."
    
    summary_parts = []
    
    if ready_exports:
        # Group by type/name for better summary
        export_names = [exp.get("name", "Unknown") for exp in ready_exports]
        unique_names = list(set(export_names))
        
        if len(unique_names) == 1:
            summary_parts.append(f"1 type of analysis ready: {unique_names[0]}")
        else:
            summary_parts.append(f"{len(ready_exports)} results ready for download")
        
        # Calculate total data size if available
        total_size = 0
        for exp in ready_exports:
            size = exp.get("file_size")
            if isinstance(size, (int, float)):
                total_size += size
        
        if total_size > 0:
            if total_size > 1024 * 1024:  # > 1MB
                summary_parts.append(f"Total size: {total_size / (1024*1024):.1f} MB")
            else:
                summary_parts.append(f"Total size: {total_size / 1024:.1f} KB")
    
    if processing_exports:
        summary_parts.append(f"{len(processing_exports)} analyses still processing")
    
    return " | ".join(summary_parts)