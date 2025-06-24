#!/usr/bin/env python3
"""
Test Flask API with Redis integration for Phase H optimization
"""

import requests
import json
import time

def test_flask_redis_integration():
    """Test Flask API endpoints with Redis caching"""
    
    # Base URL for local testing
    base_url = "http://localhost:5001"
    
    print("🚀 Testing Flask API with Redis Integration...")
    
    # Test 1: Root endpoint
    print("\n📊 Test 1: Root Endpoint")
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Root endpoint working: {data['service']}")
            print(f"Version: {data['version']}")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Root endpoint error: {e}")
    
    # Test 2: Health check
    print("\n💚 Test 2: Health Check")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check working: {data['status']}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")
    
    # Test 3: Cache stats
    print("\n📈 Test 3: Cache Statistics")
    try:
        response = requests.get(f"{base_url}/api/cache-stats")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Cache stats working")
            print(f"Connected: {data['cache_stats']['connected']}")
            if 'error' in data['cache_stats']:
                print(f"Info: {data['cache_stats']['error']}")
        else:
            print(f"❌ Cache stats failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Cache stats error: {e}")
    
    # Test 4: Enhanced chat (with caching)
    print("\n💬 Test 4: Enhanced Chat with Caching")
    try:
        chat_data = {
            "user_input": "What is the current status of the system?",
            "session_id": "test_session_123"
        }
        
        # First request
        start_time = time.time()
        response = requests.post(f"{base_url}/api/enhanced-chat", json=chat_data)
        first_request_time = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ First chat request successful ({first_request_time:.2f}s)")
            print(f"Cached: {data.get('cached', False)}")
            
            # Second identical request (should be cached)
            start_time = time.time()
            response2 = requests.post(f"{base_url}/api/enhanced-chat", json=chat_data)
            second_request_time = time.time() - start_time
            
            if response2.status_code == 200:
                data2 = response2.json()
                print(f"✅ Second chat request successful ({second_request_time:.2f}s)")
                print(f"Cached: {data2.get('cached', False)}")
                
                if second_request_time < first_request_time:
                    print(f"🚀 Cache optimization: {((first_request_time - second_request_time) / first_request_time * 100):.1f}% faster")
            else:
                print(f"❌ Second chat request failed: {response2.status_code}")
        else:
            print(f"❌ Chat request failed: {response.status_code}")
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"❌ Chat request error: {e}")
    
    # Test 5: Partners list (with caching)
    print("\n👥 Test 5: Partners List with Caching")
    try:
        # First request
        start_time = time.time()
        response = requests.get(f"{base_url}/api/mcp/habu_list_partners")
        first_request_time = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ First partners request successful ({first_request_time:.2f}s)")
            print(f"Cached: {data.get('cached', False)}")
            
            # Second request (should be cached)
            start_time = time.time()
            response2 = requests.get(f"{base_url}/api/mcp/habu_list_partners")
            second_request_time = time.time() - start_time
            
            if response2.status_code == 200:
                data2 = response2.json()
                print(f"✅ Second partners request successful ({second_request_time:.2f}s)")
                print(f"Cached: {data2.get('cached', False)}")
                
                if second_request_time < first_request_time:
                    print(f"🚀 Cache optimization: {((first_request_time - second_request_time) / first_request_time * 100):.1f}% faster")
            else:
                print(f"❌ Second partners request failed: {response2.status_code}")
        else:
            print(f"❌ Partners request failed: {response.status_code}")
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"❌ Partners request error: {e}")
    
    # Test 6: Enhanced templates (with caching)
    print("\n📋 Test 6: Enhanced Templates with Caching")
    try:
        # First request
        start_time = time.time()
        response = requests.get(f"{base_url}/api/mcp/habu_enhanced_templates?cleanroom_id=test_123")
        first_request_time = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ First templates request successful ({first_request_time:.2f}s)")
            print(f"Cached: {data.get('cached', False)}")
            
            # Second request (should be cached)
            start_time = time.time()
            response2 = requests.get(f"{base_url}/api/mcp/habu_enhanced_templates?cleanroom_id=test_123")
            second_request_time = time.time() - start_time
            
            if response2.status_code == 200:
                data2 = response2.json()
                print(f"✅ Second templates request successful ({second_request_time:.2f}s)")
                print(f"Cached: {data2.get('cached', False)}")
                
                if second_request_time < first_request_time:
                    print(f"🚀 Cache optimization: {((first_request_time - second_request_time) / first_request_time * 100):.1f}% faster")
            else:
                print(f"❌ Second templates request failed: {response2.status_code}")
        else:
            print(f"❌ Templates request failed: {response.status_code}")
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"❌ Templates request error: {e}")
    
    print("\n🏁 Flask API Redis integration test complete!")
    print("\nℹ️ Note: If Redis is not running locally, the API will use fallback behavior")
    print("   This is expected and the API should still function correctly.")

if __name__ == "__main__":
    test_flask_redis_integration()