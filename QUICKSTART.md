# 🚀 Magentic UI - Quick Start Guide

## First Time Setup

### Step 1: Check Your System
```powershell
.\check-installation.ps1
```
This verifies all dependencies are installed.

### Step 2: Install Frontend Dependencies
```powershell
cd magentic-ui
npm install
cd ..
```

### Step 3: Verify Azure Login
```powershell
az login
az account show
```

## Starting the Application

### Option A: Automatic Start (Recommended)
```powershell
.\start-magentic-ui.ps1
```
This automatically:
- ✅ Checks prerequisites
- ✅ Starts backend on port 8000
- ✅ Starts frontend on port 3000
- ✅ Opens browser to http://localhost:3000

### Option B: Manual Start

**Terminal 1 - Backend:**
```powershell
python magentic_ui_backend.py
```

**Terminal 2 - Frontend:**
```powershell
cd magentic-ui
npm run dev
```

## Using the UI

### 1️⃣ Submit a Task
Type your task in the text area:
```
Analyze the cloud computing market growth from 2020-2025.
Include top 3 providers and calculate CAGR.
```

### 2️⃣ Use Examples
Click any example task card to load it instantly.

### 3️⃣ Chat with AI
Click the chat bubble (💬) in the bottom right to get help from CopilotKit.

## Example Tasks

**Market Research:**
```
Analyze the current state of the AI chip market including top 3 companies,
market size CAGR from $20B (2020) to $120B (2025), and fastest growing segment.
```

**Financial Calculation:**
```
Calculate ROI for an AI project: $500K initial investment, $150K annual savings,
5-year lifespan. Include payback period, ROI%, and NPV at 8% discount rate.
```

**Technical Comparison:**
```
Compare AWS, Azure, and Google Cloud for AI/ML capabilities, GPU pricing,
and market positioning in 2025.
```

## The 3 AI Agents

🔍 **Researcher Agent** - Gathers information and facts  
💻 **Coder Agent** - Performs calculations and data analysis  
🎯 **Manager Agent** - Coordinates the team and compiles final report

## Typical Workflow

1. **User submits task** → Manager receives it
2. **Manager delegates** → Researcher gathers info, Coder does calculations
3. **Agents collaborate** → Share findings, Manager synthesizes
4. **Results ready** → Comprehensive report displayed (usually 1-3 minutes)

## Common Issues

### Backend won't start
```powershell
# Check Python packages
pip install fastapi uvicorn agent-framework agent-framework-azure agent-framework-chatkit azure-identity

# Check .env file exists
Get-Content .env
```

### Frontend won't connect
```powershell
# Verify backend is running
Invoke-RestMethod http://localhost:8000/api/health

# Check proxy in vite.config.js
```

### Azure authentication errors
```powershell
# Re-login to Azure
az login
az account set --subscription "your-subscription-id"
```

### Port already in use
```powershell
# Kill process on port 8000 (backend)
Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess | Stop-Process

# Kill process on port 3000 (frontend)
Get-Process -Id (Get-NetTCPConnection -LocalPort 3000).OwningProcess | Stop-Process
```

## File Structure

```
c:\E2EDemo\
├── .env                         # Azure OpenAI config
├── Magentic.py                  # Original workflow (CLI)
├── magentic_ui_backend.py       # FastAPI backend
├── start-magentic-ui.ps1        # Auto-start script
├── check-installation.ps1       # System check
└── magentic-ui\                 # React frontend
    ├── package.json
    ├── vite.config.js
    ├── src\
    │   ├── App.jsx              # Main app with CopilotKit
    │   └── components\
    │       └── MagenticWorkflow.jsx
    └── README.md                # Full documentation
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check |
| `/api/health` | GET | API status |
| `/api/examples` | GET | Example tasks |
| `/api/execute` | POST | Execute task (sync) |
| `/api/execute-stream` | POST | Execute with streaming |
| `/copilotkit` | POST | CopilotKit integration |

## Performance Tips

- **Simple tasks:** ~30 seconds
- **Complex tasks:** 1-3 minutes
- **Timeout:** 5 minutes max
- **Rate limits:** Respect Azure OpenAI quotas

## Next Steps

1. ✅ Try the example tasks
2. ✅ Experiment with custom tasks
3. ✅ Use CopilotKit chat for task creation
4. ✅ Check the full README: `magentic-ui\README.md`

## Need Help?

📚 Full documentation: `magentic-ui\README.md`  
🔧 Check system: `.\check-installation.ps1`  
🚀 Start app: `.\start-magentic-ui.ps1`

---

**Built with:** Microsoft Agent Framework • Azure OpenAI • FastAPI • React • CopilotKit
