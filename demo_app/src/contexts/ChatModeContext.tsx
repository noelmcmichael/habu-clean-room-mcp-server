import React, { createContext, useContext, useState, useCallback, useEffect, ReactNode } from 'react';
import {
  ChatMode,
  ChatModeState,
  CustomerSupportContext,
  TechnicalContext,
  ChatMessage,
  UserPreferences,
  DEFAULT_USER_PREFERENCES,
  CHAT_MODE_CONFIGS
} from '../types/ChatModes';

interface ChatModeContextType {
  modeState: ChatModeState;
  switchMode: (mode: ChatMode) => void;
  updateSupportContext: (context: Partial<CustomerSupportContext>) => void;
  updateTechnicalContext: (context: Partial<TechnicalContext>) => void;
  addMessage: (message: Omit<ChatMessage, 'mode'>) => void;
  updatePreferences: (preferences: Partial<UserPreferences>) => void;
  getCurrentModeConfig: () => typeof CHAT_MODE_CONFIGS[ChatMode];
  getSystemPrompt: () => string;
  isCustomerSupportMode: () => boolean;
  isTechnicalExpertMode: () => boolean;
}

const ChatModeContext = createContext<ChatModeContextType | undefined>(undefined);

interface ChatModeProviderProps {
  children: ReactNode;
}

export const ChatModeProvider: React.FC<ChatModeProviderProps> = ({ children }) => {
  const [modeState, setModeState] = useState<ChatModeState>({
    currentMode: ChatMode.CUSTOMER_SUPPORT,
    conversationHistory: [],
    preferences: DEFAULT_USER_PREFERENCES
  });

  // Initialize contexts on mount
  useEffect(() => {
    // Initialize support context with default values
    const defaultSupportContext: CustomerSupportContext = {
      commonQuestions: [],
      industryFocus: ['retail', 'automotive', 'finance'],
      customerTier: 'enterprise',
      supportLevel: 'standard',
      escalationThreshold: 3,
      lastUpdate: new Date()
    };

    // Initialize technical context with default values
    const defaultTechnicalContext: TechnicalContext = {
      availableTools: [],
      apiVersion: '2.0',
      limitations: [],
      recentChanges: [],
      capabilityMatrix: {},
      documentationVersion: '2.0.1',
      integrationPatterns: []
    };

    setModeState(prev => ({
      ...prev,
      supportContext: defaultSupportContext,
      technicalContext: defaultTechnicalContext
    }));

    // Load contexts from API
    loadSupportContext();
    loadTechnicalContext();
  }, []);

  const loadSupportContext = async () => {
    try {
      const response = await fetch('/api/support-context');
      if (response.ok) {
        const context = await response.json();
        updateSupportContext(context);
      }
    } catch (error) {
      console.warn('Failed to load support context:', error);
    }
  };

  const loadTechnicalContext = async () => {
    try {
      const response = await fetch('/api/technical-context');
      if (response.ok) {
        const context = await response.json();
        updateTechnicalContext(context);
      }
    } catch (error) {
      console.warn('Failed to load technical context:', error);
    }
  };

  const switchMode = useCallback((mode: ChatMode) => {
    setModeState(prev => ({
      ...prev,
      currentMode: mode,
      // Clear conversation history when switching modes (optional)
      // conversationHistory: []
    }));
  }, []);

  const updateSupportContext = useCallback((context: Partial<CustomerSupportContext>) => {
    setModeState(prev => ({
      ...prev,
      supportContext: {
        ...prev.supportContext!,
        ...context
      }
    }));
  }, []);

  const updateTechnicalContext = useCallback((context: Partial<TechnicalContext>) => {
    setModeState(prev => ({
      ...prev,
      technicalContext: {
        ...prev.technicalContext!,
        ...context
      }
    }));
  }, []);

  const addMessage = useCallback((message: Omit<ChatMessage, 'mode'>) => {
    const fullMessage: ChatMessage = {
      ...message,
      mode: modeState.currentMode
    };

    setModeState(prev => ({
      ...prev,
      conversationHistory: [...prev.conversationHistory, fullMessage]
    }));
  }, [modeState.currentMode]);

  const updatePreferences = useCallback((preferences: Partial<UserPreferences>) => {
    setModeState(prev => ({
      ...prev,
      preferences: {
        ...prev.preferences,
        ...preferences
      }
    }));
  }, []);

  const getCurrentModeConfig = useCallback(() => {
    return CHAT_MODE_CONFIGS[modeState.currentMode];
  }, [modeState.currentMode]);

  const getSystemPrompt = useCallback(() => {
    const config = getCurrentModeConfig();
    let prompt = config.systemPrompt;

    // Add context-specific information to the prompt
    if (modeState.currentMode === ChatMode.CUSTOMER_SUPPORT && modeState.supportContext) {
      prompt += `\n\nCurrent Support Context:
- Customer Tier: ${modeState.supportContext.customerTier}
- Industry Focus: ${modeState.supportContext.industryFocus.join(', ')}
- Support Level: ${modeState.supportContext.supportLevel}
- Employee Role: ${modeState.preferences.employeeRole}
- Last Update: ${modeState.supportContext.lastUpdate.toISOString()}`;
    }

    if (modeState.currentMode === ChatMode.TECHNICAL_EXPERT && modeState.technicalContext) {
      prompt += `\n\nCurrent Technical Context:
- Available Tools: ${modeState.technicalContext.availableTools.length}
- API Version: ${modeState.technicalContext.apiVersion}
- Documentation Version: ${modeState.technicalContext.documentationVersion}
- Recent Changes: ${modeState.technicalContext.recentChanges.length > 0 ? modeState.technicalContext.recentChanges.join(', ') : 'None'}`;
    }

    return prompt;
  }, [modeState, getCurrentModeConfig]);

  const isCustomerSupportMode = useCallback(() => {
    return modeState.currentMode === ChatMode.CUSTOMER_SUPPORT;
  }, [modeState.currentMode]);

  const isTechnicalExpertMode = useCallback(() => {
    return modeState.currentMode === ChatMode.TECHNICAL_EXPERT;
  }, [modeState.currentMode]);

  const value: ChatModeContextType = {
    modeState,
    switchMode,
    updateSupportContext,
    updateTechnicalContext,
    addMessage,
    updatePreferences,
    getCurrentModeConfig,
    getSystemPrompt,
    isCustomerSupportMode,
    isTechnicalExpertMode
  };

  return (
    <ChatModeContext.Provider value={value}>
      {children}
    </ChatModeContext.Provider>
  );
};

export const useChatMode = (): ChatModeContextType => {
  const context = useContext(ChatModeContext);
  if (context === undefined) {
    throw new Error('useChatMode must be used within a ChatModeProvider');
  }
  return context;
};

export default ChatModeContext;