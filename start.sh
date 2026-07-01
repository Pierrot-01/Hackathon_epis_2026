#!/bin/bash
# Script de inicio del servidor — Vanguardia EPIS Backend
# Uso: ./start.sh [--api-key AIzaSy...]

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$PROJECT_DIR/backend"
ENV_FILE="$BACKEND_DIR/.env"

# Parsear argumento de API key
if [ "$1" = "--api-key" ] && [ -n "$2" ]; then
    echo "GEMINI_API_KEY=$2" > "$ENV_FILE"
    echo "✅ API key guardada en $ENV_FILE"
fi

# Verificar que el .env existe
if [ ! -f "$ENV_FILE" ]; then
    if [ -n "$GEMINI_API_KEY" ]; then
        echo "GEMINI_API_KEY=$GEMINI_API_KEY" > "$ENV_FILE"
        echo "✅ API key tomada desde variable de entorno"
    else
        echo "⚠️  No se encontró GEMINI_API_KEY."
        echo "   El servidor iniciará en modo de respaldo (fallback)."
        echo "   Para configurar la API: ./start.sh --api-key TU_KEY"
        echo ""
    fi
fi

# Generar cache si la API key está disponible y el cache no existe
CACHE_FILE="$PROJECT_DIR/cache/respuestas_ia.json"
if [ -f "$ENV_FILE" ] && [ ! -f "$CACHE_FILE" ]; then
    echo "🔄 Generando cache de respaldo (primera vez)..."
    cd "$PROJECT_DIR" && python3 generar_cache.py && echo "✅ Cache generado."
elif [ -f "$CACHE_FILE" ]; then
    echo "✅ Cache de respaldo encontrado."
fi

echo ""
echo "🚀 Iniciando Vanguardia EPIS Backend..."
echo "   URL: http://localhost:8000"
echo "   Dashboard: http://localhost:8000/monitoreo.html"
echo "   API Docs: http://localhost:8000/docs"
echo ""

cd "$BACKEND_DIR" && python3 main.py
