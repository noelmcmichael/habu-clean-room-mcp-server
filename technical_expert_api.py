#!/usr/bin/env python3
"""
Technical Expert API endpoints for LiveRamp API technical implementation guidance
Provides detailed technical responses, code examples, and troubleshooting for engineers
"""

import json
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from flask import Flask, request, jsonify
from flask_cors import CORS

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class CodeExample:
    language: str
    title: str
    description: str
    code: str
    dependencies: List[str]
    notes: List[str]

@dataclass
class APIMethod:
    name: str
    endpoint: str
    method: str
    description: str
    parameters: List[Dict]
    responses: List[Dict]
    examples: List[Dict]
    use_cases: List[str]
    limitations: List[str]
    best_practices: List[str]
    related_methods: List[str]

@dataclass
class TechnicalResponse:
    type: str  # 'api_method', 'implementation', 'troubleshooting', 'best_practice', 'explanation'
    title: str
    summary: str
    code_examples: List[Dict]
    api_methods: List[Dict]
    implementation_steps: List[str]
    best_practices: List[str]
    common_issues: List[Dict]
    performance_considerations: List[str]
    security_guidance: List[str]
    limitations: List[str]
    related_topics: List[str]
    documentation: List[Dict]
    validation_status: str  # 'verified', 'needs_verification', 'community_contributed'

