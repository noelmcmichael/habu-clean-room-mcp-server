#!/usr/bin/env python3
"""
Customer Support API endpoints for LiveRamp API expertise
Provides structured customer support responses and use case assessments
"""

import json
import logging
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from flask import Flask, request, jsonify
from flask_cors import CORS

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class CustomerUseCase:
    id: str
    title: str
    description: str
    industry: List[str]
    business_outcome: str
    api_capabilities: List[str]
    requirements: List[str]
    timeline: str
    limitations: List[str]
    alternatives: List[str]
    competitive_advantage: List[str]
    success_metrics: List[str]
    min_data_size: str
    complexity: str
    confidence: str

@dataclass
class SupportResponse:
    summary: str
    feasibility: str
    confidence: str
    business_value: str
    implementation: Dict
    limitations: List[str]
    alternatives: List[str]
    competitive_advantage: List[str]
    next_steps: List[str]
    pricing: Dict
    risk_factors: List[str]
    success_factors: List[str]

class CustomerSupportEngine:
    def __init__(self):
        self.use_cases = self._initialize_use_cases()
        self.competitive_advantages = self._initialize_competitive_advantages()
        
    def _initialize_use_cases(self) -> List[CustomerUseCase]:
        """Initialize the customer use case library"""
        return [
            CustomerUseCase(
                id="lookalike-modeling",
                title="Lookalike Audience Expansion",
                description="Find new customers similar to existing high-value customers using CRM data",
                industry=["retail", "e-commerce", "finance", "automotive", "travel"],
                business_outcome="Increase customer acquisition efficiency by 40-60%",
                api_capabilities=["habu_enhanced_templates", "habu_submit_query", "habu_get_results"],
                requirements=[
                    "Minimum 1,000 seed customers",
                    "Customer data with email or postal address", 
                    "Historical purchase/engagement data"
                ],
                timeline="24-48 hours for model creation",
                limitations=[
                    "Requires sufficient match rate (>60%)",
                    "Performance varies by industry vertical",
                    "Need ongoing model refresh (monthly recommended)"
                ],
                alternatives=[
                    "Cohort analysis for smaller datasets",
                    "Behavioral segmentation as alternative approach"
                ],
                competitive_advantage=[
                    "90%+ match rates vs industry 60-70%",
                    "Identity graph spans 300M+ US consumers",
                    "Real-time audience activation"
                ],
                success_metrics=[
                    "Match rate >60%",
                    "Audience size 5-10x seed list", 
                    "Conversion rate improvement >25%"
                ],
                min_data_size="1,000+ customers",
                complexity="simple",
                confidence="high"
            ),
            CustomerUseCase(
                id="customer-segmentation",
                title="Advanced Customer Segmentation", 
                description="Create behavioral and demographic customer segments for targeted marketing",
                industry=["retail", "finance", "travel", "entertainment", "b2b"],
                business_outcome="Increase campaign effectiveness through personalized targeting",
                api_capabilities=["habu_enhanced_templates", "habu_submit_query", "habu_get_results"],
                requirements=[
                    "Customer transaction/behavior data",
                    "Demographic information",
                    "Engagement history"
                ],
                timeline="3-5 days for analysis",
                limitations=[
                    "Segment quality depends on data richness",
                    "Minimum segment sizes for statistical significance",
                    "Regular refresh needed for accuracy"
                ],
                alternatives=[
                    "Simple RFM segmentation",
                    "Geographic segmentation", 
                    "Product affinity groups"
                ],
                competitive_advantage=[
                    "AI-powered segment discovery",
                    "Real-time segment updates",
                    "Privacy-compliant demographic enrichment"
                ],
                success_metrics=[
                    "5-10 distinct segments identified",
                    "Segment lift >20% vs broad targeting",
                    "Customer lifetime value increase"
                ],
                min_data_size="5,000+ customers",
                complexity="moderate",
                confidence="high"
            ),
            CustomerUseCase(
                id="identity-resolution",
                title="Customer Identity Resolution",
                description="Unify customer identities across devices, channels, and data sources",
                industry=["retail", "media", "finance", "healthcare", "automotive"],
                business_outcome="Create unified customer view for personalized experiences", 
                api_capabilities=["habu_list_partners", "habu_enhanced_templates", "habu_submit_query"],
                requirements=[
                    "Multiple data sources with customer identifiers",
                    "PII data (email, phone, address)",
                    "Device/session data"
                ],
                timeline="1-3 weeks depending on complexity",
                limitations=[
                    "Match rates vary by data quality",
                    "Privacy regulations may limit linking", 
                    "Requires ongoing maintenance"
                ],
                alternatives=[
                    "Probabilistic matching for lower confidence",
                    "Device-only linking",
                    "Email-based identity spine"
                ],
                competitive_advantage=[
                    "Industry-leading match rates",
                    "Privacy-first approach",
                    "Real-time identity graph updates"
                ],
                success_metrics=[
                    "Identity match rate >80%",
                    "Unified customer records",
                    "Cross-device attribution accuracy"
                ],
                min_data_size="1,000+ customers",
                complexity="complex", 
                confidence="high"
            )
        ]
    
    def _initialize_competitive_advantages(self) -> Dict[str, Dict]:
        """Initialize competitive advantages database"""
        return {
            "match_rates": {
                "advantage": "90%+ identity match rates",
                "proof": "Industry average is 60-70%",
                "customer_benefit": "More accurate targeting, better campaign performance"
            },
            "privacy": {
                "advantage": "Privacy-first architecture", 
                "proof": "No raw PII exposure, built-in compliance",
                "customer_benefit": "Reduced compliance risk, future-proof data strategy"
            },
            "scale": {
                "advantage": "300M+ consumer identity graph",
                "proof": "Largest authenticated identity dataset",
                "customer_benefit": "Better reach and audience discovery"
            },
            "speed": {
                "advantage": "Real-time data activation",
                "proof": "Sub-second audience updates", 
                "customer_benefit": "Respond to customer behavior immediately"
            }
        }
    
    def find_relevant_use_cases(self, query: str, industry: Optional[str] = None) -> List[CustomerUseCase]:
        """Find use cases relevant to the query"""
        query_lower = query.lower()
        relevant_cases = []
        
        for use_case in self.use_cases:
            # Check if query matches title or description
            if (query_lower in use_case.title.lower() or 
                query_lower in use_case.description.lower() or
                any(keyword in query_lower for keyword in ['lookalike', 'segment', 'identity', 'resolution', 'audience'])):
                
                # Boost relevance if industry matches
                if industry and industry.lower() in use_case.industry:
                    relevant_cases.insert(0, use_case)
                else:
                    relevant_cases.append(use_case)
        
        # If no matches found, return most common use cases
        if not relevant_cases:
            relevant_cases = [self.use_cases[0], self.use_cases[1]]  # lookalike and segmentation
            
        return relevant_cases[:3]  # Return top 3 matches
    
    def generate_support_response(self, query: str, industry: Optional[str] = None, 
                                customer_size: Optional[str] = None) -> SupportResponse:
        """Generate a comprehensive support response"""
        
        # Find relevant use cases
        relevant_cases = self.find_relevant_use_cases(query, industry)
        primary_case = relevant_cases[0] if relevant_cases else None
        
        if not primary_case:
            return self._generate_fallback_response(query)
        
        # Assess feasibility
        feasibility = "yes" if primary_case.confidence == "high" else "partially"
        if industry and industry.lower() not in primary_case.industry:
            feasibility = "partially"
        
        # Generate summary
        feasibility_emoji = {"yes": "✅", "partially": "⚠️", "no": "❌"}[feasibility]
        feasibility_text = {
            "yes": "Yes, this is fully supported!",
            "partially": "Partially supported - see details below", 
            "no": "Not directly supported - see alternatives"
        }[feasibility]
        
        summary = f"{feasibility_emoji} **{feasibility_text}**\n\n{primary_case.description}"
        
        # Generate implementation details
        implementation = {
            "timeline": primary_case.timeline,
            "requirements": primary_case.requirements,
            "complexity": f"{primary_case.complexity.capitalize()} implementation"
        }
        
        # Generate pricing guidance
        pricing_tier = {
            "small": "Starter",
            "medium": "Professional",
            "large": "Enterprise", 
            "enterprise": "Enterprise+"
        }.get(customer_size, "Professional")
        
        pricing = {
            "tier": pricing_tier,
            "considerations": [
                "Pricing based on data volume and use case complexity",
                "POC typically available at reduced cost",
                "Annual commitments offer better pricing"
            ]
        }
        
        # Generate next steps based on feasibility
        if feasibility == "yes":
            next_steps = [
                "Confirm data requirements and timeline",
                "Set up proof of concept (POC)",
                "Schedule technical integration planning"
            ]
        else:
            next_steps = [
                "Clarify specific requirements and constraints",
                "Explore alternative approaches", 
                "Consult with solution engineering team"
            ]
        
        return SupportResponse(
            summary=summary,
            feasibility=feasibility,
            confidence=primary_case.confidence,
            business_value=primary_case.business_outcome,
            implementation=implementation,
            limitations=primary_case.limitations,
            alternatives=primary_case.alternatives,
            competitive_advantage=primary_case.competitive_advantage,
            next_steps=next_steps,
            pricing=pricing,
            risk_factors=self._generate_risk_factors(primary_case),
            success_factors=primary_case.success_metrics
        )
    
    def _generate_fallback_response(self, query: str) -> SupportResponse:
        """Generate response when no specific use case matches"""
        return SupportResponse(
            summary="❓ **Need More Details** - Please provide more specific information about the use case",
            feasibility="no",
            confidence="low",
            business_value="Business value assessment requires more specific use case details",
            implementation={
                "timeline": "Timeline depends on specific requirements",
                "requirements": ["Detailed use case definition needed"],
                "complexity": "Cannot assess without more details"
            },
            limitations=["Requires more specific use case definition"],
            alternatives=["Contact solution engineering for custom approach"],
            competitive_advantage=["Privacy-first architecture", "Industry-leading match rates"],
            next_steps=["Provide more details about specific use case", "Schedule discovery call"],
            pricing={"tier": "Custom", "considerations": ["Pricing depends on specific requirements"]},
            risk_factors=["Unclear requirements increase implementation risk"],
            success_factors=["Clear use case definition", "Well-defined success metrics"]
        )
    
    def _generate_risk_factors(self, use_case: CustomerUseCase) -> List[str]:
        """Generate risk factors for a use case"""
        risks = []
        
        if use_case.confidence == "low":
            risks.append("Lower confidence in success - recommend POC")
        if use_case.complexity == "complex":
            risks.append("Complex implementation - ensure adequate resources")
        
        return risks if risks else ["Low risk implementation"]

