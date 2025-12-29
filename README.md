# Multi-Agent AI System with Magentic Pattern

A sophisticated multi-agent AI system built with Azure OpenAI, Agent Framework, and React that demonstrates the Magentic workflow pattern. Four specialized AI agents collaborate to analyze complex tasks requiring research, computation, critical review, and synthesis.

## 🌟 Features

- **4 Specialized AI Agents**:
  - 🔍 **Researcher**: Information gathering and market research
  - 💻 **Coder**: Data analysis and computational tasks with code execution
  - 🔎 **Reviewer**: Critical quality assurance and validation
  - 🎯 **Manager**: Orchestrates agent collaboration and synthesizes reports

- **Flexible Model Selection**: Choose different GPT models  for each agent
- **Real-time Activity Logging**: Watch agents collaborate in real-time
- **CopilotKit Integration**: AI-powered chat interface
- **Pre-loaded Examples**: ML model analysis, market research, financial calculations, technical comparisons

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    React Frontend                        │
│              (CopilotKit + Vite)                        │
└─────────────────┬───────────────────────────────────────┘
                  │ HTTP/REST
┌─────────────────▼───────────────────────────────────────┐
│              FastAPI Backend                             │
│         (Multi-Agent Orchestration)                      │
└─────────────────┬───────────────────────────────────────┘
                  │
      ┌───────────┴───────────┬───────────┬──────────┐
      │                       │           │          │
┌─────▼──────┐  ┌──────▼──────┐  ┌──────▼──────┐  ┌──▼────┐
│ Researcher │  │   Coder     │  │  Reviewer   │  │Manager│
│   Agent    │  │   Agent     │  │   Agent     │  │ Agent │
└────────────┘  └─────────────┘  └─────────────┘  └───────┘
      │                 │               │              │
      └─────────────────┴───────────────┴──────────────┘
                         │
                         ▼
              Azure OpenAI GPT-4o/4.1
```

## 📋 Prerequisites

- **Python 3.10+**
- **Node.js 18+** and npm
- **Azure OpenAI Service** with deployed model(s)
- **Azure CLI** (for authentication)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd E2EDemo
```

### 2. Configure Azure OpenAI

Copy the example environment file and fill in your Azure OpenAI details:

```bash
cp .env.example .env
```

Edit `.env` with your Azure OpenAI configuration:

```env
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=gpt-4o
AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME=gpt-4o
AZURE_OPENAI_API_VERSION=2024-10-01-preview
```

### 3. Authenticate with Azure

```bash
az login
```

The application uses `DefaultAzureCredential` which will use your Azure CLI authentication.

### 4. Install Python Dependencies

```bash
pip install -r requirements.txt
```

Required packages:
- `agent-framework` - Multi-agent orchestration
- `fastapi` - Backend API framework
- `uvicorn` - ASGI server
- `azure-identity` - Azure authentication
- `python-dotenv` - Environment variable management

### 5. Install Frontend Dependencies

```bash
cd magentic-ui
npm install
cd ..
```

### 6. Run the Application

**Option A: Using PowerShell (Windows)**

Terminal 1 - Backend:
```powershell
python magentic_ui_backend.py
```

Terminal 2 - Frontend:
```powershell
cd magentic-ui
npm run dev
```

**Option B: Using bash/zsh (Linux/Mac)**

Terminal 1 - Backend:
```bash
python magentic_ui_backend.py
```

Terminal 2 - Frontend:
```bash
cd magentic-ui
npm run dev
```

### 7. Open the Application

Navigate to **http://localhost:3000** in your browser.

## 🎯 Usage

### Using Pre-loaded Examples

1. Click on any example card (e.g., "ML Model Energy Analysis")
2. Select AI models for each agent (or use defaults)
3. Click "Execute with AI Team"
4. Watch the activity log to see agents collaborating
5. Review the comprehensive analysis report

### Creating Custom Tasks

1. Enter your task in the text area
2. For best results, include:
   - Clear objectives
   - Relevant data or context
   - Specific questions to answer
3. Select appropriate models for each agent
4. Execute and review results

### Example Custom Task

```
Analyze the growth of the electric vehicle market from 2020-2025:
- Research: Market size, key players, adoption rates
- Calculate: CAGR, market share changes, revenue projections
- Review: Validate assumptions and identify data gaps
```

## 🧠 How It Works

### The Magentic Pattern

The system uses the **Magentic workflow pattern** where:

1. **Manager Agent** receives the task and creates a plan
2. **Manager** delegates subtasks to specialist agents:
   - **Researcher** for information gathering
   - **Coder** for calculations and data analysis
   - **Reviewer** for quality assurance
3. Agents work collaboratively, with the Manager coordinating
4. **Reviewer** validates outputs and challenges assumptions
5. **Manager** synthesizes findings into a final report

### Agent Roles

**🔍 Researcher Agent**
- Gathers information from general knowledge
- Performs market research and competitive analysis
- Identifies trends and patterns
- No computational capabilities

