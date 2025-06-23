# 🎯 EXACT ENVIRONMENT VARIABLES FOR RENDER.COM

## Copy-paste these exact values in Render dashboard:

### For `habu-mcp-server` service:
```
JOKE_MCP_SERVER_API_KEY=secure-habu-demo-key-2024
HABU_CLIENT_ID=oP7KnpwzUQvf53P7jY0aCzuZeutqMnKT
HABU_CLIENT_SECRET=paste-your-client-secret-here
HABU_USE_MOCK_DATA=true
LOG_LEVEL=INFO
PORT=8000
```

### For `habu-demo-api` service:
```
JOKE_MCP_SERVER_API_KEY=secure-habu-demo-key-2024
HABU_CLIENT_ID=oP7KnpwzUQvf53P7jY0aCzuZeutqMnKT
HABU_CLIENT_SECRET=paste-your-client-secret-here
HABU_USE_MOCK_DATA=true
LOG_LEVEL=INFO
PORT=5001
```

### For `habu-demo-frontend` service:
```
REACT_APP_API_URL=https://habu-demo-api.onrender.com
```

### For `habu-admin-app` service:
```
FLASK_SECRET_KEY=super-secret-flask-key-12345
ADMIN_EMAIL=admin@habu-demo.com
ADMIN_PASSWORD=HabuDemo2024!
JOKE_MCP_SERVER_API_KEY=secure-habu-demo-key-2024
```

## 🔐 Get Your HABU_CLIENT_SECRET:
Run this in terminal to get your secret:
```bash
cd /Users/noelmcmichael/Workspace/streamable_http_mcp_server
grep HABU_CLIENT_SECRET .env
```

## 🎯 RENDER.COM DEPLOYMENT STEPS:

1. **Repository Connected** ✅ 
   - `https://github.com/noelmcmichael/habu-clean-room-mcp-server`

2. **In Render.com** (should be open in your browser):
   - Click "Connect" on your repository
   - Click "Apply" to deploy all services
   - Wait for services to build (5-15 minutes)

3. **Add Environment Variables**:
   - Click each service name
   - Go to "Environment" tab  
   - Add the variables above
   - Click "Save Changes"

4. **Services will redeploy automatically**

## 🚀 EXPECTED RESULT:
- 5 services showing "Live" status
- Professional demo URLs ready for presentations
- VS Code MCP integration with production server
- Mock data working for reliable demonstrations

**Deployment is 90% complete! Just need to set environment variables in Render dashboard.**