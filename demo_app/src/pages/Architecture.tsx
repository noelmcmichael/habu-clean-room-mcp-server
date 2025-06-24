import React, { useState } from 'react';
import './Architecture.css';

interface ArchitectureComponent {
  id: string;
  name: string;
  type: 'frontend' | 'api' | 'mcp' | 'database' | 'external';
  status: 'healthy' | 'degraded' | 'issue';
  description: string;
  technologies: string[];
  connections: string[];
  url?: string;
  issues?: string[];
}

const Architecture: React.FC = () => {
  const [selectedComponent, setSelectedComponent] = useState<ArchitectureComponent | null>(null);
  const [viewMode, setViewMode] = useState<'overview' | 'data-flow' | 'deployment'>('overview');

  const components: ArchitectureComponent[] = [
    {
      id: 'react-frontend',
      name: 'React Frontend',
      type: 'frontend',
      status: 'healthy',
      description: 'Professional React application with TypeScript, multi-page navigation, and real-time system monitoring.',
      technologies: ['React 18', 'TypeScript', 'React Router', 'CSS3'],
      connections: ['flask-api'],
      url: 'https://habu-demo-frontend-v2.onrender.com',
    },
    {
      id: 'flask-api',
      name: 'Flask API Bridge',
      type: 'api',
      status: 'healthy',
      description: 'Phase H optimized Python Flask API with Redis caching, response compression, and intelligent TTL management. 50-90% performance improvement through caching.',
      technologies: ['Flask', 'Python 3.11', 'Flask-CORS', 'Flask-Compress', 'Redis Cache', 'Asyncio'],
      connections: ['react-frontend', 'enhanced-agent', 'redis-cache', 'cdn-optimization'],
      url: 'https://habu-demo-api-v2.onrender.com',
    },
    {
      id: 'enhanced-agent',
      name: 'Enhanced Chat Agent',
      type: 'api',
      status: 'healthy',
      description: 'OpenAI GPT-4 powered conversational agent with business intelligence, enhanced template processing, and real API integration.',
      technologies: ['OpenAI GPT-4', 'Python', 'AsyncIO', 'Circuit Breaker', 'Context Awareness', 'JSON Actions'],
      connections: ['flask-api', 'mcp-tools', 'openai-api'],
    },
    {
      id: 'mcp-server',
      name: 'MCP Server',
      type: 'mcp',
      status: 'healthy',
      description: 'Phase H enhanced FastMCP 2.0 server with Redis caching support. Implements Model Context Protocol with 8 high-performance Habu Clean Room tools.',
      technologies: ['FastMCP 2.0', 'Starlette', 'Uvicorn', 'PostgreSQL', 'Redis Cache'],
      connections: ['enhanced-agent', 'habu-api', 'postgresql', 'redis-cache'],
      url: 'https://habu-mcp-server-v2.onrender.com/mcp',
    },
    {
      id: 'mcp-tools',
      name: 'MCP Tools (8 Enhanced Tools)',
      type: 'mcp',
      status: 'healthy',
      description: 'Eight specialized tools for LiveRamp Clean Room operations: partners, enhanced templates with AI metadata, queries, status, results, chat agents.',
      technologies: ['Python', 'Async/Await', 'Real API Integration', 'AI Enhancement', 'Business Intelligence'],
      connections: ['mcp-server', 'habu-api'],
    },
    {
      id: 'postgresql',
      name: 'PostgreSQL Database',
      type: 'database',
      status: 'healthy',
      description: 'Production PostgreSQL database for MCP server data persistence and caching.',
      technologies: ['PostgreSQL 16', 'SQLAlchemy', 'AsyncPG', 'Connection Pooling'],
      connections: ['mcp-server', 'admin-app'],
      url: 'Render.com Managed Database',
    },
    {
      id: 'redis-cache',
      name: 'Redis Cache',
      type: 'database',
      status: 'healthy',
      description: 'Phase H Redis cache for high-performance API response caching and session management. Provides 10-100ms response times for cached data.',
      technologies: ['Redis 7', 'In-Memory Cache', 'TTL Management', 'Async Operations'],
      connections: ['flask-api', 'mcp-server'],
      url: 'Render.com Managed Redis',
    },
    {
      id: 'cdn-optimization',
      name: 'CDN Optimization Layer',
      type: 'api',
      status: 'healthy',
      description: 'Phase H1.2 CDN optimization with intelligent caching, compression, ETag support, and performance monitoring. Provides global edge caching and content delivery acceleration.',
      technologies: ['Edge Caching', 'Gzip Compression', 'ETag Validation', 'Content Optimization', 'Performance Analytics'],
      connections: ['flask-api', 'react-frontend'],
      url: 'Integrated CDN System',
    },
    {
      id: 'admin-app',
      name: 'Admin Interface',
      type: 'api',
      status: 'healthy',
      description: 'Flask-based admin interface for database management and system administration.',
      technologies: ['Flask', 'Flask-Login', 'Gunicorn', 'HTML Templates'],
      connections: ['postgresql'],
      url: 'https://habu-admin-app-v2.onrender.com',
    },
    {
      id: 'habu-api',
      name: 'LiveRamp Clean Room API',
      type: 'external',
      status: 'healthy',
      description: 'Official LiveRamp API for clean room data collaboration. Real API integration with intelligent enhancement of sparse data.',
      technologies: ['REST API', 'OAuth2', 'JWT', 'HTTPS', 'AI Enhancement'],
      connections: ['mcp-tools'],
      url: 'https://app.habu.com',
    },
    {
      id: 'openai-api',
      name: 'OpenAI GPT-4 API',
      type: 'external',
      status: 'healthy',
      description: 'OpenAI API providing GPT-4 language model for intelligent conversation and business insights.',
      technologies: ['GPT-4', 'REST API', 'JSON', 'Rate Limiting'],
      connections: ['enhanced-agent'],
      url: 'https://api.openai.com',
    },
    {
      id: 'render-platform',
      name: 'Render.com Platform',
      type: 'external',
      status: 'healthy',
      description: 'Cloud hosting platform running all 5 services with automatic deployments from GitHub.',
      technologies: ['Docker', 'GitHub Integration', 'SSL/TLS', 'Load Balancing'],
      connections: ['react-frontend', 'flask-api', 'mcp-server', 'admin-app', 'postgresql'],
      url: 'https://render.com',
    }
  ];

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'healthy': return '#48bb78';
      case 'degraded': return '#ed8936';
      case 'issue': return '#f56565';
      default: return '#a0aec0';
    }
  };

  const getTypeColor = (type: string) => {
    switch (type) {
      case 'frontend': return '#4c51bf';
      case 'api': return '#38b2ac';
      case 'mcp': return '#9f7aea';
      case 'database': return '#48bb78';
      case 'external': return '#ed8936';
      default: return '#a0aec0';
    }
  };

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'frontend': return '🎨';
      case 'api': return '🔧';
      case 'mcp': return '🤖';
      case 'database': return '🗄️';
      case 'external': return '🌐';
      default: return '📦';
    }
  };

  const dataFlowSteps = [
    {
      step: 1,
      component: 'User Input',
      description: 'User types message in React frontend chat interface',
      tech: 'React ChatInterface Component'
    },
    {
      step: 2,
      component: 'Frontend → API',
      description: 'React sends POST request with user_input parameter',
      tech: 'Fetch API → Flask /api/enhanced-chat'
    },
    {
      step: 3,
      component: 'Flask API Bridge + Redis Cache',
      description: 'Flask checks Redis cache first, validates input, creates async loop if cache miss',
      tech: 'Flask + Redis Cache + AsyncIO Event Loop'
    },
    {
      step: 4,
      component: 'Enhanced Chat Agent',
      description: 'GPT-4 processes request, determines intent, selects appropriate tools',
      tech: 'OpenAI GPT-4 + System Prompt'
    },
    {
      step: 5,
      component: 'Tool Execution',
      description: 'Agent executes MCP tools (partners, enhanced templates, queries, etc.) with real API integration',
      tech: 'Python Tool Functions + Real API + AI Enhancement'
    },
    {
      step: 6,
      component: 'Business Intelligence',
      description: 'GPT-4 analyzes enhanced results with rich metadata, adds business context and actionable recommendations',
      tech: 'GPT-4 Response Generation + Enhanced Template Processing'
    },
    {
      step: 7,
      component: 'Response Assembly + Caching',
      description: 'Flask formats response, caches result in Redis with intelligent TTL, compresses response, returns JSON',
      tech: 'Flask Response Formatting + Redis Caching + Compression'
    },
    {
      step: 8,
      component: 'Frontend Display',
      description: 'React receives response, formats message, updates chat interface',
      tech: 'React State Management + UI Update'
    }
  ];

  const deploymentInfo = {
    platform: 'Render.com Pro Tier',
    services: 5,
    database: 'PostgreSQL 16 + Redis 7',
    deployment: 'GitHub → Render (Automatic)',
    domains: [
      'habu-demo-frontend-v2.onrender.com',
      'habu-demo-api-v2.onrender.com', 
      'habu-mcp-server-v2.onrender.com',
      'habu-admin-app-v2.onrender.com'
    ],
    environment: 'Production (Phase H Optimized)',
    monitoring: 'Built-in Health Checks + Redis Monitoring',
    ssl: 'Automatic SSL/TLS',
    scaling: 'Auto-scaling (Pro Tier Performance)'
  };

  return (
    <div className="architecture">
      <div className="architecture-header">
        <h1>🏗️ System Architecture</h1>
        <p>Comprehensive view of the Habu Clean Room MCP Server platform</p>
        
        <div className="view-modes">
          <button 
            className={`view-mode ${viewMode === 'overview' ? 'active' : ''}`}
            onClick={() => setViewMode('overview')}
          >
            📊 Overview
          </button>
          <button 
            className={`view-mode ${viewMode === 'data-flow' ? 'active' : ''}`}
            onClick={() => setViewMode('data-flow')}
          >
            🔄 Data Flow
          </button>
          <button 
            className={`view-mode ${viewMode === 'deployment' ? 'active' : ''}`}
            onClick={() => setViewMode('deployment')}
          >
            🚀 Deployment
          </button>
        </div>
      </div>

      <div className="architecture-content">
        {viewMode === 'overview' && (
          <div className="overview-section">
            <div className="components-grid">
              {components.map((component) => (
                <div
                  key={component.id}
                  className={`component-card ${selectedComponent?.id === component.id ? 'selected' : ''}`}
                  onClick={() => setSelectedComponent(component)}
                  style={{ borderColor: getTypeColor(component.type) }}
                >
                  <div className="component-header">
                    <span className="component-icon">{getTypeIcon(component.type)}</span>
                    <h3>{component.name}</h3>
                    <div 
                      className="status-indicator"
                      style={{ backgroundColor: getStatusColor(component.status) }}
                      title={component.status}
                    ></div>
                  </div>
                  
                  <div className="component-type" style={{ color: getTypeColor(component.type) }}>
                    {component.type.toUpperCase()}
                  </div>
                  
                  <p className="component-description">{component.description}</p>
                  
                  <div className="component-tech">
                    {component.technologies.slice(0, 2).map((tech, index) => (
                      <span key={index} className="tech-tag">{tech}</span>
                    ))}
                    {component.technologies.length > 2 && (
                      <span className="tech-more">+{component.technologies.length - 2}</span>
                    )}
                  </div>

                  {component.issues && (
                    <div className="component-issues">
                      <span className="issues-indicator">⚠️ {component.issues.length} issues</span>
                    </div>
                  )}
                </div>
              ))}
            </div>

            {selectedComponent && (
              <div className="component-details">
                <div className="details-header">
                  <h2>
                    {getTypeIcon(selectedComponent.type)} {selectedComponent.name}
                  </h2>
                  <div className="details-status">
                    <span 
                      className="status-dot"
                      style={{ backgroundColor: getStatusColor(selectedComponent.status) }}
                    ></span>
                    Status: {selectedComponent.status.toUpperCase()}
                  </div>
                </div>

                <div className="details-content">
                  <div className="details-section">
                    <h4>Description</h4>
                    <p>{selectedComponent.description}</p>
                  </div>

                  <div className="details-section">
                    <h4>Technologies</h4>
                    <div className="tech-list">
                      {selectedComponent.technologies.map((tech, index) => (
                        <span key={index} className="tech-badge">{tech}</span>
                      ))}
                    </div>
                  </div>

                  <div className="details-section">
                    <h4>Connections</h4>
                    <div className="connections-list">
                      {selectedComponent.connections.map((connectionId, index) => {
                        const connectedComponent = components.find(c => c.id === connectionId);
                        return (
                          <span key={index} className="connection-badge">
                            {connectedComponent ? connectedComponent.name : connectionId}
                          </span>
                        );
                      })}
                    </div>
                  </div>

                  {selectedComponent.url && (
                    <div className="details-section">
                      <h4>URL</h4>
                      <a href={selectedComponent.url} target="_blank" rel="noopener noreferrer" className="component-url">
                        {selectedComponent.url}
                      </a>
                    </div>
                  )}

                  {selectedComponent.issues && (
                    <div className="details-section">
                      <h4>Known Issues</h4>
                      <ul className="issues-list">
                        {selectedComponent.issues.map((issue, index) => (
                          <li key={index} className="issue-item">{issue}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
        )}

        {viewMode === 'data-flow' && (
          <div className="data-flow-section">
            <h2>🔄 Request/Response Data Flow</h2>
            <p>Step-by-step breakdown of how user requests are processed through the system</p>
            
            <div className="flow-steps">
              {dataFlowSteps.map((step, index) => (
                <div key={index} className="flow-step">
                  <div className="step-number">{step.step}</div>
                  <div className="step-content">
                    <h3>{step.component}</h3>
                    <p>{step.description}</p>
                    <span className="step-tech">{step.tech}</span>
                  </div>
                  {index < dataFlowSteps.length - 1 && (
                    <div className="step-arrow">↓</div>
                  )}
                </div>
              ))}
            </div>

            <div className="flow-diagram">
              <h3>System Architecture Diagram</h3>
              <div className="diagram-container">
                <div className="diagram-text">
                  <pre>{`
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────────┐
│   React Frontend │────│  Flask API Bridge │────│ Enhanced Chat Agent │
│   (TypeScript)   │    │ (Python + Redis) │    │   (OpenAI GPT-4)   │
└─────────────────┘    └──────────────────┘    └─────────────────────┘
                              │                            │
                              ▼                            ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────────┐
│   Redis Cache   │────│   MCP Server     │────│ Enhanced MCP Tools  │
│ (Phase H Perf.) │    │   (FastMCP 2.0) │    │ (8 AI-Enhanced)    │
└─────────────────┘    └──────────────────┘    └─────────────────────┘
                              │                            │
                              ▼                            ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────────┐
│   PostgreSQL DB │    │   Render.com     │    │  LiveRamp Clean API │
│   (Async ORM)   │    │   (Pro Tier)     │    │ (Real API + AI)    │
└─────────────────┘    └──────────────────┘    └─────────────────────┘
                              │
                              ▼
┌─────────────────┐
│   Admin App     │
│   (Flask)       │
└─────────────────┘
                  `}</pre>
                </div>
              </div>
            </div>
          </div>
        )}

        {viewMode === 'deployment' && (
          <div className="deployment-section">
            <h2>🚀 Deployment Architecture</h2>
            <p>Production deployment configuration on Render.com platform</p>
            
            <div className="deployment-grid">
              <div className="deployment-card">
                <h3>🌐 Platform</h3>
                <p><strong>Host:</strong> {deploymentInfo.platform}</p>
                <p><strong>Services:</strong> {deploymentInfo.services} Web Services</p>
                <p><strong>Database:</strong> {deploymentInfo.database}</p>
                <p><strong>Deployment:</strong> {deploymentInfo.deployment}</p>
              </div>

              <div className="deployment-card">
                <h3>🔗 Domains</h3>
                {deploymentInfo.domains.map((domain, index) => (
                  <p key={index}>
                    <a href={`https://${domain}`} target="_blank" rel="noopener noreferrer">
                      {domain}
                    </a>
                  </p>
                ))}
              </div>

              <div className="deployment-card">
                <h3>⚙️ Configuration</h3>
                <p><strong>Environment:</strong> {deploymentInfo.environment}</p>
                <p><strong>SSL/TLS:</strong> {deploymentInfo.ssl}</p>
                <p><strong>Monitoring:</strong> {deploymentInfo.monitoring}</p>
                <p><strong>Scaling:</strong> {deploymentInfo.scaling}</p>
              </div>
            </div>

            <div className="service-status-grid">
              <h3>Service Status Overview</h3>
              {components
                .filter(c => c.url && c.type !== 'external')
                .map((service, index) => (
                  <div key={index} className="service-status-card">
                    <div className="service-header">
                      <span className="service-icon">{getTypeIcon(service.type)}</span>
                      <h4>{service.name}</h4>
                      <div 
                        className="service-status-dot"
                        style={{ backgroundColor: getStatusColor(service.status) }}
                      ></div>
                    </div>
                    <p className="service-url">
                      <a href={service.url} target="_blank" rel="noopener noreferrer">
                        {service.url}
                      </a>
                    </p>
                    <div className="service-tech">
                      {service.technologies.slice(0, 3).map((tech, techIndex) => (
                        <span key={techIndex} className="service-tech-tag">{tech}</span>
                      ))}
                    </div>
                  </div>
                ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Architecture;