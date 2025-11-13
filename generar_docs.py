#!/usr/bin/env python3
"""
Menú principal para generar documentación
Permite seleccionar entre OpenAI, Ollama o ambos
"""
import os
import sys
import pathlib
import subprocess
from datetime import datetime

def mostrar_banner():
    """Mostrar banner del sistema"""
    print("🎯" + "="*70 + "🎯")
    print("   📚 GENERADOR DE DOCUMENTACIÓN KLINIKARE / CLINIQQUER 📚")
    print("🎯" + "="*70 + "🎯")
    print()

def listar_transcripciones():
    """Lista archivos de transcripciones disponibles"""
    procesados_dir = pathlib.Path("procesados")
    transcripciones_files = list(procesados_dir.glob("transcripciones_*.txt"))
    
    if not transcripciones_files:
        print("❌ No se encontraron archivos de transcripciones")
        print("💡 Ejecuta primero: python transcribir.py")
        return []
    
    print("📋 Archivos de transcripciones disponibles:")
    for i, file in enumerate(transcripciones_files, 1):
        fecha_mod = datetime.fromtimestamp(file.stat().st_mtime)
        tamaño_kb = file.stat().st_size / 1024
        print(f"   {i}. {file.name}")
        print(f"      📅 {fecha_mod.strftime('%d/%m/%Y %H:%M:%S')} | 💾 {tamaño_kb:.1f} KB")
        print()
    
    return transcripciones_files

def verificar_configuracion():
    """Verificar que las herramientas estén configuradas"""
    from dotenv import load_dotenv
    load_dotenv()
    
    openai_ok = bool(os.getenv('OPENAI_API_KEY'))
    
    try:
        import ollama
        ollama_ok = True
    except ImportError:
        ollama_ok = False
    
    print("🔍 Estado de configuración:")
    print(f"   🌐 OpenAI: {'✅ Configurado' if openai_ok else '❌ API Key faltante'}")
    print(f"   🏠 Ollama: {'✅ Disponible' if ollama_ok else '❌ No instalado'}")
    print()
    
    return openai_ok, ollama_ok

def ejecutar_script(script_name, descripcion):
    """Ejecutar un script Python"""
    print(f"🚀 Ejecutando {descripcion}...")
    print(f"📝 Script: {script_name}")
    print("-" * 50)
    
    try:
        result = subprocess.run([
            sys.executable, script_name
        ], cwd=pathlib.Path(__file__).parent, check=True, capture_output=False)
        
        print("-" * 50)
        print(f"✅ {descripcion} completado exitosamente")
        return True
        
    except subprocess.CalledProcessError as e:
        print("-" * 50)
        print(f"❌ Error ejecutando {descripcion}: {e}")
        return False
    except FileNotFoundError:
        print(f"❌ No se encontró el script: {script_name}")
        return False

def main():
    mostrar_banner()
    
    # Verificar configuración
    openai_ok, ollama_ok = verificar_configuracion()
    
    # Listar transcripciones disponibles
    transcripciones = listar_transcripciones()
    if not transcripciones:
        return
    
    # Mostrar menú principal
    while True:
        print("🎮 MENÚ DE OPCIONES:")
        print()
        
        opciones = []
        if openai_ok:
            opciones.append("1. 🌐 Generar con OpenAI GPT-4o (nube)")
        else:
            print("   🌐 OpenAI: ❌ No disponible (API Key faltante)")
            
        if ollama_ok:
            opciones.append("2. 🏠 Generar con Ollama GPT-OSS (local)")
            opciones.append("3. 🧠 Generar con Ollama DeepSeek-R1 (local)")
        else:
            print("   🏠 Ollama: ❌ No disponible (no instalado)")
        
        if openai_ok and ollama_ok:
            opciones.append("4. 🔄 Generar con TODOS (OpenAI + GPT-OSS + DeepSeek)")
        
        opciones.append("5. 📋 Mostrar transcripciones disponibles")
        opciones.append("6. 🔧 Verificar configuración")
        opciones.append("0. 🚪 Salir")
        
        print()
        for opcion in opciones:
            print(f"   {opcion}")
        
        print()
        seleccion = input("👆 Selecciona una opción: ").strip()
        print()
        
        if seleccion == "0":
            print("👋 ¡Hasta luego!")
            break
            
        elif seleccion == "1" and openai_ok:
            ejecutar_script("generar_docs_openai.py", "Documentación con OpenAI")
            input("\n📱 Presiona Enter para continuar...")
            print()
            
        elif seleccion == "2" and ollama_ok:
            ejecutar_script("generar_docs_ollama.py", "Documentación con Ollama GPT-OSS")
            input("\n📱 Presiona Enter para continuar...")
            print()
            
        elif seleccion == "3" and ollama_ok:
            ejecutar_script("generar_docs_deepseek.py", "Documentación con DeepSeek-R1")
            input("\n📱 Presiona Enter para continuar...")
            print()
            
        elif seleccion == "4" and openai_ok and ollama_ok:
            print("🔄 Generando documentación con TODOS los motores...")
            print()
            
            # Ejecutar OpenAI
            if ejecutar_script("generar_docs_openai.py", "Documentación con OpenAI"):
                print("✅ OpenAI completado")
                print()
                
                # Ejecutar Ollama GPT-OSS
                if ejecutar_script("generar_docs_ollama.py", "Documentación con Ollama GPT-OSS"):
                    print("✅ Ollama GPT-OSS completado")
                    print()
                    
                    # Ejecutar DeepSeek
                    if ejecutar_script("generar_docs_deepseek.py", "Documentación con DeepSeek-R1"):
                        print("🎉 ¡Documentación generada con TODOS los motores!")
                    else:
                        print("⚠️ OpenAI y GPT-OSS completados, pero DeepSeek falló")
                else:
                    print("⚠️ OpenAI completado, pero Ollama GPT-OSS falló")
            else:
                print("❌ Error con OpenAI, cancelando otros motores")
            
            input("\n📱 Presiona Enter para continuar...")
            print()
            
        elif seleccion == "5":
            transcripciones = listar_transcripciones()
            input("\n📱 Presiona Enter para continuar...")
            print()
            
        elif seleccion == "6":
            openai_ok, ollama_ok = verificar_configuracion()
            input("\n📱 Presiona Enter para continuar...")
            print()
            
        else:
            print("❌ Opción no válida o no disponible")
            print()

if __name__ == "__main__":
    main()