**💻 Coder Agent**
- Executes Python code via hosted code interpreter
- Performs calculations and statistical analysis
- Generates charts and visualizations
- Processes and analyzes data

**🔎 Reviewer Agent**
- Critically evaluates analysis quality
- Validates assumptions and calculations
- Identifies gaps and missing considerations
- Challenges conclusions and weak reasoning
- Suggests improvements

**🎯 Manager Agent**
- Coordinates workflow between agents
- Plans task decomposition
- Synthesizes agent outputs
- Produces executive-ready reports

## 📁 Project Structure

```
E2EDemo/
├── .env.example              # Environment configuration template
├── .gitignore               # Git ignore rules
├── requirements.txt         # Python dependencies
├── Magentic.py             # Original CLI multi-agent workflow
├── magentic_ui_backend.py  # FastAPI backend server
├── demo.py                 # Simple demo script
├── test_detailed_logging.py # Backend testing script
├── JJ_DEMO_GUIDE.md        # Additional demo guide
├── PROJECT_EXPLANATION.md   # Technical deep-dive
├── DEMO_PITCH.md           # Presentation guide
├── VISUAL_GUIDE.md         # Visual aids
└── magentic-ui/            # React frontend
    ├── package.json
    ├── vite.config.js
    ├── index.html
    └── src/
        ├── App.jsx
        ├── main.jsx
        └── components/
            ├── MagenticWorkflow.jsx
            └── MagenticWorkflow.css
```

## 🔧 Configuration

### Backend Configuration

The backend (`magentic_ui_backend.py`) can be configured via:

- **Port**: Default 8000, change in `uvicorn.run()` call
- **Max Rounds**: Default 20, adjust in `MagenticBuilder().with_standard_manager(max_round_count=20)`
- **Models**: Default GPT-4o, can be changed per-request via API

### Frontend Configuration

The frontend connects to `http://localhost:8000` by default. To change:

1. Update proxy in `magentic-ui/vite.config.js`
2. Update axios base URL if needed

## 🎨 Customization

### Adding New Example Scenarios

Edit `magentic_ui_backend.py`, find the `/api/examples` endpoint:

```python
@app.get("/api/examples")
async def get_examples():
    return {
        "examples": [
            {
                "title": "Your Title",
                "description": "Short description",
                "task": "Detailed task description..."
            }
        ]
    }
```

### Customizing Agent Instructions

Modify agent instructions in `create_workflow_with_models()` function:

```python
researcher = ChatAgent(
    name="ResearcherAgent",
    description="Your custom description",
    instructions="Your custom instructions...",
    ...
)
```

## 🐛 Troubleshooting

### "Workflow not initialized"
- Ensure Azure OpenAI credentials are correct in `.env`
- Check `az login` is successful
- Verify your Azure OpenAI deployment names match `.env`

### Backend won't start
- Check port 8000 is not in use: `netstat -ano | findstr :8000` (Windows) or `lsof -i :8000` (Mac/Linux)
- Verify all Python packages are installed: `pip list | grep agent-framework`

### Frontend can't connect to backend
- Ensure backend is running on port 8000
- Check browser console for CORS errors
- Verify proxy configuration in `vite.config.js`

### "No module named 'agent_framework'"
- Install the correct package version: `pip install agent-framework`
- Check you're using the right Python environment

## 📊 API Documentation

When the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints

- `POST /api/execute` - Execute a task with the multi-agent system
- `GET /api/examples` - Get pre-loaded example tasks
- `GET /api/models` - Get available AI model options
- `GET /api/health` - Health check endpoint

## 🔒 Security Notes

- ⚠️ **Never commit `.env` file** - Contains sensitive Azure credentials
- Use Azure Managed Identity in production instead of DefaultAzureCredential
- Consider implementing rate limiting for the API
- Add authentication/authorization for production deployment

## 📈 Performance

- **Typical execution time**: 30-90 seconds depending on task complexity
- **Token usage**: Varies by model and task (GPT-4o: ~2000-5000 tokens per request)
- **Concurrent requests**: Backend supports async, but agents run sequentially per request

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

[Your License Here]

## 🙏 Acknowledgments

- Built with [Agent Framework](https://github.com/microsoft/agent-framework)
- Powered by Azure OpenAI
- UI powered by [CopilotKit](https://github.com/CopilotKit/CopilotKit)

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Check the troubleshooting section above
- Review Azure OpenAI documentation

## 🎓 Learn More

- [Agent Framework Documentation](https://github.com/microsoft/agent-framework)
- [Azure OpenAI Service](https://azure.microsoft.com/en-us/products/ai-services/openai-service)
- [Magentic Pattern Blog Post](https://devblogs.microsoft.com/semantic-kernel/)
- [CopilotKit Documentation](https://docs.copilotkit.ai/)

---

**Built with ❤️ using Azure OpenAI and Agent Framework**
