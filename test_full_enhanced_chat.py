#!/usr/bin/env python3
"""
Test the enhanced chat agent with full OpenAI integration and real API
"""
import asyncio
import os
import keyring

# Set up environment
os.environ["HABU_USE_MOCK_DATA"] = "false"

# Get OpenAI API key
try:
    openai_key = keyring.get_password("memex", "OpenAI Key")
    if openai_key:
        os.environ["OPENAI_API_KEY"] = openai_key
        print("✅ OpenAI API key configured")
    else:
        print("❌ OpenAI API key not found")
except Exception as e:
    print(f"❌ Error getting OpenAI key: {e}")

from agents.enhanced_habu_chat_agent import enhanced_habu_agent

async def test_full_enhanced_chat():
    """Test enhanced chat with full OpenAI integration"""
    print("🚀 TESTING ENHANCED CHAT WITH FULL OPENAI + REAL API")
    print("="*60)
    
    test_questions = [
        "What cleanrooms and templates do I have access to?",
        "Show me my data partners and available analytics templates",
        "What kinds of analyses can I run on my data?"
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n{i}. Question: '{question}'")
        print("-" * 50)
        
        try:
            response = await enhanced_habu_agent.process_request(question)
            print(f"Response: {response}")
            
            # Check if the agent has context memory
            if hasattr(enhanced_habu_agent, 'context_memory'):
                print(f"Context memory: {len(enhanced_habu_agent.context_memory)} entries")
                
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*60)
    print("🎯 ENHANCED CHAT TEST COMPLETE")
    print("="*60)

if __name__ == "__main__":
    asyncio.run(test_full_enhanced_chat())