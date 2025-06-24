#!/usr/bin/env python3
"""
Discover Advanced Habu Features
Based on actual working endpoints, discover additional API capabilities
"""

import asyncio
import httpx
import json
from datetime import datetime
from typing import Dict, List, Any
from config.habu_config import habu_config

class HabuAdvancedFeatureDiscovery:
    def __init__(self):
        self.base_url = "https://api.habu.com/v1"
        self.discoveries = {}
        self.high_value_findings = []
        
    async def discover_advanced_features(self):
        """Discover advanced features using known working patterns"""
        print("🔍 Discovering Advanced Habu Features")
        print("=" * 50)
        
        headers = await habu_config.get_auth_headers()
        
        discoveries = {}
        
        # Step 1: Explore cleanroom-questions variations
        print("🎯 Step 1: Exploring template/query variations...")
        template_discoveries = await self._explore_template_variations(headers)
        discoveries["template_variations"] = template_discoveries
        
        # Step 2: Explore query-related endpoints
        print("\\n🎯 Step 2: Exploring query management endpoints...")
        query_discoveries = await self._explore_query_variations(headers)
        discoveries["query_variations"] = query_discoveries
        
        # Step 3: Explore export endpoints (already working)
        print("\\n🎯 Step 3: Exploring export management endpoints...")
        export_discoveries = await self._explore_export_variations(headers)
        discoveries["export_variations"] = export_discoveries
        
        # Step 4: Explore organizational endpoints
        print("\\n🎯 Step 4: Exploring organizational endpoints...")
        org_discoveries = await self._explore_organizational_endpoints(headers)
        discoveries["organizational"] = org_discoveries
        
        # Step 5: Look for advanced analytics
        print("\\n🎯 Step 5: Exploring advanced analytics endpoints...")
        analytics_discoveries = await self._explore_analytics_endpoints(headers)
        discoveries["analytics"] = analytics_discoveries
        
        return discoveries
    
    async def _explore_template_variations(self, headers: Dict[str, str]) -> Dict[str, Any]:
        """Explore template and cleanroom-questions variations"""
        
        # Get cleanrooms first
        cleanrooms = await self._get_cleanrooms(headers)
        if not cleanrooms:
            return {"error": "No cleanrooms available"}
        
        cleanroom_id = cleanrooms[0].get('id')
        discoveries = {}
        
        # Known working: /cleanrooms/{id}/cleanroom-questions
        # Let's explore variations
        template_endpoints = [
            f"/cleanrooms/{cleanroom_id}/cleanroom-questions",  # Known working
            f"/cleanrooms/{cleanroom_id}/templates",
            f"/cleanrooms/{cleanroom_id}/question-templates", 
            f"/cleanrooms/{cleanroom_id}/query-templates",
            f"/cleanrooms/{cleanroom_id}/analytics-templates",
            f"/cleanrooms/{cleanroom_id}/template-library",
            f"/cleanrooms/{cleanroom_id}/shared-templates",
            f"/cleanrooms/{cleanroom_id}/public-templates",
            f"/template-library",
            f"/public-templates",
            f"/template-categories",
            f"/template-marketplace"
        ]
        
        async with httpx.AsyncClient() as client:
            for endpoint in template_endpoints:
                result = await self._test_endpoint_safe(client, endpoint, headers)
                discoveries[endpoint] = result
                
                if result.get("accessible"):
                    self.high_value_findings.append({
                        "endpoint": endpoint,
                        "category": "Template Management",
                        "value": "HIGH - Extends current template capabilities"
                    })
                    print(f"  ✅ FOUND: {endpoint}")
                elif result.get("protected"):
                    print(f"  🔒 PROTECTED: {endpoint}")
                
                await asyncio.sleep(0.3)
        
        return discoveries
    
    async def _explore_query_variations(self, headers: Dict[str, str]) -> Dict[str, Any]:
        """Explore query management variations"""
        
        # Known working: /queries, /queries/{id}, /queries/{id}/results
        query_endpoints = [
            "/queries",  # Known working
            "/queries/search",
            "/queries/history", 
            "/queries/scheduled",
            "/queries/running",
            "/queries/completed",
            "/queries/failed",
            "/queries/templates",
            "/queries/library",
            "/query-builder",
            "/query-scheduler",
            "/query-monitor",
            "/query-analytics",
            "/scheduled-queries",
            "/query-history",
            "/query-results",
            "/bulk-queries",
            "/query-batches"
        ]
        
        discoveries = {}
        
        async with httpx.AsyncClient() as client:
            for endpoint in query_endpoints:
                result = await self._test_endpoint_safe(client, endpoint, headers)
                discoveries[endpoint] = result
                
                if result.get("accessible"):
                    self.high_value_findings.append({
                        "endpoint": endpoint,
                        "category": "Query Management",
                        "value": "HIGH - Advanced query capabilities"
                    })
                    print(f"  ✅ FOUND: {endpoint}")
                elif result.get("protected"):
                    print(f"  🔒 PROTECTED: {endpoint}")
                
                await asyncio.sleep(0.3)
        
        return discoveries
    
    async def _explore_export_variations(self, headers: Dict[str, str]) -> Dict[str, Any]:
        """Explore export management variations"""
        
        # Known working: /exports
        export_endpoints = [
            "/exports",  # Known working
            "/exports/search",
            "/exports/history",
            "/exports/scheduled", 
            "/exports/formats",
            "/exports/templates",
            "/exports/bulk",
            "/export-jobs",
            "/download-center",
            "/file-manager",
            "/data-exports",
            "/result-exports",
            "/scheduled-exports",
            "/export-analytics",
            "/export-monitor"
        ]
        
        discoveries = {}
        
        async with httpx.AsyncClient() as client:
            for endpoint in export_endpoints:
                result = await self._test_endpoint_safe(client, endpoint, headers)
                discoveries[endpoint] = result
                
                if result.get("accessible"):
                    self.high_value_findings.append({
                        "endpoint": endpoint,
                        "category": "Export Management", 
                        "value": "HIGH - Enhanced export capabilities"
                    })
                    print(f"  ✅ FOUND: {endpoint}")
                elif result.get("protected"):
                    print(f"  🔒 PROTECTED: {endpoint}")
                
                await asyncio.sleep(0.3)
        
        return discoveries
    
    async def _explore_organizational_endpoints(self, headers: Dict[str, str]) -> Dict[str, Any]:
        """Explore organizational and admin endpoints"""
        
        org_endpoints = [
            "/organizations",
            "/organizations/current",
            "/organization/settings", 
            "/organization/users",
            "/organization/billing",
            "/organization/usage",
            "/organization/limits",
            "/organization/audit-logs",
            "/organization/integrations",
            "/users",
            "/users/current",
            "/user/preferences",
            "/user/profile",
            "/teams",
            "/roles",
            "/permissions",
            "/billing",
            "/usage",
            "/limits",
            "/audit",
            "/activity-logs"
        ]
        
        discoveries = {}
        
        async with httpx.AsyncClient() as client:
            for endpoint in org_endpoints:
                result = await self._test_endpoint_safe(client, endpoint, headers)
                discoveries[endpoint] = result
                
                if result.get("accessible"):
                    self.high_value_findings.append({
                        "endpoint": endpoint,
                        "category": "Organization Management",
                        "value": "MEDIUM - Admin and user management"
                    })
                    print(f"  ✅ FOUND: {endpoint}")
                elif result.get("protected"):
                    print(f"  🔒 PROTECTED: {endpoint}")
                
                await asyncio.sleep(0.3)
        
        return discoveries
    
    async def _explore_analytics_endpoints(self, headers: Dict[str, str]) -> Dict[str, Any]:
        """Explore advanced analytics endpoints"""
        
        analytics_endpoints = [
            "/analytics",
            "/analytics/insights",
            "/analytics/recommendations",
            "/analytics/models",
            "/analytics/predictions",
            "/analytics/forecasts",
            "/insights",
            "/recommendations", 
            "/ml-models",
            "/machine-learning",
            "/predictions",
            "/forecasting",
            "/data-science",
            "/advanced-analytics",
            "/ai-insights",
            "/intelligent-recommendations",
            "/pattern-analysis",
            "/trend-analysis",
            "/anomaly-detection",
            "/clustering",
            "/segmentation",
            "/cohort-analysis"
        ]
        
        discoveries = {}
        
        async with httpx.AsyncClient() as client:
            for endpoint in analytics_endpoints:
                result = await self._test_endpoint_safe(client, endpoint, headers)
                discoveries[endpoint] = result
                
                if result.get("accessible"):
                    self.high_value_findings.append({
                        "endpoint": endpoint,
                        "category": "Advanced Analytics",
                        "value": "VERY HIGH - AI/ML capabilities"
                    })
                    print(f"  ✅ FOUND: {endpoint}")
                elif result.get("protected"):
                    print(f"  🔒 PROTECTED: {endpoint}")
                
                await asyncio.sleep(0.3)
        
        return discoveries
    
    async def _get_cleanrooms(self, headers: Dict[str, str]) -> List[Dict]:
        """Get available cleanrooms"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/cleanrooms", headers=headers, timeout=30.0)
                if response.status_code == 200:
                    return response.json()
                return []
        except:
            return []
    
    async def _test_endpoint_safe(self, client: httpx.AsyncClient, endpoint: str, headers: Dict[str, str]) -> Dict[str, Any]:
        """Safely test an endpoint and return detailed results"""
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
                "response_size": len(response.content)
            }
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    result["data_preview"] = str(data)[:200] + "..." if len(str(data)) > 200 else str(data)
                    result["data_analysis"] = self._analyze_response_data(data)
                    result["business_potential"] = self._assess_business_potential(endpoint, data)
                except:
                    result["content_preview"] = response.text[:200]
                    result["business_potential"] = self._assess_business_potential(endpoint, response.text)
            
            return result
            
        except Exception as e:
            return {
                "error": str(e),
                "accessible": False
            }
    
    def _analyze_response_data(self, data: Any) -> Dict[str, Any]:
        """Analyze response data structure"""
        analysis = {
            "type": type(data).__name__,
            "size": len(str(data)),
            "capabilities": []
        }
        
        if isinstance(data, list):
            analysis["record_count"] = len(data)
            if data and isinstance(data[0], dict):
                analysis["sample_keys"] = list(data[0].keys())[:10]
                
                # Detect capabilities
                keys_str = str(analysis["sample_keys"]).lower()
                if any(term in keys_str for term in ["schedule", "cron", "frequency"]):
                    analysis["capabilities"].append("Scheduling")
                if any(term in keys_str for term in ["export", "download", "file"]):
                    analysis["capabilities"].append("File Management")
                if any(term in keys_str for term in ["insight", "recommendation", "prediction"]):
                    analysis["capabilities"].append("AI/ML Features")
                if any(term in keys_str for term in ["template", "library", "catalog"]):
                    analysis["capabilities"].append("Template Library")
                if any(term in keys_str for term in ["user", "permission", "role"]):
                    analysis["capabilities"].append("User Management")
                if any(term in keys_str for term in ["analytics", "metric", "report"]):
                    analysis["capabilities"].append("Analytics & Reporting")
        
        elif isinstance(data, dict):
            analysis["keys"] = list(data.keys())[:10]
            
            # Detect configuration capabilities
            for key in data.keys():
                if key.lower() in ["settings", "config", "preferences"]:
                    analysis["capabilities"].append("Configuration Management")
                elif key.lower() in ["limits", "quotas", "usage"]:
                    analysis["capabilities"].append("Resource Management")
                elif key.lower() in ["integrations", "connections", "webhooks"]:
                    analysis["capabilities"].append("Integration Management")
        
        return analysis
    
    def _assess_business_potential(self, endpoint: str, data: Any) -> str:
        """Assess business potential of discovered endpoint"""
        endpoint_lower = endpoint.lower()
        data_str = str(data).lower() if data else ""
        
        # Very High Value
        if any(term in endpoint_lower for term in ["analytics", "insight", "recommendation", "prediction", "ml", "ai"]):
            return "🚀 VERY HIGH - Advanced AI/Analytics capabilities"
        elif any(term in endpoint_lower for term in ["export", "download", "file", "result"]) and "bulk" in endpoint_lower:
            return "🚀 VERY HIGH - Bulk data operations"
        
        # High Value  
        elif any(term in endpoint_lower for term in ["schedule", "automation", "batch", "job"]):
            return "🔧 HIGH - Process automation"
        elif any(term in endpoint_lower for term in ["template", "library", "marketplace"]):
            return "📚 HIGH - Template management"
        elif any(term in endpoint_lower for term in ["search", "filter", "query-builder"]):
            return "🔍 HIGH - Enhanced query capabilities"
        
        # Medium Value
        elif any(term in endpoint_lower for term in ["user", "team", "permission", "role"]):
            return "👥 MEDIUM - User management"
        elif any(term in endpoint_lower for term in ["billing", "usage", "limit", "quota"]):
            return "💰 MEDIUM - Resource management"
        
        # Lower Value
        elif any(term in endpoint_lower for term in ["audit", "log", "monitor", "health"]):
            return "📊 LOW - Monitoring & logging"
        
        else:
            return "❓ UNKNOWN - Needs investigation"
    
    async def generate_phase_d_implementation_plan(self, discoveries: Dict) -> str:
        """Generate Phase D implementation plan based on discoveries"""
        
        plan = f"""# 🚀 Phase D Implementation Plan
