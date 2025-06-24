import React, { useState, useEffect } from 'react';
import { useConversation } from '../contexts/ConversationContext';
import './Cleanrooms.css';

interface EnhancedTemplate {
  id: string;
  name: string;
  description: string;
  category: string;
  question_type: string;
  cleanroom_id: string;
  cleanroom_name: string;
  status: string;
  created_on: string;
  enhanced_data?: {
    parameters?: Array<{name: string; type: string; description: string; required: boolean}>;
    data_types?: string[];
    complexity?: string;
    estimated_runtime?: string;
    business_value?: string;
  };
}

interface EnhancedCleanroomData {
  templates: EnhancedTemplate[];
  ready_templates: number;
  missing_datasets_templates: number;
  total_templates: number;
  categories: string[];
  enhancement_features: {
    parameters_added: number;
    data_types_enriched: number;
    complexity_assessed: number;
    business_intelligence_added: number;
  };
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
  const { updateTemplateContext } = useConversation();
  const [enhancedTemplates, setEnhancedTemplates] = useState<EnhancedCleanroomData | null>(null);
  const [partners, setPartners] = useState<PartnersData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5001';

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        
        // Fetch enhanced templates and partners
        const [enhancedTemplatesResponse, partnersResponse] = await Promise.all([
          fetch(`${API_BASE_URL}/api/mcp/habu_enhanced_templates`),
          fetch(`${API_BASE_URL}/api/mcp/habu_list_partners`)
        ]);

        if (!enhancedTemplatesResponse.ok || !partnersResponse.ok) {
          throw new Error('Failed to fetch cleanroom data');
        }

        const enhancedTemplatesData = await enhancedTemplatesResponse.json();
        const partnersData = await partnersResponse.json();

        setEnhancedTemplates(enhancedTemplatesData);
        setPartners(partnersData);
        
        // Update conversation context with template data
        if (enhancedTemplatesData && enhancedTemplatesData.templates) {
          const categories = new Set<string>();
          let hasLocationData = false;
          let hasSentimentAnalysis = false;
          let hasPatternOfLife = false;
          let hasCombinedAnalysis = false;
          
          enhancedTemplatesData.templates.forEach((template: EnhancedTemplate) => {
            categories.add(template.category);
            
            // Detect specific template types
            const templateName = template.name.toLowerCase();
            const templateCategory = template.category.toLowerCase();
            
            if (templateCategory.includes('sentiment') || templateName.includes('sentiment')) {
              hasSentimentAnalysis = true;
            }
            if (templateCategory.includes('location') || templateName.includes('location') || templateName.includes('geotrace')) {
              hasLocationData = true;
            }
            if (templateCategory.includes('pattern') || templateName.includes('pattern')) {
              hasPatternOfLife = true;
            }
            if (templateName.includes('combined') || templateName.includes('timberMac')) {
              hasCombinedAnalysis = true;
            }
          });
          
          updateTemplateContext({
            totalTemplates: enhancedTemplatesData?.total_templates || enhancedTemplatesData?.templates?.length || 0,
            readyTemplates: enhancedTemplatesData.ready_templates || 0,
            missingDatasetTemplates: enhancedTemplatesData.missing_datasets_templates || 0,
            categories: Array.from(categories),
            hasLocationData,
            hasSentimentAnalysis,
            hasPatternOfLife,
            hasCombinedAnalysis
          });
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [API_BASE_URL, updateTemplateContext]);

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

