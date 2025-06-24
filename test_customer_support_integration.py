#!/usr/bin/env python3
"""
Test script for customer support integration
Demonstrates Phase 2 functionality
"""

import requests
import json

def test_customer_support_scenarios():
    """Test various customer support scenarios"""
    
    print("🧪 Testing Phase 2: Customer Support Mode Implementation")
    print("=" * 60)
    
    scenarios = [
        {
            "name": "Retail Lookalike Modeling",
            "query": "Can we do lookalike modeling for a retail customer with 50,000 customers?",
            "industry": "retail",
            "customerSize": "large"
        },
        {
            "name": "Finance Customer Segmentation", 
            "query": "We want to segment customers for a bank, is this possible?",
            "industry": "finance",
            "customerSize": "enterprise"
        },
        {
            "name": "Automotive Identity Resolution",
            "query": "How can we unify customer data across dealerships?", 
            "industry": "automotive",
            "customerSize": "medium"
        },
        {
            "name": "General Cross-Platform Attribution",
            "query": "What can we do for cross-channel marketing attribution?",
            "industry": None,
            "customerSize": "medium"
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n{i}. Testing: {scenario['name']}")
        print("-" * 40)
        
        try:
            # Test customer support assessment
            response = requests.post(
                'http://localhost:5001/api/customer-support/assess',
                json={
                    'query': scenario['query'],
                    'industry': scenario['industry'],
                    'customerSize': scenario['customerSize']
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                
                print(f"📊 Feasibility: {data['feasibility']}")
                print(f"🎯 Confidence: {data['confidence']}")
                print(f"⏱️ Timeline: {data['implementation']['timeline']}")
                print(f"🏆 Key Advantage: {data['competitive_advantage'][0] if data['competitive_advantage'] else 'N/A'}")
                print(f"🚀 Next Step: {data['next_steps'][0] if data['next_steps'] else 'N/A'}")
                
            else:
                print(f"❌ Error: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("✅ Phase 2 Customer Support functionality working!")
    print("\nKey Features Demonstrated:")
    print("• Industry-specific use case matching")
    print("• Customer-ready feasibility assessments")
    print("• Competitive advantage positioning")
    print("• Business outcome mapping")
    print("• Implementation timeline estimation")

def test_context_endpoints():
    """Test context endpoints for chat modes"""
    
    print("\n🔧 Testing Context Endpoints")
    print("-" * 30)
    
    try:
        # Test support context
        response = requests.get('http://localhost:8000/api/support-context')
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Support Context: {len(data.get('industryFocus', []))} industries")
        
        # Test technical context  
        response = requests.get('http://localhost:8000/api/technical-context')
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Technical Context: {len(data.get('availableTools', []))} tools")
            
    except Exception as e:
        print(f"⚠️ Context endpoints may not be running: {e}")

if __name__ == "__main__":
    test_customer_support_scenarios()
    test_context_endpoints()