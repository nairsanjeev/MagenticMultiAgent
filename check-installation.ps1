# Magentic UI - Installation Verification Script
# Checks all dependencies and configurations

Write-Host "🔍 Magentic UI - System Check" -ForegroundColor Cyan
Write-Host "==============================" -ForegroundColor Cyan
Write-Host ""

$allGood = $true

# 1. Check Python
Write-Host "1️⃣  Checking Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1 | Out-String
    $versionMatch = $pythonVersion -match "Python (\d+)\.(\d+)"
    if ($versionMatch) {
        $major = [int]$Matches[1]
        $minor = [int]$Matches[2]
        if ($major -ge 3 -and $minor -ge 12) {
            Write-Host "   ✅ Python $major.$minor installed" -ForegroundColor Green
        } else {
            Write-Host "   ⚠️  Python $major.$minor found, but 3.12+ recommended" -ForegroundColor Yellow
        }
    } else {
        Write-Host "   ✅ $pythonVersion" -ForegroundColor Green
    }
} catch {
    Write-Host "   ❌ Python not found!" -ForegroundColor Red
    Write-Host "      Install from: https://www.python.org/downloads/" -ForegroundColor Yellow
    $allGood = $false
}
Write-Host ""

# 2. Check Node.js
Write-Host "2️⃣  Checking Node.js..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version 2>&1
    Write-Host "   ✅ Node.js $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Node.js not found!" -ForegroundColor Red
    Write-Host "      Install from: https://nodejs.org/" -ForegroundColor Yellow
    $allGood = $false
}
Write-Host ""

# 3. Check npm
Write-Host "3️⃣  Checking npm..." -ForegroundColor Yellow
try {
    $npmVersion = npm --version 2>&1
    Write-Host "   ✅ npm $npmVersion" -ForegroundColor Green
} catch {
    Write-Host "   ❌ npm not found!" -ForegroundColor Red
    $allGood = $false
}
Write-Host ""

# 4. Check Python packages
Write-Host "4️⃣  Checking Python packages..." -ForegroundColor Yellow
$requiredPackages = @(
    "fastapi",
    "uvicorn",
    "agent-framework",
    "agent-framework-azure", 
    "agent-framework-chatkit",
    "azure-identity",
    "python-dotenv"
)

$missingPackages = @()
foreach ($package in $requiredPackages) {
    $installed = pip show $package 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   ✅ $package" -ForegroundColor Green
    } else {
        Write-Host "   ❌ $package (missing)" -ForegroundColor Red
        $missingPackages += $package
    }
}

if ($missingPackages.Count -gt 0) {
    Write-Host ""
    Write-Host "   📦 To install missing packages, run:" -ForegroundColor Cyan
    Write-Host "      pip install $($missingPackages -join ' ')" -ForegroundColor White
    $allGood = $false
}
Write-Host ""

# 5. Check Azure CLI
Write-Host "5️⃣  Checking Azure CLI..." -ForegroundColor Yellow
try {
    $azVersion = az --version 2>&1 | Select-String "azure-cli" | Select-Object -First 1
    Write-Host "   ✅ Azure CLI installed: $azVersion" -ForegroundColor Green
    
    # Check if logged in
    $azAccount = az account show 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   ✅ Azure: Logged in" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️  Azure: Not logged in" -ForegroundColor Yellow
        Write-Host "      Run: az login" -ForegroundColor White
    }
} catch {
    Write-Host "   ⚠️  Azure CLI not found (optional but recommended)" -ForegroundColor Yellow
    Write-Host "      Install from: https://aka.ms/azure-cli" -ForegroundColor White
}
Write-Host ""

# 6. Check .env file
Write-Host "6️⃣  Checking configuration..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "   ✅ .env file exists" -ForegroundColor Green
    
    # Check required variables
    $envContent = Get-Content ".env" -Raw
    $requiredVars = @(
        "AZURE_OPENAI_ENDPOINT",
        "AZURE_OPENAI_CHAT_DEPLOYMENT_NAME",
        "AZURE_OPENAI_API_VERSION"
    )
    
    foreach ($var in $requiredVars) {
        if ($envContent -match "$var=") {
            Write-Host "   ✅ $var configured" -ForegroundColor Green
        } else {
            Write-Host "   ❌ $var missing" -ForegroundColor Red
            $allGood = $false
        }
    }
} else {
    Write-Host "   ❌ .env file not found!" -ForegroundColor Red
    Write-Host "      Create .env with Azure OpenAI credentials" -ForegroundColor Yellow
    $allGood = $false
}
Write-Host ""

# 7. Check backend file
Write-Host "7️⃣  Checking backend..." -ForegroundColor Yellow
if (Test-Path "magentic_ui_backend.py") {
    Write-Host "   ✅ magentic_ui_backend.py exists" -ForegroundColor Green
} else {
    Write-Host "   ❌ magentic_ui_backend.py not found!" -ForegroundColor Red
    $allGood = $false
}
Write-Host ""

# 8. Check frontend
Write-Host "8️⃣  Checking frontend..." -ForegroundColor Yellow
if (Test-Path "magentic-ui") {
    Write-Host "   ✅ magentic-ui directory exists" -ForegroundColor Green
    
    if (Test-Path "magentic-ui\package.json") {
        Write-Host "   ✅ package.json exists" -ForegroundColor Green
    } else {
        Write-Host "   ❌ package.json not found!" -ForegroundColor Red
        $allGood = $false
    }
    
    if (Test-Path "magentic-ui\node_modules") {
        Write-Host "   ✅ node_modules installed" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️  node_modules not found" -ForegroundColor Yellow
        Write-Host "      Run: cd magentic-ui && npm install" -ForegroundColor White
    }
} else {
    Write-Host "   ❌ magentic-ui directory not found!" -ForegroundColor Red
    $allGood = $false
}
Write-Host ""

# Summary
Write-Host "========================================" -ForegroundColor Cyan
if ($allGood) {
    Write-Host "✅ All checks passed! Ready to go!" -ForegroundColor Green
    Write-Host ""
    Write-Host "🚀 To start Magentic UI, run:" -ForegroundColor Cyan
    Write-Host "   .\start-magentic-ui.ps1" -ForegroundColor White
} else {
    Write-Host "⚠️  Some issues found. Please fix them first." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "📚 For help, see: magentic-ui\README.md" -ForegroundColor Cyan
}
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Press any key to continue..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
