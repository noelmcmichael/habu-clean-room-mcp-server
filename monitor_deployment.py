#!/usr/bin/env python3
"""
Production Deployment Monitoring Script
Monitors the Render.com deployment in real-time and validates all services
"""
import requests
import time
import json
from datetime import datetime
from typing import Dict, List, Any

# Update these URLs after Render deployment
PRODUCTION_URLS = {
    'mcp_server': 'https://habu-mcp-server-v2.onrender.com',
    'demo_api': 'https://habu-demo-api-v2.onrender.com',
    'admin_app': 'https://habu-admin-app-v2.onrender.com',
    'react_frontend': 'https://habu-demo-frontend-v2.onrender.com'
}

API_KEY = 'secure-habu-demo-key-2024'
HEADERS = {'X-API-Key': API_KEY, 'Content-Type': 'application/json'}

def check_service_health(service_name: str, url: str, timeout: int = 10) -> Dict[str, Any]:
    """Check health endpoint for a specific service"""
    try:
        health_url = f"{url}/health"
        start_time = time.time()
        response = requests.get(health_url, timeout=timeout)
        response_time = time.time() - start_time
        
        return {
            'service': service_name,
            'url': health_url,
            'status': 'healthy' if response.status_code == 200 else 'unhealthy',
            'status_code': response.status_code,
            'response_time': round(response_time, 3),
            'timestamp': datetime.now().isoformat(),
            'data': response.json() if response.status_code == 200 else None,
            'error': None
        }
    except requests.exceptions.Timeout:
        return {
            'service': service_name,
            'url': health_url,
            'status': 'timeout',
            'error': f'Request timed out after {timeout}s',
            'timestamp': datetime.now().isoformat()
        }
    except requests.exceptions.ConnectionError:
        return {
            'service': service_name,
            'url': health_url,
            'status': 'connection_error',
            'error': 'Failed to connect to service',
            'timestamp': datetime.now().isoformat()
        }
    except Exception as e:
        return {
            'service': service_name,
            'url': health_url,
            'status': 'error',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }

def test_enhanced_features(base_url: str) -> Dict[str, Any]:
    """Test enhanced UX features in production"""
    tests = []
    
    # Test Customer Support Mode
    try:
        response = requests.post(
            f"{base_url}/api/customer-support/assess",
            headers=HEADERS,
            json={
                'query': 'Customer wants lookalike modeling for retail audience',
                'industry': 'retail',
                'customerSize': 'enterprise'
            },
            timeout=30
        )
        
        tests.append({
            'test': 'Customer Support Mode',
            'status': 'pass' if response.status_code == 200 else 'fail',
            'status_code': response.status_code,
            'response_length': len(response.text) if response.status_code == 200 else 0,
            'has_enhanced_features': 'summary' in response.text if response.status_code == 200 else False
        })
    except Exception as e:
        tests.append({
            'test': 'Customer Support Mode',
            'status': 'error',
            'error': str(e)
        })
    
    # Test Technical Expert Mode  
    try:
        response = requests.post(
            f"{base_url}/api/technical-expert/query",
            headers=HEADERS,
            json={
                'query': 'Show me Python identity resolution with error handling',
                'context': {
                    'programmingLanguage': 'python',
                    'useCase': 'api_integration'
                }
            },
            timeout=30
        )
        
        tests.append({
            'test': 'Technical Expert Mode',
            'status': 'pass' if response.status_code == 200 else 'fail',
            'status_code': response.status_code,
            'response_length': len(response.text) if response.status_code == 200 else 0,
            'has_code_examples': 'python' in response.text.lower() if response.status_code == 200 else False
        })
    except Exception as e:
        tests.append({
            'test': 'Technical Expert Mode',
            'status': 'error',
            'error': str(e)
        })
    
    return {'enhanced_features': tests}

