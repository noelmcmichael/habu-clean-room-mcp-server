"""
Setup Habu credentials from Memex keyring
Securely retrieves credentials and updates .env file
"""
import keyring
import os
from pathlib import Path

def get_secret_safely(secret_name_variations):
    """Try to get secret with various name formats"""
    for name in secret_name_variations:
        try:
            secret = keyring.get_password("memex", name)
            if secret:
                return secret
        except Exception:
            continue
    return None

def setup_habu_credentials():
    """Retrieve Habu credentials from keyring and update .env"""
    print("🔐 Retrieving Habu credentials from Memex keyring...")
    
    # Try various name formats for the client ID
    client_id_variations = [
        "Habu Client ID",
        "habu client id", 
        "HABU_CLIENT_ID",
        "habu_client_id",
        "Habu_Client_ID"
    ]
    
    # Try various name formats for the secret
    secret_variations = [
        "Habu Secret Key",
        "habu secret key",
        "HABU_CLIENT_SECRET", 
        "habu_client_secret",
        "Habu_Secret_Key",
        "Habu Client Secret"
    ]
    
    client_id = get_secret_safely(client_id_variations)
    client_secret = get_secret_safely(secret_variations)
    
    if not client_id:
        print("❌ Could not retrieve Habu Client ID from keyring")
        print("Available variations tried:", client_id_variations)
        return False
        
    if not client_secret:
        print("❌ Could not retrieve Habu Client Secret from keyring") 
        print("Available variations tried:", secret_variations)
        return False
    
    print("✅ Successfully retrieved Habu credentials from keyring")
    
    # Update .env file
    env_path = Path(".env")
    if not env_path.exists():
        print("❌ .env file not found")
        return False
    
    # Read current .env content
    with open(env_path, 'r') as f:
        env_content = f.read()
    
    # Update or add Habu credentials
    lines = env_content.split('\n')
    updated_lines = []
    client_id_updated = False
    client_secret_updated = False
    
    for line in lines:
        if line.startswith('HABU_CLIENT_ID='):
            updated_lines.append(f'HABU_CLIENT_ID={client_id}')
            client_id_updated = True
        elif line.startswith('HABU_CLIENT_SECRET='):
            updated_lines.append(f'HABU_CLIENT_SECRET={client_secret}')
            client_secret_updated = True
        else:
            updated_lines.append(line)
    
    # Add if not found
    if not client_id_updated:
        updated_lines.append(f'HABU_CLIENT_ID={client_id}')
    if not client_secret_updated:
        updated_lines.append(f'HABU_CLIENT_SECRET={client_secret}')
    
    # Write back to .env file
    with open(env_path, 'w') as f:
        f.write('\n'.join(updated_lines))
    
    print("✅ Updated .env file with Habu credentials")
    print("🚀 Habu API integration is now ready!")
    return True

if __name__ == "__main__":
    setup_habu_credentials()