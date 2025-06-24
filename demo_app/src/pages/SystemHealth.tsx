import React, { useState, useEffect } from 'react';
import './SystemHealth.css';

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
}

const SystemHealth: React.FC = () => {
  const [healthData, setHealthData] = useState<SystemHealthData | null>(null);
  const [loading, setLoading] = useState(true);
  const [autoRefresh, setAutoRefresh] = useState(true);

  const checkServiceHealth = async (service: { name: string; url: string; healthPath: string }): Promise<ServiceStatus> => {
    const startTime = Date.now();
    try {
      const response = await fetch(`${service.url}${service.healthPath}`, {
        method: 'GET',
        headers: service.name.includes('mcp') ? { 'X-API-Key': 'secure-habu-demo-key-2024' } : {},
        timeout: 10000
      });
      
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
      return {
        name: service.name,
        status: 'down',
        url: service.url,
        lastCheck: new Date(),
        details: { error: error instanceof Error ? error.message : 'Unknown error' }
      };
    }
  };

  const performHealthCheck = async () => {
    setLoading(true);
    
    const services = [
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
      },
      {
        name: 'Admin App',
        url: 'https://habu-admin-app-v2.onrender.com',
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

    // Extract configuration details
    const apiService = serviceStatuses.find(s => s.name === 'Demo API');
    const mockMode = apiService?.details?.mock_mode || false;
    const openaiConfigured = apiService?.details?.openai_configured || false;

    setHealthData({
      services: serviceStatuses,
      overallHealth,
      lastUpdated: new Date(),
      environment: 'Production (Render.com)',
      mockMode,
      openaiConfigured
    });

    setLoading(false);
  };

  useEffect(() => {
    performHealthCheck();
    
    if (autoRefresh) {
      const interval = setInterval(performHealthCheck, 30000); // 30 seconds
      return () => clearInterval(interval);
    }
  }, [autoRefresh]);

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
        <h1>System Health Dashboard</h1>
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
            <h3>Configuration Status</h3>
            <div className="config-grid">
              <div className={`config-item ${healthData.mockMode ? 'enabled' : 'disabled'}`}>
                <span className="config-label">Mock Data Mode:</span>
                <span className="config-value">
                  {healthData.mockMode ? '✅ Enabled' : '❌ Disabled'}
                </span>
              </div>
              <div className={`config-item ${healthData.openaiConfigured ? 'enabled' : 'disabled'}`}>
                <span className="config-label">OpenAI Integration:</span>
                <span className="config-value">
                  {healthData.openaiConfigured ? '✅ Configured' : '❌ Not Configured'}
                </span>
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