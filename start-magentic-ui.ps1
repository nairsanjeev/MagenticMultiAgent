# Magentic UI Startup Script
# This script starts both the backend and frontend servers

Write-Host "🚀 Starting Magentic UI with CopilotKit..." -ForegroundColor Cyan
Write-Host ""

# Check if we're in the right directory
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

# Check prerequisites
Write-Host "✅ Checking prerequisites..." -ForegroundColor Yellow

# Check Python
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✓ Python: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "  ✗ Python not found! Please install Python 3.12+" -ForegroundColor Red
    exit 1
}

# Check Node.js
$nodeVersion = node --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✓ Node.js: $nodeVersion" -ForegroundColor Green
} else {
    Write-Host "  ✗ Node.js not found! Please install Node.js 18+" -ForegroundColor Red
    exit 1
}

# Check Azure CLI login
Write-Host "  ℹ Checking Azure authentication..." -ForegroundColor Cyan
$azAccount = az account show 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✓ Azure: Logged in" -ForegroundColor Green
} else {
    Write-Host "  ⚠ Azure: Not logged in. Run 'az login' if needed" -ForegroundColor Yellow
}

Write-Host ""

# Check if npm packages are installed
if (!(Test-Path "magentic-ui\node_modules")) {
    Write-Host "📦 Installing frontend dependencies..." -ForegroundColor Yellow
    Set-Location magentic-ui
    npm install
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ npm install failed!" -ForegroundColor Red
        exit 1
    }
    Set-Location ..
    Write-Host "✅ Frontend dependencies installed!" -ForegroundColor Green
    Write-Host ""
}

# Start backend in new window
Write-Host "🔧 Starting Backend Server (Port 8000)..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", @"
Write-Host '🔧 Magentic Backend Server' -ForegroundColor Cyan
Write-Host '================================' -ForegroundColor Cyan
Write-Host ''
Set-Location '$scriptDir'
python magentic_ui_backend.py
"@

Start-Sleep -Seconds 3

# Start frontend in new window
Write-Host "🎨 Starting Frontend Server (Port 3000)..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", @"
Write-Host '🎨 Magentic Frontend Server' -ForegroundColor Green
Write-Host '================================' -ForegroundColor Green
Write-Host ''
Set-Location '$scriptDir\magentic-ui'
npm run dev
"@

Start-Sleep -Seconds 2

Write-Host ""
Write-Host "✨ Magentic UI is starting up!" -ForegroundColor Green
Write-Host ""
Write-Host "📍 Access the application:" -ForegroundColor Yellow
Write-Host "   Frontend: http://localhost:3000" -ForegroundColor Cyan
Write-Host "   Backend:  http://localhost:8000" -ForegroundColor Cyan
Write-Host ""
Write-Host "⏱  Please wait 10-20 seconds for both servers to fully start..." -ForegroundColor Yellow
Write-Host ""
Write-Host "💡 Tips:" -ForegroundColor Magenta
Write-Host "   • Two new windows opened for backend and frontend" -ForegroundColor White
Write-Host "   • Close those windows to stop the servers" -ForegroundColor White
Write-Host "   • Check those windows for any errors" -ForegroundColor White
Write-Host "   • Backend initializes AI agents on startup (may take 15-20 seconds)" -ForegroundColor White
Write-Host ""

# Wait and then open browser
Write-Host "🌐 Opening browser in 10 seconds..." -ForegroundColor Cyan
Start-Sleep -Seconds 10
Start-Process "http://localhost:3000"

Write-Host ""
Write-Host "✅ Done! Your browser should open automatically." -ForegroundColor Green
Write-Host "   If not, navigate to: http://localhost:3000" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press any key to close this window..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
