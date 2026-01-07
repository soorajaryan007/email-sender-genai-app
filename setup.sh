#!/bin/bash

echo "🚀 AI Cold Email Generator setup starting..."

ROOT_DIR=$(pwd)

# ----------------------------
# Check Python
# ----------------------------
if ! command -v python3 &> /dev/null
then
    echo "❌ Python3 not found. Please install Python 3.9+"
    exit 1
fi

echo "✅ $(python3 --version)"

# ----------------------------
# Backend setup
# ----------------------------
echo "📦 Setting up backend..."
cd backend || exit 1

# Create venv
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate

# Install deps
pip install --upgrade pip
pip install -r requirements.txt

# ----------------------------
# Collect ENV values
# ----------------------------
echo "🔐 Enter configuration details"

read -p "Enter GROQ API Key: " GROQ_API_KEY

read -p "SMTP Host (default: smtp.gmail.com): " SMTP_HOST
SMTP_HOST=${SMTP_HOST:-smtp.gmail.com}

read -p "SMTP Port (default: 465): " SMTP_PORT
SMTP_PORT=${SMTP_PORT:-465}

read -p "SMTP Email: " SMTP_EMAIL
read -s -p "SMTP App Password: " SMTP_PASSWORD
echo ""

# ----------------------------
# Create .env in backend/
# ----------------------------
cat <<EOF > .env
GROQ_API_KEY=$GROQ_API_KEY

SMTP_HOST=$SMTP_HOST
SMTP_PORT=$SMTP_PORT
SMTP_EMAIL=$SMTP_EMAIL
SMTP_PASSWORD=$SMTP_PASSWORD
EOF

echo "✅ backend/.env created"

# ----------------------------
# Start backend
# ----------------------------
echo "⚙️ Starting FastAPI backend..."
nohup uvicorn app.main:app --reload > backend.log 2>&1 &

BACKEND_PID=$!

# ----------------------------
# Start frontend
# ----------------------------
echo "🌐 Starting frontend..."
cd "$ROOT_DIR/frontend" || exit 1
nohup python3 -m http.server 8080 > frontend.log 2>&1 &

# ----------------------------
# Open browser
# ----------------------------
sleep 3

if command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:8080
else
    echo "➡️ Open http://localhost:8080 in your browser"
fi

echo ""
echo "🎉 Setup complete!"
echo "Backend running on http://127.0.0.1:8000"
echo "Frontend running on http://localhost:8080"
