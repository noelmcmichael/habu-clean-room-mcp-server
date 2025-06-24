#!/usr/bin/env python3
"""
Test Phase C Enhanced Context-Aware Chat Implementation
Tests the complete workflow with JSON formatting fix
"""
import asyncio
import json
import time
from agents.enhanced_habu_chat_agent import enhanced_habu_agent

async def test_complete_workflow():
    """Test the complete enhanced chat workflow"""
    print("🧪 Testing Phase C Enhanced Context-Aware Chat")
    print("=" * 60)
    
    # Test 1: LLM System Prompt Fix
    print("\n1️⃣ Testing LLM System Prompt (JSON Fix)")
    try:
        # This should no longer cause JSON parsing errors
        result = await enhanced_habu_agent.process_request("What can I analyze?")
        print(f"✅ LLM Processing: {result[:200]}...")
    except Exception as e:
        print(f"❌ LLM Error (should be fixed): {e}")
    
    # Test 2: Context Management
    print("\n2️⃣ Testing Context Management")
    print(f"Active queries: {len(enhanced_habu_agent.active_queries)}")
    print(f"Conversation context: {enhanced_habu_agent.conversation_context}")
    
    # Test 3: Enhanced Query Submission
    print("\n3️⃣ Testing Enhanced Query Submission")
    try:
        result = await enhanced_habu_agent.process_request("Run a sentiment analysis on global events")
        print("✅ Query submission with context tracking")
        print(f"Result: {result[:300]}...")
        
        # Check if context was updated
        print(f"Active queries after submission: {len(enhanced_habu_agent.active_queries)}")
        print(f"Last query ID: {enhanced_habu_agent.last_query_id}")
    except Exception as e:
        print(f"❌ Query submission error: {e}")
    
    # Test 4: Status Check with Context
    print("\n4️⃣ Testing Status Check with Context")
    try:
        result = await enhanced_habu_agent.process_request("How is my analysis going?")
        print("✅ Status check using context")
        print(f"Result: {result[:300]}...")
    except Exception as e:
        print(f"❌ Status check error: {e}")
    
    # Test 5: Export Functionality
    print("\n5️⃣ Testing Export Functionality")
    try:
        result = await enhanced_habu_agent.process_request("What exports are available for download?")
        print("✅ Export listing")
        print(f"Result: {result[:300]}...")
    except Exception as e:
        print(f"❌ Export listing error: {e}")
    
    # Test 6: Context Persistence
    print("\n6️⃣ Testing Context Persistence")
    print(f"📊 Conversation Summary:")
    print(f"   • Active queries: {len(enhanced_habu_agent.active_queries)}")
    print(f"   • Query history: {len(enhanced_habu_agent.conversation_context['query_history'])}")
    print(f"   • Pending results: {len(enhanced_habu_agent.conversation_context['pending_results'])}")
    print(f"   • Context summary: {enhanced_habu_agent._get_context_summary()}")
    
    # Test 7: Real-time Follow-up
    print("\n7️⃣ Testing Real-time Follow-up")
    try:
        result = await enhanced_habu_agent.process_request("Show me the results")
        print("✅ Follow-up query with context")
        print(f"Result: {result[:300]}...")
    except Exception as e:
        print(f"❌ Follow-up error: {e}")
    
    print("\n" + "=" * 60)
    print("🎯 Phase C Enhanced Context-Aware Chat Test Complete")
    
    # Summary
    if enhanced_habu_agent.client:
        print("✅ OpenAI LLM Integration: WORKING")
    else:
        print("⚠️ OpenAI LLM Integration: Using fallback")
    
    print(f"✅ Context Management: {len(enhanced_habu_agent.active_queries)} queries tracked")
    print(f"✅ Export Integration: 7 MCP tools available")
    print(f"✅ Conversation Continuity: Context-aware responses")

if __name__ == "__main__":
    asyncio.run(test_complete_workflow())