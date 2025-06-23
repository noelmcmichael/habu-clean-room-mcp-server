"""
Debug OAuth2 flow with Habu API
"""
import asyncio
import httpx
import base64
import os
from dotenv import load_dotenv

load_dotenv()

async def debug_oauth():
    """Debug the OAuth2 authentication flow"""
    client_id = os.getenv("HABU_CLIENT_ID")
    client_secret = os.getenv("HABU_CLIENT_SECRET")
    token_url = "https://api.habu.com/v1/oauth/token"
    
    if not client_id or not client_secret:
        print("❌ Missing credentials in environment variables")
        return
    
    print("🔐 Testing OAuth2 Authentication with Habu API")
    print(f"Client ID: {client_id[:8]}...")
    print(f"Token URL: {token_url}")
    
    async with httpx.AsyncClient() as client:
        # Method 1: Basic Auth
        print("\n1️⃣ Trying Basic Authentication...")
        credentials = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
        headers = {
            "Authorization": f"Basic {credentials}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {"grant_type": "client_credentials"}
        
        try:
            response = await client.post(token_url, data=data, headers=headers)
            print(f"Status: {response.status_code}")
            print(f"Headers: {dict(response.headers)}")
            print(f"Response: {response.text[:500]}")
            
            if response.status_code == 200:
                token_data = response.json()
                access_token = token_data.get("accessToken") or token_data.get("access_token")
                if access_token:
                    print("✅ Basic Auth successful!")
                    print(f"Token: {access_token[:50]}...")
                    return access_token
        except Exception as e:
            print(f"❌ Basic Auth error: {e}")
        
        # Method 2: Credentials in body
        print("\n2️⃣ Trying credentials in request body...")
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret
        }
        
        try:
            response = await client.post(token_url, data=data, headers=headers)
            print(f"Status: {response.status_code}")
            print(f"Headers: {dict(response.headers)}")
            print(f"Response: {response.text[:500]}")
            
            if response.status_code == 200:
                token_data = response.json()
                if "access_token" in token_data:
                    print("✅ Body credentials successful!")
                    return token_data["access_token"]
        except Exception as e:
            print(f"❌ Body credentials error: {e}")
        
        # Method 3: JSON body
        print("\n3️⃣ Trying JSON body...")
        headers = {"Content-Type": "application/json"}
        data = {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret
        }
        
        try:
            response = await client.post(token_url, json=data, headers=headers)
            print(f"Status: {response.status_code}")
            print(f"Headers: {dict(response.headers)}")
            print(f"Response: {response.text[:500]}")
            
            if response.status_code == 200:
                token_data = response.json()
                if "access_token" in token_data:
                    print("✅ JSON body successful!")
                    return token_data["access_token"]
        except Exception as e:
            print(f"❌ JSON body error: {e}")
    
    print("\n❌ All authentication methods failed")
    return None

async def test_with_token(token):
    """Test API call with token"""
    if not token:
        print("No token available for API testing")
        return
    
    print(f"\n🧪 Testing API call with token: {token[:20]}...")
    
    async with httpx.AsyncClient() as client:
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        try:
            response = await client.get("https://api.habu.com/v1/cleanrooms", headers=headers)
            print(f"API Status: {response.status_code}")
            print(f"API Response: {response.text[:200]}...")
            
            if response.status_code == 200:
                print("✅ API call successful!")
            else:
                print(f"❌ API call failed: {response.status_code}")
        except Exception as e:
            print(f"❌ API call error: {e}")

if __name__ == "__main__":
    async def main():
        token = await debug_oauth()
        await test_with_token(token)
    
    asyncio.run(main())