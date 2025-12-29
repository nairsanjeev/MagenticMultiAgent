"""
Magentic Multi-Agent Backend with CopilotKit Integration
=========================================================
This backend exposes the Magentic workflow as a CopilotKit-compatible endpoint
that can be used with a React frontend.
"""

import asyncio
import logging
from typing import AsyncGenerator
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent_framework import (
    ChatAgent,
    HostedCodeInterpreterTool,
    MagenticBuilder,
    WorkflowEvent,
    WorkflowOutputEvent,
)
from agent_framework.azure import AzureOpenAIChatClient
from azure.identity import DefaultAzureCredential
from contextlib import asynccontextmanager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global agents (initialized once)
researcher_agent = None
coder_agent = None
manager_agent = None
workflow = None


def create_workflow_with_models(researcher_model="gpt-4o", coder_model="gpt-4o", manager_model="gpt-4o", reviewer_model="gpt-4o"):
    """Create a workflow with specified models for each agent"""
    credential = DefaultAzureCredential()
    env_path = "c:\\E2EDemo\\.env"
    
    # Create specialized agents with model selection
    researcher = ChatAgent(
        name="ResearcherAgent",
        description="Specialist in research and information gathering",
        instructions=(
            "You are a Researcher. You find information without additional "
            "computation or quantitative analysis."
        ),
        chat_client=AzureOpenAIChatClient(
            env_file_path=env_path,
            credential=credential,
            model=researcher_model
        ),
    )
    
    coder = ChatAgent(
        name="CoderAgent",
        description="A helpful assistant that writes and executes code to process and analyze data.",
        instructions="You solve questions using code. Please provide detailed analysis and computation process.",
        chat_client=AzureOpenAIChatClient(
            env_file_path=env_path,
            credential=credential,
            model=coder_model
        ),
        tools=HostedCodeInterpreterTool(),
    )
    
    reviewer = ChatAgent(
        name="ReviewerAgent",
        description="Critical reviewer who validates analysis quality, identifies gaps, and ensures accuracy",
        instructions=(
            "You are a Senior Analyst who critically reviews analysis outputs. "
            "Your role: Validate assumptions, check calculation accuracy, identify missing considerations, "
            "challenge conclusions, spot logical flaws, and ensure recommendations are evidence-based. "
            "Be constructive but rigorous. Flag data gaps, questionable assumptions, and weak reasoning."
        ),
        chat_client=AzureOpenAIChatClient(
            env_file_path=env_path,
            credential=credential,
            model=reviewer_model
        ),
    )
    
    # Create chat client for the manager
    manager_chat_client = AzureOpenAIChatClient(
        env_file_path=env_path,
        credential=credential,
        model=manager_model
    )
    
    # Build the workflow with reviewer as participant
    return (
        MagenticBuilder()
        .participants(researcher=researcher, coder=coder, reviewer=reviewer)
        .with_standard_manager(
            chat_client=manager_chat_client,
            max_round_count=20,
            max_stall_count=5,
            max_reset_count=3,
        )
        .build()
    )


async def initialize_agents():
    """Initialize the agents once at startup with default models"""
    global researcher_agent, coder_agent, manager_agent, workflow
    
    if workflow is not None:
        return  # Already initialized
    
    logger.info("Initializing agents with default models...")
    
    workflow = create_workflow_with_models()
    
    logger.info("Agents initialized successfully")


class TaskRequest(BaseModel):
    """Request model for task execution"""
    task: str
    max_rounds: int = 20
    researcher_model: str = "gpt-4o"
    coder_model: str = "gpt-4o"
    manager_model: str = "gpt-4o"
    reviewer_model: str = "gpt-4o"


class TaskResponse(BaseModel):
    """Response model for task execution"""
    status: str
    result: str = None
    error: str = None
    activity_log: list = []


