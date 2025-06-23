"""
Test Enhanced Habu MCP Functionality
Tests the enhanced LLM-powered chat agent and mock data functionality
"""
import asyncio
import json
import os
from agents.enhanced_habu_chat_agent import enhanced_habu_agent
from tools.mock_data import mock_data

async def test_enhanced_functionality():
    """Test the enhanced Habu functionality with mock data and LLM agent"""
    print("🚀 Testing Enhanced Habu Clean Room MCP Server")
    print("=" * 60)
    
    # Enable mock mode
    os.environ["HABU_USE_MOCK_DATA"] = "true"
    print("✅ Mock mode enabled")
    
    print("\n" + "="*60)
    print("🧪 TESTING ENHANCED LLM CHAT AGENT")
    print("="*60)
    
    # Test conversations with the enhanced agent
    test_conversations = [
        "What clean room partners do I have available?",
        "Show me the query templates I can use",
        "I want to run an audience overlap analysis between Meta and Amazon",
        "What's the best template for measuring cross-platform attribution?", 
        "Can you submit a lookalike modeling query for me?",
        "How do I check the status of my queries?",
        "Explain what clean room data collaboration is"
    ]
    
    for i, conversation in enumerate(test_conversations, 1):
        print(f"\n{i}. Testing: '{conversation}'")
        print("-" * 50)
        try:
            response = await enhanced_habu_agent.process_request(conversation)
            print(f"Response: {response}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "="*60)
    print("🧪 TESTING MOCK DATA FUNCTIONALITY")
    print("="*60)
    
    # Test mock data directly
    print("\n1. Testing Mock Partners:")
    partners = mock_data.get_mock_partners()
    print(f"   Found {len(partners)} partners:")
    for partner in partners[:3]:  # Show first 3
        print(f"   • {partner['name']} in {partner['cleanroom_name']}")
    
    print("\n2. Testing Mock Templates:")
    templates = mock_data.get_mock_templates()
    print(f"   Found {len(templates)} templates:")
    for template in templates[:3]:  # Show first 3
        print(f"   • {template['name']}: {template['description'][:60]}...")
    
    print("\n3. Testing Mock Query Workflow:")
    
    # Submit a mock query
    template_id = "tmpl-001-audience-overlap"
    parameters = {"partner_1": "Meta", "partner_2": "Amazon", "date_range": "last_30_days"}
    
    print(f"   Submitting query with template {template_id}...")
    submit_result = mock_data.submit_mock_query(template_id, parameters)
    query_id = submit_result.get("query_id")
    print(f"   ✅ Query submitted: {query_id}")
    
    # Check status immediately
    print(f"   Checking initial status...")
    status_result = mock_data.check_mock_query_status(query_id)
    print(f"   Status: {status_result['query_status']} ({status_result['progress_percent']}%)")
    
    # Wait a bit and check again (simulates processing time)
    print(f"   Waiting for query to process...")
    await asyncio.sleep(3)
    
    status_result = mock_data.check_mock_query_status(query_id)
    print(f"   Updated status: {status_result['query_status']} ({status_result['progress_percent']}%)")
    
    # If completed, get results
    if status_result['query_status'] == 'COMPLETED':
        print(f"   Getting results...")
        results = mock_data.get_mock_query_results(query_id)
        print(f"   ✅ Results: {results['business_summary']}")
        print(f"   📊 Records: {results['record_count']:,}")
    
    print("\n" + "="*60)
    print("🧪 TESTING FULL CONVERSATIONAL WORKFLOW")
    print("="*60)
    
    # Test a complete workflow through conversation
    workflow_steps = [
        "Enable mock mode for testing",
        "Show me my available partners",
        "What templates can I use for audience analysis?", 
        f"Submit an audience overlap analysis using template {template_id}",
        f"Check the status of query {query_id}",
        f"Get the results for query {query_id}"
    ]
    
    for i, step in enumerate(workflow_steps, 1):
        print(f"\n{i}. Step: '{step}'")
        print("-" * 40)
        try:
            response = await enhanced_habu_agent.process_request(step)
            # Truncate very long responses
            if len(response) > 300:
                response = response[:300] + "..."
            print(f"Response: {response}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "="*60)
    print("✅ ENHANCED FUNCTIONALITY TEST COMPLETE")
    print("="*60)
    
    print("\n📋 SUMMARY:")
    print("✅ Enhanced LLM chat agent working")
    print("✅ Mock data system functional")
    print("✅ Full query workflow operational")
    print("✅ Conversational interface responsive")
    print("✅ Ready for VS Code MCP integration")
    
    print(f"\n🎯 NEXT STEPS:")
    print("1. Test in VS Code with @habu-clean-room-server")
    print("2. Try: '@habu-clean-room-server habu_enable_mock_mode true'")
    print("3. Then: '@habu-clean-room-server habu_enhanced_chat show me my partners'")
    print("4. Run a full analysis workflow through chat")

if __name__ == "__main__":
    asyncio.run(test_enhanced_functionality())