// Customer Support Response Generator - Create customer-ready responses

import CustomerUseCaseLibrary, { CustomerUseCase, IndustryConstraints } from './CustomerUseCaseLibrary';

export interface SupportQuery {
  question: string;
  customerIndustry?: string;
  customerSize?: 'small' | 'medium' | 'large' | 'enterprise';
  urgency?: 'low' | 'medium' | 'high';
  technicalLevel?: 'business' | 'technical' | 'executive';
  context?: string;
}

export interface SupportResponse {
  summary: string;
  feasibility: 'yes' | 'partially' | 'no';
  confidence: 'high' | 'medium' | 'low';
  businessValue: string;
  implementation: {
    timeline: string;
    requirements: string[];
    complexity: string;
  };
  limitations: string[];
  alternatives: string[];
  competitiveAdvantage: string[];
  nextSteps: string[];
  pricing: {
    tier: string;
    considerations: string[];
  };
  riskFactors: string[];
  successFactors: string[];
}

export interface CompetitiveAdvantage {
  category: string;
  advantage: string;
  proof: string;
  customerBenefit: string;
}

class CustomerSupportResponseGenerator {
  private static instance: CustomerSupportResponseGenerator;
  private useCaseLibrary: CustomerUseCaseLibrary;
  private competitiveAdvantages: CompetitiveAdvantage[] = [];

  private constructor() {
    this.useCaseLibrary = CustomerUseCaseLibrary.getInstance();
    this.initializeCompetitiveAdvantages();
  }

  public static getInstance(): CustomerSupportResponseGenerator {
    if (!CustomerSupportResponseGenerator.instance) {
      CustomerSupportResponseGenerator.instance = new CustomerSupportResponseGenerator();
    }
    return CustomerSupportResponseGenerator.instance;
  }

  private initializeCompetitiveAdvantages(): void {
    this.competitiveAdvantages = [
      {
        category: 'Match Rates',
        advantage: '90%+ identity match rates',
        proof: 'Industry average is 60-70%',
        customerBenefit: 'More accurate targeting, better campaign performance'
      },
      {
        category: 'Privacy',
        advantage: 'Privacy-first architecture',
        proof: 'No raw PII exposure, built-in compliance',
        customerBenefit: 'Reduced compliance risk, future-proof data strategy'
      },
      {
        category: 'Scale',
        advantage: '300M+ consumer identity graph',
        proof: 'Largest authenticated identity dataset',
        customerBenefit: 'Better reach and audience discovery'
      },
      {
        category: 'Speed',
        advantage: 'Real-time data activation',
        proof: 'Sub-second audience updates',
        customerBenefit: 'Respond to customer behavior immediately'
      },
      {
        category: 'Integration',
        advantage: '500+ platform integrations',
        proof: 'Direct connections to major ad platforms',
        customerBenefit: 'Simplified data workflows, faster time-to-market'
      }
    ];
  }

  public generateResponse(query: SupportQuery): SupportResponse {
    // Find relevant use cases
    const relevantUseCases = this.findRelevantUseCases(query);
    const primaryUseCase = relevantUseCases[0];
    
    // Get industry constraints
    const industryConstraints = query.customerIndustry 
      ? this.useCaseLibrary.getIndustryConstraints(query.customerIndustry) || null
      : null;

    // Determine feasibility
    const feasibility = this.assessFeasibility(query, relevantUseCases);
    const confidence = this.assessConfidence(query, relevantUseCases);

    // Generate response sections
    const summary = this.generateSummary(query, primaryUseCase, feasibility);
    const businessValue = this.generateBusinessValue(primaryUseCase);
    const implementation = this.generateImplementation(primaryUseCase, query);
    const limitations = this.generateLimitations(primaryUseCase, industryConstraints);
    const alternatives = this.generateAlternatives(primaryUseCase, relevantUseCases);
    const competitiveAdvantage = this.generateCompetitiveAdvantage(primaryUseCase);
    const nextSteps = this.generateNextSteps(query, feasibility);
    const pricing = this.generatePricing(query, primaryUseCase);
    const riskFactors = this.generateRiskFactors(primaryUseCase, industryConstraints);
    const successFactors = this.generateSuccessFactors(primaryUseCase, industryConstraints);

    return {
      summary,
      feasibility,
      confidence,
      businessValue,
      implementation,
      limitations,
      alternatives,
      competitiveAdvantage,
      nextSteps,
      pricing,
      riskFactors,
      successFactors
    };
  }

