#!/bin/bash

# Run the Video RAG Chat System
# Usage: ./run_app.sh

set -e

echo "🎥 Starting Video RAG Chat System..."
echo ""

# ==============================
# Check .env
# ==============================
if [ ! -f .env ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo ""
    echo "❗ Please edit .env and add your API keys before running again."
    exit 1
fi

# ==============================
# Check ffmpeg
# ==============================
if ! command -v ffmpeg &> /dev/null; then
    echo "❌ ffmpeg not found!"
    echo ""
    echo "Install it using:"
    echo "  sudo apt update && sudo apt install -y ffmpeg"
    exit 1
fi

# ==============================
# Virtual Environment
# ==============================
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
    echo "✅ Virtual environment created"
    echo ""
fi

echo "🔌 Activating virtual environment..."
source .venv/bin/activate

# ==============================
# Install deps ONLY if needed
# ==============================
if [ ! -f ".venv/.deps_installed" ]; then
    echo "📥 Installing dependencies (first time only)..."
    pip install --upgrade pip
    pip install -r requirements.txt
    touch .venv/.deps_installed
    echo "✅ Dependencies installed"
    echo ""
else
    echo "⚡ Dependencies already installed — skipping"
    echo ""
fi

# ==============================
# Run App
# ==============================
echo "🌐 Launching Gradio interface..."
echo "📍 Local URL: http://localhost:7860"
echo "🎬 Ready to process YouTube videos!"
echo "Press Ctrl+C to stop"
echo "============================================================"
echo ""

python ui/gradio_app.py
