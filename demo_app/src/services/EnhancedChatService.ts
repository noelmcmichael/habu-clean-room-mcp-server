// Enhanced Chat Service - Integrates customer support capabilities with chat

import { ChatMode } from '../types/ChatModes';
import CustomerSupportResponseGenerator, { SupportQuery, SupportResponse } from './CustomerSupportResponseGenerator';
import CustomerUseCaseLibrary from './CustomerUseCaseLibrary';

export interface EnhancedChatRequest {
  message: string;
  mode: ChatMode;
  context?: {
    industry?: string;
    customerSize?: string;
    urgency?: string;
    employeeRole?: string;
  };
  conversationHistory?: Array<{
    role: 'user' | 'assistant';
    content: string;
  }>;
}

export interface EnhancedChatResponse {
  content: string;
  metadata: {
    supportResponse?: SupportResponse;
    useCasesFound?: string[];
    industryRelevant?: boolean;
    confidenceScore?: number;
    sourceValidation?: boolean;
    businessImpact?: string;
    competitiveAdvantage?: string[];
    suggestedActions?: string[];
  };
}

class EnhancedChatService {
  private static instance: EnhancedChatService;
  private supportGenerator: CustomerSupportResponseGenerator;
  private useCaseLibrary: CustomerUseCaseLibrary;

  private constructor() {
    this.supportGenerator = CustomerSupportResponseGenerator.getInstance();
    this.useCaseLibrary = CustomerUseCaseLibrary.getInstance();
  }

  public static getInstance(): EnhancedChatService {
    if (!EnhancedChatService.instance) {
      EnhancedChatService.instance = new EnhancedChatService();
    }
    return EnhancedChatService.instance;
  }

  public async processCustomerSupportQuery(request: EnhancedChatRequest): Promise<EnhancedChatResponse> {
    // Parse the user query to understand intent
    const intent = this.parseCustomerIntent(request.message);
    
    // Create support query
    const supportQuery: SupportQuery = {
      question: request.message,
      customerIndustry: request.context?.industry,
      customerSize: request.context?.customerSize as any,
      urgency: request.context?.urgency as any,
      technicalLevel: this.mapEmployeeRoleToTechnicalLevel(request.context?.employeeRole),
      context: this.extractContextFromHistory(request.conversationHistory)
    };

    // Generate support response
    const supportResponse = this.supportGenerator.generateResponse(supportQuery);
    
    // Format customer-ready response
    const formattedResponse = this.formatCustomerSupportResponse(supportResponse, intent);
    
    // Calculate metadata
    const metadata = this.generateMetadata(supportResponse, intent);

    return {
      content: formattedResponse,
      metadata
    };
  }

  public async processTechnicalExpertQuery(request: EnhancedChatRequest): Promise<EnhancedChatResponse> {
    // For technical queries, focus on implementation details
    const technicalResponse = this.generateTechnicalResponse(request);
    
    return {
      content: technicalResponse.content,
      metadata: technicalResponse.metadata
    };
  }

  private parseCustomerIntent(message: string): {
    type: 'capability' | 'feasibility' | 'pricing' | 'timeline' | 'comparison' | 'implementation' | 'general';
    keywords: string[];
    industry?: string;
    confidence: number;
  } {
    const lowerMessage = message.toLowerCase();
    
    // Capability questions
    if (lowerMessage.includes('can we') || lowerMessage.includes('is it possible') || lowerMessage.includes('do you support')) {
      return {
        type: 'capability',
        keywords: this.extractKeywords(message),
        industry: this.detectIndustry(message),
        confidence: 0.8
      };
    }
    
    // Feasibility questions
    if (lowerMessage.includes('feasible') || lowerMessage.includes('realistic') || lowerMessage.includes('achievable')) {
      return {
        type: 'feasibility',
        keywords: this.extractKeywords(message),
        industry: this.detectIndustry(message),
        confidence: 0.7
      };
    }
    
    // Pricing questions
    if (lowerMessage.includes('cost') || lowerMessage.includes('price') || lowerMessage.includes('budget')) {
      return {
        type: 'pricing',
        keywords: this.extractKeywords(message),
        industry: this.detectIndustry(message),
        confidence: 0.9
      };
    }
    
    // Timeline questions
    if (lowerMessage.includes('how long') || lowerMessage.includes('timeline') || lowerMessage.includes('when')) {
      return {
        type: 'timeline',
        keywords: this.extractKeywords(message),
        industry: this.detectIndustry(message),
        confidence: 0.8
      };
    }
    
    // Comparison questions
    if (lowerMessage.includes('vs') || lowerMessage.includes('versus') || lowerMessage.includes('compared to') || lowerMessage.includes('better than')) {
      return {
        type: 'comparison',
        keywords: this.extractKeywords(message),
        industry: this.detectIndustry(message),
        confidence: 0.7
      };
    }
    
    // Implementation questions
    if (lowerMessage.includes('how to') || lowerMessage.includes('implement') || lowerMessage.includes('integrate')) {
      return {
        type: 'implementation',
        keywords: this.extractKeywords(message),
        industry: this.detectIndustry(message),
        confidence: 0.8
      };
    }
    
    return {
      type: 'general',
      keywords: this.extractKeywords(message),
      industry: this.detectIndustry(message),
      confidence: 0.5
    };
  }

