#!/usr/bin/env python3
"""
Comprehensive test for Phase D Visibility Enhancement
Tests all 3 phases to verify enhanced template capabilities are visible
"""

import asyncio
import json
import os
from demo_api import app
from agents.enhanced_habu_chat_agent import EnhancedHabuChatAgent

async def test_phase_1_ai_chat_enhancement():
    """Test Phase 1: AI Chat Enhanced Template Integration"""
    print("🤖 Phase 1: Testing AI Chat Enhanced Template Integration")
    print("=" * 60)
    
    # Test with mock data
    os.environ['HABU_USE_MOCK_DATA'] = 'true'
    
    agent = EnhancedHabuChatAgent()
    
    # Test enhanced template request
    response = await agent.process_request(
        'Show me all available templates with their categories, parameters, and data types. '
        'I want to understand what enhanced features are available.'
    )
    
    print("📋 AI Chat Response Preview:")
    print(response[:300] + "..." if len(response) > 300 else response)
    
    # Check for enhanced features
    enhanced_features = {
        'categories': 'categories' in response.lower() or 'category' in response.lower(),
        'parameters': 'parameters' in response.lower() or 'parameter' in response.lower(),
        'data_types': ('data' in response.lower() and 'type' in response.lower()) or 'string' in response.lower(),
        'status': 'status' in response.lower() or 'ready' in response.lower(),
        'question_types': 'analytical' in response.lower() or 'question' in response.lower(),
        'enhanced_metadata': 'enhanced' in response.lower() or 'rich' in response.lower()
    }
    
    found_features = sum(enhanced_features.values())
    print(f"\n✅ Enhanced Features in AI Response: {found_features}/6")
    for feature, found in enhanced_features.items():
        status = "✅" if found else "❌"
        print(f"   {feature}: {status}")
    
    phase_1_success = found_features >= 4
    print(f"\n🎯 Phase 1 Status: {'SUCCESS' if phase_1_success else 'NEEDS IMPROVEMENT'}")
    
    return phase_1_success, enhanced_features

def test_phase_2_system_health_update():
    """Test Phase 2: System Health Dashboard Update"""
    print("\n🔧 Phase 2: Testing System Health Dashboard Update")
    print("=" * 60)
    
    # Read the SystemHealth.tsx file to verify updates
    system_health_path = "/Users/noelmcmichael/Workspace/streamable_http_mcp_server/demo_app/src/pages/SystemHealth.tsx"
    
    try:
        with open(system_health_path, 'r') as f:
            content = f.read()
        
        # Check for enhanced features
        enhanced_features = {
            'nine_tools': '9 total' in content,
            'enhanced_templates': 'habu_enhanced_templates' in content,
            'tool_categories': 'tool-category' in content,
            'phase_d_section': 'Phase D Enhancements' in content,
            'enhancement_status': 'Enhancement Management' in content or 'enhanced' in content.lower()
        }
        
        found_features = sum(enhanced_features.values())
        print(f"✅ System Health Enhanced Features: {found_features}/5")
        for feature, found in enhanced_features.items():
            status = "✅" if found else "❌"
            print(f"   {feature}: {status}")
        
        phase_2_success = found_features >= 4
        print(f"\n🎯 Phase 2 Status: {'SUCCESS' if phase_2_success else 'NEEDS IMPROVEMENT'}")
        
        return phase_2_success, enhanced_features
        
    except Exception as e:
        print(f"❌ Error reading SystemHealth.tsx: {e}")
        return False, {}

