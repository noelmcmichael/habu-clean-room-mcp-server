"""
Phase H1.2: CloudFlare CDN Integration
Advanced content optimization and delivery acceleration
"""

import os
import time
import hashlib
import json
from typing import Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
from flask import Response, request, current_app
import gzip
import io

class CDNOptimizer:
    """Optimizes content delivery with CDN-ready headers and caching strategies"""
    
    def __init__(self):
        self.static_cache_duration = 31536000  # 1 year for static assets
        self.api_cache_duration = 300  # 5 minutes for API responses
        self.html_cache_duration = 3600  # 1 hour for HTML
        self.cdn_enabled = os.getenv('CDN_ENABLED', 'true').lower() == 'true'
        
    def generate_etag(self, content: str) -> str:
        """Generate ETag for content versioning"""
        return f'"{hashlib.md5(content.encode()).hexdigest()}"'
    
    def should_gzip(self, content_type: str, content_length: int) -> bool:
        """Determine if content should be gzipped"""
        if content_length < 1024:  # Don't gzip small content
            return False
            
        gzippable_types = {
            'text/html', 'text/css', 'text/javascript', 'application/javascript',
            'application/json', 'text/plain', 'text/xml', 'application/xml',
            'image/svg+xml'
        }
        
        return any(gzippable in content_type for gzippable in gzippable_types)
    
    def compress_content(self, content: str) -> Tuple[bytes, int]:
        """Compress content using gzip"""
        if isinstance(content, str):
            content = content.encode('utf-8')
            
        buffer = io.BytesIO()
        with gzip.GzipFile(fileobj=buffer, mode='wb', compresslevel=6) as gz_file:
            gz_file.write(content)
        
        compressed = buffer.getvalue()
        compression_ratio = (1 - len(compressed) / len(content)) * 100
        
        return compressed, compression_ratio
    
    def get_cache_headers(self, response_type: str, etag: Optional[str] = None) -> Dict[str, str]:
        """Generate appropriate cache headers for different content types"""
        headers = {}
        
        if response_type == 'static':
            # Static assets - long cache with immutable
            headers.update({
                'Cache-Control': f'public, max-age={self.static_cache_duration}, immutable',
                'Expires': (datetime.utcnow() + timedelta(seconds=self.static_cache_duration)).strftime('%a, %d %b %Y %H:%M:%S GMT'),
            })
        elif response_type == 'api':
            # API responses - shorter cache with revalidation
            headers.update({
                'Cache-Control': f'public, max-age={self.api_cache_duration}, must-revalidate',
                'Expires': (datetime.utcnow() + timedelta(seconds=self.api_cache_duration)).strftime('%a, %d %b %Y %H:%M:%S GMT'),
            })
        elif response_type == 'html':
            # HTML pages - medium cache with revalidation
            headers.update({
                'Cache-Control': f'public, max-age={self.html_cache_duration}, must-revalidate',
                'Expires': (datetime.utcnow() + timedelta(seconds=self.html_cache_duration)).strftime('%a, %d %b %Y %H:%M:%S GMT'),
            })
        elif response_type == 'no-cache':
            # Dynamic content - no cache
            headers.update({
                'Cache-Control': 'no-cache, no-store, must-revalidate',
                'Pragma': 'no-cache',
                'Expires': '0'
            })
        
        # Add ETag if provided
        if etag:
            headers['ETag'] = etag
        
        # Add security and performance headers
        headers.update({
            'X-Content-Type-Options': 'nosniff',
            'X-Frame-Options': 'DENY',
            'X-XSS-Protection': '1; mode=block',
            'Referrer-Policy': 'strict-origin-when-cross-origin',
            'Vary': 'Accept-Encoding',
        })
        
        return headers
    
    def optimize_response(self, response: Response, response_type: str = 'api') -> Response:
        """Optimize Flask response with CDN headers and compression"""
        if not self.cdn_enabled:
            return response
            
        try:
            # Get original content
            content = response.get_data(as_text=True)
            content_type = response.content_type or 'text/html'
            
            # Generate ETag
            etag = self.generate_etag(content)
            
            # Check if client has cached version
            client_etag = request.headers.get('If-None-Match')
            if client_etag == etag:
                return Response(status=304)
            
            # Apply compression if appropriate
            should_compress = self.should_gzip(content_type, len(content))
            if should_compress and 'gzip' in request.headers.get('Accept-Encoding', ''):
                compressed_content, compression_ratio = self.compress_content(content)
                response.data = compressed_content
                response.headers['Content-Encoding'] = 'gzip'
                response.headers['X-Compression-Ratio'] = f'{compression_ratio:.1f}%'
            
            # Add cache headers
            cache_headers = self.get_cache_headers(response_type, etag)
            for key, value in cache_headers.items():
                response.headers[key] = value
            
            # Add performance metrics
            response.headers['X-CDN-Optimized'] = 'true'
            response.headers['X-Optimization-Time'] = str(int(time.time() * 1000))
            
            return response
            
        except Exception as e:
            print(f"CDN optimization error: {e}")
            return response