# Generated from Habu Advanced Feature Discovery
# Discovery Date: {datetime.now().isoformat()}

## 📊 Discovery Summary
- High-value findings: {len([f for f in self.high_value_findings if "HIGH" in f.get("value", "")])}
- Very high-value findings: {len([f for f in self.high_value_findings if "VERY HIGH" in f.get("value", "")])}
- Total new endpoints discovered: {len(self.high_value_findings)}

## 🎯 Priority 1: Very High Value Features
"""
        
        very_high_value = [f for f in self.high_value_findings if "VERY HIGH" in f.get("value", "")]
        for finding in very_high_value:
            plan += f"""
### {finding['endpoint']}
- **Category**: {finding['category']}
- **Business Value**: {finding['value']}
- **Implementation**: Create MCP tool `habu_{finding['endpoint'].split('/')[-1].replace('-', '_')}`
"""
        
        plan += """
## 🔧 Priority 2: High Value Features
"""
        
        high_value = [f for f in self.high_value_findings if f.get("value", "").startswith("🔧 HIGH") or f.get("value", "").startswith("📚 HIGH") or f.get("value", "").startswith("🔍 HIGH")]
        for finding in high_value:
            plan += f"""
### {finding['endpoint']}
- **Category**: {finding['category']}
- **Business Value**: {finding['value']}
- **Implementation**: Enhance existing tools or create new MCP tool
"""
        
        plan += """
