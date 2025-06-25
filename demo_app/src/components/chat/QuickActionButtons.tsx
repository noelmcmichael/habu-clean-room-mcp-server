import React from 'react';
import { useChatMode } from '../../contexts/ChatModeContext';

interface QuickAction {
  id: string;
  label: string;
  icon: string;
  query: string;
  category: string;
}

interface QuickActionButtonsProps {
  onQuickAction: (query: string) => void;
}

const QuickActionButtons: React.FC<QuickActionButtonsProps> = ({ onQuickAction }) => {
  const { isCustomerSupportMode, isTechnicalExpertMode } = useChatMode();

  const customerSupportActions: QuickAction[] = [
    {
      id: 'lookalike',
      label: 'Lookalike Modeling',
      icon: '🎯',
      query: 'Customer wants lookalike modeling for their retail audience',
      category: 'Audience'
    },
    {
      id: 'attribution',
      label: 'Real-time Attribution',
      icon: '⚡',
      query: 'Financial services client needs real-time attribution analysis',
      category: 'Analytics'
    },
    {
      id: 'segmentation',
      label: 'Audience Segmentation',
      icon: '📊',
      query: 'Can we help automotive client with audience segmentation?',
      category: 'Audience'
    },
    {
      id: 'privacy',
      label: 'Privacy Compliance',
      icon: '🛡️',
      query: 'Customer asking about GDPR compliance for data collaboration',
      category: 'Compliance'
    }
  ];

  const technicalExpertActions: QuickAction[] = [
    {
      id: 'identity-api',
      label: 'Identity Resolution API',
      icon: '🔑',
      query: 'Show me Python code for identity resolution with error handling',
      category: 'API'
    },
    {
      id: 'auth-troubleshoot',
      label: 'Authentication Issues',
      icon: '🔐',
      query: 'I am getting 401 errors when calling the LiveRamp API',
      category: 'Troubleshooting'
    },
    {
      id: 'performance',
      label: 'Performance Optimization',
      icon: '⚡',
      query: 'How to optimize API calls for large datasets?',
      category: 'Performance'
    },
    {
      id: 'security',
      label: 'Security Best Practices',
      icon: '🛡️',
      query: 'What are the security best practices for API integration?',
      category: 'Security'
    }
  ];

  const actions = isCustomerSupportMode() ? customerSupportActions : technicalExpertActions;

  const groupedActions = actions.reduce((groups, action) => {
    const category = action.category;
    if (!groups[category]) {
      groups[category] = [];
    }
    groups[category].push(action);
    return groups;
  }, {} as Record<string, QuickAction[]>);

  return (
    <div className="quick-actions-container">
      <div className="quick-actions-header">
        <h3>🚀 Quick Actions</h3>
        <p>{isCustomerSupportMode() ? 'Customer Support Scenarios' : 'Technical Implementation'}</p>
      </div>
      
      {Object.entries(groupedActions).map(([category, categoryActions]) => (
        <div key={category} className="quick-actions-category">
          <h4 className="category-title">{category}</h4>
          <div className="quick-actions-grid">
            {categoryActions.map((action) => (
              <button
                key={action.id}
                className="quick-action-button"
                onClick={() => onQuickAction(action.query)}
                title={action.query}
              >
                <span className="action-icon">{action.icon}</span>
                <span className="action-label">{action.label}</span>
              </button>
            ))}
          </div>
        </div>
      ))}
      
      <div className="quick-actions-footer">
        <p>💡 Click any button to try a sample query</p>
      </div>
    </div>
  );
};

export default QuickActionButtons;