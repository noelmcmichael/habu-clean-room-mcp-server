// Chat Mode Types and Interfaces

export enum ChatMode {
  CUSTOMER_SUPPORT = 'customer_support',
  TECHNICAL_EXPERT = 'technical_expert'
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

export interface CustomerSupportContext {
  commonQuestions: string[];
  industryFocus: string[];
  customerTier: string;
  supportLevel: string;
  escalationThreshold: number;
  lastUpdate: Date;
}

export interface TechnicalContext {
  availableTools: string[];
  apiVersion: string;
  limitations: string[];
  recentChanges: string[];
  capabilityMatrix: Record<string, boolean>;
  documentationVersion: string;
  integrationPatterns: string[];
}

export interface ChatModeState {
  currentMode: ChatMode;
  supportContext?: CustomerSupportContext;
  technicalContext?: TechnicalContext;
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
    // Customer Support specific
    competitiveAdvantages?: string[];
    suggestedActions?: string[];
    // Technical Expert specific
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

export interface UserPreferences {
  defaultMode: ChatMode;
  verbosity: 'brief' | 'detailed';
  showTechnicalDetails: boolean;
  includeCompetitiveInfo: boolean;
  employeeRole: 'support' | 'sales' | 'engineering' | 'product' | 'other';
  autoExpand: boolean;
}

// Mode Configuration Constants
export const CHAT_MODE_CONFIGS: Record<ChatMode, ChatModeConfig> = {
  [ChatMode.CUSTOMER_SUPPORT]: {
    mode: ChatMode.CUSTOMER_SUPPORT,
    name: 'Customer Support',
    description: 'Help LiveRamp employees answer customer questions about API capabilities',
    icon: '🎧',
    systemPrompt: `You are a Senior Customer Support Specialist and expert on LiveRamp's data collaboration APIs. 
Your role is to help LiveRamp employees (support, sales, solution engineers) answer customer questions accurately and persuasively.

Key Responsibilities:
- Translate customer business needs into API capability assessments
- Provide clear "yes/no" answers with supporting details
- Explain what's possible vs what's not, with alternatives
- Include competitive advantages and differentiators
- Give timeline estimates and implementation requirements
- Suggest next steps for customers

Communication Style:
- Customer-ready language (avoid internal jargon)
- Clear capability statements with confidence levels
- Include business benefits and ROI indicators
- Provide competitive talking points when relevant
- Always offer expansion into technical details
- Include risk assessments and success factors

CRITICAL: Never promise capabilities that don't exist. Always base responses on actual API documentation and current system capabilities. When uncertain, clearly state limitations.`,
    capabilities: [
      'Customer capability assessment',
      'Use case feasibility analysis',
      'Competitive positioning',
      'Implementation timeline estimation',
      'ROI and business case support',
      'Industry-specific guidance'
    ],
    responseStyle: {
      tone: 'business',
      verbosity: 'brief',
      format: 'executive',
      includeActions: true,
      includeExpansion: true
    }
  },
  [ChatMode.TECHNICAL_EXPERT]: {
    mode: ChatMode.TECHNICAL_EXPERT,
    name: 'Technical Expert',
    description: 'Deep technical guidance for engineers, PMs, and technical staff',
    icon: '🔧',
    systemPrompt: `You are a Senior Solution Engineer and expert on LiveRamp's data collaboration API technical implementation.
Your role is to provide accurate, detailed technical guidance for engineers, product managers, and technical staff.

Key Responsibilities:
- Explain API methods, parameters, and data models in detail
- Provide implementation code examples and patterns
- Clarify technical capabilities and limitations
- Suggest best practices and optimization strategies
- Help troubleshoot integration issues
- Explain privacy, security, and compliance considerations

Communication Style:
- Technical accuracy is paramount
- Use code examples and practical scenarios
- Include method signatures and parameter details
- Explain concepts with increasing complexity
- Provide performance and scaling guidance
- Always validate against real API schema

CRITICAL: Never make up API methods, parameters, or capabilities. Always base responses on actual API documentation and real-time validation. When documentation is incomplete, clearly state what needs verification.`,
    capabilities: [
      'Complete API method documentation',
      'Implementation code examples',
      'Integration pattern guidance',
      'Performance optimization',
      'Security and compliance',
      'Troubleshooting support',
      'Best practices',
      'Capability limitations'
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
  defaultMode: ChatMode.CUSTOMER_SUPPORT,
  verbosity: 'brief',
  showTechnicalDetails: false,
  includeCompetitiveInfo: true,
  employeeRole: 'support',
  autoExpand: false
};