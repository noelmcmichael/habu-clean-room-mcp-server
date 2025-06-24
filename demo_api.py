#!/usr/bin/env python3
"""
Clean Flask API server - Complete rollback to stable Redis-only version
Removes ALL CDN optimization complexity that was causing issues
"""
import os
import asyncio
import logging
from flask import Flask, request, jsonify
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

# Enable basic compression only
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
        'version': 'Phase H1.1 - Stable Redis Only',
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

@app.route('/api/health', methods=['GET'])
def api_health():
    """API health check endpoint for system monitoring"""
    # Check OpenAI availability
    openai_available = bool(os.getenv("OPENAI_API_KEY"))
    
    # Check real API mode
    real_api_mode = not production_config.HABU_USE_MOCK_DATA
    
    # Check Redis connection
    redis_connected = cache.connected if hasattr(cache, 'connected') else False
    
    # Demo readiness - all systems operational
    demo_ready = openai_available and (real_api_mode or production_config.HABU_USE_MOCK_DATA)
    
    return jsonify({
        'status': 'healthy', 
        'service': 'habu-demo-api-v2', 
        'version': 'Phase H1.1 - Stable Redis Only',
        'timestamp': 'working',
        'redis_connected': redis_connected,
        'real_api_mode': real_api_mode,
        'openai_available': openai_available,
        'demo_ready': demo_ready,
        'mcp_server': 'online',
        'demo_mode': 'real-api' if real_api_mode else 'mock-data',
        'habu_client_configured': bool(production_config.HABU_CLIENT_ID),
        'cache_enabled': redis_connected
    })

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

@app.route('/api/support-context', methods=['GET'])
def get_support_context():
    """Get current support context for Customer Support mode"""
    return jsonify({
        "commonQuestions": [
            "Can we do lookalike modeling?",
            "What's the minimum data size?", 
            "How long does implementation take?",
            "What industries do you support?"
        ],
        "industryFocus": ["retail", "automotive", "finance"],
        "customerTier": "enterprise",
        "supportLevel": "standard",
        "escalationThreshold": 3,
        "lastUpdate": "2025-01-22T10:00:00Z"
    })

@app.route('/api/technical-context', methods=['GET'])
def get_technical_context():
    """Get current technical context for Technical Expert mode"""
    return jsonify({
        "availableTools": [
            "habu_list_partners",
            "habu_enhanced_templates", 
            "habu_submit_query",
            "habu_check_status",
            "habu_get_results",
            "habu_list_exports"
        ],
        "apiVersion": "2.0",
        "documentationVersion": "2.0.1",
        "limitations": [
            "Rate limits apply to high-volume queries",
            "Some features require partner agreements"
        ],
        "recentChanges": [
            "Added enhanced privacy controls",
            "Improved match rate algorithms"
        ],
        "capabilityMatrix": {
            "lookalike_modeling": True,
            "identity_resolution": True,
            "segmentation": True,
            "attribution": True,
            "real_time_activation": True
        },
        "integrationPatterns": [
            "REST API integration",
            "Batch file processing",
            "Real-time streaming"
        ]
    })

@app.route('/api/customer-support/quick-assess', methods=['POST'])
def quick_customer_assessment():
    """Quick customer capability assessment for support mode"""
    data = request.get_json()
    if not data or 'query' not in data:
        return jsonify({'error': 'Query is required'}), 400
    
    query = data['query']
    industry = data.get('industry')
    
    try:
        # Simple capability assessment logic
        assessment = generate_quick_assessment(query, industry)
        return jsonify(assessment)
    except Exception as e:
        logger.error(f"Error in quick assessment: {e}")
        return jsonify({'error': 'Assessment failed'}), 500

