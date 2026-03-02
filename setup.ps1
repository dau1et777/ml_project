# Career Guidance Platform - Automated Setup Script for Windows
# Run this script once on a new computer to set up everything

param(
    [switch]$SkipBackend,
    [switch]$SkipFrontend
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Career Guidance Platform - Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
Write-Host "[1/6] Checking Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found. Please install Python 3.10+ from python.org" -ForegroundColor Red
    exit 1
}

# Check Node.js
Write-Host "[2/6] Checking Node.js..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version 2>&1
    Write-Host "✓ Found: Node.js $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Node.js not found. Please install Node.js 18+ from nodejs.org" -ForegroundColor Red
    exit 1
}

# Backend Setup
if (-not $SkipBackend) {
    Write-Host "[3/6] Setting up Backend..." -ForegroundColor Yellow
    Push-Location backend
    
    # Create virtual environment
    if (-not (Test-Path ".venv")) {
        Write-Host "  Creating virtual environment..." -ForegroundColor White
        python -m venv .venv
    } else {
        Write-Host "  Virtual environment exists" -ForegroundColor White
    }
    
    # Activate and install
    Write-Host "  Installing dependencies..." -ForegroundColor White
    .\.venv\Scripts\Activate.ps1
    pip install -q -r requirements.txt
    
    # Check if database exists
    if (-not (Test-Path "db.sqlite3")) {
        Write-Host "  Creating database..." -ForegroundColor White
        python manage.py migrate
        Write-Host "  Populating initial data..." -ForegroundColor White
        python manage.py populate_initial_data
        
        Write-Host ""
        Write-Host "  Would you like to create an admin user? (Y/N): " -NoNewline -ForegroundColor Cyan
        $createAdmin = Read-Host
        if ($createAdmin -eq "Y" -or $createAdmin -eq "y") {
            python manage.py createsuperuser
        }
    } else {
        Write-Host "  Database exists, skipping setup" -ForegroundColor White
    }
    
    Pop-Location
    Write-Host "✓ Backend setup complete" -ForegroundColor Green
} else {
    Write-Host "[3/6] Skipping Backend setup" -ForegroundColor Gray
}

# Frontend Setup
if (-not $SkipFrontend) {
    Write-Host "[4/6] Setting up Frontend..." -ForegroundColor Yellow
    Push-Location frontend
    
    if (-not (Test-Path "node_modules")) {
        Write-Host "  Installing dependencies (this may take a few minutes)..." -ForegroundColor White
        npm install --silent
    } else {
        Write-Host "  Dependencies already installed" -ForegroundColor White
    }
    
    Pop-Location
    Write-Host "✓ Frontend setup complete" -ForegroundColor Green
} else {
    Write-Host "[4/6] Skipping Frontend setup" -ForegroundColor Gray
}

Write-Host "[5/6] Configuration check..." -ForegroundColor Yellow
if (Test-Path "backend\.venv") { Write-Host "  ✓ Backend virtual environment" -ForegroundColor Green } else { Write-Host "  ✗ Backend virtual environment missing" -ForegroundColor Red }
if (Test-Path "backend\db.sqlite3") { Write-Host "  ✓ Database created" -ForegroundColor Green } else { Write-Host "  ✗ Database missing" -ForegroundColor Red }
if (Test-Path "frontend\node_modules") { Write-Host "  ✓ Frontend dependencies" -ForegroundColor Green } else { Write-Host "  ✗ Frontend dependencies missing" -ForegroundColor Red }

Write-Host ""
Write-Host "[6/6] Setup Complete!" -ForegroundColor Green
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Terminal 1 - Start Backend:" -ForegroundColor White
Write-Host "  cd backend" -ForegroundColor Gray
Write-Host "  .\.venv\Scripts\Activate.ps1" -ForegroundColor Gray
Write-Host "  python manage.py runserver" -ForegroundColor Gray
Write-Host ""
Write-Host "Terminal 2 - Start Frontend:" -ForegroundColor White
Write-Host "  cd frontend" -ForegroundColor Gray
Write-Host "  npm start" -ForegroundColor Gray
Write-Host ""
Write-Host "Then open: http://localhost:3000" -ForegroundColor Yellow
Write-Host ""
Write-Host "Admin panel: http://localhost:8000/admin/" -ForegroundColor Yellow
Write-Host ""
