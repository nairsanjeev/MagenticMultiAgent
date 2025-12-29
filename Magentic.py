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

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main() -> None:
    # Use Azure credential for authentication
    credential = DefaultAzureCredential()
    
    # Define specialized agents
    researcher_agent = ChatAgent(
        name="ResearcherAgent",
        description="Specialist in research and information gathering",
        instructions=(
            "You are a Researcher. You find information without additional "
            "computation or quantitative analysis."
        ),
        chat_client=AzureOpenAIChatClient(
            env_file_path="c:\\E2EDemo\\.env",
            credential=credential
        ),
    )

    coder_agent = ChatAgent(
        name="CoderAgent",
        description="A helpful assistant that writes and executes code to process and analyze data.",
        instructions="You solve questions using code. Please provide detailed analysis and computation process.",
        chat_client=AzureOpenAIChatClient(
            env_file_path="c:\\E2EDemo\\.env",
            credential=credential
        ),
        tools=HostedCodeInterpreterTool(),
    )

    # Event handler for workflow events
    def handle_event(event: WorkflowEvent) -> None:
        """Handle workflow events and print relevant information."""
        print(f"\n[EVENT] {event.__class__.__name__}")
        
        # Print event details
        if hasattr(event, 'source'):
            print(f"  Source: {event.source}")
        
        # Handle output events - this is where the final report is!
        if isinstance(event, WorkflowOutputEvent):
            print("\n" + "=" * 80)
            print("🎯 FINAL REPORT:")
            print("=" * 80)
            # Extract and print the actual message text
            if event.data and len(event.data) > 0:
                for message in event.data:
                    if hasattr(message, 'text') and message.text:
                        print(message.text)
                    elif hasattr(message, 'content'):
                        print(message.content)
            print("=" * 80)

    # Build the workflow
    print("\nBuilding Magentic Workflow...")

    # Create manager agent
    manager_agent = ChatAgent(
        name="ManagerAgent",
        description="Workflow coordinator for task planning and agent coordination",
        instructions="You are a coordinator. Plan tasks and select appropriate agents to accomplish the user's request.",
        chat_client=AzureOpenAIChatClient(
            env_file_path="c:\\E2EDemo\\.env",
            credential=credential
        ),
    )

    workflow = (
        MagenticBuilder()
        .participants(researcher=researcher_agent, coder=coder_agent)
        .with_standard_manager(
            agent=manager_agent,
            max_round_count=20,
            max_stall_count=5,
            max_reset_count=3,
        )
        .build()
    )

    # Define the task
    task = (
        "I am preparing a report on the energy efficiency of different machine learning model architectures. "
        "Compare the estimated training and inference energy consumption of ResNet-50, BERT-base, and GPT-2 "
        "on standard datasets (e.g., ImageNet for ResNet, GLUE for BERT, WebText for GPT-2). "
        "Then, estimate the CO2 emissions associated with each, assuming training on an Azure Standard_NC6s_v3 "
        "VM for 24 hours. Provide tables for clarity, and recommend the most energy-efficient model "
        "per task type (image classification, text classification, and text generation)."
    )

    print(f"\nTask: {task}")
    print("\nStarting workflow execution...")

    # Run the workflow
    try:
        print("\n" + "=" * 50)
        print("WORKFLOW EXECUTION")
        print("=" * 50)
        
        async for event in workflow.run_stream(task):
            handle_event(event)

        print("\n" + "=" * 50)
        print("WORKFLOW COMPLETED SUCCESSFULLY")
        print("=" * 50)

    except Exception as e:
        print(f"\n❌ Workflow execution failed: {e}")
        logger.exception("Workflow exception", exc_info=e)

if __name__ == "__main__":
    asyncio.run(main())