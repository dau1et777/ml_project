# Career Guidance Platform - Start Script
# This script starts both backend and frontend servers

Write-Host "🚀 Starting Career Guidance Platform..." -ForegroundColor Green
Write-Host ""

# Check if we're in the right directory
if (-Not (Test-Path "backend\manage.py")) {
    Write-Host "❌ Error: Please run this script from the ml/ root directory" -ForegroundColor Red
    exit 1
}

Write-Host "📊 Starting Django Backend..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; python manage.py runserver"

Start-Sleep -Seconds 2

Write-Host "⚛️  Starting React Frontend..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; npm start"

Write-Host ""
Write-Host "✅ Both servers are starting!" -ForegroundColor Green
Write-Host ""
Write-Host "📍 Backend:  http://localhost:8000" -ForegroundColor Yellow
Write-Host "📍 Frontend: http://localhost:3000" -ForegroundColor Yellow
Write-Host ""
Write-Host "💡 Tip: Close the terminal windows to stop the servers" -ForegroundColor Gray
Write-Host "📖 See QUICKSTART.md for complete usage guide" -ForegroundColor Gray
