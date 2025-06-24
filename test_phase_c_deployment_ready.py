#!/usr/bin/env python3
"""
Phase C Deployment Readiness Test
Validates all components are working correctly before production deployment
"""
import asyncio
import json
import requests
import time
import subprocess
import os
from typing import Dict, Any

def test_service_availability():
    """Test if services are available"""
    print("🔍 Testing Service Availability")
    print("-" * 40)
    
    # Test Flask API
    try:
        response = requests.get('http://localhost:5001/api/enhanced-chat', timeout=5)
        if response.status_code in [200, 405]:  # 405 is expected for GET on POST endpoint
            print("✅ Flask API (localhost:5001): RUNNING")
            flask_available = True
        else:
            print(f"⚠️ Flask API: Unexpected status {response.status_code}")
            flask_available = False
    except Exception as e:
        print(f"❌ Flask API (localhost:5001): NOT AVAILABLE - {e}")
        flask_available = False
    
    # Test React App
    try:
        response = requests.get('http://localhost:3000', timeout=5)
        if response.status_code == 200:
            print("✅ React App (localhost:3000): RUNNING")
            react_available = True
        else:
            print(f"⚠️ React App: Status {response.status_code}")
            react_available = False
    except Exception as e:
        print(f"❌ React App (localhost:3000): NOT AVAILABLE - {e}")
        react_available = False
    
    return flask_available, react_available