  const getComplexityColor = (complexity: string) => {
    switch (complexity.toLowerCase()) {
      case 'low':
        return '#48bb78';
      case 'medium':
        return '#ed8936';
      case 'high':
        return '#f56565';
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
        <h1>🏢 LiveRamp Cleanrooms</h1>
        <p className="subtitle">
          Secure data collaboration environment - Real API Mode
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
              <span className="label">Total Templates:</span>
              <span className="value">{enhancedTemplates?.total_templates || 0}</span>
            </div>
            <div className="overview-item">
              <span className="label">Ready Templates:</span>
              <span className="value" style={{ color: getStatusColor('ready') }}>
                {enhancedTemplates?.ready_templates || 0}
              </span>
            </div>
            <div className="overview-item">
              <span className="label">Categories:</span>
              <span className="value">{enhancedTemplates?.categories?.length || 0}</span>
            </div>
          </div>
        </div>

        {/* Business Intelligence Summary */}
        {enhancedTemplates?.enhancement_features && (
          <div className="enhancement-summary">
            <h3>🧠 Enhanced Intelligence</h3>
            <div className="enhancement-stats">
              <div className="stat">
                <span className="stat-value">{enhancedTemplates.enhancement_features.parameters_added}</span>
                <span className="stat-label">Parameters Enriched</span>
              </div>
              <div className="stat">
                <span className="stat-value">{enhancedTemplates.enhancement_features.data_types_enriched}</span>
                <span className="stat-label">Data Types Added</span>
              </div>
              <div className="stat">
                <span className="stat-value">{enhancedTemplates.enhancement_features.complexity_assessed}</span>
                <span className="stat-label">Complexity Assessed</span>
              </div>
              <div className="stat">
                <span className="stat-value">{enhancedTemplates.enhancement_features.business_intelligence_added}</span>
                <span className="stat-label">Business Insights</span>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Analytics Templates */}
      <div className="section">
        <h2>📋 Enhanced Analytics Templates</h2>
        <p className="section-description">
          Ready-to-use analytics templates with AI-powered metadata and business intelligence
        </p>
        
        {enhancedTemplates && enhancedTemplates.templates.length > 0 ? (
          <div className="templates-grid">
            {enhancedTemplates.templates.map((template) => (
              <div key={template.id} className="enhanced-template-card">
                <div className="template-header">
                  <h3>{template.name}</h3>
                  <div className="template-badges">
                    <span 
                      className="status-badge"
                      style={{ backgroundColor: getStatusColor(template.status) }}
                    >
                      {template.status.replace('_', ' ')}
                    </span>
                    {template.enhanced_data?.complexity && (
                      <span 
                        className="complexity-badge"
                        style={{ backgroundColor: getComplexityColor(template.enhanced_data.complexity) }}
                      >
                        {template.enhanced_data.complexity} Complexity
                      </span>
                    )}
                  </div>
                </div>
                
                <div className="template-details">
                  <div className="template-meta">
                    <span className="category">{template.category}</span>
                    <span className="type">{template.question_type}</span>
                  </div>
                  
                  <div className="template-info">
                    <p><strong>Cleanroom:</strong> {template.cleanroom_name}</p>
                    <p><strong>Created:</strong> {formatDate(template.created_on)}</p>
                    {template.enhanced_data?.estimated_runtime && (
                      <p><strong>Runtime:</strong> {template.enhanced_data.estimated_runtime}</p>
                    )}
                  </div>

                  {template.description && (
                    <p className="template-description">{template.description}</p>
                  )}

                  {/* Enhanced metadata */}
                  {template.enhanced_data && (
                    <div className="enhanced-metadata">
                      {template.enhanced_data.parameters && template.enhanced_data.parameters.length > 0 && (
                        <div className="metadata-section">
                          <h4>🔧 Parameters</h4>
                          <div className="parameters-list">
                            {template.enhanced_data.parameters.slice(0, 3).map((param, index) => (
                              <span key={index} className="parameter-tag">
                                {param.name} ({param.type})
                              </span>
                            ))}
                            {template.enhanced_data.parameters.length > 3 && (
                              <span className="parameter-more">
                                +{template.enhanced_data.parameters.length - 3} more
                              </span>
                            )}
                          </div>
                        </div>
                      )}

                      {template.enhanced_data.data_types && template.enhanced_data.data_types.length > 0 && (
                        <div className="metadata-section">
                          <h4>📊 Data Types</h4>
                          <div className="data-types-list">
                            {template.enhanced_data.data_types.slice(0, 4).map((type, index) => (
                              <span key={index} className="data-type-tag">{type}</span>
                            ))}
                            {template.enhanced_data.data_types.length > 4 && (
                              <span className="data-type-more">
                                +{template.enhanced_data.data_types.length - 4} more
                              </span>
                            )}
                          </div>
                        </div>
                      )}

                      {template.enhanced_data.business_value && (
                        <div className="metadata-section">
                          <h4>💡 Business Value</h4>
                          <p className="business-value">{template.enhanced_data.business_value}</p>
                        </div>
                      )}
                    </div>
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
            <p>Contact your administrator to establish data partnerships through LiveRamp's ecosystem</p>
            <div className="partner-info">
              <p><strong>Partnership Capabilities:</strong></p>
              <ul>
                <li>First-party data collaboration</li>
                <li>Privacy-safe data activation</li>
                <li>Cross-platform measurement</li>
                <li>Audience enrichment and insights</li>
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
              <span className="status-dot" style={{ backgroundColor: '#4299e1' }}></span>
              <span>Real API Mode</span>
            </div>
            <div className="status-item">
              <span className="status-dot" style={{ backgroundColor: '#48bb78' }}></span>
              <span>Enhanced Templates API: Active</span>
            </div>
            <div className="status-item">
              <span className="status-dot" style={{ backgroundColor: '#48bb78' }}></span>
              <span>Partners API: Active</span>
            </div>
            <div className="status-item">
              <span className="status-dot" style={{ backgroundColor: '#9f7aea' }}></span>
              <span>AI Enhancement: Active</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Cleanrooms;