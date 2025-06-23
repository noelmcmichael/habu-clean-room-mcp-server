#!/usr/bin/env python3
"""
Test the enhanced mock data system with realistic business scenarios
"""
import asyncio
import os
import json
from agents.enhanced_habu_chat_agent import enhanced_habu_agent

async def test_enhanced_mock_data():
    """Test all the enhanced mock data functionality"""
    print("🚀 Testing Enhanced Mock Data System")
    print("=" * 60)
    
    # Enable mock mode
    os.environ["HABU_USE_MOCK_DATA"] = "true"
    
    # Test scenarios showcasing new capabilities
    test_scenarios = [
        {
            "name": "Advanced Partner Discovery",
            "input": "Show me detailed information about my data partners"
        },
        {
            "name": "Sophisticated Template Exploration", 
            "input": "What are the most advanced analytics I can run?"
        },
        {
            "name": "Complex Overlap Analysis",
            "input": "Run a cross-platform audience overlap analysis between Meta Business and Amazon DSP"
        },
        {
            "name": "AI Lookalike Modeling",
            "input": "Create an AI-powered lookalike model for high-value customers"
        },
        {
            "name": "Churn Prediction Analysis",
            "input": "Predict which customers are at risk of churning"
        },
        {
            "name": "Lifetime Value Analysis",
            "input": "Analyze customer lifetime value and segmentation"
        },
        {
            "name": "Query Status with Progress",
            "input": "Check the status of my latest analysis"
        },
        {
            "name": "Detailed Results Retrieval",
            "input": "Show me the detailed results of my completed analysis"
        }
    ]
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n🧪 Test {i}: {scenario['name']}")
        print(f"💭 User: {scenario['input']}")
        print("-" * 50)
        
        try:
            response = await enhanced_habu_agent.process_request(scenario['input'])
            print(f"🤖 Assistant: {response}")
            
            # Add delay for demo effect and query progression
            await asyncio.sleep(2)
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("✅ Enhanced Mock Data Testing Complete!")
    print("\n📊 New Features Tested:")
    print("• Detailed partner profiles with real metrics")
    print("• 8 sophisticated query templates")
    print("• Advanced business insights and recommendations")
    print("• Multi-tier audience analysis")
    print("• Geographic and demographic breakdowns")
    print("• Strategic action plans and projections")
    print("• Performance forecasting")
    
    print("\n🎯 Ready for impressive demonstrations!")

if __name__ == "__main__":
    asyncio.run(test_enhanced_mock_data())