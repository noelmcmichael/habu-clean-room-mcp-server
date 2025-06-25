#!/usr/bin/env python3
"""
Enhanced Production Deployment Test Script
Tests both Customer Support Mode and Technical Expert Mode in production
"""
import requests
import json
import time
from typing import Dict, Any

# Production URLs - Update these after deployment to Render
PRODUCTION_URLS = {
    'mcp_server': 'https://habu-mcp-server-v2.onrender.com',
    'demo_api': 'https://habu-demo-api-v2.onrender.com',
    'admin_app': 'https://habu-admin-app-v2.onrender.com',
    'react_frontend': 'https://habu-demo-frontend-v2.onrender.com'
}

# Development URLs - For local testing
LOCAL_URLS = {
    'mcp_server': 'http://localhost:8000',
    'demo_api': 'http://localhost:5001',
    'admin_app': 'http://localhost:5000',
    'react_frontend': 'http://localhost:3000'
}

# Use production URLs by default, set USE_LOCAL=True for local testing
USE_LOCAL = False
BASE_URLS = LOCAL_URLS if USE_LOCAL else PRODUCTION_URLS

API_KEY = 'secure-habu-demo-key-2024'
HEADERS = {'X-API-Key': API_KEY, 'Content-Type': 'application/json'}

def test_service_health(service_name: str, url: str) -> Dict[str, Any]:
    """Test basic health endpoint for a service"""
    try:
        response = requests.get(f"{url}/health", timeout=10)
        return {
            'service': service_name,
            'status': 'healthy' if response.status_code == 200 else 'unhealthy',
            'status_code': response.status_code,
            'response_time': response.elapsed.total_seconds(),
            'data': response.json() if response.status_code == 200 else None
        }
    except Exception as e:
        return {
            'service': service_name,
            'status': 'error',
            'error': str(e)
        }

def test_customer_support_mode(base_url: str) -> Dict[str, Any]:
    """Test Customer Support Mode functionality"""
    test_queries = [
        {
            'name': 'Retail Lookalike Modeling',
            'query': 'Customer wants lookalike modeling for retail with 90% accuracy',
            'expected_keywords': ['lookalike', 'retail', 'accuracy', 'supported']
        },
        {
            'name': 'Financial Real-time Attribution',
            'query': 'Financial services client needs real-time attribution',
            'expected_keywords': ['real-time', 'attribution', 'financial', 'timeline']
        },
        {
            'name': 'Generic Feasibility Check',
            'query': 'What can LiveRamp do for audience targeting?',
            'expected_keywords': ['audience', 'targeting', 'capabilities']
        }
    ]
    
    results = []
    for test in test_queries:
        try:
            response = requests.post(
                f"{base_url}/api/customer-support/assess",
                headers=HEADERS,
                json={
                    'query': test['query'],
                    'industry': 'retail',
                    'customerSize': 'enterprise'
                },
                timeout=30
            )
            
            result = {
                'test': test['name'],
                'status': 'pass' if response.status_code == 200 else 'fail',
                'status_code': response.status_code,
                'response_time': response.elapsed.total_seconds()
            }
            
            if response.status_code == 200:
                data = response.json()
                result['response_length'] = len(data.get('summary', ''))
                result['has_keywords'] = any(
                    keyword.lower() in data.get('summary', '').lower() 
                    for keyword in test['expected_keywords']
                )
            
            results.append(result)
            
        except Exception as e:
            results.append({
                'test': test['name'],
                'status': 'error',
                'error': str(e)
            })
    
    return {'mode': 'Customer Support', 'tests': results}

def test_technical_expert_mode(base_url: str) -> Dict[str, Any]:
    """Test Technical Expert Mode functionality"""
    test_queries = [
        {
            'name': 'Python Identity Resolution',
            'query': 'Show me Python code for identity resolution with error handling',
            'expected_keywords': ['python', 'identity', 'resolution', 'error', 'handling']
        },
        {
            'name': 'API Troubleshooting',
            'query': 'I am getting 401 errors when calling the LiveRamp API',
            'expected_keywords': ['401', 'authentication', 'token', 'credentials']
        },
        {
            'name': 'Performance Optimization',
            'query': 'How to optimize API calls for large datasets?',
            'expected_keywords': ['optimization', 'performance', 'large', 'datasets']
        }
    ]
    
    results = []
    for test in test_queries:
        try:
            response = requests.post(
                f"{base_url}/api/technical-expert/query",
                headers=HEADERS,
                json={
                    'query': test['query'],
                    'programming_language': 'python',
                    'use_case': 'api_integration'
                },
                timeout=30
            )
            
            result = {
                'test': test['name'],
                'status': 'pass' if response.status_code == 200 else 'fail',
                'status_code': response.status_code,
                'response_time': response.elapsed.total_seconds()
            }
            
            if response.status_code == 200:
                data = response.json()
                result['response_length'] = len(data.get('summary', ''))
                result['has_keywords'] = any(
                    keyword.lower() in data.get('summary', '').lower() 
                    for keyword in test['expected_keywords']
                )
                result['has_code'] = 'python' in data.get('summary', '').lower()
            
            results.append(result)
            
        except Exception as e:
            results.append({
                'test': test['name'],
                'status': 'error',
                'error': str(e)
            })
    
    return {'mode': 'Technical Expert', 'tests': results}

