# 🤝 Guía de Contribución

¡Bienvenido! Esta guía te ayudará a contribuir al proyecto Video Whisper-Transcriptor.

## 🎯 Tipos de Contribuciones

Aceptamos diferentes tipos de contribuciones:

### 🐛 Reportes de Bugs
- Errores en transcripción
- Problemas con generación de documentación
- Fallos de instalación
- Problemas de compatibilidad GPU/CUDA

### ✨ Nuevas Funcionalidades
- Nuevos motores de IA
- Mejoras en la interfaz web
- Optimizaciones de rendimiento
- Soporte para nuevos formatos de vídeo

### 📚 Documentación
- Correcciones de typos
- Mejoras en guías de instalación
- Nuevos tutoriales
- Traducciones

### 🔧 Optimizaciones
- Mejoras de velocidad
- Reducción de uso de memoria
- Optimizaciones específicas de GPU

## 🚀 Configuración del Entorno de Desarrollo

### 1. Fork y Clone

```bash
# Fork el repositorio en GitHub
# Luego clona tu fork

git clone https://github.com/tu-usuario/Video-Whisper-Transcriptor.git
cd Video-Whisper-Transcriptor

# Configurar upstream
git remote add upstream https://github.com/original-user/Video-Whisper-Transcriptor.git
```

### 2. Crear Entorno de Desarrollo

```bash
# Crear entorno virtual
python -m venv .venv-dev
source .venv-dev/bin/activate  # Linux/Mac
# .venv-dev\Scripts\activate   # Windows

# Instalar dependencias de desarrollo
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 3. Configurar Pre-commit Hooks

```bash
# Instalar pre-commit
pip install pre-commit

# Configurar hooks
pre-commit install

# Test (opcional)
pre-commit run --all-files
```

## 📝 Proceso de Desarrollo

### 1. Crear Rama de Feature

```bash
# Sincronizar con upstream
git fetch upstream
git checkout main
git merge upstream/main

# Crear nueva rama
git checkout -b feature/nueva-funcionalidad
# o
git checkout -b bugfix/solucionar-problema
# o
git checkout -b docs/mejorar-documentacion
```

### 2. Implementar Cambios

#### Para Código Python

**Estándares de código:**
- Usar PEP 8 para formateo
- Type hints cuando sea posible
- Docstrings para funciones públicas
- Nombres descriptivos para variables

**Ejemplo:**
```python
def generar_documentacion_con_nuevo_motor(
    transcripciones_file: pathlib.Path,
    modelo: str = "nuevo-modelo"
) -> bool:
    """
    Genera documentación usando un nuevo motor de IA.
    
    Args:
        transcripciones_file: Ruta al archivo de transcripciones
        modelo: Nombre del modelo a utilizar
        
    Returns:
        True si la generación fue exitosa, False en caso contrario
        
    Raises:
        FileNotFoundError: Si el archivo de transcripciones no existe
        ConnectionError: Si no se puede conectar al motor de IA
    """
    # Implementación...
    return True
```

#### Para Documentación

**Usar formato Markdown:**
- Títulos descriptivos con emojis
- Bloques de código con sintaxis específica
- Enlaces internos para navegación
- Ejemplos prácticos

#### Para Tests

```python
import pytest
import pathlib
from unittest.mock import Mock, patch

def test_transcribir_video_exitoso():
    """Test de transcripción exitosa"""
    # Arrange
    video_path = pathlib.Path("test_video.mp4")
    
    # Act
    with patch('faster_whisper.WhisperModel') as mock_whisper:
        mock_whisper.return_value.transcribe.return_value = [
            Mock(text="Texto transcrito")
        ]
        resultado = transcribir_video(video_path)
    
    # Assert
    assert resultado is not None
    assert "Texto transcrito" in resultado
```

### 3. Testing

```bash
# Ejecutar todos los tests
pytest

# Tests con coverage
pytest --cov=.

# Test específico
pytest tests/test_transcripcion.py::test_transcribir_video_exitoso

# Test de integración con GPU (requiere CUDA)
pytest tests/test_gpu.py -m gpu
```

### 4. Linting y Formateo

```bash
# Formatear código
black .
isort .

# Verificar estilo
flake8 .

# Type checking
mypy transcribir.py generar_docs.py

# Verificar documentación
pydocstyle .
```

## 📋 Pull Request Guidelines

### 1. Antes de Crear PR

```bash
# Verificar que pasan todos los tests
pytest

# Verificar linting
pre-commit run --all-files

# Actualizar desde upstream
git fetch upstream
git rebase upstream/main

# Push a tu fork
git push origin feature/nueva-funcionalidad
```

### 2. Template de PR

```markdown
## Descripción
Breve descripción de los cambios implementados.

## Tipo de cambio
- [ ] Bug fix (cambio que soluciona un problema)
- [ ] Nueva funcionalidad (cambio que añade funcionalidad)
- [ ] Breaking change (cambio que puede afectar funcionalidad existente)
- [ ] Documentación (cambios solo en documentación)

## ¿Cómo se ha probado?
- [ ] Tests unitarios
- [ ] Tests de integración
- [ ] Prueba manual con GPU RTX 5090
- [ ] Prueba manual con diferentes motores IA

