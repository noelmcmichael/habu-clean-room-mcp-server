#!/usr/bin/env python3
"""
Test script for production deployment verification
Run this after deploying to Render.com
"""
import asyncio
import httpx
import json

# Update these URLs with your actual Render service URLs
BASE_URLS = {
    "mcp_server": "https://habu-mcp-server.onrender.com",
    "demo_api": "https://habu-demo-api.onrender.com", 
    "frontend": "https://habu-demo-frontend.onrender.com",
    "admin": "https://habu-admin-app.onrender.com"
}

# Your API key (set this to match your production config)
API_KEY = "your-production-api-key"

async def test_health_endpoints():
    """Test all health endpoints"""
    print("🏥 Testing Health Endpoints")
    print("=" * 50)
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        
        # Test Demo API health
        try:
            response = await client.get(f"{BASE_URLS['demo_api']}/api/health")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Demo API: {data['status']} (OpenAI: {data.get('openai_configured', 'unknown')})")
            else:
                print(f"❌ Demo API: HTTP {response.status_code}")
        except Exception as e:
            print(f"❌ Demo API: {e}")
        
        # Test React Frontend
        try:
            response = await client.get(BASE_URLS['frontend'])
            if response.status_code == 200:
                print(f"✅ React Frontend: Live")
            else:
                print(f"❌ React Frontend: HTTP {response.status_code}")
        except Exception as e:
            print(f"❌ React Frontend: {e}")

async def test_mcp_integration():
    """Test MCP server functionality"""
    print(f"\n🔧 Testing MCP Server")
    print("=" * 50)
    
    if not API_KEY or API_KEY == "your-production-api-key":
        print("⚠️  Please set your actual API key in the script")
        return
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        headers = {
            "X-API-Key": API_KEY,
            "Content-Type": "application/json"
        }
        
        # Test MCP tools/list
        try:
            mcp_request = {
                "jsonrpc": "2.0",
                "method": "tools/list",
                "id": 1
            }
            
            response = await client.post(
                f"{BASE_URLS['mcp_server']}/mcp",
                headers=headers,
                json=mcp_request
            )
            
            if response.status_code == 200:
                data = response.json()
                tools = data.get('result', {}).get('tools', [])
                print(f"✅ MCP Server: {len(tools)} tools available")
                for tool in tools[:3]:  # Show first 3 tools
                    print(f"   - {tool.get('name', 'unknown')}")
                if len(tools) > 3:
                    print(f"   ... and {len(tools) - 3} more")
            else:
                print(f"❌ MCP Server: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ MCP Server: {e}")

async def test_enhanced_chat():
    """Test enhanced chat via Demo API"""
    print(f"\n💬 Testing Enhanced Chat")
    print("=" * 50)
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            chat_request = {
                "user_input": "List my clean room partners"
            }
            
            response = await client.post(
                f"{BASE_URLS['demo_api']}/api/enhanced-chat",
                headers={"Content-Type": "application/json"},
                json=chat_request
            )
            
            if response.status_code == 200:
                data = response.json()
                response_text = data.get('response', '')
                print(f"✅ Enhanced Chat: Working")
                print(f"   Sample response: {response_text[:100]}...")
            else:
                print(f"❌ Enhanced Chat: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ Enhanced Chat: {e}")

async def main():
    """Run all deployment tests"""
    print("🚀 Production Deployment Verification")
    print("=" * 60)
    print("Update BASE_URLS in this script with your actual Render URLs")
    print("Update API_KEY with your production API key")
    print("=" * 60)
    
    await test_health_endpoints()
    await test_mcp_integration()
    await test_enhanced_chat()
    
    print(f"\n✅ Deployment verification complete!")
    print(f"\n📋 Next Steps:")
    print(f"1. Configure VS Code MCP integration")
    print(f"2. Test with GitHub Copilot Chat")
    print(f"3. Share frontend URL for demos: {BASE_URLS['frontend']}")

if __name__ == "__main__":
    asyncio.run(main())