  private extractKeywords(message: string): string[] {
    const apiKeywords = [
      'lookalike', 'segmentation', 'attribution', 'identity', 'resolution',
      'collaboration', 'audience', 'targeting', 'personalization', 'matching'
    ];
    
    return apiKeywords.filter(keyword => 
      message.toLowerCase().includes(keyword)
    );
  }

  private detectIndustry(message: string): string | undefined {
    const industries = this.useCaseLibrary.getAllIndustries();
    
    for (const industry of industries) {
      if (message.toLowerCase().includes(industry)) {
        return industry;
      }
    }
    
    return undefined;
  }

  private mapEmployeeRoleToTechnicalLevel(role?: string): 'business' | 'technical' | 'executive' {
    const roleMapping: Record<string, 'business' | 'technical' | 'executive'> = {
      'support': 'business',
      'sales': 'business', 
      'engineering': 'technical',
      'product': 'executive',
      'other': 'business'
    };
    
    return roleMapping[role || 'other'] || 'business';
  }

  private extractContextFromHistory(history?: Array<{role: string; content: string}>): string {
    if (!history || history.length === 0) return '';
    
    const recent = history.slice(-3); // Last 3 exchanges
    return recent.map(h => `${h.role}: ${h.content}`).join('\n');
  }

  private formatCustomerSupportResponse(response: SupportResponse, intent: any): string {
    let formatted = response.summary + '\n\n';
    
    // Add business value
    if (response.businessValue) {
      formatted += `**💰 Business Value**\n${response.businessValue}\n\n`;
    }
    
    // Add implementation details based on intent
    if (intent.type === 'timeline' || intent.type === 'feasibility') {
      formatted += `**⏱️ Implementation**\n`;
      formatted += `• **Timeline**: ${response.implementation.timeline}\n`;
      formatted += `• **Complexity**: ${response.implementation.complexity}\n\n`;
    }
    
    // Add requirements if relevant
    if (intent.type === 'capability' || intent.type === 'implementation') {
      formatted += `**📋 Requirements**\n`;
      response.implementation.requirements.forEach(req => {
        formatted += `• ${req}\n`;
      });
      formatted += '\n';
    }
    
    // Add competitive advantages
    if (response.competitiveAdvantage.length > 0) {
      formatted += `**🏆 LiveRamp Advantages**\n`;
      response.competitiveAdvantage.forEach(advantage => {
        formatted += `• ${advantage}\n`;
      });
      formatted += '\n';
    }
    
    // Add pricing info if requested
    if (intent.type === 'pricing') {
      formatted += `**💸 Pricing Guidance**\n`;
      formatted += `• **Recommended Tier**: ${response.pricing.tier}\n`;
      response.pricing.considerations.forEach(consideration => {
        formatted += `• ${consideration}\n`;
      });
      formatted += '\n';
    }
    
    // Add limitations and alternatives
    if (response.limitations.length > 0) {
      formatted += `**⚠️ Considerations**\n`;
      response.limitations.slice(0, 3).forEach(limitation => {
        formatted += `• ${limitation}\n`;
      });
      formatted += '\n';
    }
    
    // Add next steps
    if (response.nextSteps.length > 0) {
      formatted += `**🚀 Recommended Next Steps**\n`;
      response.nextSteps.forEach(step => {
        formatted += `• ${step}\n`;
      });
      formatted += '\n';
    }
    
    // Add expansion offer
    formatted += `💡 **Want more details?** Ask about technical implementation, competitive positioning, or specific industry considerations.`;
    
    return formatted;
  }

  private generateTechnicalResponse(request: EnhancedChatRequest): EnhancedChatResponse {
    // For now, return a placeholder technical response
    // This will be enhanced in Phase 3
    const content = `🔧 **Technical Expert Mode**

I'm ready to provide detailed technical guidance on LiveRamp API implementation.

**Available Topics**:
• API method documentation and examples
• Integration patterns and best practices  
• Security and compliance implementation
• Performance optimization strategies
• Troubleshooting common issues

What specific technical question can I help you with?`;

    return {
      content,
      metadata: {
        confidenceScore: 1.0,
        sourceValidation: true,
        suggestedActions: [
          'Ask about specific API methods',
          'Request code examples',
          'Inquire about integration patterns'
        ]
      }
    };
  }

  private generateMetadata(response: SupportResponse, intent: any): any {
    const confidenceMap = { 'high': 0.9, 'medium': 0.7, 'low': 0.5 };
    
    return {
      supportResponse: response,
      useCasesFound: [intent.keywords.join(', ')],
      industryRelevant: !!intent.industry,
      confidenceScore: confidenceMap[response.confidence],
      sourceValidation: true,
      businessImpact: response.businessValue,
      competitiveAdvantage: response.competitiveAdvantage,
      suggestedActions: response.nextSteps
    };
  }

  // Public method for quick capability assessment
  public async quickCapabilityCheck(question: string, industry?: string): Promise<string> {
    const response = this.supportGenerator.quickAssessment(question, industry);
    return response;
  }
}

export default EnhancedChatService;