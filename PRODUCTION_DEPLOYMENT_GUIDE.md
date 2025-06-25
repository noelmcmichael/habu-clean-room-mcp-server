# 🚀 LiveRamp AI Assistant - Production Deployment Guide

## System Overview

**LiveRamp AI Assistant** is a dual-mode AI system designed for LiveRamp employees:

- **Customer Support Mode**: Sales/support teams get instant customer feasibility assessments
- **Technical Expert Mode**: Engineers get comprehensive API implementation guidance

## Deployment Architecture

```
GitHub Repository → Render.com Blueprint → Production Services
├── PostgreSQL Database (Customer data, conversation history)
├── Redis Cache (Performance optimization)
├── MCP Server (Model Context Protocol integration)
├── Flask API (Backend services with OpenAI GPT-4)
├── React Frontend (Chat interface with mode switching)
└── Admin Interface (Database management)
```

## Quick Deploy to Render.com

### Prerequisites
- GitHub account with repository access
- Render.com account
- OpenAI API key for GPT-4 access

### Step 1: Repository Setup

1. Fork/clone this repository to your GitHub account
2. Ensure all code is committed and pushed to `main` branch

### Step 2: Deploy to Render

1. Go to [Render.com](https://render.com) and sign in
2. Click **"New"** → **"Blueprint"**
3. Connect your GitHub repository
4. Render will detect `render.yaml` and create 5 services:
   - `habu-mcp-db` (PostgreSQL)
   - `habu-redis-cache` (Redis)
   - `habu-mcp-server-v2` (MCP Server)
   - `habu-demo-api-v2` (Flask API)
   - `habu-demo-frontend-v2` (React App)
   - `habu-admin-app-v2` (Admin Interface)

### Step 3: Configure Environment Variables

#### Required for API Services:
```bash
OPENAI_API_KEY=sk-your-openai-api-key-here
```

#### Optional Customizations:
```bash
# API Security
JOKE_MCP_SERVER_API_KEY=your-custom-api-key

# Admin Access
ADMIN_EMAIL=your-admin@company.com
ADMIN_PASSWORD=your-secure-password

# Feature Flags
HABU_USE_MOCK_DATA=true  # Set to false for live Habu API
LOG_LEVEL=INFO
```

### Step 4: Verify Deployment

Monitor deployment progress in Render dashboard. All services should show **"Live"** status.

**Health Check URLs:**
- MCP Server: `https://your-mcp-server.onrender.com/health`
- Demo API: `https://your-demo-api.onrender.com/health`
- React Frontend: `https://your-frontend.onrender.com`

## Production Features

### Customer Support Mode Capabilities
```
User: "Can we support real-time attribution for automotive customers?"

AI Response:
✅ Yes, fully supported! 
📊 90%+ accuracy vs industry 60-70%
⏱️ Timeline: 24-48 hours setup
🎯 Use case: Perfect for automotive attribution
📋 Next steps: Confirm data requirements and compliance needs
```

### Technical Expert Mode Capabilities
```python
User: "Show me Python identity resolution with error handling"

AI Response: [Complete implementation with:]
- Authentication setup and token management
- Retry logic with exponential backoff
- Error handling for 401, 429, timeout scenarios  
- Input validation and response processing
- Dependencies, deployment notes, security guidance
```

## System Monitoring

### Key Metrics to Track
- **Response Accuracy**: Monitor user satisfaction ratings
- **Mode Usage**: Track Customer Support vs Technical Expert usage
- **Performance**: API response times and error rates
- **Business Impact**: Customer conversion rates, engineering productivity

### Health Monitoring
```bash
# Check all services
curl https://your-mcp-server.onrender.com/health
curl https://your-demo-api.onrender.com/health
curl https://your-admin-app.onrender.com/health
```

## Integration with VS Code

### MCP Server Configuration
```json
// .vscode/mcp.json
{
  "servers": {
    "liveramp-ai-assistant": {
      "url": "https://your-mcp-server.onrender.com/mcp/",
      "headers": {
        "X-API-Key": "your-api-key"
      }
    }
  }
}
```

### Usage in VS Code
```
@liveramp-ai-assistant List available clean room partners
@liveramp-ai-assistant Show me audience segmentation implementation
@liveramp-ai-assistant What are common API integration issues?
```

## Security & Compliance

### Data Protection
- All customer queries encrypted in transit (HTTPS)
- No sensitive data stored in conversation logs
- API keys secured via Render environment variables
- Database connections encrypted

### Access Control
- Admin interface password protected
- API endpoints require authentication
- MCP server access via secure tokens
- Role-based access for different user types

## Scaling Considerations

### Performance Optimization
- Redis caching for frequently accessed data
- CDN integration for static assets
- Database connection pooling
- API rate limiting and throttling

### Cost Management
- Start with Render free/starter tiers
- Monitor usage and upgrade as needed
- Optimize API calls to reduce OpenAI costs
- Cache common responses to improve performance

## Troubleshooting

### Common Issues

**1. OpenAI API Rate Limits**
```bash
# Solution: Implement exponential backoff
# Add OPENAI_API_KEY with higher tier limits
```

**2. Database Connection Issues**
```bash
# Check DATABASE_URL environment variable
# Verify PostgreSQL service is running
# Test connection from admin interface
```

**3. Frontend Build Failures**
```bash
# Check Node.js version compatibility
# Clear npm cache: npm cache clean --force
# Rebuild: cd demo_app && npm install && npm run build
```

### Support Resources
- **GitHub Issues**: Technical problems and feature requests
- **Render Documentation**: Deployment and scaling guidance
- **OpenAI API Docs**: GPT-4 integration help

## Success Metrics

### Technical KPIs
- ✅ All 5 services deployed and healthy
- ✅ Response time < 3 seconds for chat queries
- ✅ 99%+ uptime for critical services
- ✅ Zero data loss or security incidents

### Business KPIs
- 📈 Customer support response time reduction
- 📈 Engineering productivity improvement
- 📈 API documentation usage increase
- 📈 Customer satisfaction scores

## Next Steps After Deployment

1. **User Training**: Onboard LiveRamp teams on both modes
2. **Feedback Collection**: Gather user experience data
3. **Performance Optimization**: Based on usage patterns
4. **Feature Enhancement**: Add new capabilities based on needs

---

**Ready to deploy?** Follow the steps above and transform how LiveRamp employees access API expertise and customer support guidance.

**Deployment Time**: ~15-20 minutes for complete system setup
**Go-Live Ready**: Immediately after successful deployment verification