"""
Decode JWT token to see permissions
"""
import base64
import json
from config.habu_config import habu_config

def decode_jwt_payload(token):
    """Decode JWT payload without verification"""
    try:
        # JWT has 3 parts separated by dots
        header, payload, signature = token.split('.')
        
        # Add padding if needed
        payload += '=' * (4 - len(payload) % 4)
        
        # Decode base64
        payload_bytes = base64.urlsafe_b64decode(payload)
        payload_json = json.loads(payload_bytes)
        
        return payload_json
    except Exception as e:
        print(f"Error decoding JWT: {e}")
        return None

async def check_token_permissions():
    """Check what permissions our token has"""
    print("🔍 Checking JWT Token Permissions")
    print("=" * 50)
    
    try:
        headers = await habu_config.get_auth_headers()
        token = headers['Authorization'].replace('Bearer ', '')
        
        payload = decode_jwt_payload(token)
        if payload:
            print("Token Payload:")
            print(json.dumps(payload, indent=2))
            
            print("\nKey Information:")
            print(f"Subject: {payload.get('sub', 'N/A')}")
            print(f"Audience: {payload.get('aud', 'N/A')}")
            print(f"Issuer: {payload.get('iss', 'N/A')}")
            
            if 'scope' in payload:
                scopes = payload['scope'].split(' ')
                print(f"\nScopes ({len(scopes)}):")
                for scope in sorted(scopes):
                    print(f"  • {scope}")
            
            if 'permissions' in payload:
                permissions = payload['permissions']
                print(f"\nPermissions ({len(permissions)}):")
                for perm in sorted(permissions):
                    print(f"  • {perm}")
        else:
            print("Failed to decode token")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    import asyncio
    asyncio.run(check_token_permissions())