  private findRelevantUseCases(query: SupportQuery): CustomerUseCase[] {
    let useCases: CustomerUseCase[] = [];

    // Search by query text
    if (query.question) {
      useCases = this.useCaseLibrary.searchUseCases(query.question);
    }

    // Filter by industry if provided
    if (query.customerIndustry && useCases.length === 0) {
      useCases = this.useCaseLibrary.getUseCasesByIndustry(query.customerIndustry);
    }

    // If still no matches, return most common use cases
    if (useCases.length === 0) {
      useCases = this.useCaseLibrary.searchUseCases('lookalike segmentation');
    }

    return useCases.slice(0, 3); // Return top 3 matches
  }

  private assessFeasibility(query: SupportQuery, useCases: CustomerUseCase[]): 'yes' | 'partially' | 'no' {
    if (useCases.length === 0) return 'no';
    
    const primaryUseCase = useCases[0];
    
    // Check industry alignment
    if (query.customerIndustry && !primaryUseCase.industry.includes(query.customerIndustry)) {
      return 'partially';
    }

    // High confidence use cases are typically feasible
    if (primaryUseCase.confidence === 'high') {
      return 'yes';
    }

    return 'partially';
  }

  private assessConfidence(query: SupportQuery, useCases: CustomerUseCase[]): 'high' | 'medium' | 'low' {
    if (useCases.length === 0) return 'low';
    
    const primaryUseCase = useCases[0];
    
    // Industry match increases confidence
    if (query.customerIndustry && primaryUseCase.industry.includes(query.customerIndustry)) {
      return primaryUseCase.confidence;
    }

    // Lower confidence if no industry match
    const confidenceMap = { 'high': 'medium', 'medium': 'low', 'low': 'low' };
    return confidenceMap[primaryUseCase.confidence] as 'high' | 'medium' | 'low';
  }

  private generateSummary(query: SupportQuery, useCase: CustomerUseCase | undefined, feasibility: string): string {
    if (!useCase) {
      return "❓ **Need More Details** - Please provide more specific information about the use case to give you an accurate assessment.";
    }

    const feasibilityEmoji = {
      'yes': '✅',
      'partially': '⚠️',
      'no': '❌'
    }[feasibility] || '❓';

    const feasibilityText = {
      'yes': 'Yes, this is fully supported!',
      'partially': 'Partially supported - see details below',
      'no': 'Not directly supported - see alternatives'
    }[feasibility] || 'Unclear';

    return `${feasibilityEmoji} **${feasibilityText}**\n\n${useCase.description}`;
  }

  private generateBusinessValue(useCase: CustomerUseCase | undefined): string {
    if (!useCase) return "Business value assessment requires more specific use case details.";
    
    return `**${useCase.businessOutcome}**\n\nKey benefits include improved targeting accuracy, better campaign performance, and enhanced customer insights.`;
  }

  private generateImplementation(useCase: CustomerUseCase | undefined, query: SupportQuery): {
    timeline: string;
    requirements: string[];
    complexity: string;
  } {
    if (!useCase) {
      return {
        timeline: "Timeline depends on specific requirements",
        requirements: ["Detailed use case definition needed"],
        complexity: "Cannot assess without more details"
      };
    }

    return {
      timeline: useCase.timeline,
      requirements: useCase.requirements,
      complexity: `${useCase.complexity.charAt(0).toUpperCase() + useCase.complexity.slice(1)} implementation`
    };
  }

  private generateLimitations(useCase: CustomerUseCase | undefined, constraints: IndustryConstraints | null): string[] {
    const limitations: string[] = [];
    
    if (useCase) {
      limitations.push(...useCase.limitations);
    }
    
    if (constraints) {
      limitations.push(`${constraints.industry} industry compliance: ${constraints.regulatoryCompliance.join(', ')}`);
    }
    
    return limitations.length > 0 ? limitations : ["No significant limitations identified"];
  }

