from dotenv import load_dotenv
load_dotenv() # Load environment variables from .env file

import random
import os
import logging
from contextlib import asynccontextmanager

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware


from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastmcp import FastMCP

from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware

# Production config
from config.production import production_config

# Database imports
from database import engine
from models import Base, Joke

# Habu tools imports
from tools.habu_list_partners import habu_list_partners
from tools.habu_enhanced_templates import habu_enhanced_templates, habu_list_templates
from tools.habu_submit_query import habu_submit_query
from tools.habu_check_status import habu_check_status
from tools.habu_get_results import habu_get_results
from tools.habu_list_exports import habu_list_exports, habu_download_export
from agents.habu_chat_agent import habu_agent
from agents.enhanced_habu_chat_agent import enhanced_habu_agent

# 1. Configure logging
logging.basicConfig(
    level=getattr(logging, production_config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 2. Validate production configuration
config_errors = production_config.validate()
if config_errors:
    logger.error("Configuration validation failed:")
    for error in config_errors:
        logger.error(f"  - {error}")
    if not production_config.HABU_USE_MOCK_DATA:
        logger.warning("Continuing with mock data enabled due to configuration issues")
        os.environ["HABU_USE_MOCK_DATA"] = "true"

# 3. Lifespan manager for initial database table creation
@asynccontextmanager
async def lifespan(app: Starlette):
    logger.info("MCP Server starting up...")
    logger.info(f"Mock data mode: {production_config.HABU_USE_MOCK_DATA}")
    
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables checked/created successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise
    
    yield
    logger.info("MCP Server shutting down...")

# 4. Create the MCP server instance
mcp_server = FastMCP(
    name="HabuCleanRoomServer",
    lifespan=lifespan
)

# 5. Create Middleware for API Key Authentication with better error handling
class ApiKeyAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # Handle health check endpoint directly
        if request.url.path == "/health":
            return JSONResponse({
                "status": "healthy",
                "service": "Habu Clean Room MCP Server",
                "version": "2.0",
                "mock_mode": production_config.HABU_USE_MOCK_DATA,
                "database_configured": bool(production_config.DATABASE_URL),
                "api_key_configured": bool(production_config.API_KEY)
            })
            
        # Handle root endpoint directly
        if request.url.path == "/":
            return JSONResponse({
                "service": "Habu Clean Room MCP Server",
                "version": "2.0",
                "mcp_endpoint": "/mcp",
                "health_endpoint": "/health",
                "documentation": "Model Context Protocol Server for Habu Clean Room APIs"
            })
        
        # Allow MCP endpoint to proceed to authentication
        if request.url.path.startswith("/mcp"):
            pass  # Continue to auth check below
        
        api_key = request.headers.get("X-API-Key")
        expected_key = production_config.API_KEY
        
        if not expected_key:
            logger.error("API key not configured")
            return JSONResponse(
                {"error": "Server configuration error", "detail": "API authentication not configured"}, 
                status_code=500
            )
        
        if not api_key:
            logger.warning(f"Missing API key for request to {request.url.path}")
            return JSONResponse(
                {"error": "Missing API key", "detail": "X-API-Key header required"}, 
                status_code=401
            )
        
        if api_key != expected_key:
            logger.warning(f"Invalid API key for request to {request.url.path}")
            return JSONResponse(
                {"error": "Invalid API key", "detail": "Provided API key is not valid"}, 
                status_code=401
            )
        
        return await call_next(request)


# 4. Define the tool using the MCP server's decorator, integrated with Postgres
@mcp_server.tool(
    name="tell_joke",
    description="Returns a random joke from the database."
)
async def tell_joke() -> str: # Changed return type to str
    """Returns a random joke from the PostgreSQL database as a string."""
    try:
        # Create a new database session for each tool call
        async with AsyncSession(engine, expire_on_commit=False) as db_session:
            result = await db_session.execute(select(Joke))
            all_jokes = result.scalars().all()

            if not all_jokes:
                raise ValueError("No jokes found in the database.") # FastMCP will report this error

            selected_joke = random.choice(all_jokes)
            joke_text = selected_joke.joke_text
            print(f"Selected joke: {joke_text}")
            
            # Process the joke text (replace newlines with <br>)
            processed_joke = joke_text.replace("\n", "<br>")
            return processed_joke
            
    except Exception as e:
        print(f"Error in tell_joke tool: {e}") # Server-side log
        # Re-raise for FastMCP to handle and send an error to the client
        raise RuntimeError(f"An error occurred while telling a joke: {str(e)}") from e

# 5. Register Habu Clean Room Tools
@mcp_server.tool(
    name="habu_list_partners",
    description="Lists all available clean room partners from the Habu API."
)
async def habu_list_partners_tool() -> str:
    """Lists all available clean room partners."""
    return await habu_list_partners()

@mcp_server.tool(
    name="habu_list_templates", 
    description="Lists all available clean room query templates with enhanced metadata including categories, parameters, data types, and status."
)
async def habu_list_templates_tool() -> str:
    """Lists all available query templates with enhanced metadata."""
    return await habu_list_templates()

@mcp_server.tool(
    name="habu_enhanced_templates",
    description="Advanced template listing with detailed metadata, parameter specifications, categorization, and data type information for better query building."
)
async def habu_enhanced_templates_tool(cleanroom_id: str = None) -> str:
    """Get enhanced template data with full metadata for intelligent query building."""
    return await habu_enhanced_templates(cleanroom_id)

@mcp_server.tool(
    name="habu_submit_query",
    description="Submits a clean room query using a template ID and parameters."
)
async def habu_submit_query_tool(template_id: str, parameters: str = "{}") -> str:
    """Submits a clean room query with template ID and parameters (JSON string)."""
    try:
        import json
        params_dict = json.loads(parameters) if parameters else {}
        return await habu_submit_query(template_id, params_dict)
    except json.JSONDecodeError:
        return json.dumps({
            "status": "error",
            "error": "Invalid parameters format. Please provide valid JSON.",
            "summary": "Parameters must be valid JSON format."
        })

@mcp_server.tool(
    name="habu_check_status",
    description="Checks the processing status of a previously submitted query."
)
async def habu_check_status_tool(query_id: str) -> str:
    """Checks the status of a query by ID."""
    return await habu_check_status(query_id)

@mcp_server.tool(
    name="habu_get_results", 
    description="Retrieves results from a completed clean room query."
)
async def habu_get_results_tool(query_id: str, format_type: str = "json") -> str:
    """Gets results for a completed query."""
    return await habu_get_results(query_id, format_type)

@mcp_server.tool(
    name="habu_list_exports",
    description="Lists available exports from completed analyses. Use this to find completed query results ready for download."
)
async def habu_list_exports_tool(status_filter: str = None) -> str:
    """Lists available exports with optional status filter (READY, PROCESSING, FAILED)."""
    return await habu_list_exports(status_filter)

@mcp_server.tool(
    name="habu_download_export",
    description="Downloads a specific export file containing complete analysis results and data."
)
async def habu_download_export_tool(export_id: str, save_path: str = None) -> str:
    """Downloads an export file by ID with optional save path."""
    return await habu_download_export(export_id, save_path)

@mcp_server.tool(
    name="habu_chat",
    description="Intelligent chat interface for Habu Clean Room operations. Handles natural language requests for running analyses, checking status, and getting results."
)
async def habu_chat_tool(user_request: str) -> str:
    """Process natural language requests for Habu Clean Room operations."""
    return await habu_agent.process_request(user_request)

@mcp_server.tool(
    name="habu_enhanced_chat",
    description="Enhanced LLM-powered natural language interface for Habu Clean Room operations. Uses Claude for intelligent conversation and tool orchestration."
)
async def habu_enhanced_chat_tool(user_message: str) -> str:
    """Enhanced conversational interface with LLM-powered understanding."""
    return await enhanced_habu_agent.process_request(user_message)

@mcp_server.tool(
    name="habu_enable_mock_mode",
    description="Enable mock mode to test Habu functionality with realistic sample data when real cleanrooms aren't available."
)
async def habu_enable_mock_mode(enable: bool = True) -> str:
    """Enable or disable mock mode for testing Habu functionality."""
    import os
    import json
    
    if enable:
        os.environ["HABU_USE_MOCK_DATA"] = "true"
        return json.dumps({
            "status": "success", 
            "message": "Mock mode enabled! All Habu tools will now return realistic sample data for testing.",
            "mock_data_available": {
                "cleanrooms": 2,
                "partners": 5, 
                "templates": 5
            }
        }, indent=2)
    else:
        os.environ["HABU_USE_MOCK_DATA"] = "false"
        return json.dumps({
            "status": "success",
            "message": "Mock mode disabled. Tools will use real Habu API endpoints."
        }, indent=2)

# 6. Run the server with FastMCP
if __name__ == "__main__":
    logger.info(f"Starting Habu Clean Room MCP Server")
    logger.info(f"Host: {production_config.HOST}")
    logger.info(f"Port: {production_config.PORT}")
    logger.info(f"Mock Mode: {production_config.HABU_USE_MOCK_DATA}")
    
    try:
        mcp_server.run(
            transport="streamable-http",
            host=production_config.HOST,
            port=production_config.PORT,
            path="/mcp",
            log_level=production_config.LOG_LEVEL.lower(),
            middleware=[
                Middleware(CORSMiddleware, 
                          allow_origins=production_config.CORS_ORIGINS,
                          allow_credentials=True,
                          allow_methods=["*"],
                          allow_headers=["*"]),
                Middleware(ApiKeyAuthMiddleware)
            ]
        )
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        raise    
