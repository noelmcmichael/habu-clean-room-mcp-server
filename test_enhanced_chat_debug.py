#!/usr/bin/env python3
"""
Debug the enhanced chat agent to see why it's not using MCP tools
"""
import asyncio
import os

# Ensure real API mode
os.environ["HABU_USE_MOCK_DATA"] = "false"

from agents.enhanced_habu_chat_agent import enhanced_habu_agent

async def test_enhanced_chat_debug():
    """Test enhanced chat agent directly"""
    print("🔍 DEBUGGING ENHANCED CHAT AGENT WITH REAL API")
    print("="*55)
    
    # Test direct agent call
    print("\n🤖 Testing Enhanced Chat Agent Directly...")
    
    try:
        response = await enhanced_habu_agent.process_request(
            "What cleanrooms are available and what templates can I use?"
        )
        
        print("✅ Enhanced chat agent successful")
        print(f"Response: {response}")
        
        # Check if tools were used
        if hasattr(response, 'tools_used'):
            print(f"Tools used: {response.tools_used}")
        
    except Exception as e:
        print(f"❌ Enhanced chat agent error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_enhanced_chat_debug())