def test_mcp_integration(base_url: str) -> Dict[str, Any]:
    """Test MCP server integration"""
    try:
        # Test MCP health
        response = requests.get(f"{base_url}/health", headers=HEADERS, timeout=10)
        
        return {
            'component': 'MCP Server',
            'status': 'healthy' if response.status_code == 200 else 'unhealthy',
            'status_code': response.status_code,
            'response_time': response.elapsed.total_seconds()
        }
    except Exception as e:
        return {
            'component': 'MCP Server',
            'status': 'error',
            'error': str(e)
        }

def test_react_frontend(base_url: str) -> Dict[str, Any]:
    """Test React frontend accessibility"""
    try:
        response = requests.get(base_url, timeout=10)
        
        return {
            'component': 'React Frontend',
            'status': 'accessible' if response.status_code == 200 else 'inaccessible',
            'status_code': response.status_code,
            'response_time': response.elapsed.total_seconds(),
            'has_react_content': 'react' in response.text.lower() or 'root' in response.text
        }
    except Exception as e:
        return {
            'component': 'React Frontend',
            'status': 'error',
            'error': str(e)
        }

def run_comprehensive_test():
    """Run comprehensive production deployment test"""
    print("🚀 Starting LiveRamp AI Assistant Production Deployment Test")
    print("=" * 70)
    
    # Test all service health
    print("\n📊 HEALTH CHECK RESULTS")
    print("-" * 30)
    
    health_results = []
    for service, url in BASE_URLS.items():
        result = test_service_health(service, url)
        health_results.append(result)
        status_emoji = "✅" if result['status'] == 'healthy' else "❌"
        print(f"{status_emoji} {service}: {result['status']}")
    
    # Test Customer Support Mode
    print("\n🤝 CUSTOMER SUPPORT MODE TEST")
    print("-" * 30)
    
    cs_results = test_customer_support_mode(BASE_URLS['demo_api'])
    for test in cs_results['tests']:
        status_emoji = "✅" if test['status'] == 'pass' else "❌"
        print(f"{status_emoji} {test['test']}: {test['status']}")
    
    # Test Technical Expert Mode
    print("\n🔧 TECHNICAL EXPERT MODE TEST")
    print("-" * 30)
    
    te_results = test_technical_expert_mode(BASE_URLS['demo_api'])
    for test in te_results['tests']:
        status_emoji = "✅" if test['status'] == 'pass' else "❌"
        print(f"{status_emoji} {test['test']}: {test['status']}")
    
    # Test MCP Integration
    print("\n⚙️ MCP SERVER INTEGRATION TEST")
    print("-" * 30)
    
    mcp_result = test_mcp_integration(BASE_URLS['mcp_server'])
    status_emoji = "✅" if mcp_result['status'] == 'healthy' else "❌"
    print(f"{status_emoji} MCP Server: {mcp_result['status']}")
    
    # Test React Frontend
    print("\n⚛️ REACT FRONTEND TEST")
    print("-" * 30)
    
    react_result = test_react_frontend(BASE_URLS['react_frontend'])
    status_emoji = "✅" if react_result['status'] == 'accessible' else "❌"
    print(f"{status_emoji} React Frontend: {react_result['status']}")
    
    # Summary
    print("\n📋 DEPLOYMENT SUMMARY")
    print("=" * 30)
    
    total_tests = (
        len(health_results) + 
        len(cs_results['tests']) + 
        len(te_results['tests']) + 
        2  # MCP + React
    )
    
    passed_tests = (
        sum(1 for r in health_results if r['status'] == 'healthy') +
        sum(1 for t in cs_results['tests'] if t['status'] == 'pass') +
        sum(1 for t in te_results['tests'] if t['status'] == 'pass') +
        (1 if mcp_result['status'] == 'healthy' else 0) +
        (1 if react_result['status'] == 'accessible' else 0)
    )
    
    success_rate = (passed_tests / total_tests) * 100
    
    print(f"✅ Passed: {passed_tests}/{total_tests} tests ({success_rate:.1f}%)")
    
    if success_rate >= 80:
        print("\n🎉 DEPLOYMENT SUCCESSFUL!")
        print("Your LiveRamp AI Assistant is ready for production use.")
        print("\nNext steps:")
        print("1. Share React frontend URL with LiveRamp teams")
        print("2. Configure VS Code MCP integration")
        print("3. Monitor usage and performance metrics")
    else:
        print("\n⚠️ DEPLOYMENT ISSUES DETECTED")
        print("Please review failed tests and resolve issues before going live.")
    
    # Save results to file
    results = {
        'timestamp': time.time(),
        'health_check': health_results,
        'customer_support_mode': cs_results,
        'technical_expert_mode': te_results,
        'mcp_integration': mcp_result,
        'react_frontend': react_result,
        'summary': {
            'total_tests': total_tests,
            'passed_tests': passed_tests,
            'success_rate': success_rate
        }
    }
    
    with open('production_deployment_test_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n📄 Detailed results saved to: production_deployment_test_results.json")

if __name__ == "__main__":
    run_comprehensive_test()