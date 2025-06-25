import React from 'react';
import { useChatMode } from '../../contexts/ChatModeContext';
import { useConversation } from '../../contexts/ConversationContext';
import { ChatMode } from '../../types/ChatModes';

const CompactHeader: React.FC = () => {
  const { 
    modeState, 
    switchMode,
    isCustomerSupportMode,
    isTechnicalExpertMode
  } = useChatMode();
  
  const { conversationState } = useConversation();
  
  // Get message history from context state  
  const messageHistory = (conversationState as any).messageHistory || [];

  return (
    <div className="compact-header">
      <div className="compact-header-left">
        <div className="app-title">
          <h1>LiveRamp AI Assistant</h1>
        </div>
        
        <div className="compact-mode-switcher">
          <button 
            className={`mode-button ${isCustomerSupportMode() ? 'active' : ''}`}
            onClick={() => switchMode(ChatMode.CUSTOMER_SUPPORT)}
            title="Customer Support Mode - Help with LiveRamp capabilities and use cases"
          >
            <span className="mode-icon">🎯</span>
            <span className="mode-label">Support</span>
          </button>
          
          <button 
            className={`mode-button ${isTechnicalExpertMode() ? 'active' : ''}`}
            onClick={() => switchMode(ChatMode.TECHNICAL_EXPERT)}
            title="Technical Expert Mode - API integration and development guidance"
          >
            <span className="mode-icon">⚙️</span>
            <span className="mode-label">Tech</span>
          </button>
        </div>
      </div>
      
      <div className="compact-metrics">
        <div className="metric-item">
          <span className="metric-value">{messageHistory.length}</span>
          <span className="metric-label">msgs</span>
        </div>
        <div className="metric-item">
          <span className="metric-value">{isCustomerSupportMode() ? 'Support' : 'Tech'}</span>
          <span className="metric-label">mode</span>
        </div>
      </div>
    </div>
  );
};

export default CompactHeader;