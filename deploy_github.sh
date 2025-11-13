#!/bin/bash

# Script para preparar y subir el proyecto a GitHub
# Ejecutar: ./deploy_github.sh

echo "🚀 Preparando Video Whisper-Transcriptor para GitHub..."

# Verificar que estamos en el directorio correcto
if [ ! -f "transcribir.py" ]; then
    echo "❌ Error: No se encuentra transcribir.py. Ejecutar desde el directorio raíz del proyecto."
    exit 1
fi

# Verificar que git está inicializado
if [ ! -d ".git" ]; then
    echo "❌ Error: Repositorio Git no inicializado. Ejecutar 'git init' primero."
    exit 1
fi

echo "✅ Verificaciones básicas completadas"

# Mostrar estado del repositorio
echo ""
echo "📊 Estado actual del repositorio:"
git status --short

echo ""
echo "📝 Últimos commits:"
git log --oneline -5

echo ""
echo "🎯 Pasos para subir a GitHub:"
echo ""
echo "1. Crear repositorio en GitHub:"
echo "   - Ve a https://github.com/new"
echo "   - Nombre: Video-Whisper-Transcriptor"
echo "   - Descripción: 🎬 Sistema avanzado de transcripción con IA triple motor: OpenAI + Ollama. CUDA optimizado para RTX 5090."
echo "   - Público o privado según preferencia"
echo "   - NO inicializar con README (ya tenemos uno)"
echo ""
echo "2. Conectar repositorio local con GitHub:"
echo "   git remote add origin https://github.com/TU_USUARIO/Video-Whisper-Transcriptor.git"
echo ""
echo "3. Subir código:"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "4. Configurar GitHub Pages (opcional):"
echo "   - Settings > Pages > Source: Deploy from a branch"
echo "   - Branch: main, folder: / (root)"
echo ""

# Mostrar resumen del proyecto
echo "📈 Estadísticas del proyecto:"
echo "   - Archivos de código: $(find . -name '*.py' | wc -l)"
echo "   - Líneas de código Python: $(find . -name '*.py' -exec wc -l {} + | tail -1 | awk '{print $1}')"
echo "   - Archivos de documentación: $(find docs/ -name '*.md' | wc -l)"
echo "   - Tamaño total: $(du -sh . | cut -f1)"

echo ""
echo "🎉 ¡Proyecto listo para GitHub! Sigue los pasos anteriores para completar la subida."