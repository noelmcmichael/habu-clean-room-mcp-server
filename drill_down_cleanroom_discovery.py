#!/usr/bin/env python3
"""
Drill-Down Cleanroom Discovery
Explore cleanroom-specific endpoints and discover hidden functionality
"""

import asyncio
import httpx
import json
from datetime import datetime
from typing import Dict, List, Any
from config.habu_config import habu_config

class CleanroomDrillDownDiscovery:
    def __init__(self):
        self.base_url = "https://api.habu.com/v1"
        self.cleanrooms = []
        self.cleanroom_specific_endpoints = {}
        self.new_discoveries = []
        
    async def discover_cleanrooms_and_drill_down(self):
        """Get cleanrooms and explore their specific endpoints"""
        print("🔍 Step 1: Discovering available cleanrooms...")
        
        headers = await habu_config.get_auth_headers()
        
        async with httpx.AsyncClient() as client:
            # Get cleanrooms
            response = await client.get(f"{self.base_url}/cleanrooms", headers=headers, timeout=30.0)
            
            if response.status_code == 200:
                self.cleanrooms = response.json()
                print(f"✅ Found {len(self.cleanrooms)} cleanrooms")
                
                # Show cleanroom details
                for i, cleanroom in enumerate(self.cleanrooms):
                    print(f"  {i+1}. {cleanroom.get('name', 'Unnamed')} (ID: {cleanroom.get('id', 'unknown')[:8]}...)")
                
            else:
                print(f"❌ Failed to get cleanrooms: {response.status_code}")
                return {}
        
        # Now drill down into each cleanroom
        if not self.cleanrooms:
            print("❌ No cleanrooms found - cannot drill down")
            return {}
        
        print(f"\\n🔬 Step 2: Drilling down into cleanroom-specific endpoints...")
        
        all_discoveries = {}
        
        # Use first cleanroom for deep exploration
        primary_cleanroom = self.cleanrooms[0]
        cleanroom_id = primary_cleanroom.get('id')
        
        if cleanroom_id:
            print(f"🎯 Deep diving into cleanroom: {primary_cleanroom.get('name', 'Unnamed')}")
            discoveries = await self._explore_cleanroom_endpoints(cleanroom_id, headers)
            all_discoveries[cleanroom_id] = discoveries
        
        return all_discoveries
    
    async def _explore_cleanroom_endpoints(self, cleanroom_id: str, headers: Dict[str, str]) -> Dict[str, Any]:
        """Explore all possible endpoints for a specific cleanroom"""
        
        # Comprehensive list of endpoints to test within a cleanroom context
        cleanroom_endpoints = [
            # Known working from your current implementation
            f"/cleanrooms/{cleanroom_id}/partners",
            f"/cleanrooms/{cleanroom_id}/templates", 
            f"/cleanrooms/{cleanroom_id}/queries",
            
            # Potential additional endpoints
            f"/cleanrooms/{cleanroom_id}/settings",
            f"/cleanrooms/{cleanroom_id}/configuration",
            f"/cleanrooms/{cleanroom_id}/permissions",
            f"/cleanrooms/{cleanroom_id}/users",
            f"/cleanrooms/{cleanroom_id}/invitations",
            f"/cleanrooms/{cleanroom_id}/roles",
            
            # Data and analytics
            f"/cleanrooms/{cleanroom_id}/datasets",
            f"/cleanrooms/{cleanroom_id}/schemas",
            f"/cleanrooms/{cleanroom_id}/data-sources",
            f"/cleanrooms/{cleanroom_id}/analytics",
            f"/cleanrooms/{cleanroom_id}/insights",
            f"/cleanrooms/{cleanroom_id}/reports",
            f"/cleanrooms/{cleanroom_id}/dashboards",
            
            # Query management
            f"/cleanrooms/{cleanroom_id}/queries/history",
            f"/cleanrooms/{cleanroom_id}/queries/running",
            f"/cleanrooms/{cleanroom_id}/queries/completed",
            f"/cleanrooms/{cleanroom_id}/queries/failed",
            f"/cleanrooms/{cleanroom_id}/queries/scheduled",
            f"/cleanrooms/{cleanroom_id}/queries/templates",
            
            # Results and exports
            f"/cleanrooms/{cleanroom_id}/results",
            f"/cleanrooms/{cleanroom_id}/exports", 
            f"/cleanrooms/{cleanroom_id}/exports/list",
            f"/cleanrooms/{cleanroom_id}/exports/history",
            f"/cleanrooms/{cleanroom_id}/exports/downloads",
            f"/cleanrooms/{cleanroom_id}/files",
            f"/cleanrooms/{cleanroom_id}/outputs",
            
            # Templates and libraries
            f"/cleanrooms/{cleanroom_id}/templates/library",
            f"/cleanrooms/{cleanroom_id}/templates/public",
            f"/cleanrooms/{cleanroom_id}/templates/private",
            f"/cleanrooms/{cleanroom_id}/templates/shared",
            f"/cleanrooms/{cleanroom_id}/templates/categories",
            
            # Collaboration features
            f"/cleanrooms/{cleanroom_id}/sharing",
            f"/cleanrooms/{cleanroom_id}/collaboration",
            f"/cleanrooms/{cleanroom_id}/activity",
            f"/cleanrooms/{cleanroom_id}/notifications",
            f"/cleanrooms/{cleanroom_id}/audit",
            f"/cleanrooms/{cleanroom_id}/logs",
            
            # Workflow and automation
            f"/cleanrooms/{cleanroom_id}/workflows",
            f"/cleanrooms/{cleanroom_id}/pipelines",
            f"/cleanrooms/{cleanroom_id}/schedules",
            f"/cleanrooms/{cleanroom_id}/automations",
            f"/cleanrooms/{cleanroom_id}/triggers",
            f"/cleanrooms/{cleanroom_id}/jobs",
            
            # Advanced analytics
            f"/cleanrooms/{cleanroom_id}/ml-models",
            f"/cleanrooms/{cleanroom_id}/predictions",
            f"/cleanrooms/{cleanroom_id}/recommendations",
            f"/cleanrooms/{cleanroom_id}/forecasts",
            f"/cleanrooms/{cleanroom_id}/segments",
            f"/cleanrooms/{cleanroom_id}/cohorts",
            
            # Partner-specific endpoints
            f"/cleanrooms/{cleanroom_id}/partners/connections",
            f"/cleanrooms/{cleanroom_id}/partners/integrations",
            f"/cleanrooms/{cleanroom_id}/partners/data-sharing",
            f"/cleanrooms/{cleanroom_id}/partners/permissions",
            
            # Monitoring and health
            f"/cleanrooms/{cleanroom_id}/health",
            f"/cleanrooms/{cleanroom_id}/status",
            f"/cleanrooms/{cleanroom_id}/metrics",
            f"/cleanrooms/{cleanroom_id}/usage",
            f"/cleanrooms/{cleanroom_id}/limits",
            f"/cleanrooms/{cleanroom_id}/quotas",
            
            # Advanced features
            f"/cleanrooms/{cleanroom_id}/marketplace",
            f"/cleanrooms/{cleanroom_id}/catalog",
            f"/cleanrooms/{cleanroom_id}/solutions",
            f"/cleanrooms/{cleanroom_id}/packages",
            f"/cleanrooms/{cleanroom_id}/extensions",
            f"/cleanrooms/{cleanroom_id}/integrations"
        ]
        
        discoveries = {}
        working_endpoints = []
        
        async with httpx.AsyncClient() as client:
            for endpoint in cleanroom_endpoints:
                try:
                    print(f"  Testing: {endpoint.split('/')[-1]}")
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
                        "response_size": len(response.content)
                    }
                    
                    if response.status_code == 200:
                        try:
                            data = response.json()
                            result["data_preview"] = str(data)[:200] + "..." if len(str(data)) > 200 else str(data)
                            result["data_analysis"] = self._analyze_endpoint_data(data)
                            result["business_value"] = self._assess_business_value(endpoint)
                            working_endpoints.append(endpoint)
                            self.new_discoveries.append(endpoint)
                            print(f"    ✅ FOUND: {endpoint.split('/')[-1]} - {result['business_value']}")
                        except:
                            result["content_preview"] = response.text[:200]
                            working_endpoints.append(endpoint)
                            print(f"    ✅ FOUND: {endpoint.split('/')[-1]} (non-JSON)")
                    elif response.status_code == 403:
                        print(f"    🔒 PROTECTED: {endpoint.split('/')[-1]}")
                    elif response.status_code == 401:
                        print(f"    🔑 AUTH REQUIRED: {endpoint.split('/')[-1]}")
                    else:
                        print(f"    ❌ {response.status_code}: {endpoint.split('/')[-1]}")
                    
                    discoveries[endpoint] = result
                    
                except Exception as e:
                    discoveries[endpoint] = {"error": str(e)}
                    print(f"    💥 ERROR: {endpoint.split('/')[-1]} - {str(e)[:30]}")
                
                await asyncio.sleep(0.4)  # Respectful rate limiting
        
        print(f"\\n🎯 Found {len(working_endpoints)} working endpoints in this cleanroom")
        return discoveries
    
    def _analyze_endpoint_data(self, data: Any) -> Dict[str, Any]:
        """Analyze endpoint data for capabilities"""
        analysis = {
            "data_type": type(data).__name__,
            "size": len(str(data)),
            "capabilities": []
        }
        
        if isinstance(data, list):
            analysis["record_count"] = len(data)
            if data and isinstance(data[0], dict):
                analysis["sample_keys"] = list(data[0].keys())
                
                # Detect capabilities from data structure
                keys_str = str(analysis["sample_keys"]).lower()
                if "export" in keys_str or "download" in keys_str:
                    analysis["capabilities"].append("Export/Download Management")
                if "schedule" in keys_str:
                    analysis["capabilities"].append("Scheduling")
                if "status" in keys_str or "state" in keys_str:
                    analysis["capabilities"].append("Status Monitoring")
                if "template" in keys_str:
                    analysis["capabilities"].append("Template Management")
                if "query" in keys_str:
                    analysis["capabilities"].append("Query Management")
                if "result" in keys_str:
                    analysis["capabilities"].append("Results Access")
                if "insight" in keys_str or "recommendation" in keys_str:
                    analysis["capabilities"].append("AI Insights")
                if "partner" in keys_str:
                    analysis["capabilities"].append("Partner Management")
                if "data" in keys_str or "dataset" in keys_str:
                    analysis["capabilities"].append("Data Management")
        
        elif isinstance(data, dict):
            analysis["keys"] = list(data.keys())
            
            # Analyze nested structure
            for key, value in data.items():
                if isinstance(value, list) and value:
                    analysis["capabilities"].append(f"List Management: {key}")
                elif key.lower() in ["config", "settings", "configuration"]:
                    analysis["capabilities"].append("Configuration Management")
                elif key.lower() in ["permissions", "roles", "access"]:
                    analysis["capabilities"].append("Access Control")
        
        return analysis
    
    def _assess_business_value(self, endpoint: str) -> str:
        """Assess business value of endpoint"""
        endpoint_lower = endpoint.lower()
        
        if any(term in endpoint_lower for term in ["export", "download", "result", "output"]):
            return "🚀 HIGH VALUE - Data Access"
        elif any(term in endpoint_lower for term in ["analytics", "insight", "recommendation", "prediction"]):
            return "🚀 HIGH VALUE - AI Analytics"
        elif any(term in endpoint_lower for term in ["workflow", "automation", "schedule", "pipeline"]):
            return "🔧 HIGH VALUE - Automation"
        elif any(term in endpoint_lower for term in ["template", "query", "job", "task"]):
            return "⚙️ MEDIUM VALUE - Operations"
        elif any(term in endpoint_lower for term in ["partner", "collaboration", "sharing"]):
            return "🤝 MEDIUM VALUE - Collaboration"
        elif any(term in endpoint_lower for term in ["health", "status", "monitor", "metrics"]):
            return "📊 LOW VALUE - Monitoring"
        else:
            return "❓ UNKNOWN VALUE"
    
    async def generate_comprehensive_mcp_tools(self, discoveries: Dict) -> str:
        """Generate comprehensive MCP tools for all discovered endpoints"""
        print("🔧 Generating comprehensive MCP tools...")
        
        # Filter for high-value accessible endpoints
        high_value_endpoints = []
        for cleanroom_id, cleanroom_discoveries in discoveries.items():
            for endpoint, data in cleanroom_discoveries.items():
                if data.get("accessible") and "HIGH VALUE" in data.get("business_value", ""):
                    high_value_endpoints.append((endpoint, data, cleanroom_id))
        
        if not high_value_endpoints:
            return "# No high-value endpoints discovered"
        
        tools_code = f'''# Comprehensive Habu MCP Tools - Phase D
# Generated from cleanroom drill-down discovery
# High-value endpoints discovered: {len(high_value_endpoints)}
# Discovery date: {datetime.now().isoformat()}

import httpx
import json
from config.habu_config import habu_config

'''
        
        for endpoint, data, cleanroom_id in high_value_endpoints:
            tool_name = self._generate_tool_name(endpoint)
            capabilities = data.get("data_analysis", {}).get("capabilities", [])
            
            tools_code += f'''
@mcp_server.tool(
    name="{tool_name}",
    description="Access {endpoint.split('/')[-1]} functionality - {data.get('business_value', 'Unknown value')}"
)
async def {tool_name.replace('-', '_')}(cleanroom_id: str = "{cleanroom_id}") -> str:
    """
    Access {endpoint.split('/')[-1]} endpoint for cleanroom operations
    Capabilities: {', '.join(capabilities) if capabilities else 'Data access'}
    Business Value: {data.get('business_value', 'Unknown')}
    """
    try:
        headers = await habu_config.get_auth_headers()
        
        # Construct endpoint with cleanroom ID
        endpoint_url = f"{{habu_config.base_url}}/cleanrooms/{{cleanroom_id}}/{endpoint.split('/')[-1]}"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(endpoint_url, headers=headers, timeout=30.0)
            response.raise_for_status()
            
            data = response.json()
            
            # Enhanced response formatting
            if isinstance(data, list):
                summary = f"Found {{len(data)}} {endpoint.split('/')[-1]} records"
                if data and isinstance(data[0], dict):
                    sample_keys = list(data[0].keys())[:5]
                    summary += f" with fields: {{', '.join(sample_keys)}}"
            else:
                summary = f"Retrieved {endpoint.split('/')[-1]} data"
            
            return json.dumps({{
                "status": "success",
                "endpoint": "{endpoint}",
                "cleanroom_id": cleanroom_id,
                "summary": summary,
                "capabilities": {capabilities},
                "record_count": len(data) if isinstance(data, list) else 1,
                "data": data
            }}, indent=2)
            
    except httpx.HTTPStatusError as e:
        return json.dumps({{
            "status": "error",
            "endpoint": "{endpoint}",
            "error": f"HTTP {{e.response.status_code}}: {{e.response.text[:100]}}",
            "suggestion": "Check cleanroom_id and endpoint availability"
        }})
    except Exception as e:
        return json.dumps({{
            "status": "error",
            "endpoint": "{endpoint}",
            "error": str(e)
        }})

'''
        
        return tools_code
    
    def _generate_tool_name(self, endpoint: str) -> str:
        """Generate meaningful tool name from endpoint"""
        parts = endpoint.split('/')
        # Take the last part and clean it up
        name_part = parts[-1].replace('-', '_')
        return f"habu_cleanroom_{name_part}"
    
    async def save_comprehensive_report(self, discoveries: Dict):
        """Save comprehensive discovery report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"cleanroom_drilldown_discovery_{timestamp}.json"
        
        # Calculate summary statistics
        total_endpoints_tested = 0
        total_accessible = 0
        high_value_accessible = 0
        
        for cleanroom_id, cleanroom_discoveries in discoveries.items():
            total_endpoints_tested += len(cleanroom_discoveries)
            for endpoint, data in cleanroom_discoveries.items():
                if data.get("accessible"):
                    total_accessible += 1
                    if "HIGH VALUE" in data.get("business_value", ""):
                        high_value_accessible += 1
        
        report = {
            "discovery_timestamp": datetime.now().isoformat(),
            "discovery_type": "cleanroom_drilldown",
            "cleanrooms_analyzed": len(discoveries),
            "summary": {
                "total_endpoints_tested": total_endpoints_tested,
                "total_accessible": total_accessible,
                "high_value_accessible": high_value_accessible,
                "success_rate": f"{(total_accessible/total_endpoints_tested)*100:.1f}%" if total_endpoints_tested > 0 else "0%"
            },
            "cleanroom_details": [
                {
                    "id": cr.get("id"),
                    "name": cr.get("name"),
                    "description": cr.get("description", "")
                }
                for cr in self.cleanrooms
            ],
            "discoveries": discoveries,
            "new_capabilities": self.new_discoveries
        }
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"💾 Comprehensive report saved to: {filename}")
        return filename

async def main():
    print("🎯 Cleanroom Drill-Down Discovery")
    print("=" * 50)
    
    discovery = CleanroomDrillDownDiscovery()
    
    # Discover cleanrooms and drill down
    discoveries = await discovery.discover_cleanrooms_and_drill_down()
    
    if not discoveries:
        print("❌ No discoveries made")
        return
    
    # Generate comprehensive MCP tools
    print("\\n🔧 Generating comprehensive MCP tools...")
    tools_code = await discovery.generate_comprehensive_mcp_tools(discoveries)
    
    if "No high-value endpoints" not in tools_code:
        tools_filename = f"comprehensive_habu_tools_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
        with open(tools_filename, 'w') as f:
            f.write(tools_code)
        print(f"💾 Comprehensive MCP tools saved to: {tools_filename}")
    
    # Save comprehensive report
    print("\\n💾 Saving comprehensive discovery report...")
    report_file = await discovery.save_comprehensive_report(discoveries)
    
    # Summary
    total_accessible = sum(
        len([ep for ep, data in cr_discoveries.items() if data.get("accessible")])
        for cr_discoveries in discoveries.values()
    )
    
    high_value_count = sum(
        len([ep for ep, data in cr_discoveries.items() 
             if data.get("accessible") and "HIGH VALUE" in data.get("business_value", "")])
        for cr_discoveries in discoveries.values()
    )
    
    print("\\n🎯 DRILL-DOWN SUMMARY:")
    print(f"  • Cleanrooms analyzed: {len(discoveries)}")
    print(f"  • Accessible endpoints: {total_accessible}")
    print(f"  • High-value endpoints: {high_value_count}")
    print(f"  • New capabilities discovered: {len(discovery.new_discoveries)}")
    
    if discovery.new_discoveries:
        print("\\n🚀 HIGH-VALUE DISCOVERIES:")
        for endpoint in discovery.new_discoveries:
            if "HIGH VALUE" in discoveries[list(discoveries.keys())[0]].get(endpoint, {}).get("business_value", ""):
                capability = endpoint.split('/')[-1]
                print(f"  • {capability.upper()} - {discoveries[list(discoveries.keys())[0]][endpoint]['business_value']}")
    
    print(f"\\n📋 FILES CREATED:")
    print(f"  • Discovery Report: {report_file}")
    if "No high-value endpoints" not in tools_code:
        print(f"  • Comprehensive Tools: {tools_filename}")
    
    print("\\n🎯 NEXT STEPS:")
    print("1. Review high-value endpoints for immediate integration")
    print("2. Test the comprehensive MCP tools")
    print("3. Implement Phase D advanced features")
    print("4. Extend React frontend with new capabilities")

if __name__ == "__main__":
    asyncio.run(main())