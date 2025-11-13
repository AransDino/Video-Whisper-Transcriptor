# 🔍 Solución de Problemas

Guía completa para resolver problemas comunes del sistema Video Whisper-Transcriptor.

## 📋 Diagnóstico Rápido

### Test de Sistema Completo

```bash
# Ejecutar diagnóstico automático
python -c "
import sys, torch, subprocess, os
from pathlib import Path

print('🔍 DIAGNÓSTICO DEL SISTEMA')
print('=' * 50)
print(f'Python: {sys.version}')
print(f'PyTorch: {torch.__version__}')
print(f'CUDA disponible: {torch.cuda.is_available()}')
if torch.cuda.is_available():
    print(f'GPU: {torch.cuda.get_device_name(0)}')
    print(f'VRAM: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB')

# Verificar archivos clave
archivos_clave = ['transcribir.py', 'generar_docs.py', '.env']
for archivo in archivos_clave:
    existe = '✅' if Path(archivo).exists() else '❌'
    print(f'{archivo}: {existe}')

# Verificar Ollama
try:
    result = subprocess.run(['ollama', 'list'], capture_output=True, text=True, timeout=5)
    if result.returncode == 0:
        print('Ollama: ✅')
    else:
        print('Ollama: ❌')
except:
    print('Ollama: ❌ No encontrado')
"
```

## 🚨 Problemas con GPU/CUDA

### Error: CUDA no disponible

**Síntoma:**
```python
>>> import torch
>>> torch.cuda.is_available()
False
```

**Diagnóstico:**
```bash
# Verificar driver NVIDIA
nvidia-smi

# Verificar CUDA
nvcc --version

# Verificar PyTorch CUDA
python -c "import torch; print(torch.version.cuda)"
```

**Soluciones:**

1. **Reinstalar PyTorch con CUDA:**
```bash
pip uninstall torch torchvision torchaudio
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

2. **Verificar compatibilidad CUDA:**
- RTX 5090: CUDA 11.8+ requerido
- RTX 4000: CUDA 11.7+ requerido
- RTX 3000: CUDA 11.0+ requerido

3. **Reinstalar drivers NVIDIA:**
```bash
# Ubuntu
sudo apt purge nvidia-*
sudo apt autoremove
sudo apt install nvidia-driver-525

# Windows: Descargar desde nvidia.com
```

### Error: Out of Memory (OOM)

**Síntoma:**
```
CUDA out of memory. Tried to allocate 2.0 GB (GPU 0; 24.0 GB total capacity...)
```

**Soluciones:**

1. **Reducir batch size en transcripción:**
```python
# En transcribir.py, línea ~850
model = faster_whisper.WhisperModel(
    model_size,
    device="cuda",
    compute_type="float16",
    # Reducir estos valores:
    cpu_threads=2,      # Era 8
    num_workers=1       # Era 2
)
```

2. **Usar modelo más pequeño:**
```python
# Cambiar de large-v3 a medium
model_size = "medium"  # En lugar de "large-v3"
```

3. **Limpiar memoria GPU:**
```bash
# Matar procesos que usen GPU
sudo pkill -f python
nvidia-smi --gpu-reset
```

## 🤖 Problemas con IA

### OpenAI: Rate Limit Exceeded

**Síntoma:**
```
Error 429: Rate limit exceeded
```

**Soluciones:**

1. **Verificar límites de cuenta:**
- Ir a https://platform.openai.com/usage
- Verificar límites de requests por minuto
- Verificar límites de tokens por minuto

2. **Esperar y reintentar:**
```python
# El sistema ya tiene retry automático
# Simplemente esperar 1-2 minutos
```

3. **Configurar límites más conservadores:**
```bash
# En .env
OPENAI_MAX_TOKENS=8192  # Reducir de 16384
OPENAI_TEMPERATURE=0.1  # Mantener bajo
```

### OpenAI: Invalid API Key

**Síntoma:**
```
Error 401: Invalid API key provided
```

**Soluciones:**

1. **Verificar API key:**
```bash
# Verificar que existe en .env
cat .env | grep OPENAI_API_KEY