  private generateAlternatives(primaryUseCase: CustomerUseCase | undefined, allUseCases: CustomerUseCase[]): string[] {
    if (!primaryUseCase) return ["Contact solution engineering for custom approach"];
    
    const alternatives = [...primaryUseCase.alternatives];
    
    // Add other relevant use cases as alternatives
    allUseCases.slice(1, 3).forEach(useCase => {
      alternatives.push(`Alternative: ${useCase.title} - ${useCase.description}`);
    });
    
    return alternatives;
  }

  private generateCompetitiveAdvantage(useCase: CustomerUseCase | undefined): string[] {
    if (!useCase) return this.competitiveAdvantages.slice(0, 2).map(adv => adv.advantage);
    
    const advantages = [...useCase.competitiveAdvantage];
    
    // Add relevant competitive advantages
    if (useCase.title.includes('identity') || useCase.title.includes('match')) {
      advantages.push(this.competitiveAdvantages[0].advantage); // Match rates
    }
    
    advantages.push(this.competitiveAdvantages[1].advantage); // Privacy
    
    return advantages;
  }

  private generateNextSteps(query: SupportQuery, feasibility: string): string[] {
    const baseSteps = [
      "Schedule technical discovery call",
      "Provide data sample for match rate assessment",
      "Review compliance requirements"
    ];

    if (feasibility === 'yes') {
      return [
        "Confirm data requirements and timeline",
        "Set up proof of concept (POC)",
        "Schedule technical integration planning"
      ];
    } else if (feasibility === 'partially') {
      return [
        "Clarify specific requirements and constraints",
        "Explore alternative approaches",
        "Consult with solution engineering team"
      ];
    } else {
      return [
        "Discuss alternative solutions",
        "Consider phased implementation approach",
        "Escalate to product team for roadmap discussion"
      ];
    }
  }

  private generatePricing(query: SupportQuery, useCase: CustomerUseCase | undefined): {
    tier: string;
    considerations: string[];
  } {
    const customerSize = query.customerSize || 'medium';
    
    const tierMapping = {
      'small': 'Starter',
      'medium': 'Professional', 
      'large': 'Enterprise',
      'enterprise': 'Enterprise+'
    };

    const considerations = [
      "Pricing based on data volume and use case complexity",
      "POC typically available at reduced cost",
      "Annual commitments offer better pricing"
    ];

    if (useCase?.complexity === 'complex') {
      considerations.push("Complex implementations may require professional services");
    }

    return {
      tier: tierMapping[customerSize],
      considerations
    };
  }

  private generateRiskFactors(useCase: CustomerUseCase | undefined, constraints: IndustryConstraints | null): string[] {
    const risks: string[] = [];
    
    if (useCase) {
      if (useCase.confidence === 'low') {
        risks.push("Lower confidence in success - recommend POC");
      }
      if (useCase.complexity === 'complex') {
        risks.push("Complex implementation - ensure adequate resources");
      }
    }
    
    if (constraints) {
      risks.push(...constraints.commonChallenges.map(challenge => `Industry challenge: ${challenge}`));
    }
    
    return risks.length > 0 ? risks : ["Low risk implementation"];
  }

  private generateSuccessFactors(useCase: CustomerUseCase | undefined, constraints: IndustryConstraints | null): string[] {
    const factors: string[] = [];
    
    if (useCase) {
      factors.push(`Minimum data requirement: ${useCase.minDataSize}`);
      factors.push(...useCase.successMetrics.map(metric => `Success metric: ${metric}`));
    }
    
    if (constraints) {
      factors.push(...constraints.successFactors);
    }
    
    return factors.length > 0 ? factors : ["Standard success factors apply"];
  }

  // Helper method for quick capability assessment
  public quickAssessment(question: string, industry?: string): string {
    const query: SupportQuery = {
      question,
      customerIndustry: industry,
      technicalLevel: 'business'
    };
    
    const response = this.generateResponse(query);
    
    return `${response.summary}\n\n**Timeline**: ${response.implementation.timeline}\n**Confidence**: ${response.confidence}`;
  }
}

export default CustomerSupportResponseGenerator;