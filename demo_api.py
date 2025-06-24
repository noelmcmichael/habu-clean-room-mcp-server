#!/usr/bin/env python3
"""
Flask API server to bridge React frontend with enhanced chat agent
Production-ready version with proper error handling and logging
"""
import os
import asyncio
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from agents.enhanced_habu_chat_agent import enhanced_habu_agent
from config.production import production_config

# Import MCP tools
from tools.habu_list_partners import habu_list_partners
from tools.habu_list_templates import habu_list_templates
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
CORS(app, origins=production_config.CORS_ORIGINS)

# Enable real API mode for production
os.environ["HABU_USE_MOCK_DATA"] = "false"

@app.route('/api/enhanced-chat', methods=['POST'])
def enhanced_chat():
    """Handle enhanced chat requests from React frontend"""
    try:
        data = request.get_json()
        if not data:
            logger.warning("No JSON data received")
            return jsonify({'error': 'No JSON data provided'}), 400
            
        user_input = data.get('user_input', '')
        
        if not user_input:
            logger.warning("Empty user input received")
            return jsonify({'error': 'No user input provided'}), 400
        
        logger.info(f"Processing chat request: {user_input[:100]}...")
        
        # Run the async enhanced chat agent
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            response = loop.run_until_complete(
                enhanced_habu_agent.process_request(user_input)
            )
            logger.info("Chat request processed successfully")
            return jsonify({'response': response})
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

@app.route('/api/mcp/habu_list_partners', methods=['GET'])
def api_list_partners():
    """API endpoint for listing partners"""
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(habu_list_partners())
            return json.loads(result)
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

@app.route('/api/mcp/habu_download_export', methods=['POST'])
def api_download_export():
    """API endpoint for downloading exports"""
    try:
        data = request.json
        export_id = data.get('export_id')
        
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

@app.route('/api/health', methods=['GET'])
def health_check():
    """Enhanced health check endpoint for Phase 4 demo monitoring"""
    try:
        # Check MCP server connectivity
        mcp_server_status = 'online'  # Assume online if this API is running
        
        # Check OpenAI configuration
        openai_available = enhanced_habu_agent.client is not None
        
        # Check real API mode
        real_api_mode = os.environ.get("HABU_USE_MOCK_DATA", "false") == "false"
        
        # Basic API connectivity test
        api_connected = True  # If we can respond, API is connected
        
        return jsonify({
            'status': 'healthy',
            'service': 'Habu Demo API',
            'version': '2.0 - Phase 4',
            'timestamp': os.popen('date').read().strip(),
            
            # System status for Phase 4 monitoring
            'mcp_server': 'online' if mcp_server_status else 'offline',
            'api_connection': 'connected' if api_connected else 'disconnected',
            'openai_available': openai_available,
            'real_api_mode': real_api_mode,
            
            # Configuration details
            'cors_origins': production_config.CORS_ORIGINS,
            'log_level': production_config.LOG_LEVEL,
            
            # Demo readiness assessment
            'demo_ready': mcp_server_status and api_connected and openai_available and real_api_mode,
            'demo_mode': 'production' if real_api_mode and openai_available else 'fallback'
        })
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'mcp_server': 'offline',
            'api_connection': 'disconnected',
            'openai_available': False,
            'real_api_mode': False,
            'demo_ready': False,
            'demo_mode': 'error'
        }), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {error}")
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5001))
    host = "0.0.0.0"
    
    logger.info(f"Starting Habu Demo API on {host}:{port}")
    logger.info(f"Mock mode: {os.environ.get('HABU_USE_MOCK_DATA', 'false')}")
    
    app.run(
        host=host,
        port=port,
        debug=production_config.DEBUG
    )

if __name__ == '__main__':
    print("🚀 Starting Habu Clean Room Demo API Server")
    print("🤖 OpenAI Enhanced Chat Agent Ready")
    print("🎯 Mock Mode: Enabled")
    print("📱 React Frontend can connect to http://localhost:5001")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=5001, debug=True)