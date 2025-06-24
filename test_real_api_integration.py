#!/usr/bin/env python3
"""
Test the complete real API integration through the Flask API bridge
"""
import asyncio
import json
import httpx

async def test_real_api_integration():
    """Test complete integration with real API through Flask bridge"""
    print("🌐 TESTING COMPLETE REAL API INTEGRATION")
    print("="*50)
    
    # Test Flask API health
    print("\n1️⃣ Testing Flask API Health...")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:5001/api/health")
            health = response.json()
            print(f"✅ Flask API: {health['status']}")
            print(f"   Mock mode: {health['mock_mode']}")
            print(f"   OpenAI: {'✅' if health['openai_configured'] else '❌'}")
    except Exception as e:
        print(f"❌ Flask API error: {e}")
        return
    
    # Test enhanced chat with real API
    print("\n2️⃣ Testing Enhanced Chat with Real API...")
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            chat_request = {
                "user_input": "What cleanrooms are available and what data partners do we have?"
            }
            
            response = await client.post(
                "http://localhost:5001/api/enhanced-chat",
                json=chat_request
            )
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Enhanced chat successful")
                print(f"   Response length: {len(result.get('response', ''))}")
                print(f"   Tools used: {result.get('tools_used', [])}")
                print("\n📝 Chat Response:")
                print("-" * 30)
                print(result.get('response', 'No response')[:500] + "...")
                
                if 'mcp_results' in result:
                    print(f"\n🔧 MCP Tools Called: {len(result['mcp_results'])}")
                    for tool, tool_result in result['mcp_results'].items():
                        print(f"   • {tool}: {len(str(tool_result))} chars")
                        
            else:
                print(f"❌ Chat request failed: {response.status_code}")
                print(f"   Error: {response.text}")
                
    except Exception as e:
        print(f"❌ Enhanced chat error: {e}")
    
    # Test specific MCP tool through Flask API
    print("\n3️⃣ Testing Direct MCP Tool Access...")
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Test list templates endpoint
            response = await client.get("http://localhost:5001/api/mcp/habu_list_templates")
            
            if response.status_code == 200:
                templates = response.json()
                print("✅ Direct MCP tool access successful")
                print(f"   Templates found: {templates.get('count', 0)}")
                if templates.get('count', 0) > 0:
                    print("   Template examples:")
                    for template in templates.get('templates', [])[:2]:
                        print(f"     • {template.get('name', 'Unknown')}")
                        print(f"       Status: {template.get('status', 'Unknown')}")
            else:
                print(f"❌ Direct MCP tool failed: {response.status_code}")
                
    except Exception as e:
        print(f"❌ Direct MCP tool error: {e}")
    
    print("\n" + "="*50)
    print("🎯 REAL API INTEGRATION TEST COMPLETE")
    print("="*50)

if __name__ == "__main__":
    asyncio.run(test_real_api_integration())