"""
WSGI para PythonAnywhere - Versión híbrida
"""
import sys
import os
from pathlib import Path

# Configurar path del proyecto (CAMBIAR ESTA RUTA)
project_home = '/home/tuusuario/perdidas_matanzas_app'  # ⚠️ CAMBIAR 'tuusuario'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Configurar modo web
os.environ["FLET_WEB_MODE"] = "true"

# Importar Flask para servir la aplicación
from flask import Flask, Response, request, jsonify
import flet as ft
from web_main import main_web

app = Flask(__name__)

@app.route('/')
def index():
    """Página principal con información"""
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <title>Pérdidas Eléctricas - Matanzas</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { 
                font-family: Arial, sans-serif; 
                text-align: center; 
                padding: 50px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                min-height: 100vh;
                margin: 0;
            }
            .container {
                background: rgba(255,255,255,0.1);
                padding: 40px;
                border-radius: 15px;
                backdrop-filter: blur(10px);
                max-width: 600px;
                margin: 0 auto;
            }
            .btn {
                background: #4CAF50;
                color: white;
                padding: 15px 30px;
                border: none;
                border-radius: 5px;
                font-size: 16px;
                cursor: pointer;
                text-decoration: none;
                display: inline-block;
                margin: 10px;
            }
            .btn:hover { background: #45a049; }
            .info { margin: 20px 0; opacity: 0.9; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>⚡ Análisis de Pérdidas Eléctricas</h1>
            <h2>Provincia de Matanzas</h2>
            
            <div class="info">
                <p>🌐 <strong>Versión Web</strong> - Sistema UNE</p>
                <p>📊 Análisis en tiempo real de pérdidas eléctricas</p>
                <p>🏛️ Gestión por municipios</p>
                <p>📈 Reportes y estadísticas</p>
            </div>
            
            <a href="/app" class="btn">🚀 Iniciar Aplicación</a>
            <a href="/status" class="btn">📊 Estado del Sistema</a>
            
            <div class="info" style="margin-top: 40px;">
                <p><small>Sistema desarrollado para la UNE - Matanzas</small></p>
                <p><small>Versión 1.0.0 - Modo Web</small></p>
            </div>
        </div>
    </body>
    </html>
    """

@app.route('/app')
def flet_app():
    """Redirige a la aplicación Flet"""
    try:
        # En PythonAnywhere, redirigir al puerto de Flet
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Cargando aplicación...</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body { 
                    font-family: Arial, sans-serif; 
                    text-align: center; 
                    padding: 50px;
                    background: #f0f2f5;
                }
                .loader {
                    border: 4px solid #f3f3f3;
                    border-top: 4px solid #3498db;
                    border-radius: 50%;
                    width: 50px;
                    height: 50px;
                    animation: spin 1s linear infinite;
                    margin: 20px auto;
                }
                @keyframes spin {
                    0% { transform: rotate(0deg); }
                    100% { transform: rotate(360deg); }
                }
            </style>
        </head>
        <body>
            <h2>⚡ Cargando Aplicación de Pérdidas...</h2>
            <div class="loader"></div>
            <p>Iniciando sistema UNE - Matanzas</p>
            <p><small>Si la aplicación no carga automáticamente, <a href="/">vuelva al inicio</a></small></p>
            
            <script>
                // Intentar cargar la aplicación Flet
                setTimeout(function() {
                    try {
                        // Aquí se inicializaría la aplicación Flet
                        document.body.innerHTML = '<div id="flet-app">Cargando interfaz...</div>';
                        
                        // En un entorno real, aquí se cargaría Flet
                        // Por ahora, mostrar mensaje
                        setTimeout(function() {
                            document.getElementById('flet-app').innerHTML = 
                                '<h3>🚧 Aplicación en desarrollo</h3>' +
                                '<p>La interfaz Flet se cargará aquí</p>' +
                                '<a href="/">← Volver al inicio</a>';
                        }, 2000);
                        
                    } catch(e) {
                        document.body.innerHTML = 
                            '<h3>❌ Error cargando aplicación</h3>' +
                            '<p>' + e.message + '</p>' +
                            '<a href="/">← Volver al inicio</a>';
                    }
                }, 1000);
            </script>
        </body>
        </html>
        """
    except Exception as e:
        return f"""
        <html>
        <body style="font-family: Arial; text-align: center; padding: 50px;">
            <h2>❌ Error</h2>
            <p>No se pudo iniciar la aplicación: {str(e)}</p>
            <a href="/">← Volver al inicio</a>
        </body>
        </html>
        """

@app.route('/status')
def status():
    """Estado del sistema"""
    try:
        import platform
        import datetime
        
        status_info = {
            "status": "online",
            "mode": "web",
            "platform": platform.platform(),
            "python_version": sys.version,
            "timestamp": datetime.datetime.now().isoformat(),
            "features": [
                "dashboard",
                "calculo_energia", 
                "facturacion",
                "infoperdidas",
                "l_ventas"
            ]
        }
        
        return jsonify(status_info)
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e),
            "timestamp": datetime.datetime.now().isoformat()
        })

@app.route('/health')
def health():
    """Health check para monitoreo"""
    return jsonify({
        "status": "healthy",
        "service": "perdidas-matanzas-web",
        "version": "1.0.0"
    })

@app.route('/api/info')
def api_info():
    """Información de la API"""
    return jsonify({
        "name": "Pérdidas Eléctricas - Matanzas",
        "version": "1.0.0",
        "mode": "web",
        "endpoints": [
            "/",
            "/app", 
            "/status",
            "/health",
            "/api/info"
        ]
    })

@app.errorhandler(404)
def not_found(error):
    """Página 404 personalizada"""
    return """
    <html>
    <body style="font-family: Arial; text-align: center; padding: 50px; background: #f8f9fa;">
        <h2>🔍 Página no encontrada</h2>
        <p>La página que busca no existe.</p>
        <a href="/" style="color: #007bff; text-decoration: none;">← Volver al inicio</a>
    </body>
    </html>
    """, 404

@app.errorhandler(500)
def internal_error(error):
    """Página 500 personalizada"""
    return """
    <html>
    <body style="font-family: Arial; text-align: center; padding: 50px; background: #f8f9fa;">
        <h2>⚠️ Error interno del servidor</h2>
        <p>Ocurrió un error interno. Intente nuevamente más tarde.</p>
        <a href="/" style="color: #007bff; text-decoration: none;">← Volver al inicio</a>
    </body>
    </html>
    """, 500

# Para PythonAnywhere
application = app

if __name__ == "__main__":
    print(" Iniciando servidor WSGI para PythonAnywhere...")
    print("Modo: WEB")
    print("Puerto: 5000 (desarrollo)")
    print("=" * 50)
    
    # Solo para desarrollo local
    app.run(debug=True, host='0.0.0.0', port=5000)

