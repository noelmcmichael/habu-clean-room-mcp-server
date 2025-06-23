# 🔐 RENDER.COM ENVIRONMENT VARIABLES

## After connecting your GitHub repository to Render, set these environment variables:

### For `habu-mcp-server` service:
```
JOKE_MCP_SERVER_API_KEY=secure-habu-demo-key-2024
HABU_CLIENT_ID=your-habu-client-id-here
HABU_CLIENT_SECRET=your-habu-client-secret-here
HABU_USE_MOCK_DATA=true
LOG_LEVEL=INFO
PORT=8000
```

### For `habu-demo-api` service:
```
JOKE_MCP_SERVER_API_KEY=secure-habu-demo-key-2024
HABU_CLIENT_ID=your-habu-client-id-here
HABU_CLIENT_SECRET=your-habu-client-secret-here
HABU_USE_MOCK_DATA=true
LOG_LEVEL=INFO
PORT=5001
```

### For `habu-demo-frontend` service:
```
REACT_APP_API_URL=https://habu-demo-api.onrender.com
```
*Note: Replace with your actual demo API URL after it's deployed*

### For `habu-admin-app` service:
```
FLASK_SECRET_KEY=super-secret-flask-key-12345
ADMIN_EMAIL=admin@yourcompany.com
ADMIN_PASSWORD=secure-admin-password-123
JOKE_MCP_SERVER_API_KEY=secure-habu-demo-key-2024
```

## 🎯 Next Steps:

1. **In Render.com**: Connect your `noelmcmichael/habu-clean-room-mcp-server` repository
2. **Deploy**: Click "Apply" to deploy all 5 services
3. **Configure**: Add the environment variables above to each service
4. **Wait**: 15-20 minutes for all services to be "Live"
5. **Test**: Visit your frontend URL to see the demo

## 📍 Your Repository: 
https://github.com/noelmcmichael/habu-clean-room-mcp-server

## 📱 Expected Live URLs (after deployment):
- **Demo Frontend**: `https://habu-demo-frontend.onrender.com`
- **Demo API**: `https://habu-demo-api.onrender.com` 
- **MCP Server**: `https://habu-mcp-server.onrender.com/mcp`
- **Admin App**: `https://habu-admin-app.onrender.com`