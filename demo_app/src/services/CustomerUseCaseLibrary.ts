// Customer Use Case Library - Industry-specific scenarios and capabilities

export interface CustomerUseCase {
  id: string;
  title: string;
  description: string;
  industry: string[];
  businessOutcome: string;
  apiCapabilities: string[];
  requirements: string[];
  timeline: string;
  limitations: string[];
  alternatives: string[];
  competitiveAdvantage: string[];
  successMetrics: string[];
  minDataSize: string;
  complexity: 'simple' | 'moderate' | 'complex';
  confidence: 'high' | 'medium' | 'low';
}

export interface BusinessOutcome {
  id: string;
  name: string;
  description: string;
  roiPotential: 'high' | 'medium' | 'low';
  timeToValue: string;
  industryRelevance: string[];
  successStories: string[];
}

export interface IndustryConstraints {
  industry: string;
  dataPrivacyRequirements: string[];
  regulatoryCompliance: string[];
  typicalDataVolumes: string;
  commonChallenges: string[];
  successFactors: string[];
}

class CustomerUseCaseLibrary {
  private static instance: CustomerUseCaseLibrary;
  private useCases: CustomerUseCase[] = [];
  private businessOutcomes: BusinessOutcome[] = [];
  private industryConstraints: IndustryConstraints[] = [];

  private constructor() {
    this.initializeUseCases();
    this.initializeBusinessOutcomes();
    this.initializeIndustryConstraints();
  }

  public static getInstance(): CustomerUseCaseLibrary {
    if (!CustomerUseCaseLibrary.instance) {
      CustomerUseCaseLibrary.instance = new CustomerUseCaseLibrary();
    }
    return CustomerUseCaseLibrary.instance;
  }

