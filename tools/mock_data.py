"""
Mock data for Habu Clean Room API testing
Provides realistic sample data when real cleanrooms aren't available
"""
import json
import uuid
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any

class HabuMockData:
    """Provides mock data for testing Habu Clean Room functionality"""
    
    def __init__(self):
        self.mock_cleanrooms = self._generate_mock_cleanrooms()
        self.mock_templates = self._generate_mock_templates()
        self.mock_queries = {}  # Will store submitted queries
        
    def _generate_mock_cleanrooms(self) -> List[Dict[str, Any]]:
        """Generate realistic mock cleanrooms with partners"""
        return [
            {
                "id": "cr-001-data-marketplace",
                "name": "Premium Retail Data Collective",
                "description": "Enterprise-grade clean room for premium retail brand collaboration and customer insights",
                "status": "ACTIVE",
                "created_date": "2024-03-15",
                "data_volume": "2.4B records",
                "monthly_queries": 1247,
                "partners": [
                    {
                        "id": "partner-001",
                        "name": "Meta Business",
                        "organization": "Meta Platforms Inc",
                        "status": "ACTIVE",
                        "joined_date": "2024-03-15",
                        "data_types": ["Customer Demographics", "Purchase History", "Social Engagement", "App Usage Patterns", "Interest Graphs"],
                        "data_volume": "847M profiles",
                        "update_frequency": "Daily",
                        "data_quality_score": 94,
                        "key_metrics": ["Reach: 1.2B users", "Engagement Rate: 3.4%", "Conversion Rate: 2.1%"]
                    },
                    {
                        "id": "partner-002", 
                        "name": "Amazon DSP",
                        "organization": "Amazon.com Inc",
                        "status": "ACTIVE",
                        "joined_date": "2024-03-20",
                        "data_types": ["Shopping Behavior", "Product Views", "Purchase Intent", "Category Affinity", "Search Patterns"],
                        "data_volume": "623M shoppers",
                        "update_frequency": "Real-time",
                        "data_quality_score": 97,
                        "key_metrics": ["AOV: $127", "Purchase Rate: 8.7%", "Return Rate: 4.2%"]
                    },
                    {
                        "id": "partner-003",
                        "name": "Google Marketing Platform",
                        "organization": "Google LLC", 
                        "status": "ACTIVE",
                        "joined_date": "2024-03-25",
                        "data_types": ["Search History", "Ad Interactions", "YouTube Engagement", "Location Data", "Device Usage"],
                        "data_volume": "1.1B users",
                        "update_frequency": "Hourly",
                        "data_quality_score": 96,
                        "key_metrics": ["CTR: 2.8%", "CPC: $1.24", "Quality Score: 8.2/10"]
                    },
                    {
                        "id": "partner-004",
                        "name": "Walmart Connect",
                        "organization": "Walmart Inc",
                        "status": "ACTIVE",
                        "joined_date": "2024-04-01",
                        "data_types": ["In-store Purchases", "Online Orders", "Customer Profiles", "Pickup/Delivery Data", "Price Sensitivity"],
                        "data_volume": "230M customers",
                        "update_frequency": "Daily",
                        "data_quality_score": 93,
                        "key_metrics": ["Basket Size: $67", "Visit Frequency: 2.3x/week", "Digital Mix: 31%"]
                    },
                    {
                        "id": "partner-005",
                        "name": "Target Media Network",
                        "organization": "Target Corporation",
                        "status": "ACTIVE",
                        "joined_date": "2024-04-05",
                        "data_types": ["Purchase Data", "Store Visits", "Digital Engagement", "RedCard Usage", "Style Preferences"],
                        "data_volume": "180M guests",
                        "update_frequency": "Daily", 
                        "data_quality_score": 91,
                        "key_metrics": ["Guest Loyalty: 73%", "Digital Sales: 18.3%", "Same-day Services: 12%"]
                    },
                    {
                        "id": "partner-006",
                        "name": "The Trade Desk",
                        "organization": "The Trade Desk Inc",
                        "status": "ACTIVE",
                        "joined_date": "2024-04-10",
                        "data_types": ["Programmatic Ad Data", "Cross-Device Tracking", "Brand Safety Metrics", "Attribution Data"],
                        "data_volume": "500M devices",
                        "update_frequency": "Real-time",
                        "data_quality_score": 95,
                        "key_metrics": ["Reach Scale: 500M", "Brand Safety: 99.7%", "Viewability: 87%"]
                    }
                ]
            },
            {
                "id": "cr-002-financial-services",
                "name": "Financial Services Intelligence Hub",
                "description": "Secure clean room for financial services customer insights and risk analytics",
                "status": "ACTIVE",
                "created_date": "2024-02-01", 
                "data_volume": "890M records",
                "monthly_queries": 643,
                "partners": [
                    {
                        "id": "partner-007",
                        "name": "Chase Media Solutions",
                        "organization": "JPMorgan Chase & Co",
                        "status": "ACTIVE",
                        "joined_date": "2024-02-01",
                        "data_types": ["Transaction Data", "Credit Profiles", "Spending Patterns", "Travel Data", "Merchant Categories"],
                        "data_volume": "65M customers",
                        "update_frequency": "Daily",
                        "data_quality_score": 98,
                        "key_metrics": ["Avg Balance: $8,420", "Monthly Transactions: 47", "Credit Score Avg: 724"]
                    },
                    {
                        "id": "partner-008",
                        "name": "American Express Media",
                        "organization": "American Express Co",
                        "status": "ACTIVE", 
                        "joined_date": "2024-02-15",
                        "data_types": ["Premium Spending", "Travel Patterns", "Merchant Loyalty", "Rewards Usage", "Lifestyle Segments"],
                        "data_volume": "54M cardholders",
                        "update_frequency": "Daily",
                        "data_quality_score": 97,
                        "key_metrics": ["Avg Spend: $2,340/mo", "Travel %: 23%", "Rewards Redemption: 81%"]
                    }
                ]
            },
            {
                "id": "cr-003-healthcare-analytics",
                "name": "Healthcare Analytics Consortium",
                "description": "Privacy-compliant clean room for healthcare outcomes and patient journey analysis",
                "status": "ACTIVE",
                "created_date": "2024-01-10",
                "data_volume": "1.2B records",
                "monthly_queries": 892,
                "partners": [
                    {
                        "id": "partner-009",
                        "name": "CVS Health Media Exchange",
                        "organization": "CVS Health Corporation",
                        "status": "ACTIVE",
                        "joined_date": "2024-01-10",
                        "data_types": ["Pharmacy Data", "Health Outcomes", "Prescription Patterns", "Wellness Programs", "Chronic Conditions"],
                        "data_volume": "85M patients",
                        "update_frequency": "Weekly",
                        "data_quality_score": 96,
                        "key_metrics": ["Medication Adherence: 78%", "Preventive Care: 64%", "Health Score Avg: 7.2/10"]
                    }
                ]
            }
        ]
    
    def _generate_mock_templates(self) -> List[Dict[str, Any]]:
        """Generate realistic query templates"""
        return [
            {
                "id": "tmpl-001-audience-overlap",
                "name": "Cross-Platform Audience Overlap Analysis", 
                "description": "Identify shared customer segments across partner datasets with privacy-preserving overlap calculations and lifetime value analysis",
                "category": "Customer Analytics",
                "complexity": "Medium",
                "data_requirements": ["Customer identifiers", "Purchase history", "Engagement metrics"],
                "business_value": "Discover high-value customer segments for coordinated marketing strategies",
                "parameters": [
                    {"name": "partner_1", "type": "string", "required": True, "description": "Primary partner dataset (e.g., 'Meta Business', 'Amazon DSP')"},
                    {"name": "partner_2", "type": "string", "required": True, "description": "Secondary partner dataset for comparison"},
                    {"name": "date_range", "type": "string", "required": False, "description": "Analysis period (default: last 90 days)", "default": "90d"},
                    {"name": "minimum_interactions", "type": "integer", "required": False, "description": "Minimum interaction threshold", "default": 3},
                    {"name": "include_ltv", "type": "boolean", "required": False, "description": "Include lifetime value analysis", "default": True}
                ],
                "estimated_runtime": "7-12 minutes",
                "output_format": "Statistical summary with segment profiles and actionable insights"
            },
            {
                "id": "tmpl-002-advanced-lookalike",
                "name": "AI-Powered Lookalike Audience Discovery",
                "description": "Advanced machine learning model to discover high-converting prospects based on multi-dimensional behavioral and demographic patterns",
                "category": "Machine Learning",
                "complexity": "High",
                "data_requirements": ["Seed audience profiles", "Behavioral data", "Conversion events"],
                "business_value": "Expand reach to high-intent prospects with 3-5x better conversion rates",
                "parameters": [
                    {"name": "seed_audience", "type": "string", "required": True, "description": "High-value seed audience definition"},
                    {"name": "target_partners", "type": "array", "required": True, "description": "Partners to search for lookalikes"},
                    {"name": "similarity_threshold", "type": "float", "required": False, "description": "Model confidence threshold (0.75-0.95)", "default": 0.85},
                    {"name": "audience_size_target", "type": "integer", "required": False, "description": "Target audience size", "default": 500000},
                    {"name": "model_features", "type": "array", "required": False, "description": "Custom features to include", "default": ["purchase_behavior", "engagement_depth", "category_affinity"]}
                ],
                "estimated_runtime": "18-28 minutes",
                "output_format": "Ranked prospect list with similarity scores and predicted performance metrics"
            },
            {
                "id": "tmpl-003-customer-journey-attribution", 
                "name": "Unified Customer Journey Attribution",
                "description": "Comprehensive multi-touch attribution analysis across all partner touchpoints with incrementality measurement",
                "category": "Attribution & Measurement",
                "complexity": "High",
                "data_requirements": ["Touchpoint data", "Conversion events", "Customer journey paths"],
                "business_value": "Optimize media spend allocation with precise channel contribution measurement",
                "parameters": [
                    {"name": "conversion_events", "type": "array", "required": True, "description": "Target conversion events to analyze"},
                    {"name": "attribution_window", "type": "integer", "required": False, "description": "Attribution window in days", "default": 30},
                    {"name": "attribution_model", "type": "string", "required": False, "description": "Attribution model type", "default": "data_driven"},
                    {"name": "include_incrementality", "type": "boolean", "required": False, "description": "Include incrementality analysis", "default": True},
                    {"name": "cross_device", "type": "boolean", "required": False, "description": "Include cross-device tracking", "default": True}
                ],
                "estimated_runtime": "15-25 minutes",
                "output_format": "Channel attribution weights with incrementality scores and optimization recommendations"
            },
            {
                "id": "tmpl-004-behavioral-segmentation",
                "name": "Advanced Behavioral Segmentation & Personas",
                "description": "AI-driven customer segmentation using unsupervised learning to discover actionable micro-segments and persona profiles",
                "category": "Customer Intelligence", 
                "complexity": "High",
                "data_requirements": ["Transaction data", "Behavioral signals", "Demographic attributes"],
                "business_value": "Unlock 20-40% improvement in campaign performance through precise audience targeting",
                "parameters": [
                    {"name": "segmentation_method", "type": "string", "required": False, "description": "Clustering algorithm", "default": "advanced_kmeans"},
                    {"name": "min_segment_size", "type": "integer", "required": False, "description": "Minimum viable segment size", "default": 10000},
                    {"name": "behavioral_dimensions", "type": "array", "required": True, "description": "Key behavioral features to analyze"},
                    {"name": "include_personas", "type": "boolean", "required": False, "description": "Generate detailed persona profiles", "default": True},
                    {"name": "seasonal_adjustment", "type": "boolean", "required": False, "description": "Account for seasonal patterns", "default": True}
                ],
                "estimated_runtime": "25-35 minutes",
                "output_format": "Segment profiles with persona descriptions, sizing, and targeting recommendations"
            },
            {
                "id": "tmpl-005-performance-optimization",
                "name": "Real-Time Campaign Performance Optimization",
                "description": "Dynamic optimization recommendations using real-time performance data and predictive analytics",
                "category": "Performance Optimization",
                "complexity": "Medium",
                "data_requirements": ["Campaign performance data", "Audience response metrics", "Conversion tracking"],
                "business_value": "Achieve 15-30% improvement in ROAS through data-driven optimization",
                "parameters": [
                    {"name": "campaigns", "type": "array", "required": True, "description": "Campaign identifiers to analyze"},
                    {"name": "optimization_goals", "type": "array", "required": True, "description": "Primary KPIs to optimize (ROAS, CPA, CTR, etc.)"},
                    {"name": "time_granularity", "type": "string", "required": False, "description": "Analysis granularity", "default": "daily"},
                    {"name": "include_forecasting", "type": "boolean", "required": False, "description": "Include performance forecasts", "default": True},
                    {"name": "budget_constraints", "type": "object", "required": False, "description": "Budget allocation constraints"}
                ],
                "estimated_runtime": "10-18 minutes",
                "output_format": "Optimization recommendations with projected impact and implementation priority"
            },
            {
                "id": "tmpl-006-competitive-intelligence",
                "name": "Market Share & Competitive Intelligence",
                "description": "Analyze market positioning, share of voice, and competitive dynamics across partner ecosystems",
                "category": "Market Intelligence",
                "complexity": "Medium",
                "data_requirements": ["Market data", "Competitive metrics", "Share of voice data"],
                "business_value": "Identify market opportunities and competitive threats with actionable insights",
                "parameters": [
                    {"name": "market_category", "type": "string", "required": True, "description": "Product/service category to analyze"},
                    {"name": "competitive_set", "type": "array", "required": False, "description": "Specific competitors to benchmark against"},
                    {"name": "geographic_scope", "type": "string", "required": False, "description": "Geographic market scope", "default": "national"},
                    {"name": "time_comparison", "type": "string", "required": False, "description": "Historical comparison period", "default": "year_over_year"}
                ],
                "estimated_runtime": "12-20 minutes",
                "output_format": "Market share analysis with competitive positioning and growth opportunities"
            },
            {
                "id": "tmpl-007-churn-prediction",
                "name": "Customer Churn Risk Prediction & Prevention",
                "description": "Machine learning model to identify at-risk customers and recommend retention strategies",
                "category": "Customer Retention",
                "complexity": "High",
                "data_requirements": ["Customer lifecycle data", "Engagement metrics", "Transaction patterns"],
                "business_value": "Reduce churn by 25-40% through proactive intervention strategies",
                "parameters": [
                    {"name": "prediction_horizon", "type": "integer", "required": False, "description": "Prediction window in days", "default": 90},
                    {"name": "risk_threshold", "type": "float", "required": False, "description": "Churn risk threshold", "default": 0.7},
                    {"name": "include_interventions", "type": "boolean", "required": False, "description": "Include retention strategy recommendations", "default": True},
                    {"name": "segment_analysis", "type": "boolean", "required": False, "description": "Analyze churn patterns by segment", "default": True}
                ],
                "estimated_runtime": "20-30 minutes",
                "output_format": "Risk-scored customer list with personalized retention recommendations"
            },
            {
                "id": "tmpl-008-lifetime-value",
                "name": "Predictive Customer Lifetime Value Analysis",
                "description": "Advanced CLV modeling with revenue forecasting and value-based segmentation",
                "category": "Revenue Analytics",
                "complexity": "High", 
                "data_requirements": ["Transaction history", "Customer demographics", "Engagement data"],
                "business_value": "Optimize acquisition spend and increase revenue per customer by 20-35%",
                "parameters": [
                    {"name": "prediction_period", "type": "integer", "required": False, "description": "CLV prediction period in months", "default": 24},
                    {"name": "discount_rate", "type": "float", "required": False, "description": "Discount rate for NPV calculation", "default": 0.1},
                    {"name": "include_acquisition_cost", "type": "boolean", "required": False, "description": "Factor in customer acquisition costs", "default": True},
                    {"name": "segment_by_value", "type": "boolean", "required": False, "description": "Create value-based segments", "default": True}
                ],
                "estimated_runtime": "15-25 minutes",
                "output_format": "CLV predictions with value tiers and investment recommendations"
            }
        ]
    
    def get_mock_partners(self) -> List[Dict[str, Any]]:
        """Get all partners from all cleanrooms"""
        all_partners = []
        for cleanroom in self.mock_cleanrooms:
            for partner in cleanroom["partners"]:
                partner_copy = partner.copy()
                partner_copy["cleanroom_id"] = cleanroom["id"]
                partner_copy["cleanroom_name"] = cleanroom["name"]
                all_partners.append(partner_copy)
        return all_partners
    
    def get_mock_templates(self) -> List[Dict[str, Any]]:
        """Get all available query templates"""
        return self.mock_templates
    
    def submit_mock_query(self, template_id: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Submit a mock query and return query metadata"""
        query_id = f"query-{uuid.uuid4().hex[:8]}"
        
        # Find template
        template = next((t for t in self.mock_templates if t["id"] == template_id), None)
        if not template:
            return {
                "status": "error",
                "error": f"Template {template_id} not found",
                "available_templates": [t["id"] for t in self.mock_templates]
            }
        
        # Create mock query
        query = {
            "id": query_id,
            "template_id": template_id,
            "template_name": template["name"],
            "parameters": parameters,
            "status": "QUEUED",
            "submitted_at": datetime.now().isoformat(),
            "estimated_completion": (datetime.now() + timedelta(minutes=random.randint(5, 25))).isoformat(),
            "progress_percent": 0
        }
        
        self.mock_queries[query_id] = query
        
        return {
            "status": "success",
            "query_id": query_id,
            "query_status": "QUEUED",
            "template_name": template["name"],
            "estimated_runtime": template["estimated_runtime"],
            "message": f"Query {query_id} submitted successfully using template '{template['name']}'"
        }
    
    def check_mock_query_status(self, query_id: str) -> Dict[str, Any]:
        """Check status of a mock query"""
        if query_id not in self.mock_queries:
            return {
                "status": "error",
                "error": f"Query {query_id} not found",
                "available_queries": list(self.mock_queries.keys())
            }
        
        query = self.mock_queries[query_id]
        
        # Simulate query progression
        submitted_time = datetime.fromisoformat(query["submitted_at"])
        elapsed_minutes = (datetime.now() - submitted_time).total_seconds() / 60
        
        if elapsed_minutes < 2:
            status = "QUEUED"
            progress = 0
        elif elapsed_minutes < 5:
            status = "RUNNING"
            progress = min(90, int(elapsed_minutes * 20))
        else:
            status = "COMPLETED"
            progress = 100
        
        # Update query status
        query["status"] = status
        query["progress_percent"] = progress
        
        next_actions = []
        if status == "COMPLETED":
            next_actions.append("Query completed! Use 'get results' to view the analysis.")
        elif status == "RUNNING":
            next_actions.append(f"Query is {progress}% complete. Check back in a few minutes.")
        else:
            next_actions.append("Query is in queue. Processing will begin shortly.")
        
        return {
            "status": "success",
            "query_id": query_id,
            "query_status": status,
            "progress_percent": progress,
            "template_name": query["template_name"],
            "submitted_at": query["submitted_at"],
            "next_actions": next_actions
        }
    
    def get_mock_query_results(self, query_id: str) -> Dict[str, Any]:
        """Get results for a completed mock query"""
        if query_id not in self.mock_queries:
            return {
                "status": "error", 
                "error": f"Query {query_id} not found"
            }
        
        query = self.mock_queries[query_id]
        
        # Check if query is completed
        status_check = self.check_mock_query_status(query_id)
        if status_check["query_status"] != "COMPLETED":
            return {
                "status": "error",
                "error": f"Query {query_id} is not yet completed (status: {status_check['query_status']})",
                "current_status": status_check["query_status"],
                "progress": status_check["progress_percent"]
            }
        
        # Generate mock results based on template
        template_id = query["template_id"]
        
        if template_id == "tmpl-001-audience-overlap":
            results = self._generate_overlap_results(query["parameters"])
        elif template_id == "tmpl-002-advanced-lookalike":
            results = self._generate_lookalike_results(query["parameters"])
        elif template_id == "tmpl-003-customer-journey-attribution":
            results = self._generate_attribution_results(query["parameters"])
        elif template_id == "tmpl-004-behavioral-segmentation":
            results = self._generate_segmentation_results(query["parameters"])
        elif template_id == "tmpl-005-performance-optimization":
            results = self._generate_optimization_results(query["parameters"])
        elif template_id == "tmpl-006-competitive-intelligence":
            results = self._generate_competitive_results(query["parameters"])
        elif template_id == "tmpl-007-churn-prediction":
            results = self._generate_churn_results(query["parameters"])
        elif template_id == "tmpl-008-lifetime-value":
            results = self._generate_ltv_results(query["parameters"])
        else:
            results = self._generate_generic_results()
        
        return {
            "status": "success",
            "query_id": query_id,
            "template_name": query["template_name"],
            "completed_at": datetime.now().isoformat(),
            "record_count": results["record_count"],
            "business_summary": results["business_summary"],
            "detailed_results": results["detailed_results"],
            "insights": results.get("insights", []),
            "next_steps": results.get("next_steps", [])
        }
    
    def _generate_overlap_results(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Generate mock audience overlap results"""
        partner_1 = parameters.get("partner_1", "Partner A")
        partner_2 = parameters.get("partner_2", "Partner B")
        
        # Generate realistic data sizes based on partner
        partner_sizes = {
            "Meta Business": random.randint(45000000, 55000000),
            "Amazon DSP": random.randint(35000000, 45000000), 
            "Google Marketing Platform": random.randint(55000000, 65000000),
            "Walmart Connect": random.randint(25000000, 35000000),
            "Target Media Network": random.randint(20000000, 30000000)
        }
        
        total_audience_1 = partner_sizes.get(partner_1, random.randint(500000, 2000000))
        total_audience_2 = partner_sizes.get(partner_2, random.randint(600000, 1800000))
        
        # More sophisticated overlap calculation
        overlap_percent = random.uniform(18, 42)
        overlap_size = int(min(total_audience_1, total_audience_2) * overlap_percent / 100)
        
        # Calculate advanced metrics
        ltv_lift = random.uniform(23, 48)
        engagement_lift = random.uniform(120, 280)
        cross_platform_rate = random.uniform(65, 85)
        premium_category_index = random.uniform(1.4, 2.8)
        
        # Generate segment analysis
        segments = [
            {"name": "High-Value Loyalists", "size": int(overlap_size * 0.23), "ltv_multiplier": 3.2, "engagement_score": 94},
            {"name": "Frequent Cross-Shoppers", "size": int(overlap_size * 0.34), "ltv_multiplier": 2.1, "engagement_score": 78},
            {"name": "Premium Category Enthusiasts", "size": int(overlap_size * 0.28), "ltv_multiplier": 2.7, "engagement_score": 86},
            {"name": "Emerging High-Value", "size": int(overlap_size * 0.15), "ltv_multiplier": 1.8, "engagement_score": 71}
        ]
        
        # Geographic distribution
        top_markets = [
            {"market": "New York-Newark", "percentage": random.uniform(12, 18), "ltv_index": random.uniform(1.2, 1.6)},
            {"market": "Los Angeles-Long Beach", "percentage": random.uniform(10, 15), "ltv_index": random.uniform(1.1, 1.4)},
            {"market": "Chicago-Naperville", "percentage": random.uniform(8, 12), "ltv_index": random.uniform(1.0, 1.3)},
            {"market": "Dallas-Fort Worth", "percentage": random.uniform(7, 11), "ltv_index": random.uniform(1.1, 1.4)},
            {"market": "San Francisco-Oakland", "percentage": random.uniform(6, 10), "ltv_index": random.uniform(1.3, 1.7)}
        ]
        
        return {
            "record_count": overlap_size,
            "business_summary": f"Cross-platform audience overlap analysis between {partner_1} and {partner_2} reveals {overlap_percent:.1f}% overlap ({overlap_size:,} customers) with {ltv_lift:.1f}% higher lifetime value and {engagement_lift:.0f}% above-average cross-platform engagement rates. Analysis identifies 4 distinct high-value segments with premium category affinity index of {premium_category_index:.1f}x.",
            "detailed_results": {
                "analysis_period": parameters.get("date_range", "90 days"),
                "partner_1": {"name": partner_1, "audience_size": total_audience_1, "overlap_rate": f"{(overlap_size/total_audience_1)*100:.2f}%"},
                "partner_2": {"name": partner_2, "audience_size": total_audience_2, "overlap_rate": f"{(overlap_size/total_audience_2)*100:.2f}%"},
                "overlap_metrics": {
                    "total_overlap": overlap_size,
                    "overlap_percentage": round(overlap_percent, 2),
                    "cross_platform_engagement_rate": f"{cross_platform_rate:.1f}%",
                    "lifetime_value_lift": f"+{ltv_lift:.1f}%",
                    "premium_category_index": round(premium_category_index, 2)
                },
                "unique_audiences": {
                    f"unique_to_{partner_1.lower().replace(' ', '_')}": total_audience_1 - overlap_size,
                    f"unique_to_{partner_2.lower().replace(' ', '_')}": total_audience_2 - overlap_size
                },
                "segment_breakdown": segments,
                "top_geographic_markets": top_markets
            },
            "insights": [
                f"Shared customers demonstrate {ltv_lift:.1f}% higher lifetime value compared to single-platform users",
                f"Cross-platform engagement rates exceed single-platform by {engagement_lift:.0f}%, indicating strong multi-channel behavior",
                f"Premium product categories show {premium_category_index:.1f}x higher affinity in overlap audience",
                f"High-Value Loyalists segment ({segments[0]['size']:,} customers) shows 3.2x LTV multiplier with 94% engagement score",
                "Geographic concentration in high-income metropolitan areas presents expansion opportunities",
                f"Emerging High-Value segment ({segments[3]['size']:,} customers) represents untapped growth potential"
            ],
            "next_steps": [
                "Implement coordinated cross-platform campaigns targeting High-Value Loyalists segment",
                "Develop lookalike models based on premium category enthusiasts characteristics",
                "Create unified customer journey mapping for cross-platform optimization",
                "Establish joint value propositions for frequent cross-shoppers segment",
                "Expand geographic presence in underrepresented high-LTV markets",
                "Design retention strategies specifically for emerging high-value prospects"
            ],
            "strategic_recommendations": [
                {"priority": "High", "action": "Launch coordinated premium campaigns", "projected_impact": "+23% ROAS improvement"},
                {"priority": "High", "action": "Implement cross-platform frequency capping", "projected_impact": "+15% efficiency gain"},
                {"priority": "Medium", "action": "Develop joint loyalty programs", "projected_impact": "+18% retention rate"},
                {"priority": "Medium", "action": "Create unified attribution framework", "projected_impact": "+12% budget optimization"}
            ]
        }
    
    def _generate_lookalike_results(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Generate mock lookalike modeling results"""
        seed_audience = parameters.get("seed_audience", "High-Value Customers")
        target_partners = parameters.get("target_partners", ["Target Partner"])
        similarity_threshold = parameters.get("similarity_threshold", 0.85)
        
        # Generate sophisticated lookalike metrics
        lookalike_size = random.randint(450000, 1200000)
        model_confidence = random.uniform(0.87, 0.96)
        similarity_score = random.uniform(max(0.75, similarity_threshold - 0.05), min(0.95, similarity_threshold + 0.08))
        conversion_lift = random.uniform(28, 52)
        cpa_improvement = random.uniform(18, 35)
        
        # Feature importance analysis
        predictive_features = [
            {"feature": "Purchase Frequency Score", "importance": random.uniform(0.18, 0.24), "correlation": 0.89},
            {"feature": "Category Affinity Index", "importance": random.uniform(0.14, 0.20), "correlation": 0.76},
            {"feature": "Engagement Depth Score", "importance": random.uniform(0.12, 0.18), "correlation": 0.82},
            {"feature": "Cross-Device Behavior", "importance": random.uniform(0.10, 0.16), "correlation": 0.71},
            {"feature": "Seasonal Purchase Patterns", "importance": random.uniform(0.08, 0.14), "correlation": 0.68},
            {"feature": "Social Engagement Level", "importance": random.uniform(0.06, 0.12), "correlation": 0.64},
            {"feature": "Geographic Clustering", "importance": random.uniform(0.05, 0.10), "correlation": 0.59}
        ]
        
        # Performance projections by segment
        performance_tiers = [
            {"tier": "Tier 1 - Ultra High Similarity", "size": int(lookalike_size * 0.15), "similarity": 0.92, "projected_cvr": "8.7%", "projected_cpa": "$34"},
            {"tier": "Tier 2 - High Similarity", "size": int(lookalike_size * 0.35), "similarity": 0.87, "projected_cvr": "6.4%", "projected_cpa": "$47"},
            {"tier": "Tier 3 - Medium-High Similarity", "size": int(lookalike_size * 0.35), "similarity": 0.82, "projected_cvr": "4.8%", "projected_cpa": "$62"},
            {"tier": "Tier 4 - Medium Similarity", "size": int(lookalike_size * 0.15), "similarity": 0.78, "projected_cvr": "3.2%", "projected_cpa": "$78"}
        ]
        
        # Geographic and demographic insights
        top_markets = [
            {"market": "San Francisco-Oakland", "concentration": "23.4%", "similarity_index": 1.34},
            {"market": "Seattle-Tacoma", "concentration": "18.7%", "similarity_index": 1.28},
            {"market": "New York-Newark", "concentration": "16.2%", "similarity_index": 1.21},
            {"market": "Boston-Cambridge", "concentration": "14.8%", "similarity_index": 1.19}
        ]
        
        demographic_profile = {
            "age_distribution": {"25-34": "31%", "35-44": "28%", "45-54": "22%", "other": "19%"},
            "income_brackets": {"$75K-$100K": "34%", "$100K-$150K": "28%", "$150K+": "24%", "other": "14%"},
            "education_level": {"Bachelor's+": "67%", "Some College": "21%", "other": "12%"},
            "household_composition": {"Families with children": "43%", "Couples no children": "31%", "other": "26%"}
        }
        
        return {
            "record_count": lookalike_size,
            "business_summary": f"AI-powered lookalike model successfully identified {lookalike_size:,} high-similarity prospects from {len(target_partners)} partner ecosystem(s) with {similarity_score:.2f} average similarity score. Model demonstrates {model_confidence:.1%} confidence and projects {conversion_lift:.1f}% conversion lift with {cpa_improvement:.1f}% CPA improvement over baseline targeting. Tier 1 ultra-high similarity segment ({performance_tiers[0]['size']:,} prospects) shows exceptional 8.7% projected conversion rate.",
            "detailed_results": {
                "model_performance": {
                    "total_lookalike_audience": lookalike_size,
                    "average_similarity_score": round(similarity_score, 3),
                    "model_confidence_level": f"{model_confidence:.1%}",
                    "cross_validation_accuracy": f"{random.uniform(0.84, 0.93):.1%}",
                    "feature_count": len(predictive_features)
                },
                "projected_performance": {
                    "conversion_lift_vs_baseline": f"+{conversion_lift:.1f}%",
                    "cpa_improvement": f"-{cpa_improvement:.1f}%",
                    "roas_improvement": f"+{random.uniform(22, 45):.1f}%",
                    "reach_expansion": f"+{random.randint(180, 340)}%"
                },
                "feature_importance": predictive_features,
                "performance_tiers": performance_tiers,
                "geographic_insights": {
                    "top_concentrated_markets": top_markets,
                    "geographic_similarity_score": random.uniform(0.78, 0.91)
                },
                "demographic_profile": demographic_profile
            },
            "insights": [
                f"Model achieves {model_confidence:.1%} confidence with strong predictive power across all similarity tiers",
                f"Purchase Frequency Score emerges as top predictor with {predictive_features[0]['correlation']:.2f} correlation to seed audience",
                f"Geographic clustering in high-income metropolitan areas shows {top_markets[0]['similarity_index']:.2f}x concentration index",
                f"Tier 1 prospects demonstrate premium characteristics with projected 8.7% conversion rate vs. 2.1% baseline",
                f"Cross-device behavior patterns strongly correlate ({predictive_features[3]['correlation']:.2f}) with high-value customer traits",
                "Seasonal purchase alignment indicates 89% pattern similarity with seed audience behavior"
            ],
            "next_steps": [
                "Implement tiered campaign strategy prioritizing Tier 1 ultra-high similarity prospects",
                "Deploy dynamic creative optimization targeting top predictive features",
                "Establish geographic concentration strategy for high-similarity markets",
                "Create progressive profiling campaigns to enhance feature data collection",
                "Develop retention strategies for converted lookalike prospects",
                "Monitor model performance and retrain quarterly with updated behavioral data"
            ],
            "activation_strategy": [
                {"phase": "Phase 1 - Pilot", "audience": "Tier 1 (Ultra High)", "budget_allocation": "40%", "expected_results": "Validate model accuracy"},
                {"phase": "Phase 2 - Scale", "audience": "Tier 1+2 (High)", "budget_allocation": "70%", "expected_results": "Scale proven segments"},
                {"phase": "Phase 3 - Expand", "audience": "All Tiers", "budget_allocation": "100%", "expected_results": "Full market penetration"}
            ]
        }
    
    def _generate_attribution_results(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Generate mock attribution analysis results"""
        total_conversions = random.randint(50000, 150000)
        platforms = parameters.get("platforms", ["Meta", "Google", "Amazon"])
        
        attribution_data = {}
        remaining = 100.0
        for i, platform in enumerate(platforms[:-1]):
            share = random.uniform(15, 35)
            attribution_data[platform] = min(share, remaining - 10)
            remaining -= attribution_data[platform]
        attribution_data[platforms[-1]] = remaining
        
        return {
            "record_count": total_conversions,
            "business_summary": f"Cross-platform attribution analysis of {total_conversions:,} conversions reveals multi-touch customer journeys with {random.randint(60, 85)}% of conversions involving multiple touchpoints.",
            "detailed_results": {
                "total_conversions": total_conversions,
                "platform_attribution": attribution_data,
                "average_touchpoints": random.uniform(2.3, 4.1),
                "attribution_window_days": parameters.get("attribution_window", 30)
            },
            "insights": [
                f"First-touch attribution shows {random.randint(20, 40)}% difference from last-touch",
                "Upper-funnel channels drive 3x more assisted conversions",
                "Cross-device journeys account for significant conversion volume"
            ]
        }
    
    def _generate_segmentation_results(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Generate mock customer segmentation results"""
        segments_found = random.randint(5, 12)
        total_customers = random.randint(800000, 2500000)
        
        return {
            "record_count": total_customers,
            "business_summary": f"Customer segment discovery identified {segments_found} distinct behavioral segments across {total_customers:,} customers, revealing new high-value micro-segments with {random.randint(25, 50)}% higher engagement rates.",
            "detailed_results": {
                "segments_discovered": segments_found,
                "total_customers_analyzed": total_customers,
                "largest_segment_size": random.randint(150000, 400000),
                "smallest_segment_size": random.randint(25000, 80000),
                "segment_characteristics": ["Premium Shoppers", "Value Seekers", "Brand Loyalists", "Trend Followers"]
            },
            "insights": [
                "Emerging 'Conscious Consumers' segment shows high growth potential",
                f"Cross-segment customer lifetime value varies by up to {random.randint(200, 400)}%",
                "Geographic clustering reveals untapped market opportunities"
            ]
        }
    
    def _generate_optimization_results(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Generate mock campaign optimization results"""
        improvement_percent = random.uniform(12, 35)
        metric = parameters.get("optimization_goal", "ROAS")
        
        return {
            "record_count": random.randint(10000, 50000),
            "business_summary": f"Campaign optimization analysis recommends targeting adjustments projected to improve {metric} by {improvement_percent:.1f}% while reducing cost per acquisition by {random.randint(8, 20)}%.",
            "detailed_results": {
                "optimization_goal": metric,
                "projected_improvement": f"{improvement_percent:.1f}%",
                "cost_reduction": f"{random.randint(8, 20)}%",
                "recommended_actions": ["Reallocate budget to high-performing segments", "Adjust daypart targeting", "Expand lookalike audiences"]
            },
            "insights": [
                "Weekend performance significantly outperforms weekday campaigns",
                f"Mobile users show {random.randint(25, 45)}% higher engagement rates",
                "Video creative performs best for awareness objectives"
            ]
        }
    
    def _generate_competitive_results(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Generate mock competitive intelligence results"""
        market_category = parameters.get("market_category", "Consumer Electronics")
        
        return {
            "record_count": random.randint(250000, 800000),
            "business_summary": f"Competitive intelligence analysis for {market_category} reveals market share opportunity with 23.4% share of voice gap vs. category leaders. Analysis identifies 3 key competitive advantages and 2 strategic threats requiring immediate attention.",
            "detailed_results": {
                "market_share_analysis": {
                    "your_share": f"{random.uniform(12, 18):.1f}%",
                    "category_leader": f"{random.uniform(28, 35):.1f}%",
                    "growth_rate": f"+{random.uniform(5, 15):.1f}% YoY"
                },
                "competitive_positioning": {
                    "strength_areas": ["Premium Product Quality", "Customer Service Excellence", "Innovation Pipeline"],
                    "improvement_areas": ["Digital Marketing Reach", "Price Competitiveness", "Market Expansion"]
                }
            },
            "insights": [
                "Digital marketing spend opportunity shows 40% efficiency improvement potential",
                "Premium positioning advantage in 18-34 demographic segment",
                "Geographic expansion opportunity in emerging markets"
            ]
        }
    
    def _generate_churn_results(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Generate mock churn prediction results"""
        prediction_horizon = parameters.get("prediction_horizon", 90)
        at_risk_customers = random.randint(45000, 120000)
        
        return {
            "record_count": at_risk_customers,
            "business_summary": f"Churn prediction model identifies {at_risk_customers:,} customers at high risk of churning within {prediction_horizon} days. Proactive retention campaigns targeting high-risk segments projected to reduce churn by 34% and preserve ${random.randint(2400, 6800):,}K in annual revenue.",
            "detailed_results": {
                "churn_risk_distribution": {
                    "high_risk": f"{random.randint(15000, 25000):,} customers",
                    "medium_risk": f"{random.randint(20000, 35000):,} customers", 
                    "low_risk": f"{random.randint(10000, 20000):,} customers"
                },
                "retention_strategies": {
                    "personalized_offers": "Projected 45% retention improvement",
                    "engagement_campaigns": "Projected 32% retention improvement",
                    "loyalty_programs": "Projected 28% retention improvement"
                }
            },
            "insights": [
                "Engagement frequency drops 67% in 30 days before churn",
                "Customer service interactions increase 2.3x before churn events",
                "Premium customers show different churn signals requiring specialized approach"
            ]
        }
    
    def _generate_ltv_results(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Generate mock lifetime value analysis results"""
        prediction_period = parameters.get("prediction_period", 24)
        customer_base = random.randint(180000, 450000)
        
        return {
            "record_count": customer_base,
            "business_summary": f"Predictive CLV analysis across {customer_base:,} customers reveals average lifetime value of ${random.randint(420, 780)} over {prediction_period} months. High-value segment (top 20%) contributes 67% of total revenue with ${random.randint(1200, 2400)} average CLV, identifying optimization opportunities worth ${random.randint(1800, 4200):,}K annually.",
            "detailed_results": {
                "clv_segments": {
                    "high_value": {"count": int(customer_base * 0.2), "avg_clv": f"${random.randint(1200, 2400)}", "revenue_contribution": "67%"},
                    "medium_value": {"count": int(customer_base * 0.3), "avg_clv": f"${random.randint(380, 680)}", "revenue_contribution": "23%"},
                    "low_value": {"count": int(customer_base * 0.5), "avg_clv": f"${random.randint(80, 180)}", "revenue_contribution": "10%"}
                },
                "optimization_opportunities": {
                    "acquisition_efficiency": f"${random.randint(125, 245)} max CPA for positive ROI",
                    "retention_investment": f"${random.randint(45, 85)} optimal retention spend per customer",
                    "upsell_potential": f"${random.randint(180, 340)} average upsell opportunity"
                }
            },
            "insights": [
                "High-value customers demonstrate 3.4x higher retention rates",
                "Cross-category purchase behavior strongly predicts CLV growth",
                "Geographic clustering in premium markets offers expansion opportunities"
            ]
        }

    def _generate_generic_results(self) -> Dict[str, Any]:
        """Generate generic mock results for unknown templates"""
        return {
            "record_count": random.randint(50000, 200000),
            "business_summary": "Analysis completed successfully with actionable insights for data-driven decision making.",
            "detailed_results": {
                "analysis_type": "Custom Analysis",
                "data_points_processed": random.randint(1000000, 5000000),
                "insights_generated": random.randint(8, 15)
            }
        }
    
    def list_mock_exports(self, status_filter: str = None) -> Dict[str, Any]:
        """Generate mock exports list for Phase C integration"""
        # Create realistic exports based on previously run queries
        exports = []
        
        # Some ready exports
        ready_exports = [
            {
                "id": f"export-{uuid.uuid4().hex[:8]}",
                "name": "Audience Overlap Analysis - Meta x Amazon",
                "query_id": "query-2024-001",
                "status": "READY",
                "created_at": "2024-06-20T14:30:00Z",
                "file_size": 2547832,  # ~2.5MB
                "download_url": "https://exports.habu.com/download/export-abc123",
                "format": "CSV",
                "record_count": 125000
            },
            {
                "id": f"export-{uuid.uuid4().hex[:8]}",
                "name": "Customer Lifetime Value Predictions",
                "query_id": "query-2024-002", 
                "status": "READY",
                "created_at": "2024-06-21T09:15:00Z",
                "file_size": 4182647,  # ~4.2MB
                "download_url": "https://exports.habu.com/download/export-def456",
                "format": "CSV", 
                "record_count": 287000
            },
            {
                "id": f"export-{uuid.uuid4().hex[:8]}",
                "name": "Sentiment Analysis - Global Events Q2",
                "query_id": "query-2024-003",
                "status": "READY",
                "created_at": "2024-06-22T16:45:00Z",
                "file_size": 1895432,  # ~1.9MB
                "download_url": "https://exports.habu.com/download/export-ghi789",
                "format": "CSV",
                "record_count": 89000
            }
        ]
        
        # Some processing exports
        processing_exports = [
            {
                "id": f"export-{uuid.uuid4().hex[:8]}",
                "name": "Lookalike Model Results - Premium Segment",
                "query_id": "query-2024-004",
                "status": "PROCESSING",
                "created_at": "2024-06-23T11:20:00Z",
                "estimated_completion": "2024-06-23T11:45:00Z",
                "progress_percent": 73
            },
            {
                "id": f"export-{uuid.uuid4().hex[:8]}",
                "name": "Cross-Platform Attribution Analysis",
                "query_id": "query-2024-005", 
                "status": "BUILDING",
                "created_at": "2024-06-23T13:05:00Z",
                "estimated_completion": "2024-06-23T13:30:00Z",
                "progress_percent": 34
            }
        ]
        
        # Combine all exports
        all_exports = ready_exports + processing_exports
        
        # Apply status filter if provided
        if status_filter:
            all_exports = [e for e in all_exports if e["status"] == status_filter.upper()]
        
        # Separate by status for response
        ready = [e for e in all_exports if e["status"] == "READY"]
        processing = [e for e in all_exports if e["status"] in ["PROCESSING", "BUILDING"]]
        failed = []  # No failed exports in mock for simplicity
        
        return {
            "status": "success",
            "total_exports": len(all_exports),
            "ready_exports": ready,
            "processing_exports": processing,
            "failed_exports": failed,
            "summary": f"{len(ready)} ready, {len(processing)} processing",
            "business_summary": f"You have {len(ready)} completed analyses ready for download ({sum(e.get('file_size', 0) for e in ready) / (1024*1024):.1f} MB total) and {len(processing)} analyses currently processing. Recent completions include audience overlap, lifetime value predictions, and sentiment analysis with comprehensive data coverage."
        }
    
    def download_mock_export(self, export_id: str) -> Dict[str, Any]:
        """Simulate export download for Phase C integration"""
        # Find the export (simulate lookup)
        mock_exports = self.list_mock_exports()
        
        all_exports = mock_exports["ready_exports"] + mock_exports["processing_exports"]
        export = next((e for e in all_exports if e["id"] == export_id), None)
        
        if not export:
            return {
                "status": "error",
                "error": f"Export {export_id} not found",
                "available_exports": [e["id"] for e in all_exports]
            }
        
        if export["status"] != "READY":
            return {
                "status": "error", 
                "error": f"Export {export_id} is not ready for download (status: {export['status']})",
                "current_status": export["status"],
                "estimated_completion": export.get("estimated_completion")
            }
        
        # Simulate successful download
        file_content_preview = self._generate_export_preview(export["name"])
        
        return {
            "status": "success",
            "export_id": export_id,
            "file_name": f"{export['name'].replace(' ', '_').lower()}.csv",
            "file_size": export["file_size"],
            "download_url": export["download_url"],
            "format": export["format"],
            "record_count": export["record_count"],
            "preview": file_content_preview,
            "summary": f"Export {export_id} downloaded successfully ({export['file_size']:,} bytes, {export['record_count']:,} records)"
        }
    
    def _generate_export_preview(self, export_name: str) -> Dict[str, Any]:
        """Generate a preview of export file contents"""
        if "Audience Overlap" in export_name:
            return {
                "columns": ["customer_id", "platform_1", "platform_2", "overlap_score", "ltv_tier", "engagement_level"],
                "sample_rows": [
                    ["cust_001", "Meta", "Amazon", "0.94", "High", "Premium"],
                    ["cust_002", "Meta", "Amazon", "0.87", "Medium", "Active"],
                    ["cust_003", "Meta", "Amazon", "0.91", "High", "Premium"]
                ],
                "total_columns": 12,
                "data_types": {"overlap_score": "float", "ltv_tier": "categorical", "engagement_level": "categorical"}
            }
        elif "Lifetime Value" in export_name:
            return {
                "columns": ["customer_id", "predicted_clv", "confidence_score", "value_tier", "churn_risk"],
                "sample_rows": [
                    ["cust_001", "1247.83", "0.92", "High", "Low"],
                    ["cust_002", "534.21", "0.85", "Medium", "Medium"],
                    ["cust_003", "892.45", "0.89", "High", "Low"]
                ],
                "total_columns": 8,
                "data_types": {"predicted_clv": "currency", "confidence_score": "float", "value_tier": "categorical"}
            }
        elif "Sentiment" in export_name:
            return {
                "columns": ["event_id", "sentiment_score", "emotion_category", "confidence", "topic_cluster"],
                "sample_rows": [
                    ["evt_001", "0.73", "Positive", "0.91", "Product_Quality"],
                    ["evt_002", "-0.24", "Negative", "0.87", "Customer_Service"],
                    ["evt_003", "0.45", "Neutral", "0.82", "Pricing"]
                ],
                "total_columns": 10,
                "data_types": {"sentiment_score": "float", "confidence": "float", "emotion_category": "categorical"}
            }
        else:
            return {
                "columns": ["id", "value", "category", "score"],
                "sample_rows": [
                    ["001", "example_value", "category_a", "0.85"],
                    ["002", "example_value_2", "category_b", "0.73"]
                ],
                "total_columns": 6,
                "data_types": {"score": "float", "category": "categorical"}
            }

# Global mock data instance
mock_data = HabuMockData()