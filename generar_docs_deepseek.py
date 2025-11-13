#!/usr/bin/env python3
"""
Generador de documentación usando Ollama con DeepSeek-R1
Script individual para documentación con DeepSeek
"""
import sys
import pathlib
from datetime import datetime

# Añadir el directorio del proyecto al path para importar transcribir
sys.path.append(str(pathlib.Path(__file__).parent))

from transcribir import generar_documentacion_con_deepseek

def main():
    # Buscar archivo de transcripciones más reciente
    procesados_dir = pathlib.Path("procesados")
    transcripciones_files = list(procesados_dir.glob("transcripciones_*.txt"))
    
    if not transcripciones_files:
        print("❌ No se encontraron archivos de transcripciones en la carpeta procesados/")
        print("💡 Ejecuta primero el script principal para generar transcripciones")
        return
    
    # Mostrar archivos disponibles si hay más de uno
    if len(transcripciones_files) > 1:
        print("📋 Archivos de transcripciones disponibles:")
        for i, file in enumerate(transcripciones_files, 1):
            fecha_mod = file.stat().st_mtime
            print(f"   {i}. {file.name} (modificado: {datetime.fromtimestamp(fecha_mod).strftime('%Y-%m-%d %H:%M')})")
        
        try:
            seleccion = input("\n🔍 Selecciona un archivo (Enter para usar el más reciente): ").strip()
            if seleccion:
                transcripciones_file = transcripciones_files[int(seleccion) - 1]
            else:
                transcripciones_file = max(transcripciones_files, key=lambda x: x.stat().st_mtime)
        except (ValueError, IndexError):
            print("⚠️ Selección inválida, usando archivo más reciente")
            transcripciones_file = max(transcripciones_files, key=lambda x: x.stat().st_mtime)
    else:
        transcripciones_file = transcripciones_files[0]
    
    print(f"📄 Usando transcripciones: {transcripciones_file.name}")
    print("🤖 Generando documentación con DeepSeek-R1...")
    
    try:
        # Generar documentación con DeepSeek
        exito = generar_documentacion_con_deepseek(transcripciones_file)
        
        if exito:
            print("✅ Documentación generada exitosamente")
            print("📂 Revisa la carpeta: www/deepseek/")
        else:
            print("❌ Error al generar documentación")
            
    except KeyboardInterrupt:
        print("\n⏹️ Proceso cancelado por el usuario")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    main()