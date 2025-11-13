#!/usr/bin/env python3
"""
Ejecutar solo la generación de documentación con Ollama
usando transcripciones existentes
"""
import sys
import pathlib
from datetime import datetime
sys.path.append(str(pathlib.Path(__file__).parent))

from transcribir import generar_documentacion_con_ollama

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
    
    # Generar documentación con Ollama
    resultado = generar_documentacion_con_ollama(transcripciones_file)
    
    if resultado:
        print(f"✅ Documentación generada exitosamente")
        print(f"📂 Revisa la carpeta: www/ollama/")
    else:
        print("❌ Error al generar documentación")

if __name__ == "__main__":
    main()