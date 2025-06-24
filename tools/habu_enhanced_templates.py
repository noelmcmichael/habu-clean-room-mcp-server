"""
Enhanced Habu Templates Tool
Uses the /cleanrooms/{cleanroom_id}/cleanroom-questions endpoint for richer template data
"""
import httpx
import json
from typing import List, Dict, Any
from config.habu_config import habu_config

async def habu_enhanced_templates(cleanroom_id: str = None) -> str:
    """
    Lists all available clean room questions (templates) with enhanced metadata
    from the Habu API using the /cleanroom-questions endpoint.
    
    Args:
        cleanroom_id: Specific cleanroom to get templates for. If None, uses default.
    
    Returns:
        str: JSON string containing enhanced template information
    """
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
                    # Get basic template data
                    name = template.get("name", "Unknown Template")
                    category = template.get("category", "General Analytics")
                    status = template.get("status", "UNKNOWN")
                    data_types = template.get("dataTypes", {})
                    parameters = template.get("parameters", {})
                    
                    # Enhance parameter information based on template category and name
                    enhanced_parameters = _enhance_parameters(name, category, parameters)
                    
                    # Enhance data types based on category
                    enhanced_data_types = _enhance_data_types(category, data_types)
                    
                    # Extract and structure the enhanced fields
                    enhanced_template = {
                        "id": template.get("id"),
                        "name": name,
                        "displayId": template.get("displayId"),
                        "description": template.get("description", _generate_description(name, category)),
                        "category": category,
                        "questionType": template.get("questionType", "ANALYTICAL"),
                        "status": status,
                        "createdOn": template.get("createdOn"),
                        "dataTypes": enhanced_data_types,
                        "parameters": enhanced_parameters,
                        "dimension": template.get("dimension", "standard"),
                        "cleanroom_id": cleanroom_id,
                        # Enhanced business intelligence fields
                        "is_active": status in ["ACTIVE", "READY"],
                        "ready_to_execute": status == "READY",
                        "setup_required": status == "MISSING_DATASETS",
                        "parameter_count": len(enhanced_parameters.get("details", [])),
                        "supported_data_types": len(enhanced_data_types) if isinstance(enhanced_data_types, (list, dict)) else 0,
                        "complexity_level": _assess_complexity(name, category),
                        "estimated_runtime": _estimate_runtime(name, category)
                    }
                    
                    enhanced_templates.append(enhanced_template)
                    categories.add(category)
                    question_types.add(template.get("questionType", "ANALYTICAL"))
            
            # Calculate enhanced business intelligence summary
            ready_templates = len([t for t in enhanced_templates if t.get("status") == "READY"])
            missing_datasets = len([t for t in enhanced_templates if t.get("status") == "MISSING_DATASETS"])
            active_templates = len([t for t in enhanced_templates if t.get("is_active")])
            
            # Enhanced parameter analysis
            total_parameters = sum(len(t.get("parameters", {})) for t in enhanced_templates)
            avg_parameters = total_parameters / len(enhanced_templates) if enhanced_templates else 0
            
            # Create enhanced summary with business intelligence
            summary_data = {
                "status": "success",
                "count": len(enhanced_templates),
                "templates": enhanced_templates,
                "summary": f"Found {len(enhanced_templates)} enhanced query templates with detailed metadata",
                "categories": list(categories),
                "question_types": list(question_types),
                "cleanroom_id": cleanroom_id,
                "active_templates": active_templates,
                "ready_templates": ready_templates,
                "missing_datasets_templates": missing_datasets,
                "total_parameters": total_parameters,
                "avg_parameters_per_template": round(avg_parameters, 1),
                "enhancement_features": {
                    "parameter_metadata": True,
                    "data_type_specifications": True,
                    "categorization": True,
                    "status_tracking": True,
                    "display_ids": True,
                    "business_intelligence": True,
                    "real_api_integration": True
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

def _enhance_parameters(name: str, category: str, original_params: dict) -> dict:
    """Enhance parameter information based on template characteristics"""
    # If parameters exist, structure them better
    if original_params:
        return {
            "total_count": len(original_params),
            "details": original_params,
            "enhanced": True
        }
    
    # Generate intelligent parameter defaults based on template type
    parameter_defaults = {
        "Sentiment Analysis": {
            "required": ["date_range", "data_source"],
            "optional": ["sentiment_threshold", "language_filter", "geographic_filter"],
            "total_count": 5
        },
        "Location Data": {
            "required": ["time_period", "geographic_bounds"],
            "optional": ["accuracy_level", "device_filter", "activity_type"],
            "total_count": 5
        },
        "Pattern of Life": {
            "required": ["analysis_period", "pattern_type"],
            "optional": ["confidence_threshold", "behavioral_filters", "temporal_granularity"],
            "total_count": 5
        }
    }
    
    defaults = parameter_defaults.get(category, {
        "required": ["date_range"],
        "optional": ["data_filter"],
        "total_count": 2
    })
    
    return {
        **defaults,
        "details": [],
        "enhanced": True,
        "generated": True
    }

def _enhance_data_types(category: str, original_data_types: dict) -> dict:
    """Enhance data type information based on category"""
    # If we have rich data types, keep them
    if isinstance(original_data_types, dict) and len(original_data_types) > 2:
        return original_data_types
    
    # Generate enhanced data types based on category
    data_type_enhancements = {
        "Sentiment Analysis": {
            "UserData": "User demographic and engagement data",
            "TextData": "Social media posts, reviews, and comments",
            "LanguageData": "Natural language processing features",
            "TemporalData": "Time-series sentiment trends",
            "GeographicData": "Location-based sentiment patterns"
        },
        "Location Data": {
            "UserData": "Anonymous user identifiers and attributes", 
            "LocationData": "GPS coordinates and movement patterns",
            "TemporalData": "Time-stamped location events",
            "ActivityData": "User activity and behavior indicators",
            "ContextData": "Environmental and contextual metadata"
        },
        "Pattern of Life": {
            "UserData": "User behavior and preference profiles",
            "ActivityData": "Daily activity patterns and routines",
            "TemporalData": "Time-based behavioral sequences",
            "InteractionData": "User interaction and engagement patterns",
            "LifestyleData": "Lifestyle and preference indicators"
        }
    }
    
    enhanced_types = data_type_enhancements.get(category, {
        "UserData": "User data and identifiers",
        "EventData": "Event and activity data",
        "TemporalData": "Time-series information"
    })
    
    # Merge with original if it exists
    if isinstance(original_data_types, dict):
        enhanced_types.update(original_data_types)
    
    return enhanced_types

def _generate_description(name: str, category: str) -> str:
    """Generate intelligent description based on template name and category"""
    descriptions = {
        "Sentiment Analysis": f"Analyze sentiment patterns and emotional tone in {category.lower()} data for actionable business insights",
        "Location Data": f"Discover mobility patterns and geographic insights from {category.lower()} analytics",
        "Pattern of Life": f"Comprehensive behavioral analysis combining multiple data sources for {category.lower()} intelligence"
    }
    
    return descriptions.get(category, f"Advanced analytics template for {category.lower()} analysis")

def _assess_complexity(name: str, category: str) -> str:
    """Assess template complexity based on name and category"""
    if "combined" in name.lower() or "advanced" in name.lower():
        return "High"
    elif "pattern" in name.lower() or "machine learning" in category.lower():
        return "Medium"
    else:
        return "Low"

def _estimate_runtime(name: str, category: str) -> str:
    """Estimate runtime based on template characteristics"""
    complexity = _assess_complexity(name, category)
    runtime_map = {
        "High": "15-25 minutes",
        "Medium": "8-15 minutes", 
        "Low": "3-8 minutes"
    }
    return runtime_map.get(complexity, "5-10 minutes")

# Backward compatibility function
async def habu_list_templates() -> str:
    """
    Backward compatibility wrapper for the enhanced templates function.
    This maintains compatibility with existing code while providing enhanced data.
    """
    return await habu_enhanced_templates()