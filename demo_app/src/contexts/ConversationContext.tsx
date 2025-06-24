/**
 * Conversation Context - Manages conversation state across the application
 * Provides context-aware data for intelligent prompt generation
 */

import React, { createContext, useContext, useReducer, useCallback, useEffect } from 'react';
import { ConversationState, TemplateContext } from '../services/ContextualPromptService';

interface ConversationContextType {
  // State
  conversationState: ConversationState;
  templateContext?: TemplateContext;
  currentPage: string;
  
  // Actions
  updateConversationState: (updates: Partial<ConversationState>) => void;
  updateTemplateContext: (context: TemplateContext) => void;
  setCurrentPage: (page: string) => void;
  addMessage: (type: 'user' | 'assistant', content: string) => void;
  resetConversation: () => void;
}

// Action types for state management
type ConversationAction = 
  | { type: 'UPDATE_CONVERSATION_STATE'; payload: Partial<ConversationState> }
  | { type: 'UPDATE_TEMPLATE_CONTEXT'; payload: TemplateContext }
  | { type: 'SET_CURRENT_PAGE'; payload: string }
  | { type: 'ADD_MESSAGE'; payload: { type: 'user' | 'assistant'; content: string } }
  | { type: 'RESET_CONVERSATION' };

interface ConversationContextState {
  conversationState: ConversationState;
  templateContext?: TemplateContext;
  currentPage: string;
  messageHistory: Array<{ type: 'user' | 'assistant'; content: string; timestamp: Date }>;
}

// Load state from localStorage with fallback
const loadPersistedState = (): ConversationContextState => {
  try {
    const persistedState = localStorage.getItem('habu-conversation-state');
    if (persistedState) {
      const parsed = JSON.parse(persistedState);
      console.log('📱 Loaded conversation state from storage');
      return parsed;
    }
  } catch (error) {
    console.warn('⚠️ Failed to load persisted state:', error);
  }
  
  // Return initial state if no persisted state or error
  return {
    conversationState: {
      hasViewedTemplates: false,
      hasSubmittedQuery: false,
      hasActiveQuery: false,
      hasCompletedQuery: false,
      hasViewedResults: false,
      availableTemplates: 0,
      readyTemplates: 0,
      currentPage: 'home',
      conversationLength: 0,
      recentTemplateCategories: []
    },
    currentPage: 'home',
    messageHistory: []
  };
};

// Initial state with persistence
const initialState: ConversationContextState = loadPersistedState();

// Persist state to localStorage
const persistState = (state: ConversationContextState) => {
  try {
    // Only persist essential data, not the full message history
    const stateToPersist = {
      ...state,
      messageHistory: state.messageHistory.slice(-10) // Keep only last 10 messages
    };
    localStorage.setItem('habu-conversation-state', JSON.stringify(stateToPersist));
  } catch (error) {
    console.warn('⚠️ Failed to persist state:', error);
  }
};

// Reducer for state management
function conversationReducer(state: ConversationContextState, action: ConversationAction): ConversationContextState {
  switch (action.type) {
    case 'UPDATE_CONVERSATION_STATE':
      return {
        ...state,
        conversationState: {
          ...state.conversationState,
          ...action.payload
        }
      };
      
    case 'UPDATE_TEMPLATE_CONTEXT':
      return {
        ...state,
        templateContext: action.payload,
        conversationState: {
          ...state.conversationState,
          availableTemplates: action.payload.totalTemplates,
          readyTemplates: action.payload.readyTemplates,
          recentTemplateCategories: action.payload.categories
        }
      };
      
    case 'SET_CURRENT_PAGE':
      return {
        ...state,
        currentPage: action.payload,
        conversationState: {
          ...state.conversationState,
          currentPage: action.payload
        }
      };
      
    case 'ADD_MESSAGE':
      const newMessage = {
        ...action.payload,
        timestamp: new Date()
      };
      
      const updatedHistory = [...state.messageHistory, newMessage];
      
      // Auto-detect conversation state changes from message content
      const messageContent = action.payload.content.toLowerCase();
      const stateUpdates: Partial<ConversationState> = {
        conversationLength: updatedHistory.length
      };
      
      // Template viewing detection
      if (messageContent.includes('template') || messageContent.includes('analytics') || 
          messageContent.includes('available') || messageContent.includes('enhanced')) {
        stateUpdates.hasViewedTemplates = true;
      }
      
      // Query submission detection
      if (messageContent.includes('submitted') || messageContent.includes('executed') || 
          messageContent.includes('query id') || messageContent.includes('running')) {
        stateUpdates.hasSubmittedQuery = true;
        stateUpdates.hasActiveQuery = true;
      }
      
      // Query completion detection
      if (messageContent.includes('completed') || messageContent.includes('finished') || 
          messageContent.includes('success') || messageContent.includes('ready')) {
        stateUpdates.hasCompletedQuery = true;
        stateUpdates.hasActiveQuery = false;
      }
      
      // Results viewing detection
      if (messageContent.includes('results') || messageContent.includes('insights') || 
          messageContent.includes('findings') || messageContent.includes('analysis')) {
        stateUpdates.hasViewedResults = true;
      }
      
      // Query status detection
      if (messageContent.includes('status') || messageContent.includes('progress')) {
        const statusMatch = messageContent.match(/(submitted|running|completed|failed|queued)/);
        if (statusMatch) {
          stateUpdates.lastQueryStatus = statusMatch[1].toUpperCase();
        }
      }
      
      return {
        ...state,
        messageHistory: updatedHistory,
        conversationState: {
          ...state.conversationState,
          ...stateUpdates
        }
      };
      
    case 'RESET_CONVERSATION':
      return {
        ...initialState,
        currentPage: state.currentPage // Preserve current page
      };
      
    default:
      return state;
  }
}

