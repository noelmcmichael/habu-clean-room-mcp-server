# Habu Clean Room MCP Server - Deployment Guide

## Overview

This guide covers deploying the Habu Clean Room MCP Server to production using Render.com. The deployment includes:

- FastMCP 2.0 server with Habu integration
- React demo frontend with professional ICDC styling
- Flask API bridge for frontend communication
- PostgreSQL database for persistence
- Optional Flask admin interface

## Prerequisites

### Accounts & Services
- [Render.com](https://render.com) account
- [GitHub](https://github.com) repository
- Habu API credentials (client ID & secret)
- OpenAI API key (for enhanced chat features)

### Local Development Setup
- Python 3.8+
- Node.js 16+ (for React frontend)
- Git

## Production Deployment (Render.com)

### Step 1: Repository Setup

1. **Fork/Clone Repository**
   ```bash
   git clone https://github.com/your-org/habu-mcp-server.git
   cd habu-mcp-server
   ```

2. **Push to Your GitHub**
   ```bash
   git remote add origin https://github.com/your-username/habu-mcp-server.git
   git push -u origin main
   ```

### Step 2: Render Deployment

1. **Connect Repository to Render**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New" → "Blueprint"
   - Connect your GitHub repository
   - Select the repository containing your MCP server

2. **Blueprint Deployment**
   - Render will automatically detect `render.yaml`
   - This creates all services:
     - PostgreSQL database (`habu-mcp-db`)
     - MCP Server (`habu-mcp-server`)
     - Demo API (`habu-demo-api`)
     - React Frontend (`habu-demo-frontend`)
     - Admin App (`habu-admin-app`)

### Step 3: Environment Configuration

Set these environment variables in Render dashboard for each service:

#### MCP Server (`habu-mcp-server`)
```env
JOKE_MCP_SERVER_API_KEY=your-secure-api-key-here
HABU_CLIENT_ID=your-habu-client-id
HABU_CLIENT_SECRET=your-habu-client-secret
HABU_USE_MOCK_DATA=true
LOG_LEVEL=INFO
```

#### Demo API (`habu-demo-api`)
```env
JOKE_MCP_SERVER_API_KEY=your-secure-api-key-here
HABU_CLIENT_ID=your-habu-client-id
HABU_CLIENT_SECRET=your-habu-client-secret
HABU_USE_MOCK_DATA=true
LOG_LEVEL=INFO
```

#### React Frontend (`habu-demo-frontend`)
```env
REACT_APP_API_URL=https://habu-demo-api.onrender.com
```

#### Admin App (`habu-admin-app`)
```env
FLASK_SECRET_KEY=your-flask-secret-key
ADMIN_EMAIL=admin@yourcompany.com
ADMIN_PASSWORD=secure-admin-password
JOKE_MCP_SERVER_API_KEY=your-secure-api-key-here
```

### Step 4: Verification

1. **Check Service Status**
   - All services should show "Live" status in Render dashboard
   - Check logs for any startup errors

2. **Test Endpoints**
   ```bash
   # Test MCP server health
   curl https://habu-mcp-server.onrender.com/health
   
   # Test Demo API health
   curl https://habu-demo-api.onrender.com/api/health
   
   # Test React frontend
   curl https://habu-demo-frontend.onrender.com
   ```

3. **Test MCP Integration**
   ```bash
   # Test with API key
   curl -X POST https://habu-mcp-server.onrender.com/mcp/ \
     -H "X-API-Key: your-api-key" \
     -H "Content-Type: application/json" \
     -d '{"jsonrpc":"2.0","method":"tools/list","id":1}'
   ```

## VS Code Integration

### Step 1: Configure VS Code MCP

Create `.vscode/mcp.json` in your workspace:
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

### Step 2: Test Integration

In VS Code with Copilot Chat:
```
@habu-clean-room-server List my clean room partners
@habu-clean-room-server What analytics templates are available?
@habu-clean-room-server habu_enhanced_chat "Show me audience overlap analysis options"
```

## Local Development

### Step 1: Environment Setup

1. **Clone Repository**
   ```bash
   git clone https://github.com/your-org/habu-mcp-server.git
   cd habu-mcp-server
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables**
   ```bash
   cp .env.sample .env
   # Edit .env with your credentials
   ```

### Step 2: Database Setup

```bash
# Start PostgreSQL (if running locally)
# Or use a cloud database URL in .env

# Run database migrations
python -c "
import asyncio
from database import engine
from models import Base

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(create_tables())
"
```

### Step 3: Start Services

```bash
# Terminal 1: MCP Server
python main.py

# Terminal 2: Demo API
python demo_api.py

# Terminal 3: React Frontend
cd demo_app
npm install
npm start
```

### Step 4: Test Locally

- **MCP Server**: http://localhost:8000/health
- **Demo API**: http://localhost:5001/api/health
- **React Frontend**: http://localhost:3001

## Configuration Management

### Secrets Management

**Production (Render)**
- Use Render's environment variable management
- Enable "Generate Value" for sensitive keys
- Never commit secrets to repository

**Local Development**
- Use `.env` file (gitignored)
- Use keyring for API keys:
  ```bash
  python -c "import keyring; keyring.set_password('memex', 'OpenAI Key', 'your-key')"
  ```

### Feature Flags

Control features via environment variables:

```env
# Enable/disable mock data
HABU_USE_MOCK_DATA=true

# Logging level
LOG_LEVEL=INFO

# CORS origins (comma-separated)
CORS_ORIGINS=https://yourapp.com,https://demo.yourapp.com
```

## Monitoring & Maintenance

### Health Checks

Set up monitoring for these endpoints:
- `https://habu-mcp-server.onrender.com/health`
- `https://habu-demo-api.onrender.com/api/health`

### Log Monitoring

Monitor application logs in Render dashboard:
- Look for authentication errors
- Monitor API response times
- Track circuit breaker activations

### Performance

**Render Free Tier Limitations:**
- Services sleep after 15 minutes of inactivity
- First request after sleep may be slow (cold start)
- Consider upgrading to paid plans for production

### Updates & Maintenance

1. **Code Updates**
   ```bash
   git add .
   git commit -m "Your update message"
   git push origin main
   ```
   Render auto-deploys on push to main branch

2. **Environment Updates**
   - Update via Render dashboard
   - Services restart automatically

3. **Database Migrations**
   - Run migration scripts via Render shell
   - Or include in startup commands

## Troubleshooting

### Common Issues

1. **Service Won't Start**
   - Check environment variables are set
   - Review startup logs in Render dashboard
   - Verify database connection string

2. **Authentication Errors**
   - Verify API key is set correctly
   - Check Habu credentials are valid
   - Test OAuth2 flow independently

3. **CORS Issues**
   - Update CORS_ORIGINS environment variable
   - Ensure frontend URL is included

4. **Database Connection Issues**
   - Verify DATABASE_URL format
   - Check PostgreSQL service status
   - Review database logs

### Debug Commands

```bash
# Test Habu authentication
python debug_oauth.py

# Test cleanroom access
python debug_cleanrooms.py

# Comprehensive API testing
python deep_api_debug.py

# Test MCP protocol
python test_mcp_comprehensive.py
```

### Support Resources

- **Render Documentation**: https://render.com/docs
- **FastMCP Documentation**: https://github.com/jlowin/fastmcp
- **MCP Specification**: https://modelcontextprotocol.io/
- **Project Repository**: https://github.com/your-org/habu-mcp-server

## Security Considerations

### API Keys
- Use strong, unique API keys
- Rotate keys regularly
- Never expose keys in client-side code

### Database Security
- Use connection pooling
- Enable SSL connections
- Regular backups via Render

### Network Security
- HTTPS only in production
- Proper CORS configuration
- Rate limiting for API endpoints

### Monitoring
- Log all authentication attempts
- Monitor for unusual request patterns
- Set up alerts for error rates

## Scaling Considerations

### Performance Optimization
- Enable connection pooling
- Implement caching for expensive operations
- Use async/await throughout

### High Availability
- Multiple service instances
- Database replicas
- Load balancing

### Cost Management
- Monitor usage and costs
- Optimize resource allocation
- Consider caching strategies

This deployment guide provides comprehensive instructions for taking the Habu Clean Room MCP Server from development to production. Follow the steps carefully and refer to the troubleshooting section for common issues.