import React, { createContext, useContext, useState, useCallback, useEffect, ReactNode } from 'react';
import {
  ChatMode,
  ChatModeState,
  BusinessContext,
  APIContext,
  ChatMessage,
  UserPreferences,
  DEFAULT_USER_PREFERENCES,
  CHAT_MODE_CONFIGS
} from '../types/ChatModes';

interface ChatModeContextType {
  modeState: ChatModeState;
  switchMode: (mode: ChatMode) => void;
  updateBusinessContext: (context: Partial<BusinessContext>) => void;
  updateAPIContext: (context: Partial<APIContext>) => void;
  addMessage: (message: Omit<ChatMessage, 'mode'>) => void;
  updatePreferences: (preferences: Partial<UserPreferences>) => void;
  getCurrentModeConfig: () => typeof CHAT_MODE_CONFIGS[ChatMode];
  getSystemPrompt: () => string;
  isManagerMode: () => boolean;
  isAPIExpertMode: () => boolean;
}

const ChatModeContext = createContext<ChatModeContextType | undefined>(undefined);

interface ChatModeProviderProps {
  children: ReactNode;
}

export const ChatModeProvider: React.FC<ChatModeProviderProps> = ({ children }) => {
  const [modeState, setModeState] = useState<ChatModeState>({
    currentMode: ChatMode.MANAGER,
    conversationHistory: [],
    preferences: DEFAULT_USER_PREFERENCES
  });

  // Initialize contexts on mount
  useEffect(() => {
    // Initialize business context with default values
    const defaultBusinessContext: BusinessContext = {
      cleanroomCount: 0,
      activeQueries: 0,
      pendingExports: 0,
      lastUpdate: new Date(),
      userRole: 'manager',
      permissions: ['read', 'execute']
    };

    // Initialize API context with default values
    const defaultAPIContext: APIContext = {
      availableTools: [],
      apiVersion: '2.0',
      limitations: [],
      recentChanges: [],
      capabilityMatrix: {}
    };

    setModeState(prev => ({
      ...prev,
      businessContext: defaultBusinessContext,
      apiContext: defaultAPIContext
    }));

    // Load contexts from API
    loadBusinessContext();
    loadAPIContext();
  }, []);

  const loadBusinessContext = async () => {
    try {
      const response = await fetch('/api/business-context');
      if (response.ok) {
        const context = await response.json();
        updateBusinessContext(context);
      }
    } catch (error) {
      console.warn('Failed to load business context:', error);
    }
  };

  const loadAPIContext = async () => {
    try {
      const response = await fetch('/api/api-context');
      if (response.ok) {
        const context = await response.json();
        updateAPIContext(context);
      }
    } catch (error) {
      console.warn('Failed to load API context:', error);
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

  const updateBusinessContext = useCallback((context: Partial<BusinessContext>) => {
    setModeState(prev => ({
      ...prev,
      businessContext: {
        ...prev.businessContext!,
        ...context
      }
    }));
  }, []);

  const updateAPIContext = useCallback((context: Partial<APIContext>) => {
    setModeState(prev => ({
      ...prev,
      apiContext: {
        ...prev.apiContext!,
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
    if (modeState.currentMode === ChatMode.MANAGER && modeState.businessContext) {
      prompt += `\n\nCurrent Business Context:
- Active Cleanrooms: ${modeState.businessContext.cleanroomCount}
- Running Queries: ${modeState.businessContext.activeQueries}
- Pending Exports: ${modeState.businessContext.pendingExports}
- User Role: ${modeState.businessContext.userRole}
- Last Update: ${modeState.businessContext.lastUpdate.toISOString()}`;
    }

    if (modeState.currentMode === ChatMode.API_EXPERT && modeState.apiContext) {
      prompt += `\n\nCurrent API Context:
- Available Tools: ${modeState.apiContext.availableTools.length}
- API Version: ${modeState.apiContext.apiVersion}
- Recent Changes: ${modeState.apiContext.recentChanges.length > 0 ? modeState.apiContext.recentChanges.join(', ') : 'None'}`;
    }

    return prompt;
  }, [modeState, getCurrentModeConfig]);

  const isManagerMode = useCallback(() => {
    return modeState.currentMode === ChatMode.MANAGER;
  }, [modeState.currentMode]);

  const isAPIExpertMode = useCallback(() => {
    return modeState.currentMode === ChatMode.API_EXPERT;
  }, [modeState.currentMode]);

  const value: ChatModeContextType = {
    modeState,
    switchMode,
    updateBusinessContext,
    updateAPIContext,
    addMessage,
    updatePreferences,
    getCurrentModeConfig,
    getSystemPrompt,
    isManagerMode,
    isAPIExpertMode
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