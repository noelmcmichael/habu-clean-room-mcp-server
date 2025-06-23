#!/bin/bash

echo "🚀 Deploying Habu Clean Room MCP Server to GitHub"
echo "=================================================="

# Create repository on GitHub
echo "Creating repository on GitHub..."
gh repo create noelmcmichael/habu-clean-room-mcp-server \
  --public \
  --description "Habu Clean Room MCP Server with OpenAI GPT-4 Integration and React Demo" \
  --clone=false

# Push code to GitHub
echo "Pushing code to GitHub..."
git remote set-url origin https://github.com/noelmcmichael/habu-clean-room-mcp-server.git
git push -u origin main

echo "✅ Code deployed to GitHub!"
echo "📍 Repository: https://github.com/noelmcmichael/habu-clean-room-mcp-server"
echo ""
echo "🎯 Next: Go to render.com to deploy the services"
echo "   1. Visit: https://render.com/blueprints"
echo "   2. Connect your GitHub repository"
echo "   3. Select 'habu-clean-room-mcp-server'"
echo "   4. Click 'Apply' to deploy all services"