"""
Magentic Quick Demo - Fast showcase of multi-agent collaboration
=================================================================
A streamlined demo showing the power of Magentic in under 5 minutes.
"""

import asyncio
import logging
from agent_framework import (
    ChatAgent,
    HostedCodeInterpreterTool,
    MagenticBuilder,
    WorkflowEvent,
    WorkflowOutputEvent,
)
from agent_framework.azure import AzureOpenAIChatClient
from azure.identity import DefaultAzureCredential

logging.basicConfig(level=logging.WARNING)


async def main():
    print("\n" + "⚡" * 50)
    print("MAGENTIC QUICK DEMO - Multi-Agent Collaboration in Action")
    print("⚡" * 50 + "\n")
    
    # Setup
    credential = DefaultAzureCredential()
    env_path = "c:\\E2EDemo\\.env"
    
    # Create specialized agents
    print("🤖 Creating AI Team Members...")
    print("   - Researcher (finds information)")
    print("   - Analyst (crunches numbers)")
    print("   - Manager (coordinates the team)\n")
    
    researcher = ChatAgent(
        name="Researcher",
        description="Research specialist",
        instructions="You find and summarize information clearly.",
        chat_client=AzureOpenAIChatClient(env_file_path=env_path, credential=credential),
    )
    
    analyst = ChatAgent(
        name="Analyst",
        description="Data analyst with code execution",
        instructions="You analyze data using Python code. Show calculations clearly.",
        chat_client=AzureOpenAIChatClient(env_file_path=env_path, credential=credential),
        tools=HostedCodeInterpreterTool(),
    )
    
    manager = ChatAgent(
        name="Manager",
        description="Team coordinator",
        instructions="You coordinate the team efficiently to accomplish tasks.",
        chat_client=AzureOpenAIChatClient(env_file_path=env_path, credential=credential),
    )
    
    # Build the workflow
    workflow = (
        MagenticBuilder()
        .participants(researcher=researcher, analyst=analyst)
        .with_standard_manager(agent=manager, max_round_count=15, max_stall_count=5)
        .build()
    )
    
    # The task - something that needs both research AND analysis
    print("📋 TASK: Analyze cloud computing market")
    print("-" * 80)
    task = """
    Create a brief market analysis:
    1. Name the top 3 cloud providers in 2025
    2. If AWS has 32% market share, Azure 23%, and Google Cloud 10%, 
       calculate what percentage the 'others' category represents
    3. Calculate: if the total market is $600B, how much revenue does each top provider have?
    
    Present as a clear summary with the math shown.
    """
    print(task)
    print("-" * 80 + "\n")
    
    print("⏳ Agents collaborating (this takes 1-2 minutes)...")
    print("   💡 Watch how the Manager delegates research and calculations!\n")
    
    # Run workflow
    try:
        async for event in workflow.run_stream(task):
            if isinstance(event, WorkflowOutputEvent):
                if event.data and len(event.data) > 0:
                    for message in event.data:
                        if hasattr(message, 'text') and message.text:
                            print("\n" + "🎯 " + "=" * 77)
                            print("FINAL RESULT:")
                            print("=" * 80)
                            print(message.text)
                            print("=" * 80 + "\n")
        
        print("✅ SUCCESS! The agents worked together to:")
        print("   ✓ Research cloud provider information")
        print("   ✓ Calculate market share percentages")
        print("   ✓ Compute revenue figures")
        print("   ✓ Present results clearly\n")
        
        print("🌟 This is the power of Magentic:")
        print("   Multiple specialized AI agents collaborating like a human team!\n")
        
    except Exception as e:
        print(f"❌ Error: {e}\n")


if __name__ == "__main__":
    print("\n🚀 Starting Quick Demo...\n")
    asyncio.run(main())
    print("✨ Demo complete!\n")
