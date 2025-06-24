/**
 * Contextual Prompt Service - Dynamic, intelligent prompt generation
 * Provides context-aware suggestions based on page, conversation state, and available data
 */

// Types for context-aware prompt generation
export interface ConversationState {
  hasViewedTemplates: boolean;
  hasSubmittedQuery: boolean;
  hasActiveQuery: boolean;
  hasCompletedQuery: boolean;
  hasViewedResults: boolean;
  lastQueryStatus?: string;
  availableTemplates?: number;
  readyTemplates?: number;
  recentTemplateCategories?: string[];
  currentPage?: string;
  conversationLength?: number;
}

export interface TemplateContext {
  totalTemplates: number;
  readyTemplates: number;
  missingDatasetTemplates: number;
  categories: string[];
  hasLocationData: boolean;
  hasSentimentAnalysis: boolean;
  hasPatternOfLife: boolean;
  hasCombinedAnalysis: boolean;
}

export interface ContextualPrompt {
  text: string;
  emoji: string;
  priority: number;
  category: 'discovery' | 'execution' | 'monitoring' | 'results' | 'exploration' | 'workflow';
  requiresTemplates?: boolean;
  requiresActiveQuery?: boolean;
  pageSpecific?: string[];
}

export class ContextualPromptService {
  private static instance: ContextualPromptService;
  
  public static getInstance(): ContextualPromptService {
    if (!ContextualPromptService.instance) {
      ContextualPromptService.instance = new ContextualPromptService();
    }
    return ContextualPromptService.instance;
  }

  // Core prompt database organized by context and priority
  private promptDatabase: Record<string, ContextualPrompt[]> = {
    // Page-specific prompts
    home_welcome: [
      { text: "What analytics can I run in my cleanroom?", emoji: "🔍", priority: 10, category: 'discovery' },
      { text: "Show me my available templates", emoji: "📊", priority: 9, category: 'discovery' },
      { text: "How do I get started with data collaboration?", emoji: "🚀", priority: 8, category: 'discovery' },
      { text: "What's my cleanroom status?", emoji: "🏢", priority: 7, category: 'exploration' }
    ],
    
    cleanrooms_page: [
      { text: "Run a sentiment analysis", emoji: "🎯", priority: 10, category: 'execution', requiresTemplates: true },
      { text: "Analyze location patterns", emoji: "📍", priority: 9, category: 'execution', requiresTemplates: true },
      { text: "Execute combined intelligence", emoji: "🔧", priority: 8, category: 'execution', requiresTemplates: true },
      { text: "What parameters do these templates need?", emoji: "⚙️", priority: 7, category: 'exploration', requiresTemplates: true }
    ],
    
    api_explorer: [
      { text: "Test the templates API", emoji: "🔬", priority: 10, category: 'exploration' },
      { text: "Check API health status", emoji: "💓", priority: 8, category: 'monitoring' },
      { text: "Show me raw API responses", emoji: "📋", priority: 7, category: 'exploration' },
      { text: "Explore advanced API features", emoji: "🎛️", priority: 6, category: 'exploration' }
    ],

    // Conversation state-specific prompts
    first_interaction: [
      { text: "What can I do with this cleanroom?", emoji: "🤔", priority: 10, category: 'discovery' },
      { text: "Show me what analytics are available", emoji: "📈", priority: 9, category: 'discovery' },
      { text: "How does LiveRamp clean room work?", emoji: "🏠", priority: 8, category: 'discovery' },
      { text: "Get me started with my first analysis", emoji: "🎯", priority: 7, category: 'workflow' }
    ],

    post_template_view: [
      { text: "Run the sentiment analysis template", emoji: "😊", priority: 10, category: 'execution', requiresTemplates: true },
      { text: "Execute location pattern analysis", emoji: "🗺️", priority: 9, category: 'execution', requiresTemplates: true },
      { text: "Start combined data intelligence", emoji: "🌐", priority: 8, category: 'execution', requiresTemplates: true },
      { text: "What data do I need for these templates?", emoji: "💾", priority: 7, category: 'exploration' }
    ],

    post_query_submission: [
      { text: "Check my query status", emoji: "⏱️", priority: 10, category: 'monitoring', requiresActiveQuery: true },
      { text: "How long will my analysis take?", emoji: "⏳", priority: 8, category: 'monitoring', requiresActiveQuery: true },
      { text: "What happens while my query runs?", emoji: "🔄", priority: 6, category: 'exploration', requiresActiveQuery: true },
      { text: "Can I run another analysis while this runs?", emoji: "⚡", priority: 5, category: 'workflow' }
    ],

    post_results: [
      { text: "Export my analysis results", emoji: "📥", priority: 10, category: 'results' },
      { text: "Run another analysis with different data", emoji: "🔄", priority: 9, category: 'workflow' },
      { text: "What insights can I get from these results?", emoji: "💡", priority: 8, category: 'results' },
      { text: "How do I share these findings?", emoji: "📤", priority: 7, category: 'results' }
    ],

    // Template-category-specific prompts
    sentiment_available: [
      { text: "Analyze brand sentiment and mentions", emoji: "📝", priority: 10, category: 'execution' },
      { text: "Run global sentiment analysis", emoji: "🌍", priority: 9, category: 'execution' },
      { text: "What sentiment insights can I get?", emoji: "💭", priority: 7, category: 'exploration' }
    ],

    location_available: [
      { text: "Analyze mobile location patterns", emoji: "📱", priority: 10, category: 'execution' },
      { text: "Study pattern of life data", emoji: "🚶", priority: 9, category: 'execution' },
      { text: "What location insights are available?", emoji: "🗺️", priority: 7, category: 'exploration' }
    ],

    combined_available: [
      { text: "Run comprehensive behavioral analysis", emoji: "🧠", priority: 10, category: 'execution' },
      { text: "Execute multi-dimensional intelligence", emoji: "🎯", priority: 9, category: 'execution' },
      { text: "What combined insights can I discover?", emoji: "🔍", priority: 7, category: 'exploration' }
    ],

    // Workflow and status-specific prompts
    no_templates: [
      { text: "How do I get analytics templates?", emoji: "❓", priority: 10, category: 'discovery' },
      { text: "Contact admin about template setup", emoji: "👥", priority: 8, category: 'workflow' },
      { text: "What do I need to start analytics?", emoji: "🔧", priority: 7, category: 'discovery' }
    ],

    templates_need_setup: [
      { text: "How do I configure missing datasets?", emoji: "⚙️", priority: 10, category: 'workflow' },
      { text: "Contact admin about dataset setup", emoji: "📞", priority: 9, category: 'workflow' },
      { text: "What templates can I use right now?", emoji: "✅", priority: 8, category: 'discovery' }
    ]
  };

