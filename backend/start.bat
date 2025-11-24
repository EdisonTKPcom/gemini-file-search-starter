@echo off
REM Quick start script for Gemini File Search Backend (Windows)

echo.
echo 🚀 Gemini File Search Backend - Quick Start
echo ===========================================
echo.

REM Check if .env exists
if not exist .env (
    echo ⚠️  .env file not found. Creating from template...
    copy .env.example .env
    echo ✅ .env file created. Please add your GOOGLE_API_KEY before continuing.
    echo.
    echo Get your API key from: https://aistudio.google.com/app/apikey
    echo.
    exit /b 1
)

REM Check if virtual environment exists
if not exist venv (
    echo 📦 Creating virtual environment...
    python -m venv venv
    echo ✅ Virtual environment created
    echo.
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate
echo ✅ Virtual environment activated
echo.

REM Install dependencies
echo 📥 Installing dependencies...
pip install -q -r requirements.txt
echo ✅ Dependencies installed
echo.

REM Create uploads directory
if not exist uploads mkdir uploads
echo ✅ Uploads directory ready
echo.

REM Check if GOOGLE_API_KEY is configured
findstr /C:"GOOGLE_API_KEY=your_google_api_key_here" .env >nul
if %errorlevel% equ 0 (
    echo ⚠️  GOOGLE_API_KEY not configured in .env file
    echo.
    echo Please edit .env and add your API key:
    echo   GOOGLE_API_KEY=your_actual_api_key_here
    echo.
    echo Get your API key from: https://aistudio.google.com/app/apikey
    echo.
    exit /b 1
)

echo ✅ GOOGLE_API_KEY configured
echo.
echo 🎉 Setup complete! Starting server...
echo.
python main.py
