#!/usr/bin/env python3
"""
Test Redis integration for Phase H optimization
"""

import asyncio
import os
import json
from redis_cache import cache, initialize_cache, shutdown_cache

async def test_redis_integration():
    """Test Redis cache functionality"""
    print("🚀 Testing Redis Integration...")
    
    # Initialize cache
    await initialize_cache()
    
    if not cache.connected:
        print("⚠️ Redis not connected - testing will use fallback behavior")
    else:
        print("✅ Redis connected successfully")
    
    # Test 1: Basic caching
    print("\n📝 Test 1: Basic API Response Caching")
    test_data = {
        "partners": [
            {"id": "123", "name": "Test Partner 1"},
            {"id": "456", "name": "Test Partner 2"}
        ],
        "total": 2
    }
    
    # Cache the data
    cached = await cache.cache_api_response(
        endpoint="test_partners",
        data=test_data,
        cache_type="partner_data",
        custom_ttl=60
    )
    print(f"Cache write result: {cached}")
    
    # Retrieve the data
    retrieved = await cache.get_cached_response("test_partners")
    if retrieved:
        print(f"✅ Cache retrieval successful: {retrieved['data']['total']} partners")
        print(f"Cached at: {retrieved['cached_at']}")
    else:
        print("❌ Cache retrieval failed")
    
    # Test 2: Chat context caching
    print("\n💬 Test 2: Chat Context Caching")
    chat_context = {
        "session_id": "test_session_123",
        "last_query": "List all partners",
        "context": "User is exploring partner data",
        "timestamp": "2024-01-01T12:00:00Z"
    }
    
    cached_chat = await cache.cache_chat_context("test_session_123", chat_context)
    print(f"Chat cache write result: {cached_chat}")
    
    # Retrieve chat context
    retrieved_chat = await cache.get_chat_context("test_session_123")
    if retrieved_chat:
        print(f"✅ Chat context retrieval successful: {retrieved_chat['last_query']}")
    else:
        print("❌ Chat context retrieval failed")
    
    # Test 3: Template data caching
    print("\n📋 Test 3: Template Data Caching")
    template_data = {
        "template_id": "template_456",
        "enhanced_metadata": {
            "business_context": "Customer segmentation analysis",
            "recommended_use": "Demographic targeting",
            "complexity": "Medium"
        },
        "columns": ["age", "gender", "location"]
    }
    
    cached_template = await cache.cache_template_data("template_456", template_data)
    print(f"Template cache write result: {cached_template}")
    
    # Retrieve template data
    retrieved_template = await cache.get_template_data("template_456")
    if retrieved_template:
        print(f"✅ Template data retrieval successful: {retrieved_template['enhanced_metadata']['business_context']}")
    else:
        print("❌ Template data retrieval failed")
    
    # Test 4: Cache statistics
    print("\n📊 Test 4: Cache Statistics")
    stats = await cache.get_cache_stats()
    print(f"Cache stats: {json.dumps(stats, indent=2)}")
    
    # Test 5: Cache invalidation
    print("\n🗑️ Test 5: Cache Invalidation")
    deleted_count = await cache.invalidate_cache("api:test_*")
    print(f"Deleted {deleted_count} cache entries")
    
    # Verify deletion
    after_delete = await cache.get_cached_response("test_partners")
    if after_delete:
        print("❌ Cache deletion failed - data still exists")
    else:
        print("✅ Cache deletion successful")
    
    # Cleanup
    await shutdown_cache()
    print("\n🏁 Redis integration test complete!")

if __name__ == "__main__":
    asyncio.run(test_redis_integration())