# 📄 Guía de Instalación Completa

Esta guía te llevará paso a paso por la instalación completa del sistema Video Whisper-Transcriptor.

## 📋 Tabla de Contenidos

1. [Requisitos del Sistema](#requisitos-del-sistema)
2. [Instalación de Dependencias](#instalación-de-dependencias)
3. [Configuración del Proyecto](#configuración-del-proyecto)
4. [Configuración de IA](#configuración-de-ia)
5. [Verificación de Instalación](#verificación-de-instalación)
6. [Problemas Comunes](#problemas-comunes)

## 🖥️ Requisitos del Sistema

### Hardware Mínimo
- **CPU**: Intel i5 4ta gen o AMD Ryzen 5 equivalente
- **RAM**: 8GB (16GB recomendado)
- **GPU**: NVIDIA GTX 1060 6GB o superior
- **Almacenamiento**: 10GB libres

### Hardware Recomendado
- **CPU**: Intel i7/i9 o AMD Ryzen 7/9
- **RAM**: 32GB
- **GPU**: NVIDIA RTX 5090 (óptimo) / RTX 4080+ (excelente)
- **Almacenamiento**: SSD NVMe con 50GB libres

### Software Base
- **OS**: Windows 10/11, Ubuntu 20.04+, macOS 12+
- **Python**: 3.10 o superior
- **Git**: Para clonar el repositorio

## 🔧 Instalación de Dependencias

### 1. Instalar CUDA (NVIDIA GPU)

#### Windows
```bash
# Descargar e instalar CUDA 11.8 desde:
# https://developer.nvidia.com/cuda-11-8-0-download-archive

# Verificar instalación
nvcc --version
nvidia-smi
```

#### Ubuntu
```bash
# Instalar CUDA
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-ubuntu2004.pin
sudo mv cuda-ubuntu2004.pin /etc/apt/preferences.d/cuda-repository-pin-600
sudo apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/3bf863cc.pub
sudo add-apt-repository "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/ /"
sudo apt-get update
sudo apt-get -y install cuda-11-8

# Agregar a PATH
echo 'export PATH=/usr/local/cuda-11.8/bin:$PATH' >> ~/.bashrc
echo 'export LD_LIBRARY_PATH=/usr/local/cuda-11.8/lib64:$LD_LIBRARY_PATH' >> ~/.bashrc
source ~/.bashrc
```

### 2. Instalar Python 3.10+

#### Windows
```bash
# Descargar desde https://www.python.org/downloads/
# Asegurar "Add to PATH" está marcado

# Verificar
python --version
pip --version
```

#### Ubuntu
```bash
sudo apt update
sudo apt install python3.10 python3.10-venv python3.10-dev python3-pip
```

#### macOS
```bash
# Con Homebrew
brew install python@3.10

# O con pyenv
pyenv install 3.10.11
pyenv global 3.10.11
```

## 📦 Configuración del Proyecto

### 1. Clonar Repositorio

```bash
git clone https://github.com/tu-usuario/Video-Whisper-Transcriptor.git
cd Video-Whisper-Transcriptor
```

### 2. Crear Entorno Virtual

#### Windows
```cmd
python -m venv .venv
.venv\Scripts\activate
```

#### Linux/macOS
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar Dependencias Python

```bash
# Actualizar pip
pip install --upgrade pip

# Instalar dependencias principales
pip install -r requirements.txt

# Para desarrollo (opcional)
pip install -r requirements-dev.txt
```

### 4. Verificar Instalación PyTorch CUDA

```bash
python -c "import torch; print(f'CUDA disponible: {torch.cuda.is_available()}'); print(f'GPU: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"No detectada\"}')"
```

**Salida esperada:**
```
CUDA disponible: True
GPU: NVIDIA GeForce RTX 5090
```

## 🤖 Configuración de IA

### 1. OpenAI (Opcional pero Recomendado)

```bash
# Copiar archivo de configuración
cp .env.example .env
```

Editar `.env`:
```bash
# API Keys
OPENAI_API_KEY=sk-tu-clave-aqui

# Configuración OpenAI
OPENAI_MODEL=gpt-4o
OPENAI_MAX_TOKENS=16384
OPENAI_TEMPERATURE=0.1
```

### 2. Ollama (Local, Gratuito)

#### Instalación Ollama

**Windows/macOS:**
- Descargar desde: https://ollama.ai/
- Ejecutar instalador

**Ubuntu:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

#### Instalar Modelos

```bash
# Modelo GPT-OSS (13GB)
ollama pull gpt-oss

# Modelo DeepSeek-R1 (5.2GB)
ollama pull deepseek-r1

# Verificar modelos instalados
ollama list
```

## ✅ Verificación de Instalación

### 1. Test de GPU

```bash
python -c "
import torch
print(f'PyTorch versión: {torch.__version__}')
print(f'CUDA disponible: {torch.cuda.is_available()}')
if torch.cuda.is_available():
    print(f'GPU: {torch.cuda.get_device_name(0)}')
    print(f'VRAM: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB')
"
```

### 2. Test de Whisper

```bash
python -c "
try:
    import faster_whisper
    print('✅ faster-whisper instalado correctamente')
except ImportError:
    print('❌ Error: faster-whisper no encontrado')
"
```

### 3. Test de Ollama

```bash
# Verificar servicio
ollama serve &
sleep 5

# Test simple
ollama run gpt-oss "Hola, ¿funcionas correctamente?"
```

### 4. Test del Sistema

```bash
# Test completo del sistema
python transcribir.py --test

# Debería mostrar:
# ✅ CUDA GPU detectada
# ✅ Whisper inicializado
# ✅ Sistema listo para transcripción
```

## 🚨 Problemas Comunes

### Error: CUDA no detectada

**Problema**: `CUDA disponible: False`

**Solución**:
```bash
# Verificar drivers NVIDIA
nvidia-smi

# Reinstalar PyTorch con CUDA
pip uninstall torch torchvision torchaudio
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### Error: Out of Memory

**Problema**: `CUDA out of memory`

**Solución**:
```python
# En transcribir.py, reducir batch_size
model = faster_whisper.WhisperModel(
    model_size,
    device="cuda",
    compute_type="float16",
    download_root=models_cache,
    # Reducir estos valores:
    cpu_threads=4,           # Era 8
    num_workers=1            # Era 2
)
```

### Error: Ollama no responde

**Problema**: `Connection refused to localhost:11434`

**Solución**:
```bash
# Reiniciar servicio Ollama
pkill ollama
ollama serve

# En otra terminal
ollama list
```

### Error: Permisos en Windows

**Problema**: `Permission denied`

**Solución**:
```cmd
# Ejecutar terminal como Administrador
# O cambiar permisos de la carpeta
icacls "Video-Whisper-Transcriptor" /grant %username%:F /T
```

## 🔄 Actualización

```bash
# Obtener últimos cambios
git pull origin main

# Actualizar dependencias
pip install -r requirements.txt --upgrade

# Verificar funcionamiento
python transcribir.py --test
```

## 📞 Soporte

Si encuentras problemas no cubiertos aquí:

1. Consulta [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. Busca en [Issues de GitHub](https://github.com/tu-usuario/Video-Whisper-Transcriptor/issues)
3. Crea un nuevo issue con:
   - Descripción del problema
   - Pasos para reproducir
   - Logs de error
   - Información del sistema (`python --version`, `nvidia-smi`)

---

**📌 Siguiente paso**: [Manual de Uso](USAGE.md)