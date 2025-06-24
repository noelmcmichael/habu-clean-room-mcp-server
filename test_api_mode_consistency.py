#!/usr/bin/env python3
"""
Test API mode consistency between chat agent and tools
"""
import asyncio
import json
import os
from agents.enhanced_habu_chat_agent import enhanced_habu_agent
from tools.habu_enhanced_templates import habu_enhanced_templates

async def test_api_consistency():
    """Test what API mode different components are using"""
    
    print("=== API MODE CONSISTENCY TEST ===\n")
    
    # Test 1: Check environment variable
    mock_mode = os.getenv("HABU_USE_MOCK_DATA", "false").lower() == "true"
    print(f"1. ENVIRONMENT VARIABLE:")
    print(f"   HABU_USE_MOCK_DATA = {os.getenv('HABU_USE_MOCK_DATA', 'not set')}")
    print(f"   Mock mode active: {mock_mode}")
    
    # Test 2: Direct tool call
    print(f"\n2. DIRECT ENHANCED TEMPLATES CALL:")
    try:
        result = await habu_enhanced_templates()
        data = json.loads(result)
        is_mock = data.get('mock_mode', False)
        print(f"   Mock mode in result: {is_mock}")
        print(f"   Template count: {data.get('count')}")
        print(f"   Categories: {data.get('categories', [])[:3]}...")
        print(f"   Ready templates: {data.get('ready_templates')}")
    except Exception as e:
        print(f"   ERROR: {e}")
    
    # Test 3: Chat agent template request
    print(f"\n3. CHAT AGENT TEMPLATE REQUEST:")
    try:
        response = await enhanced_habu_agent.process_request("What templates are available?")
        print(f"   Response length: {len(response)} chars")
        
        # Check for mock vs real indicators
        mock_indicators = ["mock", "MOCK", "test data", "sample"]
        real_indicators = ["Sentiment Analysis", "Geotrace", "TimberMac", "MISSING_DATASETS"]
        enhanced_indicators = ["Category:", "Status:", "Parameters:", "Data Types:"]
        
        mock_found = any(ind in response for ind in mock_indicators)
        real_found = any(ind in response for ind in real_indicators) 
        enhanced_found = any(ind in response for ind in enhanced_indicators)
        
        print(f"   Mock indicators found: {mock_found}")
        print(f"   Real API indicators found: {real_found}")
        print(f"   Enhanced features found: {enhanced_found}")
        
        # Show first 300 chars for analysis
        print(f"   Response preview: {response[:300]}...")
        
    except Exception as e:
        print(f"   ERROR: {e}")
    
    # Test 4: Force mock mode and compare
    print(f"\n4. FORCED MOCK MODE COMPARISON:")
    os.environ["HABU_USE_MOCK_DATA"] = "true"
    try:
        mock_result = await habu_enhanced_templates()
        mock_data = json.loads(mock_result)
        print(f"   Mock templates count: {mock_data.get('count')}")
        print(f"   Mock categories: {mock_data.get('categories', [])[:3]}...")
        print(f"   Mock ready count: {mock_data.get('ready_templates')}")
    except Exception as e:
        print(f"   ERROR: {e}")
    finally:
        # Restore original setting
        os.environ["HABU_USE_MOCK_DATA"] = "false"
    
    print(f"\n5. RECOMMENDATIONS:")
    if mock_mode:
        print("   ⚠️  System is in MOCK mode - switch to real API for production")
    else:
        print("   ✅ System is in REAL API mode")
    
    print("   📋 For enhanced chat responses:")
    print("   - Ensure consistent API mode across all components")
    print("   - Update system prompt to match actual available templates")
    print("   - Verify enhanced metadata is being utilized")

if __name__ == "__main__":
    asyncio.run(test_api_consistency())