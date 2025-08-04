"""
Script para construir la aplicación web
"""

import subprocess
import sys
import os
from pathlib import Path

def build_web():
    """Construye la aplicación para web"""
    print("🚀 Iniciando build para web...")
    
    # Verificar que flet esté instalado
    try:
        import flet
        print(f"✅ Flet {flet.__version__} encontrado")
    except ImportError:
        print("❌ Flet no encontrado. Instalando...")
        subprocess.run([sys.executable, "-m", "pip", "install", "flet>=0.28.3"])
    
    # Limpiar build anterior
    build_dir = Path("build")
    if build_dir.exists():
        print("🧹 Limpiando build anterior...")
        import shutil
        shutil.rmtree(build_dir)
    
    # Crear directorio de assets si no existe
    assets_dir = Path("assets")
    if not assets_dir.exists():
        assets_dir.mkdir()
        print("📁 Directorio assets creado")
    
    # Ejecutar build
    try:
        print("🔨 Ejecutando flet build web...")
        result = subprocess.run([
            sys.executable, "-m", "flet", "build", "web",
            "--module-name", "main",
            "--base-url", "/",
            "--route-url-strategy", "path"
        ], check=True, capture_output=True, text=True)
        
        print("✅ Build completado exitosamente!")
        print(f"📦 Archivos generados en: {build_dir / 'web'}")
        
        # Mostrar información del build
        web_dir = build_dir / "web"
        if web_dir.exists():
            files = list(web_dir.rglob("*"))
            print(f"📊 Total de archivos generados: {len(files)}")
            
            # Buscar index.html
            index_file = web_dir / "index.html"
            if index_file.exists():
                print(f"🌐 Archivo principal: {index_file}")
            
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en el build: {e}")
        print(f"Salida: {e.stdout}")
        print(f"Error: {e.stderr}")
        return False

def serve_web():
    """Sirve la aplicación web localmente"""
    web_dir = Path("build/web")
    if not web_dir.exists():
        print("❌ No se encontró el build web. Ejecuta build_web() primero.")
        return
    
    print("🌐 Sirviendo aplicación web...")
    print("📍 URL: http://localhost:8000")
    print("⏹️  Presiona Ctrl+C para detener")
    
    os.chdir(web_dir)
    subprocess.run([sys.executable, "-m", "http.server", "8000"])

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Build y serve para aplicación web")
    parser.add_argument("--serve", action="store_true", help="Servir aplicación después del build")
    parser.add_argument("--only-serve", action="store_true", help="Solo servir (sin build)")
    
    args = parser.parse_args()
    
    if args.only_serve:
        serve_web()
    else:
        success = build_web()
        if success and args.serve:
            serve_web()
