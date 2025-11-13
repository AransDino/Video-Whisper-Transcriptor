# 📚 Glosario de Términos

Definiciones y explicaciones de términos técnicos utilizados en el proyecto.

## 🤖 Inteligencia Artificial y Modelos

### **Whisper**
Modelo de transcripción automática de voz a texto desarrollado por OpenAI. Entrenado en 680,000 horas de audio multilingüe, ofrece transcripción robusta y precisa para múltiples idiomas.

**Variantes disponibles:**
- `tiny`: 39 MB, más rápido pero menor precisión
- `small`: 244 MB, equilibrio entre velocidad y precisión  
- `medium`: 769 MB, buena precisión para uso general
- `large`: 1550 MB, alta precisión
- `large-v3`: Última versión optimizada

### **faster-whisper**
Implementación optimizada de Whisper usando CTranslate2. Ofrece:
- 4x más velocidad que la implementación original
- Menor uso de memoria
- Soporte completo para GPU CUDA
- Compatibilidad total con modelos Whisper

### **GPT-4o (OpenAI)**
Modelo de lenguaje multimodal de OpenAI optimizado para conversaciones y tareas de texto. Características:
- Límite de contexto: 128,000 tokens
- Límite de salida configurable hasta 16,384 tokens
- Procesamiento rápido y coherente
- API REST estable

### **GPT-OSS (Ollama)**
Modelo de código abierto compatible con GPT ejecutado localmente via Ollama:
- Tamaño: ~13 GB descargado
- Ejecución completamente local
- Sin límites de tokens por API
- Privacidad total de datos

### **DeepSeek-R1**
Modelo de razonamiento avanzado de DeepSeek ejecutado via Ollama:
- Tamaño: ~5.2 GB
- Especializado en razonamiento paso a paso
- Contexto extendido: 32,768 tokens
- Salida optimizada: 16,384 tokens

## 💻 Hardware y GPU

### **CUDA (Compute Unified Device Architecture)**
Plataforma de computación paralela y API de NVIDIA que permite usar GPUs para computación general:
- Acelera significativamente el procesamiento de audio/vídeo
- Especialmente efectivo para modelos de deep learning
- Requiere GPU NVIDIA compatible

### **RTX 5090**
GPU de alta gama de NVIDIA con especificaciones excepcionales:
- **VRAM**: 31.8 GB GDDR7
- **CUDA Cores**: 21,760
- **Rendimiento**: 7-8x tiempo real en transcripción
- **Compute Capability**: 8.9+

### **VRAM (Video RAM)**
Memoria dedicada de la tarjeta gráfica utilizada para:
- Almacenar modelos de IA (Whisper requiere 1-6 GB según versión)
- Cache de datos durante procesamiento
- Buffers de audio/vídeo temporales

### **Tensor Cores**
Unidades especializadas en GPUs NVIDIA para acelerar operaciones de:
- Multiplicación de matrices
- Inferencia de redes neuronales
- Procesamiento de modelos transformer como Whisper

## 🏗️ Arquitectura del Sistema

### **Motor de IA**
Componente que gestiona la comunicación con un servicio de IA específico:
- **Motor OpenAI**: Conecta con API de OpenAI
- **Motor Ollama**: Conecta con servidor Ollama local
- **Motor DeepSeek**: Especialización de Ollama para DeepSeek-R1

### **Prompt Maestro**
Template unificado que:
- Define la estructura de salida esperada
- Establece el formato HTML requerido
- Mantiene consistencia entre motores
- Incluye instrucciones específicas de formateo

### **Transcripciones Consolidadas**
Archivo de texto que contiene:
- Todas las transcripciones de una sesión de procesamiento
- Formato: `KK-F1-v1: [contenido]`
- Timestamp de procesamiento
- Estadísticas de rendimiento

### **Estructura Web Separada**
Organización de archivos HTML por motor:
```
proyecto/
├── index-openai.html      # Índice OpenAI
├── index-ollama.html      # Índice Ollama  
├── index-deepseek.html    # Índice DeepSeek
└── www/
    ├── openai/           # Fases OpenAI
    ├── ollama/           # Fases Ollama
    └── deepseek/         # Fases DeepSeek
```

## 📄 Formatos y Protocolos

### **Segmentación por Fases**
División del contenido en secciones temáticas:
- **Fase 1**: Introducción y conceptos básicos
- **Fase 2**: Desarrollo técnico detallado  
- **Fase 3**: Ejemplos prácticos y aplicaciones
- **Fase 4**: Conclusiones y próximos pasos

