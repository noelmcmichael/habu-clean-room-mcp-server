import React, { useState } from 'react';
import { ChatMessage, ChatMode } from '../../types/ChatModes';
import { useChatMode } from '../../contexts/ChatModeContext';
import './EnhancedChatMessage.css';

interface EnhancedChatMessageProps {
  message: ChatMessage;
  onExpand?: (messageId: string) => void;
  onAction?: (action: string, messageId: string) => void;
}

const EnhancedChatMessage: React.FC<EnhancedChatMessageProps> = ({ 
  message, 
  onExpand,
  onAction 
}) => {
  const { modeState } = useChatMode();
  const [isExpanded, setIsExpanded] = useState(false);
  const [showTechnicalDetails, setShowTechnicalDetails] = useState(false);

  const handleExpand = () => {
    setIsExpanded(!isExpanded);
    if (onExpand) {
      onExpand(message.id);
    }
  };

  const handleAction = (action: string) => {
    if (onAction) {
      onAction(action, message.id);
    }
  };

  const renderManagerModeMessage = () => {
    const { content, metadata } = message;
    
    return (
      <div className="manager-message">
        <div className="message-header">
          <div className="mode-indicator">
            <span className="mode-icon">📊</span>
            <span className="mode-label">Manager Mode</span>
          </div>
          {metadata?.confidenceScore && (
            <div className="confidence-score">
              <span className="confidence-label">Confidence:</span>
              <span className="confidence-value">{Math.round(metadata.confidenceScore * 100)}%</span>
            </div>
          )}
        </div>
        
        <div className="message-content">
          <div className="primary-content">
            {content}
          </div>
          
          {metadata?.businessImpact && (
            <div className="business-impact">
              <h4>💡 Business Impact</h4>
              <p>{metadata.businessImpact}</p>
            </div>
          )}
          
          {metadata?.toolsUsed && metadata.toolsUsed.length > 0 && (
            <div className="tools-used">
              <span className="tools-label">Data Sources:</span>
              {metadata.toolsUsed.map((tool, index) => (
                <span key={index} className="tool-tag business">
                  {formatToolForBusiness(tool)}
                </span>
              ))}
            </div>
          )}
        </div>
        
        <div className="message-actions">
          {!isExpanded && (
            <button 
              className="expand-button business"
              onClick={handleExpand}
            >
              📋 Show Details
            </button>
          )}
          
          <button 
            className="action-button business"
            onClick={() => handleAction('get_recommendations')}
          >
            💡 Get Recommendations
          </button>
          
          <button 
            className="action-button business"
            onClick={() => handleAction('export_summary')}
          >
            📊 Export Summary
          </button>
        </div>
        
        {isExpanded && (
          <div className="expanded-content">
            <div className="technical-toggle">
              <button
                className={`toggle-button ${showTechnicalDetails ? 'active' : ''}`}
                onClick={() => setShowTechnicalDetails(!showTechnicalDetails)}
              >
                {showTechnicalDetails ? '👔 Business View' : '🔧 Technical Details'}
              </button>
            </div>
            
            {showTechnicalDetails && metadata && (
              <div className="technical-details">
                <h4>Technical Information</h4>
                <div className="tech-info">
                  {metadata.processingTime && (
                    <div className="tech-stat">
                      <span>Processing Time:</span>
                      <span>{metadata.processingTime}ms</span>
                    </div>
                  )}
                  {metadata.queryExecuted && (
                    <div className="tech-stat">
                      <span>Query Executed:</span>
                      <span>✅ Yes</span>
                    </div>
                  )}
                  {metadata.sourceValidation && (
                    <div className="tech-stat">
                      <span>Source Validation:</span>
                      <span>✅ Verified</span>
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    );
  };

  const renderAPIExpertMessage = () => {
    const { content, metadata } = message;
    
    return (
      <div className="api-expert-message">
        <div className="message-header">
          <div className="mode-indicator">
            <span className="mode-icon">🔧</span>
            <span className="mode-label">API Expert</span>
          </div>
          {metadata?.sourceValidation && (
            <div className="validation-indicator">
              <span className="validation-icon">✅</span>
              <span className="validation-label">API Verified</span>
            </div>
          )}
        </div>
        
        <div className="message-content">
          <div className="primary-content">
            {content}
          </div>
          
          {metadata?.toolsUsed && metadata.toolsUsed.length > 0 && (
            <div className="tools-used">
              <span className="tools-label">API Methods:</span>
              {metadata.toolsUsed.map((tool, index) => (
                <span key={index} className="tool-tag technical">
                  {tool}
                </span>
              ))}
            </div>
          )}
        </div>
        
        <div className="message-actions">
          {!isExpanded && (
            <button 
              className="expand-button technical"
              onClick={handleExpand}
            >
              📖 Learn More
            </button>
          )}
          
          <button 
            className="action-button technical"
            onClick={() => handleAction('show_examples')}
          >
            💻 Show Examples
          </button>
          
          <button 
            className="action-button technical"
            onClick={() => handleAction('test_api')}
          >
            🧪 Test API
          </button>
        </div>
        
        {isExpanded && (
          <div className="expanded-content">
            <div className="api-details">
              <h4>Additional Information</h4>
              {metadata && (
                <div className="api-metadata">
                  {metadata.processingTime && (
                    <div className="api-stat">
                      <span>Response Time:</span>
                      <span>{metadata.processingTime}ms</span>
                    </div>
                  )}
                  {metadata.confidenceScore && (
                    <div className="api-stat">
                      <span>Information Accuracy:</span>
                      <span>{Math.round(metadata.confidenceScore * 100)}%</span>
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    );
  };

  const formatToolForBusiness = (tool: string): string => {
    const businessNames: Record<string, string> = {
      'habu_list_partners': 'Partner Directory',
      'habu_enhanced_templates': 'Analysis Templates',
      'habu_submit_query': 'Query Execution',
      'habu_check_status': 'Status Monitoring',
      'habu_get_results': 'Results Retrieval',
      'habu_list_exports': 'Export Management'
    };
    
    return businessNames[tool] || tool.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
  };

  if (message.type === 'user') {
    return (
      <div className="chat-message user-message">
        <div className="message-content">
          {message.content}
        </div>
        <div className="message-timestamp">
          {message.timestamp.toLocaleTimeString()}
        </div>
      </div>
    );
  }

  return (
    <div className={`chat-message assistant-message ${message.mode}-mode`}>
      {message.mode === ChatMode.CUSTOMER_SUPPORT ? renderManagerModeMessage() : renderAPIExpertMessage()}
      
      <div className="message-footer">
        <div className="message-timestamp">
          {message.timestamp.toLocaleTimeString()}
        </div>
        {message.metadata?.isAiPowered && (
          <div className="ai-indicator">
            <span className="ai-icon">🤖</span>
            <span className="ai-label">AI Powered</span>
          </div>
        )}
      </div>
    </div>
  );
};

export default EnhancedChatMessage;