#!/usr/bin/env python3
"""
Test MCP protocol directly to verify all tools are available
"""
import asyncio
import json
import aiohttp
import os

async def test_mcp_protocol():
    """Test the MCP server protocol directly"""
    base_url = "http://localhost:8000/mcp/"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
        "X-API-Key": "test-api-key-123"
    }
    
    # Enable mock mode
    os.environ["HABU_USE_MOCK_DATA"] = "true"
    
    print("🔍 Testing MCP Protocol Direct Communication")
    print("=" * 50)
    
    async with aiohttp.ClientSession() as session:
        # Test 1: Initialize MCP session
        print("\n1. Testing MCP Session Initialization...")
        init_payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "clientInfo": {
                    "name": "test-client",
                    "version": "1.0.0"
                }
            }
        }
        
        try:
            async with session.post(base_url, headers=headers, json=init_payload) as response:
                result = await response.text()
                print(f"Status: {response.status}")
                print(f"Response: {result[:200]}...")
        except Exception as e:
            print(f"❌ Session init failed: {e}")
        
        # Test 2: List available tools
        print("\n2. Testing Tools List...")
        tools_payload = {
            "jsonrpc": "2.0", 
            "id": 2,
            "method": "tools/list",
            "params": {}
        }
        
        try:
            async with session.post(base_url, headers=headers, json=tools_payload) as response:
                result = await response.text()
                print(f"Status: {response.status}")
                if response.status == 200:
                    data = json.loads(result)
                    if "result" in data and "tools" in data["result"]:
                        tools = data["result"]["tools"]
                        print(f"✅ Found {len(tools)} tools:")
                        for tool in tools:
                            print(f"  • {tool.get('name', 'Unknown')}: {tool.get('description', 'No description')[:60]}...")
                    else:
                        print(f"Response: {result}")
                else:
                    print(f"Response: {result}")
        except Exception as e:
            print(f"❌ Tools list failed: {e}")
        
        # Test 3: Test enhanced chat tool
        print("\n3. Testing Enhanced Chat Tool...")
        chat_payload = {
            "jsonrpc": "2.0",
            "id": 3, 
            "method": "tools/call",
            "params": {
                "name": "habu_enhanced_chat",
                "arguments": {
                    "user_input": "show me my partners"
                }
            }
        }
        
        try:
            async with session.post(base_url, headers=headers, json=chat_payload) as response:
                result = await response.text()
                print(f"Status: {response.status}")
                if response.status == 200:
                    data = json.loads(result)
                    if "result" in data:
                        content = data["result"].get("content", [])
                        if content and len(content) > 0:
                            print(f"✅ Enhanced chat response: {content[0].get('text', 'No text')[:100]}...")
                        else:
                            print(f"Response: {result}")
                    else:
                        print(f"Response: {result}")
                else:
                    print(f"❌ Response: {result}")
        except Exception as e:
            print(f"❌ Enhanced chat test failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_mcp_protocol())