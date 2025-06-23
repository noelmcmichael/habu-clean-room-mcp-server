# 🚀 DEPLOY NOW - Exact Commands to Execute

## 1. Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `habu-clean-room-mcp-server`
3. Description: `Habu Clean Room MCP Server with OpenAI GPT-4 Integration`
4. Set to Public (or Private if preferred)
5. **DO NOT** initialize with README, .gitignore, or license
6. Click "Create repository"

## 2. Push Code to GitHub

Copy your repository URL from GitHub, then run these commands in terminal:

```bash
cd /Users/noelmcmichael/Workspace/streamable_http_mcp_server

# Remove existing remote
git remote remove origin

# Add your new repository (REPLACE WITH YOUR ACTUAL URL)
git remote add origin https://github.com/YOUR_USERNAME/habu-clean-room-mcp-server.git

# Push all code
git push -u origin main
```

## 3. Deploy to Render.com

1. Go to https://render.com and sign in/up
2. Click **"New"** → **"Blueprint"**
3. Click **"Connect GitHub"** if not already connected
4. Find and select your `habu-clean-room-mcp-server` repository
5. Click **"Connect"**
6. Render will detect `render.yaml` automatically
7. Review the services that will be created:
   - ✅ habu-mcp-db (PostgreSQL)
   - ✅ habu-mcp-server (MCP Server)
   - ✅ habu-demo-api (Demo API)
   - ✅ habu-demo-frontend (React App)
   - ✅ habu-admin-app (Admin Interface)
8. Click **"Apply"** to start deployment

## 4. Configure Environment Variables

After deployment starts, set these environment variables for each service:

### For `habu-mcp-server`:
```
JOKE_MCP_SERVER_API_KEY=your-secure-api-key-123
HABU_CLIENT_ID=your-habu-client-id
HABU_CLIENT_SECRET=your-habu-client-secret  
HABU_USE_MOCK_DATA=true
LOG_LEVEL=INFO
```

### For `habu-demo-api`:
```
JOKE_MCP_SERVER_API_KEY=your-secure-api-key-123
HABU_CLIENT_ID=your-habu-client-id
HABU_CLIENT_SECRET=your-habu-client-secret
HABU_USE_MOCK_DATA=true
LOG_LEVEL=INFO
```

### For `habu-demo-frontend`:
```
REACT_APP_API_URL=https://habu-demo-api.onrender.com
```
*Replace with your actual demo API URL from Render*

### For `habu-admin-app`:
```
FLASK_SECRET_KEY=your-flask-secret-key-456
ADMIN_EMAIL=admin@yourcompany.com
ADMIN_PASSWORD=secure-admin-password
JOKE_MCP_SERVER_API_KEY=your-secure-api-key-123
```

## 5. Wait for Deployment

Monitor the deployment in Render dashboard:
- **Database**: ~2-3 minutes
- **Python services**: ~3-5 minutes each  
- **React frontend**: ~5-7 minutes

All services should show **"Live"** status when complete.

## 6. Test Your Deployment

Update and run the test script:

```bash
# Edit test_production_deployment.py
# Update BASE_URLS with your actual Render URLs
# Update API_KEY with your actual API key

python test_production_deployment.py
```

## 7. Configure VS Code

Update `.vscode/mcp.json`:

```json
{
  "servers": {
    "habu-clean-room-server-production": {
      "url": "https://YOUR_MCP_SERVER.onrender.com/mcp/",
      "headers": {
        "X-API-Key": "your-secure-api-key-123"
      }
    }
  }
}
```

## 8. Test in VS Code

In VS Code with GitHub Copilot Chat:

```
@habu-clean-room-server-production List my clean room partners
@habu-clean-room-server-production What analytics templates are available?
@habu-clean-room-server-production habu_enhanced_chat "Show me audience overlap analysis"
```

---

## 🎯 SUCCESS CRITERIA

✅ All 5 services show "Live" in Render  
✅ Health endpoints return 200 OK  
✅ VS Code MCP integration working  
✅ React demo frontend accessible  
✅ Enhanced chat responding to requests  

## 📱 DEMO URLS (After Deployment)

- **Demo Frontend**: Share this URL for presentations
- **VS Code Integration**: Use MCP server URL
- **API Access**: Available for third-party integrations

Your Habu Clean Room MCP Server will be live and ready for enterprise demonstrations!