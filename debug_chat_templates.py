#!/usr/bin/env python3
"""
Debug script to test what template endpoint the chat agent is actually using
"""
import asyncio
import json
import os
from agents.enhanced_habu_chat_agent import enhanced_habu_agent

async def test_template_usage():
    """Test which template endpoint is being called"""
    
    # Set to mock mode for predictable testing
    os.environ["HABU_USE_MOCK_DATA"] = "true"
    
    print("=== TESTING TEMPLATE ENDPOINT USAGE ===\n")
    
    # Test 1: Direct tool calls
    print("1. DIRECT TOOL CALLS:")
    from tools.habu_enhanced_templates import habu_enhanced_templates, habu_list_templates
    
    print("   a) Enhanced templates:")
    enhanced_result = await habu_enhanced_templates()
    enhanced_data = json.loads(enhanced_result)
    print(f"      - Status: {enhanced_data.get('status')}")
    print(f"      - Count: {enhanced_data.get('count')}")
    print(f"      - Enhancement features: {enhanced_data.get('enhancement_features')}")
    print(f"      - Categories: {enhanced_data.get('categories')}")
    
    print("\n   b) Basic templates (should be same as enhanced):")
    basic_result = await habu_list_templates()
    basic_data = json.loads(basic_result)
    print(f"      - Status: {basic_data.get('status')}")
    print(f"      - Count: {basic_data.get('count')}")
    print(f"      - Enhancement features: {basic_data.get('enhancement_features')}")
    
    # Test 2: Chat agent template requests
    print("\n2. CHAT AGENT TEMPLATE REQUESTS:")
    
    test_queries = [
        "What templates are available?",
        "Show me query templates",
        "What can I run?"
    ]
    
    for query in test_queries:
        print(f"\n   Query: '{query}'")
        response = await enhanced_habu_agent.process_request(query)
        print(f"   Response preview: {response[:200]}...")
        
        # Check if response mentions enhanced features
        enhanced_indicators = [
            "categories",
            "parameters",
            "data types", 
            "status",
            "enhanced",
            "Parameter",
            "Category",
            "Ready for execution"
        ]
        
        found_indicators = [ind for ind in enhanced_indicators if ind.lower() in response.lower()]
        print(f"   Enhanced indicators found: {found_indicators}")

    # Test 3: Check imports in agent
    print("\n3. AGENT IMPORT ANALYSIS:")
    import inspect
    from agents.enhanced_habu_chat_agent import EnhancedHabuChatAgent
    
    # Get the source code to see which function is being imported
    source = inspect.getsource(EnhancedHabuChatAgent)
    
    if "habu_enhanced_templates" in source:
        print("   ✅ Agent imports habu_enhanced_templates")
    else:
        print("   ❌ Agent does NOT import habu_enhanced_templates")
        
    if "habu_list_templates" in source:
        print("   ⚠️  Agent also imports habu_list_templates (could be confusion)")
    
    # Test 4: Check specific system prompt mentions
    print("\n4. SYSTEM PROMPT ANALYSIS:")
    agent = EnhancedHabuChatAgent()
    
    # Check if the agent is using the enhanced tools in its LLM system prompt
    if hasattr(agent, '_llm_powered_processing'):
        source = inspect.getsource(agent._llm_powered_processing)
        if "habu_enhanced_templates" in source:
            print("   ✅ System prompt likely references enhanced templates")
        else:
            print("   ❌ System prompt may not be using enhanced templates")

if __name__ == "__main__":
    asyncio.run(test_template_usage())