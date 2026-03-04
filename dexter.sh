#!/bin/bash

case "$1" in
  compare)
    echo "🚀 Iniciando comparador de modelos con memoria conversacional..."
    docker run -it --rm \
      --name dexter-compare \
      --env-file .env \
      -v $(pwd)/sessions:/app/sessions \
      dexter-free \
      uv run python interactive_compare_with_memory.py
    ;;
  compare-simple)
    echo "🚀 Iniciando comparador de modelos (sin memoria)..."
    docker run -it --rm \
      --name dexter-compare \
      --env-file .env \
      -v $(pwd)/sessions:/app/sessions \
      dexter-free
    ;;
  agent)
    echo "🤖 Iniciando Dexter Agent original..."
    docker run -it --rm \
      --name dexter-agent \
      --env-file .env \
      dexter-free \
      uv run dexter-agent
    ;;
  *)
    echo "Uso: $0 {compare|compare-simple|agent}"
    echo ""
    echo "  compare        - Comparador con memoria conversacional (RECOMENDADO)"
    echo "  compare-simple - Comparador sin memoria"
    echo "  agent          - CLI original de Dexter"
    exit 1
    ;;
esac
