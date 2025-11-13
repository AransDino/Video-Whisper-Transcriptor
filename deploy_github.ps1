# 🚀 Script de Deploy a GitHub
# Ejecutar: .\deploy_github.ps1

Write-Host "🚀 Preparando Video Whisper-Transcriptor para GitHub..." -ForegroundColor Cyan

# Verificar que estamos en el directorio correcto
if (-not (Test-Path "transcribir.py")) {
    Write-Host "❌ Error: No se encuentra transcribir.py. Ejecutar desde el directorio raíz del proyecto." -ForegroundColor Red
    exit 1
}

# Verificar que git está inicializado
if (-not (Test-Path ".git")) {
    Write-Host "❌ Error: Repositorio Git no inicializado. Ejecutar 'git init' primero." -ForegroundColor Red
    exit 1
}

Write-Host "✅ Verificaciones básicas completadas" -ForegroundColor Green

# Mostrar estado del repositorio
Write-Host "`n📊 Estado actual del repositorio:" -ForegroundColor Yellow
git status --short

Write-Host "`n📝 Últimos commits:" -ForegroundColor Yellow
git log --oneline -5

Write-Host "`n🎯 Pasos para subir a GitHub:" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Crear repositorio en GitHub:" -ForegroundColor White
Write-Host "   - Ve a https://github.com/new" -ForegroundColor Gray
Write-Host "   - Nombre: Video-Whisper-Transcriptor" -ForegroundColor Gray
Write-Host "   - Descripción: 🎬 Sistema avanzado de transcripción con IA triple motor: OpenAI + Ollama. CUDA optimizado para RTX 5090." -ForegroundColor Gray
Write-Host "   - Público o privado según preferencia" -ForegroundColor Gray
Write-Host "   - NO inicializar con README (ya tenemos uno)" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Conectar repositorio local con GitHub:" -ForegroundColor White
Write-Host "   git remote add origin https://github.com/TU_USUARIO/Video-Whisper-Transcriptor.git" -ForegroundColor Yellow
Write-Host ""
Write-Host "3. Subir código:" -ForegroundColor White
Write-Host "   git branch -M main" -ForegroundColor Yellow
Write-Host "   git push -u origin main" -ForegroundColor Yellow
Write-Host ""
Write-Host "4. Configurar GitHub Pages (opcional):" -ForegroundColor White
Write-Host "   - Settings > Pages > Source: Deploy from a branch" -ForegroundColor Gray
Write-Host "   - Branch: main, folder: / (root)" -ForegroundColor Gray
Write-Host ""

# Mostrar resumen del proyecto
Write-Host "📈 Estadísticas del proyecto:" -ForegroundColor Green
$pythonFiles = (Get-ChildItem -Recurse -Filter "*.py" | Measure-Object).Count
$docFiles = (Get-ChildItem -Path "docs" -Filter "*.md" | Measure-Object).Count
$totalSize = (Get-ChildItem -Recurse | Measure-Object -Property Length -Sum).Sum
$totalSizeMB = [math]::Round($totalSize / 1MB, 2)

Write-Host "   - Archivos de código Python: $pythonFiles" -ForegroundColor White
Write-Host "   - Archivos de documentación: $docFiles" -ForegroundColor White
Write-Host "   - Tamaño total: $totalSizeMB MB" -ForegroundColor White

Write-Host "`n🎉 ¡Proyecto listo para GitHub! Sigue los pasos anteriores para completar la subida." -ForegroundColor Green
Write-Host ""

# Opción para abrir GitHub en el navegador
$openGitHub = Read-Host "¿Quieres abrir GitHub en el navegador para crear el repositorio? (y/n)"
if ($openGitHub -eq "y" -or $openGitHub -eq "Y") {
    Start-Process "https://github.com/new"
    Write-Host "🌐 Abriendo GitHub en el navegador..." -ForegroundColor Cyan
}