#!/usr/bin/env python3
"""
Simple API test to identify deployment issues
"""

from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def root():
    return jsonify({
        'service': 'Habu API Test',
        'status': 'working',
        'message': 'Simple test successful'
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=False)