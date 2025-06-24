#!/usr/bin/env python3
"""
Deep Habu API Discovery
Comprehensive exploration of Habu Clean Room API endpoints and capabilities
"""

import asyncio
import httpx
import json
import os
import time
from datetime import datetime
from typing import Dict, List, Any, Optional, Set
from dotenv import load_dotenv
from urllib.parse import urljoin, urlparse
import re

load_dotenv()

class DeepHabuAPIDiscovery:
    def __init__(self):
        self.client_id = os.getenv('HABU_CLIENT_ID')
        self.client_secret = os.getenv('HABU_CLIENT_SECRET')
        self.base_url = "https://api.habu.com"
        self.token = None
        self.discovered_endpoints = {}
        self.api_structure = {}
        self.rate_limit_delay = 0.5  # Start conservative
        
    async def smart_authenticate(self) -> bool:
        """Try multiple authentication approaches"""
        auth_patterns = [
            # Standard OAuth2 patterns
            {"url": "/oauth/token", "method": "POST"},
            {"url": "/auth/token", "method": "POST"},
            {"url": "/v1/oauth/token", "method": "POST"},
            {"url": "/api/v1/oauth/token", "method": "POST"},
            {"url": "/token", "method": "POST"},
            
            # Alternative auth patterns
            {"url": "/auth/login", "method": "POST"},
            {"url": "/login", "method": "POST"},
            {"url": "/authenticate", "method": "POST"},
        ]
        
        async with httpx.AsyncClient() as client:
            for pattern in auth_patterns:
                try:
                    print(f"🔑 Trying auth endpoint: {pattern['url']}")
                    
                    auth_data = {
                        'grant_type': 'client_credentials',
                        'client_id': self.client_id,
                        'client_secret': self.client_secret
                    }
                    
                    response = await client.post(
                        f"{self.base_url}{pattern['url']}",
                        data=auth_data,
                        timeout=15.0
                    )
                    
                    if response.status_code == 200:
                        token_data = response.json()
                        self.token = token_data.get('access_token')
                        if self.token:
                            print(f"✅ Authentication successful via {pattern['url']}")
                            return True
                    elif response.status_code == 404:
                        continue  # Try next pattern
                    else:
                        print(f"  Status {response.status_code}: {response.text[:100]}")
                        
                except Exception as e:
                    print(f"  Error: {str(e)[:50]}")
                
                await asyncio.sleep(0.2)
        
        print("❌ Could not authenticate with any known pattern")
        return False
    
    async def discover_api_structure(self) -> Dict:
        """Discover the overall API structure using multiple techniques"""
        
        discovery_results = {
            "base_endpoints": await self._discover_base_endpoints(),
            "api_versions": await self._discover_api_versions(),
            "resource_patterns": await self._discover_resource_patterns(),
            "advanced_endpoints": await self._discover_advanced_endpoints(),
            "admin_endpoints": await self._discover_admin_endpoints(),
            "webhook_endpoints": await self._discover_webhook_endpoints()
        }
        
        return discovery_results
    
    async def _discover_base_endpoints(self) -> Dict[str, Any]:
        """Discover base API endpoints"""
        print("🔍 Discovering base endpoints...")
        
        base_endpoints = [
            # Core functionality (known working)
            "/clean-rooms",
            "/partners", 
            "/templates",
            "/queries",
            
            # Standard REST patterns
            "/users",
            "/organizations",
            "/projects",
            "/workspaces",
            "/accounts",
            
            # Data management
            "/datasets",
            "/data-sources",
            "/connections",
            "/schemas",
            "/catalogs",
            
            # Analytics
            "/analytics",
            "/reports",
            "/dashboards",
            "/metrics",
            "/insights",
            "/recommendations",
            
            # Exports and results
            "/exports",
            "/results",
            "/downloads",
            "/files",
            "/outputs",
            
            # Workflow management
            "/workflows",
            "/pipelines",
            "/jobs",
            "/tasks",
            "/schedules",
            "/automations",
            
            # Collaboration
            "/sharing",
            "/permissions",
            "/invitations",
            "/teams",
            "/roles",
            
            # Monitoring
            "/health",
            "/status",
            "/monitoring",
            "/logs",
            "/audit",
            "/events"
        ]
        
        discoveries = {}
        headers = {'Authorization': f'Bearer {self.token}'} if self.token else {}
        
        async with httpx.AsyncClient() as client:
            for endpoint in base_endpoints:
                try:
                    print(f"  Testing: {endpoint}")
                    response = await client.get(
                        f"{self.base_url}{endpoint}",
                        headers=headers,
                        timeout=10.0
                    )
                    
                    result = {
                        "status_code": response.status_code,
                        "accessible": response.status_code == 200,
                        "requires_auth": response.status_code == 401,
                        "exists": response.status_code != 404,
                        "response_size": len(response.content),
                        "content_type": response.headers.get("content-type"),
                    }
                    
                    if response.status_code == 200:
                        try:
                            data = response.json()
                            result["data_preview"] = str(data)[:200] + "..." if len(str(data)) > 200 else str(data)
                            result["data_structure"] = self._analyze_data_structure(data)
                            print(f"    ✅ SUCCESS - {len(str(data))} chars")
                        except:
                            result["data_preview"] = response.text[:200]
                            print(f"    ✅ SUCCESS - Non-JSON response")
                    elif response.status_code == 401:
                        print(f"    🔒 PROTECTED - Requires authentication")
                    elif response.status_code == 403:
                        print(f"    🚫 FORBIDDEN - Insufficient permissions")
                    elif response.status_code == 404:
                        print(f"    ❌ NOT FOUND")
                    else:
                        print(f"    ⚠️ STATUS {response.status_code}")
                    
                    discoveries[endpoint] = result
                    
                except Exception as e:
                    discoveries[endpoint] = {
                        "error": str(e),
                        "accessible": False
                    }
                    print(f"    💥 ERROR: {str(e)[:50]}")
                
                await asyncio.sleep(self.rate_limit_delay)
        
        return discoveries
    
    async def _discover_api_versions(self) -> Dict[str, Any]:
        """Discover API versioning patterns"""
        print("🔍 Discovering API versions...")
        
        version_patterns = [
            "/v1", "/v2", "/v3", "/api/v1", "/api/v2", "/api/v3",
            "/version", "/versions", "/api/version"
        ]
        
        discoveries = {}
        headers = {'Authorization': f'Bearer {self.token}'} if self.token else {}
        
        async with httpx.AsyncClient() as client:
            for pattern in version_patterns:
                try:
                    response = await client.get(
                        f"{self.base_url}{pattern}",
                        headers=headers,
                        timeout=10.0
                    )
                    
                    if response.status_code == 200:
                        try:
                            data = response.json()
                            discoveries[pattern] = {
                                "available": True,
                                "data": data
                            }
                            print(f"  ✅ Found version endpoint: {pattern}")
                        except:
                            discoveries[pattern] = {
                                "available": True,
                                "content": response.text[:200]
                            }
                    
                except Exception as e:
                    pass
                
                await asyncio.sleep(0.2)
        
        return discoveries
    
    async def _discover_resource_patterns(self) -> Dict[str, Any]:
        """Discover resource-specific endpoints using known resource IDs"""
        print("🔍 Discovering resource patterns...")
        
        # We'll use the working endpoints to discover resource patterns
        discoveries = {}
        
        # Try to get resource lists first, then explore individual resources
        known_resources = {
            "partners": await self._explore_resource_operations("/partners"),
            "templates": await self._explore_resource_operations("/templates"), 
            "queries": await self._explore_resource_operations("/queries"),
            "clean-rooms": await self._explore_resource_operations("/clean-rooms")
        }
        
        return known_resources
    
    async def _explore_resource_operations(self, base_path: str) -> Dict[str, Any]:
        """Explore CRUD operations for a specific resource"""
        operations = {}
        headers = {'Authorization': f'Bearer {self.token}'} if self.token else {}
        
        # Test different HTTP methods and paths
        test_patterns = [
            {"method": "GET", "path": base_path},
            {"method": "GET", "path": f"{base_path}/search"},
            {"method": "GET", "path": f"{base_path}/filter"},
            {"method": "GET", "path": f"{base_path}/list"},
            {"method": "OPTIONS", "path": base_path},
            {"method": "HEAD", "path": base_path},
        ]
        
        async with httpx.AsyncClient() as client:
            for pattern in test_patterns:
                try:
                    response = await client.request(
                        pattern["method"],
                        f"{self.base_url}{pattern['path']}",
                        headers=headers,
                        timeout=10.0
                    )
                    
                    operations[f"{pattern['method']} {pattern['path']}"] = {
                        "status_code": response.status_code,
                        "supported": response.status_code < 400,
                        "headers": dict(response.headers) if response.status_code == 200 else None
                    }
                    
                    if pattern["method"] == "OPTIONS":
                        # OPTIONS response shows allowed methods
                        allowed_methods = response.headers.get("Allow", "").split(", ")
                        if allowed_methods:
                            operations["allowed_methods"] = allowed_methods
                    
                except Exception as e:
                    pass
                
                await asyncio.sleep(0.1)
        
        return operations
    
    async def _discover_advanced_endpoints(self) -> Dict[str, Any]:
        """Discover advanced/enterprise endpoints"""
        print("🔍 Discovering advanced endpoints...")
        
        advanced_endpoints = [
            # Advanced analytics
            "/advanced-analytics",
            "/machine-learning",
            "/ml-models",
            "/predictions", 
            "/forecasting",
            "/anomaly-detection",
            "/clustering",
            "/segmentation",
            
            # Data science
            "/notebooks",
            "/experiments",
            "/model-registry",
            "/feature-store",
            "/data-lineage",
            "/data-quality",
            
            # Enterprise features
            "/governance",
            "/compliance",
            "/data-privacy",
            "/encryption",
            "/key-management",
            "/access-control",
            
            # Integration
            "/integrations",
            "/connectors",
            "/apis",
            "/webhooks",
            "/streaming",
            "/real-time",
            
            # Marketplace/Catalog
            "/marketplace",
            "/catalog",
            "/packages",
            "/modules",
            "/templates-library",
            "/solutions"
        ]
        
        return await self._test_endpoint_list(advanced_endpoints, "Advanced")
    
    async def _discover_admin_endpoints(self) -> Dict[str, Any]:
        """Discover administrative endpoints"""
        print("🔍 Discovering admin endpoints...")
        
        admin_endpoints = [
            "/admin",
            "/admin/users",
            "/admin/organizations", 
            "/admin/settings",
            "/admin/billing",
            "/admin/usage",
            "/admin/quotas",
            "/admin/limits",
            "/admin/maintenance",
            "/admin/system",
            "/admin/logs",
            "/admin/monitoring",
            "/admin/alerts",
            "/admin/backups"
        ]
        
        return await self._test_endpoint_list(admin_endpoints, "Admin")
    
    async def _discover_webhook_endpoints(self) -> Dict[str, Any]:
        """Discover webhook and event endpoints"""
        print("🔍 Discovering webhook endpoints...")
        
        webhook_endpoints = [
            "/webhooks",
            "/events",
            "/notifications",
            "/subscriptions",
            "/callbacks",
            "/triggers",
            "/hooks",
            "/listeners"
        ]
        
        return await self._test_endpoint_list(webhook_endpoints, "Webhooks")
    
    async def _test_endpoint_list(self, endpoints: List[str], category: str) -> Dict[str, Any]:
        """Helper to test a list of endpoints"""
        discoveries = {}
        headers = {'Authorization': f'Bearer {self.token}'} if self.token else {}
        
        async with httpx.AsyncClient() as client:
            for endpoint in endpoints:
                try:
                    response = await client.get(
                        f"{self.base_url}{endpoint}",
                        headers=headers,
                        timeout=8.0
                    )
                    
                    discoveries[endpoint] = {
                        "status_code": response.status_code,
                        "accessible": response.status_code == 200,
                        "protected": response.status_code == 401,
                        "forbidden": response.status_code == 403,
                        "exists": response.status_code != 404
                    }
                    
                    if response.status_code == 200:
                        try:
                            data = response.json()
                            discoveries[endpoint]["data_preview"] = str(data)[:150]
                            discoveries[endpoint]["data_type"] = type(data).__name__
                        except:
                            discoveries[endpoint]["content_preview"] = response.text[:150]
                    
                except Exception as e:
                    discoveries[endpoint] = {"error": str(e)}
                
                await asyncio.sleep(0.3)
        
        return discoveries
    
    def _analyze_data_structure(self, data: Any) -> Dict[str, Any]:
        """Analyze the structure of returned data"""
        analysis = {
            "type": type(data).__name__,
            "size": len(str(data))
        }
        
        if isinstance(data, dict):
            analysis["keys"] = list(data.keys())
            analysis["nested_objects"] = sum(1 for v in data.values() if isinstance(v, (dict, list)))
        elif isinstance(data, list):
            analysis["length"] = len(data)
            if data:
                analysis["item_type"] = type(data[0]).__name__
                if isinstance(data[0], dict):
                    analysis["common_keys"] = list(data[0].keys())
        
        return analysis
    
    async def generate_mcp_tools(self, discoveries: Dict) -> str:
        """Generate MCP tool implementations based on discoveries"""
        print("🔧 Generating MCP tools for discovered endpoints...")
        
        accessible_endpoints = []
        for category, endpoints in discoveries.items():
            for endpoint, info in endpoints.items():
                if isinstance(info, dict) and info.get("accessible"):
                    accessible_endpoints.append((endpoint, info, category))
        
        if not accessible_endpoints:
            return "# No accessible endpoints found for MCP tool generation"
        
        tools_code = """# Generated MCP Tools for Discovered Habu Endpoints
# Auto-generated from API discovery process

"""
        
        for endpoint, info, category in accessible_endpoints:
            tool_name = self._endpoint_to_tool_name(endpoint)
            tool_description = self._generate_tool_description(endpoint, info, category)
            
            tools_code += f'''
@mcp_server.tool(
    name="{tool_name}",
    description="{tool_description}"
)
async def {tool_name.replace("-", "_")}() -> str:
    """Auto-generated tool for {endpoint}"""
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
            
            return json.dumps({{
                "status": "success",
                "endpoint": "{endpoint}",
                "data": data,
                "summary": f"Retrieved {{len(str(data))}} characters of data from {endpoint}"
            }}, indent=2)
            
    except Exception as e:
        return json.dumps({{
            "status": "error",
            "endpoint": "{endpoint}",
            "error": str(e)
        }})

'''
        
        return tools_code
    
    def _endpoint_to_tool_name(self, endpoint: str) -> str:
        """Convert endpoint path to MCP tool name"""
        # Clean up the path and convert to tool name
        clean_path = endpoint.strip("/").replace("/", "_").replace("-", "_")
        return f"habu_{clean_path}"
    
    def _generate_tool_description(self, endpoint: str, info: Dict, category: str) -> str:
        """Generate a description for the MCP tool"""
        base_desc = f"Access {category.lower()} endpoint {endpoint}"
        
        if info.get("data_structure", {}).get("keys"):
            keys = info["data_structure"]["keys"][:3]  # First 3 keys
            base_desc += f" - Returns data with keys: {', '.join(keys)}"
        
        return base_desc
    
    async def save_discovery_report(self, discoveries: Dict, filename: str = None):
        """Save comprehensive discovery report"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"habu_deep_api_discovery_{timestamp}.json"
        
        report = {
            "discovery_timestamp": datetime.now().isoformat(),
            "base_url": self.base_url,
            "authentication_successful": bool(self.token),
            "total_endpoints_tested": sum(len(cat) for cat in discoveries.values() if isinstance(cat, dict)),
            "discoveries": discoveries,
            "summary": self._generate_discovery_summary(discoveries)
        }
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"💾 Discovery report saved to: {filename}")
        return filename
    
    def _generate_discovery_summary(self, discoveries: Dict) -> Dict:
        """Generate summary statistics"""
        summary = {
            "categories_explored": len(discoveries),
            "accessible_endpoints": 0,
            "protected_endpoints": 0,
            "not_found_endpoints": 0,
            "error_endpoints": 0,
            "new_capabilities": []
        }
        
        for category, endpoints in discoveries.items():
            if isinstance(endpoints, dict):
                for endpoint, info in endpoints.items():
                    if isinstance(info, dict):
                        if info.get("accessible"):
                            summary["accessible_endpoints"] += 1
                        elif info.get("protected") or info.get("requires_auth"):
                            summary["protected_endpoints"] += 1
                        elif not info.get("exists", True):
                            summary["not_found_endpoints"] += 1
                        elif info.get("error"):
                            summary["error_endpoints"] += 1
        
        return summary

async def main():
    print("🚀 Deep Habu API Discovery")
    print("=" * 60)
    
    discovery = DeepHabuAPIDiscovery()
    
    # Step 1: Authentication
    print("🔑 Step 1: Authentication")
    if not await discovery.smart_authenticate():
        print("⚠️  Proceeding without authentication (limited discovery)")
    
    # Step 2: Comprehensive API Discovery
    print("\\n🔍 Step 2: Comprehensive API Structure Discovery")
    discoveries = await discovery.discover_api_structure()
    
    # Step 3: Analysis and Reporting
    print("\\n📊 Step 3: Analysis and Reporting")
    
    # Count discoveries
    total_accessible = 0
    total_protected = 0
    total_tested = 0
    
    for category, endpoints in discoveries.items():
        if isinstance(endpoints, dict):
            accessible = sum(1 for info in endpoints.values() 
                           if isinstance(info, dict) and info.get("accessible"))
            protected = sum(1 for info in endpoints.values() 
                          if isinstance(info, dict) and (info.get("protected") or info.get("requires_auth")))
            tested = len(endpoints)
            
            total_accessible += accessible
            total_protected += protected
            total_tested += tested
            
            print(f"  {category.upper()}: {tested} tested, {accessible} accessible, {protected} protected")
    
    print(f"\\n📈 TOTALS: {total_tested} endpoints tested, {total_accessible} accessible, {total_protected} protected")
    
    # Step 4: Generate MCP Tools
    if total_accessible > 0:
        print("\\n🔧 Step 4: Generating MCP Tools")
        tools_code = await discovery.generate_mcp_tools(discoveries)
        
        tools_filename = f"generated_habu_mcp_tools_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
        with open(tools_filename, 'w') as f:
            f.write(tools_code)
        print(f"💾 Generated MCP tools saved to: {tools_filename}")
    
    # Step 5: Save Report
    print("\\n💾 Step 5: Saving Discovery Report")
    report_file = await discovery.save_discovery_report(discoveries)
    
    print("\\n🎯 NEXT STEPS:")
    print("1. Review the discovery report for new endpoints")
    print("2. Test the generated MCP tools")
    print("3. Implement the most valuable new capabilities")
    print("4. Contact Habu support about protected endpoints")
    
    print(f"\\n📋 Key Files Created:")
    print(f"  • Discovery Report: {report_file}")
    if total_accessible > 0:
        print(f"  • Generated Tools: {tools_filename}")

if __name__ == "__main__":
    asyncio.run(main())