## Checklist
- [ ] Mi código sigue el estilo del proyecto
- [ ] He realizado self-review de mi código
- [ ] He comentado mi código, especialmente en áreas complejas
- [ ] He añadido tests que prueban mi fix/feature
- [ ] Tests nuevos y existentes pasan localmente
- [ ] He actualizado la documentación si es necesario

## Screenshots (si aplica)
[Capturas de pantalla de cambios en UI]

## Información adicional
[Cualquier información adicional relevante]
```

### 3. Criterios de Aprobación

- ✅ Todos los tests pasan
- ✅ Code coverage > 80%
- ✅ Sin errores de linting
- ✅ Documentación actualizada
- ✅ Funcionamiento verificado en al menos una GPU
- ✅ Review de al menos un mantenedor

## 🔍 Áreas que Necesitan Contribuciones

### 🚨 Alta Prioridad

1. **Soporte para más modelos de IA**
   - Integración con Claude
   - Soporte para Llama 3.3
   - Integración con Gemini

2. **Optimizaciones de memoria**
   - Streaming para vídeos largos
   - Procesamiento por chunks
   - Limpieza automática de memoria

3. **Mejoras en la web generada**
   - Diseño responsive
   - Modo oscuro
   - Navegación mejorada

### 🔧 Prioridad Media

1. **Nuevos formatos de entrada**
   - Soporte para audio únicamente
   - Streaming de vídeo (YouTube, etc.)
   - Archivos de subtítulos

2. **Exportación de resultados**
   - PDF de la documentación
   - Exportar a Notion/Obsidian
   - API REST para integración

3. **Interfaz gráfica**
   - GUI con tkinter/PyQt
   - Aplicación web con Flask
   - Aplicación Electron

### 📚 Siempre Bienvenidas

1. **Documentación**
   - Tutoriales específicos
   - Casos de uso reales
   - Troubleshooting específico por GPU

2. **Tests**
   - Tests de integración
   - Tests de performance
   - Tests con diferentes GPUs

3. **Localización**
   - Traducciones de documentación
   - Soporte multi-idioma en UI

## 🎨 Estándares de Código

### Python

```python
# ✅ Bueno
def procesar_transcripciones(
    archivo_entrada: pathlib.Path,
    motor_ia: str = "gpt-4o"
) -> Dict[str, Any]:
    """Procesa transcripciones con el motor de IA especificado."""
    try:
        resultado = {}
        # Procesamiento...
        return resultado
    except Exception as error:
        logger.error(f"Error procesando {archivo_entrada}: {error}")
        raise

# ❌ Evitar
def proc_trans(file, ai):
    res = {}
    # código sin documentar...
    return res
```

### Documentación Markdown

```markdown
# ✅ Bueno
## 🔧 Instalación de CUDA

### Requisitos
- NVIDIA GPU RTX 3060 o superior
- Drivers NVIDIA 525.60.11+

```bash
# Instalar CUDA
wget https://developer.download.nvidia.com/...
```

# ❌ Evitar
## Instalación

Instalar CUDA desde la página web.
```

### Commits

```bash
# ✅ Buenos commits
feat(transcripcion): añadir soporte para archivos MKV
fix(docs): corregir enlaces rotos en manual de instalación
docs(readme): actualizar tabla de compatibilidad GPU
refactor(ai): extraer lógica común de motores IA

# ❌ Commits poco claros
fix stuff
update files
changes
wip
```

## 🏷️ Proceso de Release

### Versionado Semántico

- **MAJOR**: Cambios incompatibles en la API
- **MINOR**: Nueva funcionalidad compatible
- **PATCH**: Bug fixes compatibles

Ejemplo: `1.2.3` → `1.3.0` (nueva funcionalidad)

### Changelog

Mantener `CHANGELOG.md` actualizado:

```markdown
## [1.3.0] - 2025-11-15

### Added
- Soporte para modelo DeepSeek-R1
- Reparación automática de enlaces HTML
- Nuevas métricas de performance

### Fixed
- Error de memoria con vídeos > 2GB
- Enlaces rotos entre páginas web

### Changed
- Mejora en velocidad de transcripción 15%
```

## 🏆 Reconocimientos

### Contributors

Los contribuidores serán añadidos a:
- `README.md` en sección de créditos
- `AUTHORS.md` con detalles de contribuciones
- Release notes para contribuciones significativas

### Tipos de Reconocimiento

- 🐛 **Bug Hunter**: Reportar bugs críticos
- 📚 **Documentarian**: Mejoras significativas en documentación
- ⚡ **Performance Guru**: Optimizaciones importantes
- 🔧 **Feature Creator**: Nuevas funcionalidades
- 🧪 **Test Master**: Cobertura de tests > 90%

## 📞 Obtener Ayuda

### Durante el Desarrollo

- 💬 **GitHub Discussions**: Preguntas generales
- 📞 **Discord** (si disponible): Chat en tiempo real
- 📧 **Email**: Para temas sensibles

### Recursos Útiles

- [Whisper Documentation](https://github.com/openai/whisper)
- [PyTorch CUDA Setup](https://pytorch.org/get-started/locally/)
- [Ollama Documentation](https://github.com/ollama/ollama)
- [OpenAI API Reference](https://platform.openai.com/docs)

---

**¡Gracias por contribuir al proyecto! 🎉**

Tu tiempo y esfuerzo ayudan a hacer este proyecto mejor para toda la comunidad.