# Start the Threat Intelligence Backend Server
Write-Host "🛡️ Starting Threat Intelligence Backend..." -ForegroundColor Green

# Check if Python is available
try {
    $pythonVersion = python --version
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found. Please install Python." -ForegroundColor Red
    exit 1
}

# Install dependencies
Write-Host "📦 Checking dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# Start the Flask application
Write-Host "🚀 Starting Flask server on http://localhost:8080" -ForegroundColor Green
Write-Host "📊 API available at: http://localhost:8080/api/data" -ForegroundColor Cyan
Write-Host "⏹️  Press Ctrl+C to stop the server" -ForegroundColor Yellow

python .\src\app.py