  /**
   * Generate contextual prompts based on current state
   */
  public generateContextualPrompts(
    conversationState: ConversationState,
    templateContext?: TemplateContext,
    maxPrompts: number = 5
  ): string[] {
    const relevantPrompts: Array<ContextualPrompt & { score: number }> = [];
    
    // Calculate context scores and select relevant prompts
    this.scoreAndSelectPrompts(conversationState, templateContext, relevantPrompts);
    
    // Sort by priority and score, then take top N
    relevantPrompts.sort((a, b) => (b.priority + b.score) - (a.priority + a.score));
    
    return relevantPrompts
      .slice(0, maxPrompts)
      .map(prompt => `${prompt.emoji} ${prompt.text}`);
  }

  private scoreAndSelectPrompts(
    state: ConversationState, 
    templateContext: TemplateContext | undefined,
    relevantPrompts: Array<ContextualPrompt & { score: number }>
  ): void {
    // Page-specific prompts
    this.addPageSpecificPrompts(state, relevantPrompts);
    
    // Conversation state prompts
    this.addConversationStatePrompts(state, relevantPrompts);
    
    // Template-aware prompts
    if (templateContext) {
      this.addTemplateAwarePrompts(state, templateContext, relevantPrompts);
    }
    
    // Workflow state prompts
    this.addWorkflowStatePrompts(state, relevantPrompts);
  }

  private addPageSpecificPrompts(state: ConversationState, prompts: Array<ContextualPrompt & { score: number }>): void {
    const currentPage = state.currentPage || 'home';
    let pageKey = 'home_welcome';
    
    if (currentPage.includes('cleanrooms')) {
      pageKey = 'cleanrooms_page';
    } else if (currentPage.includes('api')) {
      pageKey = 'api_explorer';
    }
    
    const pagePrompts = this.promptDatabase[pageKey] || [];
    pagePrompts.forEach(prompt => {
      if (this.isPromptRelevant(prompt, state)) {
        prompts.push({ ...prompt, score: 5 }); // Page context bonus
      }
    });
  }

