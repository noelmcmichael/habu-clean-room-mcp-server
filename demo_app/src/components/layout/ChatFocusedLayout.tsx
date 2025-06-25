import React, { useState, useRef, useEffect } from 'react';
import CompactHeader from './CompactHeader';
import EnhancedChatMessage from '../chat/EnhancedChatMessage';
import ChatInput from '../chat/ChatInput';
import TypingIndicator from '../chat/TypingIndicator';
import { useChatMode } from '../../contexts/ChatModeContext';
import { useConversation } from '../../contexts/ConversationContext';

const ChatFocusedLayout: React.FC = () => {
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const { getCurrentModeConfig, modeState, isCustomerSupportMode, isTechnicalExpertMode } = useChatMode();
  const { conversationState, addMessage } = useConversation();
  
  // Get message history from context state
  const messageHistory = (conversationState as any).messageHistory || [];

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messageHistory]);

  const handleSendMessage = async (messageText: string) => {
    setIsLoading(true);
    
    // Add user message immediately
    addMessage('user', messageText);

    try {
      // API call logic (same as before but cleaner)
      const apiUrl = process.env.REACT_APP_API_URL || '';
      const endpoint = isCustomerSupportMode() 
        ? '/api/customer-support/quick-assess' 
        : '/api/enhanced-chat';
      
      const requestBody = isCustomerSupportMode()
        ? { 
            query: messageText,
            industry: 'general', // Could extract from context
            context: { mode: modeState.currentMode }
          }
        : {
            message: messageText,
            context: { mode: modeState.currentMode }
          };

      const response = await fetch(`${apiUrl}${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      // Add assistant response
      addMessage('assistant', data.summary || data.response || 'Response received successfully');

    } catch (error) {
      console.error('Chat error:', error);
      addMessage('assistant', 'I apologize, but I encountered an error processing your request. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const getQuickActions = () => {
    if (isCustomerSupportMode()) {
      return [
        'Customer wants lookalike modeling for retail',
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

  const modeConfig = getCurrentModeConfig();

  return (
    <div className="chat-focused-layout">
      <CompactHeader />
      
      <div className="chat-main-area">
        <div className="messages-area">
          {messageHistory.length === 0 && (
            <div className="welcome-message">
              <div className="welcome-content">
                <h2>👋 Welcome to LiveRamp AI Assistant</h2>
                <p>I'm in <strong>{modeConfig.name}</strong> mode, ready to help with {modeConfig.description.toLowerCase()}.</p>
                
                <div className="quick-suggestions">
                  <p><strong>Try asking:</strong></p>
                  {getQuickActions().map((action, index) => (
                    <button 
                      key={index} 
                      className="suggestion-pill"
                      onClick={() => handleSendMessage(action)}
                    >
                      {action}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          )}
          
          {messageHistory.map((message: any, index: number) => (
            <div key={index} className={`message ${message.type}`}>
              <div className="message-content">{message.content}</div>
            </div>
          ))}
          
          {isLoading && <TypingIndicator isVisible={true} />}
          <div ref={messagesEndRef} />
        </div>
        
        <div className="chat-input-area">
          <ChatInput
            onSendMessage={handleSendMessage}
            isLoading={isLoading}
            placeholder={`Ask your ${modeConfig.name.toLowerCase()} a question...`}
          />
        </div>
      </div>
    </div>
  );
};

export default ChatFocusedLayout;