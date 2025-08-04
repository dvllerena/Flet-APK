
"""
Aplicación Web de Análisis de Pérdidas Eléctricas - Matanzas
"""

import flet as ft      
import sys
from pathlib import Path    

# Agregar el directorio raíz al path de Python
ROOT_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT_DIR))

def main(page: ft.Page):
    """Función principal de la aplicación Flet WEB"""
    try:
        from core.app import PerdidasMatanzasApp
        from core.logger import setup_logger
        from core.config import load_config
        
        # Configurar el sistema de logging para WEB
        logger = setup_logger()
        logger.info("=== Iniciando Aplicación Web de Pérdidas Matanzas ===")
        
        # Cargar configuraciones WEB
        config = load_config()
        app_config = config.get_app_config()
        logger.info("Configuraciones web cargadas correctamente")
        
        # Configurar la página para WEB
        page.title = app_config["name"]
        page.theme_mode = ft.ThemeMode.LIGHT
        page.padding = 0
        page.spacing = 0
        page.scroll = ft.ScrollMode.AUTO
        page.adaptive = True
        
        # Crear y ejecutar la aplicación
        app = PerdidasMatanzasApp(page)
        logger.info("Aplicación Web Flet inicializada")
        
        # Inicializar la aplicación
        app.initialize()
        
    except Exception as e:
        print(f"Error: {e}")
        
        # Mostrar error en la página
        page.clean()
        page.add(
            ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.ERROR, color=ft.Colors.RED, size=64),
                    ft.Text("Error al iniciar la aplicación web", size=20, weight=ft.FontWeight.BOLD),
                    ft.Text(str(e), size=14),
                    ft.ElevatedButton("Recargar", on_click=lambda _: page.go("/"))
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                alignment=ft.alignment.center,
                expand=True
            )
        )
        page.update()

if __name__ == "__main__":
    print("Iniciando Aplicación Web de Pérdidas Eléctricas - Matanzas")
    print("Provincia: Matanzas, Cuba")
    print("Sistema: UNE - Versión Web")
    print("=" * 50)

    # Ejecutar la aplicación Flet para WEB
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=8080)
