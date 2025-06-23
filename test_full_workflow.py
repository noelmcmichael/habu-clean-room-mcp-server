#!/usr/bin/env python3
"""
Test the full workflow: partners -> templates -> submit query -> check status -> get results
"""
import asyncio
import os
from agents.enhanced_habu_chat_agent import enhanced_habu_agent

async def test_full_workflow():
    """Test the complete workflow using the enhanced chat agent"""
    print("🔄 Testing Full Habu Clean Room Workflow")
    print("=" * 50)
    
    # Enable mock mode
    os.environ["HABU_USE_MOCK_DATA"] = "true"
    
    workflow_steps = [
        "Show me my partners",
        "What query templates can I use?",
        "Can you run an audience overlap analysis between Meta and Amazon?",
        "Check the status of my last query",
        "Get the results of my analysis"
    ]
    
    for i, step in enumerate(workflow_steps, 1):
        print(f"\n🔸 Step {i}: {step}")
        print("-" * 40)
        
        try:
            response = await enhanced_habu_agent.process_request(step)
            print(f"💬 Response: {response}")
            
            # Add a small delay to simulate user interaction
            await asyncio.sleep(1)
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n✅ Workflow test completed!")

if __name__ == "__main__":
    asyncio.run(test_full_workflow())