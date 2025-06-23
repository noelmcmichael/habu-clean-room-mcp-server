"""
Check users endpoint and try to create a cleanroom
"""
import asyncio
import httpx
import json
from config.habu_config import habu_config

async def check_users_and_create():
    """Check users and try to create a cleanroom"""
    print("🔍 Checking Users and Testing Cleanroom Creation")
    print("=" * 60)
    
    headers = await habu_config.get_auth_headers()
    base_url = habu_config.base_url
    
    async with httpx.AsyncClient() as client:
        
        # 1. Check what users endpoint returns
        print("1. Checking /users endpoint:")
        print("-" * 30)
        
        try:
            response = await client.get(f"{base_url}/users", headers=headers, timeout=10.0)
            if response.status_code == 200:
                users_data = response.json()
                print(f"Users data: {json.dumps(users_data, indent=2)}")
            else:
                print(f"Error: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Error: {e}")
        
        # 2. Check what happens when we try to create a cleanroom
        print(f"\n2. Testing cleanroom creation:")
        print("-" * 30)
        
        # Try a minimal cleanroom creation request
        test_cleanroom = {
            "name": "API Test Cleanroom",
            "description": "Test cleanroom created via API to verify connectivity"
        }
        
        try:
            response = await client.post(
                f"{base_url}/cleanrooms",
                headers=headers,
                json=test_cleanroom,
                timeout=10.0
            )
            
            print(f"Creation attempt status: {response.status_code}")
            response_data = response.text
            print(f"Response: {response_data}")
            
            if response.status_code == 201 or response.status_code == 200:
                print("✅ Cleanroom created successfully!")
                # Now try to list cleanrooms again
                list_response = await client.get(f"{base_url}/cleanrooms", headers=headers, timeout=10.0)
                if list_response.status_code == 200:
                    cleanrooms = list_response.json()
                    print(f"✅ Now showing {len(cleanrooms)} cleanrooms")
                    if cleanrooms:
                        print(f"First cleanroom: {cleanrooms[0]}")
            else:
                # Parse the error to understand what fields are required
                try:
                    error_data = json.loads(response_data)
                    print(f"Error details: {json.dumps(error_data, indent=2)}")
                except:
                    print(f"Raw error: {response_data}")
                    
        except Exception as e:
            print(f"Error creating cleanroom: {e}")
        
        # 3. Try to get schema/documentation
        print(f"\n3. Testing API schema endpoints:")
        print("-" * 30)
        
        schema_endpoints = [
            "/swagger",
            "/docs", 
            "/api-docs",
            "/openapi.json",
            "/schema",
            "/.well-known/openapi",
        ]
        
        for endpoint in schema_endpoints:
            try:
                response = await client.get(f"{base_url}{endpoint}", headers=headers, timeout=5.0)
                if response.status_code == 200:
                    print(f"✅ Found schema at {endpoint}")
                    content_type = response.headers.get('content-type', '')
                    if 'json' in content_type:
                        try:
                            schema_data = response.json()
                            if 'paths' in schema_data and '/cleanrooms' in str(schema_data):
                                print("✅ Contains cleanrooms API documentation")
                        except:
                            pass
                else:
                    print(f"  {endpoint} -> {response.status_code}")
            except Exception as e:
                print(f"  {endpoint} -> ERROR")

if __name__ == "__main__":
    asyncio.run(check_users_and_create())