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

# Configure logging
logging.basicConfig(
    level=getattr(logging, production_config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, origins=production_config.CORS_ORIGINS)

# Enable mock mode for demo
os.environ["HABU_USE_MOCK_DATA"] = "true"

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

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Habu Demo API',
        'version': '2.0',
        'openai_configured': enhanced_habu_agent.client is not None,
        'mock_mode': os.environ.get("HABU_USE_MOCK_DATA", "false") == "true",
        'cors_origins': production_config.CORS_ORIGINS
    })

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