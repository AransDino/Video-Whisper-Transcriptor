import pathlib
import torch
import shutil
import time
import os
from datetime import datetime, timedelta
from faster_whisper import WhisperModel
from openai import OpenAI
from dotenv import load_dotenv
import ollama

# Configurar OpenAI
load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

VIDEO_EXTS = [".mp4", ".mkv", ".avi", ".mov", ".m4a", ".mp3", ".wav"]

def transcribir_archivos(videos: pathlib.Path, carpeta_procesados: pathlib.Path):
    # Crear carpeta procesados si no existe
    carpeta_procesados.mkdir(exist_ok=True)
    
    # Crear carpeta backup si no existe
    carpeta_backup = carpeta_procesados.parent / "videos_backup"
    carpeta_backup.mkdir(exist_ok=True)
    
    # Detectar si CUDA está disponible
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"🚀 Usando dispositivo: {device}")
    
    if device == "cuda":
        print(f"🎮 GPU detectada: {torch.cuda.get_device_name(0)}")
        print(f"💾 Memoria GPU disponible: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
        # Para RTX 5090, usamos compute_type optimizado
        compute_type = "float16"
    else:
        compute_type = "int8"
    
    # Inicializar el modelo Whisper
    print(f"🤖 Cargando modelo Whisper (small) en {device}...")
    model_start = time.time()
    model = WhisperModel("small", device=device, compute_type=compute_type)
    model_load_time = time.time() - model_start
    print(f"✅ Modelo cargado en {model_load_time:.2f}s")
    print(f"💾 Backup configurado en: {carpeta_backup}")
    
    videos_procesados = []
    videos_info = []  # Para almacenar información detallada de cada video
    estadisticas_videos = []  # Para el sistema de estadísticas detalladas
    tiempo_total_inicio = time.time()
    tiempo_total_video = 0
    
    # Archivo de log general
    log_file = carpeta_procesados.parent / "registro_transcripciones.txt"
    
    # Archivo de transcripciones consolidadas de esta ejecución
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    archivo_transcripciones = carpeta_procesados / f"transcripciones_{timestamp}.txt"
    
    for ext in VIDEO_EXTS:
        for fichero in videos.glob(f"*{ext}"):
            print(f"\n{'='*60}")
            print(f"🎬 Procesando: {fichero.name}")
            print(f"📅 Inicio: {datetime.now().strftime('%H:%M:%S')}")
            
            # Obtener tamaño del archivo
            tamaño_mb = fichero.stat().st_size / (1024 * 1024)
            print(f"📦 Tamaño archivo: {tamaño_mb:.2f} MB")
            
            try:
                # Crear carpeta específica para este video
                carpeta_video = carpeta_procesados / fichero.stem
                carpeta_video.mkdir(exist_ok=True)
                
                # Tiempo de inicio de transcripción
                transcripcion_inicio = time.time()
                
                # Transcribir con faster-whisper
                segments, info = model.transcribe(
                    str(fichero), 
                    language="es",
                    beam_size=5,
                    word_timestamps=True
                )
                
                # Métricas del video
                duracion_video = info.duration
                tiempo_total_video += duracion_video
                
                print(f"⏱️ Duración video: {format_duration(duracion_video)}")
                print(f"🌐 Idioma detectado: {info.language} (confianza: {info.language_probability:.1%})")
                
                # Guardar transcripción en texto
                output_file = carpeta_video / f"{fichero.stem}.txt"
                segmentos_count = 0
                palabras_count = 0
                transcripcion_completa = ""  # Para el archivo consolidado
                
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(f"=== MÉTRICAS DEL VIDEO ===\n")
                    f.write(f"Archivo: {fichero.name}\n")
                    f.write(f"Tamaño: {tamaño_mb:.2f} MB\n")
                    f.write(f"Duración: {format_duration(duracion_video)}\n")
                    f.write(f"Idioma detectado: {info.language} (confianza: {info.language_probability:.1%})\n")
                    f.write(f"Fecha procesamiento: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"Dispositivo usado: {device.upper()}\n\n")
                    f.write(f"=== TRANSCRIPCIÓN ===\n\n")
                    
                    for segment in segments:
                        texto = segment.text.strip()
                        f.write(f"{texto}\n")
                        transcripcion_completa += f"{texto}\n"
                        segmentos_count += 1
                        palabras_count += len(texto.split())
                
                # Agregar transcripción al archivo consolidado de la ejecución
                agregar_transcripcion_consolidada(archivo_transcripciones, fichero, transcripcion_completa, duracion_video, segmentos_count, palabras_count)
                
                # Guardar también en formato SRT
                srt_file = carpeta_video / f"{fichero.stem}.srt"
                with open(srt_file, 'w', encoding='utf-8') as f:
                    segments, _ = model.transcribe(str(fichero), language="es")
                    for i, segment in enumerate(segments, 1):
                        start = format_time(segment.start)
                        end = format_time(segment.end)
                        f.write(f"{i}\n")
                        f.write(f"{start} --> {end}\n")
                        f.write(f"{segment.text.strip()}\n\n")
                
                # Calcular métricas de rendimiento
                transcripcion_tiempo = time.time() - transcripcion_inicio
                velocidad_procesamiento = duracion_video / transcripcion_tiempo
                
                # Crear backup del video original
                backup_destino = carpeta_backup / fichero.name
                print(f"💾 Creando backup...")
                shutil.copy2(str(fichero), str(backup_destino))
                
                # Mover el video procesado a su carpeta
                video_destino = carpeta_video / fichero.name
                shutil.move(str(fichero), str(video_destino))
                videos_procesados.append(fichero.name)
                
                # Recopilar estadísticas detalladas para la tabla
                estadisticas_video = recopilar_estadisticas_video(fichero, duracion_video, transcripcion_completa)
                if estadisticas_video:
                    estadisticas_videos.append(estadisticas_video)
                
                # Almacenar información detallada del video para el resumen
                videos_info.append({
                    'nombre': fichero.name,
                    'carpeta': fichero.stem,
                    'tamaño_mb': tamaño_mb,
                    'duracion': duracion_video,
                    'tiempo_proc': transcripcion_tiempo,
                    'velocidad': velocidad_procesamiento,
                    'segmentos': segmentos_count,
                    'palabras': palabras_count,
                    'idioma': info.language,
                    'confianza': info.language_probability
                })
                
                # Registrar en el log general
                registrar_transcripcion(log_file, fichero, duracion_video, transcripcion_tiempo, 
                                      velocidad_procesamiento, segmentos_count, palabras_count, 
                                      tamaño_mb, info, device)
                
                # Mostrar métricas detalladas
                print(f"⚡ Tiempo procesamiento: {transcripcion_tiempo:.2f}s")
                print(f"🚄 Velocidad: {velocidad_procesamiento:.2f}x (realtime)")
                print(f"📝 Segmentos generados: {segmentos_count}")
                print(f"📊 Palabras transcritas: {palabras_count}")
                print(f"📈 Palabras por minuto: {(palabras_count / duracion_video * 60):.0f}")
                
                print(f"✅ Completado exitosamente!")
                print(f"   📁 Carpeta: {carpeta_video.name}")
                print(f"   🎞️ Video: {fichero.name}")
                print(f"   💾 Backup: videos_backup/{fichero.name}")
                print(f"   📄 Transcripción: {output_file.name}")
                print(f"   🎬 Subtítulos: {srt_file.name}")
                
            except Exception as e:
                print(f"❌ Error procesando {fichero.name}: {e}")
    
    # Resumen final con métricas globales
    tiempo_total_final = time.time() - tiempo_total_inicio
    
    if videos_procesados:
        # Agregar resumen al log
        agregar_resumen_log(log_file, len(videos_procesados), tiempo_total_video, tiempo_total_final)
        
        # Generar tabla de estadísticas detalladas
        if estadisticas_videos:
            print(f"📊 Generando tabla de estadísticas detalladas...")
            archivo_estadisticas = generar_tabla_estadisticas(estadisticas_videos, carpeta_procesados)
        
        print(f"\n{'='*60}")
        print(f"🎉 ¡PROCESAMIENTO COMPLETADO!")
        print(f"{'='*60}")
        print(f"📊 MÉTRICAS GLOBALES:")
        print(f"   📺 Videos procesados: {len(videos_procesados)}")
        print(f"   ⏱️ Duración total videos: {format_duration(tiempo_total_video)}")
        print(f"   ⚡ Tiempo total procesamiento: {format_duration(tiempo_total_final)}")
        print(f"   🚄 Velocidad promedio: {(tiempo_total_video / tiempo_total_final):.2f}x")
        print(f"   💾 Ahorro de tiempo: {format_duration(tiempo_total_video - tiempo_total_final)}")
        print(f"   📁 Organizados en: {carpeta_procesados}")
        print(f"   💾 Backups guardados en: {carpeta_backup}")
        print(f"   📋 Log actualizado: {log_file.name}")
        print(f"   📄 Transcripciones consolidadas: transcripciones_{timestamp}.txt")
        
        # Mostrar información de estadísticas si se generaron
        if estadisticas_videos and 'archivo_estadisticas' in locals():
            print(f"   📊 Estadísticas detalladas: {archivo_estadisticas.name}")
        
        print(f"   🧹 Carpeta 'videos' liberada para nuevos archivos")
        print(f"   📅 Finalizado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Preguntar si quiere generar documentación y con qué motor
        motor_elegido = preguntar_generar_documentacion()
        if motor_elegido == 'openai':
            generar_documentacion_con_openai(archivo_transcripciones)
        elif motor_elegido == 'ollama':
            generar_documentacion_con_ollama(archivo_transcripciones)
            
    else:
        print(f"\n📭 No se encontraron videos para procesar en la carpeta 'videos'")

def agregar_transcripcion_consolidada(archivo_transcripciones, fichero, transcripcion_completa, duracion_video, segmentos_count, palabras_count):
    """Agrega la transcripción de un video al archivo consolidado de la ejecución"""
    
    # Crear el archivo si es la primera transcripción de la ejecución
    if not archivo_transcripciones.exists():
        with open(archivo_transcripciones, 'w', encoding='utf-8') as f:
            f.write(f"TRANSCRIPCIONES CONSOLIDADAS - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*80 + "\n\n")
    
    # Agregar la transcripción del video actual
    with open(archivo_transcripciones, 'a', encoding='utf-8') as f:
        f.write(f"📂 {fichero.name}\n")
        f.write(f"⏱️ Duración: {format_duration(duracion_video)} | 📝 Segmentos: {segmentos_count} | 📊 Palabras: {palabras_count}\n")
        f.write("-" * 80 + "\n")
        f.write(transcripcion_completa)
        f.write("\n" + "="*80 + "\n\n")

def agregar_resumen_log(log_file, num_videos, tiempo_total_video, tiempo_total_final):
    """Agrega un resumen de la sesión al archivo de log"""
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write("=" * 50 + "\n")
        f.write(f"🎉 RESUMEN DE SESIÓN - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 50 + "\n")
        f.write(f"📺 Videos procesados en esta sesión: {num_videos}\n")
        f.write(f"⏱️ Duración total de videos: {format_duration(tiempo_total_video)}\n")
        f.write(f"⚡ Tiempo total de procesamiento: {format_duration(tiempo_total_final)}\n")
        f.write(f"🚄 Velocidad promedio: {(tiempo_total_video / tiempo_total_final):.2f}x\n")
        f.write(f"💾 Ahorro de tiempo: {format_duration(tiempo_total_video - tiempo_total_final)}\n")
        f.write("=" * 50 + "\n\n")

def format_duration(seconds):
    """Convierte segundos a formato legible (HH:MM:SS)"""
    return str(timedelta(seconds=int(seconds)))

def registrar_transcripcion(log_file, fichero, duracion_video, tiempo_procesamiento, 
                          velocidad, segmentos, palabras, tamaño_mb, info, device):
    """Registra los detalles de la transcripción en el archivo de log general"""
    
    # Crear encabezado si el archivo no existe
    if not log_file.exists():
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write("REGISTRO GENERAL DE TRANSCRIPCIONES\n")
            f.write("="*80 + "\n")
            f.write(f"Archivo de log creado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Sistema: faster-whisper con {device.upper()}\n")
            f.write("="*80 + "\n\n")
    
    # Agregar entrada de la transcripción
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"📅 FECHA: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"📁 ARCHIVO: {fichero.name}\n")
        f.write(f"📦 TAMAÑO: {tamaño_mb:.2f} MB\n")
        f.write(f"⏱️ DURACIÓN: {format_duration(duracion_video)}\n")
        f.write(f"🌐 IDIOMA: {info.language} (confianza: {info.language_probability:.1%})\n")
        f.write(f"⚡ TIEMPO PROC: {tiempo_procesamiento:.2f}s\n")
        f.write(f"🚄 VELOCIDAD: {velocidad:.2f}x\n")
        f.write(f"📝 SEGMENTOS: {segmentos}\n")
        f.write(f"📊 PALABRAS: {palabras}\n")
        f.write(f"📈 PAL/MIN: {(palabras / duracion_video * 60):.0f}\n")
        f.write(f"🎮 DISPOSITIVO: {device.upper()}\n")
        f.write(f"📁 CARPETA: procesados/{fichero.stem}/\n")
        f.write(f"💾 BACKUP: videos_backup/{fichero.name}\n")
        f.write("-" * 50 + "\n\n")

def format_time(seconds):
    """Convierte segundos a formato SRT (HH:MM:SS,mmm)"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millisecs = int((seconds - int(seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millisecs:03d}"

def crear_prompt_documentacion(transcripciones_consolidadas):
    """Crea el prompt maestro para generar documentación con las transcripciones"""
    
    prompt = f"""Quiero que actúes como analista y diseñador de material formativo para la plataforma Klinikare / CliniQuer.

Te voy a dar transcripciones de varios vídeos de formación. 
Cada vídeo sigue esta nomenclatura en el nombre de archivo:

- Siempre empieza por "KLC" (de Klinikare / CliniQuer).
- Luego "-T" + número de tema. Ejemplo: T1, T2, T3…
- Luego "-v" + número de vídeo dentro de ese tema. Ejemplo: v1, v2, v3…
- Después del nombre, suele venir un título descriptivo. 
  Ejemplo: "KLC-T1-v1-Introducción a la IA.mp4"

Quiero dos grandes bloques de salida:

1) ANÁLISIS Y SÍNTESIS EN TEXTO
2) GENERACIÓN DE ESTRUCTURA WEB EN HTML (MÚLTIPLES PÁGINAS + QUIZ INTERACTIVO)"""

    return prompt

def crear_prompt_maestro_original(transcripciones_consolidadas):
    """Prompt maestro original del usuario adaptado al proyecto KLC"""
    
    prompt = f"""Quiero que actúes como analista y diseñador de material formativo para la plataforma Klinikare / CliniQuer.

Te voy a dar transcripciones de varios vídeos de formación. 
Cada vídeo sigue esta nomenclatura en el nombre de archivo:

- Siempre empieza por "KK" (de Klinikare).
- Luego "-F" + número de fase. Ejemplo: F1, F2, F3…
- Luego "-v" + número de vídeo dentro de esa fase. Ejemplo: v1, v2, v3…
- Después del nombre, suele venir un título descriptivo. 
  Ejemplo: "KK-F1-v1-Introducción a la IA.mp4"

Quiero dos grandes bloques de salida:

1) ANÁLISIS Y SÍNTESIS EN TEXTO
2) GENERACIÓN DE ESTRUCTURA WEB EN HTML (MÚLTIPLES PÁGINAS + QUIZ INTERACTIVO)

--------------------------------
BLOQUE 0 – ENTRADA (TRANSCRIPCIONES)
--------------------------------

Estas son las transcripciones consolidadas que debes analizar:

{transcripciones_consolidadas}

(Nota: las transcripciones ya vienen agrupadas por archivo. Cada bloque empieza con algo parecido a:
"📂 KK-F1-v1-Introducción a la IA.mp4" seguido del contenido).

--------------------------------
BLOQUE 1 – ANÁLISIS Y SÍNTESIS
--------------------------------

Primero quiero un análisis en texto, SIN generar HTML todavía.

1.1. Identificación de estructura por fases y vídeos
- Detecta todas las fases: F1, F2, F3, etc. a partir de los nombres de archivo (KK-F{{fase}}-v{{n}}).
- Dentro de cada fase, lista los vídeos en orden (v1, v2, v3…).
- Para cada vídeo, indica:
  - Código: por ejemplo "KK-F1-v1"
  - Título (si aparece en el nombre)
  - Fase a la que pertenece

1.2. Resumen corto por vídeo
Para cada vídeo, genera un resumen muy breve (2–3 frases) que explique:
- De qué trata.
- Qué quiere que aprenda el usuario al final.

1.3. Resumen extendido por vídeo
Para cada vídeo, genera:
- Un resumen en 1–3 párrafos.
- Una lista de 4–8 ideas clave o puntos importantes.
- Opcional: una lista de "errores típicos" o "malos usos" relacionados con el tema, si se deducen del contenido.

1.4. Síntesis global por fase
Para cada fase F1, F2, etc.:
- Explica en 1–2 párrafos cuál es el objetivo de la fase.
- Indica el perfil objetivo (por ejemplo: recepción, dirección, clínicos, etc. si se intuye).
- Resume qué sabrá hacer el usuario al terminar la fase.

Haz este BLOQUE 1 en texto estructurado con títulos y subtítulos, pero sin HTML.

Cuando termines el BLOQUE 1, continúa con el BLOQUE 2.

--------------------------------
BLOQUE 2 – GENERACIÓN WEB HTML
--------------------------------

Ahora quiero que conviertas todo esto en una pequeña "web de formación" en HTML, NO en una sola página, sino MULTI-PÁGINA:

REQUISITOS GENERALES:
- Usa solo HTML, CSS y JavaScript puro (sin frameworks).
- No dependas de librerías externas.
- El estilo puede ser sencillo pero ordenado y legible.
- El idioma de la interfaz debe ser ESPAÑOL.
- Respeta la organización por FASES (F1, F2…) y vídeos.

2.1. Estructura de archivos HTML a generar

Quiero que me devuelvas el código de estos archivos (cada uno en su bloque de código separado):

1) index.html  
2) fase-F1.html (si existe la fase 1)  
3) fase-F2.html (si existe la fase 2)  
4) etc. para todas las fases que aparezcan en las transcripciones.

