import React from 'react';
import { useChatMode } from '../../contexts/ChatModeContext';
import { useConversation } from '../../contexts/ConversationContext';

interface ChatMetricsProps {
  className?: string;
}

const ChatMetrics: React.FC<ChatMetricsProps> = ({ className = '' }) => {
  const { modeState } = useChatMode();
  const { conversationState } = useConversation();

  const metrics = {
    totalMessages: (conversationState.conversationLength || 0),
    customerSupportQueries: modeState.conversationHistory.filter(m => m.mode === 'customer_support' && m.type === 'user').length,
    technicalExpertQueries: modeState.conversationHistory.filter(m => m.mode === 'technical_expert' && m.type === 'user').length,
    sessionStartTime: new Date(), // Use current time as fallback
    currentMode: modeState.currentMode
  };

  const getSessionDuration = () => {
    if (!metrics.sessionStartTime) return '0m';
    const now = new Date();
    const diff = now.getTime() - metrics.sessionStartTime.getTime();
    const minutes = Math.floor(diff / 60000);
    return minutes > 0 ? `${minutes}m` : '<1m';
  };

  const getModeIcon = (mode: string) => {
    switch (mode) {
      case 'customer_support': return '🤝';
      case 'technical_expert': return '🔧';
      default: return '💬';
    }
  };

  return (
    <div className={`chat-metrics ${className}`}>
      <div className="metrics-header">
        <h4>📊 Session Metrics</h4>
      </div>
      
      <div className="metrics-grid">
        <div className="metric-item">
          <span className="metric-icon">💬</span>
          <div className="metric-details">
            <span className="metric-value">{metrics.totalMessages}</span>
            <span className="metric-label">Total Messages</span>
          </div>
        </div>
        
        <div className="metric-item">
          <span className="metric-icon">⏱️</span>
          <div className="metric-details">
            <span className="metric-value">{getSessionDuration()}</span>
            <span className="metric-label">Session Time</span>
          </div>
        </div>
        
        <div className="metric-item">
          <span className="metric-icon">{getModeIcon(metrics.currentMode)}</span>
          <div className="metric-details">
            <span className="metric-value">{metrics.currentMode.replace('_', ' ')}</span>
            <span className="metric-label">Current Mode</span>
          </div>
        </div>
        
        <div className="metric-item">
          <span className="metric-icon">🤝</span>
          <div className="metric-details">
            <span className="metric-value">{metrics.customerSupportQueries}</span>
            <span className="metric-label">Support Queries</span>
          </div>
        </div>
        
        <div className="metric-item">
          <span className="metric-icon">🔧</span>
          <div className="metric-details">
            <span className="metric-value">{metrics.technicalExpertQueries}</span>
            <span className="metric-label">Tech Queries</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatMetrics;