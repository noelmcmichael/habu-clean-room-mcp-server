import React, { useState, useEffect } from 'react';

interface SystemStatus {
  mcpServer: 'online' | 'offline' | 'checking';
  apiConnection: 'connected' | 'disconnected' | 'checking';
  aiPowered: 'active' | 'fallback' | 'checking';
  cleanroomData: 'live' | 'mock' | 'checking';
}

interface DemoStatusIndicatorsProps {
  isCollapsed?: boolean;
  onToggle?: () => void;
}

const DemoStatusIndicators: React.FC<DemoStatusIndicatorsProps> = ({ 
  isCollapsed = false, 
  onToggle 
}) => {
  const [systemStatus, setSystemStatus] = useState<SystemStatus>({
    mcpServer: 'checking',
    apiConnection: 'checking',
    aiPowered: 'checking',
    cleanroomData: 'checking'
  });

  const [lastUpdate, setLastUpdate] = useState<Date>(new Date());

  useEffect(() => {
    checkSystemStatus();
    const interval = setInterval(checkSystemStatus, 30000); // Check every 30 seconds
    return () => clearInterval(interval);
  }, []);

  const checkSystemStatus = async () => {
    try {
      const apiUrl = process.env.REACT_APP_API_URL || '';
      
      // Check API health
      const healthResponse = await fetch(`${apiUrl}/api/health`, {
        method: 'GET',
        timeout: 5000
      } as any);
      
      if (healthResponse.ok) {
        const healthData = await healthResponse.json();
        
        setSystemStatus({
          mcpServer: healthData.mcp_server === 'online' ? 'online' : 'offline',
          apiConnection: 'connected',
          aiPowered: healthData.openai_available ? 'active' : 'fallback',
          cleanroomData: healthData.real_api_mode ? 'live' : 'mock'
        });
      } else {
        setSystemStatus({
          mcpServer: 'offline',
          apiConnection: 'disconnected',
          aiPowered: 'fallback',
          cleanroomData: 'mock'
        });
      }
    } catch (error) {
      console.error('Status check failed:', error);
      setSystemStatus({
        mcpServer: 'offline',
        apiConnection: 'disconnected',
        aiPowered: 'fallback',
        cleanroomData: 'mock'
      });
    }
    
    setLastUpdate(new Date());
  };

  const getStatusIcon = (status: string): string => {
    switch (status) {
      case 'online':
      case 'connected':
      case 'active':
      case 'live':
        return '🟢';
      case 'offline':
      case 'disconnected':
      case 'fallback':
      case 'mock':
        return '🟡';
      case 'checking':
      default:
        return '🔄';
    }
  };

  const getStatusText = (component: keyof SystemStatus): string => {
    const status = systemStatus[component];
    switch (component) {
      case 'mcpServer':
        return status === 'online' ? 'MCP Server Online' : 
               status === 'offline' ? 'MCP Server Offline' : 'Checking MCP...';
      case 'apiConnection':
        return status === 'connected' ? 'API Connected' : 
               status === 'disconnected' ? 'API Disconnected' : 'Checking API...';
      case 'aiPowered':
        return status === 'active' ? 'AI-Powered (GPT-4)' : 
               status === 'fallback' ? 'Rule-based Fallback' : 'Checking AI...';
      case 'cleanroomData':
        return status === 'live' ? 'Live Cleanroom Data' : 
               status === 'mock' ? 'Mock Data Mode' : 'Checking Data...';
      default:
        return 'Unknown';
    }
  };

  const getOverallStatus = (): 'excellent' | 'good' | 'degraded' | 'checking' => {
    const { mcpServer, apiConnection, aiPowered, cleanroomData } = systemStatus;
    
    if ([mcpServer, apiConnection, aiPowered, cleanroomData].some(s => s === 'checking')) {
      return 'checking';
    }
    
    if (mcpServer === 'online' && apiConnection === 'connected' && 
        aiPowered === 'active' && cleanroomData === 'live') {
      return 'excellent';
    }
    
    if (mcpServer === 'online' && apiConnection === 'connected') {
      return 'good';
    }
    
    return 'degraded';
  };

  const getDemoReadiness = (): string => {
    const overall = getOverallStatus();
    switch (overall) {
      case 'excellent':
        return '🎯 Demo Ready - Full Production Mode';
      case 'good':
        return '✅ Demo Ready - Core Features Available';
      case 'degraded':
        return '⚠️ Limited Functionality';
      case 'checking':
      default:
        return '🔄 Checking Demo Readiness...';
    }
  };

  if (isCollapsed) {
    return (
      <div className="demo-status-collapsed" onClick={onToggle}>
        <span className="overall-status-icon">
          {getOverallStatus() === 'excellent' ? '🎯' : 
           getOverallStatus() === 'good' ? '✅' : 
           getOverallStatus() === 'degraded' ? '⚠️' : '🔄'}
        </span>
        <span className="demo-readiness-text">{getDemoReadiness()}</span>
      </div>
    );
  }

  return (
    <div className="demo-status-indicators">
      <div className="status-header">
        <h3>🎬 Demo System Status</h3>
        <button className="status-collapse" onClick={onToggle}>
          ⬆
        </button>
      </div>

      <div className="demo-readiness">
        <div className="readiness-indicator">
          {getDemoReadiness()}
        </div>
      </div>

      <div className="system-components">
        {Object.entries(systemStatus).map(([component, status]) => (
          <div key={component} className={`component-status ${status}`}>
            <span className="status-icon">
              {getStatusIcon(status)}
            </span>
            <span className="status-text">
              {getStatusText(component as keyof SystemStatus)}
            </span>
          </div>
        ))}
      </div>

      <div className="status-footer">
        <div className="last-update">
          Last checked: {lastUpdate.toLocaleTimeString()}
        </div>
        <button className="refresh-status" onClick={checkSystemStatus}>
          🔄 Refresh
        </button>
      </div>

      <div className="demo-features">
        <h4>🚀 Active Demo Features:</h4>
        <div className="feature-list">
          <div className="feature">
            <span className="feature-icon">🤖</span>
            <span>AI-Powered Chat Agent</span>
          </div>
          <div className="feature">
            <span className="feature-icon">🔧</span>
            <span>Interactive Query Execution</span>
          </div>
          <div className="feature">
            <span className="feature-icon">📊</span>
            <span>Real-Time Analytics</span>
          </div>
          <div className="feature">
            <span className="feature-icon">🏢</span>
            <span>Live Cleanroom Data</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DemoStatusIndicators;