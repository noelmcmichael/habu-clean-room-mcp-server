#!/usr/bin/env python3
"""
Targeted Habu API Discovery
Using the actual Habu API structure and authentication to discover new endpoints
"""

import asyncio
import httpx
import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv
from config.habu_config import habu_config

load_dotenv()

class TargetedHabuDiscovery:
    def __init__(self):
        self.base_url = "https://api.habu.com/v1"
        self.discovered_endpoints = {}
        self.working_endpoints = []
        self.protected_endpoints = []
        self.new_capabilities = []
        
    async def authenticate_and_discover(self):
        """Authenticate and discover using working Habu patterns"""
        print("🔑 Authenticating with Habu...")
        
        try:
            headers = await habu_config.get_auth_headers()
            print("✅ Authentication successful!")
            return headers
        except Exception as e:
            print(f"❌ Authentication failed: {e}")
            return None
    
    async def discover_from_known_working_endpoints(self, headers: Dict[str, str]):
        """Start from known working endpoints and explore related functionality"""
        print("🔍 Exploring from known working endpoints...")
        
        # These are the endpoints we know work from your current implementation
        known_working = [
            "/organizations",
            "/cleanrooms", 
            "/cleanrooms/{cleanroom_id}/partners",
            "/cleanrooms/{cleanroom_id}/templates",
            "/cleanrooms/{cleanroom_id}/queries"
        ]
        
        discoveries = {}
        
        async with httpx.AsyncClient() as client:
            # First, test the known endpoints
            for endpoint in known_working:
                if "{cleanroom_id}" not in endpoint:
                    result = await self._test_endpoint(client, endpoint, headers)
                    discoveries[endpoint] = result
                    
                    if result.get("accessible"):
                        self.working_endpoints.append(endpoint)
                        print(f"  ✅ {endpoint} - Working")
                    else:
                        print(f"  ❌ {endpoint} - {result.get('status_code', 'Error')}")
        
        return discoveries
    
    async def discover_related_endpoints(self, headers: Dict[str, str]):
        """Discover endpoints related to known functionality"""
        print("🔍 Discovering related endpoints...")
        
        # Based on working endpoints, try related patterns
        related_patterns = [
            # Organization-level endpoints
            "/organizations/{org_id}/settings",
            "/organizations/{org_id}/users", 
            "/organizations/{org_id}/billing",
            "/organizations/{org_id}/usage",
            "/organizations/{org_id}/limits",
            "/organizations/{org_id}/integrations",
            "/organizations/{org_id}/audit-logs",
            
            # Clean room variations
            "/cleanrooms/search",
            "/cleanrooms/templates",  # Global templates
            "/cleanrooms/shared",
            "/cleanrooms/archived",
            
            # Query-related endpoints  
            "/queries",  # Global queries
            "/queries/history",
            "/queries/templates",
            "/queries/results",
            "/queries/exports",
            "/queries/schedules",
            
            # Results and exports
            "/results",
            "/exports", 
            "/exports/list",
            "/exports/download",
            "/exports/formats",
            "/exports/schedules",
            
            # Templates
            "/templates",
            "/templates/library",
            "/templates/public",
            "/templates/shared",
            "/templates/categories",
            
            # Partners
            "/partners",
            "/partners/catalog", 
            "/partners/available",
            "/partners/connections",
            "/partners/integrations",
            
            # Advanced analytics
            "/analytics",
            "/analytics/insights",
            "/analytics/recommendations", 
            "/analytics/models",
            "/analytics/predictions",
            
            # Data management
            "/datasets",
            "/datasets/catalog",
            "/datasets/schemas",
            "/datasets/lineage", 
            "/datasets/quality",
            
            # Collaboration
            "/sharing",
            "/permissions",
            "/invitations",
            "/notifications",
            "/activity",
            
            # System
            "/health",
            "/status", 
            "/version",
            "/limits",
            "/quotas",
            
            # Marketplace/Catalog
            "/marketplace",
            "/catalog",
            "/solutions",
            "/packages"
        ]
        
        discoveries = {}
        
        async with httpx.AsyncClient() as client:
            for endpoint in related_patterns:
                # Skip parameterized endpoints for now
                if "{" not in endpoint:
                    result = await self._test_endpoint(client, endpoint, headers)
                    discoveries[endpoint] = result
                    
                    if result.get("accessible"):
                        self.working_endpoints.append(endpoint)
                        self.new_capabilities.append(endpoint)
                        print(f"  ✅ NEW: {endpoint}")
                    elif result.get("protected"):
                        self.protected_endpoints.append(endpoint)
                        print(f"  🔒 PROTECTED: {endpoint}")
                    else:
                        print(f"  ❌ {endpoint}")
                    
                    await asyncio.sleep(0.3)  # Rate limiting
        
        return discoveries
    
    async def explore_discovered_endpoints(self, headers: Dict[str, str]):
        """Deep dive into newly discovered endpoints"""
        print("🔬 Deep diving into discovered endpoints...")
        
        detailed_analysis = {}
        
        async with httpx.AsyncClient() as client:
            for endpoint in self.working_endpoints[-5:]:  # Analyze last 5 discovered
                print(f"  📋 Analyzing: {endpoint}")
                
                analysis = {
                    "endpoint": endpoint,
                    "data_analysis": await self._analyze_endpoint_data(client, endpoint, headers),
                    "related_operations": await self._explore_endpoint_operations(client, endpoint, headers),
                    "business_value": self._assess_business_value(endpoint),
                    "integration_priority": self._assess_integration_priority(endpoint)
                }
                
                detailed_analysis[endpoint] = analysis
                await asyncio.sleep(0.5)
        
        return detailed_analysis
    
    async def _test_endpoint(self, client: httpx.AsyncClient, endpoint: str, headers: Dict[str, str]) -> Dict[str, Any]:
        """Test a single endpoint and return detailed results"""
        try:
            response = await client.get(
                f"{self.base_url}{endpoint}",
                headers=headers,
                timeout=15.0
            )
            
            result = {
                "status_code": response.status_code,
                "accessible": response.status_code == 200,
                "protected": response.status_code == 401,
                "forbidden": response.status_code == 403,
                "not_found": response.status_code == 404,
                "response_size": len(response.content),
                "content_type": response.headers.get("content-type"),
                "rate_limited": response.status_code == 429
            }
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    result["data_preview"] = str(data)[:300] + "..." if len(str(data)) > 300 else str(data)
                    result["data_structure"] = self._analyze_data_structure(data)
                    result["record_count"] = len(data) if isinstance(data, list) else (1 if data else 0)
                except:
                    result["content_preview"] = response.text[:300]
            
            return result
            
        except Exception as e:
            return {
                "error": str(e),
                "accessible": False
            }
    
    async def _analyze_endpoint_data(self, client: httpx.AsyncClient, endpoint: str, headers: Dict[str, str]) -> Dict[str, Any]:
        """Analyze the data structure and content of an endpoint"""
        try:
            response = await client.get(f"{self.base_url}{endpoint}", headers=headers, timeout=10.0)
            
            if response.status_code != 200:
                return {"error": f"Status {response.status_code}"}
            
            data = response.json()
            
            analysis = {
                "data_type": type(data).__name__,
                "size_chars": len(str(data)),
                "potential_capabilities": []
            }
            
            # Analyze structure for capabilities
            if isinstance(data, list):
                analysis["record_count"] = len(data)
                if data and isinstance(data[0], dict):
                    analysis["sample_keys"] = list(data[0].keys())
                    
                    # Look for capability indicators
                    keys_str = str(analysis["sample_keys"]).lower()
                    if "export" in keys_str:
                        analysis["potential_capabilities"].append("Export Management")
                    if "schedule" in keys_str:
                        analysis["potential_capabilities"].append("Scheduling")
                    if "status" in keys_str:
                        analysis["potential_capabilities"].append("Status Monitoring")
                    if "template" in keys_str:
                        analysis["potential_capabilities"].append("Template Management")
            
            elif isinstance(data, dict):
                analysis["keys"] = list(data.keys())
                
                # Look for nested capabilities
                for key, value in data.items():
                    if isinstance(value, list) and len(value) > 0:
                        analysis["potential_capabilities"].append(f"List Management: {key}")
                    elif key.lower() in ["settings", "config", "configuration"]:
                        analysis["potential_capabilities"].append("Configuration Management")
            
            return analysis
            
        except Exception as e:
            return {"error": str(e)}
    
    async def _explore_endpoint_operations(self, client: httpx.AsyncClient, endpoint: str, headers: Dict[str, str]) -> Dict[str, Any]:
        """Explore what operations are supported on an endpoint"""
        operations = {}
        
        # Test different HTTP methods
        methods_to_test = ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"]
        
        for method in methods_to_test:
            try:
                if method == "OPTIONS":
                    response = await client.request(method, f"{self.base_url}{endpoint}", headers=headers, timeout=5.0)
                    if response.status_code == 200:
                        allowed = response.headers.get("Allow", "").split(", ")
                        operations["allowed_methods"] = [m for m in allowed if m]
                elif method == "GET":
                    # Already tested GET
                    operations[method] = "tested_separately"
                else:
                    # For other methods, just check if they're not rejected outright
                    response = await client.request(
                        method, 
                        f"{self.base_url}{endpoint}", 
                        headers=headers, 
                        timeout=5.0,
                        content="{}" if method in ["POST", "PUT", "PATCH"] else None
                    )
                    operations[method] = {
                        "status": response.status_code,
                        "supported": response.status_code not in [404, 405]  # Not Not Found or Method Not Allowed
                    }
                    
            except Exception as e:
                operations[method] = {"error": str(e)[:50]}
            
            await asyncio.sleep(0.1)
        
        return operations
    
    def _analyze_data_structure(self, data: Any) -> Dict[str, Any]:
        """Analyze data structure"""
        analysis = {
            "type": type(data).__name__,
            "size": len(str(data))
        }
        
        if isinstance(data, dict):
            analysis["keys"] = list(data.keys())[:10]  # First 10 keys
            analysis["nested_depth"] = self._calculate_nesting_depth(data)
        elif isinstance(data, list):
            analysis["length"] = len(data)
            if data and isinstance(data[0], dict):
                analysis["item_keys"] = list(data[0].keys())[:10]
        
        return analysis
    
    def _calculate_nesting_depth(self, obj, current_depth=1):
        """Calculate maximum nesting depth of a dictionary"""
        if not isinstance(obj, dict):
            return current_depth
        
        if not obj:
            return current_depth
        
        return max(
            self._calculate_nesting_depth(value, current_depth + 1) 
            for value in obj.values() 
            if isinstance(value, dict)
        ) if any(isinstance(v, dict) for v in obj.values()) else current_depth
    
    def _assess_business_value(self, endpoint: str) -> str:
        """Assess business value of discovered endpoint"""
        endpoint_lower = endpoint.lower()
        
        if any(term in endpoint_lower for term in ["export", "result", "download"]):
            return "HIGH - Data access and export capabilities"
        elif any(term in endpoint_lower for term in ["analytics", "insight", "recommendation"]):
            return "HIGH - Advanced analytics features"  
        elif any(term in endpoint_lower for term in ["schedule", "automation", "workflow"]):
            return "MEDIUM - Process automation"
        elif any(term in endpoint_lower for term in ["template", "catalog", "library"]):
            return "MEDIUM - Template and content management"
        elif any(term in endpoint_lower for term in ["health", "status", "monitoring"]):
            return "LOW - System monitoring"
        else:
            return "UNKNOWN - Needs investigation"
    
    def _assess_integration_priority(self, endpoint: str) -> int:
        """Assess integration priority (1-5, 5 being highest)"""
        endpoint_lower = endpoint.lower()
        
        # High priority - direct user value
        if any(term in endpoint_lower for term in ["export", "result", "analytics", "insight"]):
            return 5
        # Medium-high priority - workflow enhancement  
        elif any(term in endpoint_lower for term in ["schedule", "template", "catalog"]):
            return 4
        # Medium priority - collaboration
        elif any(term in endpoint_lower for term in ["sharing", "notification", "activity"]):
            return 3
        # Low-medium priority - admin features
        elif any(term in endpoint_lower for term in ["settings", "config", "permission"]):
            return 2
        # Low priority - system features
        else:
            return 1
    
    async def generate_enhanced_mcp_tools(self, detailed_analysis: Dict) -> str:
        """Generate enhanced MCP tools based on discovered capabilities"""
        print("🔧 Generating enhanced MCP tools...")
        
        high_priority_endpoints = [
            endpoint for endpoint, analysis in detailed_analysis.items()
            if analysis.get("integration_priority", 0) >= 4
        ]
        
        if not high_priority_endpoints:
            return "# No high-priority endpoints discovered for tool generation"
        
        tools_code = f'''# Enhanced Habu MCP Tools
# Generated from targeted API discovery - {datetime.now().isoformat()}
# High-priority endpoints: {len(high_priority_endpoints)}

import httpx
import json
from config.habu_config import habu_config

'''
        
        for endpoint in high_priority_endpoints:
            analysis = detailed_analysis[endpoint]
            
            # Generate tool name and description
            tool_name = self._endpoint_to_tool_name(endpoint)
            tool_description = self._generate_enhanced_description(endpoint, analysis)
            
            # Generate tool implementation
            tools_code += f'''
@mcp_server.tool(
    name="{tool_name}",
    description="{tool_description}"
)
async def {tool_name.replace("-", "_")}() -> str:
    """
    Enhanced tool for {endpoint}
    Business Value: {analysis.get("business_value", "Unknown")}
    Capabilities: {", ".join(analysis.get("data_analysis", {}).get("potential_capabilities", []))}
    """
    try:
        headers = await habu_config.get_auth_headers()
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{{habu_config.base_url}}{endpoint}",
                headers=headers,
                timeout=30.0
            )
            
            response.raise_for_status()
            data = response.json()
            
            # Business-intelligent formatting
            if isinstance(data, list):
                summary = f"Retrieved {{len(data)}} records from {endpoint}"
                if data and isinstance(data[0], dict):
                    # Show sample of available fields
                    sample_keys = list(data[0].keys())[:5]
                    summary += f" with fields: {{', '.join(sample_keys)}}"
            else:
                summary = f"Retrieved data from {endpoint} endpoint"
            
            return json.dumps({{
                "status": "success",
                "endpoint": "{endpoint}",
                "summary": summary,
                "record_count": len(data) if isinstance(data, list) else 1,
                "data": data,
                "business_capabilities": {analysis.get("data_analysis", {}).get("potential_capabilities", [])}
            }}, indent=2)
            
    except Exception as e:
        return json.dumps({{
            "status": "error", 
            "endpoint": "{endpoint}",
            "error": str(e),
            "suggestion": "This endpoint may require specific parameters or have usage restrictions"
        }})

'''
        
        return tools_code
    
    def _endpoint_to_tool_name(self, endpoint: str) -> str:
        """Convert endpoint to meaningful tool name"""
        clean_path = endpoint.strip("/").replace("/", "_").replace("-", "_")
        return f"habu_{clean_path}"
    
    def _generate_enhanced_description(self, endpoint: str, analysis: Dict) -> str:
        """Generate enhanced description with business context"""
        base_desc = f"Access {endpoint} endpoint"
        
        capabilities = analysis.get("data_analysis", {}).get("potential_capabilities", [])
        if capabilities:
            base_desc += f" - Provides: {', '.join(capabilities)}"
        
        business_value = analysis.get("business_value", "")
        if "HIGH" in business_value:
            base_desc += " (High business value)"
        
        return base_desc
    
    async def save_discovery_report(self, discoveries: Dict, detailed_analysis: Dict):
        """Save comprehensive discovery report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"targeted_habu_discovery_{timestamp}.json"
        
        report = {
            "discovery_timestamp": datetime.now().isoformat(),
            "api_base_url": self.base_url,
            "summary": {
                "total_working_endpoints": len(self.working_endpoints),
                "new_capabilities_found": len(self.new_capabilities),
                "protected_endpoints": len(self.protected_endpoints),
                "high_priority_integrations": len([
                    ep for ep, analysis in detailed_analysis.items()
                    if analysis.get("integration_priority", 0) >= 4
                ])
            },
            "working_endpoints": self.working_endpoints,
            "new_capabilities": self.new_capabilities,
            "protected_endpoints": self.protected_endpoints,
            "detailed_analysis": detailed_analysis,
            "endpoint_discoveries": discoveries
        }
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"💾 Detailed discovery report saved to: {filename}")
        return filename

async def main():
    print("🎯 Targeted Habu API Discovery")
    print("=" * 50)
    
    discovery = TargetedHabuDiscovery()
    
    # Step 1: Authentication
    headers = await discovery.authenticate_and_discover()
    if not headers:
        print("❌ Cannot proceed without authentication")
        return
    
    # Step 2: Discover from known working endpoints
    print("\\n📋 Step 2: Mapping known functionality")
    known_discoveries = await discovery.discover_from_known_working_endpoints(headers)
    
    # Step 3: Discover related endpoints
    print("\\n🔍 Step 3: Discovering related endpoints") 
    related_discoveries = await discovery.discover_related_endpoints(headers)
    
    # Step 4: Deep analysis of new discoveries
    if discovery.working_endpoints:
        print("\\n🔬 Step 4: Deep analysis of discoveries")
        detailed_analysis = await discovery.explore_discovered_endpoints(headers)
    else:
        detailed_analysis = {}
    
    # Step 5: Generate enhanced MCP tools
    if detailed_analysis:
        print("\\n🔧 Step 5: Generating enhanced MCP tools")
        tools_code = await discovery.generate_enhanced_mcp_tools(detailed_analysis)
        
        tools_filename = f"enhanced_habu_tools_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
        with open(tools_filename, 'w') as f:
            f.write(tools_code)
        print(f"💾 Enhanced MCP tools saved to: {tools_filename}")
    
    # Step 6: Save comprehensive report
    print("\\n💾 Step 6: Saving discovery report")
    report_file = await discovery.save_discovery_report(
        {**known_discoveries, **related_discoveries}, 
        detailed_analysis
    )
    
    # Summary
    print("\\n🎯 DISCOVERY SUMMARY:")
    print(f"  • Working endpoints: {len(discovery.working_endpoints)}")
    print(f"  • New capabilities: {len(discovery.new_capabilities)}")
    print(f"  • Protected endpoints: {len(discovery.protected_endpoints)}")
    
    if discovery.new_capabilities:
        print("\\n🚀 NEW CAPABILITIES DISCOVERED:")
        for capability in discovery.new_capabilities:
            print(f"  • {capability}")
    
    print(f"\\n📋 FILES CREATED:")
    print(f"  • Discovery Report: {report_file}")
    if detailed_analysis:
        print(f"  • Enhanced Tools: {tools_filename}")
    
    print("\\n🎯 RECOMMENDED NEXT STEPS:")
    print("1. Review new capabilities for immediate integration")
    print("2. Test generated MCP tools")
    print("3. Prioritize high-value endpoints for Phase D implementation")

if __name__ == "__main__":
    asyncio.run(main())