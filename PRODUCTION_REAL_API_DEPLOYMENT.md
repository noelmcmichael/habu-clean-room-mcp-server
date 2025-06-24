# 🚀 Production Deployment with Real API - Step by Step

## **🎯 Objective**
Deploy the working real API integration to production on Render.com, replacing the mock data with live Habu API data.

---

## **📋 Pre-Deployment Checklist**

### **✅ Local Verification Complete**
- [x] MCP Server running with real API (`mock_mode: false`)
- [x] Flask API serving real MCP data via REST endpoints
- [x] React frontend with new Cleanrooms page
- [x] 4 real templates accessible from live cleanroom
- [x] OpenAI integration working
- [x] All services tested and functional

### **🔧 Services to Update**
1. **habu-mcp-server-v2** - MCP protocol server
2. **habu-demo-api-v2** - Flask API bridge
3. **habu-demo-frontend-v2** - React application
4. **habu-admin-app-v2** - Admin interface
5. **habu-mcp-db** - PostgreSQL database (no changes needed)

---

## **🔑 Environment Variables for Real API**

### **1. habu-mcp-server-v2**
```
JOKE_MCP_SERVER_API_KEY=secure-habu-demo-key-2024
HABU_CLIENT_ID=oP7KnpwzUQvf53P7jY0aCzuZeutqMnKT
HABU_CLIENT_SECRET=HA9CiXEXi43fWBqFfZzJUkZga1zbjUngR1P9iH9JczyMgU70DdIW-h0eDrfKpk3w
HABU_USE_MOCK_DATA=false
OPENAI_API_KEY=sk-proj-[your-openai-key-here]
LOG_LEVEL=INFO
PORT=8000
```

### **2. habu-demo-api-v2**
```
JOKE_MCP_SERVER_API_KEY=secure-habu-demo-key-2024
HABU_CLIENT_ID=oP7KnpwzUQvf53P7jY0aCzuZeutqMnKT
HABU_CLIENT_SECRET=HA9CiXEXi43fWBqFfZzJUkZga1zbjUngR1P9iH9JczyMgU70DdIW-h0eDrfKpk3w
HABU_USE_MOCK_DATA=false
OPENAI_API_KEY=sk-proj-[your-openai-key-here]
LOG_LEVEL=INFO
PORT=5001
```

### **3. habu-demo-frontend-v2**
```
REACT_APP_API_URL=https://habu-demo-api-v2.onrender.com
```

### **4. habu-admin-app-v2**
```
DATABASE_URL=postgresql://habu_mcp_db_user:password@server/habu_mcp_db
FLASK_SECRET_KEY=production-secret-key-habu-2024
JOKE_MCP_SERVER_API_KEY=secure-habu-demo-key-2024
HABU_CLIENT_ID=oP7KnpwzUQvf53P7jY0aCzuZeutqMnKT
HABU_CLIENT_SECRET=HA9CiXEXi43fWBqFfZzJUkZga1zbjUngR1P9iH9JczyMgU70DdIW-h0eDrfKpk3w
HABU_USE_MOCK_DATA=false
OPENAI_API_KEY=sk-proj-[your-openai-key-here]
```

---

## **🔄 Deployment Steps**

### **Step 1: Update GitHub Repository**
First, we need to push our local changes to GitHub so Render can deploy them.

```bash
# Commit local changes
git add .
git commit -m "feat: Real API integration with React cleanrooms page

- Switch from mock data to real Habu API integration
- Add professional Cleanrooms page displaying live data
- Update status indicators to show Real API mode
- Add Flask API endpoints for MCP tools
- Integrate OpenAI GPT-4 with real API context
- Display 4 real analytics templates with actual status
- Show live cleanroom 'Data Marketplace Demo'

🤖 Generated with Memex (https://memex.tech)
Co-Authored-By: Memex <noreply@memex.tech>"

# Push to production
git push origin main
```

### **Step 2: Update Environment Variables**
For each service in Render.com dashboard:

