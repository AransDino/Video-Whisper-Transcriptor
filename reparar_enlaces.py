#!/usr/bin/env python3
"""
Script para reparar los enlaces en los archivos HTML ya generados
"""
import pathlib
import re

def reparar_enlaces_index(archivo_index, motor):
    """Reparar enlaces en archivo index"""
    print(f"🔧 Reparando enlaces en {archivo_index.name}")
    
    with open(archivo_index, 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    contenido_original = contenido
    
    # Convertir "fase-F1.html" -> "www/motor/fase-F1.html"
    contenido = re.sub(r'href="(fase-F\d+\.html)"', rf'href="www/{motor}/\1"', contenido)
    contenido = re.sub(r"href='(fase-F\d+\.html)'", rf"href='www/{motor}/\1'", contenido)
    
    # También para temas si existen
    contenido = re.sub(r'href="(tema-T\d+\.html)"', rf'href="www/{motor}/\1"', contenido)
    contenido = re.sub(r"href='(tema-T\d+\.html)'", rf"href='www/{motor}/\1'", contenido)
    
    if contenido != contenido_original:
        with open(archivo_index, 'w', encoding='utf-8') as f:
            f.write(contenido)
        print(f"   ✅ Enlaces reparados en {archivo_index.name}")
        return True
    else:
        print(f"   ℹ️  No se encontraron enlaces que reparar en {archivo_index.name}")
        return False

def reparar_enlaces_fases(carpeta_motor, motor):
    """Reparar enlaces en archivos de fases"""
    carpeta = pathlib.Path(carpeta_motor)
    archivos_reparados = 0
    
    for archivo in carpeta.glob("*.html"):
        print(f"🔧 Reparando enlaces en {archivo.name}")
        
        with open(archivo, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        contenido_original = contenido
        
        # Enlaces al index desde subcarpetas www/motor/
        contenido = re.sub(r'href="index\.html"', rf'href="../../index-{motor}.html"', contenido)
        contenido = re.sub(r"href='index\.html'", rf"href='../../index-{motor}.html'", contenido)
        
        if contenido != contenido_original:
            with open(archivo, 'w', encoding='utf-8') as f:
                f.write(contenido)
            print(f"   ✅ Enlaces reparados en {archivo.name}")
            archivos_reparados += 1
        else:
            print(f"   ℹ️  No se encontraron enlaces que reparar en {archivo.name}")
    
    return archivos_reparados

def main():
    print("🔧 REPARADOR DE ENLACES HTML")
    print("=" * 50)
    
    # Lista de motores y sus archivos
    motores = {
        "openai": {
            "index": "index-openai.html",
            "carpeta": "www/openai"
        },
        "ollama": {
            "index": "index-ollama.html", 
            "carpeta": "www/ollama"
        },
        "deepseek": {
            "index": "index-deepseek.html",
            "carpeta": "www/deepseek"
        }
    }
    
    total_reparados = 0
    
    for motor, config in motores.items():
        print(f"\n🔍 Verificando motor: {motor.upper()}")
        
        # Verificar y reparar index
        archivo_index = pathlib.Path(config["index"])
        if archivo_index.exists():
            if reparar_enlaces_index(archivo_index, motor):
                total_reparados += 1
        else:
            print(f"   ⚠️  No se encontró {config['index']}")
        
        # Verificar y reparar archivos en carpeta
        carpeta_motor = pathlib.Path(config["carpeta"])
        if carpeta_motor.exists():
            reparados = reparar_enlaces_fases(carpeta_motor, motor)
            total_reparados += reparados
        else:
            print(f"   ⚠️  No se encontró la carpeta {config['carpeta']}")
    
    print(f"\n✅ Proceso completado: {total_reparados} archivos reparados")
    
    if total_reparados > 0:
        print("\n🎉 Los enlaces ahora deberían funcionar correctamente:")
        print("   - Desde index-{motor}.html a las fases")
        print("   - Desde las fases de vuelta al index correspondiente")

if __name__ == "__main__":
    main()