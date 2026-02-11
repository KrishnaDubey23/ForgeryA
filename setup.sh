#!/bin/bash
# ForgeryA Quick Setup Script for macOS/Linux
# Run this after cloning the repo

set -e  # Exit on error

echo ""
echo "============================================"
echo "ForgeryA - Quick Setup"
echo "============================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    exit 1
fi

echo "[1/4] Creating Python virtual environment..."
cd backend
python3 -m venv .venv
cd ..

echo "[2/4] Installing Python dependencies..."
source backend/.venv/bin/activate
pip install -r backend/requirements.txt
deactivate

echo "[3/4] Installing frontend dependencies..."
cd frontend
npm install
cd ..

echo "[4/4] Verifying installation..."
source backend/.venv/bin/activate
python3 -c "import fastapi; print('✓ Backend OK')"
deactivate

echo ""
echo "============================================"
echo "✓ Setup Complete!"
echo "============================================"
echo ""
echo "Next steps:"
echo ""
echo "[Terminal 1] Start Backend:"
echo "  cd backend"
echo "  source .venv/bin/activate"
echo "  python main.py"
echo ""
echo "Frontend: http://localhost:3000"
echo "Backend:  http://localhost:8000"
echo ""
