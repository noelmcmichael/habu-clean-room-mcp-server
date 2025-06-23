# 🚀 SIMPLE DEPLOYMENT INSTRUCTIONS

## You're Ready! Here's What to Do:

### Step 1: GitHub Authentication (1 minute)
```bash
cd /Users/noelmcmichael/Workspace/streamable_http_mcp_server
gh auth login
```
- Choose "GitHub.com"
- Choose "HTTPS"
- Choose "Login with a web browser" 
- Press Enter and follow the browser login

### Step 2: Create Repository & Deploy (30 seconds)
```bash
./deploy_to_github.sh
```

### Step 3: Deploy to Render.com (2 minutes)
1. Go to: https://render.com/blueprints
2. Sign in with GitHub
3. Click "New Blueprint"
4. Select repository: `noelmcmichael/habu-clean-room-mcp-server`
5. Click "Apply"

### Step 4: Configure Environment Variables (3 minutes)

Set these in Render dashboard for both `habu-mcp-server` and `habu-demo-api`:

```
JOKE_MCP_SERVER_API_KEY=secure-habu-demo-key-2024
HABU_CLIENT_ID=your-habu-client-id
HABU_CLIENT_SECRET=your-habu-client-secret
HABU_USE_MOCK_DATA=true
LOG_LEVEL=INFO
```

### Step 5: Update VS Code Configuration

After deployment, update `.vscode/mcp.json`:
```json
{
  "servers": {
    "habu-clean-room-server-production": {
      "url": "https://habu-mcp-server.onrender.com/mcp/",
      "headers": {
        "X-API-Key": "secure-habu-demo-key-2024"
      }
    }
  }
}
```

## 🎯 EXPECTED RESULTS (15-20 minutes total)

✅ **5 Services Live on Render.com:**
- habu-mcp-server (MCP Protocol)
- habu-demo-api (REST API)  
- habu-demo-frontend (React App)
- habu-admin-app (Admin Interface)
- habu-mcp-db (PostgreSQL)

✅ **Professional Demo URLs:**
- Frontend: `https://habu-demo-frontend.onrender.com`
- API: `https://habu-demo-api.onrender.com`
- MCP: `https://habu-mcp-server.onrender.com/mcp`

✅ **VS Code Integration:**
```
@habu-clean-room-server-production List my partners
@habu-clean-room-server-production habu_enhanced_chat "Show me audience overlap analysis"
```

## 🆘 IF YOU GET STUCK

1. **GitHub Authentication Issues**: Make sure you're logged into GitHub in your browser
2. **Render Deployment**: All services should show "Building" then "Live" 
3. **Environment Variables**: Double-check spelling and values match exactly

**Ready? Run the first command: `gh auth login`**