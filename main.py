from dotenv import load_dotenv
load_dotenv() # Load environment variables from .env file

import random
import os
from contextlib import asynccontextmanager

from starlette.applications import Starlette
from starlette.responses import JSONResponse

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastmcp import FastMCP

from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware

# Database imports
from database import engine
from models import Base, Joke

# 1. Lifespan manager for initial database table creation
@asynccontextmanager
async def lifespan(app: Starlette):
    print("MCP Server Lifespan startup. Checking/creating database tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("MCP Server Lifespan startup. Database tables checked/created.")
    yield
    print("MCP Server Lifespan shutdown.")

# 2. Create the MCP server instance
mcp_server = FastMCP(
    name="JokeServer",
    lifespan=lifespan
)

# 3. Create Middleware for API Key Authentication
class ApiKeyAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        if request.url.path == "/":
            return await call_next(request)
        if request.headers.get("X-API-Key") != os.getenv("JOKE_MCP_SERVER_API_KEY"):
            return JSONResponse({"error": "Unauthorized"}, status_code=401)
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

# 5. Run the server
if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000")) 
    
    print(f"Starting FastMCP 2.0 streamable-http server at (/mcp) on {host}:{port}")    
    mcp_server.run(
        transport="streamable-http",
        host=host,
        port=port,
        path="/mcp",
        log_level="debug",
        middleware=[Middleware(ApiKeyAuthMiddleware)]
    )    