## 🛠️ Implementation Steps

### Phase D1: Advanced Analytics Integration (Week 1)
1. Implement AI/ML endpoint tools
2. Add predictive analytics capabilities
3. Enhance chat agent with advanced insights

### Phase D2: Process Automation (Week 2)
1. Add scheduling and automation tools
2. Implement bulk operations
3. Create workflow management features

### Phase D3: Enhanced User Experience (Week 3)
1. Advanced template management
2. Enhanced search and filtering
3. Improved export capabilities

### Phase D4: Integration & Polish (Week 4)
1. User and team management
2. Resource monitoring
3. Complete testing and documentation
"""
        
        return plan
    
    async def save_discovery_results(self, discoveries: Dict, implementation_plan: str):
        """Save discovery results and implementation plan"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save detailed discovery report
        discovery_filename = f"habu_advanced_features_discovery_{timestamp}.json"
        with open(discovery_filename, 'w') as f:
            json.dump({
                "discovery_timestamp": datetime.now().isoformat(),
                "summary": {
                    "total_endpoints_tested": sum(len(cat) for cat in discoveries.values()),
                    "high_value_findings": len(self.high_value_findings),
                    "very_high_value_count": len([f for f in self.high_value_findings if "VERY HIGH" in f.get("value", "")]),
                    "categories_found": list(set([f['category'] for f in self.high_value_findings]))
                },
                "discoveries": discoveries,
                "high_value_findings": self.high_value_findings
            }, f, indent=2, default=str)
        
        # Save implementation plan
        plan_filename = f"phase_d_implementation_plan_{timestamp}.md"
        with open(plan_filename, 'w') as f:
            f.write(implementation_plan)
        
        print(f"💾 Discovery report saved to: {discovery_filename}")
        print(f"📋 Implementation plan saved to: {plan_filename}")
        
        return discovery_filename, plan_filename

