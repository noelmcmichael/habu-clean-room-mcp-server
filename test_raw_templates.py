#!/usr/bin/env python3
"""
Test the raw templates tool directly
"""
import asyncio
import os
import json

# Ensure real API mode
os.environ["HABU_USE_MOCK_DATA"] = "false"

from tools.habu_list_templates import habu_list_templates

async def test_raw_templates():
    """Test raw templates tool"""
    print("🔧 TESTING RAW TEMPLATES TOOL WITH REAL API")
    print("="*50)
    
    try:
        result = await habu_list_templates()
        print("✅ Raw templates call successful")
        
        # Parse the result
        data = json.loads(result)
        print(f"Status: {data.get('status')}")
        print(f"Count: {data.get('count')}")
        print(f"Mock mode: {data.get('mock_mode', 'Not specified')}")
        
        if data.get('templates'):
            print("\nTemplates found:")
            for i, template in enumerate(data['templates'][:3], 1):
                print(f"{i}. {template.get('name', 'Unknown')}")
                print(f"   Category: {template.get('category', 'Unknown')}")
                print(f"   Status: {template.get('status', 'Unknown')}")
                print(f"   Cleanroom: {template.get('cleanroom_name', 'Unknown')}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_raw_templates())