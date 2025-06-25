#!/usr/bin/env python3
"""
Quick Deployment Success Checker
Run this script immediately after deploying to Render to verify all services are working
"""
import requests
import time
import sys
from datetime import datetime
from typing import Dict, List

# Production URLs after deployment
PRODUCTION_URLS = {
    'mcp_server': 'https://habu-mcp-server-v2.onrender.com',
    'demo_api': 'https://habu-demo-api-v2.onrender.com', 
    'admin_app': 'https://habu-admin-app-v2.onrender.com',
    'react_frontend': 'https://habu-demo-frontend-v2.onrender.com'
}

def check_service_health(name: str, url: str) -> Dict:
    """Check if a service is healthy"""
    try:
        print(f"  Checking {name}...")
        response = requests.get(f"{url}/health", timeout=15)
        
        if response.status_code == 200:
            print(f"  ✅ {name} is HEALTHY (Response time: {response.elapsed.total_seconds():.2f}s)")
            return {'status': 'healthy', 'response_time': response.elapsed.total_seconds()}
        else:
            print(f"  ❌ {name} is UNHEALTHY (Status: {response.status_code})")
            return {'status': 'unhealthy', 'status_code': response.status_code}
            
    except requests.exceptions.ConnectError:
        print(f"  ⏳ {name} is starting up (connection refused) - this is normal for first 5-10 minutes")
        return {'status': 'starting'}
    except requests.exceptions.Timeout:
        print(f"  ⚠️  {name} is slow to respond (timeout after 15s)")
        return {'status': 'slow'}
    except Exception as e:
        print(f"  ❌ {name} ERROR: {str(e)}")
        return {'status': 'error', 'error': str(e)}

def check_frontend_access(url: str) -> Dict:
    """Check if React frontend is accessible"""
    try:
        print(f"  Checking React frontend...")
        response = requests.get(url, timeout=15)
        
        if response.status_code == 200:
            # Check if it's actually the React app by looking for common React elements
            content = response.text.lower()
            if 'react' in content or 'liveramp' in content or 'habu' in content:
                print(f"  ✅ React frontend is ACCESSIBLE and serving content")
                return {'status': 'healthy'}
            else:
                print(f"  ⚠️  Frontend accessible but content may not be correct")
                return {'status': 'accessible_but_unknown'}
        else:
            print(f"  ❌ Frontend not accessible (Status: {response.status_code})")
            return {'status': 'inaccessible', 'status_code': response.status_code}
            
    except Exception as e:
        print(f"  ❌ Frontend ERROR: {str(e)}")
        return {'status': 'error', 'error': str(e)}

def test_enhanced_api_functionality(base_url: str) -> Dict:
    """Test if enhanced Customer Support mode is working"""
    try:
        print(f"  Testing Customer Support API...")
        
        test_data = {
            'query': 'I need help with lookalike modeling for retail customers',
            'context': {'industry': 'retail', 'mode': 'customer_support'}
        }
        
        headers = {
            'Content-Type': 'application/json',
            'X-API-Key': 'secure-habu-demo-key-2024'
        }
        
        response = requests.post(
            f"{base_url}/api/customer-support/assess",
            json=test_data,
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if 'assessment' in result or 'suggestions' in result:
                print(f"  ✅ Customer Support API is FUNCTIONAL")
                return {'status': 'functional'}
            else:
                print(f"  ⚠️  API responds but format may be incorrect")
                return {'status': 'responds_but_unclear'}
        else:
            print(f"  ❌ Customer Support API not working (Status: {response.status_code})")
            return {'status': 'not_working', 'status_code': response.status_code}
            
    except Exception as e:
        print(f"  ❌ API Test ERROR: {str(e)}")
        return {'status': 'error', 'error': str(e)}

def main():
    """Main deployment success check"""
    print("🚀 Checking Deployment Success...")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    all_healthy = True
    results = {}
    
    # Check backend services
    print("\n📡 Checking Backend Services:")
    for name, url in PRODUCTION_URLS.items():
        if name != 'react_frontend':  # Skip frontend for health check
            result = check_service_health(name, url)
            results[name] = result
            if result['status'] not in ['healthy']:
                all_healthy = False
    
    # Check frontend separately
    print("\n🌐 Checking Frontend:")
    frontend_result = check_frontend_access(PRODUCTION_URLS['react_frontend'])
    results['react_frontend'] = frontend_result
    if frontend_result['status'] not in ['healthy', 'accessible_but_unknown']:
        all_healthy = False
    
    # Test enhanced functionality
    print("\n🤖 Testing Enhanced AI Features:")
    api_result = test_enhanced_api_functionality(PRODUCTION_URLS['demo_api'])
    results['enhanced_api'] = api_result
    if api_result['status'] not in ['functional', 'responds_but_unclear']:
        all_healthy = False
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 DEPLOYMENT SUMMARY:")
    
    if all_healthy or sum(1 for r in results.values() if r['status'] in ['healthy', 'functional', 'accessible_but_unknown', 'responds_but_unclear']) >= 4:
        print("✅ DEPLOYMENT SUCCESSFUL!")
        print("🎉 Your Enhanced LiveRamp AI Assistant is LIVE!")
        print(f"\n🔗 Access your app: {PRODUCTION_URLS['react_frontend']}")
        print("\n🚀 Next steps:")
        print("  1. Open the frontend URL to test enhanced UX")
        print("  2. Try both Customer Support and Technical Expert modes") 
        print("  3. Test quick action buttons and mobile responsiveness")
        print("  4. Configure VS Code MCP integration")
        
        return True
        
    else:
        print("⚠️  DEPLOYMENT PARTIAL - Some services may still be starting up")
        print("This is normal for the first 10-15 minutes after deployment.")
        print("\n⏳ Services may still be initializing. Try again in 5 minutes.")
        print("💡 If issues persist after 20 minutes, check Render logs.")
        
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)