import React, { useState, useEffect } from 'react';
import './Cleanrooms.css';

interface Template {
  id: string;
  name: string;
  description: string;
  category: string;
  question_type: string;
  cleanroom_id: string;
  cleanroom_name: string;
  status: string;
  created_on: string;
}

interface CleanroomData {
  count: number;
  templates: Template[];
  summary: string;
  mock_mode: boolean;
}

interface Partner {
  name: string;
  type: string;
  description: string;
}

interface PartnersData {
  count: number;
  partners: Partner[];
  summary: string;
  mock_mode: boolean;
}

const Cleanrooms: React.FC = () => {
  const [templates, setTemplates] = useState<CleanroomData | null>(null);
  const [partners, setPartners] = useState<PartnersData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5001';

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        
        // Fetch templates and partners simultaneously
        const [templatesResponse, partnersResponse] = await Promise.all([
          fetch(`${API_BASE_URL}/api/mcp/habu_list_templates`),
          fetch(`${API_BASE_URL}/api/mcp/habu_list_partners`)
        ]);

        if (!templatesResponse.ok || !partnersResponse.ok) {
          throw new Error('Failed to fetch cleanroom data');
        }

        const templatesData = await templatesResponse.json();
        const partnersData = await partnersResponse.json();

        setTemplates(templatesData);
        setPartners(partnersData);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [API_BASE_URL]);

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'ready':
        return '#48bb78';
      case 'missing_datasets':
        return '#ed8936';
      case 'complete':
        return '#4299e1';
      default:
        return '#718096';
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  if (loading) {
    return (
      <div className="cleanrooms-container">
        <div className="loading">
          <div className="loading-spinner"></div>
          <p>Loading cleanroom data...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="cleanrooms-container">
        <div className="error">
          <h2>Error Loading Cleanroom Data</h2>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="cleanrooms-container">
      <div className="cleanrooms-header">
        <h1>🏢 Habu Cleanrooms</h1>
        <p className="subtitle">
          Secure data collaboration environment - {templates?.mock_mode ? 'Mock Mode' : 'Live API'}
        </p>
      </div>

      {/* Cleanroom Overview */}
      <div className="cleanroom-overview">
        <div className="overview-card">
          <h2>📊 Data Marketplace Demo</h2>
          <div className="overview-details">
            <div className="overview-item">
              <span className="label">Organization:</span>
              <span className="value">ICDC - Demo</span>
            </div>
            <div className="overview-item">
              <span className="label">Status:</span>
              <span className="value" style={{ color: getStatusColor('complete') }}>
                COMPLETE
              </span>
            </div>
            <div className="overview-item">
              <span className="label">Templates:</span>
              <span className="value">{templates?.count || 0} Available</span>
            </div>
            <div className="overview-item">
              <span className="label">Partners:</span>
              <span className="value">{partners?.count || 0} Active</span>
            </div>
          </div>
        </div>
      </div>

      {/* Analytics Templates */}
      <div className="section">
        <h2>📋 Analytics Templates</h2>
        <p className="section-description">
          Ready-to-use analytics templates for secure data collaboration
        </p>
        
        {templates && templates.count > 0 ? (
          <div className="templates-grid">
            {templates.templates.map((template) => (
              <div key={template.id} className="template-card">
                <div className="template-header">
                  <h3>{template.name}</h3>
                  <span 
                    className="status-badge"
                    style={{ backgroundColor: getStatusColor(template.status) }}
                  >
                    {template.status.replace('_', ' ')}
                  </span>
                </div>
                <div className="template-details">
                  <div className="template-meta">
                    <span className="category">{template.category}</span>
                    <span className="type">{template.question_type}</span>
                  </div>
                  <div className="template-info">
                    <p><strong>Cleanroom:</strong> {template.cleanroom_name}</p>
                    <p><strong>Created:</strong> {formatDate(template.created_on)}</p>
                  </div>
                  {template.description && (
                    <p className="template-description">{template.description}</p>
                  )}
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="empty-state">
            <p>No analytics templates available</p>
          </div>
        )}
      </div>

      {/* Data Partners */}
      <div className="section">
        <h2>🤝 Data Partners</h2>
        <p className="section-description">
          Trusted partners for secure data collaboration
        </p>
        
        {partners && partners.count > 0 ? (
          <div className="partners-grid">
            {partners.partners.map((partner, index) => (
              <div key={index} className="partner-card">
                <div className="partner-header">
                  <h3>{partner.name}</h3>
                  <span className="partner-type">{partner.type}</span>
                </div>
                <p className="partner-description">{partner.description}</p>
              </div>
            ))}
          </div>
        ) : (
          <div className="empty-state">
            <div className="empty-icon">🔗</div>
            <h3>No Active Partners</h3>
            <p>Contact your administrator to establish data partnerships</p>
            <div className="partner-info">
              <p><strong>Available Partner Types:</strong></p>
              <ul>
                <li>Data Providers (GDELT, Geotrace, TimberMac)</li>
                <li>Retail Partners</li>
                <li>Media & Advertising Partners</li>
                <li>Financial Services Partners</li>
              </ul>
            </div>
          </div>
        )}
      </div>

      {/* API Status */}
      <div className="api-status">
        <div className="status-card">
          <h3>🔗 API Status</h3>
          <div className="status-items">
            <div className="status-item">
              <span className="status-dot" style={{ backgroundColor: templates?.mock_mode ? '#ed8936' : '#4299e1' }}></span>
              <span>{templates?.mock_mode ? 'Mock Data Mode' : 'Live API Mode'}</span>
            </div>
            <div className="status-item">
              <span className="status-dot" style={{ backgroundColor: '#48bb78' }}></span>
              <span>Templates API: Active</span>
            </div>
            <div className="status-item">
              <span className="status-dot" style={{ backgroundColor: '#48bb78' }}></span>
              <span>Partners API: Active</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Cleanrooms;