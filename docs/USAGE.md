# 📚 Manual de Uso

Guía completa para usar todas las funcionalidades del sistema Video Whisper-Transcriptor.

## 🎯 Flujo de Trabajo Completo

1. **Preparar vídeos** → Copiar a carpeta `videos/`
2. **Transcribir** → Ejecutar `transcribir.py`
3. **Generar documentación** → Ejecutar `generar_docs.py`
4. **Revisar resultados** → Abrir archivos HTML generados

## 🎬 Transcripción de Vídeos

### Preparar Vídeos

```bash
# Estructura recomendada de nombres
videos/
├── KK-F1-v1-Introduccion_a_la_IA.mp4
├── KK-F1-v2-Chatbots_vs_IA.mp4
├── KK-F2-v1-Navegacion_sistema.mp4
└── KK-F2-v2-Gestion_agenda.mp4
```

**Nomenclatura importante:**
- `KK` = Prefijo del proyecto (Klinikare)
- `F1, F2, F3` = Número de fase
- `v1, v2, v3` = Número de vídeo dentro de la fase

### Ejecutar Transcripción

```bash
# Activar entorno virtual
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Transcribir todos los vídeos
python transcribir.py
```

### Opciones de Transcripción

**Menú interactivo:**
```
🎬 TRANSCRIPTOR DE VÍDEOS KLINIKARE / CLINIQQUER 🎬

📂 Vídeos encontrados: 4 archivos
💾 Total: 156.3 MB

🎮 OPCIONES:
   1. 🚀 Procesar TODOS los vídeos
   2. 📝 Seleccionar vídeos específicos
   3. 🔄 Solo vídeos nuevos
   0. 🚪 Salir

👆 Elige una opción:
```

**Configuraciones disponibles:**
- **Modelo Whisper**: large-v3 (recomendado), medium, small
- **Idioma**: Auto-detección o español específico
- **Calidad**: float16 (rápido) o float32 (máxima calidad)

### Resultados de Transcripción

Los archivos se guardan en `procesados/`:

```
procesados/
├── transcripciones_20251113_192357.txt    # Transcripciones consolidadas
├── registro_transcripciones.txt           # Log detallado
├── estadisticas_transcripcion.json        # Métricas de rendimiento
└── transcripciones_individuales/          # Archivos por vídeo
    ├── KK-F1-v1-Introduccion_a_la_IA.txt
    └── KK-F1-v2-Chatbots_vs_IA.txt
```

## 🤖 Generación de Documentación

### Menú Principal

```bash
python generar_docs.py
```

**Opciones disponibles:**
```
🎮 MENÚ DE OPCIONES:

   1. 🌐 Generar con OpenAI GPT-4o (nube)
   2. 🏠 Generar con Ollama GPT-OSS (local)
   3. 🧠 Generar con Ollama DeepSeek-R1 (local)
   4. 🔄 Generar con TODOS (OpenAI + GPT-OSS + DeepSeek)
   5. 📋 Mostrar transcripciones disponibles
   6. 🔧 Verificar configuración
   0. 🚪 Salir
```

### Motores de IA Disponibles

#### 1. OpenAI GPT-4o (Nube)

**Ventajas:**
- ✅ Máxima calidad de análisis
- ✅ Rápido (~2 minutos)
- ✅ Continuación automática para respuestas largas
- ✅ HTML bien estructurado

**Desventajas:**
- ❌ Requiere API key (de pago)
- ❌ Necesita conexión a internet
- ❌ Coste por uso ($0.10-0.30 por análisis)

**Configuración:**
```bash
# En .env
OPENAI_API_KEY=sk-tu-clave-aqui
OPENAI_MODEL=gpt-4o
OPENAI_MAX_TOKENS=16384
```

#### 2. Ollama GPT-OSS (Local)

**Ventajas:**
- ✅ Completamente gratuito
- ✅ Funciona sin internet
- ✅ Muy rápido (~1 minuto)
- ✅ Privacidad total

**Desventajas:**
- ❌ Requiere 13GB de RAM para el modelo
- ❌ Calidad ligeramente inferior a GPT-4o
- ❌ Necesita instalación de Ollama

**Instalación:**
```bash
# Instalar Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Descargar modelo
ollama pull gpt-oss
```

#### 3. Ollama DeepSeek-R1 (Local)

**Ventajas:**
- ✅ Completamente gratuito
- ✅ Muy eficiente (5GB modelo)
- ✅ Excelente calidad de análisis
- ✅ Respuestas muy detalladas

**Desventajas:**
- ❌ Ligeramente más lento (~2 minutos)
- ❌ Formato de salida ocasionalmente irregular

**Instalación:**
```bash
ollama pull deepseek-r1
```

### Ejecutar Motores Individuales

```bash
# Solo OpenAI
python generar_docs_openai.py

# Solo Ollama GPT-OSS
python generar_docs_ollama.py

# Solo DeepSeek-R1
python generar_docs_deepseek.py
```

## 📊 Resultados Generados

### Estructura de Salida