# Verificar formato
# Debe empezar por sk- y tener ~50 caracteres
```

2. **Regenerar API key:**
- Ir a https://platform.openai.com/api-keys
- Revocar key antigua
- Crear nueva key
- Actualizar .env

### Ollama: Connection Refused

**Síntoma:**
```
Connection refused to localhost:11434
```

**Diagnóstico:**
```bash
# Verificar servicio
ps aux | grep ollama

# Verificar puerto
netstat -an | grep 11434

# Test de conexión
curl http://localhost:11434/api/version
```

**Soluciones:**

1. **Iniciar servicio Ollama:**
```bash
# Matar proceso previo
pkill ollama

# Iniciar en background
ollama serve &

# Verificar que funciona
ollama list
```

2. **Reinstalar Ollama:**
```bash
# Ubuntu
sudo apt remove ollama
curl -fsSL https://ollama.com/install.sh | sh

# Windows/Mac: Descargar desde ollama.ai
```

3. **Verificar modelos:**
```bash
# Verificar modelos descargados
ollama list

# Re-descargar si es necesario
ollama pull gpt-oss
ollama pull deepseek-r1
```

### Ollama: Modelo no disponible

**Síntoma:**
```
Error: model 'gpt-oss' not found
```

**Soluciones:**

1. **Descargar modelo:**
```bash
ollama pull gpt-oss
ollama pull deepseek-r1
```

2. **Verificar espacio en disco:**
```bash
df -h  # Necesario ~15GB para gpt-oss
```

3. **Limpiar modelos viejos:**
```bash
ollama list
ollama rm modelo-viejo
```

## 📁 Problemas con Archivos

### Error: Archivo de vídeo no encontrado

**Síntoma:**
```
FileNotFoundError: No such file or directory: 'videos/video.mp4'
```

**Soluciones:**

1. **Verificar estructura:**
```bash
ls -la videos/
# Debe contener archivos .mp4, .mkv, .avi, etc.
```

2. **Verificar permisos:**
```bash
chmod 755 videos/
chmod 644 videos/*.mp4
```

3. **Verificar nombres de archivo:**
- Sin espacios especiales
- Codificación UTF-8
- Extensiones válidas: .mp4, .avi, .mkv, .mov, .webm

### Error: Permisos insuficientes

**Síntoma:**
```
PermissionError: [Errno 13] Permission denied: 'procesados/'
```

**Soluciones:**

**Linux/Mac:**
```bash
chmod -R 755 .
chown -R $USER:$USER .
```

**Windows:**
```cmd
# Ejecutar terminal como Administrador
icacls . /grant %username%:F /T
```

### Error: Espacio insuficiente

**Síntoma:**
```
OSError: [Errno 28] No space left on device
```

**Soluciones:**

1. **Verificar espacio:**
```bash
df -h  # Linux/Mac
dir C:\  # Windows
```

2. **Limpiar archivos temporales:**
```bash
# Eliminar transcripciones antiguas
rm -rf procesados/transcripciones_*.txt

# Limpiar cache de modelos
rm -rf ~/.cache/huggingface/
```

3. **Mover a disco con más espacio:**
```bash
# Crear symlink a disco grande
mv Video-Whisper-Transcriptor /path/to/big/disk/
ln -s /path/to/big/disk/Video-Whisper-Transcriptor .
```

## 🌐 Problemas con Generación Web

### Enlaces rotos entre páginas

**Síntoma:**
Los enlaces no funcionan entre index y páginas de fases.

**Soluciones:**

1. **Ejecutar reparador de enlaces:**
```bash
python reparar_enlaces.py
```

2. **Verificar estructura:**
```bash
ls -la www/
ls -la www/openai/
ls -la www/ollama/
ls -la www/deepseek/
```

3. **Regenerar documentación:**
```bash
python generar_docs.py
# Seleccionar opción 4 (TODOS) para regenerar
```

### JavaScript no funciona

**Síntoma:**
Los cuestionarios no se corrigen automáticamente.

**Soluciones:**

1. **Verificar JavaScript en navegador:**
- Abrir herramientas de desarrollador (F12)
- Verificar errores en consola
- Comprobar que JavaScript está habilitado

2. **Verificar archivos HTML:**
```bash
grep -n "<script>" www/*/fase-*.html
# Debe mostrar JavaScript al final de cada archivo
```

### CSS no se aplica

**Síntoma:**
Las páginas se ven sin estilos.

**Soluciones:**

1. **Verificar estilos integrados:**
```bash
grep -n "<style>" index-*.html
# Los estilos deben estar integrados en el HTML
```

2. **Abrir en navegador diferente:**
- Chrome/Firefox/Safari
- Modo incógnito para evitar cache

## 🔧 Problemas de Instalación

### Error: pip install failed

**Síntoma:**
```
ERROR: Failed building wheel for some-package
```

**Soluciones:**

1. **Actualizar herramientas:**
```bash
pip install --upgrade pip setuptools wheel
```

2. **Instalar dependencias de sistema:**

**Ubuntu:**
```bash
sudo apt update
sudo apt install build-essential python3-dev ffmpeg
```

**macOS:**
```bash
xcode-select --install
brew install ffmpeg
```

**Windows:**
```bash
# Instalar Visual Studio Build Tools
# Descargar desde: https://visualstudio.microsoft.com/downloads/
```

3. **Usar conda en lugar de pip:**
```bash
conda create -n whisper python=3.10
conda activate whisper
conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia
pip install -r requirements.txt
```

### Error: Python versión incorrecta

**Síntoma:**
```
Python 3.8.x is not supported. Please use Python 3.10+
```

**Soluciones:**

1. **Instalar Python correcto:**

**Ubuntu:**
```bash
sudo apt install python3.10 python3.10-venv python3.10-dev
python3.10 -m venv .venv
```

**Windows:**
- Descargar Python 3.10+ desde python.org
- Marcar "Add to PATH"

**macOS:**
```bash
brew install python@3.10
```

2. **Usar pyenv:**
```bash
# Instalar pyenv
curl https://pyenv.run | bash