IMPORTANTE:
- En cada archivo HTML, incluye el `<head>` completo (doctype, meta charset, título, estilos, etc.).
- Puedes repetir el CSS en cada archivo para simplificar (no pasa nada).
- Usa una misma barra de navegación en todos los archivos con enlaces a:
  - Inicio (index.html)
  - Cada fase detectada: F1, F2, F3, etc. (ej: fase-F1.html, fase-F2.html…)

2.2. Contenido de index.html

El `index.html` debe ser una portada/resumen con:

- Un título general: "Formación Klinikare / CliniQuer".
- Un pequeño texto explicando:
  - Que los vídeos están organizados por fases.
  - Que cada fase tiene su propia página.
  - Que hay cuestionarios tipo test al final de cada fase.
- Una sección "Listado de fases":
  - Una tarjeta por fase (F1, F2, F3…).
  - En cada tarjeta: 
    - Título de la fase (resumen breve basado en el análisis).
    - Lista de los vídeos de esa fase (con su código y título).
    - Un botón/enlace a la página de esa fase: por ejemplo `fase-F1.html`.
- Opcional: una pequeña nota recordando buenas prácticas para preguntar a la IA (si aplica por los contenidos).

2.3. Contenido de cada página de fase (fase-F1.html, fase-F2.html, etc.)

Para cada página de fase, estructura así:

- Cabecera con:
  - Título: "Fase F{{n}}: [nombre o descripción breve]".
  - Párrafo introductorio con el objetivo de la fase (usa la síntesis global de la fase).

- Sección "Vídeos de la fase":
  - Para cada vídeo de esa fase (por ejemplo KK-F1-v1, KK-F1-v2…):
    - Un bloque con:
      - Código y título (ej.: "KK-F1-v1 – Introducción a la IA").
      - Un resumen corto.
      - Un bloque desplegable (puedes usar `<details><summary>…</summary>…</details>`) con:
        - Resumen extendido del vídeo.
        - Lista de ideas clave.
        - Lista de errores típicos o puntos de atención (si los hay).

- Sección "Manual / Guía rápida de la fase":
  - Redacta un pequeño manual en texto (no hace falta HTML complejo, solo `<h3>`, `<p>`, `<ul>`).
  - Enfocado a que alguien pueda leerlo sin ver los vídeos y aún así saber usar lo básico del tema de la fase.

- Sección "Cuestionario de autoevaluación (tipo test)":
  - Crea entre 5 y 10 preguntas tipo test por fase.
  - Cada pregunta debe:
    - Estar basada en los contenidos reales de los vídeos de la fase.
    - Tener 3 o 4 opciones de respuesta.
    - Indicar internamente cuál es la correcta (para que el JS pueda comprobar).
  - Implementa un formulario sencillo con:
    - Preguntas con opciones tipo `radio`.
    - Un botón "Corregir".
    - Un bloque de resultados que muestre:
      - Cuántas respuestas correctas ha tenido el usuario.
      - Un mensaje general según el porcentaje (ej: "Necesitas repasar", "Bien", "Excelente").
    - Opción: mostrar un pequeño mensaje bajo cada pregunta indicando si esa pregunta se ha respondido bien o mal al corregir.

IMPORTANTE: 
- El JS debe ir al final del `<body>` dentro de `<script>`.
- No uses librerías, solo JavaScript nativo.
- Usa IDs o `data-` atributos para marcar qué opción es correcta.

2.4. Interactividad mínima (JS) para el cuestionario

Quiero un JS genérico que:
- Recorra todas las preguntas del cuestionario de la fase.
- Para cada pregunta:
  - Compruebe si la opción seleccionada coincide con la respuesta correcta.
- Cuente el número de aciertos.
- Muestre:
  - Nº de aciertos.
  - Nº de preguntas totales.
  - Un mensaje general según el porcentaje de acierto.
- Opcional: añada a cada pregunta una clase CSS o texto "Correcto" / "Incorrecto".

2.5. Estilo general (CSS)

Mantén un estilo limpio:
- Fondo claro.
- Tipografía sans-serif.
- Contenedores tipo "tarjeta" para cada bloque.
- Barra de navegación sencilla con enlaces a las fases.
- Botones sencillos pero visibles para:
  - "Ir a la fase F{{n}}".
  - "Corregir cuestionario".

--------------------------------
FORMATO DE LA RESPUESTA
--------------------------------

Quiero que tu respuesta siga este orden:

1) BLOQUE 1 – ANÁLISIS Y SÍNTESIS (solo texto, bien estructurado, sin HTML)
2) BLOQUE 2 – HTML

Dentro del BLOQUE 2, dame cada archivo HTML en un bloque de código separado así:

- Comentario indicando el nombre del archivo.
- Luego el contenido completo.

Ejemplo de formato:

[ARCHIVO: index.html]
```html
...código...
```

[ARCHIVO: fase-F1.html]
```html
...código...
```

Y así sucesivamente para cada fase que detectes.
Si por límite de longitud no puedes generar todos los HTML en una sola respuesta, prioriza:
1) index.html
2) la fase más baja (por ejemplo F1)
y luego indica qué quedaría pendiente.

Con todo esto, genera ahora el análisis y la estructura HTML en base a las transcripciones proporcionadas."""

    return prompt
    
    prompt = f"""Quiero que actúes como analista y diseñador de material formativo para la plataforma Klinikare / CliniQuer.

Te voy a dar transcripciones de varios vídeos de formación. 
Cada vídeo sigue esta nomenclatura en el nombre de archivo:

- Siempre empieza por "KK" (de Klinikare).
- Luego "-F" + número de fase. Ejemplo: F1, F2, F3…
- Luego "-v" + número de vídeo dentro de esa fase. Ejemplo: v1, v2, v3…
- Después del nombre, suele venir un título descriptivo. 
  Ejemplo: "KK-F1-v1-Introducción a la IA.mp4"

Quiero dos grandes bloques de salida:

1) ANÁLISIS Y SÍNTESIS EN TEXTO
2) GENERACIÓN DE ESTRUCTURA WEB EN HTML (MÚLTIPLES PÁGINAS + QUIZ INTERACTIVO)

--------------------------------
BLOQUE 0 – ENTRADA (TRANSCRIPCIONES)
--------------------------------

Estas son las transcripciones consolidadas que debes analizar:

{transcripciones_consolidadas}

(Nota: las transcripciones ya vienen agrupadas por archivo. Cada bloque empieza con algo parecido a:
"📂 KK-F1-v1-Introducción a la IA.mp4" seguido del contenido).

--------------------------------
BLOQUE 1 – ANÁLISIS Y SÍNTESIS
--------------------------------

Primero quiero un análisis en texto, SIN generar HTML todavía.

1.1. Identificación de estructura por fases y vídeos
- Detecta todas las fases: F1, F2, F3, etc. a partir de los nombres de archivo (KK-F{{fase}}-v{{n}}).
- Dentro de cada fase, lista los vídeos en orden (v1, v2, v3…).
- Para cada vídeo, indica:
  - Código: por ejemplo "KK-F1-v1"
  - Título (si aparece en el nombre)
  - Fase a la que pertenece

1.2. Resumen corto por vídeo
Para cada vídeo, genera un resumen muy breve (2–3 frases) que explique:
- De qué trata.
- Qué quiere que aprenda el usuario al final.

1.3. Resumen extendido por vídeo
Para cada vídeo, genera:
- Un resumen en 1–3 párrafos.
- Una lista de 4–8 ideas clave o puntos importantes.
- Opcional: una lista de "errores típicos" o "malos usos" relacionados con el tema, si se deducen del contenido.

1.4. Síntesis global por fase
Para cada fase F1, F2, etc.:
- Explica en 1–2 párrafos cuál es el objetivo de la fase.
- Indica el perfil objetivo (por ejemplo: recepción, dirección, clínicos, etc. si se intuye).
- Resume qué sabrá hacer el usuario al terminar la fase.

