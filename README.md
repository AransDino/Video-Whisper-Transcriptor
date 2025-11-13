# 🎯 Video Whisper-Transcriptor

Sistema integral de transcripción de vídeos con IA y generación automática de documentación educativa interactiva.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![CUDA](https://img.shields.io/badge/CUDA-RTX_5090-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🚀 Características Principales

- **🎬 Transcripción de vídeos** con Whisper optimizado para CUDA RTX 5090
- **🤖 Generación automática de documentación** con 3 motores de IA:
  - OpenAI GPT-4o (nube, máxima calidad)
  - Ollama GPT-OSS (local, gratuito)
  - Ollama DeepSeek-R1 (local, gratuito, eficiente)
- **📚 Web educativa interactiva** con cuestionarios y navegación
- **⚡ Alto rendimiento**: 7-8x velocidad real en RTX 5090
- **🔄 Sistema modular** con menús independientes

## 📁 Estructura del Proyecto

```
Video Whisper-Transcriptor/
├── 📄 transcribir.py              # Script principal de transcripción
├── 🎮 generar_docs.py            # Menú principal de documentación
├── 📝 generar_docs_openai.py     # Motor OpenAI individual
├── 📝 generar_docs_ollama.py     # Motor Ollama GPT-OSS individual
├── 📝 generar_docs_deepseek.py   # Motor DeepSeek-R1 individual
├── 🔧 reparar_enlaces.py         # Utilidad para reparar enlaces HTML
├── 📊 requirements.txt           # Dependencias Python
├── ⚙️ .env.example               # Variables de entorno (ejemplo)
├── 📂 videos/                    # Carpeta de vídeos a procesar
├── 📂 procesados/                # Transcripciones y análisis generados
├── 📂 www/                       # Documentación web generada
│   ├── 📂 openai/               # HTML generado por OpenAI
│   ├── 📂 ollama/               # HTML generado por Ollama GPT-OSS
│   └── 📂 deepseek/             # HTML generado por DeepSeek-R1
└── 📚 docs/                      # Documentación del proyecto
    ├── 📄 INSTALLATION.md       # Guía de instalación completa
    ├── 📄 USAGE.md               # Manual de uso
    ├── 📄 API_REFERENCE.md       # Referencia de funciones
    ├── 📄 TROUBLESHOOTING.md     # Solución de problemas
    └── 📄 CONTRIBUTING.md        # Guía de contribución
```

## 🚀 Instalación Rápida

### 1. Requisitos del Sistema
- **Python 3.10+**
- **NVIDIA GPU** (RTX 5090 recomendada, pero funciona con otras)
- **CUDA 11.8+** instalado
- **16GB+ RAM** recomendado

### 2. Clonación e Instalación
```bash
git clone https://github.com/tu-usuario/Video-Whisper-Transcriptor.git
cd Video-Whisper-Transcriptor

# Crear entorno virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Instalar dependencias
pip install -r requirements.txt
```

### 3. Configuración
```bash
# Copiar archivo de configuración
cp .env.example .env

# Editar .env con tus claves API
nano .env
```

### 4. Primera Ejecución
```bash
# Transcribir vídeos
python transcribir.py

# Generar documentación
python generar_docs.py
```

## 📖 Documentación Completa

| Documento | Descripción |
|-----------|-------------|
| [📄 Instalación](docs/INSTALLATION.md) | Guía detallada de instalación paso a paso |
| [📄 Manual de Uso](docs/USAGE.md) | Cómo usar todas las funcionalidades |
| [📄 Referencia API](docs/API_REFERENCE.md) | Documentación técnica de funciones |
| [📄 Solución de Problemas](docs/TROUBLESHOOTING.md) | Errores comunes y soluciones |
| [📄 Contribuir](docs/CONTRIBUTING.md) | Cómo contribuir al proyecto |

## ⚡ Rendimiento

| Motor | Velocidad | Calidad | Coste | Tipo |
|-------|-----------|---------|-------|------|
| **DeepSeek-R1** | ~2 min | ⭐⭐⭐⭐⭐ | Gratis | Local |
| **GPT-OSS** | ~1 min | ⭐⭐⭐⭐ | Gratis | Local |
| **OpenAI GPT-4o** | ~2 min | ⭐⭐⭐⭐⭐ | $0.10-0.30 | Nube |

*Tiempos aproximados para 30 min de vídeo en RTX 5090*

## 🎯 Casos de Uso

- **📚 Formación empresarial**: Convertir seminarios en material educativo
- **🏥 Documentación médica**: Transcribir consultas y generar guías
- **🎓 Contenido educativo**: Crear cursos interactivos desde vídeos
- **📊 Análisis de reuniones**: Transcribir y documentar decisiones

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Lee la [guía de contribución](docs/CONTRIBUTING.md) para empezar.

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver [LICENSE](LICENSE) para más detalles.

## ⭐ Soporte

Si este proyecto te resulta útil, ¡considera darle una estrella! ⭐

---

**Desarrollado con ❤️ para automatizar la creación de contenido educativo**