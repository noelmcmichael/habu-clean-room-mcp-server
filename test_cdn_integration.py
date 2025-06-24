#!/usr/bin/env python3
"""
Test script for CDN integration and optimization
Verifies Phase H1.2 implementation
"""

import time
import json
import requests
import asyncio
from typing import Dict, List, Any

# Test configuration
BASE_URL = "http://localhost:5000"
TEST_ENDPOINTS = [
    "/",
    "/health", 
    "/api/cdn-stats",
    "/api/cache-stats",
    "/api/mcp/habu_list_partners",
    "/api/mcp/habu_enhanced_templates",
    "/api/mcp/habu_list_templates"
]

class CDNIntegrationTester:
    """Test CDN integration and performance optimization"""
    
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self.results = []
        
    def test_cdn_headers(self, endpoint: str) -> Dict[str, Any]:
        """Test CDN optimization headers"""
        try:
            response = self.session.get(f"{self.base_url}{endpoint}")
            
            # Check for CDN optimization headers
            cdn_headers = {
                'cache_control': response.headers.get('Cache-Control'),
                'etag': response.headers.get('ETag'),
                'expires': response.headers.get('Expires'),
                'vary': response.headers.get('Vary'),
                'compression': response.headers.get('Content-Encoding'),
                'compression_ratio': response.headers.get('X-Compression-Ratio'),
                'cdn_optimized': response.headers.get('X-CDN-Optimized'),
                'content_length': response.headers.get('Content-Length'),
                'content_type': response.headers.get('Content-Type')
            }
            
            return {
                'endpoint': endpoint,
                'status_code': response.status_code,
                'response_time': response.elapsed.total_seconds() * 1000,
                'headers': cdn_headers,
                'content_size': len(response.content),
                'success': response.status_code == 200
            }
            
        except Exception as e:
            return {
                'endpoint': endpoint,
                'error': str(e),
                'success': False
            }
    
    def test_compression(self, endpoint: str) -> Dict[str, Any]:
        """Test compression functionality"""
        try:
            # Test without compression
            headers_no_compression = {'Accept-Encoding': 'identity'}
            response_no_compression = self.session.get(
                f"{self.base_url}{endpoint}", 
                headers=headers_no_compression
            )
            
            # Test with compression
            headers_with_compression = {'Accept-Encoding': 'gzip, deflate'}
            response_with_compression = self.session.get(
                f"{self.base_url}{endpoint}", 
                headers=headers_with_compression
            )
            
            size_without = len(response_no_compression.content)
            size_with = len(response_with_compression.content)
            
            compression_ratio = 0
            if size_without > 0:
                compression_ratio = ((size_without - size_with) / size_without) * 100
            
            return {
                'endpoint': endpoint,
                'size_without_compression': size_without,
                'size_with_compression': size_with,
                'compression_ratio': round(compression_ratio, 2),
                'compression_enabled': 'gzip' in response_with_compression.headers.get('Content-Encoding', ''),
                'success': True
            }
            
        except Exception as e:
            return {
                'endpoint': endpoint,
                'error': str(e),
                'success': False
            }
    
    def test_etag_caching(self, endpoint: str) -> Dict[str, Any]:
        """Test ETag caching functionality"""
        try:
            # First request
            response1 = self.session.get(f"{self.base_url}{endpoint}")
            etag = response1.headers.get('ETag')
            
            if not etag:
                return {
                    'endpoint': endpoint,
                    'etag_present': False,
                    'success': False
                }
            
            # Second request with ETag
            headers = {'If-None-Match': etag}
            response2 = self.session.get(f"{self.base_url}{endpoint}", headers=headers)
            
            return {
                'endpoint': endpoint,
                'etag_present': True,
                'etag_value': etag,
                'first_response_code': response1.status_code,
                'second_response_code': response2.status_code,
                'cache_hit': response2.status_code == 304,
                'success': True
            }
            
        except Exception as e:
            return {
                'endpoint': endpoint,
                'error': str(e),
                'success': False
            }
    
    def test_cdn_stats_endpoint(self) -> Dict[str, Any]:
        """Test the CDN statistics endpoint"""
        try:
            response = self.session.get(f"{self.base_url}/api/cdn-stats")
            
            if response.status_code != 200:
                return {
                    'success': False,
                    'error': f"Status code: {response.status_code}"
                }
            
            data = response.json()
            cdn_stats = data.get('cdn_stats', {})
            
            expected_fields = [
                'total_requests', 'cache_hit_ratio', 'compression_ratio',
                'average_response_time', 'performance_score', 'last_updated'
            ]
            
            missing_fields = [field for field in expected_fields if field not in cdn_stats]
            
            return {
                'success': len(missing_fields) == 0,
                'cdn_stats': cdn_stats,
                'missing_fields': missing_fields,
                'performance_score': cdn_stats.get('performance_score', 0)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def run_performance_test(self, endpoint: str, iterations: int = 5) -> Dict[str, Any]:
        """Run performance test with multiple iterations"""
        response_times = []
        
        for i in range(iterations):
            try:
                start_time = time.time()
                response = self.session.get(f"{self.base_url}{endpoint}")
                end_time = time.time()
                
                if response.status_code == 200:
                    response_times.append((end_time - start_time) * 1000)
                    
            except Exception as e:
                print(f"Error in iteration {i+1}: {e}")
        
        if not response_times:
            return {'success': False, 'error': 'No successful requests'}
        
        avg_time = sum(response_times) / len(response_times)
        min_time = min(response_times)
        max_time = max(response_times)
        
        return {
            'endpoint': endpoint,
            'iterations': iterations,
            'successful_requests': len(response_times),
            'average_response_time': round(avg_time, 2),
            'min_response_time': round(min_time, 2),
            'max_response_time': round(max_time, 2),
            'success': True
        }
    
    def run_comprehensive_test(self) -> Dict[str, Any]:
        """Run comprehensive CDN integration test"""
        print("🚀 Starting CDN Integration Test Suite")
        print("=" * 50)
        
        # Test CDN stats endpoint
        print("\n1. Testing CDN Stats Endpoint...")
        stats_test = self.test_cdn_stats_endpoint()
        if stats_test['success']:
            print(f"   ✅ CDN Stats endpoint working")
            print(f"   📊 Performance Score: {stats_test.get('performance_score', 0)}")
        else:
            print(f"   ❌ CDN Stats endpoint failed: {stats_test.get('error')}")
        
        # Test each endpoint
        endpoint_results = []
        for endpoint in TEST_ENDPOINTS:
            print(f"\n2. Testing endpoint: {endpoint}")
            
            # Test CDN headers
            header_test = self.test_cdn_headers(endpoint)
            if header_test['success']:
                print(f"   ✅ Headers: {header_test['response_time']:.2f}ms")
                if header_test['headers']['cdn_optimized']:
                    print(f"   🚀 CDN Optimized: True")
                if header_test['headers']['compression']:
                    print(f"   📦 Compressed: {header_test['headers']['compression']}")
            else:
                print(f"   ❌ Headers test failed: {header_test.get('error')}")
            
            # Test compression
            compression_test = self.test_compression(endpoint)
            if compression_test['success']:
                print(f"   📦 Compression: {compression_test['compression_ratio']:.1f}% reduction")
            
            # Test ETag caching
            etag_test = self.test_etag_caching(endpoint)
            if etag_test['success'] and etag_test['cache_hit']:
                print(f"   ⚡ ETag caching: Working (304 response)")
            
            # Performance test
            perf_test = self.run_performance_test(endpoint, 3)
            if perf_test['success']:
                print(f"   ⚡ Performance: {perf_test['average_response_time']:.2f}ms avg")
            
            endpoint_results.append({
                'endpoint': endpoint,
                'headers': header_test,
                'compression': compression_test,
                'etag': etag_test,
                'performance': perf_test
            })
        
        # Calculate overall results
        successful_endpoints = sum(1 for r in endpoint_results if r['headers']['success'])
        compression_working = sum(1 for r in endpoint_results if r['compression']['success'] and r['compression']['compression_ratio'] > 0)
        
        overall_result = {
            'test_timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'total_endpoints_tested': len(TEST_ENDPOINTS),
            'successful_endpoints': successful_endpoints,
            'compression_working_endpoints': compression_working,
            'cdn_stats_working': stats_test['success'],
            'endpoint_results': endpoint_results,
            'stats_result': stats_test,
            'success_rate': round((successful_endpoints / len(TEST_ENDPOINTS)) * 100, 2)
        }
        
        print("\n" + "=" * 50)
        print("📊 CDN Integration Test Results")
        print("=" * 50)
        print(f"✅ Successful endpoints: {successful_endpoints}/{len(TEST_ENDPOINTS)} ({overall_result['success_rate']}%)")
        print(f"📦 Compression working: {compression_working}/{len(TEST_ENDPOINTS)} endpoints")
        print(f"📊 CDN Stats endpoint: {'✅ Working' if stats_test['success'] else '❌ Failed'}")
        
        if stats_test['success']:
            print(f"🎯 Performance Score: {stats_test.get('performance_score', 0)}/100")
        
        return overall_result

def main():
    """Main test function"""
    tester = CDNIntegrationTester()
    
    try:
        # Test server availability
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code != 200:
            print(f"❌ Server not available at {BASE_URL}")
            return
            
        print(f"✅ Server available at {BASE_URL}")
        
        # Run comprehensive test
        results = tester.run_comprehensive_test()
        
        # Save results to file
        with open('cdn_integration_test_results.json', 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n📁 Detailed results saved to: cdn_integration_test_results.json")
        
    except requests.exceptions.ConnectionError:
        print(f"❌ Cannot connect to server at {BASE_URL}")
        print("   Make sure the Flask server is running with: python demo_api.py")
    except Exception as e:
        print(f"❌ Test failed with error: {e}")

if __name__ == "__main__":
    main()