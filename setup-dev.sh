#!/bin/bash
# Setup script for new developers
# Usage: ./setup-dev.sh

set -e

echo "🚀 PequeLectores - Development Setup"
echo "======================================"

# Check prerequisites
command -v docker >/dev/null 2>&1 || { echo "❌ Docker is required but not installed."; exit 1; }
command -v npm >/dev/null 2>&1 || { echo "❌ npm is required but not installed."; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "❌ Python 3 is required but not installed."; exit 1; }

echo ""
echo "📦 Step 1: Starting PostgreSQL..."
docker-compose up -d
echo "✅ PostgreSQL is running"

echo ""
echo "📦 Step 2: Setting up Backend..."
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Run migrations (if using Alembic)
# alembic upgrade head

echo "✅ Backend is ready"
echo "   Run: cd backend && source venv/bin/activate && uvicorn app.main:app --reload"

echo ""
echo "📦 Step 3: Setting up Frontend..."
cd ../frontend

# Install npm dependencies
echo "Installing npm dependencies..."
npm install

echo "✅ Frontend is ready"
echo "   Run: cd frontend && npm run dev"

echo ""
echo "📦 Step 4: Verifying installation..."
echo ""

echo "Backend tests:"
cd ../backend
source venv/bin/activate
pytest --collect-only -q 2>/dev/null && echo "   ✅ Tests collection works" || echo "   ⚠️  Some tests may need dependencies"

echo ""
echo "Frontend tests:"
cd ../frontend
npm test -- --run --reporter=verbose 2>/dev/null && echo "   ✅ Tests pass" || echo "   ⚠️  Run npm test to verify"

echo ""
echo "======================================"
echo "🎉 Setup complete!"
echo ""
echo "To start the development servers:"
echo "  Terminal 1: cd backend && source venv/bin/activate && uvicorn app.main:app --reload"
echo "  Terminal 2: cd frontend && npm run dev"
echo ""
echo "Then open http://localhost:5173 in your browser."