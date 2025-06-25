# 🚀 Deploy to Render.com - Exact Steps

## Pre-Deployment Checklist ✅
- [x] Code pushed to GitHub: https://github.com/noelmcmichael/habu-clean-room-mcp-server
- [x] Rollback plan established with tag: `pre-enhanced-deployment`
- [x] Enhanced UX components built and tested
- [x] render.yaml configuration ready for 5-service deployment

## Step-by-Step Deployment Instructions

### 1. Access Render.com
1. Go to https://render.com
2. Sign in with your account (or create one if needed)
3. Click **"New"** button in the top-right corner

### 2. Connect GitHub Repository
1. Select **"Blueprint"** from the New menu
2. Click **"Connect GitHub"** if not already connected
3. Search for repository: `habu-clean-room-mcp-server`
4. Select the repository and click **"Connect"**

### 3. Review Blueprint Configuration
Render will detect the `render.yaml` file and show these services:

**✅ 5 Services Will Be Created:**
- `habu-mcp-db` (PostgreSQL Database)
- `habu-redis-cache` (Redis Cache)  
- `habu-mcp-server-v2` (MCP Server)
- `habu-demo-api-v2` (Flask API)
- `habu-demo-frontend-v2` (React Frontend)
- `habu-admin-app-v2` (Admin Interface)

### 4. Configure Environment Variables
**CRITICAL**: Set these environment variables in Render dashboard:

#### For ALL Python Services (MCP Server + Demo API + Admin App):
```
OPENAI_API_KEY=sk-your-openai-api-key-here
```

#### Optional (Already configured in render.yaml):
```
JOKE_MCP_SERVER_API_KEY=secure-habu-demo-key-2024
HABU_CLIENT_ID=oP7KnpwzUQvf53P7jY0aCzuZeutqMnKT
HABU_CLIENT_SECRET=HA9CiXEXi43fWBqFfZzJUkZga1zbjUngR1P9iH9JczyMgU70DdIW-h0eDrfKpk3w
HABU_USE_MOCK_DATA=true
```

### 5. Deploy Services
1. Click **"Apply"** to start deployment
2. Monitor deployment progress in Render dashboard
3. **Expected Timeline:**
   - Database creation: 2-3 minutes
   - Python services: 4-6 minutes each
   - React frontend: 5-8 minutes

### 6. Verify Deployment Success
All services should show **"Live"** status. Note these URLs:

- **MCP Server**: `https://habu-mcp-server-v2.onrender.com`
- **Demo API**: `https://habu-demo-api-v2.onrender.com`  
- **React Frontend**: `https://habu-demo-frontend-v2.onrender.com`
- **Admin App**: `https://habu-admin-app-v2.onrender.com`

## Step 5: Post-Deployment Testing

### Health Check URLs
Test these endpoints immediately after deployment:

```bash
# MCP Server Health
curl https://habu-mcp-server-v2.onrender.com/health

# Demo API Health  
curl https://habu-demo-api-v2.onrender.com/health

# Admin App Health
curl https://habu-admin-app-v2.onrender.com/health
```

**Expected Response**: All should return `200 OK` with health status

### Frontend Access
1. Open: `https://habu-demo-frontend-v2.onrender.com`
2. Verify enhanced UX components load
3. Test both Customer Support and Technical Expert modes
4. Try quick action buttons
5. Verify mobile responsiveness

### Enhanced Features Testing
**Customer Support Mode:**
- Click "Lookalike Modeling" quick action
- Verify contextual suggestions appear
- Test mode switching functionality
- Check real-time metrics display

**Technical Expert Mode:**
- Click "Identity Resolution API" quick action  
- Verify code examples render properly
- Test message actions (copy, regenerate, feedback)
- Check syntax highlighting in responses

## Step 6: Configure VS Code Integration

Update your `.vscode/mcp.json` with production URLs:

```json
{
  "servers": {
    "liveramp-ai-assistant-production": {
      "url": "https://habu-mcp-server-v2.onrender.com/mcp/",
      "headers": {
        "X-API-Key": "secure-habu-demo-key-2024"
      }
    }
  }
}
```

### Test VS Code Integration
In VS Code GitHub Copilot Chat:
```
@liveramp-ai-assistant-production List my clean room partners
@liveramp-ai-assistant-production Show me audience overlap analysis  
@liveramp-ai-assistant-production What are common API integration issues?
```

## Expected Deployment Results

### ✅ Success Indicators
- [ ] All 5 services show "Live" status in Render
- [ ] Health endpoints return 200 OK
- [ ] React frontend accessible with enhanced UX
- [ ] Mode switching works between Customer Support and Technical Expert
- [ ] Quick actions generate appropriate responses
- [ ] Real-time metrics display correctly
- [ ] Mobile responsiveness functions properly
- [ ] VS Code MCP integration operational

### ⚠️ Rollback Triggers
**Initiate rollback if:**
- [ ] React frontend completely inaccessible (404 errors)
- [ ] Multiple services fail to start (>2 services down)
- [ ] TypeScript compilation errors in production
- [ ] Database connection failures across services
- [ ] Critical API endpoints returning 500 errors consistently

## Rollback Procedure (If Needed)

### Quick Rollback Commands
```bash
cd /Users/noelmcmichael/Workspace/streamable_http_mcp_server
git checkout pre-enhanced-deployment
git push origin main --force
```

### Render Rollback
1. Go to Render dashboard
2. Select failing services
3. Redeploy from previous commit
4. Or delete blueprint and redeploy from rollback tag

## Production URLs (After Deployment)

**Update these URLs in test script:**
```python
BASE_URLS = {
    'mcp_server': 'https://habu-mcp-server-v2.onrender.com',
    'demo_api': 'https://habu-demo-api-v2.onrender.com',
    'admin_app': 'https://habu-admin-app-v2.onrender.com',
    'react_frontend': 'https://habu-demo-frontend-v2.onrender.com'
}
```

## Support Resources

### If Deployment Issues Occur:
1. **Check Render Logs**: Each service has detailed logs in Render dashboard
2. **Environment Variables**: Verify OPENAI_API_KEY is set correctly
3. **Test Script**: Run `test_production_deployment_enhanced.py` with production URLs
4. **GitHub Issues**: Document any deployment problems
5. **Rollback Plan**: Use established rollback procedure if critical issues

### Performance Monitoring
- **Response Times**: Monitor API response latency
- **Error Rates**: Track 4xx/5xx error percentages
- **User Metrics**: Observe enhanced UX component usage
- **Resource Usage**: Monitor memory and CPU utilization

---

## 🎯 Success Criteria

**Deployment is successful when:**
- ✅ All 5 services operational in production
- ✅ Enhanced UX features functional across all devices
- ✅ Both AI modes (Customer Support + Technical Expert) working
- ✅ VS Code MCP integration active
- ✅ Performance metrics within acceptable ranges
- ✅ Zero critical errors in production logs

**Estimated Deployment Time**: 15-20 minutes for complete system

**Business Impact**: Immediate productivity gains for LiveRamp teams with world-class AI assistant experience