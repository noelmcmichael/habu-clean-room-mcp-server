#!/usr/bin/env python3
"""
Conservative version of Flask API with minimal CDN optimization
Emergency rollback version to fix performance issues
"""
import os
import asyncio
import logging
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from flask_compress import Compress
from agents.enhanced_habu_chat_agent import enhanced_habu_agent
from config.production import production_config
from redis_cache import cache, initialize_cache, shutdown_cache

# Import MCP tools
from tools.habu_list_partners import habu_list_partners
from tools.habu_enhanced_templates import habu_enhanced_templates, habu_list_templates
from tools.habu_submit_query import habu_submit_query
from tools.habu_check_status import habu_check_status
from tools.habu_get_results import habu_get_results
from tools.habu_list_exports import habu_list_exports, habu_download_export
import json

# Configure logging
logging.basicConfig(
    level=getattr(logging, production_config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Enable compression for all responses (70-80% size reduction)
Compress(app)

CORS(app, origins=production_config.CORS_ORIGINS)

# Initialize Redis cache on startup
@app.before_first_request
def initialize_redis():
    """Initialize Redis cache before first request"""
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(initialize_cache())
        logger.info("✅ Redis cache initialized successfully")
    except Exception as e:
        logger.warning(f"⚠️ Redis cache initialization failed: {e}")
    finally:
        loop.close()

@app.teardown_appcontext
def close_redis(error):
    """Clean up Redis connection"""
    # Connection cleanup is handled by Redis connection pool
    pass

@app.route('/', methods=['GET'])
def root():
    """Root endpoint for health checks"""
    return jsonify({
        'service': 'Habu Enhanced Chat API',
        'version': 'Phase H - Conservative Rollback',
        'status': 'operational',
        'endpoints': [
            '/api/enhanced-chat',
            '/api/health',
            '/api/cache-stats',
            '/api/mcp/habu_list_templates',
            '/api/mcp/habu_enhanced_templates',
            '/api/mcp/habu_list_partners'
        ]
    })

@app.route('/health', methods=['GET'])
def simple_health():
    """Simple health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'habu-chat-api', 'timestamp': 'working'})

@app.route('/api/cache-stats', methods=['GET'])
def cache_stats():
    """Redis cache statistics endpoint"""
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            stats = loop.run_until_complete(cache.get_cache_stats())
            return jsonify({
                'cache_stats': stats,
                'timestamp': 'working'
            })
        finally:
            loop.close()
    except Exception as e:
        logger.error(f"Error getting cache stats: {e}")
        return jsonify({
            'error': 'Failed to get cache stats',
            'detail': str(e)
        }), 500

@app.route('/api/enhanced-chat', methods=['POST'])
def enhanced_chat():
    """Handle enhanced chat requests from React frontend with Redis caching"""
    try:
        data = request.get_json()
        if not data:
            logger.warning("No JSON data received")
            return jsonify({'error': 'No JSON data provided'}), 400
            
        user_input = data.get('user_input', '')
        session_id = data.get('session_id', 'default')
        
        if not user_input:
            logger.warning("Empty user input received")
            return jsonify({'error': 'No user input provided'}), 400
        
        logger.info(f"Processing chat request: {user_input[:100]}...")
        
        # Run the async enhanced chat agent with caching
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            # Check for cached response (for exact same queries)
            cache_key = f"chat_{hash(user_input) % 10000}"
            cached_response = loop.run_until_complete(
                cache.get_cached_response(cache_key)
            )
            
            if cached_response and cached_response.get('data'):
                logger.info("✅ Serving cached chat response")
                response_data = cached_response['data']
                response_data['cached'] = True
                response_data['cached_at'] = cached_response.get('cached_at')
                return jsonify({'response': response_data})
            
            # Process new request
            response = loop.run_until_complete(
                enhanced_habu_agent.process_request(user_input)
            )
            
            # Cache the response for similar queries (5 minute TTL)
            loop.run_until_complete(
                cache.cache_api_response(
                    endpoint=cache_key,
                    data=response,
                    cache_type='chat_context',
                    custom_ttl=300  # 5 minutes for chat responses
                )
            )
            
            logger.info("Chat request processed and cached successfully")
            return jsonify({
                'response': response,
                'cached': False
            })
        finally:
            loop.close()
            
    except Exception as e:
        logger.error(f"Error in enhanced_chat: {e}")
        return jsonify({
            'error': 'Internal server error',
            'detail': str(e) if production_config.DEBUG else 'An error occurred processing your request'
        }), 500

@app.route('/api/mcp/habu_list_templates', methods=['GET'])
def api_list_templates():
    """API endpoint for listing templates (now uses enhanced version)"""
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(habu_list_templates())
            return json.loads(result)
        finally:
            loop.close()
    except Exception as e:
        logger.error(f"Error in list_templates: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/mcp/habu_enhanced_templates', methods=['GET'])
def api_enhanced_templates():
    """API endpoint for listing enhanced templates with detailed metadata and caching"""
    try:
        cleanroom_id = request.args.get('cleanroom_id', 'default')
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            # Check cache first
            cache_key = f"enhanced_templates_{cleanroom_id}"
            cached_result = loop.run_until_complete(
                cache.get_cached_response(cache_key)
            )
            
            if cached_result and cached_result.get('data'):
                logger.info("✅ Serving cached enhanced templates")
                response_data = cached_result['data']
                response_data['cached'] = True
                response_data['cached_at'] = cached_result.get('cached_at')
                return response_data
            
            # Fetch fresh data
            result = loop.run_until_complete(habu_enhanced_templates(cleanroom_id))
            result_data = json.loads(result)
            
            # Cache the result (30 minutes TTL for template data)
            loop.run_until_complete(
                cache.cache_api_response(
                    endpoint=cache_key,
                    data=result_data,
                    cache_type='template_data',
                    custom_ttl=1800  # 30 minutes
                )
            )
            
            result_data['cached'] = False
            return result_data
        finally:
            loop.close()
    except Exception as e:
        logger.error(f"Error in enhanced_templates: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/mcp/habu_list_partners', methods=['GET'])
def api_list_partners():
    """API endpoint for listing partners with Redis caching - CONSERVATIVE VERSION"""
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            # Check cache first with shorter timeout to avoid slowdowns
            cached_result = None
            try:
                cached_result = loop.run_until_complete(
                    asyncio.wait_for(
                        cache.get_cached_response('partners_list'),
                        timeout=1.0  # 1 second timeout
                    )
                )
            except asyncio.TimeoutError:
                logger.warning("Cache lookup timed out, proceeding without cache")
            
            if cached_result and cached_result.get('data'):
                logger.info("✅ Serving cached partners list")
                response_data = cached_result['data']
                response_data['cached'] = True
                response_data['cached_at'] = cached_result.get('cached_at')
                return response_data
            
            # Fetch fresh data with timeout
            logger.info("Fetching fresh partners data...")
            result = loop.run_until_complete(
                asyncio.wait_for(
                    habu_list_partners(),
                    timeout=10.0  # 10 second timeout for API call
                )
            )
            result_data = json.loads(result)
            
            # Try to cache the result (don't let caching failure break the response)
            try:
                loop.run_until_complete(
                    asyncio.wait_for(
                        cache.cache_api_response(
                            endpoint='partners_list',
                            data=result_data,
                            cache_type='partner_data',
                            custom_ttl=900  # 15 minutes
                        ),
                        timeout=2.0  # 2 second timeout for caching
                    )
                )
            except asyncio.TimeoutError:
                logger.warning("Cache storage timed out, but response will be served")
            except Exception as cache_error:
                logger.warning(f"Cache storage failed: {cache_error}")
            
            result_data['cached'] = False
            return result_data
        finally:
            loop.close()
    except asyncio.TimeoutError:
        logger.error("Partners API call timed out")
        return jsonify({'error': 'Request timed out', 'status': 'timeout'}), 504
    except Exception as e:
        logger.error(f"Error in list_partners: {e}")
        return jsonify({'error': str(e)}), 500

# Keep other endpoints simple without CDN optimization for now
@app.route('/api/mcp/habu_submit_query', methods=['POST'])
def api_submit_query():
    """API endpoint for submitting queries"""
    try:
        data = request.json
        template_id = data.get('template_id')
        parameters = data.get('parameters', {})
        
        if not template_id:
            return jsonify({'error': 'template_id is required'}), 400
            
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(habu_submit_query(template_id, parameters))
            return json.loads(result)
        finally:
            loop.close()
    except Exception as e:
        logger.error(f"Error in submit_query: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Production configuration
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=production_config.DEBUG)