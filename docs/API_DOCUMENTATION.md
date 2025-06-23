# Habu Clean Room MCP Server API Documentation

## Overview

The Habu Clean Room MCP Server provides Model Context Protocol (MCP) 2.0 integration for Habu's clean room data collaboration platform. It enables AI assistants to interact with clean room analytics through natural language.

## Architecture

```
AI Assistant (VS Code/Copilot) 
    ↓ MCP Protocol
FastMCP 2.0 Server (Port 8000)
    ↓ API Calls
Habu Clean Room API
    ↓ Database
PostgreSQL Database
```

## Deployment URLs

### Production (Render.com)
- **MCP Server**: `https://habu-mcp-server.onrender.com/mcp/`
- **Demo API**: `https://habu-demo-api.onrender.com/api/`
- **React Frontend**: `https://habu-demo-frontend.onrender.com/`
- **Admin Interface**: `https://habu-admin-app.onrender.com/`

### Local Development
- **MCP Server**: `http://localhost:8000/mcp/`
- **Demo API**: `http://localhost:5001/api/`
- **React Frontend**: `http://localhost:3001/`

## Authentication

### API Key Authentication
All MCP requests require the `X-API-Key` header:
```http
X-API-Key: your-api-key-here
```

### Habu API Credentials
The server uses OAuth2 client credentials flow:
- `HABU_CLIENT_ID`: Your Habu client ID
- `HABU_CLIENT_SECRET`: Your Habu client secret

## MCP Tools

### 1. habu_list_partners
Lists all available clean room partners.

**Usage:**
```
@habu-clean-room-server habu_list_partners
```

**Response:**
```json
{
  "status": "success",
  "count": 5,
  "partners": [...],
  "summary": "Found 5 clean room partners"
}
```

### 2. habu_list_templates
Lists all available query templates.

**Usage:**
```
@habu-clean-room-server habu_list_templates
```

**Response:**
```json
{
  "status": "success",
  "count": 8,
  "templates": [...],
  "summary": "Found 8 query templates"
}
```

### 3. habu_submit_query
Submits a clean room query using a template.

**Parameters:**
- `template_id` (required): Template identifier
- `parameters` (optional): JSON string of query parameters

**Usage:**
```
@habu-clean-room-server habu_submit_query --template_id="audience_overlap" --parameters='{"partner_1": "meta", "partner_2": "amazon"}'
```

**Response:**
```json
{
  "status": "success",
  "query_id": "abc123",
  "estimated_completion": "2-3 minutes"
}
```

### 4. habu_check_status
Checks the processing status of a submitted query.

**Parameters:**
- `query_id` (required): Query identifier

**Usage:**
```
@habu-clean-room-server habu_check_status --query_id="abc123"
```

**Response:**
```json
{
  "status": "success",
  "query_status": "completed",
  "progress": 100,
  "results_available": true
}
```

### 5. habu_get_results
Retrieves results from a completed query.

**Parameters:**
- `query_id` (required): Query identifier
- `format_type` (optional): "json" or "csv" (default: "json")

**Usage:**
```
@habu-clean-room-server habu_get_results --query_id="abc123"
```

**Response:**
```json
{
  "status": "success",
  "results": {...},
  "insights": [...],
  "recommendations": [...]
}
```

### 6. habu_enhanced_chat
Natural language interface powered by OpenAI GPT-4.

**Parameters:**
- `user_message` (required): Natural language request

**Usage:**
```
@habu-clean-room-server habu_enhanced_chat "Show me audience overlap between Meta and Amazon"
```

**Response:**
Natural language response with executed actions and results.

### 7. habu_enable_mock_mode
Enable/disable mock data mode for testing.

**Parameters:**
- `enable` (optional): Boolean (default: true)

**Usage:**
```
@habu-clean-room-server habu_enable_mock_mode
```

## Demo API Endpoints

### POST /api/enhanced-chat
Bridge endpoint for React frontend.

