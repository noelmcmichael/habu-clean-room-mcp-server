import asyncio
import httpx
import json

async def test_mcp_server():
    """Test the MCP server functionality."""
    base_url = "http://localhost:8000/mcp/"
    headers = {
        "X-API-Key": "test-api-key-123",
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream"
    }
    
    async with httpx.AsyncClient() as client:
        # Test server capabilities
        print("Testing MCP server initialization...")
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "test-client",
                    "version": "1.0.0"
                }
            }
        }
        
        try:
            response = await client.post(base_url, json=init_request, headers=headers)
            print(f"Initialize response status: {response.status_code}")
            if response.status_code == 200:
                print("✅ MCP server initialized successfully")
                print(f"Response: {response.text[:200]}...")
            else:
                print(f"❌ Initialization failed: {response.text}")
                return
        except Exception as e:
            print(f"❌ Error connecting to MCP server: {e}")
            return
        
        # Test listing tools
        print("\nTesting tools/list...")
        tools_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list"
        }
        
        try:
            response = await client.post(base_url, json=tools_request, headers=headers)
            print(f"Tools list response status: {response.status_code}")
            if response.status_code == 200:
                print("✅ Tools listed successfully")
                print(f"Response: {response.text}")
            else:
                print(f"❌ Tools list failed: {response.text}")
        except Exception as e:
            print(f"❌ Error listing tools: {e}")

if __name__ == "__main__":
    asyncio.run(test_mcp_server())