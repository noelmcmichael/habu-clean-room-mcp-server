#!/usr/bin/env python3
"""
Test templates directly to see what's happening
"""
import asyncio
import os
import json

# Ensure real API mode
os.environ["HABU_USE_MOCK_DATA"] = "false"

from agents.enhanced_habu_chat_agent import enhanced_habu_agent

async def test_templates():
    """Test template requests"""
    print("📋 TESTING TEMPLATE REQUESTS WITH REAL API")
    print("="*50)
    
    test_questions = [
        "What templates are available?",
        "Show me the query templates",
        "What analyses can I run?",
        "List all templates",
        "What cleanrooms and templates do I have access to?"
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n{i}. Question: '{question}'")
        try:
            response = await enhanced_habu_agent.process_request(question)
            print(f"   Response: {response[:200]}...")
        except Exception as e:
            print(f"   Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_templates())