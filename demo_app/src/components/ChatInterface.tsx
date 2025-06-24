import React, { useState, useRef, useEffect } from 'react';
import DemoErrorHandler from './DemoErrorHandler';
import { useConversation } from '../contexts/ConversationContext';
import { useChatMode } from '../contexts/ChatModeContext';
import { ChatMessage as ModeChatMessage } from '../types/ChatModes';
import ContextualPromptService from '../services/ContextualPromptService';
import EnhancedChatService from '../services/EnhancedChatService';
import ModeSwitcher from './chat/ModeSwitcher';
import EnhancedChatMessage from './chat/EnhancedChatMessage';

interface LegacyChatMessage {
  id: string;
  type: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  metadata?: {
    isAiPowered?: boolean;
    queryExecuted?: boolean;
    processingTime?: number;
    toolsUsed?: string[];
    mode?: string;
    confidenceScore?: number;
    businessImpact?: string;
    competitiveAdvantages?: string[];
    suggestedActions?: string[];
  };
}

const ChatInterface: React.FC = () => {
  const { 
    conversationState, 
    templateContext, 
    currentPage, 
    addMessage, 
    updateTemplateContext 
  } = useConversation();
  
  const { 
    modeState, 
    getCurrentModeConfig,
    getSystemPrompt,
    isCustomerSupportMode,
    addMessage: addModeMessage
  } = useChatMode();
  
  const getWelcomeMessage = (): LegacyChatMessage => {
    const modeConfig = getCurrentModeConfig();
    let content = `${modeConfig.icon} **Welcome to LiveRamp AI Assistant** - ${modeConfig.name}\n\n`;
    
    if (isCustomerSupportMode()) {
      content += `I'm your **Customer Support Specialist** for LiveRamp APIs:\n• 🎯 **Instant Feasibility Assessments** for customer requests\n• 🏭 **Industry-Specific Guidance** (retail, finance, automotive)\n• 💪 **Competitive Advantages** with proof points\n• ⏱️ **Implementation Timelines** and complexity estimates\n• 📋 **Customer-Ready Talking Points** for sales teams\n\nTry: "Customer wants lookalike modeling" or "Can we do real-time attribution?"`;
    } else {
      content += `I'm your **Technical Implementation Expert** for LiveRamp APIs:\n• 🔧 **API Methods & Code Examples**\n• 📚 **Implementation Patterns & Best Practices**\n• 🛡️ **Security & Compliance Guidance**\n• ⚡ **Performance Optimization Tips**\n• 🔍 **Troubleshooting Support**\n\nTry: "Show me identity resolution API" or "How to implement secure data collaboration?"`;
    }
    
    return {
      id: '1',
      type: 'assistant',
      content,
      timestamp: new Date(),
      metadata: {
        isAiPowered: true,
        processingTime: 0,
        toolsUsed: ['initialization'],
        mode: modeState.currentMode
      }
    };
  };

  const [messages, setMessages] = useState<LegacyChatMessage[]>([getWelcomeMessage()]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [retryAttempts, setRetryAttempts] = useState(0);
  const [contextualPrompts, setContextualPrompts] = useState<string[]>([]);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const promptService = ContextualPromptService.getInstance();
  const enhancedChatService = EnhancedChatService.getInstance();
  
  const currentModeConfig = getCurrentModeConfig();
  
  // Convert legacy messages to mode messages for enhanced rendering
  const convertToModeMessage = (message: LegacyChatMessage): ModeChatMessage => ({
    id: message.id,
    type: message.type,
    content: message.content,
    timestamp: message.timestamp,
    mode: modeState.currentMode,
    metadata: message.metadata
  });

  // Helper functions to extract context from queries
  const extractIndustryFromQuery = (query: string): string | undefined => {
    const queryLower = query.toLowerCase();
    if (queryLower.includes('retail') || queryLower.includes('e-commerce') || queryLower.includes('shopping')) {
      return 'retail';
    }
    if (queryLower.includes('finance') || queryLower.includes('bank') || queryLower.includes('credit')) {
      return 'finance';
    }
    if (queryLower.includes('automotive') || queryLower.includes('car') || queryLower.includes('vehicle')) {
      return 'automotive';
    }
    return undefined;
  };

  const extractCustomerSizeFromQuery = (query: string): string | undefined => {
    const queryLower = query.toLowerCase();
    if (queryLower.includes('enterprise') || queryLower.includes('large')) {
      return 'enterprise';
    }
    if (queryLower.includes('mid-market') || queryLower.includes('medium')) {
      return 'mid-market';
    }
    if (queryLower.includes('small') || queryLower.includes('startup')) {
      return 'small';
    }
    return undefined;
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Update welcome message when mode changes
  useEffect(() => {
    setMessages([getWelcomeMessage()]);
  }, [modeState.currentMode, getCurrentModeConfig, isCustomerSupportMode]);

  // Generate contextual prompts based on current state
  useEffect(() => {
    const generatePrompts = () => {
      const prompts = promptService.generateContextualPrompts(
        conversationState,
        templateContext,
        5
      );
      setContextualPrompts(prompts);
    };

    generatePrompts();
  }, [conversationState, templateContext, currentPage, promptService]);

  const sendMessage = async (messageText?: string) => {
    const textToSend = messageText || inputValue;
    if (!textToSend.trim() || isLoading) return;

    const startTime = Date.now();
    const userMessage: LegacyChatMessage = {
      id: Date.now().toString(),
      type: 'user',
      content: textToSend,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    if (!messageText) setInputValue('');
    setIsLoading(true);
    
    // Track message in conversation context
    addMessage('user', textToSend);

    try {
      const apiUrl = process.env.REACT_APP_API_URL || '';
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 30000); // 30 second timeout

      // Use mode-specific endpoint if in customer support mode
      const endpoint = isCustomerSupportMode() ? '/api/customer-support/assess' : '/api/enhanced-chat';
      
      const requestBody = isCustomerSupportMode() 
        ? { 
            query: textToSend,
            industry: extractIndustryFromQuery(textToSend),
            customerSize: extractCustomerSizeFromQuery(textToSend)
          }
        : { user_input: textToSend };

      const response = await fetch(`${apiUrl}${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
        signal: controller.signal
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      const processingTime = Date.now() - startTime;
      
      // Handle mode-specific response format
      const responseContent = isCustomerSupportMode() 
        ? (data.summary || data.response || 'I processed your request successfully.')
        : (data.response || 'I processed your request successfully.');

      const assistantMessage: LegacyChatMessage = {
        id: (Date.now() + 1).toString(),
        type: 'assistant',
        content: responseContent,
        timestamp: new Date(),
        metadata: {
          isAiPowered: data.ai_powered || isCustomerSupportMode(),
          queryExecuted: data.query_executed || false,
          processingTime,
          toolsUsed: data.tools_used || [],
          mode: modeState.currentMode,
          // Customer support specific metadata
          confidenceScore: data.confidence === 'high' ? 0.9 : (data.confidence === 'medium' ? 0.7 : 0.5),
          businessImpact: data.business_value,
          competitiveAdvantages: data.competitive_advantage,
          suggestedActions: data.next_steps
        }
      };

      setMessages(prev => [...prev, assistantMessage]);
      setRetryAttempts(0); // Reset retry count on success
      
      // Track assistant message in conversation context
      addMessage('assistant', responseContent);
      
      // Also track in mode context
      addModeMessage({
        id: assistantMessage.id,
        type: 'assistant',
        content: responseContent,
        timestamp: assistantMessage.timestamp,
        metadata: assistantMessage.metadata
      });
      
      // Update template context if response contains template data
      if (data.response && data.response.includes('template')) {
        // Try to extract template information from response
        const templateMatch = data.response.match(/(\d+)\s+(ready|available|template)/i);
        if (templateMatch) {
          const readyCount = parseInt(templateMatch[1]) || 0;
          updateTemplateContext({
            totalTemplates: readyCount + 1,
            readyTemplates: readyCount,
            missingDatasetTemplates: 1,
            categories: ['Sentiment Analysis', 'Location Data', 'Pattern of Life'],
            hasLocationData: true,
            hasSentimentAnalysis: true,
            hasPatternOfLife: true,
            hasCombinedAnalysis: true
          });
        }
      }
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
      
      const assistantMessage: LegacyChatMessage = {
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
    // Strip emoji from question for input
    const cleanQuestion = question.replace(/^[^\w\s]+\s*/, '');
    setInputValue(cleanQuestion);
  };

  const getContextualPromptHeader = (): string => {
    const { conversationLength, hasViewedTemplates, hasActiveQuery, hasCompletedQuery } = conversationState;
    
    if (conversationLength === 0) {
      return "🚀 Get Started:";
    } else if (currentPage === 'cleanrooms' && hasViewedTemplates) {
      return "🎯 Ready to Execute:";
    } else if (hasActiveQuery) {
      return "⏱️ Monitor Progress:";
    } else if (hasCompletedQuery) {
      return "📊 Next Steps:";
    } else if (currentPage === 'cleanrooms') {
      return "🏛️ Cleanroom Actions:";
    } else if (currentPage === 'api_explorer') {
      return "⚙️ API Testing:";
    } else {
      return "💡 Suggestions:";
    }
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

  // Use mode-specific prompts
  const getModeSpecificPrompts = (): string[] => {
    if (isCustomerSupportMode()) {
      return [
        "🛒 Customer wants lookalike modeling for retail",
        "🏦 Can we support financial compliance requirements?",
        "🚗 Real-time attribution for automotive campaigns",
        "🔗 Identity resolution across platforms",
        "📊 Customer segmentation capabilities"
      ];
    } else {
      return [
        "🔧 Show me identity resolution API examples",
        "📚 Best practices for secure data collaboration",
        "⚡ Performance optimization for large datasets",
        "🛡️ GDPR compliance implementation guide",
        "🔍 Troubleshoot API integration issues"
      ];
    }
  };

  // Use contextual prompts instead of static questions
  const suggestedQuestions = contextualPrompts.length > 0 ? contextualPrompts : getModeSpecificPrompts();

  return (
    <DemoErrorHandler onError={handleError} onRetry={handleRetry}>
      <div className="chat-interface">
        {/* Add Mode Switcher */}
        <div className="chat-mode-switcher">
          <ModeSwitcher />
        </div>
        
        <div className="chat-messages">
          {messages.map((message) => (
            <EnhancedChatMessage key={message.id} message={convertToModeMessage(message)} />
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
          <p>{getContextualPromptHeader()}</p>
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