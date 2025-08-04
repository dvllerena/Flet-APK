"""
Punto de entrada para la aplicación web
"""
import flet as ft
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT_DIR))

from main import main

if __name__ == "__main__":
    print("Iniciando aplicación web en puerto 8000...")
    ft.app(
        target=main,
        view=ft.AppView.WEB_BROWSER,
        port=8000,
        host="0.0.0.0"
    )
