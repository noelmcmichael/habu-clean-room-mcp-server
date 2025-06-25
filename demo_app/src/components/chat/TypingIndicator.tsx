import React from 'react';

interface TypingIndicatorProps {
  isVisible: boolean;
  message?: string;
}

const TypingIndicator: React.FC<TypingIndicatorProps> = ({ 
  isVisible, 
  message = "AI Assistant is thinking..." 
}) => {
  if (!isVisible) return null;

  return (
    <div className="typing-indicator">
      <div className="typing-indicator-content">
        <div className="typing-dots">
          <div className="typing-dot"></div>
          <div className="typing-dot"></div>
          <div className="typing-dot"></div>
        </div>
        <span className="typing-message">{message}</span>
      </div>
    </div>
  );
};

export default TypingIndicator;