Haz este BLOQUE 1 en texto estructurado con títulos y subtítulos, pero sin HTML.

Cuando termines el BLOQUE 1, continúa con el BLOQUE 2.

--------------------------------
BLOQUE 2 – GENERACIÓN WEB HTML
--------------------------------

Ahora quiero que conviertas todo esto en una pequeña "web de formación" en HTML, NO en una sola página, sino MULTI-PÁGINA:

REQUISITOS GENERALES:
- Usa solo HTML, CSS y JavaScript puro (sin frameworks).
- No dependas de librerías externas.
- El estilo puede ser sencillo pero ordenado y legible.
- El idioma de la interfaz debe ser ESPAÑOL.
- Respeta la organización por FASES (F1, F2…) y vídeos.

2.1. Estructura de archivos HTML a generar

Quiero que me devuelvas el código de estos archivos (cada uno en su bloque de código separado):

1) index.html  
2) fase-F1.html (si existe la fase 1)  
3) fase-F2.html (si existe la fase 2)  
4) etc. para todas las fases que aparezcan en las transcripciones.

IMPORTANTE:
- En cada archivo HTML, incluye el `<head>` completo (doctype, meta charset, título, estilos, etc.).
- Puedes repetir el CSS en cada archivo para simplificar (no pasa nada).
- Usa una misma barra de navegación en todos los archivos con enlaces a:
  - Inicio (index.html)
  - Cada fase detectada: F1, F2, F3, etc. (ej: fase-F1.html, fase-F2.html…)

2.2. Contenido de index.html

El `index.html` debe ser una portada/resumen con:

- Un título general: "Formación Klinikare / CliniQuer".
- Un pequeño texto explicando:
  - Que los vídeos están organizados por fases.
  - Que cada fase tiene su propia página.
  - Que hay cuestionarios tipo test al final de cada fase.
- Una sección "Listado de fases":
  - Una tarjeta por fase (F1, F2, F3…).
  - En cada tarjeta: 
    - Título de la fase (resumen breve basado en el análisis).
    - Lista de los vídeos de esa fase (con su código y título).
    - Un botón/enlace a la página de esa fase: por ejemplo `fase-F1.html`.
- Opcional: una pequeña nota recordando buenas prácticas para preguntar a la IA (si aplica por los contenidos).

2.3. Contenido de cada página de fase (fase-F1.html, fase-F2.html, etc.)

Para cada página de fase, estructura así:

- Cabecera con:
  - Título: "Fase F{{n}}: [nombre o descripción breve]".
  - Párrafo introductorio con el objetivo de la fase (usa la síntesis global de la fase).

- Sección "Vídeos de la fase":
  - Para cada vídeo de esa fase (por ejemplo KK-F1-v1, KK-F1-v2…):
    - Un bloque con:
      - Código y título (ej.: "KK-F1-v1 – Introducción a la IA").
      - Un resumen corto.
      - Un bloque desplegable (puedes usar `<details><summary>…</summary>…</details>`) con:
        - Resumen extendido del vídeo.
        - Lista de ideas clave.
        - Lista de errores típicos o puntos de atención (si los hay).

- Sección "Manual / Guía rápida de la fase":
  - Redacta un pequeño manual en texto (no hace falta HTML complejo, solo `<h3>`, `<p>`, `<ul>`).
  - Enfocado a que alguien pueda leerlo sin ver los vídeos y aún así saber usar lo básico del tema de la fase.

- Sección "Cuestionario de autoevaluación (tipo test)":
  - Crea entre 5 y 10 preguntas tipo test por fase.
  - Cada pregunta debe:
    - Estar basada en los contenidos reales de los vídeos de la fase.
    - Tener 3 o 4 opciones de respuesta.
    - Indicar internamente cuál es la correcta (para que el JS pueda comprobar).
  - Implementa un formulario sencillo con:
    - Preguntas con opciones tipo `radio`.
    - Un botón "Corregir".
    - Un bloque de resultados que muestre:
      - Cuántas respuestas correctas ha tenido el usuario.
      - Un mensaje general según el porcentaje (ej: "Necesitas repasar", "Bien", "Excelente").
    - Opción: mostrar un pequeño mensaje bajo cada pregunta indicando si esa pregunta se ha respondido bien o mal al corregir.

IMPORTANTE: 
- El JS debe ir al final del `<body>` dentro de `<script>`.
- No uses librerías, solo JavaScript nativo.
- Usa IDs o `data-` atributos para marcar qué opción es correcta.

2.4. Interactividad mínima (JS) para el cuestionario

Quiero un JS genérico que:
- Recorra todas las preguntas del cuestionario de la fase.
- Para cada pregunta:
  - Compruebe si la opción seleccionada coincide con la respuesta correcta.
- Cuente el número de aciertos.
- Muestre:
  - Nº de aciertos.
  - Nº de preguntas totales.
  - Un mensaje general según el porcentaje de acierto.
- Opcional: añada a cada pregunta una clase CSS o texto "Correcto" / "Incorrecto".

2.5. Estilo general (CSS)

Mantén un estilo limpio:
- Fondo claro.
- Tipografía sans-serif.
- Contenedores tipo "tarjeta" para cada bloque.
- Barra de navegación sencilla con enlaces a las fases.
- Botones sencillos pero visibles para:
  - "Ir a la fase F{{n}}".
  - "Corregir cuestionario".

--------------------------------
FORMATO DE LA RESPUESTA
--------------------------------

Quiero que tu respuesta siga este orden:

1) BLOQUE 1 – ANÁLISIS Y SÍNTESIS (solo texto, bien estructurado, sin HTML)
2) BLOQUE 2 – HTML

Dentro del BLOQUE 2, dame cada archivo HTML en un bloque de código separado así:

- Comentario indicando el nombre del archivo.
- Luego el contenido completo.

Ejemplo de formato:

[ARCHIVO: index.html]
```html
...código...
```

[ARCHIVO: fase-F1.html]
```html
...código...
```

Y así sucesivamente para cada fase que detectes.
Si por límite de longitud no puedes generar todos los HTML en una sola respuesta, prioriza:
1) index.html
2) la fase más baja (por ejemplo F1)
y luego indica qué quedaría pendiente.

