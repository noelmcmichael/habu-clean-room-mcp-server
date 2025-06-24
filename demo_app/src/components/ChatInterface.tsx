import React, { useState, useRef, useEffect } from 'react';
import DemoErrorHandler from './DemoErrorHandler';

interface ChatMessage {
  id: string;
  type: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  metadata?: {
    isAiPowered?: boolean;
    queryExecuted?: boolean;
    processingTime?: number;
    toolsUsed?: string[];
  };
}

const ChatInterface: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: '1',
      type: 'assistant',
      content: '🚀 **Welcome to LiveRamp Clean Room Demo** - Your AI-Powered Data Collaboration Assistant!\n\nI\'m running in **Full Production Mode** with:\n• 🤖 **GPT-4 AI Intelligence** for natural conversation\n• 🔧 **Interactive Query Execution** on real cleanroom data\n• 📊 **Enhanced Analytics** with AI-powered metadata\n• 🎯 **Ready Templates** with business intelligence\n\nTry: "Run a sentiment analysis" or "What analytics can I run on my cleanroom?"',
      timestamp: new Date(),
      metadata: {
        isAiPowered: true,
        processingTime: 0,
        toolsUsed: ['initialization']
      }
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [retryAttempts, setRetryAttempts] = useState(0);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async (messageText?: string) => {
    const textToSend = messageText || inputValue;
    if (!textToSend.trim() || isLoading) return;

    const startTime = Date.now();
    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      type: 'user',
      content: textToSend,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    if (!messageText) setInputValue('');
    setIsLoading(true);

    try {
      const apiUrl = process.env.REACT_APP_API_URL || '';
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 30000); // 30 second timeout

      const response = await fetch(`${apiUrl}/api/enhanced-chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ user_input: textToSend }),
        signal: controller.signal
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      const processingTime = Date.now() - startTime;
      
      const assistantMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        type: 'assistant',
        content: data.response || 'I processed your request successfully.',
        timestamp: new Date(),
        metadata: {
          isAiPowered: data.ai_powered || false,
          queryExecuted: data.query_executed || false,
          processingTime,
          toolsUsed: data.tools_used || []
        }
      };

      setMessages(prev => [...prev, assistantMessage]);
      setRetryAttempts(0); // Reset retry count on success
    } catch (error: any) {
      console.error('Error sending message:', error);
      
      let errorMessage = 'I\'m experiencing technical difficulties. ';
      
      if (error.name === 'AbortError') {
        errorMessage += 'The request timed out. The server may be busy.';
      } else if (error.message.includes('Failed to fetch')) {
        errorMessage += 'Unable to connect to the server. Please check your connection.';
      } else {
        errorMessage += 'Please try again or use Demo Mode for your presentation.';
      }
      
      const assistantMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        type: 'assistant',
        content: errorMessage,
        timestamp: new Date(),
        metadata: {
          isAiPowered: false,
          processingTime: Date.now() - startTime
        }
      };
      setMessages(prev => [...prev, assistantMessage]);
      
      // Increment retry attempts
      setRetryAttempts(prev => prev + 1);
      
      // Re-throw for error handler
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const handleSuggestedQuestion = (question: string) => {
    setInputValue(question);
  };



  const handleRetry = async (): Promise<boolean> => {
    try {
      // Test connection with a simple health check
      const apiUrl = process.env.REACT_APP_API_URL || '';
      const response = await fetch(`${apiUrl}/api/health`);
      return response.ok;
    } catch {
      return false;
    }
  };

  const handleError = (error: any) => {
    console.error('Demo error:', error);
  };

  // Enhanced suggested questions for Phase 4
  const suggestedQuestions = [
    "🎯 Run a sentiment analysis",
    "📍 Analyze location patterns", 
    "🔧 Execute combined intelligence",
    "📊 Show my analytics templates",
    "⚡ What's ready for immediate execution?"
  ];

  return (
    <DemoErrorHandler onError={handleError} onRetry={handleRetry}>
      <div className="chat-interface">
        <div className="chat-messages">
          {messages.map((message) => (
            <div key={message.id} className={`message ${message.type}`}>
              <div className="message-content">
                <div className="message-text">{message.content}</div>
                
                {/* Enhanced message metadata for demo */}
                {message.metadata && (
                  <div className="message-metadata">
                    {message.metadata.isAiPowered && (
                      <span className="metadata-badge ai-powered">🤖 AI-Powered</span>
                    )}
                    {message.metadata.queryExecuted && (
                      <span className="metadata-badge query-executed">🔧 Query Executed</span>
                    )}
                    {message.metadata.toolsUsed && message.metadata.toolsUsed.length > 0 && (
                      <span className="metadata-badge tools-used">
                        🛠️ {message.metadata.toolsUsed.length} tool{message.metadata.toolsUsed.length > 1 ? 's' : ''} used
                      </span>
                    )}
                    {message.metadata.processingTime && message.metadata.processingTime > 0 && (
                      <span className="metadata-badge processing-time">
                        ⚡ {message.metadata.processingTime}ms
                      </span>
                    )}
                  </div>
                )}
                
                <div className="message-time">
                  {message.timestamp.toLocaleTimeString()}
                </div>
              </div>
            </div>
          ))}
          {isLoading && (
            <div className="message assistant">
              <div className="message-content">
                <div className="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
                <div className="loading-text">
                  🤖 AI Assistant processing your request...
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <div className="suggested-questions">
          <p>🚀 Quick Actions for Demo:</p>
          <div className="suggested-buttons">
            {suggestedQuestions.map((question, index) => (
              <button
                key={index}
                onClick={() => handleSuggestedQuestion(question)}
                className="suggested-question"
                disabled={isLoading}
              >
                {question}
              </button>
            ))}
          </div>
        </div>

        <div className="chat-input">
          <div className="input-container">
            <textarea
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyDown={handleKeyPress}
              placeholder="Ask me about your cleanroom analytics... (Try: 'Run a sentiment analysis')"
              disabled={isLoading}
              rows={1}
            />
            <button 
              onClick={() => sendMessage()} 
              disabled={!inputValue.trim() || isLoading}
              className="send-button"
            >
              {isLoading ? '⏳' : '🚀'} Send
            </button>
          </div>
          
          {retryAttempts > 0 && (
            <div className="retry-banner">
              ⚠️ Connection issues detected. Check system health or try again.
            </div>
          )}
        </div>
      </div>
    </DemoErrorHandler>
  );
};

export default ChatInterface;