### **Hash de Verificación**
Código único MD5 de 8 caracteres que:
- Identifica respuestas únicas de IA
- Detecta respuestas truncadas o incompletas
- Permite validación de integridad
- Facilita debugging de generación

### **Enlaces Relativos**
Sistema de navegación HTML que:
- Conecta index con archivos de fase
- Mantiene estructura independiente por motor
- Permite navegación local sin servidor web
- Se auto-repara con utilidad `reparar_enlaces.py`

## 🔧 Configuración y Variables

### **Variables de Entorno**
Configuraciones del sistema almacenadas en `.env`:
- `OPENAI_API_KEY`: Clave de autenticación OpenAI
- `WHISPER_MODEL`: Versión de Whisper a utilizar
- `OLLAMA_HOST`: URL del servidor Ollama local
- `*_MAX_TOKENS`: Límites de tokens por motor

### **Compute Type**
Precisión numérica para cálculos GPU:
- `float32`: Máxima precisión, más lento
- `float16`: Equilibrio óptimo velocidad/precisión
- `int8`: Mayor velocidad, menor precisión

### **Temperatura de IA**
Parámetro que controla creatividad vs consistencia:
- `0.0`: Respuestas completamente deterministas
- `0.1`: Ligeramente variable, mantiene consistencia
- `1.0`: Alta creatividad y variabilidad

## 📊 Métricas y Rendimiento

### **Factor de Velocidad**
Ratio entre tiempo real del vídeo y tiempo de transcripción:
- `1x`: Transcripción toma tanto tiempo como duración del vídeo
- `7-8x`: Transcripción 7-8 veces más rápida que tiempo real
- Depende de hardware, modelo y complejidad del audio

### **Tokens**
Unidades de texto procesadas por modelos de IA:
- **Token**: Fragmento de palabra, palabra completa o carácter
- **Límite de contexto**: Máximo tokens de entrada
- **Límite de salida**: Máximo tokens generados
- Aproximadamente: 1 token ≈ 0.75 palabras en español

### **Rate Limiting**
Límites de velocidad impuestos por APIs:
- **OpenAI**: Requests por minuto y tokens por minuto
- **Ollama**: Sin límites (local)
- **Backoff**: Espera automática cuando se alcanzan límites

## 🔍 Debugging y Diagnósticos

### **Logging**
Sistema de registro de eventos del sistema:
- **INFO**: Operaciones normales
- **WARNING**: Situaciones inusuales pero manejables
- **ERROR**: Fallos que impiden operación normal
- **DEBUG**: Información detallada para diagnóstico

### **Truncamiento**
Corte de respuesta de IA debido a límites:
- Detectado por ausencia de etiquetas de cierre HTML
- Activado por límites de tokens o tiempo
- Se maneja con sistema de continuación automática

### **Regex Patterns**
Expresiones regulares para procesamiento de texto:
- Extracción de bloques HTML
- Detección de nombres de archivo
- Corrección de enlaces relativos
- Validación de formato de respuesta

## 🌐 Tecnologías Web

### **HTML Semántico**
Estructura HTML que utiliza:
- Etiquetas semánticamente correctas (`<nav>`, `<main>`, `<section>`)
- Atributos de accesibilidad (`aria-*`, `role`)
- Meta tags para responsividad y SEO
- Enlaces de navegación intuitivos

### **CSS Responsive**
Hojas de estilo que se adaptan a:
- Diferentes tamaños de pantalla
- Dispositivos móviles y desktop
- Modo oscuro y claro
- Distintas resoluciones

### **JavaScript Vanilla**
Funcionalidad interactiva sin frameworks:
- Navegación suave entre secciones
- Animaciones y transiciones
- Mejora progresiva (funciona sin JS)
- Rendimiento optimizado

## 🐍 Python y Dependencias

### **Virtual Environment (venv)**
Entorno aislado de Python que:
- Separa dependencias del sistema
- Evita conflictos entre proyectos
- Permite versiones específicas de paquetes
- Facilita reproducibilidad

### **Requirements.txt**
Archivo que especifica:
- Dependencias exactas del proyecto
- Versiones específicas de paquetes
- Separación entre producción y desarrollo
- Instalación automática con `pip install -r`

### **Pathlib**
Biblioteca moderna de Python para manejo de rutas:
- Sintaxis orientada a objetos
- Compatibilidad multiplataforma
- Operaciones seguras de archivos
- Mejor que `os.path` para proyectos nuevos

---

**💡 Tip**: Si encuentras un término técnico no listado aquí, consulta la [API Reference](API_REFERENCE.md) para detalles técnicos específicos.