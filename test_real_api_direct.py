#!/usr/bin/env python3
"""
Test our MCP tools directly against the real API to see what's happening
"""
import asyncio
import os
import json

# Disable mock mode for testing
os.environ["HABU_USE_MOCK_DATA"] = "false"

# Import our MCP tools
from tools.habu_list_partners import habu_list_partners
from tools.habu_list_templates import habu_list_templates

async def test_real_api_tools():
    """Test our MCP tools against the real API"""
    print("🔧 Testing MCP Tools Against Real API")
    print("="*50)
    
    # Test 1: List Partners
    print("\n1. Testing habu_list_partners...")
    try:
        partners_result = await habu_list_partners()
        print("✅ Partners API call successful")
        print(f"Result: {partners_result[:500]}...")
    except Exception as e:
        print(f"❌ Partners API call failed: {e}")
    
    # Test 2: List Templates  
    print("\n2. Testing habu_list_templates...")
    try:
        templates_result = await habu_list_templates()
        print("✅ Templates API call successful")
        print(f"Result: {templates_result[:500]}...")
    except Exception as e:
        print(f"❌ Templates API call failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_real_api_tools())