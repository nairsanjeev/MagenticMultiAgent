"""
Magentic Multi-Agent Workflow Demo
===================================
This demo showcases the power of the Magentic pattern where multiple specialized
AI agents collaborate to solve complex tasks that would be difficult for a single agent.

Each demo highlights different collaboration patterns and real-world use cases.
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

logging.basicConfig(level=logging.WARNING)  # Reduce noise for demo
logger = logging.getLogger(__name__)

# Global counter for demo progress
demo_count = 0


def print_banner(title: str, subtitle: str = ""):
    """Print a nice banner for each demo"""
    print("\n" + "=" * 100)
    print(f"🎯 {title}")
    if subtitle:
        print(f"   {subtitle}")
    print("=" * 100 + "\n")


def print_result(content: str):
    """Print the final result with formatting"""
    print("\n" + "🎉 " + "=" * 95)
    print("RESULT:")
    print("=" * 100)
    print(content)
    print("=" * 100 + "\n")


async def run_workflow(workflow, task: str, description: str):
    """Execute a workflow and handle events"""
    global demo_count
    demo_count += 1
    
    print_banner(f"Demo {demo_count}: {description}", task)
    print("⏳ Agents are collaborating... (this may take 1-2 minutes)\n")
    
    try:
        async for event in workflow.run_stream(task):
            # Only show important events to keep demo clean
            if isinstance(event, WorkflowOutputEvent):
                if event.data and len(event.data) > 0:
                    for message in event.data:
                        if hasattr(message, 'text') and message.text:
                            print_result(message.text)
        
        print("✅ Demo completed successfully!\n")
        return True
    except Exception as e:
        print(f"❌ Demo failed: {e}\n")
        logger.exception("Workflow exception")
        return False


async def setup_agents():
    """Create and return the specialized agents"""
    credential = DefaultAzureCredential()
    env_path = "c:\\E2EDemo\\.env"
    
    # Researcher Agent - Good at finding information
    researcher = ChatAgent(
        name="ResearcherAgent",
        description="Information gathering and research specialist",
        instructions="You are a researcher who finds and synthesizes information. Be thorough and cite sources when possible.",
        chat_client=AzureOpenAIChatClient(env_file_path=env_path, credential=credential),
    )
    
    # Analyst Agent - Good at data analysis and computation
    analyst = ChatAgent(
        name="AnalystAgent",
        description="Data analysis and computational specialist",
        instructions="You analyze data using code and mathematics. Provide clear calculations and visualizations through code.",
        chat_client=AzureOpenAIChatClient(env_file_path=env_path, credential=credential),
        tools=HostedCodeInterpreterTool(),
    )
    
    # Writer Agent - Good at creating polished content
    writer = ChatAgent(
        name="WriterAgent",
        description="Content creation and writing specialist",
        instructions="You create well-structured, clear, and engaging written content. Format professionally.",
        chat_client=AzureOpenAIChatClient(env_file_path=env_path, credential=credential),
    )
    
    # Manager Agent - Coordinates the team
    manager = ChatAgent(
        name="ManagerAgent",
        description="Team coordinator and workflow manager",
        instructions="You coordinate agents to accomplish tasks efficiently. Break down complex tasks and delegate appropriately.",
        chat_client=AzureOpenAIChatClient(env_file_path=env_path, credential=credential),
    )
    
    return researcher, analyst, writer, manager


async def demo_1_business_analysis(researcher, analyst, manager):
    """Demo 1: Business Analysis - Research + Analysis collaboration"""
    
    workflow = (
        MagenticBuilder()
        .participants(researcher=researcher, analyst=analyst)
        .with_standard_manager(agent=manager, max_round_count=15, max_stall_count=5)
        .build()
    )
    
    task = """
    Analyze the current state of the AI chip market. Include:
    1. Top 3 companies by market share
    2. Calculate the compound annual growth rate (CAGR) if the market was $20B in 2020 and projected to be $120B by 2025
    3. Identify the fastest growing segment
    Provide a summary with calculations shown.
    """
    
    await run_workflow(workflow, task, "Business Market Analysis")


async def demo_2_technical_report(researcher, analyst, writer, manager):
    """Demo 2: Technical Report - Full team collaboration"""
    
    workflow = (
        MagenticBuilder()
        .participants(researcher=researcher, analyst=analyst, writer=writer)
        .with_standard_manager(agent=manager, max_round_count=20, max_stall_count=5)
        .build()
    )
    
    task = """
    Create a brief technical report on quantum computing readiness:
    1. Research current quantum computing capabilities (2025)
    2. Calculate how many qubits would be needed for a practical application (assume 1000 qubits needed)
    3. Write a 2-paragraph executive summary with findings
    Keep it concise but informative.
    """
    
    await run_workflow(workflow, task, "Technical Report Generation")


async def demo_3_data_analysis(analyst, manager):
    """Demo 3: Pure Data Analysis - Single specialized agent"""
    
    workflow = (
        MagenticBuilder()
        .participants(analyst=analyst)
        .with_standard_manager(agent=manager, max_round_count=10, max_stall_count=3)
        .build()
    )
    
    task = """
    Using code, calculate and visualize:
    1. The Fibonacci sequence up to the 15th number
    2. Calculate the ratio between consecutive Fibonacci numbers (approaching golden ratio)
    3. Show how this ratio converges to approximately 1.618
    Present results in a clear format with the calculations.
    """
    
    await run_workflow(workflow, task, "Mathematical Analysis")


async def demo_4_quick_research(researcher, manager):
    """Demo 4: Rapid Research - Fast information gathering"""
    
    workflow = (
        MagenticBuilder()
        .participants(researcher=researcher)
        .with_standard_manager(agent=manager, max_round_count=8, max_stall_count=3)
        .build()
    )
    
    task = """
    Quick research brief:
    What are the top 3 programming languages in 2025 and their primary use cases?
    Keep it brief - 2-3 sentences per language.
    """
    
    await run_workflow(workflow, task, "Quick Research Brief")


async def demo_5_cost_calculator(analyst, manager):
    """Demo 5: Cost Analysis - Practical business calculation"""
    
    workflow = (
        MagenticBuilder()
        .participants(analyst=analyst)
        .with_standard_manager(agent=manager, max_round_count=10, max_stall_count=3)
        .build()
    )
    
    task = """
    Calculate the ROI for this AI project:
    - Initial investment: $500,000
    - Annual cost savings: $150,000
    - Project lifespan: 5 years
    
    Calculate:
    1. Payback period
    2. Total ROI percentage
    3. Net present value (assume 8% discount rate)
    
    Show all calculations clearly.
    """
    
    await run_workflow(workflow, task, "ROI Calculator")


async def main():
    """Run all demos"""
    print("\n" + "🌟" * 50)
    print("MAGENTIC MULTI-AGENT WORKFLOW DEMONSTRATION")
    print("Showcasing AI agent collaboration for complex tasks")
    print("🌟" * 50 + "\n")
    
    print("⚙️  Setting up specialized agents...\n")
    researcher, analyst, writer, manager = await setup_agents()
    print("✅ Agents ready!\n")
    
    # Run demos
    demos = [
        ("Quick Research (Fastest)", demo_4_quick_research(researcher, manager)),
        ("Cost Calculator", demo_5_cost_calculator(analyst, manager)),
        ("Math Analysis", demo_3_data_analysis(analyst, manager)),
        ("Business Analysis", demo_1_business_analysis(researcher, analyst, manager)),
        ("Technical Report (Most Complex)", demo_2_technical_report(researcher, analyst, writer, manager)),
    ]
    
    print("\n📋 Running 5 demos to showcase different collaboration patterns...\n")
    print("Note: Each demo demonstrates how agents work together based on their specializations\n")
    
    results = []
    for demo_name, demo_coro in demos:
        print(f"▶️  Starting: {demo_name}")
        success = await demo_coro
        results.append((demo_name, success))
        
        if demo_count < len(demos):
            print("\n⏸️  Press Enter to continue to next demo...")
            input()
    
    # Summary
    print("\n" + "🎊" * 50)
    print("DEMO SUMMARY")
    print("🎊" * 50 + "\n")
    
    for demo_name, success in results:
        status = "✅ SUCCESS" if success else "❌ FAILED"
        print(f"{status} - {demo_name}")
    
    successful = sum(1 for _, success in results if success)
    print(f"\n📊 Results: {successful}/{len(results)} demos completed successfully")
    
    print("\n" + "=" * 100)
    print("🎯 KEY TAKEAWAYS:")
    print("=" * 100)
    print("""
1. 🤝 COLLABORATION: Multiple specialized agents working together
2. 🎯 SPECIALIZATION: Each agent has specific skills (research, analysis, writing)
3. 🧠 INTELLIGENCE: Manager agent orchestrates and delegates tasks
4. 🔄 FLEXIBILITY: Workflows adapt based on task complexity
5. 💪 POWER: Solves complex tasks that single agents struggle with

The Magentic pattern enables AI systems to work like human teams - 
with specialized roles collaborating towards a common goal!
    """)
    print("=" * 100 + "\n")


if __name__ == "__main__":
    print("\n🚀 Starting Magentic Demo...")
    print("This will showcase 5 different use cases of multi-agent collaboration\n")
    
    try:
        asyncio.run(main())
        print("\n✨ Demo completed! Thank you for watching!\n")
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user. Goodbye!\n")
    except Exception as e:
        print(f"\n\n❌ Demo error: {e}\n")
        logger.exception("Demo failed")