  private initializeUseCases(): void {
    this.useCases = [
      {
        id: 'lookalike-modeling',
        title: 'Lookalike Audience Expansion',
        description: 'Find new customers similar to existing high-value customers using CRM data',
        industry: ['retail', 'e-commerce', 'finance', 'automotive', 'travel'],
        businessOutcome: 'Increase customer acquisition efficiency by 40-60%',
        apiCapabilities: ['habu_enhanced_templates', 'habu_submit_query', 'habu_get_results'],
        requirements: [
          'Minimum 1,000 seed customers',
          'Customer data with email or postal address',
          'Historical purchase/engagement data'
        ],
        timeline: '24-48 hours for model creation',
        limitations: [
          'Requires sufficient match rate (>60%)',
          'Performance varies by industry vertical',
          'Need ongoing model refresh (monthly recommended)'
        ],
        alternatives: [
          'Cohort analysis for smaller datasets',
          'Behavioral segmentation as alternative approach'
        ],
        competitiveAdvantage: [
          '90%+ match rates vs industry 60-70%',
          'Identity graph spans 300M+ US consumers',
          'Real-time audience activation'
        ],
        successMetrics: [
          'Match rate >60%',
          'Audience size 5-10x seed list',
          'Conversion rate improvement >25%'
        ],
        minDataSize: '1,000+ customers',
        complexity: 'simple',
        confidence: 'high'
      },
      {
        id: 'cross-platform-attribution',
        title: 'Cross-Platform Customer Journey Attribution',
        description: 'Track customer interactions across digital and offline touchpoints',
        industry: ['retail', 'automotive', 'finance', 'healthcare'],
        businessOutcome: 'Optimize marketing spend allocation across channels',
        apiCapabilities: ['habu_enhanced_templates', 'habu_list_partners', 'habu_submit_query'],
        requirements: [
          'Multi-channel customer data',
          'Consistent customer identifiers',
          'Conversion event tracking'
        ],
        timeline: '1-2 weeks for implementation',
        limitations: [
          'Requires data from multiple touchpoints',
          'Attribution windows configurable but not unlimited',
          'Some channels may have limited visibility'
        ],
        alternatives: [
          'Single-channel attribution for simplified analysis',
          'Marketing mix modeling for aggregate insights'
        ],
        competitiveAdvantage: [
          'Unified identity resolution across channels',
          'Privacy-compliant cross-device tracking',
          'Real-time attribution updates'
        ],
        successMetrics: [
          'Cross-channel match rate >70%',
          'Attribution accuracy improvement >30%',
          'ROAS optimization 15-25%'
        ],
        minDataSize: '10,000+ interactions',
        complexity: 'moderate',
        confidence: 'high'
      },
      {
        id: 'customer-segmentation',
        title: 'Advanced Customer Segmentation',
        description: 'Create behavioral and demographic customer segments for targeted marketing',
        industry: ['retail', 'finance', 'travel', 'entertainment', 'b2b'],
        businessOutcome: 'Increase campaign effectiveness through personalized targeting',
        apiCapabilities: ['habu_enhanced_templates', 'habu_submit_query', 'habu_get_results'],
        requirements: [
          'Customer transaction/behavior data',
          'Demographic information',
          'Engagement history'
        ],
        timeline: '3-5 days for analysis',
        limitations: [
          'Segment quality depends on data richness',
          'Minimum segment sizes for statistical significance',
          'Regular refresh needed for accuracy'
        ],
        alternatives: [
          'Simple RFM segmentation',
          'Geographic segmentation',
          'Product affinity groups'
        ],
        competitiveAdvantage: [
          'AI-powered segment discovery',
          'Real-time segment updates',
          'Privacy-compliant demographic enrichment'
        ],
        successMetrics: [
          '5-10 distinct segments identified',
          'Segment lift >20% vs broad targeting',
          'Customer lifetime value increase'
        ],
        minDataSize: '5,000+ customers',
        complexity: 'moderate',
        confidence: 'high'
      },
      {
        id: 'identity-resolution',
        title: 'Customer Identity Resolution',
        description: 'Unify customer identities across devices, channels, and data sources',
        industry: ['retail', 'media', 'finance', 'healthcare', 'automotive'],
        businessOutcome: 'Create unified customer view for personalized experiences',
        apiCapabilities: ['habu_list_partners', 'habu_enhanced_templates', 'habu_submit_query'],
        requirements: [
          'Multiple data sources with customer identifiers',
          'PII data (email, phone, address)',
          'Device/session data'
        ],
        timeline: '1-3 weeks depending on complexity',
        limitations: [
          'Match rates vary by data quality',
          'Privacy regulations may limit linking',
          'Requires ongoing maintenance'
        ],
        alternatives: [
          'Probabilistic matching for lower confidence',
          'Device-only linking',
          'Email-based identity spine'
        ],
        competitiveAdvantage: [
          'Industry-leading match rates',
          'Privacy-first approach',
          'Real-time identity graph updates'
        ],
        successMetrics: [
          'Identity match rate >80%',
          'Unified customer records',
          'Cross-device attribution accuracy'
        ],
        minDataSize: '1,000+ customers',
        complexity: 'complex',
        confidence: 'high'
      },
      {
        id: 'data-collaboration',
        title: 'Secure Data Collaboration',
        description: 'Collaborate with partners on shared customer insights without exposing raw data',
        industry: ['retail', 'finance', 'automotive', 'travel', 'media'],
        businessOutcome: 'Unlock new revenue opportunities through partner data',
        apiCapabilities: ['habu_list_partners', 'habu_enhanced_templates', 'habu_submit_query'],
        requirements: [
          'Partner agreement and data sharing terms',
          'Matched customer base with partner',
          'Clear use case definition'
        ],
        timeline: '2-4 weeks including partner onboarding',
        limitations: [
          'Requires partner participation',
          'Limited to pre-approved use cases',
          'Match rates depend on overlap'
        ],
        alternatives: [
          'Third-party data enrichment',
          'Lookalike modeling without collaboration',
          'Public data sources'
        ],
        competitiveAdvantage: [
          'Privacy-preserving collaboration',
          'No raw data exposure',
          'Compliance-ready frameworks'
        ],
        successMetrics: [
          'Partner match rate >50%',
          'New customer insights generated',
          'Revenue lift from collaboration'
        ],
        minDataSize: '5,000+ overlapping customers',
        complexity: 'complex',
        confidence: 'medium'
      }
    ];
  }

  private initializeBusinessOutcomes(): void {
    this.businessOutcomes = [
      {
        id: 'customer-acquisition',
        name: 'Improved Customer Acquisition',
        description: 'Acquire new customers more efficiently through better targeting',
        roiPotential: 'high',
        timeToValue: '1-2 months',
        industryRelevance: ['retail', 'finance', 'automotive', 'travel'],
        successStories: [
          'Major retailer increased acquisition efficiency by 45%',
          'Auto brand reduced CAC by 30% with lookalike modeling'
        ]
      },
      {
        id: 'marketing-optimization',
        name: 'Marketing Spend Optimization',
        description: 'Allocate marketing budget more effectively across channels',
        roiPotential: 'high',
        timeToValue: '2-3 months',
        industryRelevance: ['retail', 'e-commerce', 'travel', 'entertainment'],
        successStories: [
          'E-commerce company improved ROAS by 25%',
          'Travel brand optimized channel mix, saved $2M annually'
        ]
      },
      {
        id: 'personalization',
        name: 'Enhanced Personalization',
        description: 'Deliver more relevant experiences through better customer understanding',
        roiPotential: 'medium',
        timeToValue: '3-6 months',
        industryRelevance: ['retail', 'media', 'finance', 'healthcare'],
        successStories: [
          'Media company increased engagement by 40%',
          'Bank improved product recommendation CTR by 60%'
        ]
      }
    ];
  }