class StaticAssetOptimizer:
    """Optimizes static assets for CDN delivery"""
    
    def __init__(self):
        self.asset_versions = {}
        self.build_time = int(time.time())
    
    def get_asset_url(self, asset_path: str, with_version: bool = True) -> str:
        """Generate versioned asset URLs for cache busting"""
        if not with_version:
            return asset_path
            
        # Use build time as version for simplicity
        separator = '&' if '?' in asset_path else '?'
        return f"{asset_path}{separator}v={self.build_time}"
    
    def optimize_css(self, css_content: str) -> str:
        """Basic CSS optimization"""
        # Remove comments and extra whitespace
        import re
        
        # Remove CSS comments
        css_content = re.sub(r'/\*.*?\*/', '', css_content, flags=re.DOTALL)
        
        # Remove extra whitespace
        css_content = re.sub(r'\s+', ' ', css_content)
        css_content = re.sub(r';\s*}', '}', css_content)
        css_content = re.sub(r'{\s*', '{', css_content)
        css_content = re.sub(r'}\s*', '}', css_content)
        
        return css_content.strip()
    
    def optimize_js(self, js_content: str) -> str:
        """Basic JavaScript optimization"""
        # Simple minification - remove comments and extra whitespace
        import re
        
        # Remove single-line comments (but preserve URLs)
        js_content = re.sub(r'//(?![^\r\n]*https?:)[^\r\n]*', '', js_content)
        
        # Remove multi-line comments
        js_content = re.sub(r'/\*.*?\*/', '', js_content, flags=re.DOTALL)
        
        # Remove extra whitespace
        js_content = re.sub(r'\s+', ' ', js_content)
        
        return js_content.strip()

class CDNAnalytics:
    """Analytics for CDN performance tracking"""
    
    def __init__(self):
        self.metrics = {
            'total_requests': 0,
            'cached_responses': 0,
            'compressed_responses': 0,
            'compression_savings': 0,
            'cache_hit_ratio': 0.0,
            'average_compression_ratio': 0.0,
            'response_times': []
        }
    
    def record_request(self, cached: bool = False, compressed: bool = False, 
                      compression_ratio: float = 0.0, response_time: float = 0.0):
        """Record request metrics"""
        self.metrics['total_requests'] += 1
        
        if cached:
            self.metrics['cached_responses'] += 1
            
        if compressed:
            self.metrics['compressed_responses'] += 1
            self.metrics['compression_savings'] += compression_ratio
            
        if response_time > 0:
            self.metrics['response_times'].append(response_time)
            if len(self.metrics['response_times']) > 1000:  # Keep last 1000
                self.metrics['response_times'] = self.metrics['response_times'][-1000:]
        
        # Update calculated metrics
        if self.metrics['total_requests'] > 0:
            self.metrics['cache_hit_ratio'] = (
                self.metrics['cached_responses'] / self.metrics['total_requests'] * 100
            )
            
        if self.metrics['compressed_responses'] > 0:
            self.metrics['average_compression_ratio'] = (
                self.metrics['compression_savings'] / self.metrics['compressed_responses']
            )
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary"""
        avg_response_time = 0.0
        if self.metrics['response_times']:
            avg_response_time = sum(self.metrics['response_times']) / len(self.metrics['response_times'])
        
        return {
            'total_requests': self.metrics['total_requests'],
            'cache_hit_ratio': round(self.metrics['cache_hit_ratio'], 2),
            'compression_ratio': round(self.metrics['average_compression_ratio'], 2),
            'average_response_time': round(avg_response_time, 2),
            'performance_score': self._calculate_performance_score(),
            'last_updated': datetime.utcnow().isoformat()
        }
    
    def _calculate_performance_score(self) -> float:
        """Calculate overall performance score (0-100)"""
        score = 0.0
        
        # Cache hit ratio component (40% of score)
        score += min(self.metrics['cache_hit_ratio'], 100) * 0.4
        
        # Compression ratio component (30% of score)  
        score += min(self.metrics['average_compression_ratio'], 100) * 0.3
        
        # Response time component (30% of score)
        if self.metrics['response_times']:
            avg_time = sum(self.metrics['response_times']) / len(self.metrics['response_times'])
            # Score inversely related to response time (100ms = 100 points, 1000ms = 0 points)
            time_score = max(0, 100 - (avg_time / 10))
            score += time_score * 0.3
        
        return round(score, 2)

# Global instances
cdn_optimizer = CDNOptimizer()
asset_optimizer = StaticAssetOptimizer()
cdn_analytics = CDNAnalytics()

def apply_cdn_optimization(response: Response, response_type: str = 'api') -> Response:
    """Decorator function to apply CDN optimization to Flask responses"""
    start_time = time.time()
    
    optimized_response = cdn_optimizer.optimize_response(response, response_type)
    
    # Record analytics
    response_time = (time.time() - start_time) * 1000  # Convert to ms
    cached = optimized_response.status_code == 304
    compressed = 'gzip' in optimized_response.headers.get('Content-Encoding', '')
    compression_ratio = float(optimized_response.headers.get('X-Compression-Ratio', '0').replace('%', ''))
    
    cdn_analytics.record_request(
        cached=cached,
        compressed=compressed,
        compression_ratio=compression_ratio,
        response_time=response_time
    )
    
    return optimized_response