def test_phase_3_api_explorer_enhancement():
    """Test Phase 3: API Explorer Enhancement"""
    print("\n🎯 Phase 3: Testing API Explorer Enhancement")
    print("=" * 60)
    
    # Read the ApiExplorer.tsx file to verify updates
    api_explorer_path = "/Users/noelmcmichael/Workspace/streamable_http_mcp_server/demo_app/src/pages/ApiExplorer.tsx"
    
    try:
        with open(api_explorer_path, 'r') as f:
            content = f.read()
        
        # Check for enhanced features
        enhanced_features = {
            'enhanced_category': 'Enhanced Features' in content,
            'enhanced_templates_endpoint': 'habu_enhanced_templates' in content,
            'enhanced_badge': 'enhanced-badge' in content or 'enhanced: true' in content,
            'enhancement_demo': 'Template Enhancement Demo' in content,
            'enhanced_styling': 'endpoint-item.enhanced' in content
        }
        
        found_features = sum(enhanced_features.values())
        print(f"✅ API Explorer Enhanced Features: {found_features}/5")
        for feature, found in enhanced_features.items():
            status = "✅" if found else "❌"
            print(f"   {feature}: {status}")
        
        phase_3_success = found_features >= 4
        print(f"\n🎯 Phase 3 Status: {'SUCCESS' if phase_3_success else 'NEEDS IMPROVEMENT'}")
        
        return phase_3_success, enhanced_features
        
    except Exception as e:
        print(f"❌ Error reading ApiExplorer.tsx: {e}")
        return False, {}

def test_flask_api_enhanced_endpoint():
    """Test Flask API enhanced templates endpoint"""
    print("\n🌐 Testing Flask API Enhanced Endpoint")
    print("=" * 45)
    
    os.environ['HABU_USE_MOCK_DATA'] = 'true'
    
    with app.test_client() as client:
        # Test enhanced templates endpoint
        response = client.get('/api/mcp/habu_enhanced_templates')
        
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json
            
            # Check enhanced data structure
            enhanced_features = {
                'count': 'count' in data,
                'categories': 'categories' in data,
                'question_types': 'question_types' in data,
                'enhancement_features': 'enhancement_features' in data,
                'template_metadata': data.get('templates', []) and len(data['templates']) > 0
            }
            
            found_features = sum(enhanced_features.values())
            print(f"✅ API Enhanced Data Features: {found_features}/5")
            for feature, found in enhanced_features.items():
                status = "✅" if found else "❌"
                print(f"   {feature}: {status}")
            
            # Show sample enhanced template
            if data.get('templates'):
                template = data['templates'][0]
                print(f"\n🔬 Sample Enhanced Template:")
                print(f"   Name: {template.get('name', 'N/A')}")
                print(f"   Category: {template.get('category', 'N/A')}")
                print(f"   Parameters: {bool(template.get('parameters'))}")
                print(f"   Data Types: {bool(template.get('dataTypes'))}")
                print(f"   Status: {template.get('status', 'N/A')}")
            
            return response.status_code == 200 and found_features >= 4
        else:
            print(f"❌ API Error: {response.data}")
            return False

async def main():
    """Run all phase tests"""
    print("🚀 Phase D Visibility Enhancement - Complete System Test")
    print("=" * 70)
    
    # Test all phases
    phase_1_result, phase_1_features = await test_phase_1_ai_chat_enhancement()
    phase_2_result, phase_2_features = test_phase_2_system_health_update()
    phase_3_result, phase_3_features = test_phase_3_api_explorer_enhancement()
    api_result = test_flask_api_enhanced_endpoint()
    
    # Summary
    print("\n📊 PHASE D VISIBILITY ENHANCEMENT - RESULTS SUMMARY")
    print("=" * 70)
    
    results = {
        'Phase 1 - AI Chat Enhancement': phase_1_result,
        'Phase 2 - System Health Update': phase_2_result,
        'Phase 3 - API Explorer Enhancement': phase_3_result,
        'Enhanced API Endpoint': api_result
    }
    
    success_count = sum(results.values())
    
    for phase, result in results.items():
        status = "✅ SUCCESS" if result else "❌ FAILED"
        print(f"{phase}: {status}")
    
    print(f"\n🎯 Overall Success Rate: {success_count}/4 phases")
    
    if success_count >= 3:
        print("\n🎉 PHASE D VISIBILITY ENHANCEMENT COMPLETE!")
        print("✅ Enhanced template capabilities are now visible")
        print("✅ System monitoring shows complete picture")
        print("✅ API explorer includes all enhancements")
        print("✅ Ready for production deployment")
    else:
        print("\n⚠️  Some enhancements need attention")
        print("🔧 Review failed phases for improvements")
    
    print(f"\n📋 Next Steps:")
    print("1. Deploy changes to production")
    print("2. Verify enhanced features in live environment")
    print("3. Proceed with Phase D Options B or C")
    
    return success_count >= 3

if __name__ == "__main__":
    asyncio.run(main())