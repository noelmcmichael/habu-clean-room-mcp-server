"""
Habu Clean Room API Configuration
Handles OAuth2 client credentials flow and API settings
"""
import os
from typing import Optional, Dict, Any
import httpx
from dotenv import load_dotenv

load_dotenv()

class HabuConfig:
    """Configuration and authentication for Habu Clean Room API"""
    
    def __init__(self):
        self.base_url = "https://api.habu.com/v1"
        self.token_url = "https://api.habu.com/v1/oauth/token"
        self.client_id = os.getenv("HABU_CLIENT_ID")
        self.client_secret = os.getenv("HABU_CLIENT_SECRET")
        self._access_token: Optional[str] = None
        self._token_type: str = "Bearer"
    
    async def get_access_token(self) -> str:
        """Get or refresh OAuth2 access token using client credentials flow"""
        if not self.client_id or not self.client_secret:
            raise ValueError("HABU_CLIENT_ID and HABU_CLIENT_SECRET must be set in environment variables")
        
        if self._access_token:
            return self._access_token
        
        async with httpx.AsyncClient() as client:
            data = {
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret
            }
            
            response = await client.post(self.token_url, data=data)
            response.raise_for_status()
            
            token_data = response.json()
            self._access_token = token_data.get("access_token")
            self._token_type = token_data.get("token_type", "Bearer")
            
            if not self._access_token:
                raise ValueError("Failed to obtain access token from Habu API")
            
            return self._access_token
    
    async def get_auth_headers(self) -> Dict[str, str]:
        """Get authenticated headers for API requests"""
        token = await self.get_access_token()
        return {
            "Authorization": f"{self._token_type} {token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    
    def reset_token(self):
        """Reset cached token (force refresh on next request)"""
        self._access_token = None

# Global config instance
habu_config = HabuConfig()