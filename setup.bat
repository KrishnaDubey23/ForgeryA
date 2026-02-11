@echo off
REM ForgeryA Quick Setup Script for Windows
REM Run this after cloning the repo

echo.
echo ============================================
echo ForgeryA - Quick Setup
echo ============================================
echo.

echo [1/4] Creating Python virtual environment...
cd backend
python -m venv .venv
if errorlevel 1 (
    echo ERROR: Failed to create venv. Make sure Python 3.9+ is installed
    pause
    exit /b 1
)
cd ..

echo [2/4] Installing Python dependencies...
call backend\.venv\Scripts\activate.bat
pip install -r backend\requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install Python packages
    pause
    exit /b 1
)
call backend\.venv\Scripts\deactivate.bat

echo [3/4] Installing frontend dependencies...
cd frontend
call npm install
if errorlevel 1 (
    echo ERROR: Failed to install npm packages. Make sure Node.js is installed
    cd ..
    pause
    exit /b 1
)
cd ..

echo [4/4] Verifying installation...
call backend\.venv\Scripts\python -c "import fastapi; print('✓ Backend OK')"
if errorlevel 1 (
    echo ERROR: Backend verification failed
    pause
    exit /b 1
)

call frontend\node_modules\.bin\npm -v >nul
if errorlevel 1 (
    echo ERROR: Frontend verification failed
    pause
    exit /b 1
)

echo.
echo ============================================
echo ✓ Setup Complete!
echo ============================================
echo.
echo Next steps:
echo.
echo [Terminal 1] Start Backend:
echo   cd backend
echo   .\.venv\Scripts\python main.py
echo.
echo [Terminal 2] Start Frontend:
echo   cd frontend
echo   npm start
echo.
echo Frontend: http://localhost:3000
echo Backend:  http://localhost:8000
echo.
echo Press any key to continue...
pause
