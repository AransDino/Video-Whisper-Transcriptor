def crear_prompt_documentacion_mejorado(transcripciones_consolidadas):
    """Crea el prompt maestro para generar una guía de formación interactiva moderna"""
    
    prompt = f"""Eres un experto diseñador de materiales educativos y plataformas de e-learning para empresas. Tu misión es crear una GUÍA DE FORMACIÓN Y ESTUDIO INTERACTIVA de alta calidad para Klinikare / CliniQuer.

🎯 OBJETIVO PRINCIPAL: Crear una plataforma web de formación profesional que sirva como:
- Guía de estudio completa y estructurada
- Material de consulta rápida para empleados
- Sistema de autoevaluación y seguimiento del aprendizaje
- Recurso de onboarding para nuevos usuarios
- Manual de referencia interactivo

Te voy a dar transcripciones de varios vídeos de formación empresarial. 
Cada vídeo sigue esta nomenclatura: KLC-T{{tema}}-v{{video}}-{{título}}

Quiero dos grandes bloques de salida:

1) ANÁLISIS EDUCATIVO Y ESTRUCTURACIÓN PEDAGÓGICA
2) PLATAFORMA WEB DE FORMACIÓN INTERACTIVA (DISEÑO MODERNO + FUNCIONALIDADES EDUCATIVAS)

--------------------------------
BLOQUE 0 – ENTRADA (TRANSCRIPCIONES)
--------------------------------

{transcripciones_consolidadas}

--------------------------------
BLOQUE 1 – ANÁLISIS EDUCATIVO Y ESTRUCTURACIÓN PEDAGÓGICA
--------------------------------

1.1. Mapa de contenidos educativos (formato tabla)
Crea una tabla con todos los vídeos:

| Código | Título | Tema | Nivel | Duración Est. |
|--------|--------|------|-------|---------------|
| KLC-T1-v1 | ... | T1: IA | Básico | 15 min |

1.2. Objetivos de aprendizaje por vídeo
Para cada vídeo:
- **Objetivo principal**: ¿Qué va a aprender?
- **Competencias**: Habilidades que desarrollará
- **Prerequisitos**: Conocimientos previos
- **Resultados**: Qué sabrá hacer al terminar

1.3. Contenido pedagógico detallado
Para cada vídeo:
- **Resumen ejecutivo**: 2-3 frases clave
- **Desarrollo**: Explicación detallada educativa
- **Conceptos clave**: 5-8 puntos fundamentales
- **Aplicación práctica**: Casos de uso reales
- **Errores comunes**: Problemas frecuentes
- **Tips profesionales**: Consejos avanzados

1.4. Estructura curricular por módulo
Para cada tema T1, T2, etc.:
- **Descripción del módulo**
- **Perfil del estudiante objetivo**
- **Duración total estimada**
- **Competencias que desarrollará**

--------------------------------
BLOQUE 2 – PLATAFORMA WEB DE FORMACIÓN INTERACTIVA
--------------------------------

🎨 ESPECIFICACIONES DE DISEÑO:
- Diseño moderno estilo plataforma educativa (tipo Coursera/Udemy)
- Layout responsivo con CSS Grid y Flexbox
- Paleta: Azul corporativo (#2563eb) + Verde éxito (#16a34a) + Gris moderno (#64748b)
- Tipografía: Inter/system-ui con jerarquía clara (h1: 2.5rem, h2: 2rem, h3: 1.5rem)
- Cards elevados con sombras sutiles
- Iconografía educativa con emojis Unicode
- Animaciones CSS (hover, transiciones, loading states)
- Sistema de navegación con breadcrumbs
- Progress bars para seguimiento

🧩 COMPONENTES EDUCATIVOS REQUERIDOS:
- **Dashboard principal**: Resumen de progreso, módulos disponibles
- **Cards de módulo**: Con progress bar, duración, nivel de dificultad
- **Timeline de lecciones**: Progresión visual del aprendizaje
- **Área de contenido**: Layout de 2 columnas (contenido + navegación)
- **Cuestionarios avanzados**: Con feedback inmediato y explicaciones
- **Sistema de puntuación**: Badges, achievements, porcentajes
- **Notas y resúmenes**: Área para apuntes del estudiante
- **Glosario integrado**: Términos clave con definiciones

📋 ARCHIVOS A GENERAR:

[ARCHIVO: index.html] - Dashboard principal
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>📚 Campus Virtual - Klinikare</title>
    <style>
        /* VARIABLES CSS */
        :root {{
            --primary: #2563eb;
            --success: #16a34a;
            --warning: #f59e0b;
            --gray: #64748b;
            --light-gray: #f8fafc;
            --dark: #1e293b;
            --shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
            --radius: 8px;
        }}
        
        /* RESET Y LAYOUT PRINCIPAL */
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: 'Inter', system-ui, sans-serif; 
            line-height: 1.6; 
            color: var(--dark);
            background: var(--light-gray);
        }}
        
        /* HEADER */
        .header {{
            background: linear-gradient(135deg, var(--primary), #3b82f6);
            color: white;
            padding: 2rem 0;
            text-align: center;
            box-shadow: var(--shadow);
        }}
        
        .header h1 {{ 
            font-size: 2.5rem; 
            font-weight: 700;
            margin-bottom: 0.5rem;
        }}
        
        .header p {{ 
            font-size: 1.1rem; 
            opacity: 0.9;
        }}
        
        /* CONTAINER PRINCIPAL */
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem 1rem;
        }}
        
        /* GRID DE MÓDULOS */
        .modules-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 2rem;
            margin-top: 2rem;
        }}
        
        /* CARD DE MÓDULO */
        .module-card {{
            background: white;
            border-radius: var(--radius);
            box-shadow: var(--shadow);
            overflow: hidden;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }}
        
        .module-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 8px 25px -8px rgb(0 0 0 / 0.2);
        }}
        
        .module-header {{
            background: linear-gradient(135deg, var(--primary), #3b82f6);
            color: white;
            padding: 1.5rem;
        }}
        
        .module-title {{
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
        }}
        
        .module-meta {{
            display: flex;
            gap: 1rem;
            font-size: 0.9rem;
            opacity: 0.9;
        }}
        
        .module-body {{
            padding: 1.5rem;
        }}
        
        .lessons-list {{
            list-style: none;
            margin-bottom: 1.5rem;
        }}
        
        .lessons-list li {{
            padding: 0.5rem 0;
            border-bottom: 1px solid #e2e8f0;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}
        
        .lesson-icon {{
            width: 20px;
            text-align: center;
        }}
        
        .progress-bar {{
            width: 100%;
            height: 8px;
            background: #e2e8f0;
            border-radius: 4px;
            overflow: hidden;
            margin: 1rem 0;
        }}
        
        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, var(--success), #22c55e);
            transition: width 0.3s ease;
        }}
        
        .btn-primary {{
            display: inline-block;
            background: var(--primary);
            color: white;
            padding: 0.8rem 1.5rem;
            border-radius: var(--radius);
            text-decoration: none;
            font-weight: 500;
            transition: background 0.2s ease;
            border: none;
            cursor: pointer;
        }}
        
        .btn-primary:hover {{
            background: #1d4ed8;
        }}
        
        /* STATS SECTION */
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin-bottom: 2rem;
        }}
        
        .stat-card {{
            background: white;
            padding: 1.5rem;
            border-radius: var(--radius);
            box-shadow: var(--shadow);
            text-align: center;
        }}
        
        .stat-number {{
            font-size: 2rem;
            font-weight: 700;
            color: var(--primary);
        }}
        
        .stat-label {{
            color: var(--gray);
            margin-top: 0.5rem;
        }}
        
        /* RESPONSIVE */
        @media (max-width: 768px) {{
            .container {{ padding: 1rem; }}
            .header h1 {{ font-size: 2rem; }}
            .modules-grid {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📚 Campus Virtual Klinikare</h1>
        <p>Plataforma de Formación y Desarrollo Profesional</p>
    </div>

    <div class="container">
        <!-- Estadísticas de progreso -->
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">2</div>
                <div class="stat-label">Módulos Disponibles</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">7</div>
                <div class="stat-label">Lecciones Totales</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">0%</div>
                <div class="stat-label">Progreso Completado</div>
            </div>
        </div>

        <!-- Grid de módulos -->
        <div class="modules-grid">
            <!-- MÓDULO T1 -->
            <div class="module-card">
                <div class="module-header">
                    <div class="module-title">🤖 Módulo T1: Inteligencia Artificial</div>
                    <div class="module-meta">
                        <span>⏱️ 60 min</span>
                        <span>📊 Básico</span>
                        <span>🎯 4 lecciones</span>
                    </div>
                </div>
                <div class="module-body">
                    <ul class="lessons-list">
                        <li><span class="lesson-icon">📹</span> Introducción a la IA</li>
                        <li><span class="lesson-icon">⚖️</span> IA vs Chatbots tradicionales</li>
                        <li><span class="lesson-icon">❓</span> Preguntas Efectivas</li>
                        <li><span class="lesson-icon">🏢</span> IA en tu recepción</li>
                    </ul>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: 0%"></div>
                    </div>
                    <a href="www/ollama/tema-T1.html" class="btn-primary">Comenzar Módulo</a>
                </div>
            </div>

            <!-- MÓDULO T2 -->
            <div class="module-card">
                <div class="module-header">
                    <div class="module-title">🖥️ Módulo T2: Navegación CliniQuer</div>
                    <div class="module-meta">
                        <span>⏱️ 45 min</span>
                        <span>📊 Intermedio</span>
                        <span>🎯 3 lecciones</span>
                    </div>
                </div>
                <div class="module-body">
                    <ul class="lessons-list">
                        <li><span class="lesson-icon">🚪</span> Introducción al sistema</li>
                        <li><span class="lesson-icon">📅</span> Gestión de agenda</li>
                        <li><span class="lesson-icon">🏠</span> Páginas principales</li>
                    </ul>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: 0%"></div>
                    </div>
                    <a href="www/ollama/tema-T2.html" class="btn-primary">Comenzar Módulo</a>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
```

[ARCHIVO: www/tema-T1.html] - Módulo de IA
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🤖 Módulo T1: Inteligencia Artificial - Campus Klinikare</title>
    <style>
        /* Variables y reset iguales que index */
        :root {{
            --primary: #2563eb;
            --success: #16a34a;
            --warning: #f59e0b;
            --gray: #64748b;
            --light-gray: #f8fafc;
            --dark: #1e293b;
            --shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
            --radius: 8px;
        }}
        
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: 'Inter', system-ui, sans-serif; 
            line-height: 1.6; 
            color: var(--dark);
            background: var(--light-gray);
        }}
        
        /* LAYOUT DE 2 COLUMNAS */
        .layout {{
            display: grid;
            grid-template-columns: 300px 1fr;
            min-height: 100vh;
        }}
        
        /* SIDEBAR DE NAVEGACIÓN */
        .sidebar {{
            background: white;
            box-shadow: var(--shadow);
            padding: 2rem 1rem;
            overflow-y: auto;
        }}
        
        .sidebar-title {{
            font-size: 1.2rem;
            font-weight: 600;
            margin-bottom: 1rem;
            color: var(--primary);
        }}
        
        .nav-menu {{
            list-style: none;
        }}
        
        .nav-item {{
            margin-bottom: 0.5rem;
        }}
        
        .nav-link {{
            display: block;
            padding: 0.8rem 1rem;
            color: var(--gray);
            text-decoration: none;
            border-radius: var(--radius);
            transition: all 0.2s ease;
        }}
        
        .nav-link:hover, .nav-link.active {{
            background: var(--light-gray);
            color: var(--primary);
        }}
        
        .nav-link.completed {{
            background: #f0fdf4;
            color: var(--success);
        }}
        
        /* ÁREA DE CONTENIDO PRINCIPAL */
        .main-content {{
            padding: 2rem;
            overflow-y: auto;
        }}
        
        /* BREADCRUMBS */
        .breadcrumbs {{
            margin-bottom: 2rem;
            font-size: 0.9rem;
            color: var(--gray);
        }}
        
        .breadcrumbs a {{
            color: var(--primary);
            text-decoration: none;
        }}
        
        /* HEADER DEL MÓDULO */
        .module-header {{
            background: linear-gradient(135deg, var(--primary), #3b82f6);
            color: white;
            padding: 2rem;
            border-radius: var(--radius);
            margin-bottom: 2rem;
        }}
        
        .module-header h1 {{
            font-size: 2rem;
            margin-bottom: 0.5rem;
        }}
        
        .module-meta {{
            display: flex;
            gap: 1rem;
            opacity: 0.9;
        }}
        
        /* SECCIONES DE CONTENIDO */
        .content-section {{
            background: white;
            border-radius: var(--radius);
            box-shadow: var(--shadow);
            padding: 2rem;
            margin-bottom: 2rem;
        }}
        
        .section-title {{
            font-size: 1.5rem;
            color: var(--primary);
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}
        
        /* TARJETAS DE LECCIÓN */
        .lesson-card {{
            border: 1px solid #e2e8f0;
            border-radius: var(--radius);
            padding: 1.5rem;
            margin-bottom: 1rem;
            transition: border-color 0.2s ease;
        }}
        
        .lesson-card:hover {{
            border-color: var(--primary);
        }}
        
        .lesson-title {{
            font-size: 1.2rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
            color: var(--dark);
        }}
        
        .lesson-summary {{
            color: var(--gray);
            margin-bottom: 1rem;
        }}
        
        /* ACCORDIONS/DETALLES */
        details {{
            border: 1px solid #e2e8f0;
            border-radius: var(--radius);
            padding: 1rem;
            margin: 1rem 0;
        }}
        
        summary {{
            font-weight: 600;
            cursor: pointer;
            padding: 0.5rem;
            border-radius: var(--radius);
            transition: background 0.2s ease;
        }}
        
        summary:hover {{
            background: var(--light-gray);
        }}
        
        /* LISTAS ESTILIZADAS */
        .key-points {{
            list-style: none;
            margin: 1rem 0;
        }}
        
        .key-points li {{
            padding: 0.5rem 0;
            padding-left: 1.5rem;
            position: relative;
        }}
        
        .key-points li::before {{
            content: "✅";
            position: absolute;
            left: 0;
        }}
        
        /* CUESTIONARIO ESTILIZADO */
        .quiz-section {{
            background: linear-gradient(135deg, #fef3c7, #fde68a);
            border-radius: var(--radius);
            padding: 2rem;
            margin-top: 2rem;
        }}
        
        .quiz-title {{
            font-size: 1.5rem;
            margin-bottom: 1rem;
            color: var(--dark);
        }}
        
        .question {{
            background: white;
            border-radius: var(--radius);
            padding: 1.5rem;
            margin-bottom: 1rem;
            box-shadow: var(--shadow);
        }}
        
        .question-text {{
            font-weight: 600;
            margin-bottom: 1rem;
        }}
        
        .options {{
            list-style: none;
        }}
        
        .options li {{
            padding: 0.5rem 0;
        }}
        
        .options input[type="radio"] {{
            margin-right: 0.5rem;
        }}
        
        .quiz-actions {{
            text-align: center;
            margin-top: 2rem;
        }}
        
        .btn-quiz {{
            background: var(--warning);
            color: white;
            padding: 1rem 2rem;
            border: none;
            border-radius: var(--radius);
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.2s ease;
        }}
        
        .btn-quiz:hover {{
            background: #d97706;
        }}
        
        .quiz-result {{
            background: white;
            border-radius: var(--radius);
            padding: 1rem;
            margin-top: 1rem;
            text-align: center;
            font-weight: 600;
        }}
        
        .result-excellent {{
            color: var(--success);
            background: #f0fdf4;
        }}
        
        .result-good {{
            color: var(--warning);
            background: #fefce8;
        }}
        
        .result-needs-work {{
            color: #dc2626;
            background: #fef2f2;
        }}
        
        /* RESPONSIVE */
        @media (max-width: 768px) {{
            .layout {{
                grid-template-columns: 1fr;
            }}
            .sidebar {{
                display: none;
            }}
            .main-content {{
                padding: 1rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="layout">
        <!-- SIDEBAR DE NAVEGACIÓN -->
        <div class="sidebar">
            <div class="sidebar-title">📚 Navegación del Curso</div>
            <ul class="nav-menu">
                <li class="nav-item">
                    <a href="../../index-ollama.html" class="nav-link">🏠 Inicio Campus</a>
                </li>
                <li class="nav-item">
                    <a href="#leccion1" class="nav-link active">📹 Lección 1: Introducción IA</a>
                </li>
                <li class="nav-item">
                    <a href="#leccion2" class="nav-link">⚖️ Lección 2: IA vs Chatbots</a>
                </li>
                <li class="nav-item">
                    <a href="#leccion3" class="nav-link">❓ Lección 3: Preguntas Efectivas</a>
                </li>
                <li class="nav-item">
                    <a href="#leccion4" class="nav-link">🏢 Lección 4: IA en Recepción</a>
                </li>
                <li class="nav-item">
                    <a href="#manual" class="nav-link">📖 Manual de Referencia</a>
                </li>
                <li class="nav-item">
                    <a href="#quiz" class="nav-link">🎯 Evaluación</a>
                </li>
                <li class="nav-item">
                    <a href="tema-T2.html" class="nav-link">➡️ Siguiente: Módulo T2</a>
                </li>
            </ul>
        </div>

        <!-- CONTENIDO PRINCIPAL -->
        <div class="main-content">
            <!-- Breadcrumbs -->
            <div class="breadcrumbs">
                <a href="../../index-ollama.html">Campus</a> > 
                <a href="#">Módulo T1</a> > 
                Inteligencia Artificial
            </div>

            <!-- Header del módulo -->
            <div class="module-header">
                <h1>🤖 Módulo T1: Inteligencia Artificial en CliniQuer</h1>
                <div class="module-meta">
                    <span>⏱️ Duración: 60 minutos</span>
                    <span>📊 Nivel: Básico</span>
                    <span>🎯 4 Lecciones</span>
                </div>
            </div>

            <!-- Objetivo del módulo -->
            <div class="content-section">
                <h2 class="section-title">🎯 Objetivos del Módulo</h2>
                <p>Al finalizar este módulo, serás capaz de:</p>
                <ul class="key-points">
                    <li>Utilizar eficientemente la IA de CliniQuer para resolver consultas</li>
                    <li>Diferenciar entre IA avanzada y chatbots tradicionales</li>
                    <li>Formular preguntas claras y específicas para obtener mejores respuestas</li>
                    <li>Implementar el asistente de recepción en tu flujo de trabajo diario</li>
                </ul>
            </div>

            <!-- Lecciones del módulo -->
            <div class="content-section">
                <h2 class="section-title">📚 Lecciones</h2>
                
                <div class="lesson-card" id="leccion1">
                    <div class="lesson-title">📹 KLC-T1-v1: Introducción a la IA</div>
                    <div class="lesson-summary">
                        <strong>Resumen:</strong> Aprende los fundamentos del uso de IA en CliniQuer y la importancia de formular preguntas claras y específicas.
                    </div>
                    
                    <details>
                        <summary>📖 Contenido Detallado</summary>
                        <p>La IA de CliniQuer está disponible 24/7 y puede responder consultas de forma rápida y precisa. Para maximizar su efectividad, es fundamental formular preguntas claras y proporcionar contexto relevante.</p>
                        
                        <h4>Conceptos Clave:</h4>
                        <ul class="key-points">
                            <li>La IA funciona mejor con preguntas específicas y detalladas</li>
                            <li>Proporcionar contexto mejora significativamente la precisión de las respuestas</li>
                            <li>La IA es una herramienta de soporte, complementa el trabajo humano</li>
                            <li>Puede ayudar con tareas como generar facturas y reportes</li>
                            <li>Disponible para formación continua y soporte técnico</li>
                        </ul>
                        
                        <h4>⚠️ Errores Comunes:</h4>
                        <ul>
                            <li>Hacer preguntas demasiado vagas o generales</li>
                            <li>No proporcionar suficiente contexto</li>
                            <li>Usar frases ambiguas o poco claras</li>
                        </ul>
                    </details>
                </div>

                <div class="lesson-card" id="leccion2">
                    <div class="lesson-title">⚖️ KLC-T1-v2: Diferencias entre IA y Chatbots</div>
                    <div class="lesson-summary">
                        <strong>Resumen:</strong> Comprende las ventajas de la IA sobre los chatbots tradicionales y cómo aprovechar sus capacidades avanzadas.
                    </div>
                    
                    <details>
                        <summary>📖 Contenido Detallado</summary>
                        <p>Los chatbots tradicionales siguen reglas preprogramadas y solo responden a palabras clave específicas. En contraste, la IA comprende el lenguaje natural y el contexto, ofreciendo soluciones personalizadas.</p>
                        
                        <h4>Conceptos Clave:</h4>
                        <ul class="key-points">
                            <li>Chatbots = reglas predefinidas; IA = aprendizaje y adaptación</li>
                            <li>La IA puede planificar, analizar y predecir</li>
                            <li>En CliniQuer ayuda con reportes, facturas y análisis</li>
                            <li>El asistente de recepción utiliza IA para interacciones naturales</li>
                            <li>Reduce significativamente la carga de trabajo administrativo</li>
                        </ul>
                        
                        <h4>💡 Tips Profesionales:</h4>
                        <ul>
                            <li>Aprovecha la capacidad de aprendizaje continuo de la IA</li>
                            <li>No limites las consultas a formatos rígidos</li>
                            <li>Utiliza el contexto para consultas más complejas</li>
                        </ul>
                    </details>
                </div>

                <div class="lesson-card" id="leccion3">
                    <div class="lesson-title">❓ KLC-T1-v3: Formulación de Preguntas Efectivas</div>
                    <div class="lesson-summary">
                        <strong>Resumen:</strong> Domina el arte de hacer preguntas claras y específicas para obtener respuestas útiles y precisas de la IA.
                    </div>
                    
                    <details>
                        <summary>📖 Contenido Detallado</summary>
                        <p>La efectividad de la IA depende directamente de la calidad de las preguntas que le hagas. Una pregunta bien formulada incluye contexto, especificidad y objetivos claros.</p>
                        
                        <h4>Conceptos Clave:</h4>
                        <ul class="key-points">
                            <li>La claridad en las preguntas genera respuestas más útiles</li>
                            <li>Añadir contexto reduce la ambigüedad significativamente</li>
                            <li>Reformular preguntas mejora los resultados</li>
                            <li>La IA está disponible 24/7 para consultas</li>
                            <li>Incluir detalles específicos del caso clínico mejora la respuesta</li>
                        </ul>
                        
                        <h4>📝 Ejemplos Prácticos:</h4>
                        <p><strong>Pregunta vaga:</strong> "¿Cómo hago una factura?"</p>
                        <p><strong>Pregunta efectiva:</strong> "¿Cómo genero una factura para un paciente menor donde el responsable de pago es su madre?"</p>
                    </details>
                </div>

                <div class="lesson-card" id="leccion4">
                    <div class="lesson-title">🏢 KLC-T1-v4: IA en la Recepción</div>
                    <div class="lesson-summary">
                        <strong>Resumen:</strong> Descubre cómo el módulo de asistente de recepción transforma la atención al paciente con IA avanzada.
                    </div>
                    
                    <details>
                        <summary>📖 Contenido Detallado</summary>
                        <p>El asistente de recepción utiliza IA para gestionar citas, recordatorios y atención al paciente las 24 horas. Proporciona respuestas empáticas y personalizadas.</p>
                        
                        <h4>Conceptos Clave:</h4>
                        <ul class="key-points">
                            <li>Gestión automatizada de citas y recordatorios</li>
                            <li>Respuestas empáticas y adaptadas al contexto</li>
                            <li>Sistema de alertas para intervención manual</li>
                            <li>Configuración personalizable según necesidades</li>
                            <li>Panel de control con estadísticas y métricas</li>
                        </ul>
                        
                        <h4>🔧 Configuración y Uso:</h4>
                        <ul>
                            <li>Definir tareas automatizables</li>
                            <li>Configurar umbrales de escalación</li>
                            <li>Monitorear estadísticas de uso</li>
                        </ul>
                    </details>
                </div>
            </div>

            <!-- Manual de referencia rápida -->
            <div class="content-section" id="manual">
                <h2 class="section-title">📖 Manual de Referencia Rápida</h2>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1rem;">
                    <div style="border: 1px solid #e2e8f0; border-radius: var(--radius); padding: 1rem;">
                        <h3>🚀 Inicio Rápido</h3>
                        <ol>
                            <li>Accede a la IA desde cualquier sección</li>
                            <li>Formula tu pregunta con contexto</li>
                            <li>Revisa y aplica la respuesta</li>
                        </ol>
                    </div>
                    <div style="border: 1px solid #e2e8f0; border-radius: var(--radius); padding: 1rem;">
                        <h3>💡 Mejores Prácticas</h3>
                        <ul>
                            <li>Sé específico en tus consultas</li>
                            <li>Proporciona contexto relevante</li>
                            <li>Reformula si es necesario</li>
                        </ul>
                    </div>
                </div>
            </div>

            <!-- Cuestionario de evaluación -->
            <div class="quiz-section" id="quiz">
                <div class="quiz-title">🎯 Evaluación del Módulo T1</div>
                
                <form id="quizT1">
                    <div class="question">
                        <div class="question-text">1. ¿Cuál es la principal ventaja de la IA de CliniQuer?</div>
                        <ul class="options">
                            <li><label><input type="radio" name="q1" value="a"> Es más económica que otras soluciones</label></li>
                            <li><label><input type="radio" name="q1" value="b" data-correct="true"> Está disponible 24/7 y comprende el contexto</label></li>
                            <li><label><input type="radio" name="q1" value="c"> Solo funciona con comandos específicos</label></li>
                        </ul>
                    </div>

                    <div class="question">
                        <div class="question-text">2. ¿Qué diferencia a la IA de los chatbots tradicionales?</div>
                        <ul class="options">
                            <li><label><input type="radio" name="q2" value="a" data-correct="true"> La IA comprende lenguaje natural y contexto</label></li>
                            <li><label><input type="radio" name="q2" value="b"> Los chatbots son más rápidos</label></li>
                            <li><label><input type="radio" name="q2" value="c"> No hay diferencias significativas</label></li>
                        </ul>
                    </div>

                    <div class="question">
                        <div class="question-text">3. ¿Cómo debes formular las preguntas a la IA?</div>
                        <ul class="options">
                            <li><label><input type="radio" name="q3" value="a" data-correct="true"> De forma clara, específica y con contexto</label></li>
                            <li><label><input type="radio" name="q3" value="b"> Lo más breve posible</label></li>
                            <li><label><input type="radio" name="q3" value="c"> Usando solo palabras clave</label></li>
                        </ul>
                    </div>

                    <div class="question">
                        <div class="question-text">4. ¿Qué puede hacer el asistente de recepción con IA?</div>
                        <ul class="options">
                            <li><label><input type="radio" name="q4" value="a"> Solo responder preguntas básicas</label></li>
                            <li><label><input type="radio" name="q4" value="b" data-correct="true"> Gestionar citas, recordatorios y atención personalizada</label></li>
                            <li><label><input type="radio" name="q4" value="c"> Reemplazar completamente al personal humano</label></li>
                        </ul>
                    </div>

                    <div class="quiz-actions">
                        <button type="button" class="btn-quiz" onclick="evaluarQuizT1()">📊 Evaluar Respuestas</button>
                    </div>

                    <div id="resultadoQuizT1" class="quiz-result" style="display: none;"></div>
                </form>
            </div>
        </div>
    </div>

    <script>
        function evaluarQuizT1() {{
            const form = document.getElementById('quizT1');
            const questions = form.querySelectorAll('.question');
            let correctas = 0;
            let total = 0;

            questions.forEach(question => {{
                const correctAnswer = question.querySelector('input[data-correct="true"]');
                const selectedAnswer = question.querySelector('input[type="radio"]:checked');
                
                if (correctAnswer) {{
                    total++;
                    if (selectedAnswer && selectedAnswer.hasAttribute('data-correct')) {{
                        correctas++;
                    }}
                }}
            }});

            const porcentaje = Math.round((correctas / total) * 100);
            const resultado = document.getElementById('resultadoQuizT1');
            
            let mensaje = '';
            let clase = '';
            
            if (porcentaje >= 80) {{
                mensaje = `🏆 ¡Excelente! Has obtenido ${{correctas}}/${{total}} respuestas correctas (${{porcentaje}}%). Has dominado los conceptos clave de IA.`;
                clase = 'result-excellent';
            }} else if (porcentaje >= 60) {{
                mensaje = `👍 Bien hecho. Has obtenido ${{correctas}}/${{total}} respuestas correctas (${{porcentaje}}%). Revisa algunos conceptos para mejorar.`;
                clase = 'result-good';
            }} else {{
                mensaje = `📚 Necesitas repasar. Has obtenido ${{correctas}}/${{total}} respuestas correctas (${{porcentaje}}%). Te recomendamos revisar las lecciones.`;
                clase = 'result-needs-work';
            }}
            
            resultado.innerHTML = mensaje;
            resultado.className = `quiz-result ${{clase}}`;
            resultado.style.display = 'block';
            
            // Scroll suave hasta el resultado
            resultado.scrollIntoView({{ behavior: 'smooth' }});
        }}

        // Navegación suave entre secciones
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {{
            anchor.addEventListener('click', function (e) {{
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {{
                    target.scrollIntoView({{ behavior: 'smooth' }});
                }}
            }});
        }});
    </script>
</body>
</html>
```

[ARCHIVO: www/tema-T2.html] - Módulo de Navegación CliniQuer
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🖥️ Módulo T2: Navegación CliniQuer - Campus Klinikare</title>
    <!-- Estilos iguales que tema-T1.html -->
    <style>
        /* [MISMO CSS QUE TEMA-T1] */
        :root {{
            --primary: #2563eb;
            --success: #16a34a;
            --warning: #f59e0b;
            --gray: #64748b;
            --light-gray: #f8fafc;
            --dark: #1e293b;
            --shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
            --radius: 8px;
        }}
        /* [RESTO DEL CSS IGUAL] */
    </style>
</head>
<body>
    <div class="layout">
        <!-- SIDEBAR -->
        <div class="sidebar">
            <div class="sidebar-title">📚 Navegación del Curso</div>
            <ul class="nav-menu">
                <li class="nav-item"><a href="../../index-ollama.html" class="nav-link">🏠 Inicio Campus</a></li>
                <li class="nav-item"><a href="#leccion1" class="nav-link active">🚪 Lección 1: Introducción</a></li>
                <li class="nav-item"><a href="#leccion2" class="nav-link">📅 Lección 2: Gestión Agenda</a></li>
                <li class="nav-item"><a href="#leccion3" class="nav-link">🏠 Lección 3: Páginas Principales</a></li>
                <li class="nav-item"><a href="#manual" class="nav-link">📖 Manual de Referencia</a></li>
                <li class="nav-item"><a href="#quiz" class="nav-link">🎯 Evaluación</a></li>
                <li class="nav-item"><a href="tema-T1.html" class="nav-link">⬅️ Anterior: Módulo T1</a></li>
            </ul>
        </div>

        <!-- CONTENIDO PRINCIPAL -->
        <div class="main-content">
            <div class="breadcrumbs">
                <a href="../../index-ollama.html">Campus</a> > 
                <a href="#">Módulo T2</a> > 
                Navegación CliniQuer
            </div>

            <div class="module-header">
                <h1>🖥️ Módulo T2: Navegación y Gestión CliniQuer</h1>
                <div class="module-meta">
                    <span>⏱️ Duración: 45 minutos</span>
                    <span>📊 Nivel: Intermedio</span>
                    <span>🎯 3 Lecciones</span>
                </div>
            </div>

            <!-- Objetivos -->
            <div class="content-section">
                <h2 class="section-title">🎯 Objetivos del Módulo</h2>
                <p>Al completar este módulo serás capaz de:</p>
                <ul class="key-points">
                    <li>Navegar eficientemente por la plataforma CliniQuer</li>
                    <li>Gestionar agendas y citas de manera profesional</li>
                    <li>Utilizar las páginas principales para tareas administrativas</li>
                    <li>Optimizar tu flujo de trabajo diario en la plataforma</li>
                </ul>
            </div>

            <!-- Lecciones -->
            <div class="content-section">
                <h2 class="section-title">📚 Lecciones</h2>
                
                <!-- LECCIÓN 1 -->
                <div class="lesson-card" id="leccion1">
                    <div class="lesson-title">🚪 KLC-T2-v1: Introducción al Sistema</div>
                    <div class="lesson-summary">
                        <strong>Resumen:</strong> Aprende a acceder a CliniQuer, configurar tu sesión y optimizar el acceso diario.
                    </div>
                    
                    <details>
                        <summary>📖 Contenido Detallado</summary>
                        <p>Esta lección te guía a través del proceso de acceso inicial a CliniQuer, desde la búsqueda en navegador hasta la configuración de marcadores para un acceso eficiente.</p>
                        
                        <h4>Conceptos Clave:</h4>
                        <ul class="key-points">
                            <li>Acceso mediante appcliniquer.com</li>
                            <li>Importancia de guardar en marcadores del navegador</li>
                            <li>Configuración inicial de la sesión de trabajo</li>
                            <li>Seguridad en el manejo de credenciales</li>
                            <li>Orientación básica en la interfaz principal</li>
                        </ul>
                        
                        <h4>💡 Tips Profesionales:</h4>
                        <ul>
                            <li>Configura acceso directo en escritorio</li>
                            <li>Utiliza gestores de contraseñas seguros</li>
                            <li>Mantén siempre actualizada tu información de acceso</li>
                        </ul>
                    </details>
                </div>

                <!-- LECCIÓN 2 -->
                <div class="lesson-card" id="leccion2">
                    <div class="lesson-title">📅 KLC-T2-v2: Gestión de Agenda de Pacientes</div>
                    <div class="lesson-summary">
                        <strong>Resumen:</strong> Domina el sistema de agenda: creación, filtrado, gestión de citas y diferentes modalidades de atención.
                    </div>
                    
                    <details>
                        <summary>📖 Contenido Detallado</summary>
                        <p>La gestión eficiente de la agenda es fundamental para el funcionamiento óptimo de una clínica. Esta lección cubre todas las funcionalidades desde filtros básicos hasta gestión avanzada de citas.</p>
                        
                        <h4>Conceptos Clave:</h4>
                        <ul class="key-points">
                            <li>Navegación por la cabecera de agenda y filtros</li>
                            <li>Búsqueda y filtrado por profesional y recurso</li>
                            <li>Gestión de tipos de cita (urgencia, lista de espera, online)</li>
                            <li>Creación, modificación y cancelación de citas</li>
                            <li>Generación de listados e informes de agenda</li>
                            <li>Visualización de estados y codificación por colores</li>
                        </ul>
                        
                        <h4>📋 Casos Prácticos:</h4>
                        <ul>
                            <li>Programación de cita urgente</li>
                            <li>Gestión de lista de espera</li>
                            <li>Configuración de citas online</li>
                            <li>Reprogramación masiva de citas</li>
                        </ul>
                    </details>
                </div>

                <!-- LECCIÓN 3 -->
                <div class="lesson-card" id="leccion3">
                    <div class="lesson-title">🏠 KLC-T2-v3: Páginas Principales de Klinikare</div>
                    <div class="lesson-summary">
                        <strong>Resumen:</strong> Explora las páginas principales de CliniQuer y aprende a navegar entre los diferentes módulos según tu perfil.
                    </div>
                    
                    <details>
                        <summary>📖 Contenido Detallado</summary>
                        <p>CliniQuer presenta diferentes componentes y páginas según el perfil del usuario. Esta lección te ayuda a entender la estructura organizativa y navegar eficientemente.</p>
                        
                        <h4>Conceptos Clave:</h4>
                        <ul class="key-points">
                            <li>Estructura de la página principal personalizada</li>
                            <li>Componentes disponibles según perfil de usuario</li>
                            <li>Navegación entre secciones de la organización</li>
                            <li>Acceso rápido a funciones más utilizadas</li>
                            <li>Personalización del dashboard de trabajo</li>
                        </ul>
                        
                        <h4>🗺️ Mapa de Navegación:</h4>
                        <ul>
                            <li>Dashboard principal → Vista general</li>
                            <li>Módulo de pacientes → Gestión de historiales</li>
                            <li>Área administrativa → Facturación y reportes</li>
                            <li>Configuración → Personalización del sistema</li>
                        </ul>
                    </details>
                </div>
            </div>

            <!-- Manual de referencia -->
            <div class="content-section" id="manual">
                <h2 class="section-title">📖 Manual de Referencia Rápida</h2>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1rem;">
                    <div style="border: 1px solid #e2e8f0; border-radius: var(--radius); padding: 1rem;">
                        <h3>🔐 Acceso Rápido</h3>
                        <ol>
                            <li>Navega a appcliniquer.com</li>
                            <li>Introduce credenciales</li>
                            <li>Guarda en marcadores</li>
                        </ol>
                    </div>
                    <div style="border: 1px solid #e2e8f0; border-radius: var(--radius); padding: 1rem;">
                        <h3>📅 Gestión de Agenda</h3>
                        <ul>
                            <li>Usa filtros para navegación rápida</li>
                            <li>Aprovecha códigos de colores</li>
                            <li>Configura tipos de cita según necesidad</li>
                        </ul>
                    </div>
                    <div style="border: 1px solid #e2e8f0; border-radius: var(--radius); padding: 1rem;">
                        <h3>🏠 Navegación Efectiva</h3>
                        <ul>
                            <li>Personaliza tu dashboard</li>
                            <li>Utiliza accesos directos</li>
                            <li>Organiza por flujo de trabajo</li>
                        </ul>
                    </div>
                </div>
            </div>

            <!-- Cuestionario -->
            <div class="quiz-section" id="quiz">
                <div class="quiz-title">🎯 Evaluación del Módulo T2</div>
                
                <form id="quizT2">
                    <div class="question">
                        <div class="question-text">1. ¿Cuál es la URL principal para acceder a CliniQuer?</div>
                        <ul class="options">
                            <li><label><input type="radio" name="q1" value="a" data-correct="true"> appcliniquer.com</label></li>
                            <li><label><input type="radio" name="q1" value="b"> cliniquer.es</label></li>
                            <li><label><input type="radio" name="q1" value="c"> app.klinikare.com</label></li>
                        </ul>
                    </div>

                    <div class="question">
                        <div class="question-text">2. ¿Qué permite hacer la gestión de agenda de CliniQuer?</div>
                        <ul class="options">
                            <li><label><input type="radio" name="q2" value="a"> Solo visualizar citas existentes</label></li>
                            <li><label><input type="radio" name="q2" value="b" data-correct="true"> Crear, modificar, filtrar y gestionar todos los tipos de citas</label></li>
                            <li><label><input type="radio" name="q2" value="c"> Únicamente programar citas básicas</label></li>
                        </ul>
                    </div>

                    <div class="question">
                        <div class="question-text">3. ¿Cómo está organizada la página principal de CliniQuer?</div>
                        <ul class="options">
                            <li><label><input type="radio" name="q3" value="a" data-correct="true"> Según el perfil del usuario con componentes personalizados</label></li>
                            <li><label><input type="radio" name="q3" value="b"> Igual para todos los usuarios</label></li>
                            <li><label><input type="radio" name="q3" value="c"> Solo muestra la agenda</label></li>
                        </ul>
                    </div>

                    <div class="quiz-actions">
                        <button type="button" class="btn-quiz" onclick="evaluarQuizT2()">📊 Evaluar Respuestas</button>
                    </div>

                    <div id="resultadoQuizT2" class="quiz-result" style="display: none;"></div>
                </form>
            </div>
        </div>
    </div>

    <script>
        function evaluarQuizT2() {{
            const form = document.getElementById('quizT2');
            const questions = form.querySelectorAll('.question');
            let correctas = 0;
            let total = 0;

            questions.forEach(question => {{
                const correctAnswer = question.querySelector('input[data-correct="true"]');
                const selectedAnswer = question.querySelector('input[type="radio"]:checked');
                
                if (correctAnswer) {{
                    total++;
                    if (selectedAnswer && selectedAnswer.hasAttribute('data-correct')) {{
                        correctas++;
                    }}
                }}
            }});

            const porcentaje = Math.round((correctas / total) * 100);
            const resultado = document.getElementById('resultadoQuizT2');
            
            let mensaje = '';
            let clase = '';
            
            if (porcentaje >= 80) {{
                mensaje = `🏆 ¡Excelente! Has obtenido ${{correctas}}/${{total}} respuestas correctas (${{porcentaje}}%). Dominas la navegación en CliniQuer.`;
                clase = 'result-excellent';
            }} else if (porcentaje >= 60) {{
                mensaje = `👍 Bien hecho. Has obtenido ${{correctas}}/${{total}} respuestas correctas (${{porcentaje}}%). Revisa algunos conceptos para mejorar.`;
                clase = 'result-good';
            }} else {{
                mensaje = `📚 Necesitas repasar. Has obtenido ${{correctas}}/${{total}} respuestas correctas (${{porcentaje}}%). Te recomendamos revisar las lecciones.`;
                clase = 'result-needs-work';
            }}
            
            resultado.innerHTML = mensaje;
            resultado.className = `quiz-result ${{clase}}`;
            resultado.style.display = 'block';
            
            resultado.scrollIntoView({{ behavior: 'smooth' }});
        }}

        document.querySelectorAll('a[href^="#"]').forEach(anchor => {{
            anchor.addEventListener('click', function (e) {{
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {{
                    target.scrollIntoView({{ behavior: 'smooth' }});
                }}
            }});
        }});
    </script>
</body>
</html>
```

🔥 INSTRUCCIONES CRÍTICAS PARA LA SALIDA:
1. **GENERA EXACTAMENTE 3 ARCHIVOS**: index.html + tema-T1.html + tema-T2.html
2. **USA EL FORMATO EXACTO**: [ARCHIVO: nombre] antes de cada ```html
3. **DISEÑO MODERNO**: Aplica todos los estilos CSS Grid, Flexbox, colores corporativos
4. **FUNCIONALIDAD EDUCATIVA**: Navegación, cuestionarios interactivos, tracking de progreso
5. **RESPONSIVE**: Debe funcionar en móvil, tablet y desktop
6. **CONTENIDO EDUCATIVO**: Basado en análisis real de las transcripciones proporcionadas

Ejemplo de salida esperada:
- [ARCHIVO: index.html] + código HTML completo con dashboard moderno
- [ARCHIVO: www/tema-T1.html] + código HTML completo con layout de 2 columnas y cuestionarios
- [ARCHIVO: www/tema-T2.html] + código HTML completo con navegación y contenido estructurado"""

    return prompt