```
# Archivos index principales
index-openai.html      # Portal OpenAI
index-ollama.html      # Portal Ollama GPT-OSS
index-deepseek.html    # Portal DeepSeek-R1

# Documentación web por motor
www/
├── openai/           # HTML OpenAI
│   ├── fase-F1.html
│   ├── fase-F2.html
│   └── fase-F3.html
├── ollama/           # HTML Ollama GPT-OSS
│   ├── fase-F1.html
│   └── fase-F2.html
└── deepseek/         # HTML DeepSeek-R1
    ├── fase-F1.html
    └── fase-F2.html

# Análisis completos en markdown
procesados/
├── documentacion_openai_20251113.md
├── documentacion_ollama_20251113.md
└── documentacion_deepseek_20251113.md
```

### Contenido de la Documentación

Cada motor genera:

**📄 Análisis de texto:**
- Identificación de fases y vídeos
- Resúmenes por vídeo (corto y extendido)
- Ideas clave y puntos importantes
- Errores típicos y malos usos
- Síntesis global por fase

**🌐 Web interactiva:**
- Página index con navegación
- Páginas individuales por fase
- Cuestionarios tipo test
- Navegación entre páginas
- Diseño responsive

**📋 Características específicas:**
- **Cuestionarios**: 5-10 preguntas por fase
- **Enlaces**: Navegación completa entre páginas
- **Estilos**: CSS integrado, diseño profesional
- **JavaScript**: Corrección automática de cuestionarios

## 🔧 Utilidades Adicionales

### Reparar Enlaces

Si los enlaces entre páginas no funcionan:

```bash
python reparar_enlaces.py
```

**Resultado:**
```
🔧 REPARADOR DE ENLACES HTML
==================================================

🔍 Verificando motor: OPENAI
🔧 Reparando enlaces en index-openai.html
   ✅ Enlaces reparados en index-openai.html

✅ Proceso completado: 11 archivos reparados
```

### Verificar Configuración

```bash
python -c "
from transcribir import verificar_configuracion
verificar_configuracion()
"
```

## 📈 Optimización de Rendimiento

### Para Transcripción

**RTX 5090 (Óptimo):**
```python
# En transcribir.py
model = faster_whisper.WhisperModel(
    "large-v3",
    device="cuda",
    compute_type="float16",
    cpu_threads=8,
    num_workers=2
)
```

**RTX 4080/4090:**
```python
model = faster_whisper.WhisperModel(
    "large-v3",
    device="cuda", 
    compute_type="float16",
    cpu_threads=6,
    num_workers=1
)
```

**RTX 3080/3090:**
```python
model = faster_whisper.WhisperModel(
    "medium",  # Modelo más pequeño
    device="cuda",
    compute_type="float16",
    cpu_threads=4,
    num_workers=1
)
```

### Para IA Local

**Para Ollama con poca RAM:**
```bash
# Modelos alternativos más pequeños
ollama pull llama2:7b      # 3.8GB
ollama pull phi3:mini      # 2.3GB

# En .env
OLLAMA_MODEL=llama2:7b
```

## 🎨 Personalización

### Modificar Prompts

Los prompts están en `transcribir.py`:

```python
def crear_prompt_maestro_original(transcripciones_consolidadas):
    """Modificar este prompt para personalizar el análisis"""
    prompt = f"""
    Tu prompt personalizado aquí...
    
    Transcripciones: {transcripciones_consolidadas}
    """
    return prompt
```

### Personalizar Estilos Web

Los estilos CSS se generan automáticamente, pero puedes modificarlos editando la función `actualizar_enlaces_html()`.

### Añadir Nuevos Motores

1. Crear archivo `generar_docs_nuevo_motor.py`
2. Implementar función `generar_documentacion_con_nuevo_motor()`
3. Añadir opción al menú en `generar_docs.py`

## 🔍 Monitoreo y Debugging

### Logs de Transcripción

```bash
# Ver progreso en tiempo real
tail -f procesados/registro_transcripciones.txt
```

### Estadísticas de Rendimiento

```bash
# Ver métricas detalladas
cat procesados/estadisticas_transcripcion.json | jq '.'
```

### Debug de IA

Cada motor guarda información de debugging:

```bash
# Hash único para verificar creatividad
grep "Hash único" procesados/documentacion_*.md

# Tiempo de ejecución
grep "Tiempo de generación" procesados/documentacion_*.md
```

## 🚨 Solución de Problemas Comunes

### Error: No se detecta GPU

```bash
python -c "import torch; print(torch.cuda.is_available())"
```

**Si imprime `False`:**
1. Verificar instalación CUDA: `nvcc --version`
2. Reinstalar PyTorch con CUDA
3. Reiniciar sistema

### Error: Ollama no responde

```bash
# Reiniciar servicio
pkill ollama
ollama serve
```

### Error: OpenAI rate limit

Esperar 1 minuto o verificar límites de API en el dashboard de OpenAI.

### Calidad pobre de transcripción

1. Verificar calidad de audio del vídeo
2. Usar modelo más grande (`large-v3` en lugar de `medium`)
3. Cambiar `compute_type` a `float32`

---

**📌 Siguiente paso**: [Referencia de la API](API_REFERENCE.md)