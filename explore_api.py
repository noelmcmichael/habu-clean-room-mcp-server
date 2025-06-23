"""
Explore different API endpoints to find cleanrooms
"""
import asyncio
import httpx
import json
from config.habu_config import habu_config

async def explore_api():
    """Try different endpoints to find cleanrooms"""
    print("🔍 Exploring Habu API Endpoints")
    print("=" * 50)
    
    headers = await habu_config.get_auth_headers()
    base_url = habu_config.base_url
    
    endpoints_to_try = [
        "/cleanrooms",
        "/cleanrooms?limit=100",
        "/cleanrooms?include=all", 
        "/cleanrooms?active=true",
        "/v1/cleanrooms",
        "/organizations/cleanrooms",
        "/user/cleanrooms",
        "/me/cleanrooms",
        "/cleanroom",
        "/cr",
    ]
    
    async with httpx.AsyncClient() as client:
        for endpoint in endpoints_to_try:
            try:
                print(f"\n🔍 Trying: {base_url}{endpoint}")
                response = await client.get(
                    f"{base_url}{endpoint}",
                    headers=headers,
                    timeout=10.0
                )
                
                print(f"Status: {response.status_code}")
                if response.status_code == 200:
                    data = response.json()
                    print(f"Response type: {type(data)}")
                    if isinstance(data, list):
                        print(f"List length: {len(data)}")
                        if data:
                            print(f"First item: {data[0]}")
                    elif isinstance(data, dict):
                        print(f"Keys: {list(data.keys())}")
                        if 'cleanrooms' in data:
                            cleanrooms = data['cleanrooms']
                            print(f"Cleanrooms count: {len(cleanrooms) if isinstance(cleanrooms, list) else 'Not a list'}")
                elif response.status_code == 404:
                    print("Not found")
                else:
                    print(f"Error: {response.text[:200]}")
                    
            except Exception as e:
                print(f"Exception: {e}")
    
    # Also try some user/org endpoints
    org_endpoints = [
        "/user",
        "/me", 
        "/profile",
        "/organization",
        "/org",
    ]
    
    print(f"\n{'='*50}")
    print("Trying user/org endpoints...")
    
    async with httpx.AsyncClient() as client:
        for endpoint in org_endpoints:
            try:
                print(f"\n🔍 Trying: {base_url}{endpoint}")
                response = await client.get(
                    f"{base_url}{endpoint}",
                    headers=headers,
                    timeout=10.0
                )
                
                print(f"Status: {response.status_code}")
                if response.status_code == 200:
                    data = response.json()
                    print(f"Response keys: {list(data.keys()) if isinstance(data, dict) else type(data)}")
                    if isinstance(data, dict) and 'cleanrooms' in str(data).lower():
                        print("Contains cleanroom references!")
                        print(json.dumps(data, indent=2))
                elif response.status_code == 404:
                    print("Not found")
                else:
                    print(f"Error: {response.text[:200]}")
                    
            except Exception as e:
                print(f"Exception: {e}")

if __name__ == "__main__":
    asyncio.run(explore_api())