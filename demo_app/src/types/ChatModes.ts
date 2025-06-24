// Chat Mode Types and Interfaces

export enum ChatMode {
  MANAGER = 'manager',
  API_EXPERT = 'api_expert'
}

export interface ChatModeConfig {
  mode: ChatMode;
  name: string;
  description: string;
  icon: string;
  systemPrompt: string;
  capabilities: string[];
  responseStyle: ResponseStyle;
}

export interface ResponseStyle {
  tone: 'business' | 'technical';
  verbosity: 'brief' | 'detailed';
  format: 'executive' | 'educational';
  includeActions: boolean;
  includeExpansion: boolean;
}

export interface BusinessContext {
  cleanroomCount: number;
  activeQueries: number;
  pendingExports: number;
  lastUpdate: Date;
  userRole: string;
  permissions: string[];
}

export interface APIContext {
  availableTools: string[];
  apiVersion: string;
  limitations: string[];
  recentChanges: string[];
  capabilityMatrix: Record<string, boolean>;
}

export interface ChatModeState {
  currentMode: ChatMode;
  businessContext?: BusinessContext;
  apiContext?: APIContext;
  conversationHistory: ChatMessage[];
  preferences: UserPreferences;
}

export interface ChatMessage {
  id: string;
  type: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  mode: ChatMode;
  metadata?: {
    isAiPowered?: boolean;
    queryExecuted?: boolean;
    processingTime?: number;
    toolsUsed?: string[];
    confidenceScore?: number;
    sourceValidation?: boolean;
    businessImpact?: string;
  };
}

export interface UserPreferences {
  defaultMode: ChatMode;
  verbosity: 'brief' | 'detailed';
  showTechnicalDetails: boolean;
  includeMetrics: boolean;
  autoExpand: boolean;
}

// Mode Configuration Constants
export const CHAT_MODE_CONFIGS: Record<ChatMode, ChatModeConfig> = {
  [ChatMode.MANAGER]: {
    mode: ChatMode.MANAGER,
    name: 'Manager Mode',
    description: 'Business-focused cleanroom operations and insights',
    icon: '📊',
    systemPrompt: `You are a Senior Data Operations Manager expert for LiveRamp Clean Room operations. 
Your role is to provide clear, actionable business insights about cleanroom performance, operations, and opportunities.

Key Responsibilities:
- Translate technical data into business impact
- Provide executive-level summaries and recommendations
- Focus on KPIs, ROI, and operational efficiency
- Identify action items and next steps
- Explain complex technical concepts in business terms

Communication Style:
- Brief, professional, action-oriented
- Use business terminology and metrics
- Include visual indicators (📊 📈 ⚡ 💡)
- Always offer to expand on details
- Provide clear next steps

Always ground responses in real API data and current system status.`,
    capabilities: [
      'Real-time cleanroom monitoring',
      'Business impact analysis',
      'Performance benchmarking',
      'Resource optimization',
      'Executive reporting',
      'Action item generation'
    ],
    responseStyle: {
      tone: 'business',
      verbosity: 'brief',
      format: 'executive',
      includeActions: true,
      includeExpansion: true
    }
  },
  [ChatMode.API_EXPERT]: {
    mode: ChatMode.API_EXPERT,
    name: 'API Expert',
    description: 'Technical guidance on Habu API capabilities and implementation',
    icon: '🔧',
    systemPrompt: `You are a Senior API Integration Specialist and expert on the Habu/LiveRamp Clean Room API.
Your role is to provide accurate, helpful technical guidance about API capabilities, methods, and best practices.

Key Responsibilities:
- Explain API methods, parameters, and data models
- Provide implementation guidance and examples
- Clarify capabilities and limitations
- Suggest best practices and optimization strategies
- Help users understand "art of the possible"

Communication Style:
- Clear, educational, technically accurate
- Use examples and practical scenarios
- Include code snippets and method signatures
- Explain concepts progressively (simple to complex)
- Always validate against real API schema

CRITICAL: Never make up API methods or capabilities. Always base responses on actual API documentation and real-time validation.`,
    capabilities: [
      'API method documentation',
      'Parameter explanation',
      'Data model guidance',
      'Implementation examples',
      'Best practices',
      'Capability discovery',
      'Limitation awareness',
      'Integration patterns'
    ],
    responseStyle: {
      tone: 'technical',
      verbosity: 'detailed',
      format: 'educational',
      includeActions: false,
      includeExpansion: true
    }
  }
};

export const DEFAULT_USER_PREFERENCES: UserPreferences = {
  defaultMode: ChatMode.MANAGER,
  verbosity: 'brief',
  showTechnicalDetails: false,
  includeMetrics: true,
  autoExpand: false
};