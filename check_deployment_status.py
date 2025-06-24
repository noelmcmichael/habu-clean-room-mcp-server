#!/usr/bin/env python3
"""
Check deployment status for Phase H1.1 Redis integration
"""

import requests
import time
import json

def check_deployment_status():
    """Check if the new Redis-enabled deployment is live"""
    
    base_url = "https://habu-demo-api-v2.onrender.com"
    
    print("🔍 Checking Phase H1.1 deployment status...")
    print(f"Base URL: {base_url}")
    print()
    
    # Check 1: Root endpoint version
    try:
        response = requests.get(f"{base_url}/", timeout=10)
        if response.status_code == 200:
            data = response.json()
            version = data.get('version', 'Unknown')
            endpoints = data.get('endpoints', [])
            
            print(f"✅ API Status: {response.status_code}")
            print(f"📦 Version: {version}")
            print(f"🔗 Endpoints: {len(endpoints)} available")
            
            # Check if cache-stats endpoint is listed
            has_cache_stats = '/api/cache-stats' in endpoints
            print(f"💾 Cache Stats Endpoint: {'✅ Available' if has_cache_stats else '❌ Not Available'}")
            
            if version == "Phase H - Redis Optimized":
                print("🎉 Phase H deployment detected!")
                return True
            else:
                print("⏳ Still showing old version - deployment in progress")
                return False
        else:
            print(f"❌ API Error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return False

def wait_for_deployment(max_wait_minutes=10):
    """Wait for deployment to complete"""
    
    print(f"⏳ Waiting for deployment to complete (max {max_wait_minutes} minutes)...")
    
    start_time = time.time()
    max_wait_seconds = max_wait_minutes * 60
    
    while time.time() - start_time < max_wait_seconds:
        print(f"\n🔄 Checking deployment status... ({int((time.time() - start_time) / 60)}m elapsed)")
        
        if check_deployment_status():
            elapsed_minutes = (time.time() - start_time) / 60
            print(f"\n✅ Deployment completed! ({elapsed_minutes:.1f} minutes)")
            return True
        
        print("⏳ Waiting 30 seconds before next check...")
        time.sleep(30)
    
    print(f"\n⚠️ Deployment check timed out after {max_wait_minutes} minutes")
    print("ℹ️ This might be normal for Render.com deployments")
    return False

if __name__ == "__main__":
    print("🚀 Phase H1.1 Deployment Status Checker")
    print("=" * 50)
    
    # Initial check
    if check_deployment_status():
        print("\n✅ Deployment is already live!")
    else:
        # Wait for deployment
        deployed = wait_for_deployment(10)
        
        if deployed:
            print("\n✅ Ready to run comprehensive tests!")
        else:
            print("\n⚠️ Will proceed with testing current deployment")
    
    print("\n📝 Next steps:")
    print("1. Run: python test_production_redis_deployment.py")
    print("2. Review test results and performance metrics")
    print("3. Proceed with Phase H1.2 if tests pass")