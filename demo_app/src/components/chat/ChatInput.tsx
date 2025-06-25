import React, { useState, useRef, useEffect } from 'react';
import { useChatMode } from '../../contexts/ChatModeContext';

interface ChatInputProps {
  onSendMessage: (message: string) => void;
  isLoading: boolean;
  placeholder?: string;
}

const ChatInput: React.FC<ChatInputProps> = ({ 
  onSendMessage, 
  isLoading, 
  placeholder 
}) => {
  const [message, setMessage] = useState('');
  const [isExpanded, setIsExpanded] = useState(false);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const { getCurrentModeConfig } = useChatMode();

  const modeConfig = getCurrentModeConfig();
  const defaultPlaceholder = placeholder || 
    `Ask your ${modeConfig.name.toLowerCase()} a question...`;

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = textareaRef.current.scrollHeight + 'px';
      setIsExpanded(textareaRef.current.scrollHeight > 48);
    }
  }, [message]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (message.trim() && !isLoading) {
      onSendMessage(message.trim());
      setMessage('');
      setIsExpanded(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const handleFocus = () => {
    setIsExpanded(true);
  };

  const handleBlur = () => {
    if (!message.trim()) {
      setIsExpanded(false);
    }
  };

  const getSuggestions = () => {
    const modeConfig = getCurrentModeConfig();
    
    if (modeConfig.mode === 'customer_support') {
      return [
        'Customer wants lookalike modeling',
        'Can we support real-time attribution?',
        'What privacy compliance options do we have?'
      ];
    } else {
      return [
        'Show me Python identity resolution code',
        'How to handle 401 authentication errors?',
        'What are API performance best practices?'
      ];
    }
  };

  return (
    <div className={`chat-input-container ${isExpanded ? 'expanded' : ''}`}>
      {isExpanded && (
        <div className="input-suggestions">
          <div className="suggestions-header">
            <span>💡 Try asking:</span>
          </div>
          <div className="suggestions-list">
            {getSuggestions().map((suggestion, index) => (
              <button
                key={index}
                className="suggestion-button"
                onClick={() => setMessage(suggestion)}
              >
                {suggestion}
              </button>
            ))}
          </div>
        </div>
      )}
      
      <form onSubmit={handleSubmit} className="chat-input-form">
        <div className="input-wrapper">
          <textarea
            ref={textareaRef}
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={handleKeyDown}
            onFocus={handleFocus}
            onBlur={handleBlur}
            placeholder={defaultPlaceholder}
            className="chat-textarea"
            rows={1}
            disabled={isLoading}
          />
          
          <div className="input-actions">
            {message.trim() && (
              <button
                type="button"
                className="clear-button"
                onClick={() => setMessage('')}
                title="Clear message"
              >
                ✕
              </button>
            )}
            
            <button
              type="submit"
              className={`send-button ${!message.trim() || isLoading ? 'disabled' : ''}`}
              disabled={!message.trim() || isLoading}
              title="Send message (Enter)"
            >
              {isLoading ? (
                <span className="loading-spinner">⏳</span>
              ) : (
                <span className="send-icon">🚀</span>
              )}
            </button>
          </div>
        </div>
        
        <div className="input-footer">
          <div className="input-hints">
            <span>💡 Press Enter to send, Shift+Enter for new line</span>
          </div>
          
          <div className="character-count">
            <span className={message.length > 500 ? 'warning' : ''}>
              {message.length}/1000
            </span>
          </div>
        </div>
      </form>
    </div>
  );
};

export default ChatInput;