  private addConversationStatePrompts(state: ConversationState, prompts: Array<ContextualPrompt & { score: number }>): void {
    let stateKey = 'first_interaction';
    
    if (state.conversationLength === 0) {
      stateKey = 'first_interaction';
    } else if (state.hasViewedTemplates && !state.hasSubmittedQuery) {
      stateKey = 'post_template_view';
    } else if (state.hasSubmittedQuery && state.hasActiveQuery) {
      stateKey = 'post_query_submission';
    } else if (state.hasCompletedQuery && state.hasViewedResults) {
      stateKey = 'post_results';
    }
    
    const statePrompts = this.promptDatabase[stateKey] || [];
    statePrompts.forEach(prompt => {
      if (this.isPromptRelevant(prompt, state)) {
        prompts.push({ ...prompt, score: 8 }); // High relevance for conversation state
      }
    });
  }

  private addTemplateAwarePrompts(
    state: ConversationState, 
    templateContext: TemplateContext, 
    prompts: Array<ContextualPrompt & { score: number }>
  ): void {
    // Handle no templates case
    if (templateContext.totalTemplates === 0) {
      const noTemplatePrompts = this.promptDatabase['no_templates'] || [];
      noTemplatePrompts.forEach(prompt => {
        prompts.push({ ...prompt, score: 9 });
      });
      return;
    }
    
    // Handle templates that need setup
    if (templateContext.missingDatasetTemplates > 0) {
      const setupPrompts = this.promptDatabase['templates_need_setup'] || [];
      setupPrompts.forEach(prompt => {
        prompts.push({ ...prompt, score: 6 });
      });
    }
    
    // Category-specific prompts for available templates
    if (templateContext.hasSentimentAnalysis) {
      this.addCategoryPrompts('sentiment_available', prompts, 7);
    }
    
    if (templateContext.hasLocationData) {
      this.addCategoryPrompts('location_available', prompts, 7);
    }
    
    if (templateContext.hasCombinedAnalysis) {
      this.addCategoryPrompts('combined_available', prompts, 7);
    }
  }

  private addWorkflowStatePrompts(state: ConversationState, prompts: Array<ContextualPrompt & { score: number }>): void {
    // Add workflow-specific prompts based on current progress
    if (state.hasActiveQuery) {
      // Prioritize monitoring prompts
      prompts.forEach(prompt => {
        if (prompt.category === 'monitoring') {
          prompt.score += 3;
        }
      });
    }
    
    if (state.hasCompletedQuery && !state.hasViewedResults) {
      // Prioritize results prompts
      prompts.forEach(prompt => {
        if (prompt.category === 'results') {
          prompt.score += 4;
        }
      });
    }
  }

  private addCategoryPrompts(category: string, prompts: Array<ContextualPrompt & { score: number }>, score: number): void {
    const categoryPrompts = this.promptDatabase[category] || [];
    categoryPrompts.forEach(prompt => {
      prompts.push({ ...prompt, score });
    });
  }

  private isPromptRelevant(prompt: ContextualPrompt, state: ConversationState): boolean {
    // Check if prompt requirements are met
    if (prompt.requiresTemplates && (state.availableTemplates || 0) === 0) {
      return false;
    }
    
    if (prompt.requiresActiveQuery && !state.hasActiveQuery) {
      return false;
    }
    
    // Check page specificity
    if (prompt.pageSpecific && state.currentPage) {
      return prompt.pageSpecific.some(page => state.currentPage?.includes(page));
    }
    
    return true;
  }

  /**
   * Update conversation state based on recent interactions
   */
  public updateConversationState(
    currentState: ConversationState,
    recentMessages: Array<{type: 'user' | 'assistant', content: string}>,
    currentPage?: string
  ): ConversationState {
    const updatedState = { ...currentState };
    
    // Update page context
    updatedState.currentPage = currentPage;
    updatedState.conversationLength = recentMessages.length;
    
    // Analyze recent messages for state indicators
    const recentContent = recentMessages.slice(-5).map(m => m.content.toLowerCase()).join(' ');
    
    // Check for template viewing
    if (recentContent.includes('template') || recentContent.includes('analytics') || recentContent.includes('available')) {
      updatedState.hasViewedTemplates = true;
    }
    
    // Check for query submission
    if (recentContent.includes('submitted') || recentContent.includes('executed') || recentContent.includes('running')) {
      updatedState.hasSubmittedQuery = true;
      updatedState.hasActiveQuery = true;
    }
    
    // Check for completed queries
    if (recentContent.includes('completed') || recentContent.includes('finished') || recentContent.includes('results')) {
      updatedState.hasCompletedQuery = true;
      updatedState.hasActiveQuery = false;
    }
    
    // Check for viewed results
    if (recentContent.includes('results') || recentContent.includes('insights') || recentContent.includes('findings')) {
      updatedState.hasViewedResults = true;
    }
    
    return updatedState;
  }
}

export default ContextualPromptService;