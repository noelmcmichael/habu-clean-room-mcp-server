"""
Combined server that runs both MCP server and health check endpoints
"""
import asyncio
import threading
import uvicorn
from main import mcp_server
from health_server import health_app
from config.production import production_config
import logging

logger = logging.getLogger(__name__)

def run_health_server():
    """Run health check server on a separate port"""
    health_port = production_config.PORT + 1
    logger.info(f"Starting health check server on port {health_port}")
    uvicorn.run(
        health_app, 
        host=production_config.HOST, 
        port=health_port,
        log_level=production_config.LOG_LEVEL.lower()
    )

def run_mcp_server():
    """Run MCP server"""
    logger.info(f"Starting MCP server on port {production_config.PORT}")
    mcp_server.run(
        transport="streamable-http",
        host=production_config.HOST,
        port=production_config.PORT,
        path="/mcp",
        log_level=production_config.LOG_LEVEL.lower()
    )

if __name__ == "__main__":
    logger.info("Starting combined MCP + Health Check server")
    
    # Start health server in a separate thread
    health_thread = threading.Thread(target=run_health_server)
    health_thread.daemon = True
    health_thread.start()
    
    # Run MCP server in main thread
    run_mcp_server()