Con todo esto, genera ahora el análisis y la estructura HTML en base a las transcripciones proporcionadas."""

    return prompt


def recopilar_estadisticas_video(video_path, duracion_transcripcion, caracteres_transcripcion):
    """Recopila estadísticas detalladas de un vídeo procesado"""
    try:
        # Obtener información básica del archivo
        video_stats = video_path.stat()
        tamaño_mb = video_stats.st_size / (1024 * 1024)
        
        # Información del nombre del archivo
        nombre_archivo = video_path.name
        codigo_video = extraer_codigo_video(nombre_archivo)
        
        # Calcular estadísticas de transcripción
        palabras_transcripcion = len(caracteres_transcripcion.split()) if caracteres_transcripcion else 0
        velocidad_transcripcion = palabras_transcripcion / (duracion_transcripcion / 60) if duracion_transcripcion > 0 else 0
        
        estadisticas = {
            'nombre_archivo': nombre_archivo,
            'codigo_video': codigo_video,
            'tamaño_mb': round(tamaño_mb, 2),
            'duracion_segundos': round(duracion_transcripcion, 2),
            'duracion_formateada': f"{int(duracion_transcripcion//60):02d}:{int(duracion_transcripcion%60):02d}",
            'caracteres_transcripcion': len(caracteres_transcripcion) if caracteres_transcripcion else 0,
            'palabras_transcripcion': palabras_transcripcion,
            'velocidad_palabras_min': round(velocidad_transcripcion, 1),
            'fecha_procesamiento': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        return estadisticas
    except Exception as e:
        print(f"⚠️ Error al recopilar estadísticas de {video_path}: {e}")
        return None


def extraer_codigo_video(nombre_archivo):
    """Extrae el código KLC-TX-vY del nombre del archivo"""
    import re
    match = re.search(r'KLC-T\d+-v\d+', nombre_archivo)
    return match.group(0) if match else "Sin código"


def generar_tabla_estadisticas(lista_estadisticas, output_dir):
    """Genera tabla HTML con estadísticas detalladas de todos los vídeos"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archivo_estadisticas = output_dir / f"estadisticas_procesamiento_{timestamp}.html"
        
        # Calcular totales
        total_videos = len(lista_estadisticas)
        total_duracion = sum(est['duracion_segundos'] for est in lista_estadisticas if est)
        total_caracteres = sum(est['caracteres_transcripcion'] for est in lista_estadisticas if est)
        total_palabras = sum(est['palabras_transcripcion'] for est in lista_estadisticas if est)
        total_tamaño = sum(est['tamaño_mb'] for est in lista_estadisticas if est)
        
        promedio_velocidad = sum(est['velocidad_palabras_min'] for est in lista_estadisticas if est and est['velocidad_palabras_min'] > 0) / total_videos if total_videos > 0 else 0
        
        # Formatear duración total
        horas = int(total_duracion // 3600)
        minutos = int((total_duracion % 3600) // 60)
        segundos = int(total_duracion % 60)
        duracion_total_formateada = f"{horas:02d}:{minutos:02d}:{segundos:02d}"
        
        html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Estadísticas de Procesamiento - Klinikare Transcriptor</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f7fa;
            color: #333;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 2.2rem;
            font-weight: 700;
        }}
        .header p {{
            margin: 10px 0 0 0;
            opacity: 0.9;
            font-size: 1.1rem;
        }}
        
        .stats-summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 30px;
            background-color: #f8fafc;
            border-bottom: 2px solid #e2e8f0;
        }}
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            border: 1px solid #e2e8f0;
        }}
        .stat-card h3 {{
            margin: 0 0 10px 0;
            color: #1e40af;
            font-size: 0.9rem;
            text-transform: uppercase;
            font-weight: 600;
            letter-spacing: 0.5px;
        }}
        .stat-card .number {{
            font-size: 2rem;
            font-weight: 700;
            color: #1f2937;
            margin: 0;
        }}
        .stat-card .unit {{
            color: #6b7280;
            font-size: 0.9rem;
            margin-top: 5px;
        }}
        
        .table-container {{
            padding: 30px;
            overflow-x: auto;
        }}
        .table-title {{
            font-size: 1.5rem;
            font-weight: 600;
            color: #1f2937;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        }}
        th {{
            background: linear-gradient(135deg, #1e40af 0%, #1d4ed8 100%);
            color: white;
            padding: 15px 12px;
            text-align: left;
            font-weight: 600;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        td {{
            padding: 12px;
            border-bottom: 1px solid #e5e7eb;
            vertical-align: top;
        }}
        tr:nth-child(even) {{
            background-color: #f8fafc;
        }}
        tr:hover {{
            background-color: #f1f5f9;
        }}
        .codigo {{
            font-family: 'Courier New', monospace;
            background: #f3f4f6;
            padding: 4px 8px;
            border-radius: 4px;
            font-weight: 600;
            color: #1f2937;
        }}
        .numero {{
            text-align: right;
            font-weight: 600;
        }}
        .fecha {{
            font-size: 0.85rem;
            color: #6b7280;
        }}
        .duracion {{
            font-family: 'Courier New', monospace;
            font-weight: 600;
        }}
        .tamaño-grande {{ color: #dc2626; }}
        .tamaño-medio {{ color: #f59e0b; }}
        .tamaño-pequeño {{ color: #16a34a; }}
        
        .footer {{
            text-align: center;
            padding: 20px;
            background-color: #f8fafc;
            color: #6b7280;
            font-size: 0.9rem;
            border-top: 1px solid #e2e8f0;
        }}
        
        @media (max-width: 768px) {{
            .stats-summary {{
                grid-template-columns: 1fr 1fr;
            }}
            .table-container {{
                padding: 15px;
            }}
            th, td {{
                padding: 8px 6px;
                font-size: 0.85rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Estadísticas de Procesamiento</h1>
            <p>Klinikare Video Whisper-Transcriptor | {datetime.now().strftime("%d de %B de %Y, %H:%M")}</p>
        </div>
        
        <div class="stats-summary">
            <div class="stat-card">
                <h3>Total Vídeos</h3>
                <div class="number">{total_videos}</div>
                <div class="unit">archivos procesados</div>
            </div>
            <div class="stat-card">
                <h3>Duración Total</h3>
                <div class="number">{duracion_total_formateada}</div>
                <div class="unit">horas:minutos:segundos</div>
            </div>
            <div class="stat-card">
                <h3>Tamaño Total</h3>
                <div class="number">{total_tamaño:.1f}</div>
                <div class="unit">MB</div>
            </div>
            <div class="stat-card">
                <h3>Palabras Totales</h3>
                <div class="number">{total_palabras:,}</div>
                <div class="unit">palabras transcritas</div>
            </div>
            <div class="stat-card">
                <h3>Caracteres Totales</h3>
                <div class="number">{total_caracteres:,}</div>
                <div class="unit">caracteres</div>
            </div>
            <div class="stat-card">
                <h3>Velocidad Promedio</h3>
                <div class="number">{promedio_velocidad:.1f}</div>
                <div class="unit">palabras/minuto</div>
            </div>
        </div>
        
        <div class="table-container">
            <h2 class="table-title">📋 Detalles por Vídeo</h2>
            <table>
                <thead>
                    <tr>
                        <th>Código</th>
                        <th>Archivo</th>
                        <th>Duración</th>
                        <th>Tamaño (MB)</th>
                        <th>Palabras</th>
                        <th>Caracteres</th>
                        <th>Vel. (pal/min)</th>
                        <th>Procesado</th>
                    </tr>
                </thead>
                <tbody>"""
        
        # Añadir filas de datos
        for est in lista_estadisticas:
            if not est:
                continue
                
            # Clasificar tamaño del archivo
            if est['tamaño_mb'] > 100:
                clase_tamaño = "tamaño-grande"
            elif est['tamaño_mb'] > 50:
                clase_tamaño = "tamaño-medio"
            else:
                clase_tamaño = "tamaño-pequeño"
            
            html_content += f"""
                    <tr>
                        <td><span class="codigo">{est['codigo_video']}</span></td>
                        <td>{est['nombre_archivo']}</td>
                        <td class="duracion numero">{est['duracion_formateada']}</td>
                        <td class="numero {clase_tamaño}">{est['tamaño_mb']}</td>
                        <td class="numero">{est['palabras_transcripcion']:,}</td>
                        <td class="numero">{est['caracteres_transcripcion']:,}</td>
                        <td class="numero">{est['velocidad_palabras_min']}</td>
                        <td class="fecha">{est['fecha_procesamiento']}</td>
                    </tr>"""
        
        html_content += f"""
                </tbody>
            </table>
        </div>
        
        <div class="footer">
            <p>Generado automáticamente por Klinikare Video Whisper-Transcriptor<br>
            🕐 Tiempo total de vídeo: {duracion_total_formateada} | 💾 Espacio total: {total_tamaño:.1f} MB | 📝 {total_palabras:,} palabras transcritas</p>
        </div>
    </div>
</body>
</html>"""
        
        with open(archivo_estadisticas, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"📊 Estadísticas guardadas en: {archivo_estadisticas}")
        return archivo_estadisticas
        
    except Exception as e:
        print(f"❌ Error al generar tabla de estadísticas: {e}")
        return None
    
    prompt = f"""Eres un experto diseñador de materiales educativos y plataformas de e-learning para empresas. Tu misión es crear una GUÍA DE FORMACIÓN Y ESTUDIO INTERACTIVA de alta calidad para Klinikare / CliniQuer.

🎯 OBJETIVO PRINCIPAL: Crear una plataforma web de formación profesional que sirva como:
- Guía de estudio completa y estructurada
- Material de consulta rápida para empleados
- Sistema de autoevaluación y seguimiento del aprendizaje
- Recurso de onboarding para nuevos usuarios
- Manual de referencia interactivo

Te voy a dar transcripciones de varios vídeos de formación empresarial. 
Cada vídeo sigue esta nomenclatura en el nombre de archivo:

- Siempre empieza por "KLC" (de Klinikare / CliniQuer).
- Luego "-T" + número de tema. Ejemplo: T1, T2, T3…
- Luego "-v" + número de vídeo dentro de ese tema. Ejemplo: v1, v2, v3…
- Después del nombre, suele venir un título descriptivo. 
  Ejemplo: "KLC-T1-v1-Introducción a la IA.mp4"

Quiero dos grandes bloques de salida:

1) ANÁLISIS EDUCATIVO Y ESTRUCTURACIÓN PEDAGÓGICA
2) PLATAFORMA WEB DE FORMACIÓN INTERACTIVA (DISEÑO MODERNO + FUNCIONALIDADES EDUCATIVAS)

--------------------------------
BLOQUE 0 – ENTRADA (TRANSCRIPCIONES)
--------------------------------

Estas son las transcripciones consolidadas que debes analizar:

{transcripciones_consolidadas}

(Nota: las transcripciones ya vienen agrupadas por archivo. Cada bloque empieza con algo parecido a:
"📂 KLC-T1-v1-Introducción a la IA.mp4" seguido del contenido).

--------------------------------
BLOQUE 1 – ANÁLISIS Y SÍNTESIS
--------------------------------

Primero quiero un análisis en texto, SIN generar HTML todavía.

1.1. Identificación de estructura por temas y vídeos
- Detecta todos los temas: T1, T2, T3, etc. a partir de los nombres de archivo (KLC-T{{tema}}-v{{n}}).
- Dentro de cada tema, lista los vídeos en orden (v1, v2, v3…).
- Para cada vídeo, indica:
  - Código: por ejemplo "KLC-T1-v1"
  - Título (si aparece en el nombre)
  - Tema al que pertenece

1.2. Resumen corto por vídeo
Para cada vídeo, genera un resumen muy breve (2–3 frases) que explique:
- De qué trata.
- Qué quiere que aprenda el usuario al final.

1.3. Resumen extendido por vídeo
Para cada vídeo, genera:
- Un resumen en 1–3 párrafos.
- Una lista de 4–8 ideas clave o puntos importantes.
- Opcional: una lista de "errores típicos" o "malos usos" relacionados con el tema, si se deducen del contenido.

1.4. Síntesis global por tema
Para cada tema T1, T2, etc.:
- Explica en 1–2 párrafos cuál es el objetivo del tema.
- Indica el perfil objetivo (por ejemplo: recepción, dirección, clínicos, etc. si se intuye).
- Resume qué sabrá hacer el usuario al terminar el tema.

Haz este BLOQUE 1 en texto estructurado con títulos y subtítulos, pero sin HTML.

Cuando termines el BLOQUE 1, continúa con el BLOQUE 2.

--------------------------------
BLOQUE 2 – GENERACIÓN WEB HTML
--------------------------------

Ahora quiero que conviertas todo esto en una pequeña "web de formación" en HTML, NO en una sola página, sino MULTI-PÁGINA:

REQUISITOS GENERALES:
- Usa solo HTML, CSS y JavaScript puro (sin frameworks).
- No dependas de librerías externas.
- El estilo puede ser sencillo pero ordenado y legible.
- El idioma de la interfaz debe ser ESPAÑOL.
- Respeta la organización por TEMAS (T1, T2…) y vídeos.

2.1. Estructura de archivos HTML a generar

Quiero que me devuelvas el código de estos archivos con esta estructura específica:

📁 ESTRUCTURA DE DIRECTORIOS:
```
/
├── index-openai.html             (Página principal OpenAI - DIRECTORIO RAÍZ)
├── index-ollama.html             (Página principal Ollama - DIRECTORIO RAÍZ)  
└── www/                          (Carpeta para archivos web)
    ├── openai/                   (Archivos generados con OpenAI)
    │   ├── tema-T1.html
    │   ├── tema-T2.html
    │   └── tema-T3.html          (etc.)
    └── ollama/                   (Archivos generados con Ollama)
        ├── tema-T1.html
        ├── tema-T2.html
        └── tema-T3.html          (etc.)
```

📋 ARCHIVOS A GENERAR (cada uno en su bloque de código separado):

1) **index.html** (EN EL DIRECTORIO RAÍZ - se renombrará según el motor)
   - Página de bienvenida y navegación principal
   - Enlaces relativos a los archivos en www/motor/
   - Ejemplo de enlaces: `<a href="www/openai/tema-T1.html">Tema 1</a>` o `<a href="www/ollama/tema-T1.html">Tema 1</a>`

2) **www/tema-T1.html** (se moverán a www/motor/ automáticamente)
3) **www/tema-T2.html** (se moverán a www/motor/ automáticamente)  
4) etc. para todos los temas que aparezcan en las transcripciones.

⚠️ IMPORTANTE PARA LOS ENLACES:
- El index.html está en la raíz, usa rutas: `www/motor/tema-TX.html` (motor será openai u ollama)
- Los archivos tema-TX.html están en www/motor/, usan rutas: `../../index-motor.html` para volver al inicio
- Entre temas: `tema-T1.html`, `tema-T2.html` (sin ../ porque están en la misma carpeta)

IMPORTANTE:
- En cada archivo HTML, incluye el `<head>` completo (doctype, meta charset, título, estilos, etc.).
- Puedes repetir el CSS en cada archivo para simplificar (no pasa nada).
- Usa una misma barra de navegación en todos los archivos con enlaces ADAPTADOS A SU UBICACIÓN:
  
  📍 **Para index.html (en raíz)**:
  - Inicio: # (misma página) 
  - Temas: www/motor/tema-T1.html, www/motor/tema-T2.html, etc. (motor = openai u ollama)
  
  📍 **Para tema-TX.html (en www/motor/)**:
  - Inicio: ../../index-motor.html (motor = openai u ollama)
  - Otros temas: tema-T1.html, tema-T2.html, etc. (sin ../../ porque están en la misma carpeta)

2.2. Contenido de index.html (EN EL DIRECTORIO RAÍZ)

El `index.html` debe ser una portada/resumen con:

- Un título general: "Formación Klinikare / CliniQuer".
- Un pequeño texto explicando:
  - Que los vídeos están organizados por temas.
  - Que cada tema tiene su propia página en la carpeta www/motor/.
  - Que hay cuestionarios tipo test al final de cada tema.
- Una sección "Listado de temas":
  - Una tarjeta por tema (T1, T2, T3…).
  - En cada tarjeta: 
    - Título del tema (resumen breve basado en el análisis).
    - Lista de los vídeos de ese tema (con su código y título).
    - Un botón/enlace a la página de ese tema usando rutas relativas: `www/motor/tema-T1.html`, `www/motor/tema-T2.html`, etc. (donde motor = openai u ollama).
- Opcional: una pequeña nota recordando buenas prácticas para preguntar a la IA (si aplica por los contenidos).

2.3. Contenido de cada página de tema (tema-T1.html, tema-T2.html, etc.)

Para cada página de tema, estructura así:

- Cabecera con:
  - Título: "Tema T{{n}}: [nombre o descripción breve]".
  - Párrafo introductorio con el objetivo del tema (usa la síntesis global del tema).

- Sección "Vídeos del tema":
  - Para cada vídeo de ese tema (por ejemplo KLC-T1-v1, KLC-T1-v2…):
    - Un bloque con:
      - Código y título (ej.: "KLC-T1-v1 – Introducción a la IA").
      - Un resumen corto.
      - Un bloque desplegable (puedes usar `<details><summary>…</summary>…</details>`) con:
        - Resumen extendido del vídeo.
        - Lista de ideas clave.
        - Lista de errores típicos o puntos de atención (si los hay).

- Sección "Manual / Guía rápida del tema":
  - Redacta un pequeño manual en texto (no hace falta HTML complejo, solo `<h3>`, `<p>`, `<ul>`).
  - Enfocado a que alguien pueda leerlo sin ver los vídeos y aún así saber usar lo básico del tema del tema.

- Sección "Cuestionario de autoevaluación (tipo test)":
  - Crea entre 5 y 10 preguntas tipo test por tema.
  - Cada pregunta debe:
    - Estar basada en los contenidos reales de los vídeos del tema.
    - Tener 3 o 4 opciones de respuesta.
    - Indicar internamente cuál es la correcta (para que el JS pueda comprobar).
  - Implementa un formulario sencillo con:
    - Preguntas con opciones tipo `radio`.
    - Un botón "Corregir".
    - Un bloque de resultados que muestre:
      - Cuántas respuestas correctas ha tenido el usuario.
      - Un mensaje general según el porcentaje (ej: "Necesitas repasar", "Bien", "Excelente").
    - Opción: mostrar un pequeño mensaje bajo cada pregunta indicando si esa pregunta se ha respondido bien o mal al corregir.

IMPORTANTE: 
- El JS debe ir al final del `<body>` dentro de `<script>`.
- No uses librerías, solo JavaScript nativo.
- Usa IDs o `data-` atributos para marcar qué opción es correcta.

2.4. Interactividad mínima (JS) para el cuestionario

Quiero un JS genérico que:
- Recorra todas las preguntas del cuestionario del tema.
- Para cada pregunta:
  - Compruebe si la opción seleccionada coincide con la respuesta correcta.
- Cuente el número de aciertos.
- Muestre:
  - Nº de aciertos.
  - Nº de preguntas totales.
  - Un mensaje general según el porcentaje de acierto.
- Opcional: añada a cada pregunta una clase CSS o texto "Correcto" / "Incorrecto".

2.5. Estilo general (CSS)

Mantén un estilo limpio:
- Fondo claro.
- Tipografía sans-serif.
- Contenedores tipo "tarjeta" para cada bloque.
- Barra de navegación sencilla con enlaces a los temas.
- Botones sencillos pero visibles para:
  - "Ir al tema T{{n}}".
  - "Corregir cuestionario".

Con este análisis, genera ahora el análisis completo y la estructura HTML en base a las transcripciones proporcionadas.

--------------------------------
FORMATO DE LA RESPUESTA
--------------------------------

Tu respuesta debe seguir este orden exacto:

**1) BLOQUE 1 – ANÁLISIS Y SÍNTESIS** (solo texto, bien estructurado, sin HTML)

**2) BLOQUE 2 – ARCHIVOS HTML**

Dentro del BLOQUE 2, dame cada archivo HTML en un bloque de código separado usando EXACTAMENTE este formato:

```
[ARCHIVO: index.html]
```html
<!DOCTYPE html>
<html lang="es">
...código completo del index.html...
```

[ARCHIVO: www/tema-T1.html]
```html
<!DOCTYPE html>
<html lang="es">
...código completo del tema T1...
```

[ARCHIVO: www/tema-T2.html]
```html
<!DOCTYPE html>
<html lang="es">
...código completo del tema T2...
```

Y así sucesivamente para cada tema detectado.

🔥 INSTRUCCIONES CRÍTICAS:
1. **SIEMPRE** genera un archivo index.html
2. **SIEMPRE** genera un archivo tema-TX.html por CADA tema que detectes (T1, T2, T3, etc.)
3. **NO OMITAS** ningún tema
4. **USA EXACTAMENTE** el formato [ARCHIVO: nombre] antes de cada ```html
5. **INCLUYE TODO** el código HTML completo en cada archivo
6. **VERIFICA** que generas al menos 2 archivos (index + al menos 1 tema)

Si detectas 3 temas (T1, T2, T3), debes generar 4 archivos:
- [ARCHIVO: index.html]
- [ARCHIVO: www/tema-T1.html] 
- [ARCHIVO: www/tema-T2.html]
- [ARCHIVO: www/tema-T3.html]

⚠️ IMPORTANTE:
- Usa EXACTAMENTE el formato [ARCHIVO: nombre] antes de cada bloque
- Para el index.html usa: [ARCHIVO: index.html]
- Para los temas usa: [ARCHIVO: www/tema-TX.html]
- DEBES generar UN ARCHIVO POR CADA TEMA detectado en las transcripciones
- Incluye el código HTML completo con DOCTYPE, head, body, estilos CSS y JavaScript
- Asegúrate de que las rutas de navegación sean correctas según la estructura de directorios
- NO omitas ningún tema, genera TODOS los archivos HTML necesarios

🔥 REQUISITO CRÍTICO: Debes generar:
1. Un archivo index.html
2. Un archivo tema-TX.html por cada tema T1, T2, T3, etc. que detectes
3. Cada tema debe tener su página completa con navegación, contenido y cuestionario

Ejemplo de salida esperada si hay 2 temas:
- [ARCHIVO: index.html] + código HTML
- [ARCHIVO: www/tema-T1.html] + código HTML  
- [ARCHIVO: www/tema-T2.html] + código HTML"""

    return prompt
    """Crea un prompt simplificado para Ollama que sea menos pesado de procesar"""
    
    # Extraer solo una muestra de las transcripciones para no sobrecargar a Ollama
    lineas = transcripciones_consolidadas.split('\n')
    muestra = '\n'.join(lineas[:150])  # Solo las primeras 150 líneas
    
    prompt = f"""Eres un analista educativo experto. Analiza estas transcripciones de videos formativos y genera documentación web.

TRANSCRIPCIONES (muestra):
{muestra}

INSTRUCCIONES:
1) Los videos siguen formato: KK-FX-vY (donde X=tema, Y=video)
2) Genera EXACTAMENTE estos archivos con formato [ARCHIVO: nombre]:

[ARCHIVO: index.html]
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Formación Klinikare</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .tema {{ border: 1px solid #ddd; padding: 15px; margin: 10px 0; }}
        .btn {{ background: #007bff; color: white; padding: 10px; text-decoration: none; }}
    </style>
</head>
<body>
    <h1>Formación Klinikare / CliniQuer</h1>
    <div class="tema">
        <h3>Tema 1: Introducción a IA</h3>
        <p>Videos sobre uso básico de IA en la plataforma</p>
        <a href="www/ollama/tema-T1.html" class="btn">Ver Tema 1</a>
    </div>
    <div class="tema">
        <h3>Tema 2: Gestión de Pacientes</h3>
        <p>Manejo de agendas y pacientes</p>
        <a href="www/ollama/tema-T2.html" class="btn">Ver Tema 2</a>
    </div>
</body>
</html>
```

[ARCHIVO: www/tema-T1.html]
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Tema 1 - IA</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .video {{ border-left: 4px solid #007bff; padding: 10px; margin: 10px 0; }}
        .nav {{ background: #f8f9fa; padding: 10px; margin-bottom: 20px; }}
        .quiz {{ background: #e9ecef; padding: 15px; margin-top: 20px; }}
    </style>
</head>
<body>
    <div class="nav">
        <a href="../../index-ollama.html">← Inicio</a> |
        <a href="tema-T2.html">Tema 2 →</a>
    </div>
    
    <h1>Tema 1: Introducción a la IA</h1>
    
    <div class="video">
        <h3>Video 1: Introducción a la IA</h3>
        <p><strong>Resumen:</strong> Conceptos básicos sobre el uso de IA en CliniQuer.</p>
        <p><strong>Ideas clave:</strong> IA disponible 24/7, importancia de preguntas claras, ejemplos prácticos.</p>
    </div>
    
    <div class="quiz">
        <h3>Cuestionario</h3>
        <form id="quiz1">
            <p><strong>1. ¿Cuál es la ventaja principal de la IA en CliniQuer?</strong></p>
            <input type="radio" name="q1" value="a"> Cuesta menos<br>
            <input type="radio" name="q1" value="b" data-correct="true"> Está disponible 24/7<br>
            <input type="radio" name="q1" value="c"> Es más rápida<br>
            
            <p><strong>2. ¿Cómo debes hacer las preguntas a la IA?</strong></p>
            <input type="radio" name="q2" value="a" data-correct="true"> Claras y específicas<br>
            <input type="radio" name="q2" value="b"> Cortas y simples<br>
            <input type="radio" name="q2" value="c"> Con muchas preguntas juntas<br>
            
            <button type="button" onclick="corregirQuiz()">Corregir</button>
            <div id="resultado1"></div>
        </form>
    </div>
    
    <script>
        function corregirQuiz() {{
            const form = document.getElementById('quiz1');
            const correctas = form.querySelectorAll('input[data-correct="true"]');
            let aciertos = 0;
            
            correctas.forEach(input => {{
                if (input.checked) aciertos++;
            }});
            
            const total = correctas.length;
            const porcentaje = (aciertos / total) * 100;
            let mensaje = "";
            
            if (porcentaje >= 80) mensaje = "¡Excelente! Has entendido perfectamente.";
            else if (porcentaje >= 60) mensaje = "Bien, pero puedes mejorar.";
            else mensaje = "Necesitas repasar el contenido.";
            
            document.getElementById('resultado1').innerHTML = 
                `<p>Aciertos: ${{aciertos}}/${{total}} (${{porcentaje}}%)</p><p>${{mensaje}}</p>`;
        }}
    </script>
</body>
</html>
```

[ARCHIVO: www/tema-T2.html]
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Tema 2 - Gestión</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .video {{ border-left: 4px solid #28a745; padding: 10px; margin: 10px 0; }}
        .nav {{ background: #f8f9fa; padding: 10px; margin-bottom: 20px; }}
        .quiz {{ background: #e9ecef; padding: 15px; margin-top: 20px; }}
    </style>
</head>
<body>
    <div class="nav">
        <a href="../../index-ollama.html">← Inicio</a> |
        <a href="tema-T1.html">← Tema 1</a>
    </div>
    
    <h1>Tema 2: Gestión de Pacientes</h1>
    
    <div class="video">
        <h3>Video 1: Introducción</h3>
        <p><strong>Resumen:</strong> Conceptos básicos de gestión en la plataforma.</p>
    </div>
    
    <div class="video">
        <h3>Video 2: Agenda de pacientes</h3>
        <p><strong>Resumen:</strong> Cómo manejar las citas y agenda de pacientes.</p>
    </div>
    
    <div class="quiz">
        <h3>Cuestionario</h3>
        <form id="quiz2">
            <p><strong>1. ¿Qué permite hacer el módulo de gestión?</strong></p>
            <input type="radio" name="q1" value="a" data-correct="true"> Manejar citas y pacientes<br>
            <input type="radio" name="q1" value="b"> Solo ver información<br>
            <input type="radio" name="q1" value="c"> Enviar emails<br>
            
            <button type="button" onclick="corregirQuiz2()">Corregir</button>
            <div id="resultado2"></div>
        </form>
    </div>
    
    <script>
        function corregirQuiz2() {{
            const aciertos = document.querySelector('input[name="q1"][data-correct="true"]').checked ? 1 : 0;
            const mensaje = aciertos > 0 ? "¡Correcto!" : "Revisa el contenido.";
            document.getElementById('resultado2').innerHTML = `<p>Resultado: ${{mensaje}}</p>`;
        }}
    </script>
</body>
</html>
```

Genera EXACTAMENTE estos 3 archivos con este formato."""

    return prompt
    """Crea el prompt maestro para generar documentación con las transcripciones"""
    
    prompt = f"""Quiero que actúes como analista y diseñador de material formativo para la plataforma Klinikare / CliniQuer.

Te voy a dar transcripciones de varios vídeos de formación. 
Cada vídeo sigue esta nomenclatura en el nombre de archivo:

- Siempre empieza por "KLC" (de Klinikare / CliniQuer).
- Luego "-T" + número de tema. Ejemplo: T1, T2, T3…
- Luego "-v" + número de vídeo dentro de ese tema. Ejemplo: v1, v2, v3…
- Después del nombre, suele venir un título descriptivo. 
  Ejemplo: "KLC-T1-v1-Introducción a la IA.mp4"

Quiero dos grandes bloques de salida:

1) ANÁLISIS Y SÍNTESIS EN TEXTO
2) GENERACIÓN DE ESTRUCTURA WEB EN HTML (MÚLTIPLES PÁGINAS + QUIZ INTERACTIVO)

--------------------------------
BLOQUE 0 – ENTRADA (TRANSCRIPCIONES)
--------------------------------

Estas son las transcripciones consolidadas que debes analizar:

{transcripciones_consolidadas}

(Nota: las transcripciones ya vienen agrupadas por archivo. Cada bloque empieza con algo parecido a:
"📂 KLC-T1-v1-Introducción a la IA.mp4" seguido del contenido).

--------------------------------
BLOQUE 1 – ANÁLISIS Y SÍNTESIS
--------------------------------

Primero quiero un análisis en texto, SIN generar HTML todavía.

1.1. Identificación de estructura por temas y vídeos
- Detecta todos los temas: T1, T2, T3, etc. a partir de los nombres de archivo (KLC-T{{tema}}-v{{n}}).
- Dentro de cada tema, lista los vídeos en orden (v1, v2, v3…).
- Para cada vídeo, indica:
  - Código: por ejemplo "KLC-T1-v1"
  - Título (si aparece en el nombre)
  - Tema al que pertenece

1.2. Resumen corto por vídeo
Para cada vídeo, genera un resumen muy breve (2–3 frases) que explique:
- De qué trata.
- Qué quiere que aprenda el usuario al final.

1.3. Resumen extendido por vídeo
Para cada vídeo, genera:
- Un resumen en 1–3 párrafos.
- Una lista de 4–8 ideas clave o puntos importantes.
- Opcional: una lista de "errores típicos" o "malos usos" relacionados con el tema, si se deducen del contenido.

1.4. Síntesis global por tema
Para cada tema T1, T2, etc.:
- Explica en 1–2 párrafos cuál es el objetivo del tema.
- Indica el perfil objetivo (por ejemplo: recepción, dirección, clínicos, etc. si se intuye).
- Resume qué sabrá hacer el usuario al terminar el tema.

Haz este BLOQUE 1 en texto estructurado con títulos y subtítulos, pero sin HTML.

Cuando termines el BLOQUE 1, continúa con el BLOQUE 2.

--------------------------------
BLOQUE 2 – GENERACIÓN WEB HTML
--------------------------------

Ahora quiero que conviertas todo esto en una pequeña "web de formación" en HTML, NO en una sola página, sino MULTI-PÁGINA:

REQUISITOS GENERALES:
- Usa solo HTML, CSS y JavaScript puro (sin frameworks).
- No dependas de librerías externas.
- El estilo puede ser sencillo pero ordenado y legible.
- El idioma de la interfaz debe ser ESPAÑOL.
- Respeta la organización por TEMAS (T1, T2…) y vídeos.

2.1. Estructura de archivos HTML a generar

Quiero que me devuelvas el código de estos archivos con esta estructura específica:

📁 ESTRUCTURA DE DIRECTORIOS:
```
/
├── index-openai.html             (Página principal OpenAI - DIRECTORIO RAÍZ)
├── index-ollama.html             (Página principal Ollama - DIRECTORIO RAÍZ)  
└── www/                          (Carpeta para archivos web)
    ├── openai/                   (Archivos generados con OpenAI)
    │   ├── tema-T1.html
    │   ├── tema-T2.html
    │   └── tema-T3.html          (etc.)
    └── ollama/                   (Archivos generados con Ollama)
        ├── tema-T1.html
        ├── tema-T2.html
        └── tema-T3.html          (etc.)
```

📋 ARCHIVOS A GENERAR (cada uno en su bloque de código separado):

1) **index.html** (EN EL DIRECTORIO RAÍZ - se renombrará según el motor)
   - Página de bienvenida y navegación principal
   - Enlaces relativos a los archivos en www/motor/
   - Ejemplo de enlaces: `<a href="www/openai/tema-T1.html">Tema 1</a>` o `<a href="www/ollama/tema-T1.html">Tema 1</a>`

2) **www/tema-T1.html** (se moverán a www/motor/ automáticamente)
3) **www/tema-T2.html** (se moverán a www/motor/ automáticamente)  
4) etc. para todos los temas que aparezcan en las transcripciones.

⚠️ IMPORTANTE PARA LOS ENLACES:
- El index.html está en la raíz, usa rutas: `www/motor/tema-TX.html` (motor será openai u ollama)
- Los archivos tema-TX.html están en www/motor/, usan rutas: `../../index-motor.html` para volver al inicio
- Entre temas: `tema-T1.html`, `tema-T2.html` (sin ../ porque están en la misma carpeta)

IMPORTANTE:
- En cada archivo HTML, incluye el `<head>` completo (doctype, meta charset, título, estilos, etc.).
- Puedes repetir el CSS en cada archivo para simplificar (no pasa nada).
- Usa una misma barra de navegación en todos los archivos con enlaces ADAPTADOS A SU UBICACIÓN:
  
  📍 **Para index.html (en raíz)**:
  - Inicio: # (misma página) 
  - Temas: www/motor/tema-T1.html, www/motor/tema-T2.html, etc. (motor = openai u ollama)
  
  📍 **Para tema-TX.html (en www/motor/)**:
  - Inicio: ../../index-motor.html (motor = openai u ollama)
  - Otros temas: tema-T1.html, tema-T2.html, etc. (sin ../../ porque están en la misma carpeta)

2.2. Contenido de index.html (EN EL DIRECTORIO RAÍZ)

El `index.html` debe ser una portada/resumen con:

- Un título general: "Formación Klinikare / CliniQuer".
- Un pequeño texto explicando:
  - Que los vídeos están organizados por temas.
  - Que cada tema tiene su propia página en la carpeta www/motor/.
  - Que hay cuestionarios tipo test al final de cada tema.
- Una sección "Listado de temas":
  - Una tarjeta por tema (T1, T2, T3…).
  - En cada tarjeta: 
    - Título del tema (resumen breve basado en el análisis).
    - Lista de los vídeos de ese tema (con su código y título).
    - Un botón/enlace a la página de ese tema usando rutas relativas: `www/motor/tema-T1.html`, `www/motor/tema-T2.html`, etc. (donde motor = openai u ollama).
- Opcional: una pequeña nota recordando buenas prácticas para preguntar a la IA (si aplica por los contenidos).

2.3. Contenido de cada página de tema (tema-T1.html, tema-T2.html, etc.)

Para cada página de tema, estructura así:

- Cabecera con:
  - Título: "Tema T{{n}}: [nombre o descripción breve]".
  - Párrafo introductorio con el objetivo del tema (usa la síntesis global del tema).

- Sección "Vídeos del tema":
  - Para cada vídeo de ese tema (por ejemplo KLC-T1-v1, KLC-T1-v2…):
    - Un bloque con:
      - Código y título (ej.: "KLC-T1-v1 – Introducción a la IA").
      - Un resumen corto.
      - Un bloque desplegable (puedes usar `<details><summary>…</summary>…</details>`) con:
        - Resumen extendido del vídeo.
        - Lista de ideas clave.
        - Lista de errores típicos o puntos de atención (si los hay).

- Sección "Manual / Guía rápida del tema":
  - Redacta un pequeño manual en texto (no hace falta HTML complejo, solo `<h3>`, `<p>`, `<ul>`).
  - Enfocado a que alguien pueda leerlo sin ver los vídeos y aún así saber usar lo básico del tema del tema.

- Sección "Cuestionario de autoevaluación (tipo test)":
  - Crea entre 5 y 10 preguntas tipo test por tema.
  - Cada pregunta debe:
    - Estar basada en los contenidos reales de los vídeos del tema.
    - Tener 3 o 4 opciones de respuesta.
    - Indicar internamente cuál es la correcta (para que el JS pueda comprobar).
  - Implementa un formulario sencillo con:
    - Preguntas con opciones tipo `radio`.
    - Un botón "Corregir".
    - Un bloque de resultados que muestre:
      - Cuántas respuestas correctas ha tenido el usuario.
      - Un mensaje general según el porcentaje (ej: "Necesitas repasar", "Bien", "Excelente").
    - Opción: mostrar un pequeño mensaje bajo cada pregunta indicando si esa pregunta se ha respondido bien o mal al corregir.

IMPORTANTE: 
- El JS debe ir al final del `<body>` dentro de `<script>`.
- No uses librerías, solo JavaScript nativo.
- Usa IDs o `data-` atributos para marcar qué opción es correcta.

2.4. Interactividad mínima (JS) para el cuestionario

Quiero un JS genérico que:
- Recorra todas las preguntas del cuestionario del tema.
- Para cada pregunta:
  - Compruebe si la opción seleccionada coincide con la respuesta correcta.
- Cuente el número de aciertos.
- Muestre:
  - Nº de aciertos.
  - Nº de preguntas totales.
  - Un mensaje general según el porcentaje de acierto.
- Opcional: añada a cada pregunta una clase CSS o texto "Correcto" / "Incorrecto".

2.5. Estilo general (CSS)

Mantén un estilo limpio:
- Fondo claro.
- Tipografía sans-serif.
- Contenedores tipo "tarjeta" para cada bloque.
- Barra de navegación sencilla con enlaces a los temas.
- Botones sencillos pero visibles para:
  - "Ir al tema T{{n}}".
  - "Corregir cuestionario".

Con este análisis, genera ahora el análisis completo y la estructura HTML en base a las transcripciones proporcionadas.

--------------------------------
FORMATO DE LA RESPUESTA
--------------------------------

Tu respuesta debe seguir este orden exacto:

**1) BLOQUE 1 – ANÁLISIS Y SÍNTESIS** (solo texto, bien estructurado, sin HTML)

**2) BLOQUE 2 – ARCHIVOS HTML**

Dentro del BLOQUE 2, dame cada archivo HTML en un bloque de código separado usando EXACTAMENTE este formato:

```
[ARCHIVO: index.html]
```html
<!DOCTYPE html>
<html lang="es">
...código completo del index.html...
```

[ARCHIVO: www/tema-T1.html]
```html
<!DOCTYPE html>
<html lang="es">
...código completo del tema T1...
```

[ARCHIVO: www/tema-T2.html]
```html
<!DOCTYPE html>
<html lang="es">
...código completo del tema T2...
```

Y así sucesivamente para cada tema detectado.

🔥 INSTRUCCIONES CRÍTICAS:
1. **SIEMPRE** genera un archivo index.html
2. **SIEMPRE** genera un archivo tema-TX.html por CADA tema que detectes (T1, T2, T3, etc.)
3. **NO OMITAS** ningún tema
4. **USA EXACTAMENTE** el formato [ARCHIVO: nombre] antes de cada ```html
5. **INCLUYE TODO** el código HTML completo en cada archivo
6. **VERIFICA** que generas al menos 2 archivos (index + al menos 1 tema)

Si detectas 3 temas (T1, T2, T3), debes generar 4 archivos:
- [ARCHIVO: index.html]
- [ARCHIVO: www/tema-T1.html] 
- [ARCHIVO: www/tema-T2.html]
- [ARCHIVO: www/tema-T3.html]

⚠️ IMPORTANTE:
- Usa EXACTAMENTE el formato [ARCHIVO: nombre] antes de cada bloque
- Para el index.html usa: [ARCHIVO: index.html]
- Para los temas usa: [ARCHIVO: www/tema-TX.html]
- DEBES generar UN ARCHIVO POR CADA TEMA detectado en las transcripciones
- Incluye el código HTML completo con DOCTYPE, head, body, estilos CSS y JavaScript
- Asegúrate de que las rutas de navegación sean correctas según la estructura de directorios
- NO omitas ningún tema, genera TODOS los archivos HTML necesarios

🔥 REQUISITO CRÍTICO: Debes generar:
1. Un archivo index.html
2. Un archivo tema-TX.html por cada tema T1, T2, T3, etc. que detectes
3. Cada tema debe tener su página completa con navegación, contenido y cuestionario

Ejemplo de salida esperada si hay 2 temas:
- [ARCHIVO: index.html] + código HTML
- [ARCHIVO: www/tema-T1.html] + código HTML  
- [ARCHIVO: www/tema-T2.html] + código HTML"""

    return prompt

def procesar_y_guardar_html(contenido_respuesta, carpeta_base, carpeta_www, motor):
    """Extrae y guarda los archivos HTML de la respuesta de IA"""
    archivos_creados = []
    
    try:
        import re
        
        print(f"🔍 Procesando respuesta del motor: {motor}")
        print(f"📁 Carpeta base: {carpeta_base}")
        print(f"📁 Carpeta www: {carpeta_www}")
        print(f"📄 Tamaño de respuesta: {len(contenido_respuesta)} caracteres")
        
        # Patrón principal para encontrar bloques con formato [ARCHIVO: nombre]
        # Mejorado para detectar archivos aunque no estén perfectamente cerrados
        patron_html = r'\[ARCHIVO:\s*([^\]]+)\]\s*```html\s*(.*?)(?=```|\[ARCHIVO:|$)'
        matches = re.findall(patron_html, contenido_respuesta, re.DOTALL | re.IGNORECASE)
        
        print(f"📄 Archivos encontrados con patrón principal: {len(matches)}")
        
        for i, (nombre_archivo, codigo_html) in enumerate(matches):
            nombre_archivo = nombre_archivo.strip()
            print(f"   📋 Procesando: {nombre_archivo}")
            
            # Determinar la ruta según el archivo y motor
            if "index" in nombre_archivo.lower():
                ruta_archivo = carpeta_base / f"index-{motor}.html"
                print(f"      → Guardando como: {ruta_archivo.name}")
            elif nombre_archivo.startswith("www/fase-") or nombre_archivo.startswith("fase-"):
                # Extraer solo el nombre de la fase
                if nombre_archivo.startswith("www/"):
                    fase_nombre = nombre_archivo.replace("www/", "")
                else:
                    fase_nombre = nombre_archivo
                ruta_archivo = carpeta_www / fase_nombre
                print(f"      → Guardando como: www/{motor}/{fase_nombre}")
            else:
                # Por defecto en la carpeta del motor
                ruta_archivo = carpeta_www / nombre_archivo
                print(f"      → Guardando como: www/{motor}/{nombre_archivo}")
            
            # Actualizar enlaces en el HTML
            codigo_html_actualizado = actualizar_enlaces_html(codigo_html, motor, nombre_archivo)
            
            # Crear directorio padre si no existe
            ruta_archivo.parent.mkdir(parents=True, exist_ok=True)
            
            # Guardar el archivo
            with open(ruta_archivo, 'w', encoding='utf-8') as f:
                f.write(codigo_html_actualizado.strip())
            
            archivos_creados.append(str(ruta_archivo.relative_to(carpeta_base)))
            print(f"      ✅ Guardado: {ruta_archivo.relative_to(carpeta_base)}")
        
        # Si no encontramos archivos con el patrón principal, intentar patrones alternativos
        if not archivos_creados:
            print("⚠️ No se encontraron archivos con formato [ARCHIVO:], probando patrones alternativos...")
            
            # Patrón específico para DeepSeek: ```html [ARCHIVO: nombre] ``` seguido de código
            patron_deepseek = r'```html\s*\[ARCHIVO:\s*([^\]]+)\]\s*```\s*```html\s*(.*?)(?=```(?:html)?(?:\s*\[ARCHIVO:|$))'
            matches_deepseek = re.findall(patron_deepseek, contenido_respuesta, re.DOTALL | re.IGNORECASE)
            
            if matches_deepseek:
                print(f"📄 Archivos encontrados con patrón DeepSeek: {len(matches_deepseek)}")
                matches = matches_deepseek
            else:
                # Buscar bloques HTML sin etiquetas de archivo
                patron_alternativo = r'```html\s*(<!DOCTYPE[^`]+?)```'
                matches_alt = re.findall(patron_alternativo, contenido_respuesta, re.DOTALL | re.IGNORECASE)
                
                print(f"📄 Archivos encontrados con patrón alternativo: {len(matches_alt)}")
                
                # Convertir a formato compatible
                matches = []
                for i, codigo_html in enumerate(matches_alt):
                    if i == 0:
                        matches.append(("index.html", codigo_html))
                    else:
                        matches.append((f"fase-F{i}.html", codigo_html))
            
            # Procesar archivos encontrados con patrones alternativos
            for nombre_archivo, codigo_html in matches:
                if i == 0:
                    # Primer archivo es el index
                    ruta_archivo = carpeta_base / f"index-{motor}.html"
                    nombre_archivo = "index.html"
                else:
                    # Siguientes archivos son fases
                    ruta_archivo = carpeta_www / f"fase-F{i}.html"
                    nombre_archivo = f"fase-F{i}.html"
                
                print(f"   📋 Procesando archivo {i+1}: {ruta_archivo.name}")
                
                codigo_html_actualizado = actualizar_enlaces_html(codigo_html, motor, nombre_archivo)
                
                # Crear directorio padre si no existe
                ruta_archivo.parent.mkdir(parents=True, exist_ok=True)
                
                with open(ruta_archivo, 'w', encoding='utf-8') as f:
                    f.write(codigo_html_actualizado.strip())
                
                archivos_creados.append(str(ruta_archivo.relative_to(carpeta_base)))
                print(f"      ✅ Guardado: {ruta_archivo.relative_to(carpeta_base)}")
        
        # Si aún no tenemos archivos, mostrar parte del contenido para debug
        if not archivos_creados:
            print("❌ No se pudieron extraer archivos HTML de la respuesta")
            print("🔍 Primeros 1000 caracteres de la respuesta:")
            print(contenido_respuesta[:1000])
            print("...")
            
            # Crear al menos un archivo index básico
            print("🆘 Creando archivo index básico como respaldo...")
            ruta_index = carpeta_base / f"index-{motor}-error.html"
            with open(ruta_index, 'w', encoding='utf-8') as f:
                f.write(f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Error - Documentación {motor.upper()}</title>
</head>
<body>
    <h1>Error al generar documentación</h1>
    <p>No se pudieron extraer los archivos HTML de la respuesta de {motor}.</p>
    <p>Revisa el archivo de documentación .md para ver la respuesta completa.</p>
</body>
</html>""")
            archivos_creados.append(str(ruta_index.relative_to(carpeta_base)))
        
        print(f"📊 Total de archivos creados: {len(archivos_creados)}")
    
    except Exception as e:
        print(f"❌ Error al procesar archivos HTML: {str(e)}")
        import traceback
        traceback.print_exc()
    
    return archivos_creados

def actualizar_enlaces_html(codigo_html, motor, nombre_archivo):
    """Actualiza los enlaces del HTML según el motor y estructura de carpetas"""
    import re
    
    # Si es el index, actualizar enlaces a fases
    if "index" in nombre_archivo:
        # Patrones para enlaces a fases desde el index
        # Convertir "fase-F1.html" -> "www/motor/fase-F1.html"
        codigo_html = re.sub(r'href="(fase-F\d+\.html)"', rf'href="www/{motor}/\1"', codigo_html)
        codigo_html = re.sub(r"href='(fase-F\d+\.html)'", rf"href='www/{motor}/\1'", codigo_html)
        
        # También para temas si existen
        codigo_html = re.sub(r'href="(tema-T\d+\.html)"', rf'href="www/{motor}/\1"', codigo_html)
        codigo_html = re.sub(r"href='(tema-T\d+\.html)'", rf"href='www/{motor}/\1'", codigo_html)
        
        # Enlaces entre index de diferentes motores (mantener como están)
        # Enlaces de navegación en index (mantener relativos)
        
    else:
        # Si es una fase/tema, actualizar enlaces al index y entre fases
        
        # Enlaces al index desde subcarpetas www/motor/
        codigo_html = re.sub(r'href="index\.html"', rf'href="../../index-{motor}.html"', codigo_html)
        codigo_html = re.sub(r"href='index\.html'", rf"href='../../index-{motor}.html'", codigo_html)
        
        # Enlaces entre fases en la misma carpeta (ya están bien, mantener)
        # Los enlaces tipo "fase-F2.html" desde www/motor/fase-F1.html están correctos
        
        # Enlaces de navegación en el nav entre fases 
        codigo_html = re.sub(r'href="(fase-F\d+\.html)"', rf'href="\1"', codigo_html)
        codigo_html = re.sub(r"href='(fase-F\d+\.html)'", rf"href='\1'", codigo_html)
    
    return codigo_html

def validar_respuesta_completa(contenido_respuesta, transcripciones_content):
    """Valida que la respuesta contenga todos los archivos HTML necesarios"""
    
    import re
    
    # Detectar cuántas fases hay en las transcripciones
    fases_encontradas = set()
    patron_fases = r'📂\s+KK-F(\d+)-v\d+'
    matches = re.findall(patron_fases, transcripciones_content)
    
    for match in matches:
        fases_encontradas.add(f"F{match}")
    
    print(f"🔍 Fases detectadas en transcripciones: {sorted(fases_encontradas)}")
    
    # Buscar archivos HTML en la respuesta
    patron_archivos = r'\[ARCHIVO:\s*([^\]]+)\]'
    archivos_en_respuesta = re.findall(patron_archivos, contenido_respuesta, re.IGNORECASE)
    
    print(f"📋 Archivos encontrados en respuesta: {archivos_en_respuesta}")
    
    # Verificar que tenemos index
    tiene_index = any("index" in archivo.lower() for archivo in archivos_en_respuesta)
    
    # Verificar que tenemos todas las fases
    fases_en_respuesta = set()
    for archivo in archivos_en_respuesta:
        match_fase = re.search(r'fase-(F\d+)', archivo, re.IGNORECASE)
        if match_fase:
            fases_en_respuesta.add(match_fase.group(1))
    
    print(f"🎯 Fases en respuesta HTML: {sorted(fases_en_respuesta)}")
    
    # Calcular qué falta
    fases_faltantes = fases_encontradas - fases_en_respuesta
    
    if not tiene_index:
        print("⚠️ FALTA: Archivo index.html")
    
    if fases_faltantes:
        print(f"⚠️ FALTAN fases: {sorted(fases_faltantes)}")
    
    if tiene_index and not fases_faltantes:
        print("✅ Respuesta completa: index + todas las fases")
        return True
    else:
        print("❌ Respuesta incompleta")
        return False

def generar_documentacion_con_openai(transcripciones_file):
    """Genera documentación usando OpenAI con las transcripciones consolidadas"""
    
    try:
        # Leer el archivo de transcripciones consolidadas
        with open(transcripciones_file, 'r', encoding='utf-8') as f:
            transcripciones_content = f.read()
        
        print("🤖 Generando documentación con OpenAI...")
        print(f"📄 Procesando: {transcripciones_file.name}")
        
        # Crear el prompt maestro original del usuario
        prompt = crear_prompt_maestro_original(transcripciones_content)
        
        # Medir tiempo de generación
        inicio_tiempo = time.time()
        print("⏱️  Enviando solicitud a OpenAI GPT-4o...")
        
        # Llamada a OpenAI
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Eres un experto analista de contenido formativo y diseñador de material educativo. Generas análisis detallados y documentación web interactiva de alta calidad. CRÍTICO: Siempre genera TODOS los archivos HTML solicitados sin excepción. Si hay múltiples fases, crea una página HTML para CADA fase. Nunca truncar la respuesta."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=16384,  # Máximo permitido por GPT-4o
            temperature=0.1
        )
        
        # Calcular tiempo transcurrido
        tiempo_transcurrido = time.time() - inicio_tiempo
        print(f"✅ Respuesta recibida en {tiempo_transcurrido:.2f} segundos")
        
        # Crear estructura de directorios para la documentación web
        timestamp = transcripciones_file.stem.replace('transcripciones_', '')
        carpeta_base = transcripciones_file.parent.parent  # Directorio raíz del proyecto
        carpeta_www_openai = carpeta_base / "www" / "openai"
        carpeta_www_openai.mkdir(parents=True, exist_ok=True)
        
        print(f"📁 Creando estructura web OpenAI:")
        print(f"   📄 index-openai.html → {carpeta_base}")
        print(f"   🌐 archivos tema → {carpeta_www_openai}")
        
        # Guardar la documentación completa en markdown
        documentacion_file = transcripciones_file.parent / f"documentacion_openai_{timestamp}.md"
        
        with open(documentacion_file, 'w', encoding='utf-8') as f:
            f.write("# DOCUMENTACIÓN GENERADA AUTOMÁTICAMENTE\n\n")
            f.write(f"**Generado el:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Motor:** OpenAI (GPT-4o)\n")
            f.write(f"**Tiempo de generación:** {tiempo_transcurrido:.2f} segundos\n")
            f.write(f"**Archivo fuente:** {transcripciones_file.name}\n\n")
            f.write("**Estructura web generada:**\n")
            f.write(f"- `index-openai.html` → Directorio raíz del proyecto\n")
            f.write(f"- `www/openai/tema-TX.html` → Carpeta www/openai/ del proyecto\n\n")
            f.write("---\n\n")
            f.write(response.choices[0].message.content)
        
        # Verificar si la respuesta está completa y solicitar continuación si es necesario
        respuesta_contenido = response.choices[0].message.content
        
        # Detectar si OpenAI truncó la respuesta
        if not respuesta_contenido.strip().endswith('```') and '[ARCHIVO:' in respuesta_contenido:
            print("⚠️ Respuesta posiblemente truncada, solicitando continuación...")
            
            # Solicitar continuación
            continuation_response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "Continúa generando EXACTAMENTE donde te quedaste. Completa todos los archivos HTML faltantes."},
                    {"role": "user", "content": prompt},
                    {"role": "assistant", "content": respuesta_contenido},
                    {"role": "user", "content": "Por favor continúa generando el resto de archivos HTML que faltan. Usa el mismo formato [ARCHIVO: nombre] ```html ... ``` para cada archivo."}
                ],
                max_tokens=16384,  # Máximo permitido por GPT-4o
                temperature=0.1
            )
            
            # Combinar respuestas
            respuesta_continuacion = continuation_response.choices[0].message.content
            respuesta_contenido = respuesta_contenido + "\n\n" + respuesta_continuacion
            print("✅ Continuación recibida y combinada")
        
        # Crear hash único de la respuesta para debugging
        import hashlib
        hash_respuesta = hashlib.md5(respuesta_contenido.encode()).hexdigest()[:8]
        print(f"🔍 Hash único de respuesta OpenAI: {hash_respuesta}")
        
        # Validar que la respuesta esté completa
        respuesta_completa = validar_respuesta_completa(respuesta_contenido, transcripciones_content)
        
        archivos_creados = procesar_y_guardar_html(respuesta_contenido, carpeta_base, carpeta_www_openai, "openai")
        
        print(f"✅ Documentación generada exitosamente!")
        print(f"📋 Archivo de análisis: {documentacion_file}")
        print(f"🌐 Archivos web creados: {len(archivos_creados)}")
        
        if archivos_creados:
            for archivo in archivos_creados:
                print(f"   📄 {archivo}")
        else:
            print("⚠️ No se crearon archivos HTML. Revisa el archivo .md para la respuesta completa.")
        
        return documentacion_file
        
    except Exception as e:
        print(f"❌ Error al generar documentación: {str(e)}")
        return None

def generar_documentacion_con_ollama(transcripciones_file):
    """Genera documentación usando Ollama local con las transcripciones consolidadas"""
    
    try:
        # Verificar que Ollama esté disponible
        ollama_host = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
        ollama_model = os.getenv('OLLAMA_MODEL', 'llama2')
        
        print(f"🤖 Generando documentación con Ollama (modelo: {ollama_model})...")
        print(f"📶 Host: {ollama_host}")
        
        # Verificar que el modelo esté disponible
        try:
            modelos_disponibles = ollama.list()
            modelo_encontrado = any(modelo.model.startswith(ollama_model) for modelo in modelos_disponibles.models)
            
            if not modelo_encontrado:
                print(f"⚠️ Modelo {ollama_model} no encontrado. Modelos disponibles:")
                for modelo in modelos_disponibles.models:
                    print(f"   - {modelo.model}")
                
                # Intentar descargar el modelo
                print(f"📥 Descargando modelo {ollama_model}...")
                ollama.pull(ollama_model)
                
        except Exception as e:
            print(f"⚠️ No se pudo verificar los modelos de Ollama: {str(e)}")
            print("Asegúrate de que Ollama esté ejecutándose: ollama serve")
            return None
        
        # Leer el archivo de transcripciones consolidadas
        with open(transcripciones_file, 'r', encoding='utf-8') as f:
            transcripciones_content = f.read()
        
        print(f"📄 Procesando: {transcripciones_file.name}")
        
        # Crear el prompt maestro original del usuario
        prompt = crear_prompt_maestro_original(transcripciones_content)
        
        # Medir tiempo de generación
        inicio_tiempo = time.time()
        
        # Llamada a Ollama con timeout y configuración optimizada
        print("🧠 Generando análisis... (esto puede tardar 10-15 minutos con Ollama)")
        print("⏱️  El modelo gpt-oss es muy potente pero requiere tiempo...")
        
        try:
            response = ollama.chat(
                model=ollama_model,
                messages=[
                    {
                        'role': 'system',
                        'content': 'Eres un experto analista de contenido formativo. Genera documentación web HTML completa siguiendo EXACTAMENTE el formato solicitado con [ARCHIVO: nombre] antes de cada código HTML.'
                    },
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ],
                options={
                    'temperature': 0.1,  # Más determinista
                    'top_p': 0.9,
                    'num_ctx': 16384,  # Contexto más amplio
                    'num_predict': 8192,  # Más tokens de salida
                    'repeat_penalty': 1.1,
                    'stop': []  # Sin paradas automáticas
                }
            )
            
            # Calcular tiempo transcurrido
            tiempo_transcurrido = time.time() - inicio_tiempo
            print(f"✅ Respuesta de Ollama recibida en {tiempo_transcurrido/60:.1f} minutos ({tiempo_transcurrido:.0f}s)")
            
        except Exception as e:
            print(f"❌ Error en llamada a Ollama: {str(e)}")
            if "timeout" in str(e).lower():
                print("⏱️  El modelo tardó más de lo esperado. Considera:")
                print("   - Usar un modelo más pequeño (llama2:7b)")
                print("   - Procesar transcripciones más cortas")
                print("   - Aumentar la RAM disponible")
            return None
        
        # Crear estructura de directorios para la documentación web
        timestamp = transcripciones_file.stem.replace('transcripciones_', '')
        carpeta_base = transcripciones_file.parent.parent  # Directorio raíz del proyecto
        carpeta_www_ollama = carpeta_base / "www" / "ollama"
        carpeta_www_ollama.mkdir(parents=True, exist_ok=True)
        
        print(f"📁 Creando estructura web Ollama:")
        print(f"   📄 index-ollama.html → {carpeta_base}")
        print(f"   🌐 archivos tema → {carpeta_www_ollama}")
        
        # Guardar la documentación completa en markdown
        documentacion_file = transcripciones_file.parent / f"documentacion_ollama_{timestamp}.md"
        
        with open(documentacion_file, 'w', encoding='utf-8') as f:
            f.write("# DOCUMENTACIÓN GENERADA CON OLLAMA\n\n")
            f.write(f"**Generado el:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Motor:** Ollama ({ollama_model})\n")
            f.write(f"**Tiempo de generación:** {tiempo_transcurrido/60:.1f} minutos ({tiempo_transcurrido:.0f}s)\n")
            f.write(f"**Archivo fuente:** {transcripciones_file.name}\n\n")
            f.write("**Estructura web generada:**\n")
            f.write(f"- `index-ollama.html` → Directorio raíz del proyecto\n")
            f.write(f"- `www/ollama/tema-TX.html` → Carpeta www/ollama/ del proyecto\n\n")
            f.write("---\n\n")
            f.write(response['message']['content'])
        
        # Validar que la respuesta de Ollama sea válida
        if not response or 'message' not in response or 'content' not in response['message']:
            print("❌ Respuesta vacía o inválida de Ollama")
            return None
            
        respuesta_contenido = response['message']['content']
        
        # Crear hash único de la respuesta para debugging
        import hashlib
        hash_respuesta = hashlib.md5(respuesta_contenido.encode()).hexdigest()[:8]
        print(f"🔍 Hash único de respuesta Ollama: {hash_respuesta}")
        
        # Verificar que la respuesta no esté vacía
        if not respuesta_contenido or len(respuesta_contenido.strip()) < 100:
            print("❌ Respuesta de Ollama muy corta o vacía")
            print(f"📏 Longitud recibida: {len(respuesta_contenido) if respuesta_contenido else 0} caracteres")
            return None
            
        print(f"✅ Respuesta recibida: {len(respuesta_contenido)} caracteres")
        
        # Validar que la respuesta esté completa
        respuesta_completa = validar_respuesta_completa(respuesta_contenido, transcripciones_content)
        
        archivos_creados = procesar_y_guardar_html(respuesta_contenido, carpeta_base, carpeta_www_ollama, "ollama")
        
        print(f"✅ Documentación generada exitosamente!")
        print(f"📋 Archivo de análisis: {documentacion_file}")
        print(f"🌐 Archivos web creados: {len(archivos_creados)}")
        
        if archivos_creados:
            for archivo in archivos_creados:
                print(f"   📄 {archivo}")
        else:
            print("⚠️ No se crearon archivos HTML. Revisa el archivo .md para la respuesta completa.")
        
        return documentacion_file
        
    except Exception as e:
        print(f"❌ Error al generar documentación con Ollama: {str(e)}")
        print("💡 Sugerencias:")
        print("   - Verifica que Ollama esté instalado: ollama --version")
        print("   - Inicia Ollama: ollama serve")
        print("   - Descarga un modelo: ollama pull llama2")
        return None
    """Extrae y guarda los archivos HTML de la respuesta de OpenAI"""
    archivos_creados = []
    
    try:
        # Buscar bloques de código HTML en la respuesta
        import re
        
        # Patrón para encontrar bloques de código HTML con nombres de archivo
        patron_html = r'\[ARCHIVO:\s*([^\]]+)\]\s*```html\s*(.*?)```'
        matches = re.findall(patron_html, contenido_respuesta, re.DOTALL | re.IGNORECASE)
        
        for nombre_archivo, codigo_html in matches:
            nombre_archivo = nombre_archivo.strip()
            
            # Determinar la ruta según el archivo
            if nombre_archivo == "index.html":
                ruta_archivo = carpeta_base / nombre_archivo
            elif nombre_archivo.startswith("tema-"):
                ruta_archivo = carpeta_www / nombre_archivo
            else:
                # Por defecto, ponerlo en www/
                ruta_archivo = carpeta_www / nombre_archivo
            
            # Guardar el archivo
            with open(ruta_archivo, 'w', encoding='utf-8') as f:
                f.write(codigo_html.strip())
            
            archivos_creados.append(str(ruta_archivo.relative_to(carpeta_base)))
        
        # Si no encontramos archivos con el patrón anterior, intentar otro patrón
        if not archivos_creados:
            patron_alternativo = r'```html\s*(<!DOCTYPE[^`]+)```'
            matches_alt = re.findall(patron_alternativo, contenido_respuesta, re.DOTALL | re.IGNORECASE)
            
            for i, codigo_html in enumerate(matches_alt):
                if i == 0:
                    # Primer archivo es el index.html
                    ruta_archivo = carpeta_base / "index.html"
                else:
                    # Siguientes archivos son temas
                    ruta_archivo = carpeta_www / f"tema-T{i}.html"
                
                with open(ruta_archivo, 'w', encoding='utf-8') as f:
                    f.write(codigo_html.strip())
                
                archivos_creados.append(str(ruta_archivo.relative_to(carpeta_base)))
    
    except Exception as e:
        print(f"⚠️ Error al procesar archivos HTML: {str(e)}")
    
    return archivos_creados

def preguntar_generar_documentacion():
    """Pregunta al usuario si quiere generar documentación y con qué motor"""
    
    print("\n" + "="*70)
    print("🤖 GENERACIÓN DE DOCUMENTACIÓN CON IA")
    print("="*70)
    print("¿Deseas generar documentación automática de los videos?")
    print("📋 Incluirá:")
    print("   - Análisis detallado por video y tema")
    print("   - Manual de referencia rápida")
    print("   - Páginas HTML interactivas")
    print("   - Cuestionarios tipo test")
    print("   - Navegación entre temas")
    
    while True:
        respuesta = input("\n¿Generar documentación? (s/n): ").lower().strip()
        if respuesta in ['s', 'si', 'sí', 'y', 'yes']:
            # Preguntar qué motor usar
            return elegir_motor_documentacion()
        elif respuesta in ['n', 'no']:
            return None
        else:
            print("Por favor, responde 's' para sí o 'n' para no.")

def generar_documentacion_con_deepseek(transcripciones_file):
    """
    Generar documentación usando Ollama con modelo DeepSeek-R1
    
    Args:
        transcripciones_file: Path al archivo de transcripciones
    
    Returns:
        bool: True si se genera correctamente, False en caso de error
    """
    print("📶 Host: http://localhost:11434")
    
    import ollama
    import time
    
    deepseek_model = "deepseek-r1:latest"
    
    try:
        # Leer transcripciones
        with open(transcripciones_file, 'r', encoding='utf-8') as f:
            transcripciones_content = f.read()
        
        print(f"📄 Procesando: {transcripciones_file.name}")
        
        # Crear el prompt maestro original del usuario
        prompt = crear_prompt_maestro_original(transcripciones_content)
        
        # Medir tiempo de generación
        inicio_tiempo = time.time()
        
        # Llamada a Ollama con DeepSeek-R1
        print("🧠 Generando análisis... (esto puede tardar 5-10 minutos con DeepSeek-R1)")
        print("⏱️  El modelo DeepSeek-R1 es muy avanzado y eficiente...")
        
        try:
            response = ollama.chat(
                model=deepseek_model,
                messages=[
                    {
                        'role': 'system',
                        'content': 'Eres un experto analista de contenido formativo. Genera documentación web HTML completa siguiendo EXACTAMENTE el formato solicitado con [ARCHIVO: nombre] antes de cada código HTML.'
                    },
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ],
                options={
                    'temperature': 0.1,  # Más determinista
                    'top_p': 0.9,
                    'num_ctx': 32768,  # Contexto más amplio para DeepSeek
                    'num_predict': 16384,  # Más tokens de salida
                    'repeat_penalty': 1.1,
                    'stop': []  # Sin paradas automáticas
                }
            )
            
            # Calcular tiempo transcurrido
            tiempo_transcurrido = time.time() - inicio_tiempo
            print(f"✅ Respuesta de DeepSeek recibida en {tiempo_transcurrido/60:.1f} minutos ({tiempo_transcurrido:.0f}s)")
            
        except Exception as e:
            print(f"❌ Error en llamada a DeepSeek: {str(e)}")
            if "timeout" in str(e).lower():
                print("⏱️  El modelo tardó más de lo esperado. Considera:")
                print("   - Procesar transcripciones más cortas")
                print("   - Verificar disponibilidad del modelo DeepSeek-R1")
            return False
        
        # Crear estructura web
        print("📁 Creando estructura web DeepSeek:")
        print("   📄 index-deepseek.html → .")
        print("   🌐 archivos tema → www\\deepseek")
        
        # Generar hash único de la respuesta
        import hashlib
        contenido_respuesta = response['message']['content']
        hash_respuesta = hashlib.md5(contenido_respuesta.encode()).hexdigest()[:8]
        print(f"🔍 Hash único de respuesta DeepSeek: {hash_respuesta}")
        
        print(f"✅ Respuesta recibida: {len(contenido_respuesta)} caracteres")
        
        # Validar completitud usando la función existente
        respuesta_completa = validar_respuesta_completa(contenido_respuesta, transcripciones_content)
        if respuesta_completa:
            print("✅ Respuesta completa: index + todas las fases")
        else:
            print("⚠️ Respuesta posiblemente incompleta")
        
        # Procesar respuesta y crear archivos
        exito = procesar_y_guardar_html(contenido_respuesta, pathlib.Path("."), pathlib.Path("www/deepseek"), "deepseek")
        
        if exito:
            # Guardar archivo de análisis completo
            fecha_actual = datetime.now().strftime("%Y%m%d_%H%M%S")
            archivo_analisis = f"procesados/documentacion_deepseek_{fecha_actual}.md"
            
            with open(archivo_analisis, 'w', encoding='utf-8') as f:
                f.write("# DOCUMENTACIÓN GENERADA CON DEEPSEEK-R1\n\n")
                f.write(f"**Generado el:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"**Motor:** Ollama (DeepSeek-R1)\n")
                f.write(f"**Tiempo de generación:** {tiempo_transcurrido/60:.1f} minutos ({tiempo_transcurrido:.0f}s)\n")
                f.write(f"**Archivo fuente:** {transcripciones_file.name}\n\n")
                f.write("**Estructura web generada:**\n")
                f.write("- `index-deepseek.html` → Directorio raíz del proyecto\n")
                f.write("- `www/deepseek/tema-TX.html` → Carpeta www/deepseek/ del proyecto\n\n")
                f.write("---\n\n")
                f.write(contenido_respuesta)
            
            print(f"📋 Archivo de análisis: {archivo_analisis}")
            
        return True
    
    except Exception as e:
        print(f"❌ Error durante el procesamiento con DeepSeek: {str(e)}")
        return False

def elegir_motor_documentacion():
    """Permite al usuario elegir entre OpenAI y Ollama"""
    
    print("\n" + "-"*50)
    print("⚙️ ¿Con qué motor quieres generar la documentación?")
    print("-"*50)
    print("🌐 [1] OpenAI (GPT-4o)")
    print("   ✅ Ventajas: Máxima calidad, rápido, muy avanzado")
    print("   ❌ Desventajas: Requiere API key, de pago")
    print("   💰 Coste estimado: ~$0.10-0.30 por análisis")
    print()
    print("🏠 [2] Ollama (Local)")
    print("   ✅ Ventajas: GRATIS, privado, funciona sin internet")
    print("   ❌ Desventajas: Más lento, requiere instalación")
    print(f"   🤖 Modelo configurado: {os.getenv('OLLAMA_MODEL', 'gpt-oss')} (13GB)")
    print("   ⚡ Velocidad: 5-10 minutos por análisis")
    print()
    
    while True:
        opcion = input("¿Elige una opción (1/2): ").strip()
        if opcion == '1':
            return 'openai'
        elif opcion == '2':
            return 'ollama'
        else:
            print("Por favor, elige '1' para OpenAI o '2' para Ollama.")

def main():
    base = pathlib.Path(__file__).parent
    carpeta_videos = base / "videos"
    carpeta_procesados = base / "procesados"
    transcribir_archivos(carpeta_videos, carpeta_procesados)

if __name__ == "__main__":
    main()