// Create context
const ConversationContext = createContext<ConversationContextType | undefined>(undefined);

// Provider component
export const ConversationProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [state, dispatch] = useReducer(conversationReducer, initialState);
  
  // Persist state on changes (debounced)
  useEffect(() => {
    const timeoutId = setTimeout(() => {
      persistState(state);
    }, 1000); // Debounce for 1 second
    
    return () => clearTimeout(timeoutId);
  }, [state]);
  
  // Actions
  const updateConversationState = useCallback((updates: Partial<ConversationState>) => {
    dispatch({ type: 'UPDATE_CONVERSATION_STATE', payload: updates });
  }, []);
  
  const updateTemplateContext = useCallback((context: TemplateContext) => {
    dispatch({ type: 'UPDATE_TEMPLATE_CONTEXT', payload: context });
  }, []);
  
  const setCurrentPage = useCallback((page: string) => {
    dispatch({ type: 'SET_CURRENT_PAGE', payload: page });
  }, []);
  
  const addMessage = useCallback((type: 'user' | 'assistant', content: string) => {
    dispatch({ type: 'ADD_MESSAGE', payload: { type, content } });
  }, []);
  
  const resetConversation = useCallback(() => {
    dispatch({ type: 'RESET_CONVERSATION' });
  }, []);
  
  // Auto-detect page changes from URL
  useEffect(() => {
    const detectPageFromUrl = () => {
      const path = window.location.pathname;
      let pageName = 'home';
      
      if (path.includes('cleanrooms')) {
        pageName = 'cleanrooms';
      } else if (path.includes('api')) {
        pageName = 'api_explorer';
      } else if (path.includes('architecture')) {
        pageName = 'architecture';
      } else if (path.includes('health')) {
        pageName = 'system_health';
      }
      
      if (pageName !== state.currentPage) {
        setCurrentPage(pageName);
      }
    };
    
    // Initial detection
    detectPageFromUrl();
    
    // Listen for navigation changes
    const handlePopState = () => {
      detectPageFromUrl();
    };
    
    window.addEventListener('popstate', handlePopState);
    
    // Also listen for pushState/replaceState (for React Router)
    const originalPushState = window.history.pushState;
    const originalReplaceState = window.history.replaceState;
    
    window.history.pushState = function(...args) {
      originalPushState.apply(this, args);
      setTimeout(detectPageFromUrl, 0);
    };
    
    window.history.replaceState = function(...args) {
      originalReplaceState.apply(this, args);
      setTimeout(detectPageFromUrl, 0);
    };
    
    return () => {
      window.removeEventListener('popstate', handlePopState);
      window.history.pushState = originalPushState;
      window.history.replaceState = originalReplaceState;
    };
  }, [state.currentPage, setCurrentPage]);
  
  const contextValue: ConversationContextType = {
    conversationState: state.conversationState,
    templateContext: state.templateContext,
    currentPage: state.currentPage,
    updateConversationState,
    updateTemplateContext,
    setCurrentPage,
    addMessage,
    resetConversation
  };
  
  return (
    <ConversationContext.Provider value={contextValue}>
      {children}
    </ConversationContext.Provider>
  );
};

// Hook for using the context
export const useConversation = (): ConversationContextType => {
  const context = useContext(ConversationContext);
  if (!context) {
    throw new Error('useConversation must be used within a ConversationProvider');
  }
  return context;
};

export default ConversationContext;