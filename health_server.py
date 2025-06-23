"""
Health check server that runs alongside the MCP server
"""
import os
import asyncio
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
import uvicorn
from config.production import production_config

async def health_check(request):
    """Health check endpoint for monitoring"""
    return JSONResponse({
        "status": "healthy",
        "service": "Habu Clean Room MCP Server",
        "version": "2.0",
        "mock_mode": production_config.HABU_USE_MOCK_DATA,
        "database_configured": bool(production_config.DATABASE_URL),
        "api_key_configured": bool(production_config.API_KEY)
    })

async def root(request):
    """Root endpoint with basic info"""
    return JSONResponse({
        "service": "Habu Clean Room MCP Server",
        "version": "2.0",
        "mcp_endpoint": "/mcp",
        "health_endpoint": "/health",
        "documentation": "https://github.com/your-org/habu-mcp-server/blob/main/docs/API_DOCUMENTATION.md"
    })

# Create health check app
health_app = Starlette(routes=[
    Route('/', root),
    Route('/health', health_check),
])

if __name__ == "__main__":
    # This can be used for testing the health check separately
    uvicorn.run(health_app, host="0.0.0.0", port=8001)