# Create Flask app for API endpoints
app = Flask(__name__)
CORS(app)
support_engine = CustomerSupportEngine()

@app.route('/api/support-context', methods=['GET'])
def get_support_context():
    """Get current support context"""
    return jsonify({
        "commonQuestions": [
            "Can we do lookalike modeling?",
            "What's the minimum data size?", 
            "How long does implementation take?",
            "What industries do you support?"
        ],
        "industryFocus": ["retail", "automotive", "finance"],
        "customerTier": "enterprise",
        "supportLevel": "standard",
        "escalationThreshold": 3,
        "lastUpdate": "2025-01-22T10:00:00Z"
    })

@app.route('/api/technical-context', methods=['GET'])
def get_technical_context():
    """Get current technical context"""
    return jsonify({
        "availableTools": [
            "habu_list_partners",
            "habu_enhanced_templates", 
            "habu_submit_query",
            "habu_check_status",
            "habu_get_results",
            "habu_list_exports"
        ],
        "apiVersion": "2.0",
        "documentationVersion": "2.0.1",
        "limitations": [
            "Rate limits apply to high-volume queries",
            "Some features require partner agreements"
        ],
        "recentChanges": [
            "Added enhanced privacy controls",
            "Improved match rate algorithms"
        ],
        "capabilityMatrix": {
            "lookalike_modeling": True,
            "identity_resolution": True,
            "segmentation": True,
            "attribution": True,
            "real_time_activation": True
        },
        "integrationPatterns": [
            "REST API integration",
            "Batch file processing",
            "Real-time streaming"
        ]
    })