def generate_quick_assessment(query, industry=None):
    """Generate a quick capability assessment"""
    query_lower = query.lower()
    
    # Check for common use cases
    if any(keyword in query_lower for keyword in ['lookalike', 'similar', 'audience', 'expand']):
        return {
            'feasibility': 'yes',
            'confidence': 'high',
            'summary': '✅ **Yes, lookalike modeling is fully supported!**\n\nCreate audiences similar to your best customers using our 300M+ identity graph.',
            'timeline': '24-48 hours for model creation',
            'businessValue': 'Increase customer acquisition efficiency by 40-60%',
            'competitiveAdvantage': ['90%+ match rates vs industry 60-70%', 'Real-time audience activation'],
            'nextSteps': ['Confirm data requirements', 'Set up proof of concept']
        }
    elif any(keyword in query_lower for keyword in ['segment', 'group', 'cohort', 'cluster']):
        return {
            'feasibility': 'yes',
            'confidence': 'high',
            'summary': '✅ **Yes, customer segmentation is fully supported!**\n\nCreate behavioral and demographic customer segments for targeted marketing.',
            'timeline': '3-5 days for analysis',
            'businessValue': 'Increase campaign effectiveness through personalized targeting',
            'competitiveAdvantage': ['AI-powered segment discovery', 'Real-time segment updates'],
            'nextSteps': ['Review data requirements', 'Schedule implementation planning']
        }
    elif any(keyword in query_lower for keyword in ['identity', 'resolution', 'unify', 'match']):
        return {
            'feasibility': 'yes',
            'confidence': 'high',
            'summary': '✅ **Yes, identity resolution is fully supported!**\n\nUnify customer identities across devices, channels, and data sources.',
            'timeline': '1-3 weeks depending on complexity',
            'businessValue': 'Create unified customer view for personalized experiences',
            'competitiveAdvantage': ['Industry-leading match rates', 'Privacy-first approach'],
            'nextSteps': ['Assess data sources', 'Plan integration approach']
        }
    else:
        return {
            'feasibility': 'partially',
            'confidence': 'medium',
            'summary': '⚠️ **Partially supported - need more details**\n\nPlease provide more specific information about your use case.',
            'timeline': 'Depends on specific requirements',
            'businessValue': 'Business value depends on specific use case',
            'competitiveAdvantage': ['Privacy-first architecture', 'Comprehensive API coverage'],
            'nextSteps': ['Clarify specific requirements', 'Schedule discovery call']
        }

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
            try:
                cached_response = loop.run_until_complete(
                    cache.get_cached_response(cache_key)
                )
                
                if cached_response and cached_response.get('data'):
                    logger.info("✅ Serving cached chat response")
                    response_data = cached_response['data']
                    response_data['cached'] = True
                    response_data['cached_at'] = cached_response.get('cached_at')
                    return jsonify({'response': response_data})
            except Exception as cache_error:
                logger.warning(f"Cache lookup failed: {cache_error}")
            
            # Process new request
            response = loop.run_until_complete(
                enhanced_habu_agent.process_request(user_input)
            )
            
            # Try to cache the response (don't let caching failure break the response)
            try:
                loop.run_until_complete(
                    cache.cache_api_response(
                        endpoint=cache_key,
                        data=response,
                        cache_type='chat_context',
                        custom_ttl=300  # 5 minutes for chat responses
                    )
                )
            except Exception as cache_error:
                logger.warning(f"Cache storage failed: {cache_error}")
            
            logger.info("Chat request processed successfully")
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
    """API endpoint for listing templates"""
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
            try:
                cached_result = loop.run_until_complete(
                    cache.get_cached_response(cache_key)
                )
                
                if cached_result and cached_result.get('data'):
                    logger.info("✅ Serving cached enhanced templates")
                    response_data = cached_result['data']
                    response_data['cached'] = True
                    response_data['cached_at'] = cached_result.get('cached_at')
                    return response_data
            except Exception as cache_error:
                logger.warning(f"Cache lookup failed: {cache_error}")
            
            # Fetch fresh data
            result = loop.run_until_complete(habu_enhanced_templates(cleanroom_id))
            result_data = json.loads(result)
            
            # Try to cache the result
            try:
                loop.run_until_complete(
                    cache.cache_api_response(
                        endpoint=cache_key,
                        data=result_data,
                        cache_type='template_data',
                        custom_ttl=1800  # 30 minutes
                    )
                )
            except Exception as cache_error:
                logger.warning(f"Cache storage failed: {cache_error}")
            
            result_data['cached'] = False
            return result_data
        finally:
            loop.close()
    except Exception as e:
        logger.error(f"Error in enhanced_templates: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/mcp/habu_list_partners', methods=['GET'])
def api_list_partners():
    """API endpoint for listing partners with Redis caching"""
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            # Check cache first
            try:
                cached_result = loop.run_until_complete(
                    cache.get_cached_response('partners_list')
                )
                
                if cached_result and cached_result.get('data'):
                    logger.info("✅ Serving cached partners list")
                    response_data = cached_result['data']
                    response_data['cached'] = True
                    response_data['cached_at'] = cached_result.get('cached_at')
                    return response_data
            except Exception as cache_error:
                logger.warning(f"Cache lookup failed: {cache_error}")
            
            # Fetch fresh data
            logger.info("Fetching fresh partners data...")
            result = loop.run_until_complete(habu_list_partners())
            result_data = json.loads(result)
            
            # Try to cache the result
            try:
                loop.run_until_complete(
                    cache.cache_api_response(
                        endpoint='partners_list',
                        data=result_data,
                        cache_type='partner_data',
                        custom_ttl=900  # 15 minutes
                    )
                )
            except Exception as cache_error:
                logger.warning(f"Cache storage failed: {cache_error}")
            
            result_data['cached'] = False
            return result_data
        finally:
            loop.close()
    except Exception as e:
        logger.error(f"Error in list_partners: {e}")
        return jsonify({'error': str(e)}), 500

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

@app.route('/api/mcp/habu_check_status', methods=['GET'])
def api_check_status():
    """API endpoint for checking status"""
    try:
        query_id = request.args.get('query_id')
        if not query_id:
            return jsonify({'error': 'query_id is required'}), 400
            
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(habu_check_status(query_id))
            return json.loads(result)
        finally:
            loop.close()
    except Exception as e:
        logger.error(f"Error in check_status: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/mcp/habu_get_results', methods=['GET'])
def api_get_results():
    """API endpoint for getting results"""
    try:
        query_id = request.args.get('query_id')
        if not query_id:
            return jsonify({'error': 'query_id is required'}), 400
            
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(habu_get_results(query_id))
            return json.loads(result)
        finally:
            loop.close()
    except Exception as e:
        logger.error(f"Error in get_results: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/mcp/habu_list_exports', methods=['GET'])
def api_list_exports():
    """API endpoint for listing exports"""
    try:
        status_filter = request.args.get('status')
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(habu_list_exports(status_filter))
            return json.loads(result)
        finally:
            loop.close()
    except Exception as e:
        logger.error(f"Error in list_exports: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/mcp/habu_download_export', methods=['GET'])
def api_download_export():
    """API endpoint for downloading exports"""
    try:
        export_id = request.args.get('export_id')
        if not export_id:
            return jsonify({'error': 'export_id is required'}), 400
            
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(habu_download_export(export_id))
            return json.loads(result)
        finally:
            loop.close()
    except Exception as e:
        logger.error(f"Error in download_export: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Production configuration
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=production_config.DEBUG)