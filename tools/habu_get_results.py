"""
Habu Get Results Tool
Fetches final results from a completed clean room query
"""
import httpx
import json
from typing import Dict, Any, Optional
from config.habu_config import habu_config

async def habu_get_results(query_id: str, format_type: Optional[str] = "json") -> str:
    """
    Retrieves the results of a completed clean room query.
    
    Args:
        query_id (str): The ID of the completed query
        format_type (str, optional): Format for results ("json", "csv", "summary")
    
    Returns:
        str: JSON string containing query results and analysis
    """
    try:
        headers = await habu_config.get_auth_headers()
        
        async with httpx.AsyncClient() as client:
            # Get query results from the Habu API
            response = await client.get(
                f"{habu_config.base_url}/queries/{query_id}/results",
                headers=headers,
                timeout=60.0  # Longer timeout for potentially large result sets
            )
            
            if response.status_code == 401:
                # Token might be expired, reset and retry
                habu_config.reset_token()
                headers = await habu_config.get_auth_headers()
                response = await client.get(
                    f"{habu_config.base_url}/queries/{query_id}/results",
                    headers=headers,
                    timeout=60.0
                )
            
            response.raise_for_status()
            results_data = response.json()
            
            # Extract and analyze results
            raw_results = results_data.get("results", results_data)
            metadata = results_data.get("metadata", {})
            record_count = metadata.get("record_count") or len(raw_results) if isinstance(raw_results, list) else 1
            
            # Generate business-friendly summary
            summary_text = _generate_results_summary(raw_results, metadata, query_id)
            
            # Prepare the structured response
            summary = {
                "status": "success",
                "query_id": query_id,
                "record_count": record_count,
                "metadata": metadata,
                "results": raw_results,
                "business_summary": summary_text,
                "format": format_type,
                "summary": f"Retrieved {record_count} result records for query {query_id}. {summary_text[:100]}..."
            }
            
            return json.dumps(summary, indent=2)
            
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            error_msg = f"Results for query {query_id} not found or query not completed"
        elif e.response.status_code == 202:
            error_msg = f"Query {query_id} is still processing, results not yet available"
        else:
            error_msg = f"HTTP error {e.response.status_code}: {e.response.text}"
        
        return json.dumps({
            "status": "error",
            "error": error_msg,
            "query_id": query_id,
            "summary": f"Failed to retrieve results for query {query_id}: {error_msg}"
        })
    except Exception as e:
        error_msg = str(e)
        return json.dumps({
            "status": "error",
            "error": error_msg,
            "query_id": query_id,
            "summary": f"An error occurred while retrieving query results: {error_msg}"
        })

def _generate_results_summary(results: Any, metadata: Dict[str, Any], query_id: str) -> str:
    """
    Generate a business-friendly summary of query results.
    
    Args:
        results: The raw query results
        metadata: Query metadata
        query_id: The query identifier
    
    Returns:
        str: Human-readable summary of the results
    """
    try:
        if not results:
            return "Query completed but returned no results."
        
        summary_parts = []
        
        # Handle different result structures
        if isinstance(results, list):
            summary_parts.append(f"Query returned {len(results)} records.")
            
            # Look for common metrics in the results
            if results and isinstance(results[0], dict):
                first_record = results[0]
                
                # Common clean room metrics
                if "overlap_count" in first_record:
                    summary_parts.append(f"Audience overlap: {first_record['overlap_count']} users")
                if "match_rate" in first_record:
                    rate = first_record["match_rate"]
                    if isinstance(rate, (int, float)):
                        summary_parts.append(f"Match rate: {rate:.1%}" if rate <= 1 else f"Match rate: {rate}%")
                if "total_audience" in first_record:
                    summary_parts.append(f"Total audience size: {first_record['total_audience']:,}")
                if "segment_size" in first_record:
                    summary_parts.append(f"Segment size: {first_record['segment_size']:,}")
        
        elif isinstance(results, dict):
            # Single result object
            if "overlap_count" in results:
                summary_parts.append(f"Audience overlap: {results['overlap_count']} users")
            if "match_rate" in results:
                rate = results["match_rate"]
                if isinstance(rate, (int, float)):
                    summary_parts.append(f"Match rate: {rate:.1%}" if rate <= 1 else f"Match rate: {rate}%")
            if "total_audience" in results:
                summary_parts.append(f"Total audience size: {results['total_audience']:,}")
        
        # Add metadata insights
        if metadata:
            if "execution_time" in metadata:
                summary_parts.append(f"Execution time: {metadata['execution_time']}")
            if "data_sources" in metadata:
                sources = metadata["data_sources"]
                if isinstance(sources, list):
                    summary_parts.append(f"Data sources: {', '.join(sources)}")
        
        return " | ".join(summary_parts) if summary_parts else "Query completed successfully with custom results structure."
        
    except Exception:
        return "Query completed with results. See full data for details."