def test_react_frontend(url: str) -> Dict[str, Any]:
    """Test React frontend with enhanced UX components"""
    try:
        response = requests.get(url, timeout=15)
        
        # Check for enhanced UX indicators
        content = response.text.lower()
        enhanced_indicators = {
            'has_react_app': 'react' in content or 'root' in content,
            'has_enhanced_css': 'enhanced-chat' in content or 'quick-action' in content,
            'has_mode_switching': 'customer-support' in content or 'technical-expert' in content,
            'has_modern_js': 'static/js' in content,
            'has_optimized_css': 'static/css' in content
        }
        
        return {
            'service': 'React Frontend',
            'status': 'accessible' if response.status_code == 200 else 'inaccessible',
            'status_code': response.status_code,
            'enhanced_features': enhanced_indicators,
            'has_enhanced_ux': sum(enhanced_indicators.values()) >= 3,
            'content_size': len(response.text)
        }
    except Exception as e:
        return {
            'service': 'React Frontend',
            'status': 'error',
            'error': str(e)
        }

def continuous_monitoring(duration_minutes: int = 30, check_interval: int = 60):
    """Continuously monitor deployment for specified duration"""
    print(f"🔍 Starting {duration_minutes}-minute deployment monitoring")
    print(f"📊 Checking every {check_interval} seconds")
    print("=" * 70)
    
    start_time = time.time()
    end_time = start_time + (duration_minutes * 60)
    
    all_results = []
    
    while time.time() < end_time:
        check_time = datetime.now().strftime("%H:%M:%S")
        print(f"\n⏰ [{check_time}] Health Check Round")
        print("-" * 40)
        
        # Check all service health
        round_results = {
            'timestamp': datetime.now().isoformat(),
            'health_checks': [],
            'enhanced_features': None,
            'react_frontend': None
        }
        
        for service, url in PRODUCTION_URLS.items():
            if service == 'react_frontend':
                continue  # Handle separately
                
            result = check_service_health(service, url)
            round_results['health_checks'].append(result)
            
            status_emoji = "✅" if result['status'] == 'healthy' else "❌"
            print(f"{status_emoji} {service}: {result['status']} ({result.get('response_time', 'N/A')}s)")
        
        # Test enhanced features
        if PRODUCTION_URLS['demo_api']:
            enhanced_result = test_enhanced_features(PRODUCTION_URLS['demo_api'])
            round_results['enhanced_features'] = enhanced_result
            
            for test in enhanced_result['enhanced_features']:
                status_emoji = "✅" if test['status'] == 'pass' else "❌"
                print(f"{status_emoji} {test['test']}: {test['status']}")
        
        # Test React frontend
        if PRODUCTION_URLS['react_frontend']:
            react_result = test_react_frontend(PRODUCTION_URLS['react_frontend'])
            round_results['react_frontend'] = react_result
            
            status_emoji = "✅" if react_result['status'] == 'accessible' else "❌"
            ux_emoji = "🎨" if react_result.get('has_enhanced_ux', False) else "⚠️"
            print(f"{status_emoji} {ux_emoji} React Frontend: {react_result['status']} (Enhanced UX: {react_result.get('has_enhanced_ux', False)})")
        
        all_results.append(round_results)
        
        # Sleep until next check
        if time.time() < end_time:
            time.sleep(check_interval)
    
    # Final summary
    print("\n" + "=" * 70)
    print("📋 DEPLOYMENT MONITORING SUMMARY")
    print("=" * 70)
    
    # Calculate success rates
    total_rounds = len(all_results)
    service_success_rates = {}
    
    for service in ['mcp_server', 'demo_api', 'admin_app']:
        successful_checks = sum(1 for result in all_results 
                              for health_check in result['health_checks']
                              if health_check['service'] == service and health_check['status'] == 'healthy')
        service_success_rates[service] = (successful_checks / total_rounds) * 100
    
    for service, success_rate in service_success_rates.items():
        status_emoji = "✅" if success_rate >= 90 else "⚠️" if success_rate >= 70 else "❌"
        print(f"{status_emoji} {service}: {success_rate:.1f}% uptime")
    
    # Enhanced features success rate
    enhanced_successful = sum(1 for result in all_results 
                            if result['enhanced_features'] and 
                            all(test['status'] == 'pass' for test in result['enhanced_features']['enhanced_features']))
    enhanced_success_rate = (enhanced_successful / total_rounds) * 100
    enhanced_emoji = "✅" if enhanced_success_rate >= 80 else "⚠️"
    print(f"{enhanced_emoji} Enhanced Features: {enhanced_success_rate:.1f}% success rate")
    
    # React frontend availability
    react_successful = sum(1 for result in all_results 
                         if result['react_frontend'] and result['react_frontend']['status'] == 'accessible')
    react_success_rate = (react_successful / total_rounds) * 100
    react_emoji = "✅" if react_success_rate >= 90 else "⚠️"
    print(f"{react_emoji} React Frontend: {react_success_rate:.1f}% availability")
    
    # Overall assessment
    overall_success = (
        sum(service_success_rates.values()) / len(service_success_rates) + 
        enhanced_success_rate + 
        react_success_rate
    ) / 3
    
    print(f"\n🎯 Overall Deployment Success: {overall_success:.1f}%")
    
    if overall_success >= 90:
        print("🎉 DEPLOYMENT EXCELLENT - Production ready!")
    elif overall_success >= 75:
        print("✅ DEPLOYMENT SUCCESSFUL - Minor issues to monitor")
    elif overall_success >= 50:
        print("⚠️ DEPLOYMENT PARTIAL - Requires attention")
    else:
        print("❌ DEPLOYMENT ISSUES - Consider rollback")
    
    # Save detailed results
    with open('deployment_monitoring_results.json', 'w') as f:
        json.dump({
            'monitoring_summary': {
                'duration_minutes': duration_minutes,
                'total_rounds': total_rounds,
                'service_success_rates': service_success_rates,
                'enhanced_success_rate': enhanced_success_rate,
                'react_success_rate': react_success_rate,
                'overall_success': overall_success
            },
            'detailed_results': all_results
        }, f, indent=2)
    
    print(f"\n📄 Detailed results saved to: deployment_monitoring_results.json")
    return overall_success

