Write-Host "🚀 AI Cold Email Generator Setup Starting..." -ForegroundColor Cyan

# ----------------------------
# Check Python
# ----------------------------
try {
    python --version | Out-Null
} catch {
    Write-Host "❌ Python not found. Please install Python 3.9+" -ForegroundColor Red
    exit
}

# ----------------------------
# Backend setup
# ----------------------------
Write-Host "📦 Setting up backend..." -ForegroundColor Yellow
cd backend

if (!(Test-Path "venv")) {
    python -m venv venv
}

& venv\Scripts\activate

pip install --upgrade pip
pip install -r requirements.txt

# ----------------------------
# Collect ENV details
# ----------------------------
Write-Host "🔐 Enter environment details" -ForegroundColor Green

$GROQ_API_KEY = Read-Host "Enter GROQ API Key"

$SMTP_EMAIL = Read-Host "Enter SMTP Email (e.g. gmail)"
$SMTP_PASSWORD = Read-Host "Enter SMTP App Password"
$SMTP_HOST = Read-Host "Enter SMTP Host (default: smtp.gmail.com)"
$SMTP_PORT = Read-Host "Enter SMTP Port (default: 465)"

if ($SMTP_HOST -eq "") { $SMTP_HOST = "smtp.gmail.com" }
if ($SMTP_PORT -eq "") { $SMTP_PORT = "465" }

@"
GROQ_API_KEY=$GROQ_API_KEY

SMTP_HOST=$SMTP_HOST
SMTP_PORT=$SMTP_PORT
SMTP_EMAIL=$SMTP_EMAIL
SMTP_PASSWORD=$SMTP_PASSWORD
"@ | Out-File -Encoding UTF8 .env

Write-Host "✅ .env file created" -ForegroundColor Green

# ----------------------------
# Start Backend (new window)
# ----------------------------
Write-Host "⚙️ Starting FastAPI backend..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "cd backend; venv\Scripts\activate; uvicorn app.main:app --reload"

# ----------------------------
# Start Frontend
# ----------------------------
Write-Host "🌐 Starting frontend..." -ForegroundColor Cyan
cd ..
cd frontend

Start-Process powershell -ArgumentList "python -m http.server 8080"

# ----------------------------
# Open Browser
# ----------------------------
Start-Sleep -Seconds 3
Start-Process "http://localhost:8080"

Write-Host "🎉 Setup complete! App is running." -ForegroundColor Green
