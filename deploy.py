"""
Script de deployment para diferentes plataformas
"""

import subprocess
import sys
import os
import shutil
from pathlib import Path
import zipfile
import json
from datetime import datetime

def deploy_web():
    """Deploy para web"""
    print("🌐 Preparando deployment web...")
    
    # Build web
    if not build_web():
        return False
    
    # Copiar archivos adicionales
    web_dir = Path("build/web")
    
    # Copiar manifest.json
    manifest_src = Path("assets/manifest.json")
    if manifest_src.exists():
        shutil.copy2(manifest_src, web_dir / "manifest.json")
        print("✅ Manifest copiado")
    
    # Crear .htaccess para Apache (si es necesario)
    htaccess_content = """
RewriteEngine On
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^(.*)$ index.html [QSA,L]

# Habilitar compresión
<IfModule mod_deflate.c>
    AddOutputFilterByType DEFLATE text/plain
    AddOutputFilterByType DEFLATE text/html
    AddOutputFilterByType DEFLATE text/xml
    AddOutputFilterByType DEFLATE text/css
    AddOutputFilterByType DEFLATE application/xml
    AddOutputFilterByType DEFLATE application/xhtml+xml
    AddOutputFilterByType DEFLATE application/rss+xml
    AddOutputFilterByType DEFLATE application/javascript
    AddOutputFilterByType DEFLATE application/x-javascript
</IfModule>

# Cache headers
<IfModule mod_expires.c>
    ExpiresActive on
    ExpiresByType text/css "access plus 1 year"
    ExpiresByType application/javascript "access plus 1 year"
    ExpiresByType image/png "access plus 1 year"
    ExpiresByType image/jpg "access plus 1 year"
    ExpiresByType image/jpeg "access plus 1 year"
    ExpiresByType image/gif "access plus 1 year"
    ExpiresByType image/svg+xml "access plus 1 year"
</IfModule>
"""
    
    htaccess_file = web_dir / ".htaccess"
    with open(htaccess_file, 'w', encoding='utf-8') as f:
        f.write(htaccess_content)
    print("✅ .htaccess creado")
    
    # Crear archivo de información de deployment
    deploy_info = {
        "build_date": datetime.now().isoformat(),
        "version": "1.0.0",
        "platform": "web",
        "files_count": len(list(web_dir.rglob("*"))),
        "size_mb": sum(f.stat().st_size for f in web_dir.rglob("*") if f.is_file()) / (1024 * 1024)
    }
    
    with open(web_dir / "deploy-info.json", 'w', encoding='utf-8') as f:
        json.dump(deploy_info, f, indent=2)
    
    print(f"✅ Deployment web completado")
    print(f"📊 Archivos: {deploy_info['files_count']}")
    print(f"📦 Tamaño: {deploy_info['size_mb']:.2f} MB")
    print(f"📁 Ubicación: {web_dir}")
    
    return True

def deploy_pythonanywhere():
    """Deploy específico para PythonAnywhere"""
    print("🐍 Preparando deployment para PythonAnywhere...")
    
    if not deploy_web():
        return False
    
    web_dir = Path("build/web")
    pa_dir = Path("build/pythonanywhere")
    
    # Crear directorio para PythonAnywhere
    if pa_dir.exists():
        shutil.rmtree(pa_dir)
    pa_dir.mkdir(parents=True)
    
    # Copiar archivos web
    shutil.copytree(web_dir, pa_dir / "static", dirs_exist_ok=True)
    
    # Crear wsgi.py específico para PythonAnywhere
    wsgi_content = '''
"""
WSGI para PythonAnywhere - Pérdidas Matanzas
"""
import sys
import os
from pathlib import Path

# Configurar path del proyecto
project_home = '/home/tuusuario/perdidas-matanzas'  # CAMBIAR POR TU USUARIO
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Importar Flask para servir archivos estáticos
from flask import Flask, send_from_directory, send_file

app = Flask(__name__)

# Directorio de archivos estáticos
STATIC_DIR = os.path.join(project_home, 'build', 'pythonanywhere', 'static')

@app.route('/')
def index():
    """Página principal"""
    return send_file(os.path.join(STATIC_DIR, 'index.html'))

@app.route('/<path:filename>')
def static_files(filename):
    """Servir archivos estáticos"""
    return send_from_directory(STATIC_DIR, filename)

# Para PythonAnywhere
application = app

if __name__ == '__main__':
    app.run(debug=False)
'''
    
    with open(pa_dir / "wsgi.py", 'w', encoding='utf-8') as f:
        f.write(wsgi_content)
    
    # Crear requirements.txt para PythonAnywhere
    pa_requirements = """
flask>=2.0.0
flet>=0.28.3
pydantic>=2.0.0
python-dotenv>=1.0.0
"""
    
    with open(pa_dir / "requirements.txt", 'w', encoding='utf-8') as f:
        f.write(pa_requirements)
    
