"""
Debug Habu API cleanrooms endpoint
"""
import asyncio
import httpx
import json
from config.habu_config import habu_config

async def debug_cleanrooms():
    """Test the cleanrooms endpoint directly"""
    print("🔍 Debugging Habu API Cleanrooms Endpoint")
    print("=" * 50)
    
    try:
        headers = await habu_config.get_auth_headers()
        print(f"Base URL: {habu_config.base_url}")
        print(f"Headers: {headers}")
        
        async with httpx.AsyncClient() as client:
            # Test cleanrooms endpoint
            response = await client.get(
                f"{habu_config.base_url}/cleanrooms",
                headers=headers,
                timeout=30.0
            )
            
            print(f"Status Code: {response.status_code}")
            print(f"Response Headers: {dict(response.headers)}")
            
            if response.status_code == 200:
                cleanrooms_data = response.json()
                print(f"Response Type: {type(cleanrooms_data)}")
                print(f"Raw Response: {json.dumps(cleanrooms_data, indent=2)}")
                
                if isinstance(cleanrooms_data, list):
                    print(f"Number of cleanrooms: {len(cleanrooms_data)}")
                    for i, cleanroom in enumerate(cleanrooms_data):
                        print(f"Cleanroom {i+1}: {cleanroom}")
                elif isinstance(cleanrooms_data, dict):
                    print("Response is a dictionary")
                    if 'cleanrooms' in cleanrooms_data:
                        cleanrooms_list = cleanrooms_data['cleanrooms']
                        print(f"Number of cleanrooms in 'cleanrooms' key: {len(cleanrooms_list)}")
                        for i, cleanroom in enumerate(cleanrooms_list):
                            print(f"Cleanroom {i+1}: {cleanroom}")
                    else:
                        for key, value in cleanrooms_data.items():
                            print(f"Key '{key}': {value}")
            else:
                print(f"Error: {response.status_code}")
                print(f"Error Text: {response.text}")
                
    except Exception as e:
        print(f"Exception: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(debug_cleanrooms())