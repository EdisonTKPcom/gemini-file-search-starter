#!/bin/bash
# Quick start script for Gemini File Search Backend

set -e

echo "🚀 Gemini File Search Backend - Quick Start"
echo "==========================================="
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from template..."
    cp .env.example .env
    echo "✅ .env file created. Please add your GOOGLE_API_KEY before continuing."
    echo ""
    echo "Get your API key from: https://aistudio.google.com/app/apikey"
    echo ""
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
    echo ""
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"
echo ""

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt
echo "✅ Dependencies installed"
echo ""

# Create uploads directory
mkdir -p uploads
echo "✅ Uploads directory ready"
echo ""

# Check if GOOGLE_API_KEY is set
if ! grep -q "GOOGLE_API_KEY=your_google_api_key_here" .env && grep -q "GOOGLE_API_KEY=" .env; then
    echo "✅ GOOGLE_API_KEY configured"
    echo ""
    echo "🎉 Setup complete! Starting server..."
    echo ""
    python main.py
else
    echo "⚠️  GOOGLE_API_KEY not configured in .env file"
    echo ""
    echo "Please edit .env and add your API key:"
    echo "  GOOGLE_API_KEY=your_actual_api_key_here"
    echo ""
    echo "Get your API key from: https://aistudio.google.com/app/apikey"
    echo ""
    exit 1
fi