def quick_deployment_check():
    """Quick one-time deployment verification"""
    print("🚀 Quick Deployment Verification")
    print("=" * 40)
    
    results = {
        'health_checks': [],
        'enhanced_features': None,
        'react_frontend': None,
        'timestamp': datetime.now().isoformat()
    }
    
    # Health checks
    for service, url in PRODUCTION_URLS.items():
        if service == 'react_frontend':
            continue
            
        result = check_service_health(service, url)
        results['health_checks'].append(result)
        
        status_emoji = "✅" if result['status'] == 'healthy' else "❌"
        print(f"{status_emoji} {service}: {result['status']}")
    
    # Enhanced features test
    if PRODUCTION_URLS['demo_api']:
        enhanced_result = test_enhanced_features(PRODUCTION_URLS['demo_api'])
        results['enhanced_features'] = enhanced_result
        
        for test in enhanced_result['enhanced_features']:
            status_emoji = "✅" if test['status'] == 'pass' else "❌"
            print(f"{status_emoji} {test['test']}: {test['status']}")
    
    # React frontend test
    if PRODUCTION_URLS['react_frontend']:
        react_result = test_react_frontend(PRODUCTION_URLS['react_frontend'])
        results['react_frontend'] = react_result
        
        status_emoji = "✅" if react_result['status'] == 'accessible' else "❌"
        ux_status = "✅ Enhanced" if react_result.get('has_enhanced_ux', False) else "⚠️ Basic"
        print(f"{status_emoji} React Frontend: {react_result['status']} ({ux_status})")
    
    # Quick assessment
    healthy_services = sum(1 for hc in results['health_checks'] if hc['status'] == 'healthy')
    total_services = len(results['health_checks'])
    
    print(f"\n📊 Services Healthy: {healthy_services}/{total_services}")
    
    if healthy_services == total_services:
        print("🎉 All services operational - Deployment successful!")
    elif healthy_services >= total_services * 0.75:
        print("✅ Most services operational - Monitor any issues")
    else:
        print("❌ Multiple service issues - Check logs and consider rollback")
    
    return results

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "monitor":
        duration = int(sys.argv[2]) if len(sys.argv) > 2 else 30
        continuous_monitoring(duration)
    else:
        quick_deployment_check()