**Request:**
```json
{
  "user_input": "List my clean room partners"
}
```

**Response:**
```json
{
  "response": "Here are your available clean room partners: ..."
}
```

### GET /api/health
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "Habu Demo API",
  "version": "2.0",
  "openai_configured": true,
  "mock_mode": true
}
```

## Error Handling

### Error Response Format
```json
{
  "status": "error",
  "error_type": "APIError",
  "error_code": "API_ERROR",
  "message": "Human-readable error message",
  "summary": "Brief summary for LLM consumption"
}
```

### Error Types
- **APIError**: API-related errors (HTTP errors, invalid responses)
- **AuthenticationError**: Authentication failures
- **NetworkError**: Network connectivity issues
- **ConfigurationError**: Server configuration problems

### Circuit Breaker
The system implements circuit breaker pattern for resilience:
- **Habu API**: 3 failures → 30 second cooldown
- **OpenAI API**: 5 failures → 60 second cooldown

## Configuration

### Environment Variables

#### Required
- `DATABASE_URL`: PostgreSQL connection string
- `JOKE_MCP_SERVER_API_KEY`: API key for MCP authentication

#### Optional
- `HABU_CLIENT_ID`: Habu API client ID
- `HABU_CLIENT_SECRET`: Habu API client secret
- `HABU_USE_MOCK_DATA`: Enable mock mode (default: "false")
- `LOG_LEVEL`: Logging level (default: "INFO")
- `PORT`: Server port (default: 8000)

### Mock Mode
When `HABU_USE_MOCK_DATA=true`, the server returns realistic sample data:
- 9 premium partners (Meta, Amazon, Google, etc.)
- 8 advanced analytics templates
- Sophisticated business intelligence results

## VS Code Integration

### Configuration
Create `.vscode/mcp.json`:
```json
{
  "servers": {
    "habu-clean-room-server": {
      "url": "https://habu-mcp-server.onrender.com/mcp/",
      "headers": {
        "X-API-Key": "your-api-key"
      }
    }
  }
}
```

### Usage Examples
```
@habu-clean-room-server List my clean room partners
@habu-clean-room-server What analytics templates are available?
@habu-clean-room-server Run audience overlap analysis between Meta and Amazon
@habu-clean-room-server Check the status of my last query
@habu-clean-room-server Enable mock mode for testing
```

## Monitoring & Logging

### Health Checks
- **MCP Server**: `GET /health`
- **Demo API**: `GET /api/health`

### Logging Levels
- **ERROR**: System errors, API failures
- **WARNING**: Authentication issues, circuit breaker activation
- **INFO**: Request processing, successful operations
- **DEBUG**: Detailed request/response data

### Metrics
- Request/response times
- Error rates by endpoint
- Circuit breaker status
- Mock mode usage

## Development

### Local Setup
1. Clone repository
2. Install dependencies: `pip install -r requirements.txt`
3. Configure environment variables in `.env`
4. Run server: `python main.py`

### Testing
- **Unit Tests**: `pytest tests/`
- **Integration Tests**: `python test_habu_integration.py`
- **MCP Protocol Tests**: `python test_mcp_comprehensive.py`

### Deployment
1. Push to GitHub
2. Connect to Render.com
3. Deploy using `render.yaml` blueprint
4. Configure environment variables in Render dashboard

## Support

### Troubleshooting
1. **Authentication Errors**: Check API key and Habu credentials
2. **Empty Results**: Enable mock mode or verify cleanroom access
3. **Timeout Errors**: Check network connectivity and API status
4. **Circuit Breaker**: Wait for cooldown period or check API health

### Debug Commands
```bash
# Test authentication
python debug_oauth.py

# Test cleanroom access
python debug_cleanrooms.py

# Deep API debugging
python deep_api_debug.py
```

### Contact
For technical support or API issues, contact the development team or refer to the GitHub repository issues.