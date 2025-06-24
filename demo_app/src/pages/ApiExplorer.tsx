import React, { useState, useEffect } from 'react';
import './ApiExplorer.css';

interface ApiEndpoint {
  name: string;
  method: 'GET' | 'POST' | 'PUT' | 'DELETE';
  path: string;
  description: string;
  category: 'MCP Tools' | 'Enhanced Features' | 'Habu API' | 'System';
  requiresAuth: boolean;
  enhanced?: boolean;
  parameters?: Array<{
    name: string;
    type: string;
    required: boolean;
    description: string;
    defaultValue?: string;
  }>;
}

interface ApiResponse {
  status: number;
  data: any;
  headers: Record<string, string>;
  responseTime: number;
  timestamp: Date;
}

const ApiExplorer: React.FC = () => {
  const [selectedEndpoint, setSelectedEndpoint] = useState<ApiEndpoint | null>(null);
  const [parameters, setParameters] = useState<Record<string, string>>({});
  const [response, setResponse] = useState<ApiResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [authStatus, setAuthStatus] = useState<'unknown' | 'valid' | 'invalid'>('unknown');

  const endpoints: ApiEndpoint[] = [
    // Enhanced Chat Interface
    {
      name: 'Enhanced Chat',
      method: 'POST',
      path: '/api/enhanced-chat',
      description: 'AI-powered chat with MCP tool integration and GPT-4 intelligence',
      category: 'MCP Tools',
      requiresAuth: false,
      parameters: [
        {
          name: 'user_input',
          type: 'string',
          required: true,
          description: 'Natural language request for data analytics',
          defaultValue: 'Show me my data partners'
        }
      ]
    },
    // Direct MCP Tool Endpoints
    {
      name: 'List Partners',
      method: 'GET',
      path: '/api/mcp/habu_list_partners',
      description: 'Direct endpoint to list available data partnership partners',
      category: 'MCP Tools',
      requiresAuth: false
    },
    {
      name: 'List Templates',
      method: 'GET',
      path: '/api/mcp/habu_list_templates',
      description: 'Direct endpoint to get available analytics templates (basic version)',
      category: 'MCP Tools',
      requiresAuth: false
    },
    {
      name: 'Enhanced Templates',
      method: 'GET',
      path: '/api/mcp/habu_enhanced_templates',
      description: 'Rich template metadata with categories, parameters, data types, and status',
      category: 'Enhanced Features',
      requiresAuth: false,
      enhanced: true,
      parameters: [
        {
          name: 'cleanroom_id',
          type: 'string',
          required: false,
          description: 'Optional specific cleanroom ID to get templates for',
          defaultValue: ''
        }
      ]
    },
    {
      name: 'Submit Query',
      method: 'POST',
      path: '/api/mcp/habu_submit_query',
      description: 'Direct endpoint to submit analytics query',
      category: 'MCP Tools',
      requiresAuth: false,
      parameters: [
        {
          name: 'template_id',
          type: 'string',
          required: true,
          description: 'Template ID for the analytics query',
          defaultValue: 'audience-overlap'
        },
        {
          name: 'parameters',
          type: 'object',
          required: false,
          description: 'Query parameters as JSON object',
          defaultValue: '{}'
        }
      ]
    },
    {
      name: 'Check Status',
      method: 'GET',
      path: '/api/mcp/habu_check_status',
      description: 'Check the status of a submitted query',
      category: 'MCP Tools',
      requiresAuth: false,
      parameters: [
        {
          name: 'query_id',
          type: 'string',
          required: true,
          description: 'Query ID to check status for',
          defaultValue: 'query_123'
        }
      ]
    },
    {
      name: 'Get Results',
      method: 'GET',
      path: '/api/mcp/habu_get_results',
      description: 'Get results from a completed query',
      category: 'MCP Tools',
      requiresAuth: false,
      parameters: [
        {
          name: 'query_id',
          type: 'string',
          required: true,
          description: 'Query ID to get results for',
          defaultValue: 'query_123'
        }
      ]
    },
    // System Endpoints
    {
      name: 'API Health Check',
      method: 'GET',
      path: '/api/health',
      description: 'Check API service health and configuration',
      category: 'System',
      requiresAuth: false
    },
    {
      name: 'MCP Server Health',
      method: 'GET',
      path: '/health',
      description: 'Check MCP server health and status',
      category: 'System',
      requiresAuth: false
    },
    // Habu API Integration Testing
    {
      name: 'Test Real API Connection',
      method: 'POST',
      path: '/api/enhanced-chat',
      description: 'Test connection to Habu API and validate authentication',
      category: 'Habu API',
      requiresAuth: false,
      parameters: [
        {
          name: 'user_input',
          type: 'string',
          required: true,
          description: 'Request to test API connectivity',
          defaultValue: 'Test my connection to the Habu API and show me what cleanrooms I have access to'
        }
      ]
    },
    {
      name: 'Query Template Status',
      method: 'POST',
      path: '/api/enhanced-chat',
      description: 'Check which analytics templates are ready to use',
      category: 'Habu API',
      requiresAuth: false,
      parameters: [
        {
          name: 'user_input',
          type: 'string',
          required: true,
          description: 'Request to check template availability',
          defaultValue: 'Which analytics templates are ready to run right now?'
        }
      ]
    },
    // Enhanced Features Testing
    {
      name: 'Test Enhanced vs Basic Templates',
      method: 'POST',
      path: '/api/enhanced-chat',
      description: 'Compare enhanced template features vs basic templates',
      category: 'Enhanced Features',
      requiresAuth: false,
      enhanced: true,
      parameters: [
        {
          name: 'user_input',
          type: 'string',
          required: true,
          description: 'Request to demonstrate enhanced template capabilities',
          defaultValue: 'Show me the templates with their categories, parameters, and data types - demonstrate the enhanced features'
        }
      ]
    },
    {
      name: 'Template Enhancement Demo',
      method: 'POST',
      path: '/api/enhanced-chat',
      description: 'Demonstrate the 50% richer template metadata in AI responses',
      category: 'Enhanced Features',
      requiresAuth: false,
      enhanced: true,
      parameters: [
        {
          name: 'user_input',
          type: 'string',
          required: true,
          description: 'Request to showcase enhanced template intelligence',
          defaultValue: 'Help me understand what data types and parameters each template works with for better query building'
        }
      ]
    }
  ];

  useEffect(() => {
    checkAuthStatus();
  }, []);

  const checkAuthStatus = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL || ''}/api/health`);
      if (response.ok) {
        setAuthStatus('valid');
      } else {
        setAuthStatus('invalid');
      }
    } catch (error) {
      setAuthStatus('invalid');
    }
  };

  const handleEndpointSelect = (endpoint: ApiEndpoint) => {
    setSelectedEndpoint(endpoint);
    setResponse(null);
    
    // Set default parameters
    const defaultParams: Record<string, string> = {};
    endpoint.parameters?.forEach(param => {
      if (param.defaultValue) {
        defaultParams[param.name] = param.defaultValue;
      }
    });
    setParameters(defaultParams);
  };

  const handleParameterChange = (paramName: string, value: string) => {
    setParameters(prev => ({
      ...prev,
      [paramName]: value
    }));
  };

  const executeRequest = async () => {
    if (!selectedEndpoint) return;

    setLoading(true);
    const startTime = Date.now();

    try {
      const baseUrl = selectedEndpoint.category === 'System' && selectedEndpoint.path === '/health' 
        ? 'https://habu-mcp-server-v2.onrender.com'
        : (process.env.REACT_APP_API_URL || '');

      const url = `${baseUrl}${selectedEndpoint.path}`;
      
      const options: RequestInit = {
        method: selectedEndpoint.method,
        headers: {
          'Content-Type': 'application/json',
        }
      };

      if (selectedEndpoint.method !== 'GET' && Object.keys(parameters).length > 0) {
        options.body = JSON.stringify(parameters);
      }

      const response = await fetch(url, options);
      const responseTime = Date.now() - startTime;
      
      const data = await response.json().catch(() => response.text());
      
      const headers: Record<string, string> = {};
      response.headers.forEach((value, key) => {
        headers[key] = value;
      });

      setResponse({
        status: response.status,
        data,
        headers,
        responseTime,
        timestamp: new Date()
      });

    } catch (error) {
      const responseTime = Date.now() - startTime;
      setResponse({
        status: 0,
        data: { error: error instanceof Error ? error.message : 'Unknown error' },
        headers: {},
        responseTime,
        timestamp: new Date()
      });
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status: number) => {
    if (status >= 200 && status < 300) return '#48bb78';
    if (status >= 300 && status < 400) return '#ed8936';
    if (status >= 400) return '#f56565';
    return '#a0aec0';
  };

  const getCategoryColor = (category: string) => {
    switch (category) {
      case 'MCP Tools': return '#4c51bf';
      case 'Enhanced Features': return '#4299e1';
      case 'Habu API': return '#38b2ac';
      case 'System': return '#48bb78';
      default: return '#a0aec0';
    }
  };

  return (
    <div className="api-explorer">
      <div className="explorer-header">
        <h1>🔧 API Explorer</h1>
        <p>Interactive testing and debugging tool for Habu Clean Room APIs</p>
        
        <div className="auth-status">
          <span className={`status-indicator ${authStatus}`}>
            {authStatus === 'valid' ? '🟢' : authStatus === 'invalid' ? '🔴' : '🟡'}
          </span>
          <span>API Connection: {authStatus.toUpperCase()}</span>
        </div>
      </div>

      <div className="explorer-content">
        {/* Endpoint List */}
        <div className="endpoints-panel">
          <h3>Available Endpoints</h3>
          <div className="endpoints-list">
            {['MCP Tools', 'Enhanced Features', 'System', 'Habu API'].map(category => (
              <div key={category} className="endpoint-category">
                <h4 className="category-header" style={{ color: getCategoryColor(category) }}>
                  {category}
                </h4>
                {endpoints
                  .filter(endpoint => endpoint.category === category)
                  .map((endpoint, index) => (
                    <div
                      key={index}
                      className={`endpoint-item ${selectedEndpoint === endpoint ? 'selected' : ''} ${endpoint.enhanced ? 'enhanced' : ''}`}
                      onClick={() => handleEndpointSelect(endpoint)}
                    >
                      <div className="endpoint-method">{endpoint.method}</div>
                      <div className="endpoint-info">
                        <div className="endpoint-name">
                          {endpoint.name}
                          {endpoint.enhanced && <span className="enhanced-badge">🆕</span>}
                        </div>
                        <div className="endpoint-path">{endpoint.path}</div>
                        <div className="endpoint-description">{endpoint.description}</div>
                      </div>
                      {endpoint.requiresAuth && (
                        <div className="auth-required">🔐</div>
                      )}
                    </div>
                  ))}
              </div>
            ))}
          </div>
        </div>

        {/* Request Panel */}
        <div className="request-panel">
          {selectedEndpoint ? (
            <>
              <div className="request-header">
                <h3>
                  <span className="method-badge" style={{ backgroundColor: getCategoryColor(selectedEndpoint.category) }}>
                    {selectedEndpoint.method}
                  </span>
                  {selectedEndpoint.name}
                </h3>
                <button 
                  className="execute-btn"
                  onClick={executeRequest}
                  disabled={loading}
                >
                  {loading ? '⏳ Executing...' : '▶️ Execute'}
                </button>
              </div>

              {selectedEndpoint.parameters && selectedEndpoint.parameters.length > 0 && (
                <div className="parameters-section">
                  <h4>Parameters</h4>
                  {selectedEndpoint.parameters.map((param, index) => (
                    <div key={index} className="parameter-input">
                      <label>
                        {param.name}
                        {param.required && <span className="required">*</span>}
                        <span className="param-type">({param.type})</span>
                      </label>
                      <textarea
                        value={parameters[param.name] || ''}
                        onChange={(e) => handleParameterChange(param.name, e.target.value)}
                        placeholder={param.description}
                        rows={param.name === 'user_input' ? 3 : 1}
                      />
                      <div className="param-description">{param.description}</div>
                    </div>
                  ))}
                </div>
              )}

              {response && (
                <div className="response-section">
                  <div className="response-header">
                    <h4>Response</h4>
                    <div className="response-meta">
                      <span 
                        className="status-code"
                        style={{ color: getStatusColor(response.status) }}
                      >
                        {response.status}
                      </span>
                      <span className="response-time">{response.responseTime}ms</span>
                      <span className="timestamp">{response.timestamp.toLocaleTimeString()}</span>
                    </div>
                  </div>
                  
                  <div className="response-content">
                    <pre>{JSON.stringify(response.data, null, 2)}</pre>
                  </div>

                  {Object.keys(response.headers).length > 0 && (
                    <details className="response-headers">
                      <summary>Response Headers</summary>
                      <pre>{JSON.stringify(response.headers, null, 2)}</pre>
                    </details>
                  )}
                </div>
              )}
            </>
          ) : (
            <div className="no-selection">
              <h3>Select an endpoint to get started</h3>
              <p>Choose an API endpoint from the list to test and explore its functionality.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ApiExplorer;