1. **Navigate to service settings**
2. **Go to Environment tab**
3. **Update `HABU_USE_MOCK_DATA` from `true` to `false`**
4. **Add `OPENAI_API_KEY` if not present**
5. **Save changes**

### **Step 3: Trigger Deployments**
After updating environment variables, each service will automatically redeploy.

### **Step 4: Verify Deployment**
Test each service after deployment:

1. **MCP Server**: `https://habu-mcp-server-v2.onrender.com/health`
2. **API Bridge**: `https://habu-demo-api-v2.onrender.com/api/health`
3. **Frontend**: `https://habu-demo-frontend-v2.onrender.com`
4. **Admin**: `https://habu-admin-app-v2.onrender.com`

---

## **🧪 Post-Deployment Testing**

### **API Verification**
```bash
# Test MCP server health
curl https://habu-mcp-server-v2.onrender.com/health

# Test API bridge health
curl https://habu-demo-api-v2.onrender.com/api/health

# Test templates endpoint
curl https://habu-demo-api-v2.onrender.com/api/mcp/habu_list_templates

# Test partners endpoint
curl https://habu-demo-api-v2.onrender.com/api/mcp/habu_list_partners
```

### **Frontend Verification**
- **Main app**: `https://habu-demo-frontend-v2.onrender.com`
- **Cleanrooms page**: `https://habu-demo-frontend-v2.onrender.com/cleanrooms`
- **Chat interface**: Test with real API questions
- **System health**: Verify all services show healthy

### **Expected Results**
- **Mock mode**: `false` in all health checks
- **Templates**: 4 real templates displayed
- **Cleanroom**: "Data Marketplace Demo" shown
- **Chat**: OpenAI responses with real data context
- **Performance**: 2-5 second response times (normal for Render free tier)

---

## **📊 Success Criteria**

### **✅ Deployment Successful When:**
- [ ] All 5 services deployed successfully
- [ ] Health checks show `mock_mode: false`
- [ ] Frontend displays real cleanroom data
- [ ] 4 real templates visible in Cleanrooms page
- [ ] Enhanced chat working with OpenAI + real API
- [ ] API endpoints returning real Habu data
- [ ] No errors in service logs

### **🎯 Demo Ready When:**
- [ ] Cleanrooms page loads with real data
- [ ] Chat responds with real template information
- [ ] System health shows all services online
- [ ] API explorer shows real endpoints
- [ ] Professional UI displays actual cleanroom status

---

## **🚨 Rollback Plan**

If issues arise, rollback by:
1. **Set `HABU_USE_MOCK_DATA=true`** in all services
2. **Save environment variables** (triggers redeploy)
3. **Verify mock data returns** in health checks
4. **Fix issues locally** and redeploy

---

## **🌐 Production URLs (After Deployment)**

### **Stakeholder Access**
- **Main Demo**: `https://habu-demo-frontend-v2.onrender.com`
- **Cleanrooms**: `https://habu-demo-frontend-v2.onrender.com/cleanrooms`
- **System Health**: `https://habu-demo-frontend-v2.onrender.com/health`

### **API Access**
- **Health**: `https://habu-demo-api-v2.onrender.com/api/health`
- **Templates**: `https://habu-demo-api-v2.onrender.com/api/mcp/habu_list_templates`
- **Partners**: `https://habu-demo-api-v2.onrender.com/api/mcp/habu_list_partners`

---

## **⏱️ Expected Timeline**
- **Code commit**: 5 minutes
- **Environment updates**: 10 minutes (5 services)
- **Deployment time**: 10-15 minutes (Render.com)
- **Testing & verification**: 10 minutes
- **Total**: ~30-40 minutes

---

## **🎯 Next Steps After Deployment**
1. **Test complete stakeholder workflow**
2. **Document production URLs for sharing**
3. **Create stakeholder demo script**
4. **Monitor performance and error rates**
5. **Plan any additional enhancements**

**Ready to proceed with production deployment!** 🚀