# Instalar Python 3.10
pyenv install 3.10.11
pyenv local 3.10.11
```

## 📞 Obtener Ayuda

### Información para reportar problemas

Cuando reportes un problema, incluye:

```bash
# Información del sistema
python --version
pip freeze > requirements-actual.txt
cat requirements-actual.txt

# Información GPU
nvidia-smi

# Logs de error
tail -50 procesados/registro_transcripciones.txt

# Configuración
cat .env | grep -v "sk-"  # Sin mostrar API keys
```

### Crear Issue en GitHub

1. Ir a: https://github.com/tu-usuario/Video-Whisper-Transcriptor/issues
2. Crear "New Issue"
3. Usar template:

```markdown
**Descripción del problema:**
[Describe qué esperabas que pasara y qué pasó realmente]

**Pasos para reproducir:**
1. 
2. 
3. 

**Información del sistema:**
- OS: [Windows 11/Ubuntu 22.04/macOS 13]
- Python: [3.10.x]
- GPU: [RTX 5090/RTX 4080/etc]
- CUDA: [11.8]

**Logs de error:**
```
[Pegar logs aquí]
```

**¿Funcionaba antes?**
[Sí/No - si sí, ¿qué cambió?]
```

### Canales de soporte

- 🐛 **Bugs**: GitHub Issues
- 💬 **Preguntas**: GitHub Discussions
- 📖 **Documentación**: Wiki del repositorio
- 🚀 **Nuevas funciones**: GitHub Issues con label "enhancement"

---

**📌 Siguiente paso**: [Contribuir al proyecto](CONTRIBUTING.md)