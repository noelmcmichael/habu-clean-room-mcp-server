#!/usr/bin/env python3
"""
Test script for OpenAI-powered enhanced chat functionality
"""
import asyncio
import json
from agents.enhanced_habu_chat_agent import enhanced_habu_agent

async def test_enhanced_chat():
    """Test the enhanced chat agent with OpenAI integration"""
    print("🤖 Testing Enhanced Habu Chat Agent with OpenAI GPT-4")
    print("=" * 60)
    
    # Enable mock mode first
    import os
    os.environ["HABU_USE_MOCK_DATA"] = "true"
    print("✅ Mock mode enabled for testing")
    
    # Test cases
    test_cases = [
        "Show me my partners",
        "What templates are available?",
        "Can you help me understand what this system does?",
        "How do I run an analysis?"
    ]
    
    for i, test_input in enumerate(test_cases, 1):
        print(f"\n📝 Test {i}: {test_input}")
        print("-" * 40)
        
        try:
            response = await enhanced_habu_agent.process_request(test_input)
            print(f"💬 Response: {response}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print()

if __name__ == "__main__":
    asyncio.run(test_enhanced_chat())