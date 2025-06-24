#!/usr/bin/env python3
"""
Phase 1: Baseline API Testing & Verification
Comprehensive test of Habu API to establish what works and what doesn't
"""
import asyncio
import logging
import json
import os
from datetime import datetime
from typing import Dict, Any, List, Optional
import httpx
from config.habu_config import HabuConfig

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class HabuBaselineTest:
    """Comprehensive baseline testing for Habu API"""
    
    def __init__(self):
        self.config = HabuConfig()
        self.test_results = {
            "timestamp": datetime.now().isoformat(),
            "authentication": {},
            "endpoints": {},
            "cleanroom_analysis": {},
            "summary": {}
        }
    
    async def run_all_tests(self):
        """Run complete baseline test suite"""
        logger.info("🚀 Starting Phase 1: Baseline API Testing")
        
        # Test 1: Authentication
        auth_success = await self.test_authentication()
        if not auth_success:
            logger.error("❌ Authentication failed - cannot proceed with API tests")
            return self.test_results
        
        # Test 2: Known working endpoints
        await self.test_known_endpoints()
        
        # Test 3: Cleanroom endpoint deep dive
        await self.test_cleanroom_endpoint()
        
        # Test 4: Generate summary
        self.generate_summary()
        
        # Save results
        await self.save_results()
        
        return self.test_results
    
    async def test_authentication(self) -> bool:
        """Test OAuth2 authentication and token analysis"""
        logger.info("\n🔐 Phase 1.1: Authentication Verification")
        
        try:
            # Test token acquisition
            token = await self.config.get_access_token()
            
            if token:
                logger.info("✅ OAuth2 token acquired successfully")
                
                # Analyze JWT token (if it's a JWT)
                token_info = await self.analyze_jwt_token(token)
                
                self.test_results["authentication"] = {
                    "success": True,
                    "token_acquired": True,
                    "token_length": len(token),
                    "token_prefix": token[:20] + "..." if len(token) > 20 else token,
                    "token_analysis": token_info,
                    "client_id": self.config.client_id[:8] + "..." if self.config.client_id else None,
                    "base_url": self.config.base_url,
                    "token_url": self.config.token_url
                }
                return True
            else:
                logger.error("❌ Failed to acquire access token")
                self.test_results["authentication"] = {
                    "success": False,
                    "error": "Failed to acquire access token"
                }
                return False
                
        except Exception as e:
            logger.error(f"❌ Authentication error: {e}")
            self.test_results["authentication"] = {
                "success": False,
                "error": str(e)
            }
            return False
    
    async def analyze_jwt_token(self, token: str) -> Dict[str, Any]:
        """Analyze JWT token structure (if applicable)"""
        try:
            import base64
            # Check if it's a JWT (has 3 parts separated by dots)
            if token.count('.') == 2:
                header, payload, signature = token.split('.')
                
                # Decode header and payload (add padding if needed)
                def decode_b64(data):
                    padding = 4 - len(data) % 4
                    if padding != 4:
                        data += '=' * padding
                    return base64.urlsafe_b64decode(data)
                
                header_data = json.loads(decode_b64(header))
                payload_data = json.loads(decode_b64(payload))
                
                return {
                    "is_jwt": True,
                    "header": header_data,
                    "payload": {
                        "sub": payload_data.get("sub"),
                        "aud": payload_data.get("aud"),
                        "iss": payload_data.get("iss"),
                        "exp": payload_data.get("exp"),
                        "iat": payload_data.get("iat"),
                        "scope": payload_data.get("scope"),
                        "permissions": payload_data.get("permissions", [])
                    }
                }
            else:
                return {
                    "is_jwt": False,
                    "token_type": "opaque"
                }
        except Exception as e:
            return {
                "is_jwt": False,
                "analysis_error": str(e)
            }
    
    async def test_known_endpoints(self):
        """Test endpoints that should work based on previous success"""
        logger.info("\n📡 Phase 1.2: Known Working Endpoints Test")
        
        endpoints_to_test = [
            ("/users", "List users", "GET"),
            ("/data-connections", "List data connections", "GET"),
            ("/me", "Current user profile", "GET"),
            ("/profile", "User profile", "GET"),
            ("/organizations", "List organizations", "GET"),
            ("/projects", "List projects", "GET"),
            ("/workspaces", "List workspaces", "GET"),
        ]
        
        for endpoint, description, method in endpoints_to_test:
            result = await self.test_endpoint(endpoint, description, method)
            self.test_results["endpoints"][endpoint] = result
    
    async def test_endpoint(self, endpoint: str, description: str, method: str = "GET") -> Dict[str, Any]:
        """Test a specific API endpoint"""
        logger.info(f"  Testing {method} {endpoint} - {description}")
        
        try:
            token = await self.config.get_access_token()
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            
            url = f"{self.config.base_url}{endpoint}"
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                if method == "GET":
                    response = await client.get(url, headers=headers)
                elif method == "POST":
                    response = await client.post(url, headers=headers, json={})
                else:
                    response = await client.request(method, url, headers=headers)
                
                result = {
                    "success": response.status_code < 400,
                    "status_code": response.status_code,
                    "headers": dict(response.headers),
                    "response_size": len(response.content),
                    "url": url
                }
                
                try:
                    response_data = response.json()
                    result["response_type"] = "json"
                    result["response_structure"] = self.analyze_response_structure(response_data)
                    
                    # Store sample of response (first few items if it's a list)
                    if isinstance(response_data, list):
                        result["sample_response"] = response_data[:2] if response_data else []
                        result["total_items"] = len(response_data)
                    else:
                        result["sample_response"] = response_data
                        
                except:
                    result["response_type"] = "non-json"
                    result["response_text"] = response.text[:500] if response.text else ""
                
                if result["success"]:
                    logger.info(f"    ✅ {response.status_code} - Success")
                else:
                    logger.warning(f"    ❌ {response.status_code} - Failed")
                
                return result
                
        except Exception as e:
            logger.error(f"    ❌ Exception: {e}")
            return {
                "success": False,
                "error": str(e),
                "url": f"{self.config.base_url}{endpoint}"
            }
    
    def analyze_response_structure(self, data) -> Dict[str, Any]:
        """Analyze the structure of an API response"""
        if isinstance(data, list):
            return {
                "type": "array",
                "length": len(data),
                "item_structure": self.analyze_response_structure(data[0]) if data else None
            }
        elif isinstance(data, dict):
            return {
                "type": "object",
                "keys": list(data.keys()),
                "key_count": len(data.keys())
            }
        else:
            return {
                "type": type(data).__name__,
                "value": str(data)[:100] if str(data) else None
            }
    
    async def test_cleanroom_endpoint(self):
        """Deep dive testing of cleanroom endpoint"""
        logger.info("\n🏢 Phase 1.3: Cleanroom Endpoint Deep Dive")
        
        # Test various cleanroom endpoint variations
        cleanroom_endpoints = [
            ("/cleanrooms", "Base cleanrooms endpoint"),
            ("/cleanrooms?limit=10", "Cleanrooms with limit parameter"),
            ("/cleanrooms?offset=0", "Cleanrooms with offset parameter"),
            ("/cleanrooms?status=active", "Cleanrooms filtered by status"),
            ("/v1/cleanrooms", "Cleanrooms with explicit v1"),
            ("/v2/cleanrooms", "Cleanrooms with v2 (if exists)"),
        ]
        
        cleanroom_results = {}
        
        for endpoint, description in cleanroom_endpoints:
            result = await self.test_endpoint(endpoint, description, "GET")
            cleanroom_results[endpoint] = result
            
            # Special analysis for cleanroom responses
            if result["success"] and "sample_response" in result:
                if isinstance(result["sample_response"], list) and len(result["sample_response"]) == 0:
                    logger.warning(f"    ⚠️  {endpoint} returned empty array []")
                elif isinstance(result["sample_response"], list) and len(result["sample_response"]) > 0:
                    logger.info(f"    ✅ {endpoint} returned {len(result['sample_response'])} cleanrooms")
        
        self.test_results["cleanroom_analysis"] = {
            "endpoints_tested": cleanroom_results,
            "empty_responses": [ep for ep, result in cleanroom_results.items() 
                              if result.get("success") and 
                              isinstance(result.get("sample_response"), list) and 
                              len(result.get("sample_response", [])) == 0],
            "successful_responses": [ep for ep, result in cleanroom_results.items() 
                                   if result.get("success") and 
                                   isinstance(result.get("sample_response"), list) and 
                                   len(result.get("sample_response", [])) > 0]
        }
    
    def generate_summary(self):
        """Generate test summary and recommendations"""
        summary = {
            "authentication_status": self.test_results["authentication"]["success"],
            "working_endpoints": [],
            "failing_endpoints": [],
            "cleanroom_status": "unknown",
            "recommendations": []
        }
        
        # Analyze endpoint results
        for endpoint, result in self.test_results["endpoints"].items():
            if result["success"]:
                summary["working_endpoints"].append(endpoint)
            else:
                summary["failing_endpoints"].append(endpoint)
        
        # Analyze cleanroom situation
        empty_cleanroom_endpoints = self.test_results["cleanroom_analysis"]["empty_responses"]
        successful_cleanroom_endpoints = self.test_results["cleanroom_analysis"]["successful_responses"]
        
        if successful_cleanroom_endpoints:
            summary["cleanroom_status"] = "accessible"
        elif empty_cleanroom_endpoints:
            summary["cleanroom_status"] = "empty_response"
        else:
            summary["cleanroom_status"] = "inaccessible"
        
        # Generate recommendations
        if summary["authentication_status"]:
            summary["recommendations"].append("Authentication is working correctly")
        
        if summary["working_endpoints"]:
            summary["recommendations"].append(f"API connectivity confirmed - {len(summary['working_endpoints'])} endpoints working")
        
        if summary["cleanroom_status"] == "empty_response":
            summary["recommendations"].append("Cleanroom endpoints respond but return empty arrays - may need cleanroom creation")
        elif summary["cleanroom_status"] == "inaccessible":
            summary["recommendations"].append("Cleanroom endpoints are not accessible - check permissions or API structure")
        
        self.test_results["summary"] = summary
        
        logger.info(f"\n📊 Test Summary:")
        logger.info(f"  Authentication: {'✅' if summary['authentication_status'] else '❌'}")
        logger.info(f"  Working endpoints: {len(summary['working_endpoints'])}")
        logger.info(f"  Failing endpoints: {len(summary['failing_endpoints'])}")
        logger.info(f"  Cleanroom status: {summary['cleanroom_status']}")
    
    async def save_results(self):
        """Save test results to file"""
        filename = f"phase1_baseline_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            with open(filename, 'w') as f:
                json.dump(self.test_results, f, indent=2, default=str)
            logger.info(f"📁 Results saved to {filename}")
        except Exception as e:
            logger.error(f"Failed to save results: {e}")

async def main():
    """Run Phase 1 baseline testing"""
    tester = HabuBaselineTest()
    results = await tester.run_all_tests()
    
    print("\n" + "="*60)
    print("PHASE 1 BASELINE TEST COMPLETE")
    print("="*60)
    
    summary = results["summary"]
    print(f"Authentication: {'✅ Working' if summary['authentication_status'] else '❌ Failed'}")
    print(f"Working endpoints: {len(summary['working_endpoints'])}")
    print(f"Failing endpoints: {len(summary['failing_endpoints'])}")
    print(f"Cleanroom status: {summary['cleanroom_status']}")
    
    print("\nRecommendations:")
    for rec in summary["recommendations"]:
        print(f"  • {rec}")
    
    return results

if __name__ == "__main__":
    asyncio.run(main())