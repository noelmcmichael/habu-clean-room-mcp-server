"""
Decode the user and org fields from the JWT token
"""
import base64
import json
from config.habu_config import habu_config

def decode_base64_field(encoded_value):
    """Decode base64 encoded field"""
    try:
        # Add padding if needed
        encoded_value += '=' * (4 - len(encoded_value) % 4)
        decoded_bytes = base64.urlsafe_b64decode(encoded_value)
        decoded_str = decoded_bytes.decode('utf-8')
        return decoded_str
    except Exception as e:
        print(f"Error decoding: {e}")
        return None

async def decode_user_org():
    """Decode user and org info from JWT"""
    print("🔍 Decoding User and Organization Info")
    print("=" * 50)
    
    try:
        headers = await habu_config.get_auth_headers()
        token = headers['Authorization'].replace('Bearer ', '')
        
        # Decode JWT payload
        header, payload, signature = token.split('.')
        payload += '=' * (4 - len(payload) % 4)
        payload_bytes = base64.urlsafe_b64decode(payload)
        payload_json = json.loads(payload_bytes)
        
        # Extract and decode user and org
        user_encoded = payload_json.get("https://api.habu.com/user")
        org_encoded = payload_json.get("https://api.habu.com/org")
        
        if user_encoded:
            user_decoded = decode_base64_field(user_encoded)
            print(f"User (encoded): {user_encoded}")
            print(f"User (decoded): {user_decoded}")
        
        if org_encoded:
            org_decoded = decode_base64_field(org_encoded)
            print(f"Org (encoded): {org_encoded}")
            print(f"Org (decoded): {org_decoded}")
        
        # Check if this matches what you expect
        print(f"\nAPI Client ID: {payload_json.get('sub', 'N/A')}")
        print(f"Audience: {payload_json.get('aud', 'N/A')}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    import asyncio
    asyncio.run(decode_user_org())