# Use lifespan context manager instead of deprecated on_event
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown"""
    # Startup
    await initialize_agents()
    yield
    # Shutdown (if needed)
    pass

# Update the app with lifespan
app = FastAPI(title="Magentic Multi-Agent API", lifespan=lifespan)

# Re-add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "running",
        "service": "Magentic Multi-Agent Backend",
        "agents": ["ResearcherAgent", "CoderAgent", "ManagerAgent"]
    }


@app.get("/api/health")
async def health():
    """Health check for the API"""
    return {"status": "healthy", "agents_initialized": workflow is not None}


@app.get("/api/models")
async def get_available_models():
    """Get list of available AI models"""
    return {
        "models": [
            {"id": "gpt-4o", "name": "GPT-4o (Recommended)", "description": "Most capable, best for complex analysis"},
            {"id": "gpt-4o-mini", "name": "GPT-4o Mini", "description": "Fast and cost-effective"},
            {"id": "gpt-4", "name": "GPT-4 Turbo", "description": "Previous generation, reliable"},
            {"id": "gpt-35-turbo", "name": "GPT-3.5 Turbo", "description": "Fast, good for simple tasks"}
        ]
    }


def extract_agent_activities_from_result(text, activity_log, researcher_outputs, coder_outputs, researcher_topics, coder_operations):
    """Extract what agents did by analyzing the final result text"""
    if not text:
        return
    
    import re
    
    # Look for calculations (Coder's work)
    calculations = re.findall(r'\$[0-9,]+|×|÷|[0-9]+%|=\s*\$?[0-9,]+|ROI|CAGR|calculation|formula', text, re.IGNORECASE)
    if calculations:
        # Found calculation-related content
        activity_log.append({
            "type": "coder",
            "message": f"🧮 Coder performed calculations:\n   Found {len(set(calculations))} mathematical operations in analysis",
            "icon": "🧮"
        })
        coder_outputs.append("calculations_found")
        coder_operations.append("Mathematical Analysis")
    
    # Look for research data (Researcher's work)
    research_indicators = re.findall(r'average|market|industry|study|research|data|statistics|according to|typical|standard', text, re.IGNORECASE)
    if research_indicators:
        activity_log.append({
            "type": "researcher",
            "message": f"📚 Researcher gathered market intelligence:\n   Found {len(set(research_indicators))} research data points",
            "icon": "📚"
        })
        researcher_outputs.append("research_found")
        researcher_topics.add("market_research")


@app.post("/api/execute", response_model=TaskResponse)
async def execute_task(request: TaskRequest):
    """
    Execute a task using the Magentic workflow with model selection
    """
    logger.info(f"Executing task with models - Researcher: {request.researcher_model}, Coder: {request.coder_model}, Reviewer: {request.reviewer_model}, Manager: {request.manager_model}")
    
    # Create workflow with selected models
    task_workflow = create_workflow_with_models(
        researcher_model=request.researcher_model,
        coder_model=request.coder_model,
        manager_model=request.manager_model,
        reviewer_model=request.reviewer_model
    )
    
    logger.info(f"Task: {request.task[:100]}...")
    
    try:
        result_text = ""
        activity_log = []
        event_count = 0
        
        # Track which agents have been active and their detailed outputs
        agent_activities = set()
        researcher_outputs = []
        coder_outputs = []
        researcher_topics = set()
        coder_operations = []
        
        async for event in task_workflow.run_stream(request.task):
            event_count += 1
            event_type = event.__class__.__name__
            
            # Get event source/agent info
            event_str = str(event)
            agent_name = None
            
            if hasattr(event, 'source'):
                agent_name = str(event.source)
            elif hasattr(event, 'agent_name'):
                agent_name = event.agent_name
            
            # Debug logging - inspect ALL event attributes
            if event_count <= 20:  # Only for first 20 events to avoid spam
                logger.info(f"Event {event_count}: {event_type}")
                logger.info(f"  Attributes: {dir(event)}")
                if hasattr(event, '__dict__'):
                    logger.info(f"  Dict: {event.__dict__}")
            
            # Extract full message content from events - check multiple possible attributes
            message_content = None
            full_message = None
            
            # Check various event data structures
            if hasattr(event, 'data') and event.data:
                messages = event.data if isinstance(event.data, list) else [event.data]
                for msg in messages:
                    if hasattr(msg, 'text') and msg.text:
                        full_message = msg.text
                        message_content = msg.text[:300]
                    elif hasattr(msg, 'content') and msg.content:
                        full_message = msg.content
                        message_content = msg.content[:300]
            
            # Also check if event itself has content
            if not message_content and hasattr(event, 'content'):
                full_message = str(event.content)
                message_content = str(event.content)[:300]
            
            # Check for messages in event directly
            if not message_content and hasattr(event, 'message'):
                full_message = str(event.message)
                message_content = str(event.message)[:300]
            
            # Log ANY message content we find for debugging
            if message_content and message_content.strip():
                logger.info(f"📝 Agent message detected: {message_content[:150]}")
            
            # Track Researcher Agent activities with detailed analysis
            if "researcher" in event_str.lower() or (agent_name and "researcher" in agent_name.lower()):
                if "researcher" not in agent_activities:
                    activity_log.append({
                        "type": "researcher",
                        "message": "🔍 Researcher Agent activated - Starting comprehensive information gathering",
                        "icon": "🔍"
                    })
                    agent_activities.add("researcher")
                
                # ALWAYS log researcher activity, even without message content
                if not message_content or message_content in researcher_outputs:
                    # Log the event type at minimum
                    if event_type not in ["WorkflowEvent", "WorkflowOutputEvent"]:
                        activity_log.append({
                            "type": "researcher",
                            "message": f"🔍 Researcher processing: {event_type}",
                            "icon": "🔍"
                        })
                
                # Track detailed researcher outputs
                if message_content and message_content not in researcher_outputs:
                    researcher_outputs.append(message_content)
                    
                    # Analyze what the researcher found
                    analysis_type = "Information"
                    if any(word in message_content.lower() for word in ['market', 'industry', 'sector', 'company', 'companies']):
                        analysis_type = "Market Research"
                        researcher_topics.add("market_analysis")
                    elif any(word in message_content.lower() for word in ['data', 'statistics', 'number', 'figure', 'percent']):
                        analysis_type = "Data Analysis"
                        researcher_topics.add("data_research")
                    elif any(word in message_content.lower() for word in ['trend', 'growth', 'increase', 'decrease', 'change']):
                        analysis_type = "Trend Analysis"
                        researcher_topics.add("trend_research")
                    elif any(word in message_content.lower() for word in ['compare', 'comparison', 'versus', 'vs', 'difference']):
                        analysis_type = "Comparative Analysis"
                        researcher_topics.add("comparative_research")
                    
                    # Extract key findings
                    key_points = []
                    if full_message:
                        # Look for bullet points or numbered lists
                        lines = full_message.split('\n')
                        for line in lines[:5]:  # First 5 lines
                            line = line.strip()
                            if line and (line.startswith('-') or line.startswith('•') or line.startswith('*') or line[0].isdigit()):
                                key_points.append(line.lstrip('-•* 0123456789.)'))
                    
                    # Create detailed log entry
                    detail_msg = f"📚 Researcher completed {analysis_type}:\n"
                    if key_points:
                        detail_msg += f"   • {key_points[0][:100]}"
                        if len(key_points) > 1:
                            detail_msg += f"\n   • {key_points[1][:100]}"
                    else:
                        detail_msg += f"   {message_content[:200]}"
                    
                    activity_log.append({
                        "type": "researcher",
                        "message": detail_msg,
                        "icon": "📚"
                    })
            
            # Track Coder Agent activities with detailed code analysis
            if "coder" in event_str.lower() or (agent_name and "coder" in agent_name.lower()):
                if "coder" not in agent_activities:
                    activity_log.append({
                        "type": "coder",
                        "message": "💻 Coder Agent activated - Initializing computational analysis tools",
                        "icon": "💻"
                    })
                    agent_activities.add("coder")
                
                # ALWAYS log coder activity, even without message content
                if not message_content or message_content in coder_outputs:
                    # Log the event type at minimum
                    if event_type not in ["WorkflowEvent", "WorkflowOutputEvent"]:
                        activity_log.append({
                            "type": "coder",
                            "message": f"💻 Coder processing: {event_type}",
                            "icon": "💻"
                        })
                
                # Track detailed coder outputs
                if message_content and message_content not in coder_outputs:
                    coder_outputs.append(message_content)
                    
                    # Analyze what type of coding/calculation was performed
                    operation_type = "Processing"
                    detail_info = ""
                    
                    # Check for mathematical operations
                    if any(op in message_content for op in ['=', 'result', 'answer', 'equals']):
                        operation_type = "Calculation"
                        
                        # Try to extract the calculation
                        if '=' in message_content:
                            parts = message_content.split('=')
                            if len(parts) >= 2:
                                detail_info = f"Formula: {parts[0].strip()[:80]} = {parts[1].strip()[:80]}"
                        
                        # Look for specific math operations
                        if any(term in message_content.lower() for term in ['cagr', 'compound', 'growth rate']):
                            operation_type = "CAGR Calculation"
                        elif any(term in message_content.lower() for term in ['roi', 'return on investment', 'payback']):
                            operation_type = "ROI Analysis"
                        elif any(term in message_content.lower() for term in ['sum', 'total', 'add']):
                            operation_type = "Summation"
                        elif any(term in message_content.lower() for term in ['average', 'mean', 'median']):
                            operation_type = "Statistical Analysis"
                        elif any(term in message_content.lower() for term in ['percent', '%', 'percentage']):
                            operation_type = "Percentage Calculation"
                    
                    elif 'python' in message_content.lower() or 'code' in message_content.lower():
                        operation_type = "Code Execution"
                        detail_info = "Running Python code interpreter"
                    
                    elif any(term in message_content.lower() for term in ['analyze', 'analysis', 'examine']):
                        operation_type = "Data Analysis"
                    
                    # Extract code snippets if present
                    code_snippet = None
                    if '```' in message_content:
                        code_parts = message_content.split('```')
                        if len(code_parts) > 1:
                            code_snippet = code_parts[1].strip()[:150]
                    
                    # Create detailed log entry
                    detail_msg = f"🧮 Coder performing {operation_type}:"
                    if detail_info:
                        detail_msg += f"\n   {detail_info}"
                    elif code_snippet:
                        detail_msg += f"\n   Code: {code_snippet}..."
                    else:
                        # Show the actual calculation or result
                        detail_msg += f"\n   {message_content[:200]}"
                    
                    coder_operations.append(operation_type)
                    
                    activity_log.append({
                        "type": "coder",
                        "message": detail_msg,
                        "icon": "🧮"
                    })
            
            # Track Reviewer Agent activities
            if "reviewer" in event_str.lower() or (agent_name and "reviewer" in agent_name.lower()):
                if "reviewer" not in agent_activities:
                    activity_log.append({
                        "type": "reviewer",
                        "message": "🔍 Reviewer Agent activated - Critically evaluating analysis quality",
                        "icon": "🔍"
                    })
                    agent_activities.add("reviewer")
                
                # Track reviewer feedback/critique
                if message_content:
                    critique_indicators = ['however', 'concern', 'gap', 'missing', 'assumption', 'validate', 'suggest', 'recommend', 'issue', 'question']
                    if any(indicator in message_content.lower() for indicator in critique_indicators):
                        activity_log.append({
                            "type": "reviewer",
                            "message": f"🔎 Reviewer providing critical feedback:\n   Identified quality checks and improvement areas",
                            "icon": "🔎"
                        })
            
            # Track Manager/Orchestrator
            if "manager" in event_str.lower() or "orchestrator" in event_str.lower() or (agent_name and "manager" in agent_name.lower()):
                if "manager" not in agent_activities:
                    activity_log.append({
                        "type": "manager",
                        "message": "🎯 Manager Agent coordinating - Analyzing task and planning workflow",
                        "icon": "🎯"
                    })
                    agent_activities.add("manager")
            
            # Track tool/code execution
            if "tool" in event_str.lower() or "code" in event_str.lower():
                activity_log.append({
                    "type": "coder",
                    "message": "🔧 Coder executing code interpreter for calculations",
                    "icon": "🔧"
                })
            
            # Track workflow progress milestones
            if event_count in [10, 20, 30, 40]:
                activity_log.append({
                    "type": "system",
                    "message": f"⚡ Workflow milestone: {event_count} events processed, agents collaborating",
                    "icon": "⚡"
                })
            
            if isinstance(event, WorkflowOutputEvent):
                if event.data:
                    # Handle if data is a list or a single object
                    messages = event.data if isinstance(event.data, list) else [event.data]
                    for message in messages:
                        if hasattr(message, 'text') and message.text:
                            result_text = message.text
                            
                            # Parse the result to extract what each agent did
                            extract_agent_activities_from_result(result_text, activity_log, researcher_outputs, coder_outputs, researcher_topics, coder_operations)
                            
                            activity_log.append({
                                "type": "success",
                                "message": f"📄 Final report compiled! Manager synthesized inputs from {len(agent_activities)} agents",
                                "icon": "✅"
                            })
                        elif hasattr(message, 'content') and message.content:
                            result_text = message.content
                            
                            # Parse the result to extract what each agent did
                            extract_agent_activities_from_result(result_text, activity_log, researcher_outputs, coder_outputs, researcher_topics, coder_operations)
                            
                            activity_log.append({
                                "type": "success",
                                "message": "✨ Results generated successfully with multi-agent collaboration",
                                "icon": "✅"
                            })
        
        # Parse the final result to extract what agents did
        extract_agent_activities_from_result(result_text, activity_log, researcher_outputs, coder_outputs, researcher_topics, coder_operations)
        
        # Add comprehensive final summary
        if len(agent_activities) > 0:
            summary_parts = []
            
            if "researcher" in agent_activities:
                research_types = []
                if "market_analysis" in researcher_topics:
                    research_types.append("market analysis")
                if "data_research" in researcher_topics:
                    research_types.append("data research")
                if "trend_research" in researcher_topics:
                    research_types.append("trend analysis")
                if "comparative_research" in researcher_topics:
                    research_types.append("comparative analysis")
                
                research_detail = f"{len(researcher_outputs)} findings"
                if research_types:
                    research_detail += f" ({', '.join(research_types)})"
                summary_parts.append(f"� Researcher: {research_detail}")
            
            if "coder" in agent_activities:
                # Count unique operation types
                unique_ops = list(set(coder_operations))
                coder_detail = f"{len(coder_outputs)} operations"
                if unique_ops:
                    coder_detail += f" ({', '.join(unique_ops[:3])})"  # Show up to 3 types
                summary_parts.append(f"💻 Coder: {coder_detail}")
            
            if "manager" in agent_activities:
                summary_parts.append(f"🎯 Manager: Coordinated {event_count} workflow events")
            
            if summary_parts:
                activity_log.append({
                    "type": "system",
                    "message": f"📊 Collaboration Summary:\n   " + "\n   ".join(summary_parts),
                    "icon": "📊"
                })
        
        if result_text:
            logger.info("Task completed successfully")
            return TaskResponse(status="success", result=result_text, activity_log=activity_log)
        else:
            logger.warning("Task completed but no result generated")
            return TaskResponse(
                status="success", 
                result="Task completed but no output generated.",
                activity_log=activity_log
            )
    
    except Exception as e:
        logger.exception("Task execution failed")
        return TaskResponse(status="error", error=str(e), activity_log=[])


@app.post("/api/execute-stream")
async def execute_task_stream(request: TaskRequest):
    """
    Execute a task and stream events (for real-time updates)
    """
    await initialize_agents()
    
    if not workflow:
        raise HTTPException(status_code=500, detail="Workflow not initialized")
    
    async def event_generator():
        try:
            async for event in workflow.run_stream(request.task):
                event_type = event.__class__.__name__
                
                # Send different event types
                if isinstance(event, WorkflowOutputEvent):
                    if event.data:
                        # Handle if data is a list or a single object
                        messages = event.data if isinstance(event.data, list) else [event.data]
                        for message in messages:
                            if hasattr(message, 'text') and message.text:
                                yield f"data: {{'type': 'result', 'content': {repr(message.text)}}}\n\n"
                            elif hasattr(message, 'content') and message.content:
                                yield f"data: {{'type': 'result', 'content': {repr(message.content)}}}\n\n"
                else:
                    yield f"data: {{'type': 'event', 'name': '{event_type}'}}\n\n"
            
            yield f"data: {{'type': 'done'}}\n\n"
        except Exception as e:
            yield f"data: {{'type': 'error', 'message': {repr(str(e))}}}\n\n"
    
    from fastapi.responses import StreamingResponse
    return StreamingResponse(event_generator(), media_type="text/event-stream")


async def execute_task_internal(task: str) -> str:
    """
    Internal helper to execute a task and return the result as a string
    """
    if not workflow:
        raise Exception("Workflow not initialized")
    
    result_text = ""
    
    async for event in workflow.run_stream(task):
        if isinstance(event, WorkflowOutputEvent):
            if event.data:
                # Handle if data is a list or a single object
                messages = event.data if isinstance(event.data, list) else [event.data]
                for message in messages:
                    if hasattr(message, 'text') and message.text:
                        result_text = message.text
                    elif hasattr(message, 'content') and message.content:
                        result_text = message.content
    
    return result_text if result_text else "Task completed but no output generated."


# CopilotKit integration endpoint (simplified)
@app.post("/copilotkit")
async def copilotkit_endpoint(request: dict):
    """
    Simplified endpoint for CopilotKit integration
    Note: Full CopilotKit runtime integration requires agent_framework.chatkit
    This version provides basic task execution support
    """
    await initialize_agents()
    
    # Extract message from CopilotKit request format
    if "messages" in request and len(request["messages"]) > 0:
        last_message = request["messages"][-1]
        user_input = last_message.get("content", "")
        
        # Execute task
        try:
            result = await execute_task_internal(user_input)
            return {
                "messages": [
                    {
                        "role": "assistant",
                        "content": result
                    }
                ]
            }
        except Exception as e:
            return {
                "messages": [
                    {
                        "role": "assistant",
                        "content": f"Error executing task: {str(e)}"
                    }
                ]
            }
    
    return {"messages": []}


@app.get("/api/examples")
async def get_examples():
    """Get example tasks that can be executed"""
    return {
        "examples": [
            {
                "title": "ML Model Energy Analysis",
                "description": "Compare energy efficiency of ML models",
                "task": "Compare the estimated training and inference energy consumption of ResNet-50, BERT-base, and GPT-2. Include CO2 emissions for 24 hours on Azure Standard_NC6s_v3 VM."
            },
            {
                "title": "Market Research",
                "description": "Analyze AI chip market trends",
                "task": "Analyze the current state of the AI chip market. Include top 3 companies, calculate CAGR from $20B (2020) to $120B (2025), and identify fastest growing segment."
            },
            {
                "title": "Financial Analysis",
                "description": "Calculate ROI for a project",
                "task": "Calculate ROI for an AI project with $500K initial investment, $150K annual savings, 5-year lifespan. Calculate payback period, ROI%, and NPV (8% discount rate)."
            },
            {
                "title": "Technical Comparison",
                "description": "Compare cloud platforms",
                "task": "Compare AWS, Azure, and Google Cloud in terms of AI/ML capabilities, pricing for GPU instances, and market positioning in 2025."
            },
            {
                "title": "Data Analysis",
                "description": "Calculate and visualize Fibonacci sequence",
                "task": "Calculate the Fibonacci sequence up to the 15th number, compute ratios between consecutive numbers, and show convergence to the golden ratio (1.618)."
            }
        ]
    }


if __name__ == "__main__":
    import uvicorn
    import sys
    
    # Set UTF-8 encoding for Windows console
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except:
            pass
    
    print("\n" + "="*80)
    print("Starting Magentic Multi-Agent Backend")
    print("="*80)
    print("\nEndpoints:")
    print("   - http://localhost:8000/          (Health check)")
    print("   - http://localhost:8000/api/execute  (Execute task)")
    print("   - http://localhost:8000/api/examples (Example tasks)")
    print("   - http://localhost:8000/copilotkit  (CopilotKit basic integration)")
    print("   - http://localhost:8000/docs       (API documentation)")
    print("\nFrontend should connect to: http://localhost:8000")
    print("="*80 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