async def main():
    print("🎯 Habu Advanced Feature Discovery")
    print("Based on working endpoints and API patterns")
    print("=" * 60)
    
    discovery = HabuAdvancedFeatureDiscovery()
    
    # Run comprehensive discovery
    discoveries = await discovery.discover_advanced_features()
    
    # Generate implementation plan
    print("\\n📋 Generating Phase D Implementation Plan...")
    implementation_plan = await discovery.generate_phase_d_implementation_plan(discoveries)
    
    # Save results
    print("\\n💾 Saving discovery results...")
    discovery_file, plan_file = await discovery.save_discovery_results(discoveries, implementation_plan)
    
    # Final summary
    print("\\n🎯 ADVANCED FEATURE DISCOVERY SUMMARY:")
    print(f"  • High-value findings: {len(discovery.high_value_findings)}")
    print(f"  • Very high-value findings: {len([f for f in discovery.high_value_findings if 'VERY HIGH' in f.get('value', '')])}")
    
    if discovery.high_value_findings:
        print("\\n🚀 TOP DISCOVERIES:")
        for finding in discovery.high_value_findings[:5]:
            endpoint_name = finding['endpoint'].split('/')[-1].upper()
            print(f"  • {endpoint_name} - {finding['value']}")
    
    print(f"\\n📋 FILES CREATED:")
    print(f"  • Discovery Report: {discovery_file}")
    print(f"  • Implementation Plan: {plan_file}")
    
    print("\\n🎯 NEXT STEPS:")
    print("1. Review implementation plan priorities")
    print("2. Start with very high-value endpoints")
    print("3. Implement Phase D features incrementally")
    print("4. Test and integrate with existing system")

if __name__ == "__main__":
    asyncio.run(main())