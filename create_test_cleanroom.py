"""
Create a test cleanroom with proper fields
"""
import asyncio
import httpx
import json
from datetime import datetime, timedelta
from config.habu_config import habu_config

async def create_test_cleanroom():
    """Create a test cleanroom with all required fields"""
    print("🔍 Creating Test Cleanroom")
    print("=" * 40)
    
    headers = await habu_config.get_auth_headers()
    base_url = habu_config.base_url
    
    async with httpx.AsyncClient() as client:
        
        # Try different variations of cleanroom creation
        start_date = datetime.now().isoformat()
        end_date = (datetime.now() + timedelta(days=30)).isoformat()
        
        cleanroom_variations = [
            {
                "name": "API Test Cleanroom 1",
                "description": "Test cleanroom created via API",
                "startDate": start_date,
                "endDate": end_date
            },
            {
                "name": "API Test Cleanroom 2", 
                "description": "Test cleanroom created via API",
                "start_date": start_date,
                "end_date": end_date
            },
            {
                "name": "API Test Cleanroom 3",
                "description": "Test cleanroom created via API", 
                "startDate": start_date
            },
            {
                "name": "API Test Cleanroom 4",
                "description": "Test cleanroom created via API",
                "start_date": start_date
            },
        ]
        
        for i, cleanroom_data in enumerate(cleanroom_variations, 1):
            print(f"\n{i}. Trying variation {i}:")
            print(f"   Data: {json.dumps(cleanroom_data, indent=2)}")
            
            try:
                response = await client.post(
                    f"{base_url}/cleanrooms",
                    headers=headers,
                    json=cleanroom_data,
                    timeout=15.0
                )
                
                print(f"   Status: {response.status_code}")
                response_text = response.text
                
                if response.status_code in [200, 201]:
                    print("   ✅ SUCCESS! Cleanroom created")
                    try:
                        created_cleanroom = response.json()
                        print(f"   Created cleanroom: {json.dumps(created_cleanroom, indent=2)}")
                    except:
                        print(f"   Response: {response_text}")
                    
                    # Now check if we can list it
                    print("\n   Checking if cleanroom appears in list...")
                    list_response = await client.get(f"{base_url}/cleanrooms", headers=headers, timeout=10.0)
                    if list_response.status_code == 200:
                        cleanrooms = list_response.json()
                        print(f"   ✅ Now showing {len(cleanrooms)} cleanrooms in list")
                        if cleanrooms:
                            for cr in cleanrooms:
                                print(f"     - {cr.get('name', 'Unknown')}: {cr.get('id', 'No ID')}")
                    
                    # Don't try more variations if one works
                    break
                    
                else:
                    print(f"   ❌ Failed with status {response.status_code}")
                    try:
                        error_data = json.loads(response_text)
                        print(f"   Error: {error_data.get('message', 'Unknown error')}")
                    except:
                        print(f"   Raw error: {response_text[:200]}")
                        
            except Exception as e:
                print(f"   ❌ Exception: {e}")
        
        # Final check - list all cleanrooms
        print(f"\n" + "="*40)
        print("Final cleanroom list check:")
        try:
            response = await client.get(f"{base_url}/cleanrooms", headers=headers, timeout=10.0)
            if response.status_code == 200:
                cleanrooms = response.json()
                print(f"✅ Total cleanrooms found: {len(cleanrooms)}")
                for i, cr in enumerate(cleanrooms, 1):
                    print(f"  {i}. {cr.get('name', 'Unnamed')} (ID: {cr.get('id', 'No ID')})")
                    print(f"     Description: {cr.get('description', 'No description')}")
                    print(f"     Status: {cr.get('status', 'Unknown')}")
            else:
                print(f"❌ Failed to list cleanrooms: {response.status_code}")
        except Exception as e:
            print(f"❌ Error listing cleanrooms: {e}")

if __name__ == "__main__":
    asyncio.run(create_test_cleanroom())