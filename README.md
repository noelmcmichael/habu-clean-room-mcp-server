# Streamable HTTP MCP Server

This template provides a FastMCP 2.0 implementation of a Model Context Protocol (MCP) server that uses Streamable HTTP protocol to communicate with clients. The MCP Server is designed to be deployed to Render.com. The MCP server exposes tools that can be used by AI assistants through the open MCP standard, with PostgreSQL database integration.

## Project Structure

```
.
├── agents/                 # LLM agents for orchestrating tool calls
│   └── habu_chat_agent.py  # Primary chat agent for Habu integration
├── config/                 # Configuration modules
│   └── habu_config.py      # Habu API credentials and OAuth2 setup
├── tools/                  # MCP tools for external API integration
│   ├── habu_list_partners.py
│   ├── habu_list_templates.py
│   ├── habu_submit_query.py
│   ├── habu_check_status.py
│   └── habu_get_results.py
├── joke_admin_app/          # Flask web app for database management
│   ├── app.py              # Flask application with authentication
│   └── templates/          # HTML templates for web interface
├── .vscode/                # VS Code MCP configuration
│   └── mcp.json            # MCP server configuration for VS Code
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

The server includes multiple tools:
- `tell_joke`: Retrieves random jokes from PostgreSQL database
- `habu_list_partners`: Lists clean room partners from Habu API
- `habu_list_templates`: Lists available query templates
- `habu_submit_query`: Submits clean room queries
- `habu_check_status`: Checks query processing status  
- `habu_get_results`: Retrieves completed query results
- `habu_chat`: Intelligent chat interface for natural language interaction

### 2. Database Layer (`database.py` & `models.py`)

- **database.py**: Configures async SQLAlchemy engine with PostgreSQL support
- **models.py**: Defines database models using SQLAlchemy ORM
- Supports both local development and Render deployment database URLs

### 3. Flask Admin Web App (`joke_admin_app/`)

A Flask web application with authentication for managing database content:
- Flask-Login authentication system
- CRUD operations for database entities
- Web interface for content management

### 4. Habu Clean Room Integration

The server includes comprehensive integration with the Habu Clean Room API:

#### Habu API Tools
- **`habu_list_partners`**: Returns available clean room partners
- **`habu_list_templates`**: Lists query templates for different analysis types
- **`habu_submit_query`**: Submits queries with template ID and parameters
- **`habu_check_status`**: Monitors query processing status
- **`habu_get_results`**: Retrieves completed query results with business summaries

#### Intelligent Chat Agent (`habu_chat_agent.py`)
An LLM-driven agent that provides natural language interface for clean room operations:
- Interprets user intent from conversational prompts
- Routes requests to appropriate API tools
- Maintains context across multi-step workflows
- Formats results in business-friendly summaries

#### Example Interactions
```text
User: "List my clean room partners"
→ Agent calls habu_list_partners() and formats partner list

User: "Run audience overlap analysis between Meta and Amazon"  
→ Agent identifies partners, finds overlap template, submits query, monitors progress

User: "What were the results of my last query?"
→ Agent retrieves and summarizes results with key metrics
```

#### Authentication
Uses OAuth2 client credentials flow:
- **Token URL**: `https://api.habu.com/v1/oauth/token`
- **Base URL**: `https://api.habu.com/v1`
- **Credentials**: Set `HABU_CLIENT_ID` and `HABU_CLIENT_SECRET` in environment variables

API Documentation: [Habu External APIs](https://app.swaggerhub.com/apis/Habu-LiveRamp/External_APIs/Generic)

## Getting Started

### Development Prerequisites

- Python 3.8 or later
- PostgreSQL database (local or cloud)
- pip or uv for package management

### Local Development

1. Clone this repository
2. Copy environment variables:
   ```
   cp .env.sample .env
   ```
3. Update `.env` with your database credentials, API key, and Habu credentials:
   ```
   DATABASE_URL=postgresql://user@localhost:5432/mcp_jokes_dev
   JOKE_MCP_SERVER_API_KEY=your-api-key
   HABU_CLIENT_ID=your_habu_client_id
   HABU_CLIENT_SECRET=your_habu_client_secret
   ```
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
5. Start the MCP server:
   ```
   python main.py
   ```
   
The MCP server will be available locally at `http://localhost:8000/mcp/`

### Testing Your MCP Server

#### Using Visual Studio Code

The recommended way to test your MCP server is using Visual Studio Code with MCP support:

1. **Enable MCP Support**: Follow the [official VS Code MCP documentation](https://code.visualstudio.com/docs/copilot/chat/mcp-servers#_enable-mcp-support-in-vs-code) to enable MCP support in VS Code.

2. **Configure Your Server**: In your VS Code workspace, create a `.vscode/mcp.json` file with the following configuration:

   For local testing:
   ```json
   {
       "servers": {
           "habu-clean-room-server": {
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

3. **Test the Connection**: 
   - Open the CHAT window in VS Code
   - Select **'Agent'** mode
   - Type something like `"tell a joke"` to test the tool functionality


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
    async with AsyncSession(engine, expire_on_commit=False) as db_session:
        # Database operations
        result = await db_session.execute(select(YourModel))
        # Process and return results
        return "Tool result"
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

## Environment Variables

Required environment variables (see `.env.sample`):

- `DATABASE_URL`: PostgreSQL connection string
- `JOKE_MCP_SERVER_API_KEY`: API key for MCP server authentication
- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 8000)

For Flask admin app:
- `FLASK_SECRET_KEY`: Secret key for Flask sessions
- `ADMIN_EMAIL`: Admin login email
- `ADMIN_PASSWORD`: Admin login password

## Resources

- [Model Context Protocol Documentation](https://modelcontextprotocol.io/)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [Render Documentation](https://render.com/docs)
- [Streamable HTTP Transport](https://modelcontextprotocol.io/specification/2025-03-26/basic/transports#streamable-http)
- [Claude Desktop Documentation](https://claude.ai/docs)