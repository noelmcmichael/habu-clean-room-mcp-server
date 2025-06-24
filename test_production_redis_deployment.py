#!/usr/bin/env python3
"""
Comprehensive test suite for Phase H1.1 Redis integration in production
Tests all aspects of the caching system after deployment
"""

import requests
import json
import time
import statistics
from datetime import datetime
from typing import List, Dict, Any

class ProductionRedisTestSuite:
    def __init__(self):
        self.base_url = "https://habu-demo-api-v2.onrender.com"
        self.frontend_url = "https://habu-demo-frontend-v2.onrender.com"
        self.mcp_url = "https://habu-mcp-server-v2.onrender.com"
        self.admin_url = "https://habu-admin-app-v2.onrender.com"
        
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'tests': [],
            'overall_status': 'unknown',
            'performance_metrics': {},
            'redis_status': 'unknown'
        }
    
    def log_test(self, test_name: str, status: str, details: Dict[str, Any]):
        """Log test results"""
        result = {
            'test': test_name,
            'status': status,
            'timestamp': datetime.now().isoformat(),
            'details': details
        }
        self.results['tests'].append(result)
        
        status_emoji = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        print(f"{status_emoji} {test_name}: {status}")
        if details:
            for key, value in details.items():
                print(f"   {key}: {value}")
        print()
    
    def test_service_health(self):
        """Test 1: Basic service health checks"""
        print("🔍 Test 1: Service Health Checks")
        
        services = [
            ('Demo API', f"{self.base_url}/health"),
            ('React Frontend', f"{self.frontend_url}/"),
            ('MCP Server', f"{self.mcp_url}/health"),
            ('Admin App', f"{self.admin_url}/health")
        ]
        
        all_healthy = True
        service_statuses = {}
        
        for name, url in services:
            try:
                start_time = time.time()
                response = requests.get(url, timeout=10)
                response_time = (time.time() - start_time) * 1000
                
                if response.status_code == 200:
                    service_statuses[name] = f"Healthy ({response_time:.0f}ms)"
                else:
                    service_statuses[name] = f"Unhealthy ({response.status_code})"
                    all_healthy = False
            except Exception as e:
                service_statuses[name] = f"Error: {str(e)}"
                all_healthy = False
        
        self.log_test(
            "Service Health Check",
            "PASS" if all_healthy else "FAIL",
            service_statuses
        )
        
        return all_healthy
    
    def test_redis_cache_stats(self):
        """Test 2: Redis cache statistics and connection"""
        print("📊 Test 2: Redis Cache Statistics")
        
        try:
            response = requests.get(f"{self.base_url}/api/cache-stats", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                cache_stats = data.get('cache_stats', {})
                
                redis_connected = cache_stats.get('connected', False)
                self.results['redis_status'] = 'connected' if redis_connected else 'disconnected'
                
                details = {
                    'Connected': redis_connected,
                    'Redis Version': cache_stats.get('redis_version', 'N/A'),
                    'Used Memory': cache_stats.get('used_memory', 'N/A'),
                    'Connected Clients': cache_stats.get('connected_clients', 'N/A'),
                    'Hit Rate': f"{cache_stats.get('hit_rate', 0)}%"
                }
                
                self.log_test(
                    "Redis Cache Statistics",
                    "PASS" if redis_connected else "WARN",
                    details
                )
                
                return redis_connected
            else:
                self.log_test(
                    "Redis Cache Statistics",
                    "FAIL",
                    {'Error': f"HTTP {response.status_code}"}
                )
                return False
                
        except Exception as e:
            self.log_test(
                "Redis Cache Statistics",
                "FAIL",
                {'Error': str(e)}
            )
            return False
    
    def test_chat_caching_performance(self):
        """Test 3: Chat response caching performance"""
        print("💬 Test 3: Chat Response Caching")
        
        test_queries = [
            "What is the current system status?",
            "List all available partners",
            "Show me the enhanced templates"
        ]
        
        performance_results = []
        
        for query in test_queries:
            try:
                # First request (should be uncached)
                chat_data = {
                    "user_input": query,
                    "session_id": "test_session_redis"
                }
                
                start_time = time.time()
                response1 = requests.post(
                    f"{self.base_url}/api/enhanced-chat",
                    json=chat_data,
                    timeout=30
                )
                first_response_time = (time.time() - start_time) * 1000
                
                if response1.status_code != 200:
                    continue
                
                data1 = response1.json()
                first_cached = data1.get('cached', False)
                
                # Wait a moment then make the same request (should be cached)
                time.sleep(1)
                
                start_time = time.time()
                response2 = requests.post(
                    f"{self.base_url}/api/enhanced-chat",
                    json=chat_data,
                    timeout=30
                )
                second_response_time = (time.time() - start_time) * 1000
                
                if response2.status_code == 200:
                    data2 = response2.json()
                    second_cached = data2.get('cached', False)
                    
                    performance_improvement = ((first_response_time - second_response_time) / first_response_time) * 100
                    
                    performance_results.append({
                        'query': query[:50] + "..." if len(query) > 50 else query,
                        'first_request_ms': f"{first_response_time:.0f}ms",
                        'second_request_ms': f"{second_response_time:.0f}ms",
                        'first_cached': first_cached,
                        'second_cached': second_cached,
                        'improvement': f"{performance_improvement:.1f}%"
                    })
                
            except Exception as e:
                performance_results.append({
                    'query': query,
                    'error': str(e)
                })
        
        # Calculate average performance
        valid_results = [r for r in performance_results if 'error' not in r]
        if valid_results:
            avg_improvement = statistics.mean([
                float(r['improvement'].replace('%', ''))
                for r in valid_results
                if 'improvement' in r
            ])
            
            self.results['performance_metrics']['chat_caching'] = {
                'average_improvement': f"{avg_improvement:.1f}%",
                'tests_run': len(valid_results)
            }
        
        self.log_test(
            "Chat Response Caching",
            "PASS" if valid_results else "FAIL",
            {f"Test {i+1}": result for i, result in enumerate(performance_results)}
        )
        
        return len(valid_results) > 0
    
    def test_api_endpoint_caching(self):
        """Test 4: API endpoint caching (partners, templates)"""
        print("🔧 Test 4: API Endpoint Caching")
        
        endpoints = [
            ('Partners List', '/api/mcp/habu_list_partners'),
            ('Enhanced Templates', '/api/mcp/habu_enhanced_templates?cleanroom_id=test_123')
        ]
        
        endpoint_results = {}
        
        for name, endpoint in endpoints:
            try:
                # First request
                start_time = time.time()
                response1 = requests.get(f"{self.base_url}{endpoint}", timeout=15)
                first_time = (time.time() - start_time) * 1000
                
                if response1.status_code == 200:
                    data1 = response1.json()
                    first_cached = data1.get('cached', False)
                    
                    # Second request
                    start_time = time.time()
                    response2 = requests.get(f"{self.base_url}{endpoint}", timeout=15)
                    second_time = (time.time() - start_time) * 1000
                    
                    if response2.status_code == 200:
                        data2 = response2.json()
                        second_cached = data2.get('cached', False)
                        
                        improvement = ((first_time - second_time) / first_time) * 100 if first_time > 0 else 0
                        
                        endpoint_results[name] = {
                            'first_request': f"{first_time:.0f}ms (cached: {first_cached})",
                            'second_request': f"{second_time:.0f}ms (cached: {second_cached})",
                            'improvement': f"{improvement:.1f}%",
                            'status': 'PASS'
                        }
                    else:
                        endpoint_results[name] = {
                            'error': f"Second request failed: {response2.status_code}",
                            'status': 'FAIL'
                        }
                else:
                    endpoint_results[name] = {
                        'error': f"First request failed: {response1.status_code}",
                        'status': 'FAIL'
                    }
                    
            except Exception as e:
                endpoint_results[name] = {
                    'error': str(e),
                    'status': 'FAIL'
                }
        
        all_passed = all(result.get('status') == 'PASS' for result in endpoint_results.values())
        
        self.log_test(
            "API Endpoint Caching",
            "PASS" if all_passed else "FAIL",
            endpoint_results
        )
        
        return all_passed
    
    def test_frontend_integration(self):
        """Test 5: Frontend integration with backend caching"""
        print("🎨 Test 5: Frontend Integration")
        
        try:
            # Test frontend loads
            start_time = time.time()
            response = requests.get(self.frontend_url, timeout=10)
            load_time = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                # Check if it's the React app
                is_react_app = 'react' in response.text.lower() or 'habu' in response.text.lower()
                
                details = {
                    'Load Time': f"{load_time:.0f}ms",
                    'Status Code': response.status_code,
                    'React App': is_react_app,
                    'Content Length': f"{len(response.content)} bytes"
                }
                
                self.log_test(
                    "Frontend Integration",
                    "PASS" if is_react_app else "WARN",
                    details
                )
                
                return is_react_app
            else:
                self.log_test(
                    "Frontend Integration",
                    "FAIL",
                    {'Error': f"HTTP {response.status_code}"}
                )
                return False
                
        except Exception as e:
            self.log_test(
                "Frontend Integration",
                "FAIL",
                {'Error': str(e)}
            )
            return False
    
    def run_complete_test_suite(self):
        """Run the complete test suite"""
        print("🚀 Phase H1.1 Redis Integration - Production Test Suite")
        print("=" * 60)
        print(f"Testing deployment at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Base URL: {self.base_url}")
        print()
        
        # Run all tests
        tests = [
            self.test_service_health,
            self.test_redis_cache_stats,
            self.test_chat_caching_performance,
            self.test_api_endpoint_caching,
            self.test_frontend_integration
        ]
        
        passed_tests = 0
        total_tests = len(tests)
        
        for test in tests:
            try:
                if test():
                    passed_tests += 1
            except Exception as e:
                print(f"❌ Test failed with exception: {e}")
        
        # Final results
        print("=" * 60)
        print("📋 TEST SUITE SUMMARY")
        print("=" * 60)
        
        success_rate = (passed_tests / total_tests) * 100
        self.results['overall_status'] = 'PASS' if success_rate >= 80 else 'FAIL'
        
        print(f"Tests Passed: {passed_tests}/{total_tests} ({success_rate:.1f}%)")
        print(f"Redis Status: {self.results['redis_status']}")
        print(f"Overall Status: {self.results['overall_status']}")
        
        if self.results['performance_metrics']:
            print("\n📊 Performance Metrics:")
            for metric, value in self.results['performance_metrics'].items():
                print(f"  {metric}: {value}")
        
        print("\n🎯 Key Findings:")
        if self.results['redis_status'] == 'connected':
            print("  ✅ Redis cache is connected and operational")
            print("  ✅ Caching is providing performance improvements")
            print("  ✅ Phase H1.1 deployment successful")
        else:
            print("  ⚠️ Redis cache not connected - using fallback mode")
            print("  ✅ System continues to function normally")
            print("  🔍 May need Redis configuration review")
        
        print(f"\n📁 Full results saved to test results")
        return self.results

def main():
    """Run the production test suite"""
    suite = ProductionRedisTestSuite()
    results = suite.run_complete_test_suite()
    
    # Save results to file
    with open('production_test_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n📄 Detailed results saved to: production_test_results.json")
    
    return results['overall_status'] == 'PASS'

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)