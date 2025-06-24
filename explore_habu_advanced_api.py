#!/usr/bin/env python3
"""
Advanced Habu API Explorer
Discover additional endpoints and functionality beyond basic templates/queries
"""

import asyncio
import httpx
import json
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

class HabuAPIExplorer:
    def __init__(self):
        self.client_id = os.getenv('HABU_CLIENT_ID')
        self.client_secret = os.getenv('HABU_CLIENT_SECRET')
        self.base_url = "https://api.habu.com"
        self.token = None
        
    async def authenticate(self):
        """Get authentication token"""
        auth_url = f"{self.base_url}/oauth/token"
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                auth_url,
                data={
                    'grant_type': 'client_credentials',
                    'client_id': self.client_id,
                    'client_secret': self.client_secret
                }
            )
            
            if response.status_code == 200:
                token_data = response.json()
                self.token = token_data.get('access_token')
                print(f"✅ Authentication successful")
                return True
            else:
                print(f"❌ Authentication failed: {response.status_code}")
                print(response.text)
                return False
    
    async def explore_endpoints(self):
        """Systematically explore API endpoints"""
        if not self.token:
            print("❌ Not authenticated")
            return
            
        headers = {'Authorization': f'Bearer {self.token}'}
        
        # Known endpoints to explore further
        endpoints_to_check = [
            # Core functionality
            '/clean-rooms',
            '/partners', 
            '/templates',
            '/queries',
            
            # Advanced features (likely exist)
            '/exports',
            '/exports/list',
            '/exports/download',
            '/results',
            '/analytics',
            '/reports',
            '/dashboards',
            '/workflows',
            '/schedules',
            '/insights',
            '/recommendations',
            
            # Admin/management
            '/users',
            '/organizations', 
            '/permissions',
            '/audit',
            '/metrics',
            
            # Data management
            '/datasets',
            '/schemas',
            '/pipelines',
            '/transformations'
        ]
        
        discoveries = {}
        
        async with httpx.AsyncClient() as client:
            for endpoint in endpoints_to_check:
                try:
                    print(f"🔍 Exploring: {endpoint}")
                    response = await client.get(
                        f"{self.base_url}{endpoint}",
                        headers=headers,
                        timeout=10.0
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        discoveries[endpoint] = {
                            "status": "✅ FOUND",
                            "data_preview": str(data)[:200] + "..." if len(str(data)) > 200 else str(data),
                            "data_type": type(data).__name__,
                            "size": len(str(data))
                        }
                        print(f"  ✅ SUCCESS: Found data ({len(str(data))} chars)")
                        
                    elif response.status_code == 404:
                        discoveries[endpoint] = {"status": "❌ NOT FOUND"}
                        print(f"  ❌ Not found")
                        
                    elif response.status_code == 403:
                        discoveries[endpoint] = {"status": "🔒 FORBIDDEN (exists but no access)"}
                        print(f"  🔒 Forbidden (endpoint exists)")
                        
                    else:
                        discoveries[endpoint] = {
                            "status": f"⚠️ OTHER ({response.status_code})",
                            "error": response.text[:100]
                        }
                        print(f"  ⚠️ Status {response.status_code}")
                        
                except Exception as e:
                    discoveries[endpoint] = {"status": f"💥 ERROR: {str(e)[:50]}"}
                    print(f"  💥 Error: {str(e)[:50]}")
                
                # Be respectful with rate limiting
                await asyncio.sleep(0.5)
        
        return discoveries
    
    async def detailed_exploration(self, endpoint):
        """Deep dive into a specific endpoint"""
        if not self.token:
            return None
            
        headers = {'Authorization': f'Bearer {self.token}'}
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}{endpoint}",
                    headers=headers,
                    timeout=15.0
                )
                
                if response.status_code == 200:
                    return response.json()
                else:
                    return {"error": f"Status {response.status_code}", "detail": response.text}
                    
            except Exception as e:
                return {"error": f"Exception: {str(e)}"}

async def main():
    print("🚀 Advanced Habu API Explorer")
    print("=" * 50)
    
    explorer = HabuAPIExplorer()
    
    # Authenticate
    if not await explorer.authenticate():
        print("❌ Cannot proceed without authentication")
        return
    
    print("\n🔍 Exploring API endpoints...")
    discoveries = await explorer.explore_endpoints()
    
    print("\n📊 DISCOVERY REPORT")
    print("=" * 50)
    
    found_endpoints = []
    forbidden_endpoints = []
    
    for endpoint, info in discoveries.items():
        print(f"{endpoint}: {info['status']}")
        if "✅ FOUND" in info['status']:
            found_endpoints.append(endpoint)
        elif "🔒 FORBIDDEN" in info['status']:
            forbidden_endpoints.append(endpoint)
    
    print(f"\n✅ SUCCESSFULLY ACCESSED ({len(found_endpoints)}):")
    for endpoint in found_endpoints:
        info = discoveries[endpoint]
        print(f"  {endpoint} - {info['data_type']} ({info['size']} chars)")
    
    print(f"\n🔒 FORBIDDEN BUT EXISTS ({len(forbidden_endpoints)}):")
    for endpoint in forbidden_endpoints:
        print(f"  {endpoint} - May need higher permissions")
    
    # Deep dive into found endpoints
    if found_endpoints:
        print(f"\n🔬 DETAILED ANALYSIS")
        print("=" * 30)
        
        for endpoint in found_endpoints[:3]:  # Analyze first 3 found endpoints
            print(f"\n📋 ENDPOINT: {endpoint}")
            details = await explorer.detailed_exploration(endpoint)
            print(json.dumps(details, indent=2)[:500] + "..." if len(str(details)) > 500 else json.dumps(details, indent=2))
    
    # Save report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"habu_api_exploration_{timestamp}.json"
    
    with open(report_file, 'w') as f:
        json.dump({
            "timestamp": timestamp,
            "discoveries": discoveries,
            "summary": {
                "found_count": len(found_endpoints),
                "forbidden_count": len(forbidden_endpoints),
                "found_endpoints": found_endpoints,
                "forbidden_endpoints": forbidden_endpoints
            }
        }, f, indent=2)
    
    print(f"\n💾 Report saved to: {report_file}")
    print("\n🎯 NEXT STEPS:")
    print("1. Review found endpoints for new functionality")
    print("2. Contact Habu support about forbidden endpoints")
    print("3. Implement new MCP tools for discovered features")

if __name__ == "__main__":
    asyncio.run(main())