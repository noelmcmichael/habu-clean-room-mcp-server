# Streamable HTTP MCP Server

This template provides a FastMCP 2.0 implementation of a Model Context Protocol (MCP) server that uses Streamable HTTP protocol to communicate with clients. The MCP Server is designed to be deployed to Render.com. The MCP server exposes tools that can be used by AI assistants through the open MCP standard, with PostgreSQL database integration.

## Project Structure

```
.
├── joke_admin_app/         # Flask web app for database management
│   ├── app.py              # Flask application with authentication
│   └── templates/          # HTML templates for web interface
├── data/                   # Sample data files
├── .env.sample             # Sample environment variables
├── .gitignore              # Git ignore file
├── database.py             # Async PostgreSQL database configuration
├── main.py                 # FastMCP 2.0 server implementation
├── models.py               # SQLAlchemy database models
├── render.yaml             # Render deployment configuration
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

## Core Components

### 1. FastMCP 2.0 Server Implementation (`main.py`)

This is a complete implementation of the Model Context Protocol using FastMCP 2.0. It supports:

- Streamable HTTP transport protocol
- API key authentication middleware
- Database integration with PostgreSQL
- Tool execution with async database operations
- Automatic database table creation

The server includes a sample tool (`tell_joke`) that retrieves random jokes from a PostgreSQL database.

### 2. Database Layer (`database.py` & `models.py`)

- **database.py**: Configures async SQLAlchemy engine with PostgreSQL support
- **models.py**: Defines database models using SQLAlchemy ORM
- Supports both local development and Render deployment database URLs

### 3. Flask Admin Web App (`joke_admin_app/`)

A Flask web application with authentication for managing database content:
- Flask-Login authentication system
- CRUD operations for database entities
- Web interface for content management

## Getting Started

### Development Prerequisites

- Python 3.8 or later
- PostgreSQL database (local or cloud)
- pip or uv for package management

### Local Development

1. Copy environment variables:
   ```
   cp .env.sample .env
   ```

2. Update `.env` with your database credentials and API key

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Start the MCP server:
   ```
   python main.py
   ```
   
The MCP server will be available locally at `http://localhost:8000/mcp/`

### Testing Your MCP Server

## Deployment

### Deploying to Render.com

#### Option 1: Using render.yaml (Recommended)

1. Push your repository to GitHub
2. Connect your repository to Render
3. Render will automatically detect the `render.yaml` file and create:
   - PostgreSQL database
   - FastMCP server web service
   - Flask admin web app

#### Option 2: Manual Setup

1. Create a PostgreSQL database on Render
2. Create a new web service with:
   - Environment: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python main.py`
3. Set environment variables:
   - `DATABASE_URL`: Connection string from your Render PostgreSQL
   - `JOKE_MCP_SERVER_API_KEY`: Your API key for authentication

After deployment, your MCP server will be available at `https://your-service-name.onrender.com/mcp`

#### Using Visual Studio Code

The recommended way to test your MCP server is using Visual Studio Code with MCP support:

1. **Enable MCP Support**: Follow the [official VS Code MCP documentation](https://code.visualstudio.com/docs/copilot/chat/mcp-servers#_enable-mcp-support-in-vs-code) to enable MCP support in VS Code.

2. **Configure Your Server**: In your VS Code workspace, create a `.vscode/mcp.json` file with the following configuration:

   For local testing:
   ```json
   {
       "servers": {
           "joke-server": {
               "url": "http://localhost:8000/mcp/",
               "headers": {
                   "X-API-Key": "your-api-key"
               }
           }
       }
   }
   ```

   For deployed server:
   ```json
   {
       "servers": {
           "joke-server": {
               "url": "https://your-service-name.onrender.com/mcp/",
               "headers": {
                   "X-API-Key": "your-api-key"
               }
           }
       }
   }
   ```

## Extending the Template

### Adding New Tools

To add a new tool, use the FastMCP decorator in `main.py`:

```python
@mcp_server.tool(
    name="your_new_tool",
    description="Description of what your tool does"
)
async def your_new_tool(param1: str, param2: int = 10) -> str:
    """Your tool implementation here."""
    try:
        # Create a new database session for each tool call
        async with AsyncSession(engine, expire_on_commit=False) as db_session:
            # Database operations
            result = await db_session.execute(select(YourModel))
            # Process and return results
            return "Tool result"
    except Exception as e:
        print(f"Error in your_new_tool: {e}")
        raise RuntimeError(f"An error occurred: {str(e)}") from e
```

### Adding New Database Models

To add a new database model in `models.py`:

```python
class YourNewModel(Base):
    __tablename__ = "your_table"
    
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    # Add more fields as needed
```

### Adding External API Integrations

To integrate with external APIs:

1. Add necessary packages to `requirements.txt`
2. Import and configure clients in your tool functions
3. Make API calls within the tool handler
4. Return processed results

Remember to handle authentication securely using environment variables.

## Resources

- [Model Context Protocol Documentation](https://modelcontextprotocol.io/)
- [FastMCP 2.0 Documentation](https://github.com/jlowin/fastmcp)
- [Render Documentation](https://render.com/docs)
- [Streamable HTTP Transport](https://modelcontextprotocol.io/specification/2025-03-26/basic/transports#streamable-http)