class TechnicalExpertEngine:
    """Core engine for generating technical expert responses"""
    
    def __init__(self):
        self.api_methods = {}
        self.implementation_patterns = {}
        self.troubleshooting_guides = {}
        self._initialize_knowledge_base()
    
    def _initialize_knowledge_base(self):
        """Initialize the technical knowledge base"""
        
        # Identity Resolution API
        identity_resolution = {
            "name": "Identity Resolution",
            "endpoint": "/v2/identity/resolve",
            "method": "POST",
            "description": "Resolve customer identities across multiple data sources and touchpoints",
            "parameters": [
                {
                    "name": "identifiers",
                    "type": "array",
                    "required": True,
                    "description": "Array of customer identifiers (email, phone, postal address)",
                    "example": [
                        {"type": "email", "value": "customer@example.com"},
                        {"type": "phone", "value": "+1234567890"}
                    ]
                },
                {
                    "name": "resolution_strategy", 
                    "type": "string",
                    "required": False,
                    "description": "Resolution strategy: strict, moderate, or flexible",
                    "example": "moderate",
                    "validation": "One of: strict, moderate, flexible"
                },
                {
                    "name": "privacy_mode",
                    "type": "string", 
                    "required": False,
                    "description": "Privacy compliance mode",
                    "example": "gdpr_compliant",
                    "validation": "One of: standard, gdpr_compliant, ccpa_compliant"
                }
            ],
            "responses": [
                {
                    "status": 200,
                    "description": "Successful identity resolution",
                    "example": {
                        "resolved_identity": {
                            "confidence_score": 0.92,
                            "canonical_identifiers": ["RampID:abc123"],
                            "linked_identifiers": [
                                {"type": "email", "value": "customer@example.com", "confidence": 0.95}
                            ]
                        }
                    }
                },
                {
                    "status": 400,
                    "description": "Invalid request parameters",
                    "example": {"error": "Missing required parameter: identifiers"}
                }
            ],
            "examples": [
                {
                    "language": "python",
                    "title": "Basic Identity Resolution",
                    "description": "Resolve customer identity using email and phone",
                    "code": """import requests

# LiveRamp Identity Resolution API
api_url = "https://api.liveramp.com/v2/identity/resolve"
headers = {
    "Authorization": "Bearer YOUR_API_TOKEN",
    "Content-Type": "application/json"
}

# Customer identifiers to resolve
identifiers = [
    {"type": "email", "value": "customer@example.com"},
    {"type": "phone", "value": "+1234567890"}
]

payload = {
    "identifiers": identifiers,
    "resolution_strategy": "moderate",
    "privacy_mode": "gdpr_compliant"
}

response = requests.post(api_url, headers=headers, json=payload)

if response.status_code == 200:
    result = response.json()
    confidence = result["resolved_identity"]["confidence_score"]
    ramp_id = result["resolved_identity"]["canonical_identifiers"][0]
    
    print(f"Identity resolved with {confidence:.1%} confidence")
    print(f"RampID: {ramp_id}")
else:
    print(f"API Error: {response.status_code} - {response.text}")""",
                    "dependencies": ["requests"],
                    "notes": [
                        "Replace YOUR_API_TOKEN with actual authentication token",
                        "Consider implementing retry logic for production use",
                        "Monitor confidence scores to ensure data quality"
                    ]
                },
                {
                    "language": "javascript",
                    "title": "Identity Resolution with Error Handling",
                    "description": "Complete implementation with error handling and retry logic",
                    "code": """const axios = require('axios');

class LiveRampIdentityAPI {
  constructor(apiToken, baseURL = 'https://api.liveramp.com') {
    this.apiToken = apiToken;
    this.baseURL = baseURL;
    this.headers = {
      'Authorization': `Bearer ${apiToken}`,
      'Content-Type': 'application/json'
    };
  }

  async resolveIdentity(identifiers, options = {}) {
    const {
      resolutionStrategy = 'moderate',
      privacyMode = 'standard',
      retries = 3
    } = options;

    const payload = {
      identifiers,
      resolution_strategy: resolutionStrategy,
      privacy_mode: privacyMode
    };

    for (let attempt = 1; attempt <= retries; attempt++) {
      try {
        const response = await axios.post(
          `${this.baseURL}/v2/identity/resolve`,
          payload,
          { headers: this.headers, timeout: 30000 }
        );

        return {
          success: true,
          data: response.data,
          confidence: response.data.resolved_identity.confidence_score
        };

      } catch (error) {
        if (attempt === retries) {
          throw new Error(`Identity resolution failed after ${retries} attempts: ${error.message}`);
        }
        
        // Exponential backoff
        await new Promise(resolve => setTimeout(resolve, Math.pow(2, attempt) * 1000));
      }
    }
  }
}

// Usage example
async function main() {
  const api = new LiveRampIdentityAPI('YOUR_API_TOKEN');
  
  const identifiers = [
    { type: 'email', value: 'customer@example.com' },
    { type: 'phone', value: '+1234567890' }
  ];

  try {
    const result = await api.resolveIdentity(identifiers, {
      resolutionStrategy: 'moderate',
      privacyMode: 'gdpr_compliant'
    });

    console.log('Identity Resolution Success:');
    console.log(`Confidence: ${(result.confidence * 100).toFixed(1)}%`);
    console.log(`RampID: ${result.data.resolved_identity.canonical_identifiers[0]}`);
    
  } catch (error) {
    console.error('Identity Resolution Error:', error.message);
  }
}

main();""",
                    "dependencies": ["axios"],
                    "notes": [
                        "Implements retry logic with exponential backoff",
                        "Includes proper error handling and timeout configuration",
                        "Consider implementing rate limiting for high-volume usage"
                    ]
                }
            ],
            "use_cases": [
                "Customer data unification across touchpoints",
                "Cross-device customer journey tracking", 
                "Privacy-compliant customer identification",
                "Data enrichment and customer profiling"
            ],
            "limitations": [
                "Requires minimum 2 identifiers for effective resolution",
                "Resolution accuracy depends on data quality and freshness",
                "Privacy regulations may limit available resolution strategies",
                "Rate limits apply: 1000 requests per minute per account"
            ],
            "best_practices": [
                "Always include multiple identifier types for better accuracy",
                "Use appropriate privacy mode based on data governance requirements",
                "Monitor confidence scores and set minimum thresholds",
                "Implement proper error handling and retry logic",
                "Cache results appropriately to minimize API calls"
            ],
            "related_methods": [
                "Audience Segmentation",
                "Lookalike Modeling", 
                "Cross-Platform Attribution"
            ]
        }
        
        self.api_methods["identity_resolution"] = identity_resolution
        
        # Audience Segmentation API
        audience_segmentation = {
            "name": "Audience Segmentation",
            "endpoint": "/v2/audiences/segment", 
            "method": "POST",
            "description": "Create customer segments based on attributes, behaviors, and identities",
            "parameters": [
                {
                    "name": "segment_criteria",
                    "type": "object",
                    "required": True,
                    "description": "Criteria for segment creation",
                    "example": {
                        "demographic": {"age_range": [25, 65], "income_range": [50000, 150000]},
                        "behavioral": {"purchase_frequency": "high", "category_affinity": ["electronics", "fashion"]},
                        "geographic": {"regions": ["US-CA", "US-NY"], "exclude_rural": True}
                    }
                },
                {
                    "name": "segment_size_target",
                    "type": "number",
                    "required": False,
                    "description": "Target segment size",
                    "example": 100000,
                    "validation": "Minimum: 1000, Maximum: 10000000"
                }
            ],
            "responses": [
                {
                    "status": 200,
                    "description": "Successful segment creation",
                    "example": {
                        "segment_id": "seg_abc123",
                        "segment_size": 95432,
                        "quality_metrics": {
                            "average_confidence": 0.84,
                            "completeness_score": 0.91
                        }
                    }
                }
            ],
            "examples": [
                {
                    "language": "python",
                    "title": "High-Value Customer Segmentation",
                    "description": "Create segment of high-value customers for premium campaign",
                    "code": """import requests
from datetime import datetime

def create_high_value_segment(api_token, target_size=50000):
    url = "https://api.liveramp.com/v2/audiences/segment"
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    
    # Define high-value customer criteria
    segment_criteria = {
        "demographic": {
            "age_range": [25, 55],
            "income_range": [75000, 500000],
            "education": ["college", "graduate"]
        },
        "behavioral": {
            "purchase_frequency": "high",
            "lifetime_value_range": [1000, None],
            "category_affinity": ["luxury", "premium_brands"],
            "recency_days": 90
        },
        "geographic": {
            "regions": ["US-CA", "US-NY", "US-FL", "US-TX"],
            "exclude_rural": True,
            "metro_areas_only": True
        }
    }
    
    payload = {
        "segment_criteria": segment_criteria,
        "segment_size_target": target_size,
        "quality_threshold": 0.8,
        "segment_name": f"High_Value_Customers_{datetime.now().strftime('%Y%m%d')}"
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        
        result = response.json()
        print(f"✅ Segment created: {result['segment_id']}")
        print(f"Size: {result['segment_size']:,} customers")
        
        return result
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Segmentation failed: {e}")
        return None

# Usage
segment = create_high_value_segment("YOUR_API_TOKEN", target_size=50000)""",
                    "dependencies": ["requests"],
                    "notes": [
                        "Adjust criteria based on your customer data attributes",
                        "Monitor quality scores to ensure segment effectiveness"
                    ]
                }
            ],
            "use_cases": [
                "Customer lifecycle stage segmentation",
                "Behavioral targeting for campaigns",
                "Lookalike seed audience creation",
                "Personalization engine input"
            ],
            "limitations": [
                "Minimum segment size: 1,000 customers",
                "Complex criteria may reduce segment size",
                "Data freshness affects segment accuracy"
            ],
            "best_practices": [
                "Start with broader criteria and refine iteratively",
                "Monitor segment performance and quality metrics",
                "Use appropriate refresh frequency for use case"
            ],
            "related_methods": [
                "Identity Resolution",
                "Lookalike Modeling",
                "Customer Journey Analytics"
            ]
        }
        
        self.api_methods["audience_segmentation"] = audience_segmentation
    
    def generate_technical_response(self, query: str, context: Optional[Dict] = None) -> TechnicalResponse:
        """Generate technical response based on query"""
        
        query_lower = query.lower()
        
        # Determine response type based on query content
        if any(keyword in query_lower for keyword in ['how to', 'implement', 'integration']):
            return self._generate_implementation_response(query, context)
        elif any(keyword in query_lower for keyword in ['error', 'issue', 'problem', 'troubleshoot']):
            return self._generate_troubleshooting_response(query, context)
        elif any(keyword in query_lower for keyword in ['api', 'method', 'endpoint']):
            return self._generate_api_method_response(query, context)
        else:
            return self._generate_explanation_response(query, context)
    
    def _generate_api_method_response(self, query: str, context: Optional[Dict] = None) -> TechnicalResponse:
        """Generate API method documentation response"""
        
        query_lower = query.lower()
        
        # Find relevant API method
        api_method = None
        if any(keyword in query_lower for keyword in ['identity', 'resolve', 'resolution']):
            api_method = self.api_methods.get("identity_resolution")
        elif any(keyword in query_lower for keyword in ['segment', 'audience', 'segmentation']):
            api_method = self.api_methods.get("audience_segmentation")
        
        if api_method:
            return TechnicalResponse(
                type="api_method",
                title=api_method["name"],
                summary=api_method["description"],
                code_examples=api_method["examples"],
                api_methods=[api_method],
                implementation_steps=[
                    "Set up authentication with API token",
                    "Configure request headers and parameters", 
                    "Implement error handling and retry logic",
                    "Test with sample data",
                    "Deploy with monitoring and logging"
                ],
                best_practices=api_method["best_practices"],
                common_issues=[
                    {
                        "issue": "Authentication failures",
                        "solution": "Verify API token and permissions",
                        "prevention": "Implement token validation before requests"
                    },
                    {
                        "issue": "Rate limit exceeded",
                        "solution": "Implement exponential backoff and reduce request frequency",
                        "prevention": "Monitor API usage and implement request queuing"
                    }
                ],
                performance_considerations=[
                    "Monitor response times and optimize as needed",
                    "Implement caching for frequently accessed data",
                    "Use appropriate timeout values"
                ],
                security_guidance=[
                    "Use HTTPS for all API communications",
                    "Store API tokens securely",
                    "Validate all input parameters"
                ],
                limitations=api_method["limitations"],
                related_topics=api_method["related_methods"],
                documentation=[
                    {
                        "title": f"{api_method['name']} API Documentation",
                        "url": f"https://docs.liveramp.com/api/{api_method['name'].lower().replace(' ', '-')}",
                        "type": "official"
                    }
                ],
                validation_status="verified"
            )
        
        # Generic API response if no specific method found
        return self._generate_generic_api_response(query)
    
    def _generate_implementation_response(self, query: str, context: Optional[Dict] = None) -> TechnicalResponse:
        """Generate implementation guidance response"""
        
        return TechnicalResponse(
            type="implementation",
            title="Implementation Guidance",
            summary=f"Technical implementation guidance for: {query}",
            code_examples=[
                {
                    "language": "python",
                    "title": "Basic Implementation Template",
                    "description": "Template for implementing LiveRamp API integration",
                    "code": """import requests
import json
from typing import Dict, Optional

class LiveRampAPIClient:
    def __init__(self, api_token: str, base_url: str = 'https://api.liveramp.com'):
        self.api_token = api_token
        self.base_url = base_url
        self.headers = {
            'Authorization': f'Bearer {api_token}',
            'Content-Type': 'application/json'
        }
    
    def make_request(self, endpoint: str, method: str = 'GET', 
                    payload: Optional[Dict] = None) -> Dict:
        \"\"\"Make authenticated request to LiveRamp API\"\"\"
        
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=self.headers, timeout=30)
            elif method == 'POST':
                response = requests.post(url, headers=self.headers, 
                                       json=payload, timeout=30)
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"API request failed: {e}")
            raise

# Usage
client = LiveRampAPIClient("YOUR_API_TOKEN")
result = client.make_request("/v2/health")
print(f"API Health: {result}")""",
                    "dependencies": ["requests"],
                    "notes": [
                        "Replace YOUR_API_TOKEN with actual authentication token",
                        "Add specific error handling for your use case",
                        "Consider implementing retry logic for production use"
                    ]
                }
            ],
            api_methods=[],
            implementation_steps=[
                "Plan your implementation approach",
                "Set up development environment", 
                "Implement core functionality",
                "Add error handling and logging",
                "Test thoroughly before deployment",
                "Monitor and optimize performance"
            ],
            best_practices=[
                "Follow coding standards and best practices",
                "Implement comprehensive testing",
                "Use version control and proper deployment procedures",
                "Document your implementation thoroughly"
            ],
            common_issues=[
                {
                    "issue": "Authentication setup",
                    "solution": "Verify API token format and permissions",
                    "prevention": "Test authentication before implementing business logic"
                }
            ],
            performance_considerations=[
                "Consider caching strategies for frequently accessed data",
                "Implement proper error handling and retry mechanisms",
                "Monitor API usage and response times"
            ],
            security_guidance=[
                "Store API credentials securely",
                "Use environment variables for configuration",
                "Implement proper input validation"
            ],
            limitations=[
                "Implementation depends on specific use case requirements",
                "Rate limits and quotas apply to all API calls"
            ],
            related_topics=[
                "API Authentication",
                "Error Handling Best Practices",
                "Performance Optimization"
            ],
            documentation=[
                {
                    "title": "LiveRamp API Getting Started Guide",
                    "url": "https://docs.liveramp.com/getting-started",
                    "type": "official"
                }
            ],
            validation_status="verified"
        )
    
    def _generate_troubleshooting_response(self, query: str, context: Optional[Dict] = None) -> TechnicalResponse:
        """Generate troubleshooting guidance response"""
        
        return TechnicalResponse(
            type="troubleshooting",
            title="Troubleshooting Guide", 
            summary=f"Troubleshooting guidance for: {query}",
            code_examples=[
                {
                    "language": "python",
                    "title": "API Health Check and Debugging",
                    "description": "Comprehensive API health check with detailed error reporting",
                    "code": """import requests
import json
from datetime import datetime

def run_api_health_check(api_token: str) -> Dict:
    \"\"\"Run comprehensive API health check\"\"\"
    
    base_url = 'https://api.liveramp.com'
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json'
    }
    
    results = {
        'timestamp': datetime.now().isoformat(),
        'api_token_valid': False,
        'endpoints_tested': {},
        'recommendations': []
    }
    
    # Test 1: Authentication
    try:
        response = requests.get(f"{base_url}/v2/auth/validate", 
                              headers=headers, timeout=10)
        results['api_token_valid'] = response.status_code == 200
        print(f"🔐 Authentication: {'✅ VALID' if results['api_token_valid'] else '❌ INVALID'}")
        
        if not results['api_token_valid']:
            print(f"   Error: {response.text}")
            results['recommendations'].append('Verify API token and permissions')
            return results
            
    except Exception as e:
        print(f"❌ Authentication test failed: {e}")
        results['recommendations'].append('Check network connectivity and API endpoint')
        return results
    
    # Test 2: Health endpoint
    try:
        response = requests.get(f"{base_url}/v2/health", 
                              headers=headers, timeout=10)
        results['endpoints_tested']['/v2/health'] = {
            'status_code': response.status_code,
            'success': response.status_code == 200
        }
        print(f"🌐 Health endpoint: {'✅ OK' if response.status_code == 200 else '❌ FAILED'}")
        
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        results['endpoints_tested']['/v2/health'] = {
            'status_code': None,
            'success': False,
            'error': str(e)
        }
    
    # Generate recommendations
    if not any(result['success'] for result in results['endpoints_tested'].values()):
        results['recommendations'].append('Check API service status and network connectivity')
    
    print("\\n💡 Recommendations:")
    for rec in results['recommendations']:
        print(f"   • {rec}")
    
    return results

# Usage
if __name__ == "__main__":
    health_results = run_api_health_check("YOUR_API_TOKEN")
    
    # Save results
    with open(f"health_check_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", 'w') as f:
        json.dump(health_results, f, indent=2)""",
                    "dependencies": ["requests"],
                    "notes": [
                        "Run this health check before deploying to production",
                        "Schedule regular health checks to monitor API status",
                        "Keep health check results for troubleshooting history"
                    ]
                }
            ],
            api_methods=[],
            implementation_steps=[
                "Identify the specific error or issue",
                "Run comprehensive health check",
                "Check authentication and permissions",
                "Test individual endpoints",
                "Analyze response times and errors",
                "Implement recommended fixes"
            ],
            best_practices=[
                "Implement comprehensive logging for all API calls",
                "Use proper timeout values for all requests",
                "Implement retry logic with exponential backoff",
                "Monitor API rate limits and quotas"
            ],
            common_issues=[
                {
                    "issue": "401 Unauthorized errors",
                    "solution": "Check API token validity and regenerate if necessary",
                    "prevention": "Implement token refresh logic and monitor expiration"
                },
                {
                    "issue": "429 Rate limit exceeded", 
                    "solution": "Implement exponential backoff and reduce request frequency",
                    "prevention": "Monitor API usage and implement request queuing"
                },
                {
                    "issue": "Timeout errors on large requests",
                    "solution": "Increase timeout values and implement request chunking",
                    "prevention": "Profile request sizes and optimize data transfer"
                }
            ],
            performance_considerations=[
                "Implement request caching for frequently accessed data",
                "Use batch operations when available",
                "Monitor and optimize request payload sizes"
            ],
            security_guidance=[
                "Never log API tokens or sensitive data",
                "Use environment variables for configuration",
                "Implement proper certificate validation"
            ],
            limitations=[
                "Rate limits vary by endpoint and account type",
                "Some operations require specific permissions",
                "Large datasets may require pagination"
            ],
            related_topics=[
                "API Authentication Best Practices",
                "Performance Optimization Strategies", 
                "Error Handling Patterns"
            ],
            documentation=[
                {
                    "title": "Troubleshooting Common Issues",
                    "url": "https://docs.liveramp.com/troubleshooting",
                    "type": "official"
                }
            ],
            validation_status="verified"
        )
    
    def _generate_explanation_response(self, query: str, context: Optional[Dict] = None) -> TechnicalResponse:
        """Generate technical explanation response"""
        
        return TechnicalResponse(
            type="explanation",
            title="Technical Explanation",
            summary=f"Technical explanation for: {query}",
            code_examples=[],
            api_methods=[],
            implementation_steps=[
                "This is a general technical explanation",
                "For specific implementation guidance, please provide more context",
                "Consider referencing our API documentation for detailed examples"
            ],
            best_practices=[
                "Follow LiveRamp API best practices",
                "Implement proper error handling",
                "Use appropriate authentication methods"
            ],
            common_issues=[],
            performance_considerations=[],
            security_guidance=[],
            limitations=[
                "This is a general response - specific implementations may vary"
            ],
            related_topics=[],
            documentation=[
                {
                    "title": "LiveRamp API Documentation",
                    "url": "https://docs.liveramp.com",
                    "type": "official"
                }
            ],
            validation_status="needs_verification"
        )
    
    def _generate_generic_api_response(self, query: str) -> TechnicalResponse:
        """Generate generic API response when no specific method is found"""
        
        return TechnicalResponse(
            type="api_method",
            title="API Method Information",
            summary=f"Information about LiveRamp API methods related to: {query}",
            code_examples=[],
            api_methods=[],
            implementation_steps=[
                "Identify the specific API method you need",
                "Review the API documentation",
                "Set up authentication",
                "Implement with proper error handling"
            ],
            best_practices=[
                "Use official SDK when available",
                "Implement retry logic for transient failures",
                "Monitor API usage and performance"
            ],
            common_issues=[],
            performance_considerations=[],
            security_guidance=[],
            limitations=[],
            related_topics=[],
            documentation=[
                {
                    "title": "LiveRamp API Documentation",
                    "url": "https://docs.liveramp.com",
                    "type": "official"
                }
            ],
            validation_status="needs_verification"
        )

