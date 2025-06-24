#!/usr/bin/env python3
"""
Enhanced Habu API Debug Tool
Systematic debugging of cleanroom visibility issue
"""
import asyncio
import logging
import json
from typing import Dict, Any, List
import aiohttp
from utils.habu_auth import get_habu_token
from config.production import production_config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HabuAPIDebugger:
    """Comprehensive debugging tool for Habu API issues"""
    
    def __init__(self):
        self.base_url = "https://app.habu.com/api/v1"
        self.token = None
        self.debug_results = {}
        
    async def authenticate(self) -> bool:
        """Test authentication and get token"""
        try:
            logger.info("🔐 Testing Habu API Authentication...")
            self.token = await get_habu_token()
            if self.token:
                logger.info("✅ Authentication successful")
                return True
            else:
                logger.error("❌ Authentication failed")
                return False
        except Exception as e:
            logger.error(f"❌ Authentication error: {e}")
            return False
    
    async def debug_endpoint(self, endpoint: str, description: str) -> Dict[str, Any]:
        """Debug a specific endpoint with detailed logging"""
        logger.info(f"\n🔍 Testing endpoint: {endpoint}")
        logger.info(f"📝 Description: {description}")
        
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        result = {
            "endpoint": endpoint,
            "description": description,
            "success": False,
            "status_code": None,
            "response_data": None,
            "error": None,
            "headers": {},
            "request_headers": headers.copy()
        }
        
        # Remove token from logged headers for security
        log_headers = headers.copy()
        if "Authorization" in log_headers:
            log_headers["Authorization"] = "Bearer [REDACTED]"
        
        try:
            async with aiohttp.ClientSession() as session:
                logger.info(f"📤 Request headers: {log_headers}")
                
                async with session.get(
                    f"{self.base_url}{endpoint}",
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    result["status_code"] = response.status
                    result["headers"] = dict(response.headers)
                    
                    logger.info(f"📊 Status Code: {response.status}")
                    logger.info(f"📋 Response Headers: {dict(response.headers)}")
                    
                    if response.status == 200:
                        try:
                            data = await response.json()
                            result["response_data"] = data
                            result["success"] = True
                            
                            if isinstance(data, list):
                                logger.info(f"✅ Success: Received list with {len(data)} items")
                                if len(data) == 0:
                                    logger.warning("⚠️  Empty list returned")
                                else:
                                    logger.info(f"📄 First item structure: {list(data[0].keys()) if data[0] else 'None'}")
                            elif isinstance(data, dict):
                                logger.info(f"✅ Success: Received object with keys: {list(data.keys())}")
                            else:
                                logger.info(f"✅ Success: Received data type: {type(data)}")
                                
                        except json.JSONDecodeError as e:
                            text_data = await response.text()
                            result["response_data"] = text_data
                            logger.warning(f"⚠️  JSON decode error: {e}")
                            logger.info(f"📄 Raw response: {text_data[:200]}...")
                    else:
                        error_text = await response.text()
                        result["error"] = error_text
                        logger.error(f"❌ Error {response.status}: {error_text}")
                        
        except asyncio.TimeoutError:
            result["error"] = "Request timeout"
            logger.error("❌ Request timeout")
        except Exception as e:
            result["error"] = str(e)
            logger.error(f"❌ Request failed: {e}")
        
        return result
    
    async def comprehensive_debug(self) -> Dict[str, Any]:
        """Run comprehensive debug analysis"""
        logger.info("🚀 Starting Comprehensive Habu API Debug Session")
        logger.info("=" * 60)
        
        # Test authentication first
        if not await self.authenticate():
            return {"error": "Authentication failed"}
        
        # Define endpoints to test
        endpoints_to_test = [
            {
                "endpoint": "/users/me",
                "description": "Get current user information - should work"
            },
            {
                "endpoint": "/cleanrooms",
                "description": "List cleanrooms - currently returns empty array"
            },
            {
                "endpoint": "/data-connections",
                "description": "List data connections - should work"
            },
            {
                "endpoint": "/cleanrooms?limit=100",
                "description": "List cleanrooms with limit parameter"
            },
            {
                "endpoint": "/cleanrooms?status=active",
                "description": "List active cleanrooms only"
            },
            {
                "endpoint": "/organizations/me",
                "description": "Get user's organization information"
            },
            {
                "endpoint": "/permissions",
                "description": "List user permissions"
            }
        ]
        
        # Test each endpoint
        for endpoint_config in endpoints_to_test:
            result = await debug_endpoint(
                endpoint_config["endpoint"],
                endpoint_config["description"]
            )
            self.debug_results[endpoint_config["endpoint"]] = result
            
            # Small delay between requests
            await asyncio.sleep(1)
        
        # Analyze results
        await self.analyze_results()
        
        return self.debug_results
    
    async def analyze_results(self):
        """Analyze debug results and provide insights"""
        logger.info("\n" + "=" * 60)
        logger.info("🔬 ANALYSIS RESULTS")
        logger.info("=" * 60)
        
        working_endpoints = []
        failing_endpoints = []
        empty_responses = []
        
        for endpoint, result in self.debug_results.items():
            if result["success"]:
                working_endpoints.append(endpoint)
                if (isinstance(result["response_data"], list) and 
                    len(result["response_data"]) == 0):
                    empty_responses.append(endpoint)
            else:
                failing_endpoints.append(endpoint)
        
        logger.info(f"✅ Working endpoints: {len(working_endpoints)}")
        for endpoint in working_endpoints:
            logger.info(f"   - {endpoint}")
        
        logger.info(f"❌ Failing endpoints: {len(failing_endpoints)}")
        for endpoint in failing_endpoints:
            logger.info(f"   - {endpoint}")
        
        logger.info(f"⚠️  Empty response endpoints: {len(empty_responses)}")
        for endpoint in empty_responses:
            logger.info(f"   - {endpoint}")
        
        # Specific cleanroom analysis
        if "/cleanrooms" in self.debug_results:
            cleanroom_result = self.debug_results["/cleanrooms"]
            logger.info("\n🏠 CLEANROOM SPECIFIC ANALYSIS:")
            
            if cleanroom_result["success"]:
                data = cleanroom_result["response_data"]
                if isinstance(data, list) and len(data) == 0:
                    logger.warning("⚠️  Cleanrooms endpoint returns empty array []")
                    logger.info("💡 Possible causes:")
                    logger.info("   1. User has no cleanrooms created")
                    logger.info("   2. User lacks permission to view cleanrooms")
                    logger.info("   3. Cleanrooms are in different organization")
                    logger.info("   4. API endpoint requires additional parameters")
                    logger.info("   5. Database/backend issue on Habu side")
                else:
                    logger.info(f"✅ Found {len(data)} cleanrooms")
            else:
                logger.error(f"❌ Cleanrooms endpoint failed: {cleanroom_result['error']}")
        
        # Compare with working endpoints
        if ("/users/me" in self.debug_results and 
            self.debug_results["/users/me"]["success"]):
            user_data = self.debug_results["/users/me"]["response_data"]
            logger.info(f"\n👤 USER CONTEXT:")
            if isinstance(user_data, dict):
                user_id = user_data.get("id", "Unknown")
                user_email = user_data.get("email", "Unknown")
                logger.info(f"   User ID: {user_id}")
                logger.info(f"   Email: {user_email}")
                
                # Check for organization info
                if "organization" in user_data:
                    org_info = user_data["organization"]
                    logger.info(f"   Organization: {org_info}")
    
    def save_debug_report(self, filename: str = "habu_api_debug_report.json"):
        """Save debug results to file"""
        try:
            with open(filename, 'w') as f:
                json.dump(self.debug_results, f, indent=2, default=str)
            logger.info(f"💾 Debug report saved to {filename}")
        except Exception as e:
            logger.error(f"❌ Failed to save debug report: {e}")

async def main():
    """Main debug function"""
    debugger = HabuAPIDebugger()
    
    try:
        results = await debugger.comprehensive_debug()
        debugger.save_debug_report()
        
        logger.info("\n" + "=" * 60)
        logger.info("🎯 SUMMARY RECOMMENDATIONS")
        logger.info("=" * 60)
        
        if "/cleanrooms" in results and results["/cleanrooms"]["success"]:
            cleanroom_data = results["/cleanrooms"]["response_data"]
            if isinstance(cleanroom_data, list) and len(cleanroom_data) == 0:
                logger.info("📋 Next steps for cleanroom visibility issue:")
                logger.info("1. Check with Habu support about user's cleanroom access")
                logger.info("2. Verify organization membership and permissions")
                logger.info("3. Test creating a new cleanroom via UI")
                logger.info("4. Compare API responses with other users")
                logger.info("5. Check if cleanrooms require specific API version")
        
        logger.info("\n✅ Debug session complete!")
        
    except Exception as e:
        logger.error(f"❌ Debug session failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())