@app.route('/api/customer-support/assess', methods=['POST'])
def assess_customer_capability():
    """Assess customer capability request"""
    data = request.get_json()
    
    query = data.get('query', '')
    industry = data.get('industry')
    customer_size = data.get('customerSize')
    
    try:
        response = support_engine.generate_support_response(query, industry, customer_size)
        return jsonify(asdict(response))
    except Exception as e:
        logger.error(f"Error generating support response: {e}")
        return jsonify({"error": "Failed to generate response"}), 500

@app.route('/api/customer-support/use-cases', methods=['GET'])
def list_use_cases():
    """List available use cases, optionally filtered by industry"""
    industry = request.args.get('industry')
    
    use_cases = support_engine.use_cases
    if industry:
        use_cases = [uc for uc in use_cases if industry.lower() in uc.industry]
    
    return jsonify([asdict(uc) for uc in use_cases])

@app.route('/api/customer-support/industries', methods=['GET'])
def list_industries():
    """List supported industries"""
    industries = set()
    for use_case in support_engine.use_cases:
        industries.update(use_case.industry)
    
    return jsonify(sorted(list(industries)))

@app.route('/api/customer-support/competitive-advantages', methods=['GET'])
def list_competitive_advantages():
    """List competitive advantages"""
    return jsonify(support_engine.competitive_advantages)

if __name__ == '__main__':
    app.run(debug=True, port=5001)