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

  const renderTechnicalExpertMessage = () => {
    const { content, metadata } = message;
    
    return (
      <div className="technical-expert-message">
        <div className="message-header">
          <div className="mode-indicator">
            <span className="mode-icon">🔧</span>
            <span className="mode-label">Technical Expert</span>
          </div>
          {metadata?.confidenceScore && (
            <div className="confidence-score">
              <span className="confidence-label">Validation:</span>
              <span className="confidence-value">
                {metadata.confidenceScore > 0.9 ? '✅ Verified' : 
                 metadata.confidenceScore > 0.7 ? '⚠️ Needs Review' : '❌ Unverified'}
              </span>
            </div>
          )}
        </div>
        
        <div className="message-content">
          <div className="primary-content">
            {content}
          </div>
          
          {/* Code Examples */}
          {metadata?.codeExamples && metadata.codeExamples.length > 0 && (
            <div className="code-examples">
              <h4>💻 Code Examples</h4>
              {metadata.codeExamples.slice(0, isExpanded ? metadata.codeExamples.length : 1).map((example: any, index: number) => (
                <div key={index} className="code-example">
                  <div className="example-header">
                    <span className="language-tag">{example.language}</span>
                    <span className="example-title">{example.title}</span>
                  </div>
                  <div className="example-description">{example.description}</div>
                  <pre className="code-block">
                    <code>{example.code}</code>
                  </pre>
                  {example.dependencies && example.dependencies.length > 0 && (
                    <div className="dependencies">
                      <span className="dependencies-label">Dependencies:</span>
                      {example.dependencies.map((dep: string, depIndex: number) => (
                        <span key={depIndex} className="dependency-tag">{dep}</span>
                      ))}
                    </div>
                  )}
                </div>
              ))}
              {!isExpanded && metadata.codeExamples.length > 1 && (
                <div className="more-examples">
                  +{metadata.codeExamples.length - 1} more examples
                </div>
              )}
            </div>
          )}
          
          {/* Implementation Steps */}
          {metadata?.implementationSteps && metadata.implementationSteps.length > 0 && (
            <div className="implementation-steps">
              <h4>📋 Implementation Steps</h4>
              <ol>
                {metadata.implementationSteps.slice(0, isExpanded ? metadata.implementationSteps.length : 3).map((step: string, index: number) => (
                  <li key={index}>{step}</li>
                ))}
              </ol>
              {!isExpanded && metadata.implementationSteps.length > 3 && (
                <div className="more-steps">
                  +{metadata.implementationSteps.length - 3} more steps
                </div>
              )}
            </div>
          )}
          
          {/* API Methods */}
          {metadata?.apiMethods && metadata.apiMethods.length > 0 && (
            <div className="api-methods">
              <h4>🔌 API Methods</h4>
              {metadata.apiMethods.map((method: any, index: number) => (
                <div key={index} className="api-method">
                  <div className="method-header">
                    <span className="method-name">{method.name}</span>
                    <span className="method-endpoint">{method.method} {method.endpoint}</span>
                  </div>
                  <div className="method-description">{method.description}</div>
                </div>
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
              📖 Show Full Details
            </button>
          )}
          
          <button 
            className="action-button technical"
            onClick={() => handleAction('copy_code')}
          >
            📋 Copy Code
          </button>
          
          <button 
            className="action-button technical"
            onClick={() => handleAction('view_docs')}
          >
            📚 View Docs
          </button>
        </div>
        
        {isExpanded && (
          <div className="expanded-content">
            {/* Performance Considerations */}
            {metadata?.performanceConsiderations && metadata.performanceConsiderations.length > 0 && (
              <div className="performance-section">
                <h4>⚡ Performance Considerations</h4>
                <ul>
                  {metadata.performanceConsiderations.map((consideration: string, index: number) => (
                    <li key={index}>{consideration}</li>
                  ))}
                </ul>
              </div>
            )}
            
            {/* Security Guidance */}
            {metadata?.securityGuidance && metadata.securityGuidance.length > 0 && (
              <div className="security-section">
                <h4>🛡️ Security Guidance</h4>
                <ul>
                  {metadata.securityGuidance.map((guidance: string, index: number) => (
                    <li key={index}>{guidance}</li>
                  ))}
                </ul>
              </div>
            )}
            
            {/* Technical Details */}
            <div className="technical-details">
              <h4>🔧 Technical Information</h4>
              <div className="tech-info">
                {metadata?.processingTime && (
                  <div className="tech-stat">
                    <span>Processing Time:</span>
                    <span>{metadata.processingTime}ms</span>
                  </div>
                )}
                {metadata?.toolsUsed && metadata.toolsUsed.length > 0 && (
                  <div className="tech-stat">
                    <span>Tools Used:</span>
                    <span>{metadata.toolsUsed.join(', ')}</span>
                  </div>
                )}
                {metadata?.confidenceScore && (
                  <div className="tech-stat">
                    <span>Confidence Score:</span>
                    <span>{(metadata.confidenceScore * 100).toFixed(1)}%</span>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}
      </div>
    );
  };

  const renderAPIExpertMessage = () => {
    // Legacy API Expert mode - redirect to Technical Expert
    return renderTechnicalExpertMessage();
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
      {message.mode === ChatMode.CUSTOMER_SUPPORT 
        ? renderManagerModeMessage() 
        : message.mode === ChatMode.TECHNICAL_EXPERT 
        ? renderTechnicalExpertMessage()
        : renderAPIExpertMessage()}
      
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