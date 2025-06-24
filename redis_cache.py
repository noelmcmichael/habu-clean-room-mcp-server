"""
Redis Cache Implementation for Phase H Performance Optimization
Provides intelligent caching for API responses and session management
"""

import json
import logging
import os
import hashlib
from typing import Optional, Any, Dict, Union
from datetime import datetime, timedelta
import redis.asyncio as redis
import asyncio

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RedisCache:
    """
    Advanced Redis caching system for API responses and session management
    """
    
    def __init__(self):
        self.redis = None
        self.connected = False
        self.redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
        
        # Cache configuration
        self.default_ttl = 300  # 5 minutes default
        self.ttl_config = {
            'api_response': 300,      # 5 minutes for API responses
            'chat_context': 600,      # 10 minutes for chat context
            'template_data': 1800,    # 30 minutes for template data
            'partner_data': 900,      # 15 minutes for partner lists
            'cleanroom_data': 600,    # 10 minutes for cleanroom data
            'status_data': 120,       # 2 minutes for status checks
            'session_data': 3600,     # 1 hour for session data
        }
        
    async def connect(self):
        """Initialize Redis connection with fallback handling"""
        try:
            self.redis = redis.from_url(
                self.redis_url,
                encoding='utf-8',
                decode_responses=True,
                socket_timeout=5,
                socket_connect_timeout=5,
                retry_on_timeout=True,
                health_check_interval=30
            )
            
            # Test connection
            await self.redis.ping()
            self.connected = True
            logger.info("✅ Redis cache connected successfully")
            
        except Exception as e:
            logger.warning(f"⚠️ Redis connection failed: {e}")
            logger.info("📄 Falling back to in-memory cache")
            self.connected = False
            self.redis = None
            
    async def disconnect(self):
        """Close Redis connection"""
        if self.redis:
            await self.redis.close()
            self.connected = False
            logger.info("Redis connection closed")
    
    def _generate_cache_key(self, prefix: str, identifier: str, params: Optional[Dict] = None) -> str:
        """Generate consistent cache key with optional parameters"""
        key_parts = [prefix, identifier]
        
        if params:
            # Sort params for consistent key generation
            sorted_params = json.dumps(params, sort_keys=True)
            param_hash = hashlib.md5(sorted_params.encode()).hexdigest()[:8]
            key_parts.append(param_hash)
            
        return ":".join(key_parts)
    
    async def cache_api_response(self, 
                               endpoint: str, 
                               data: Union[Dict, str], 
                               cache_type: str = 'api_response',
                               custom_ttl: Optional[int] = None,
                               params: Optional[Dict] = None) -> bool:
        """
        Cache API response with intelligent TTL
        
        Args:
            endpoint: API endpoint identifier
            data: Response data to cache
            cache_type: Type of cache for TTL lookup
            custom_ttl: Override TTL in seconds
            params: Additional parameters for cache key generation
        """
        if not self.connected:
            return False
            
        try:
            cache_key = self._generate_cache_key('api', endpoint, params)
            ttl = custom_ttl or self.ttl_config.get(cache_type, self.default_ttl)
            
            # Prepare cache entry with metadata
            cache_entry = {
                'data': data,
                'cached_at': datetime.utcnow().isoformat(),
                'cache_type': cache_type,
                'ttl': ttl
            }
            
            # Store in Redis
            await self.redis.setex(
                cache_key,
                ttl,
                json.dumps(cache_entry, default=str)
            )
            
            logger.info(f"✅ Cached {cache_type} for {endpoint} (TTL: {ttl}s)")
            return True
            
        except Exception as e:
            logger.error(f"❌ Cache write failed for {endpoint}: {e}")
            return False
    
    async def get_cached_response(self, 
                                endpoint: str, 
                                params: Optional[Dict] = None) -> Optional[Dict]:
        """
        Retrieve cached API response with metadata
        
        Args:
            endpoint: API endpoint identifier
            params: Additional parameters for cache key generation
            
        Returns:
            Cached data with metadata or None if not found/expired
        """
        if not self.connected:
            return None
            
        try:
            cache_key = self._generate_cache_key('api', endpoint, params)
            cached_data = await self.redis.get(cache_key)
            
            if cached_data:
                cache_entry = json.loads(cached_data)
                
                # Add cache hit metadata
                cache_entry['cache_hit'] = True
                cache_entry['retrieved_at'] = datetime.utcnow().isoformat()
                
                logger.info(f"✅ Cache hit for {endpoint}")
                return cache_entry
                
        except Exception as e:
            logger.error(f"❌ Cache read failed for {endpoint}: {e}")
            
        return None
    
    async def cache_chat_context(self, 
                               session_id: str, 
                               context: Dict,
                               custom_ttl: Optional[int] = None) -> bool:
        """Cache chat conversation context"""
        return await self.cache_api_response(
            endpoint=f"chat_context_{session_id}",
            data=context,
            cache_type='chat_context',
            custom_ttl=custom_ttl
        )
    
    async def get_chat_context(self, session_id: str) -> Optional[Dict]:
        """Retrieve cached chat context"""
        result = await self.get_cached_response(f"chat_context_{session_id}")
        return result['data'] if result else None
    
    async def cache_template_data(self, 
                                template_id: str, 
                                enhanced_data: Dict,
                                custom_ttl: Optional[int] = None) -> bool:
        """Cache enhanced template data"""
        return await self.cache_api_response(
            endpoint=f"template_{template_id}",
            data=enhanced_data,
            cache_type='template_data',
            custom_ttl=custom_ttl
        )
    
    async def get_template_data(self, template_id: str) -> Optional[Dict]:
        """Retrieve cached template data"""
        result = await self.get_cached_response(f"template_{template_id}")
        return result['data'] if result else None
    
    async def cache_partner_list(self, 
                               org_id: str, 
                               partners: Dict,
                               custom_ttl: Optional[int] = None) -> bool:
        """Cache partner list data"""
        return await self.cache_api_response(
            endpoint=f"partners_{org_id}",
            data=partners,
            cache_type='partner_data',
            custom_ttl=custom_ttl
        )
    
    async def get_partner_list(self, org_id: str) -> Optional[Dict]:
        """Retrieve cached partner list"""
        result = await self.get_cached_response(f"partners_{org_id}")
        return result['data'] if result else None
    
    async def invalidate_cache(self, pattern: str) -> int:
        """
        Invalidate cache entries matching pattern
        
        Args:
            pattern: Redis key pattern (e.g., 'api:partners_*')
            
        Returns:
            Number of keys deleted
        """
        if not self.connected:
            return 0
            
        try:
            keys = await self.redis.keys(pattern)
            if keys:
                deleted = await self.redis.delete(*keys)
                logger.info(f"🗑️ Invalidated {deleted} cache entries matching {pattern}")
                return deleted
        except Exception as e:
            logger.error(f"❌ Cache invalidation failed for {pattern}: {e}")
            
        return 0
    
    async def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics and health info"""
        if not self.connected:
            return {
                'connected': False,
                'error': 'Redis not connected'
            }
            
        try:
            info = await self.redis.info()
            
            # Get key counts by pattern
            key_counts = {}
            for cache_type in self.ttl_config.keys():
                pattern = f"api:*{cache_type}*"
                keys = await self.redis.keys(pattern)
                key_counts[cache_type] = len(keys)
            
            return {
                'connected': True,
                'redis_version': info.get('redis_version'),
                'used_memory': info.get('used_memory_human'),
                'connected_clients': info.get('connected_clients'),
                'total_commands_processed': info.get('total_commands_processed'),
                'keyspace_hits': info.get('keyspace_hits', 0),
                'keyspace_misses': info.get('keyspace_misses', 0),
                'hit_rate': self._calculate_hit_rate(
                    info.get('keyspace_hits', 0),
                    info.get('keyspace_misses', 0)
                ),
                'cache_key_counts': key_counts,
                'ttl_config': self.ttl_config
            }
        except Exception as e:
            return {
                'connected': True,
                'error': str(e)
            }
    
    def _calculate_hit_rate(self, hits: int, misses: int) -> float:
        """Calculate cache hit rate percentage"""
        total = hits + misses
        if total == 0:
            return 0.0
        return round((hits / total) * 100, 2)

# Global cache instance
cache = RedisCache()

async def initialize_cache():
    """Initialize the global cache instance"""
    await cache.connect()

async def shutdown_cache():
    """Shutdown the global cache instance"""
    await cache.disconnect()

# Decorator for automatic caching
def cache_response(cache_type: str = 'api_response', ttl: Optional[int] = None):
    """
    Decorator to automatically cache function responses
    
    Usage:
        @cache_response('partner_data', 900)
        async def get_partners(org_id: str):
            # API call here
            return partner_data
    """
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # Generate cache key from function name and arguments
            cache_key = f"{func.__name__}_{hashlib.md5(str(args + tuple(kwargs.items())).encode()).hexdigest()[:8]}"
            
            # Try to get from cache first
            cached_result = await cache.get_cached_response(cache_key)
            if cached_result:
                return cached_result['data']
            
            # Execute function and cache result
            result = await func(*args, **kwargs)
            await cache.cache_api_response(cache_key, result, cache_type, ttl)
            
            return result
        return wrapper
    return decorator