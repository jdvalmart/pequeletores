#!/bin/bash
# ============================================
# PequeLectores — Modo Local
# Usar cuando Railway esté caído o para desarrollo
# ============================================
# Uso: ./start-local.sh
# Luego abrí http://localhost:5173 en el navegador
# ============================================

set -e

echo "🚂 PequeLectores — Modo Local"
echo "=============================="
echo ""

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"

# 1. PostgreSQL (Docker)
echo "📦 Paso 1: PostgreSQL..."
if docker ps --filter "name=pequelectores_db" --format "{{.Names}}" | grep -q pequelectores_db; then
    echo "   ✅ Ya está corriendo en puerto 5433"
else
    echo "   Iniciando..."
    docker-compose -f "$PROJECT_DIR/docker-compose.yml" up -d
    sleep 3
    echo "   ✅ Iniciado en puerto 5433"
fi
echo ""

# 2. Backend
echo "🧠 Paso 2: Backend (FastAPI)..."
cd "$PROJECT_DIR/backend"
source .venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
sleep 3
if kill -0 $BACKEND_PID 2>/dev/null; then
    echo "   ✅ Backend corriendo en http://localhost:8000"
else
    echo "   ❌ Error al iniciar backend"
    exit 1
fi
echo ""

# 3. Frontend
echo "🖥️  Paso 3: Frontend (React)..."
cd "$PROJECT_DIR/frontend"
npm run dev &
FRONTEND_PID=$!
sleep 3
echo "   ✅ Frontend corriendo en http://localhost:5173"
echo ""

echo "=============================="
echo "🎉 ¡Todo listo!"
echo ""
echo "   Abrí http://localhost:5173 en tu navegador"
echo ""
echo "Para detener:"
echo "   kill $BACKEND_PID $FRONTEND_PID"
echo "=============================="

# Esperar a que el usuario presione Ctrl+C
wait
