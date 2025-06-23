#!/usr/bin/env python3
"""
Test Production Deployment - Live URL Verification
Run this after Render deployment is complete
"""

import requests
import json
import time

# Update these URLs after your Render deployment
BASE_URLS = {
    'frontend': 'https://habu-demo-frontend.onrender.com',
    'api': 'https://habu-demo-api.onrender.com', 
    'mcp': 'https://habu-mcp-server.onrender.com',
    'admin': 'https://habu-admin-app.onrender.com'
}

API_KEY = 'secure-habu-demo-key-2024'

def test_service(name, url, endpoint='/', expected_status=200, headers=None):
    """Test a service endpoint"""
    print(f"\n🧪 Testing {name}...")
    print(f"   URL: {url}{endpoint}")
    
    try:
        response = requests.get(f"{url}{endpoint}", headers=headers, timeout=30)
        status = "✅ PASS" if response.status_code == expected_status else "❌ FAIL"
        print(f"   Status: {response.status_code} {status}")
        
        if response.headers.get('content-type', '').startswith('application/json'):
            try:
                data = response.json()
                print(f"   Response: {json.dumps(data, indent=2)[:200]}...")
            except:
                print(f"   Response: {response.text[:100]}...")
        else:
            print(f"   Response: {response.text[:100]}...")
            
        return response.status_code == expected_status
        
    except requests.exceptions.RequestException as e:
        print(f"   ❌ ERROR: {e}")
        return False

def main():
    print("🚀 PRODUCTION DEPLOYMENT VERIFICATION")
    print("=" * 50)
    
    results = {}
    
    # Test React Frontend
    results['frontend'] = test_service(
        'React Frontend', 
        BASE_URLS['frontend']
    )
    
    # Test Demo API Health
    results['api_health'] = test_service(
        'Demo API Health', 
        BASE_URLS['api'], 
        '/api/health'
    )
    
    # Test Enhanced Chat
    results['enhanced_chat'] = test_service(
        'Enhanced Chat', 
        BASE_URLS['api'], 
        '/api/enhanced-chat',
        expected_status=405  # GET not allowed, but service is up
    )
    
    # Test MCP Server Capabilities  
    results['mcp_capabilities'] = test_service(
        'MCP Server Capabilities',
        BASE_URLS['mcp'],
        '/mcp/v1/capabilities',
        expected_status=401,  # Requires auth
        headers={'X-API-Key': API_KEY}
    )
    
    # Test Admin App
    results['admin'] = test_service(
        'Admin App',
        BASE_URLS['admin']
    )
    
    # Summary
    print(f"\n📊 DEPLOYMENT SUMMARY")
    print("=" * 30)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for service, passed_test in results.items():
        status = "✅ LIVE" if passed_test else "❌ DOWN"
        print(f"{service:20} {status}")
    
    print(f"\n🎯 Overall: {passed}/{total} services operational")
    
    if passed == total:
        print("\n🎉 DEPLOYMENT SUCCESSFUL!")
        print("Your Habu Clean Room MCP Server is live and ready for demos!")
        print(f"\n📱 Demo URL: {BASE_URLS['frontend']}")
        print(f"🔧 API URL: {BASE_URLS['api']}")
        print(f"🤖 MCP URL: {BASE_URLS['mcp']}/mcp")
    else:
        print(f"\n⚠️  {total - passed} services need attention.")
        print("Check Render dashboard for service logs.")

if __name__ == "__main__":
    main()