# Flask application setup
app = Flask(__name__)
CORS(app)

# Initialize technical expert engine
technical_engine = TechnicalExpertEngine()

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "technical_expert_api"})

@app.route('/api/technical-expert/query', methods=['POST'])
def handle_technical_query():
    """Handle technical expert queries"""
    data = request.get_json()
    
    query = data.get('query', '')
    context = data.get('context', {})
    
    if not query:
        return jsonify({"error": "Query is required"}), 400
    
    try:
        response = technical_engine.generate_technical_response(query, context)
        return jsonify(asdict(response))
    except Exception as e:
        logger.error(f"Error generating technical response: {e}")
        return jsonify({"error": "Failed to generate response"}), 500

@app.route('/api/technical-expert/api-methods', methods=['GET'])
def list_api_methods():
    """List available API methods"""
    methods = []
    for method_key, method_data in technical_engine.api_methods.items():
        methods.append({
            "key": method_key,
            "name": method_data["name"],
            "endpoint": method_data["endpoint"],
            "method": method_data["method"],
            "description": method_data["description"]
        })
    
    return jsonify(methods)

@app.route('/api/technical-expert/api-methods/<method_key>', methods=['GET'])
def get_api_method_details(method_key):
    """Get detailed information about a specific API method"""
    method_data = technical_engine.api_methods.get(method_key)
    
    if not method_data:
        return jsonify({"error": "API method not found"}), 404
    
    return jsonify(method_data)

@app.route('/api/technical-context', methods=['GET'])
def get_technical_context():
    """Get technical context for the chat mode"""
    return jsonify({
        "availableTools": list(technical_engine.api_methods.keys()),
        "apiVersion": "2.0",
        "limitations": [
            "API documentation is based on current version",
            "Code examples may need adaptation for specific use cases",
            "Rate limits apply to all API endpoints"
        ],
        "recentChanges": [
            "Added comprehensive error handling examples",
            "Updated authentication documentation",
            "Enhanced code examples with best practices"
        ],
        "capabilityMatrix": {
            "identity_resolution": True,
            "audience_segmentation": True,
            "lookalike_modeling": True,
            "cross_platform_attribution": True,
            "secure_data_collaboration": True
        },
        "documentationVersion": "2.0.1",
        "integrationPatterns": [
            "REST API integration",
            "Batch file processing",
            "Real-time streaming"
        ]
    })

if __name__ == '__main__':
    app.run(debug=True, port=5002)