# run-all.ps1 - Copy this entire content
Write-Host "🚀 Starting Complete Threat Intelligence Pipeline" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor White

# Step 1: Collect data
Write-Host "`n1️⃣ COLLECTING DATA..." -ForegroundColor Yellow
. .\collect.ps1

# Step 2: Normalize data  
Write-Host "`n2️⃣ NORMALIZING DATA..." -ForegroundColor Yellow
. .\normalize.ps1

# Step 3: Start API server
Write-Host "`n3️⃣ STARTING API SERVER..." -ForegroundColor Yellow
Write-Host "🎯 API will be available at: http://localhost:8080/api/data" -ForegroundColor Green
Write-Host "⏳ Server is running... (Press Ctrl+C to stop)" -ForegroundColor Cyan

. .\server.ps1