  private initializeIndustryConstraints(): void {
    this.industryConstraints = [
      {
        industry: 'retail',
        dataPrivacyRequirements: ['CCPA compliance', 'GDPR for EU customers', 'Consent management'],
        regulatoryCompliance: ['PCI DSS for payment data', 'State privacy laws'],
        typicalDataVolumes: '1M-100M+ customer records',
        commonChallenges: [
          'Seasonal data patterns',
          'Cross-channel attribution complexity',
          'Inventory-driven personalization'
        ],
        successFactors: [
          'Rich transaction history',
          'Multi-channel data integration',
          'Real-time activation capabilities'
        ]
      },
      {
        industry: 'finance',
        dataPrivacyRequirements: ['CCPA compliance', 'GDPR', 'Financial privacy regulations'],
        regulatoryCompliance: ['GLBA', 'Fair Credit Reporting Act', 'Anti-discrimination laws'],
        typicalDataVolumes: '100K-10M customer records',
        commonChallenges: [
          'Strict regulatory environment',
          'Risk management integration',
          'Fraud prevention requirements'
        ],
        successFactors: [
          'High-quality customer data',
          'Compliance-first approach',
          'Risk-adjusted targeting'
        ]
      },
      {
        industry: 'automotive',
        dataPrivacyRequirements: ['CCPA compliance', 'GDPR', 'Connected vehicle data privacy'],
        regulatoryCompliance: ['State lemon laws', 'Safety regulations'],
        typicalDataVolumes: '500K-5M prospect records',
        commonChallenges: [
          'Long purchase cycles',
          'Dealer network complexity',
          'Multi-stakeholder decisions'
        ],
        successFactors: [
          'Intent signal identification',
          'Lifecycle stage targeting',
          'Local market considerations'
        ]
      }
    ];
  }

  // Public methods for accessing the library
  public getUseCasesByIndustry(industry: string): CustomerUseCase[] {
    return this.useCases.filter(useCase => 
      useCase.industry.includes(industry.toLowerCase())
    );
  }

  public getUseCaseById(id: string): CustomerUseCase | undefined {
    return this.useCases.find(useCase => useCase.id === id);
  }

  public searchUseCases(query: string): CustomerUseCase[] {
    const lowerQuery = query.toLowerCase();
    return this.useCases.filter(useCase =>
      useCase.title.toLowerCase().includes(lowerQuery) ||
      useCase.description.toLowerCase().includes(lowerQuery) ||
      useCase.businessOutcome.toLowerCase().includes(lowerQuery)
    );
  }

  public getBusinessOutcomeById(id: string): BusinessOutcome | undefined {
    return this.businessOutcomes.find(outcome => outcome.id === id);
  }

  public getIndustryConstraints(industry: string): IndustryConstraints | undefined {
    return this.industryConstraints.find(constraints => 
      constraints.industry === industry.toLowerCase()
    );
  }

  public getAllIndustries(): string[] {
    const industries = new Set<string>();
    this.useCases.forEach(useCase => {
      useCase.industry.forEach(ind => industries.add(ind));
    });
    return Array.from(industries).sort();
  }

  public getCapabilityMapping(): Record<string, string[]> {
    const mapping: Record<string, string[]> = {};
    this.useCases.forEach(useCase => {
      useCase.apiCapabilities.forEach(capability => {
        if (!mapping[capability]) {
          mapping[capability] = [];
        }
        mapping[capability].push(useCase.title);
      });
    });
    return mapping;
  }

  public assessFeasibility(requirements: {
    industry: string;
    dataSize: number;
    timeline: string;
    complexity: 'simple' | 'moderate' | 'complex';
  }): CustomerUseCase[] {
    return this.useCases.filter(useCase => {
      const industryMatch = useCase.industry.includes(requirements.industry.toLowerCase());
      const dataSizeOk = this.parseDataSize(useCase.minDataSize) <= requirements.dataSize;
      const complexityOk = this.getComplexityScore(useCase.complexity) <= this.getComplexityScore(requirements.complexity);
      
      return industryMatch && dataSizeOk && complexityOk;
    });
  }

  private parseDataSize(sizeString: string): number {
    const match = sizeString.match(/(\d+)/);
    return match ? parseInt(match[1]) : 0;
  }

  private getComplexityScore(complexity: string): number {
    const scores = { 'simple': 1, 'moderate': 2, 'complex': 3 };
    return scores[complexity as keyof typeof scores] || 1;
  }
}

export default CustomerUseCaseLibrary;