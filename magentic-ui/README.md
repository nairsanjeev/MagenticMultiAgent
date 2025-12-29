# Magentic UI with CopilotKit Integration

A beautiful React-based user interface for the Magentic Multi-Agent Workflow, integrated with CopilotKit for enhanced AI assistance.

## 🌟 Features

- **Interactive UI** - Beautiful, modern interface for submitting tasks
- **Multi-Agent Visualization** - See which agents are working on your task
- **Example Tasks** - Pre-built examples to get started quickly
- **CopilotKit Integration** - Chat with an AI assistant to help create tasks
- **Real-time Results** - See results as agents complete their work
- **Responsive Design** - Works on desktop, tablet, and mobile

## 🏗️ Architecture

```
┌─────────────────────┐
│   React Frontend    │  (Port 3000)
│   + CopilotKit UI   │
└──────────┬──────────┘
           │
           ↓
┌─────────────────────┐
│  FastAPI Backend    │  (Port 8000)
│  + Agent Framework  │
└──────────┬──────────┘
           │
           ↓
┌─────────────────────┐
│  Magentic Workflow  │
│  3 AI Agents        │
│  - Researcher       │
│  - Coder            │
│  - Manager          │
└─────────────────────┘
```

## 📋 Prerequisites

- Python 3.12+
- Node.js 18+ and npm
- Azure OpenAI access
- Azure CLI (logged in with `az login`)

## 🚀 Quick Start

### 1. Start the Backend

```powershell
# Install Python dependencies (if not already installed)
pip install fastapi uvicorn agent-framework agent-framework-azure agent-framework-chatkit azure-identity

# Start the backend server
python magentic_ui_backend.py
```

The backend will start on **http://localhost:8000**

### 2. Start the Frontend

Open a new terminal:

```powershell
# Navigate to the UI directory
cd magentic-ui

# Install dependencies (first time only)
npm install

# Start the development server
npm run dev
```

The frontend will start on **http://localhost:3000**

### 3. Open in Browser

Navigate to: **http://localhost:3000**

## 🎮 How to Use

### Method 1: Direct Task Input

1. Type or paste your task in the text area
2. Click "Execute with AI Team"
3. Wait for agents to collaborate (1-3 minutes)
4. View the results!

### Method 2: Use Example Tasks

1. Click on any example task card
2. The task will populate the input field
3. Click "Execute with AI Team"

### Method 3: Chat with CopilotKit Assistant

1. Click the chat bubble in the bottom right
2. Ask the AI assistant to help create a task
3. The assistant can execute tasks directly via the Magentic agents

## 💡 Example Tasks

**Market Research:**
```
Analyze the current state of the AI chip market. Include top 3 companies, 
calculate CAGR from $20B (2020) to $120B (2025), and identify fastest growing segment.
```

**Financial Analysis:**
```
Calculate ROI for an AI project with $500K initial investment, $150K annual savings, 
5-year lifespan. Calculate payback period, ROI%, and NPV (8% discount rate).
```

**Technical Comparison:**
```
Compare AWS, Azure, and Google Cloud in terms of AI/ML capabilities, pricing for 
GPU instances, and market positioning in 2025.
```

## 🎨 UI Features

### Agents Dashboard
- **Researcher Agent** 🔍 - Information gathering
- **Coder Agent** 💻 - Data analysis and computation
- **Manager Agent** 🎯 - Team coordination

### Task Interface
- Large text area for complex tasks
- Character count and formatting
- Clear visual feedback

### Results Display
- Formatted output with syntax highlighting
- Copy to clipboard functionality
- Download as text/markdown

### CopilotKit Chat
- Floating chat interface
- Context-aware assistance
- Direct task execution

## 🔧 Configuration

### Backend Configuration

Edit `magentic_ui_backend.py`:

```python
# Change port
uvicorn.run(app, host="0.0.0.0", port=8000)

# Adjust workflow limits
max_round_count=20,  # Maximum interaction rounds
max_stall_count=5,   # Maximum stalls before reset
max_reset_count=3,   # Maximum resets
```

### Frontend Configuration

Edit `vite.config.js`:

```javascript
server: {
  port: 3000,  // Change frontend port
  proxy: {
    '/api': {
      target: 'http://localhost:8000',  // Backend URL
    }
  }
}
```

## 📡 API Endpoints

### Backend Endpoints

- `GET /` - Health check
- `GET /api/health` - API health status
- `GET /api/examples` - Get example tasks
- `POST /api/execute` - Execute a task
- `POST /api/execute-stream` - Execute with streaming
- `POST /copilotkit` - CopilotKit integration endpoint

### Example API Call

```javascript
const response = await fetch('http://localhost:8000/api/execute', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    task: "Your task here",
    max_rounds: 20
  })
})

const result = await response.json()
console.log(result.result)
```

## 🐛 Troubleshooting

### Backend won't start
- Check Python version: `python --version` (need 3.12+)
- Verify Azure login: `az account show`
- Check `.env` file exists in `c:\E2EDemo\`

### Frontend won't connect to backend
- Verify backend is running on port 8000
- Check CORS settings in `magentic_ui_backend.py`
- Clear browser cache

### CopilotKit not working
- Verify `/copilotkit` endpoint is accessible
- Check browser console for errors
- Ensure backend has `agent-framework-chatkit` installed

### Agents timeout or fail
- Check Azure OpenAI quota and rate limits
- Reduce `max_round_count` for simpler tasks
- Review task complexity

## 📦 Production Deployment

### Build for Production

```powershell
cd magentic-ui
npm run build
```

### Serve with Backend

```python
# Add to magentic_ui_backend.py
from fastapi.staticfiles import StaticFiles

app.mount("/", StaticFiles(directory="magentic-ui/dist", html=True), name="static")
```

### Environment Variables

```env
# .env file
AZURE_OPENAI_ENDPOINT=https://your-endpoint.openai.azure.com/
AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=gpt-4.1
AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME=gpt-4.1
AZURE_OPENAI_API_VERSION=2024-10-01-preview
```

## 🎯 Next Steps

- Add authentication/authorization
- Implement task history/saved tasks
- Add real-time streaming of agent messages
- Create admin panel for agent configuration
- Add analytics dashboard
- Support for custom agent creation

## 📚 Learn More

- [CopilotKit Documentation](https://docs.copilotkit.ai/)
- [Microsoft Agent Framework](https://github.com/microsoft/agent-framework)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📄 License

This project is part of the Magentic Multi-Agent demonstration.

---

**Enjoy building with Magentic! 🚀**
