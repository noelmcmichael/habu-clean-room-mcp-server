import React, { useState, useEffect, useRef } from 'react';
import { useConversation } from '../contexts/ConversationContext';
import { useChatMode } from '../contexts/ChatModeContext';
import { ChatMessage as ModeChatMessage } from '../types/ChatModes';
import EnhancedChatMessage from './chat/EnhancedChatMessage';
import QuickActionButtons from './chat/QuickActionButtons';
import TypingIndicator from './chat/TypingIndicator';
import ChatMetrics from './chat/ChatMetrics';
import ChatInput from './chat/ChatInput';
import MessageActions from './chat/MessageActions';
import ModeSwitcher from './chat/ModeSwitcher';
import '../styles/enhanced-chat.css';

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
    codeExamples?: Array<{
      language: string;
      title: string;
      description: string;
      code: string;
      dependencies: string[];
      notes: string[];
    }>;
    apiMethods?: Array<{
      name: string;
      endpoint: string;
      method: string;
      description: string;
    }>;
    implementationSteps?: string[];
    performanceConsiderations?: string[];
    securityGuidance?: string[];
  };
}

const EnhancedChatInterface: React.FC = () => {
  const [messages, setMessages] = useState<LegacyChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [showQuickActions, setShowQuickActions] = useState(true);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  
  const { addMessage } = useConversation();
  const { 
    modeState, 
    getCurrentModeConfig,
    isCustomerSupportMode,
    isTechnicalExpertMode,
    addMessage: addModeMessage
  } = useChatMode();

  // Initialize with welcome message
  useEffect(() => {
    const welcomeMessage = getWelcomeMessage();
    setMessages([welcomeMessage]);
  }, [modeState.currentMode]);

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  const getWelcomeMessage = (): LegacyChatMessage => {
    const modeConfig = getCurrentModeConfig();
    let content = `${modeConfig.icon} **Welcome to LiveRamp AI Assistant** - ${modeConfig.name}\n\n`;
    
    if (isCustomerSupportMode()) {
      content += `I'm your **Customer Support Specialist** for LiveRamp APIs:\n• 🎯 **Instant Feasibility Assessments** for customer requests\n• 🏭 **Industry-Specific Guidance** (retail, finance, automotive)\n• 💪 **Competitive Advantages** with proof points\n• ⏱️ **Implementation Timelines** and complexity estimates\n• 📋 **Customer-Ready Talking Points** for sales teams\n\n**Ready to help with your customer questions!**`;
    } else {
      content += `I'm your **Technical Implementation Expert** for LiveRamp APIs:\n• 🔧 **API Methods & Code Examples**\n• 📚 **Implementation Patterns & Best Practices**\n• 🛡️ **Security & Compliance Guidance**\n• ⚡ **Performance Optimization Tips**\n• 🔍 **Troubleshooting Support**\n\n**Ready to help with your technical implementation!**`;
    }
    
    return {
      id: 'welcome',
      type: 'assistant',
      content,
      timestamp: new Date(),
      metadata: {
        isAiPowered: true,
        mode: modeState.currentMode
      }
    };
  };

  const extractContextFromQuery = (query: string) => {
    return {
      industry: extractIndustryFromQuery(query),
      customerSize: extractCustomerSizeFromQuery(query),
      programmingLanguage: extractLanguageFromQuery(query),
      useCase: extractUseCaseFromQuery(query),
      errorType: extractErrorFromQuery(query)
    };
  };

  const extractIndustryFromQuery = (query: string): string => {
    const industries = ['retail', 'finance', 'automotive', 'healthcare', 'media', 'entertainment'];
    const lowerQuery = query.toLowerCase();
    return industries.find(industry => lowerQuery.includes(industry)) || 'general';
  };

  const extractCustomerSizeFromQuery = (query: string): string => {
    const lowerQuery = query.toLowerCase();
    if (lowerQuery.includes('enterprise') || lowerQuery.includes('large')) return 'enterprise';
    if (lowerQuery.includes('small') || lowerQuery.includes('startup')) return 'small';
    return 'medium';
  };

  const extractLanguageFromQuery = (query: string): string => {
    const languages = ['python', 'javascript', 'java', 'curl', 'php', 'ruby'];
    const lowerQuery = query.toLowerCase();
    return languages.find(lang => lowerQuery.includes(lang)) || 'python';
  };

  const extractUseCaseFromQuery = (query: string): string => {
    const useCases = ['identity_resolution', 'audience_segmentation', 'lookalike_modeling', 'attribution'];
    const lowerQuery = query.toLowerCase();
    if (lowerQuery.includes('identity') || lowerQuery.includes('resolution')) return 'identity_resolution';
    if (lowerQuery.includes('audience') || lowerQuery.includes('segment')) return 'audience_segmentation';
    if (lowerQuery.includes('lookalike') || lowerQuery.includes('similar')) return 'lookalike_modeling';
    if (lowerQuery.includes('attribution') || lowerQuery.includes('tracking')) return 'attribution';
    return 'general_api_integration';
  };

  const extractErrorFromQuery = (query: string): string => {
    const lowerQuery = query.toLowerCase();
    if (lowerQuery.includes('401') || lowerQuery.includes('unauthorized')) return '401_authentication';
    if (lowerQuery.includes('403') || lowerQuery.includes('forbidden')) return '403_authorization';
    if (lowerQuery.includes('429') || lowerQuery.includes('rate limit')) return '429_rate_limit';
    if (lowerQuery.includes('timeout') || lowerQuery.includes('slow')) return 'timeout';
    return 'general_error';
  };

  const sendMessage = async (messageText: string) => {
    if (!messageText.trim() || isLoading) return;

    const startTime = Date.now();
    const userMessage: LegacyChatMessage = {
      id: Date.now().toString(),
      type: 'user',
      content: messageText,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);
    setShowQuickActions(false);

    // Track message in contexts
    addMessage('user', messageText);
    addModeMessage({
      id: Date.now().toString(),
      type: 'user',
      content: messageText,
      timestamp: new Date()
    });

    try {
      const apiUrl = process.env.REACT_APP_API_URL || '';
      const context = extractContextFromQuery(messageText);
      
      const endpoint = isCustomerSupportMode() 
        ? '/api/customer-support/assess' 
        : isTechnicalExpertMode() 
        ? '/api/technical-expert/query'
        : '/api/enhanced-chat';
      
      const requestBody = isCustomerSupportMode() 
        ? { 
            query: messageText,
            industry: context.industry,
            customerSize: context.customerSize
          }
        : isTechnicalExpertMode()
        ? {
            query: messageText,
            context: {
              programmingLanguage: context.programmingLanguage,
              useCase: context.useCase,
              errorType: context.errorType
            }
          }
        : { user_input: messageText };

      const response = await fetch(`${apiUrl}${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
        signal: AbortSignal.timeout(30000)
      });

      if (!response.ok) {
        throw new Error(`API request failed: ${response.status} ${response.statusText}`);
      }

      const data = await response.json();
      const processingTime = Date.now() - startTime;

      const responseContent = isCustomerSupportMode() 
        ? (data.summary || 'Customer support response')
        : isTechnicalExpertMode()
        ? (data.summary || 'Technical response') 
        : (data.response || 'Standard response');

      const assistantMessage: LegacyChatMessage = {
        id: (Date.now() + 1).toString(),
        type: 'assistant',
        content: responseContent,
        timestamp: new Date(),
        metadata: {
          isAiPowered: true,
          queryExecuted: true,
          processingTime,
          mode: modeState.currentMode,
          toolsUsed: data.tools_used || [],
          confidenceScore: data.confidence_score,
          businessImpact: data.business_impact,
          competitiveAdvantages: data.competitive_advantages,
          suggestedActions: data.suggested_actions,
          codeExamples: data.code_examples,
          apiMethods: data.api_methods,
          implementationSteps: data.implementation_steps,
          performanceConsiderations: data.performance_considerations,
          securityGuidance: data.security_guidance
        }
      };

      setMessages(prev => [...prev, assistantMessage]);
      addMessage('assistant', responseContent);
      addModeMessage({
        id: assistantMessage.id,
        type: 'assistant',
        content: responseContent,
        timestamp: new Date()
      });

    } catch (error) {
      console.error('Error sending message:', error);
      
      const errorMessage: LegacyChatMessage = {
        id: (Date.now() + 1).toString(),
        type: 'assistant',
        content: `I apologize, but I'm having trouble connecting to the API. Please check your connection and try again.\n\nError: ${error instanceof Error ? error.message : 'Unknown error'}`,
        timestamp: new Date(),
        metadata: {
          isAiPowered: false,
          mode: modeState.currentMode
        }
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleQuickAction = (query: string) => {
    sendMessage(query);
  };

  const handleCopyMessage = (content: string) => {
    navigator.clipboard.writeText(content);
    // You could add a toast notification here
  };

  const handleRegenerateMessage = (messageId: string) => {
    // Find the user message that preceded this assistant message
    const messageIndex = messages.findIndex(m => m.id === messageId);
    if (messageIndex > 0) {
      const previousUserMessage = messages[messageIndex - 1];
      if (previousUserMessage.type === 'user') {
        // Remove the assistant message and regenerate
        setMessages(prev => prev.filter(m => m.id !== messageId));
        sendMessage(previousUserMessage.content);
      }
    }
  };

  const handleFeedback = (messageId: string, feedback: 'positive' | 'negative', comment?: string) => {
    // Log feedback for analytics
    console.log('User feedback:', { messageId, feedback, comment, mode: modeState.currentMode });
    
    // You could send this to an analytics service
    // analytics.track('message_feedback', { messageId, feedback, comment, mode: modeState.currentMode });
  };

  return (
    <div className="enhanced-chat-interface" data-mode={modeState.currentMode}>
      <div className="chat-header">
        <div className="header-content">
          <div className="mode-info">
            <ModeSwitcher />
          </div>
          <div className="metrics-panel">
            <ChatMetrics className="header-metrics" />
          </div>
        </div>
      </div>

      <div className="chat-body">
        <div className="messages-container">
          {messages.map((message) => (
            <div key={message.id} className="message-wrapper">
              <EnhancedChatMessage
                message={{
                  id: message.id,
                  type: message.type,
                  content: message.content,
                  timestamp: message.timestamp,
                  metadata: message.metadata,
                  mode: modeState.currentMode
                }}
              />
              
              {message.type === 'assistant' && message.id !== 'welcome' && (
                <MessageActions
                  messageId={message.id}
                  messageContent={message.content}
                  messageType={message.type}
                  onCopy={handleCopyMessage}
                  onRegenerate={handleRegenerateMessage}
                  onFeedback={handleFeedback}
                />
              )}
            </div>
          ))}
          
          {isLoading && (
            <TypingIndicator 
              isVisible={true} 
              message={`${getCurrentModeConfig().name} is analyzing your request...`}
            />
          )}
          
          <div ref={messagesEndRef} />
        </div>

        {showQuickActions && messages.length <= 1 && (
          <div className="quick-actions-panel">
            <QuickActionButtons onQuickAction={handleQuickAction} />
          </div>
        )}
      </div>

      <div className="chat-input-panel">
        <ChatInput
          onSendMessage={sendMessage}
          isLoading={isLoading}
          placeholder={`Ask your ${getCurrentModeConfig().name.toLowerCase()} a question...`}
        />
      </div>
    </div>
  );
};

export default EnhancedChatInterface;