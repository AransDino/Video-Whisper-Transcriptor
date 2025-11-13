# 🔧 API Reference

Documentación técnica completa de las funciones y módulos del sistema.

## 📋 Tabla de Contenidos

- [Módulo Principal (`transcribir.py`)](#módulo-principal-transcribirpy)
- [Menús de Documentación](#menús-de-documentación)
- [Utilidades](#utilidades)
- [Configuración](#configuración)
- [Tipos de Datos](#tipos-de-datos)

## 📄 Módulo Principal (`transcribir.py`)

### Funciones de Transcripción

#### `transcribir_video(video_path: pathlib.Path, model: WhisperModel) -> str`

Transcribe un archivo de vídeo individual.

**Parámetros:**
- `video_path`: Ruta al archivo de vídeo
- `model`: Modelo de Whisper inicializado

**Retorna:**
- `str`: Texto transcrito del vídeo

**Excepciones:**
- `FileNotFoundError`: Si el archivo de vídeo no existe
- `RuntimeError`: Si falla la transcripción

**Ejemplo:**
```python
from faster_whisper import WhisperModel
import pathlib

model = WhisperModel("large-v3", device="cuda")
video_path = pathlib.Path("videos/mi_video.mp4")
texto = transcribir_video(video_path, model)
print(texto)
```

#### `procesar_todos_los_videos() -> bool`

Procesa todos los vídeos en la carpeta de vídeos.

**Retorna:**
- `bool`: True si el procesamiento fue exitoso

**Ejemplo:**
```python
if procesar_todos_los_videos():
    print("Todos los vídeos procesados correctamente")
```

### Funciones de Generación de Documentación

#### `crear_prompt_maestro_original(transcripciones_consolidadas: str) -> str`

Crea el prompt maestro unificado para todos los motores de IA.

**Parámetros:**
- `transcripciones_consolidadas`: Texto consolidado de todas las transcripciones

**Retorna:**
- `str`: Prompt formateado para enviar a la IA

**Ejemplo:**
```python
transcripciones = "KK-F1-v1: Texto del vídeo..."
prompt = crear_prompt_maestro_original(transcripciones)
```

#### `generar_documentacion_con_openai(transcripciones_file: pathlib.Path) -> bool`

Genera documentación usando OpenAI GPT-4o.

**Parámetros:**
- `transcripciones_file`: Ruta al archivo de transcripciones consolidadas

**Retorna:**
- `bool`: True si la generación fue exitosa

**Excepciones:**
- `openai.AuthenticationError`: API key inválida
- `openai.RateLimitError`: Límite de rate alcanzado

**Ejemplo:**
```python
archivo = pathlib.Path("procesados/transcripciones_20251113.txt")
if generar_documentacion_con_openai(archivo):
    print("Documentación OpenAI generada")
```

#### `generar_documentacion_con_ollama(transcripciones_file: pathlib.Path) -> bool`

Genera documentación usando Ollama con GPT-OSS.

**Parámetros:**
- `transcripciones_file`: Ruta al archivo de transcripciones

**Retorna:**
- `bool`: True si la generación fue exitosa

**Excepciones:**
- `ConnectionError`: No se puede conectar a Ollama
- `RuntimeError`: Error durante la generación

#### `generar_documentacion_con_deepseek(transcripciones_file: pathlib.Path) -> bool`

Genera documentación usando Ollama con DeepSeek-R1.

**Parámetros:**
- `transcripciones_file`: Ruta al archivo de transcripciones

**Retorna:**
- `bool`: True si la generación fue exitosa

### Funciones de Procesamiento HTML

#### `procesar_y_guardar_html(contenido_respuesta: str, carpeta_base: pathlib.Path, carpeta_www: pathlib.Path, motor: str) -> bool`

Extrae y guarda los archivos HTML de la respuesta de IA.

**Parámetros:**
- `contenido_respuesta`: Respuesta completa del motor de IA
- `carpeta_base`: Directorio base para archivos index
- `carpeta_www`: Directorio para archivos de fases
- `motor`: Nombre del motor ("openai", "ollama", "deepseek")

**Retorna:**
- `bool`: True si el procesamiento fue exitoso

#### `actualizar_enlaces_html(codigo_html: str, motor: str, nombre_archivo: str) -> str`

Actualiza los enlaces del HTML según el motor y estructura de carpetas.

**Parámetros:**
- `codigo_html`: Código HTML a procesar
- `motor`: Nombre del motor
- `nombre_archivo`: Nombre del archivo HTML

**Retorna:**
- `str`: HTML con enlaces corregidos

### Funciones de Validación

#### `validar_respuesta_completa(contenido_respuesta: str, transcripciones_content: str) -> bool`

Valida que la respuesta de IA sea completa.

**Parámetros:**
- `contenido_respuesta`: Respuesta del motor de IA
- `transcripciones_content`: Contenido de transcripciones original

**Retorna:**
- `bool`: True si la respuesta está completa

### Funciones de Utilidad

#### `recopilar_estadisticas_video(video_path: pathlib.Path, duracion_transcripcion: float, caracteres_transcripcion: int) -> dict`

Recopila estadísticas de procesamiento de un vídeo.

**Parámetros:**
- `video_path`: Ruta al archivo de vídeo
- `duracion_transcripcion`: Tiempo de transcripción en segundos
- `caracteres_transcripcion`: Número de caracteres transcritos

**Retorna:**
- `dict`: Diccionario con estadísticas completas

## 🎮 Menús de Documentación

### `generar_docs.py`

Menú principal para generación de documentación.

#### Funciones principales:

```python
def mostrar_banner() -> None:
    """Muestra el banner del sistema"""

def verificar_configuracion() -> tuple[bool, bool]:
    """
    Verifica configuración de OpenAI y Ollama
    
    Returns:
        tuple: (openai_disponible, ollama_disponible)
    """

def listar_transcripciones() -> list[pathlib.Path]:
    """
    Lista archivos de transcripciones disponibles
    
    Returns:
        list: Lista de rutas a archivos de transcripciones
    """
```

### Scripts Individuales

#### `generar_docs_openai.py`
```python
def main() -> None:
    """Ejecuta generación solo con OpenAI"""
```

#### `generar_docs_ollama.py`
```python
def main() -> None:
    """Ejecuta generación solo con Ollama GPT-OSS"""
```

#### `generar_docs_deepseek.py`
```python
def main() -> None:
    """Ejecuta generación solo con DeepSeek-R1"""
```

## 🔧 Utilidades (`reparar_enlaces.py`)

### `reparar_enlaces_index(archivo_index: pathlib.Path, motor: str) -> bool`

Repara enlaces en archivo index.

**Parámetros:**
- `archivo_index`: Ruta al archivo index
- `motor`: Nombre del motor

**Retorna:**
- `bool`: True si se repararon enlaces

### `reparar_enlaces_fases(carpeta_motor: pathlib.Path, motor: str) -> int`

Repara enlaces en archivos de fases.

**Parámetros:**
- `carpeta_motor`: Carpeta con archivos de fases
- `motor`: Nombre del motor

**Retorna:**
- `int`: Número de archivos reparados

## ⚙️ Configuración

### Variables de Entorno

```python
# OpenAI
OPENAI_API_KEY: str = "sk-..."
OPENAI_MODEL: str = "gpt-4o"
OPENAI_MAX_TOKENS: int = 16384
OPENAI_TEMPERATURE: float = 0.1

# Ollama
OLLAMA_HOST: str = "http://localhost:11434"
OLLAMA_MODEL: str = "gpt-oss"
DEEPSEEK_MODEL: str = "deepseek-r1:latest"

# Whisper
WHISPER_MODEL: str = "large-v3"
WHISPER_COMPUTE_TYPE: str = "float16"
WHISPER_DEVICE: str = "cuda"
WHISPER_CPU_THREADS: int = 8
WHISPER_NUM_WORKERS: int = 2

# Directorios
VIDEOS_DIR: str = "videos"
PROCESADOS_DIR: str = "procesados"
WWW_DIR: str = "www"
MODELS_CACHE_DIR: str = "models_cache"
```

### Funciones de Configuración

```python
def cargar_configuracion() -> dict:
    """
    Carga configuración desde variables de entorno y .env
    
    Returns:
        dict: Configuración completa del sistema
    """

def verificar_gpu() -> bool:
    """
    Verifica disponibilidad de GPU CUDA
    
    Returns:
        bool: True si CUDA está disponible
    """

def inicializar_whisper(modelo: str = "large-v3") -> WhisperModel:
    """
    Inicializa modelo Whisper con configuración óptima
    
    Args:
        modelo: Nombre del modelo Whisper
        
    Returns:
        WhisperModel: Modelo inicializado
    """
```

## 📊 Tipos de Datos

### Estructuras de Datos

```python
from typing import TypedDict, Optional
from pathlib import Path

class EstadisticasVideo(TypedDict):
    """Estadísticas de procesamiento de vídeo"""
    archivo: str
    tamaño_mb: float
    duracion_segundos: float
    tiempo_transcripcion: float
    velocidad_factor: float
    caracteres_transcritos: int
    palabras_estimadas: int

class ConfiguracionMotor(TypedDict):
    """Configuración para motor de IA"""
    nombre: str
    tipo: str  # "openai" | "ollama"
    modelo: str
    parametros: dict

class ResultadoTranscripcion(TypedDict):
    """Resultado de transcripción"""
    exito: bool
    archivo_entrada: Path
    archivo_salida: Optional[Path]
    texto_transcrito: str
    estadisticas: EstadisticasVideo
    errores: list[str]
```

### Enums

```python
from enum import Enum

class TipoMotor(Enum):
    """Tipos de motores de IA disponibles"""
    OPENAI = "openai"
    OLLAMA = "ollama"
    DEEPSEEK = "deepseek"

class EstadoProcesamiento(Enum):
    """Estados de procesamiento"""
    PENDIENTE = "pendiente"
    PROCESANDO = "procesando"
    COMPLETADO = "completado"
    ERROR = "error"

class CalidadTranscripcion(Enum):
    """Niveles de calidad de transcripción"""
    RAPIDA = "small"
    NORMAL = "medium"
    ALTA = "large"
    MAXIMA = "large-v3"
```

## 🐞 Debugging y Logging

### Funciones de Debug

```python
def activar_debug() -> None:
    """Activa modo debug con logging detallado"""

def generar_hash_respuesta(contenido: str) -> str:
    """
    Genera hash único para verificar respuestas
    
    Args:
        contenido: Contenido de la respuesta
        
    Returns:
        str: Hash MD5 de 8 caracteres
    """

def medir_tiempo_ejecucion(func):
    """
    Decorator para medir tiempo de ejecución
    
    Usage:
        @medir_tiempo_ejecucion
        def mi_funcion():
            pass
    """
```

### Logging

```python
import logging

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('transcripcion.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
```

## 🧪 Testing

### Funciones de Test

```python
def test_transcribir_video_exitoso():
    """Test de transcripción exitosa"""

def test_generar_documentacion_openai():
    """Test de generación con OpenAI"""

def test_generar_documentacion_ollama():
    """Test de generación con Ollama"""

def test_procesar_html():
    """Test de procesamiento de HTML"""

def test_reparar_enlaces():
    """Test de reparación de enlaces"""
```

### Fixtures

```python
import pytest
from pathlib import Path

@pytest.fixture
def video_test():
    """Video de prueba para tests"""
    return Path("tests/fixtures/video_test.mp4")

@pytest.fixture
def transcripcion_test():
    """Transcripción de prueba"""
    return "KK-F1-v1: Contenido de prueba..."

@pytest.fixture
def mock_openai():
    """Mock de OpenAI para tests"""
    with patch('openai.ChatCompletion.create') as mock:
        mock.return_value.choices[0].message.content = "Respuesta test"
        yield mock
```

---

**📌 Para más ejemplos prácticos, consulta**: [Manual de Uso](USAGE.md)