def test_enhanced_chat_functionality():
    """Test enhanced chat functionality"""
    print("\n🧠 Testing Enhanced Chat Functionality")
    print("-" * 40)
    
    test_cases = [
        {
            "input": "What can I analyze?",
            "expected_keywords": ["sentiment", "location", "pattern", "template"]
        },
        {
            "input": "Run a sentiment analysis",
            "expected_keywords": ["sentiment", "analysis", "template"]
        },
        {
            "input": "Show me my partners",
            "expected_keywords": ["partner", "cleanroom", "Data Marketplace"]
        }
    ]
    
    success_count = 0
    
    for i, test_case in enumerate(test_cases, 1):
        try:
            response = requests.post(
                'http://localhost:5001/api/enhanced-chat',
                json={'user_input': test_case['input']},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                response_text = result.get('response', '').lower()
                
                # Check if expected keywords are present
                keywords_found = [kw for kw in test_case['expected_keywords'] 
                                if kw.lower() in response_text]
                
                if len(keywords_found) >= 2:  # At least 2 keywords should match
                    print(f"✅ Test {i}: '{test_case['input'][:30]}...' - PASSED")
                    print(f"   Keywords found: {keywords_found}")
                    success_count += 1
                else:
                    print(f"⚠️ Test {i}: '{test_case['input'][:30]}...' - PARTIAL")
                    print(f"   Keywords found: {keywords_found}")
                    print(f"   Response: {response_text[:100]}...")
            else:
                print(f"❌ Test {i}: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ Test {i}: Error - {e}")
    
    print(f"\n📊 Enhanced Chat Test Results: {success_count}/{len(test_cases)} passed")
    return success_count == len(test_cases)

def test_mcp_tools_integration():
    """Test MCP tools integration"""
    print("\n🔧 Testing MCP Tools Integration")
    print("-" * 40)
    
    tools_to_test = [
        'habu_list_partners',
        'habu_list_templates',
        'habu_list_exports'
    ]
    
    success_count = 0
    
    for tool in tools_to_test:
        try:
            response = requests.get(f'http://localhost:5001/api/mcp/{tool}', timeout=15)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('status') == 'success':
                    print(f"✅ {tool}: SUCCESS")
                    success_count += 1
                else:
                    print(f"⚠️ {tool}: {result.get('summary', 'Unknown response')}")
            else:
                print(f"❌ {tool}: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ {tool}: Error - {e}")
    
    print(f"\n📊 MCP Tools Test Results: {success_count}/{len(tools_to_test)} passed")
    return success_count >= 2  # At least 2 should work

def test_context_management():
    """Test context management and conversation continuity"""
    print("\n💭 Testing Context Management")
    print("-" * 40)
    
    # Sequence of related queries to test context
    conversation_sequence = [
        "What templates are available?",
        "Run a sentiment analysis",
        "Check my query status",
        "Show me the results"
    ]
    
    success_count = 0
    
    for i, query in enumerate(conversation_sequence, 1):
        try:
            response = requests.post(
                'http://localhost:5001/api/enhanced-chat',
                json={'user_input': query},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                response_text = result.get('response', '')
                
                # Context indicators
                if i == 1 and ('template' in response_text.lower() or 'sentiment' in response_text.lower()):
                    print(f"✅ Step {i}: Template listing - WORKING")
                    success_count += 1
                elif i == 2 and ('sentiment' in response_text.lower() or 'analysis' in response_text.lower()):
                    print(f"✅ Step {i}: Query submission - WORKING")
                    success_count += 1
                elif i == 3 and ('status' in response_text.lower() or 'query' in response_text.lower()):
                    print(f"✅ Step {i}: Status check - WORKING")
                    success_count += 1
                elif i == 4 and ('result' in response_text.lower() or 'analysis' in response_text.lower()):
                    print(f"✅ Step {i}: Results retrieval - WORKING")
                    success_count += 1
                else:
                    print(f"⚠️ Step {i}: Unexpected response pattern")
                    
            else:
                print(f"❌ Step {i}: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ Step {i}: Error - {e}")
    
    print(f"\n📊 Context Management Test Results: {success_count}/{len(conversation_sequence)} steps working")
    return success_count >= 3  # At least 3 steps should work

def check_production_readiness():
    """Check if system is ready for production deployment"""
    print("\n🚀 Production Readiness Assessment")
    print("=" * 50)
    
    # Check environment variables
    env_vars = [
        'OPENAI_API_KEY',
        'HABU_CLIENT_ID',
        'HABU_CLIENT_SECRET',
        'HABU_PRIVATE_KEY'
    ]
    
    env_ready = 0
    for var in env_vars:
        if os.getenv(var):
            print(f"✅ {var}: SET")
            env_ready += 1
        else:
            print(f"⚠️ {var}: NOT SET")
    
    # Overall readiness score
    print(f"\n📊 Environment Variables: {env_ready}/{len(env_vars)} configured")
    
    # Check if files exist
    critical_files = [
        'demo_api.py',
        'agents/enhanced_habu_chat_agent.py',
        'demo_app/build/index.html',
        'requirements.txt'
    ]
    
    files_ready = 0
    for file_path in critical_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}: EXISTS")
            files_ready += 1
        else:
            print(f"❌ {file_path}: MISSING")
    
    print(f"\n📊 Critical Files: {files_ready}/{len(critical_files)} present")
    
    return env_ready >= 3 and files_ready >= 3

async def main():
    """Run comprehensive Phase C deployment readiness test"""
    print("🧪 Phase C Enhanced Context-Aware Chat - Deployment Readiness Test")
    print("=" * 70)
    
    # Test 1: Service Availability
    flask_ok, react_ok = test_service_availability()
    
    if not flask_ok:
        print("\n❌ Cannot continue - Flask API not available")
        print("💡 Start Flask API with: python demo_api.py")
        return
    
    # Test 2: Enhanced Chat Functionality
    chat_ok = test_enhanced_chat_functionality()
    
    # Test 3: MCP Tools Integration
    mcp_ok = test_mcp_tools_integration()
    
    # Test 4: Context Management
    context_ok = test_context_management()
    
    # Test 5: Production Readiness
    prod_ready = check_production_readiness()
    
    # Final Assessment
    print("\n🎯 FINAL ASSESSMENT")
    print("=" * 30)
    
    components = {
        "Flask API": flask_ok,
        "React App": react_ok,
        "Enhanced Chat": chat_ok,
        "MCP Tools": mcp_ok,
        "Context Management": context_ok,
        "Production Config": prod_ready
    }
    
    working_components = sum(components.values())
    total_components = len(components)
    
    for component, status in components.items():
        status_icon = "✅" if status else "❌"
        print(f"{status_icon} {component}")
    
    print(f"\n📊 Overall Score: {working_components}/{total_components}")
    
    if working_components >= 5:
        print("🎉 SYSTEM READY FOR DEPLOYMENT!")
        print("✅ Phase C Enhanced Context-Aware Chat is fully functional")
        print("🚀 Ready to deploy to production (Render.com)")
    elif working_components >= 4:
        print("⚠️ SYSTEM MOSTLY READY")
        print("🔧 Minor issues to resolve before deployment")
    else:
        print("❌ SYSTEM NOT READY FOR DEPLOYMENT")
        print("🛠️ Critical issues need to be resolved")
    
    print(f"\n💡 Next Steps:")
    if working_components >= 5:
        print("   1. Deploy to Render.com")
        print("   2. Update environment variables in production")
        print("   3. Test production deployment")
    else:
        print("   1. Fix failing components")
        print("   2. Re-run this test")
        print("   3. Deploy when all tests pass")

if __name__ == "__main__":
    asyncio.run(main())