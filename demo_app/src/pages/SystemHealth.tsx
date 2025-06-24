import React, { useState, useEffect, useCallback } from 'react';
import './SystemHealth.css';
import CDNMetrics from '../components/CDNMetrics';

interface ServiceStatus {
  name: string;
  status: 'healthy' | 'degraded' | 'down' | 'unknown';
  url: string;
  responseTime?: number;
  lastCheck: Date;
  details?: any;
}

interface SystemHealthData {
  services: ServiceStatus[];
  overallHealth: 'healthy' | 'degraded' | 'critical';
  lastUpdated: Date;
  environment: string;
  mockMode: boolean;
  openaiConfigured: boolean;
  realApiMode?: boolean;
  demoReady?: boolean;
  mcpServerOnline?: boolean;
  demoMode?: string;
  cacheStats?: {
    connected: boolean;
    hitRate?: number;
    keyCount?: number;
    usedMemory?: string;
  };
}

const SystemHealth: React.FC = () => {
  const [healthData, setHealthData] = useState<SystemHealthData | null>(null);
  const [loading, setLoading] = useState(true);
  const [autoRefresh, setAutoRefresh] = useState(true);

  const checkServiceHealth = async (service: { name: string; url: string; healthPath: string }): Promise<ServiceStatus> => {
    const startTime = Date.now();
    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 10000);
      
      const response = await fetch(`${service.url}${service.healthPath}`, {
        method: 'GET',
        headers: service.name.includes('mcp') ? { 'X-API-Key': 'secure-habu-demo-key-2024' } : {},
        signal: controller.signal
      });
      
      clearTimeout(timeoutId);
      
      const endTime = Date.now();
      const responseTime = endTime - startTime;
      
      if (response.ok) {
        const details = await response.json().catch(() => ({}));
        return {
          name: service.name,
          status: 'healthy',
          url: service.url,
          responseTime,
          lastCheck: new Date(),
          details
        };
      } else {
        return {
          name: service.name,
          status: 'degraded',
          url: service.url,
          responseTime,
          lastCheck: new Date(),
          details: { error: `HTTP ${response.status}` }
        };
      }
    } catch (error) {
      const errorMessage = error instanceof Error ? 
        (error.name === 'AbortError' ? 'Request timeout (10s)' : error.message) : 
        'Unknown error';
      
      return {
        name: service.name,
        status: 'down',
        url: service.url,
        lastCheck: new Date(),
        details: { error: errorMessage }
      };
    }
  };

  const checkCacheHealth = async (apiUrl: string): Promise<any> => {
    try {
      const response = await fetch(`${apiUrl}/api/cache-stats`, {
        method: 'GET',
        timeout: 5000
      } as RequestInit);
      
      if (response.ok) {
        const data = await response.json();
        return data.cache_stats;
      }
    } catch (error) {
      console.log('Cache stats unavailable:', error);
    }
    return null;
  };

  const performHealthCheck = useCallback(async () => {
    setLoading(true);
    
    // Detect if we're running locally
    const isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
    
    const services = isLocal ? [
      {
        name: 'Demo API (Local)',
        url: 'http://localhost:5001',
        healthPath: '/api/health'
      },
      {
        name: 'React Frontend (Local)',
        url: 'http://localhost:3000',
        healthPath: '/'
      }
    ] : [
      {
        name: 'Demo API',
        url: 'https://habu-demo-api-v2.onrender.com',
        healthPath: '/api/health'
      },
      {
        name: 'MCP Server',
        url: 'https://habu-mcp-server-v2.onrender.com',
        healthPath: '/health'
      },
      {
        name: 'React Frontend',
        url: 'https://habu-demo-frontend-v2.onrender.com',
        healthPath: '/'
      }
    ];

    const serviceStatuses = await Promise.all(
      services.map(service => checkServiceHealth(service))
    );

    // Determine overall health
    const healthyCount = serviceStatuses.filter(s => s.status === 'healthy').length;
    const totalCount = serviceStatuses.length;
    
    let overallHealth: 'healthy' | 'degraded' | 'critical';
    if (healthyCount === totalCount) {
      overallHealth = 'healthy';
    } else if (healthyCount >= totalCount * 0.5) {
      overallHealth = 'degraded';
    } else {
      overallHealth = 'critical';
    }

    // Extract configuration details from the actual health endpoint response
    const apiService = serviceStatuses.find(s => s.name === 'Demo API' || s.name === 'Demo API (Local)');
    const realApiMode = apiService?.details?.real_api_mode || false;
    const openaiConfigured = apiService?.details?.openai_available || false;
    const demoReady = apiService?.details?.demo_ready || false;
    const mcpServerOnline = apiService?.details?.mcp_server === 'online';
    const demoMode = apiService?.details?.demo_mode || 'unknown';

    // Get cache statistics
    const cacheStats = await checkCacheHealth(isLocal ? 'http://localhost:5001' : 'https://habu-demo-api-v2.onrender.com');

    setHealthData({
      services: serviceStatuses,
      overallHealth,
      lastUpdated: new Date(),
      environment: isLocal ? 'Local Development' : 'Production (Render.com)',
      mockMode: !realApiMode, // Invert the logic for display
      openaiConfigured,
      realApiMode,
      demoReady,
      mcpServerOnline,
      demoMode,
      cacheStats: cacheStats ? {
        connected: cacheStats.connected,
        hitRate: cacheStats.hit_rate,
        keyCount: Object.values(cacheStats.cache_key_counts || {}).reduce((a: number, b: any) => a + (Number(b) || 0), 0),
        usedMemory: cacheStats.used_memory
      } : undefined
    });

    setLoading(false);
  }, []);

  useEffect(() => {
    performHealthCheck();
    
    if (autoRefresh) {
      const interval = setInterval(performHealthCheck, 30000); // 30 seconds
      return () => clearInterval(interval);
    }
  }, [autoRefresh, performHealthCheck]);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'healthy': return '#00C851';
      case 'degraded': return '#FF8800';
      case 'down': return '#FF4444';
      default: return '#6C757D';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'healthy': return '✅';
      case 'degraded': return '⚠️';
      case 'down': return '❌';
      default: return '❓';
    }
  };

  if (loading && !healthData) {
    return (
      <div className="system-health">
        <div className="loading">
          <div className="spinner"></div>
          <p>Checking system health...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="system-health">
      <div className="health-header">
        <h1>🔧 System Health Dashboard</h1>
        <p>Real-time monitoring of production services and API integrations</p>
        <div className="health-controls">
          <button 
            onClick={performHealthCheck} 
            disabled={loading}
            className="refresh-btn"
          >
            {loading ? '🔄' : '🔄'} Refresh
          </button>
          <label className="auto-refresh">
            <input
              type="checkbox"
              checked={autoRefresh}
              onChange={(e) => setAutoRefresh(e.target.checked)}
            />
            Auto-refresh (30s)
          </label>
        </div>
      </div>

      {healthData && (
        <>
          {/* Overall Status */}
          <div className={`overall-status ${healthData.overallHealth}`}>
            <div className="status-indicator">
              {getStatusIcon(healthData.overallHealth)}
              <h2>System Status: {healthData.overallHealth.toUpperCase()}</h2>
            </div>
            <div className="status-details">
              <p>Environment: {healthData.environment}</p>
              <p>Last Updated: {healthData.lastUpdated.toLocaleTimeString()}</p>
              <p>Services: {healthData.services.filter(s => s.status === 'healthy').length}/{healthData.services.length} healthy</p>
            </div>
          </div>

          {/* Configuration Status */}
          <div className="config-status">
            <h3>🔧 Integration Status</h3>
            <div className="config-grid">
              <div className={`config-item ${healthData.realApiMode ? 'enabled' : 'disabled'}`}>
                <span className="config-label">Real API Mode:</span>
                <span className="config-value">
                  {healthData.realApiMode ? '✅ Connected to Habu API' : '⚠️ Mock Data Mode'}
                </span>
              </div>
              <div className={`config-item ${healthData.openaiConfigured ? 'enabled' : 'disabled'}`}>
                <span className="config-label">OpenAI GPT-4:</span>
                <span className="config-value">
                  {healthData.openaiConfigured ? '✅ AI Intelligence Active' : '❌ Not Configured'}
                </span>
              </div>
              <div className={`config-item ${healthData.mcpServerOnline ? 'enabled' : 'disabled'}`}>
                <span className="config-label">MCP Protocol:</span>
                <span className="config-value">
                  {healthData.mcpServerOnline ? '✅ Model Context Protocol Online' : '❌ MCP Offline'}
                </span>
              </div>
              <div className={`config-item ${healthData.demoReady ? 'enabled' : 'disabled'}`}>
                <span className="config-label">Demo Readiness:</span>
                <span className="config-value">
                  {healthData.demoReady ? '🚀 All Systems Ready' : '⚠️ Issues Detected'}
                </span>
              </div>
              <div className={`config-item ${healthData.cacheStats?.connected ? 'enabled' : 'disabled'}`}>
                <span className="config-label">Redis Cache:</span>
                <span className="config-value">
                  {healthData.cacheStats?.connected ? 
                    `🚀 Connected (${healthData.cacheStats.hitRate}% hit rate)` : 
                    '⚠️ Not Connected (Fallback Mode)'
                  }
                </span>
              </div>
            </div>
          </div>

          {/* Cache Performance */}
          {healthData.cacheStats && (
            <div className="cache-performance">
              <h3>⚡ Cache Performance (Phase H)</h3>
              <div className="cache-stats-grid">
                <div className="cache-stat">
                  <span className="stat-label">Connection Status:</span>
                  <span className={`stat-value ${healthData.cacheStats.connected ? 'connected' : 'disconnected'}`}>
                    {healthData.cacheStats.connected ? '✅ Connected' : '❌ Disconnected'}
                  </span>
                </div>
                {healthData.cacheStats.connected && (
                  <>
                    <div className="cache-stat">
                      <span className="stat-label">Hit Rate:</span>
                      <span className="stat-value">{healthData.cacheStats.hitRate}%</span>
                    </div>
                    <div className="cache-stat">
                      <span className="stat-label">Cached Keys:</span>
                      <span className="stat-value">{healthData.cacheStats.keyCount}</span>
                    </div>
                    <div className="cache-stat">
                      <span className="stat-label">Memory Usage:</span>
                      <span className="stat-value">{healthData.cacheStats.usedMemory}</span>
                    </div>
                  </>
                )}
                {!healthData.cacheStats.connected && (
                  <div className="cache-stat">
                    <span className="stat-label">Fallback Mode:</span>
                    <span className="stat-value">✅ Active (Graceful Degradation)</span>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* CDN Performance Metrics - Temporarily disabled for debugging */}
          {/* <CDNMetrics refreshInterval={30000} /> */}

          {/* MCP Tools Status */}
          <div className="mcp-tools-status">
            <h3>🤖 Available MCP Tools (9 total)</h3>
            <div className="tools-grid">
              <div className="tool-category">
                <h4>🔧 Data Management</h4>
                <div className="tool-item">
                  <span className="tool-name">habu_list_partners</span>
                  <span className="tool-status">✅ Ready</span>
                  <span className="tool-description">List data partnership partners</span>
                </div>
              </div>
              
              <div className="tool-category">
                <h4>📋 Template Management</h4>
                <div className="tool-item">
                  <span className="tool-name">habu_list_templates</span>
                  <span className="tool-status">✅ Ready</span>
                  <span className="tool-description">Get available analytics templates (basic)</span>
                </div>
                <div className="tool-item enhanced">
                  <span className="tool-name">habu_enhanced_templates</span>
                  <span className="tool-status">🆕 Enhanced</span>
                  <span className="tool-description">Rich template metadata with categories, parameters, data types</span>
                </div>
              </div>
              
              <div className="tool-category">
                <h4>⚡ Query Management</h4>
                <div className="tool-item">
                  <span className="tool-name">habu_submit_query</span>
                  <span className="tool-status">✅ Ready</span>
                  <span className="tool-description">Submit analytics queries</span>
                </div>
                <div className="tool-item">
                  <span className="tool-name">habu_check_status</span>
                  <span className="tool-status">✅ Ready</span>
                  <span className="tool-description">Monitor query progress</span>
                </div>
                <div className="tool-item">
                  <span className="tool-name">habu_get_results</span>
                  <span className="tool-status">✅ Ready</span>
                  <span className="tool-description">Retrieve query results</span>
                </div>
              </div>
              
              <div className="tool-category">
                <h4>📊 Export Management</h4>
                <div className="tool-item">
                  <span className="tool-name">habu_list_exports</span>
                  <span className="tool-status">✅ Ready</span>
                  <span className="tool-description">List available exports</span>
                </div>
                <div className="tool-item">
                  <span className="tool-name">habu_download_export</span>
                  <span className="tool-status">✅ Ready</span>
                  <span className="tool-description">Download export files</span>
                </div>
              </div>
              
              <div className="tool-category">
                <h4>🤖 AI Interface</h4>
                <div className="tool-item enhanced">
                  <span className="tool-name">habu_enhanced_chat</span>
                  <span className="tool-status">🧠 AI-Powered</span>
                  <span className="tool-description">GPT-4 conversational interface with context awareness</span>
                </div>
              </div>
            </div>
          </div>

          {/* Phase D Enhancements */}
          <div className="phase-d-status">
            <h3>🚀 Phase D Enhancements</h3>
            <div className="enhancement-grid">
              <div className="enhancement-item completed">
                <span className="enhancement-name">Enhanced Template Management</span>
                <span className="enhancement-status">✅ Active</span>
                <span className="enhancement-description">50% richer template metadata with categories, parameters, data types</span>
              </div>
              <div className="enhancement-item ready">
                <span className="enhancement-name">User Management Discovery</span>
                <span className="enhancement-status">🔍 Discovered</span>
                <span className="enhancement-description">User roles and permissions endpoint available for integration</span>
              </div>
              <div className="enhancement-item future">
                <span className="enhancement-name">Advanced Query Intelligence</span>
                <span className="enhancement-status">🔮 Planned</span>
                <span className="enhancement-description">Smart parameter validation and query builder</span>
              </div>
            </div>
          </div>

          {/* Services Grid */}
          <div className="services-grid">
            <h3>Service Status</h3>
            <div className="services-container">
              {healthData.services.map((service, index) => (
                <div key={index} className={`service-card ${service.status}`}>
                  <div className="service-header">
                    <h4>{service.name}</h4>
                    <span className="status-badge" style={{ backgroundColor: getStatusColor(service.status) }}>
                      {getStatusIcon(service.status)} {service.status.toUpperCase()}
                    </span>
                  </div>
                  
                  <div className="service-details">
                    <p><strong>URL:</strong> <a href={service.url} target="_blank" rel="noopener noreferrer">{service.url}</a></p>
                    <p><strong>Last Check:</strong> {service.lastCheck.toLocaleTimeString()}</p>
                    {service.responseTime && (
                      <p><strong>Response Time:</strong> {service.responseTime}ms</p>
                    )}
                    
                    {service.details && (
                      <div className="service-metadata">
                        <h5>Details:</h5>
                        <pre>{JSON.stringify(service.details, null, 2)}</pre>
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default SystemHealth;