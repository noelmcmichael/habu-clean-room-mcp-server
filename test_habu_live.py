"""
Test Habu API integration with real credentials
"""
import asyncio
import json
from tools.habu_list_partners import habu_list_partners
from tools.habu_list_templates import habu_list_templates
from agents.habu_chat_agent import habu_agent

async def test_habu_api():
    """Test Habu API with real credentials"""
    print("🧪 Testing Habu API with Real Credentials")
    print("=" * 50)
    
    # Test 1: List Partners
    print("\n1. Testing habu_list_partners...")
    try:
        result = await habu_list_partners()
        result_data = json.loads(result)
        print(f"✅ Status: {result_data['status']}")
        if result_data['status'] == 'success':
            print(f"✅ Partner Count: {result_data['count']}")
            if result_data['partners']:
                print("✅ Partners found:")
                for partner in result_data['partners'][:3]:  # Show first 3
                    name = partner.get('name', 'Unknown')
                    print(f"   • {name}")
        else:
            print(f"❌ Error: {result_data.get('summary', 'Unknown error')}")
    except Exception as e:
        print(f"❌ Exception: {e}")
    
    # Test 2: List Templates  
    print("\n2. Testing habu_list_templates...")
    try:
        result = await habu_list_templates()
        result_data = json.loads(result)
        print(f"✅ Status: {result_data['status']}")
        if result_data['status'] == 'success':
            print(f"✅ Template Count: {result_data['count']}")
            if result_data['templates']:
                print("✅ Templates found:")
                for template in result_data['templates'][:3]:  # Show first 3
                    name = template.get('name', 'Unknown')
                    desc = template.get('description', 'No description')[:50]
                    print(f"   • {name}: {desc}...")
        else:
            print(f"❌ Error: {result_data.get('summary', 'Unknown error')}")
    except Exception as e:
        print(f"❌ Exception: {e}")
    
    # Test 3: Chat Agent
    print("\n3. Testing chat agent with 'list partners'...")
    try:
        result = await habu_agent.process_request("list my clean room partners")
        print(f"✅ Chat Agent Response:")
        print(result[:300] + "..." if len(result) > 300 else result)
    except Exception as e:
        print(f"❌ Exception: {e}")
    
    print("\n4. Testing chat agent with 'show templates'...")
    try:
        result = await habu_agent.process_request("what templates are available?")
        print(f"✅ Chat Agent Response:")
        print(result[:300] + "..." if len(result) > 300 else result)
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    asyncio.run(test_habu_api())