"""
Production configuration for Habu Clean Room MCP Server
"""
import os
from typing import Optional

class ProductionConfig:
    """Production environment configuration"""
    
    # Server Configuration
    HOST = "0.0.0.0"
    PORT = int(os.getenv("PORT", 8000))
    DEBUG = False
    
    # Database Configuration
    DATABASE_URL = os.getenv("DATABASE_URL")
    if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
        # Render uses postgres:// but SQLAlchemy needs postgresql://
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    
    # API Configuration
    API_KEY = os.getenv("JOKE_MCP_SERVER_API_KEY")
    
    # Habu Configuration
    HABU_CLIENT_ID = os.getenv("HABU_CLIENT_ID")
    HABU_CLIENT_SECRET = os.getenv("HABU_CLIENT_SECRET")
    HABU_USE_MOCK_DATA = os.getenv("HABU_USE_MOCK_DATA", "true").lower() == "true"
    
    # Logging Configuration
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # CORS Configuration
    CORS_ORIGINS = [
        "https://habu-demo-frontend-v2.onrender.com",
        "https://habu-demo-frontend-v2.onrender.com/",
        "https://habu-demo-frontend.onrender.com",
        "https://habu-demo-frontend.onrender.com/",
        "http://localhost:3000",
        "http://localhost:3001"
    ]
    
    @classmethod
    def validate(cls) -> list[str]:
        """Validate required configuration"""
        errors = []
        
        if not cls.DATABASE_URL:
            errors.append("DATABASE_URL is required")
        
        if not cls.API_KEY:
            errors.append("JOKE_MCP_SERVER_API_KEY is required")
        
        if not cls.HABU_USE_MOCK_DATA and not cls.HABU_CLIENT_ID:
            errors.append("HABU_CLIENT_ID is required when not using mock data")
            
        if not cls.HABU_USE_MOCK_DATA and not cls.HABU_CLIENT_SECRET:
            errors.append("HABU_CLIENT_SECRET is required when not using mock data")
        
        return errors

# Global config instance
production_config = ProductionConfig()