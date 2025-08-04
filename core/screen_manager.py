"""
Gestor de pantallas de la aplicación
Maneja la navegación entre diferentes pantallas
"""

import flet as ft
from typing import Dict, Callable, Any, Optional
from core.logger import get_logger

class ScreenManager:
    """Gestor de pantallas y navegación"""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.logger = get_logger(__name__)
        self.screens: Dict[str, Callable] = {}
        self.current_screen = None
        self.history = []
    
    def register_screen(self, name: str, screen_factory: Callable):
        """Registra una pantalla en el gestor"""
        self.screens[name] = screen_factory
        self.logger.info(f"Pantalla registrada: {name}")
    
    def navigate_to(self, screen_name: str, **kwargs) -> bool:
        """Navega a una pantalla específica"""
        try:
            if screen_name not in self.screens:
                self.logger.error(f"Pantalla no encontrada: {screen_name}")
                return False
            
            # Crear la pantalla usando la función registrada
            screen_factory = self.screens[screen_name]
            
            screen_instance = screen_factory(**kwargs)
            
            # Construir la interfaz
            screen_content = screen_instance.build()
            
            # Limpiar la página y agregar el nuevo contenido
            self.page.clean()
            self.page.add(screen_content)
            self.page.update()
            
            # Actualizar historial
            if self.current_screen:
                self.history.append(self.current_screen)
            
            self.current_screen = screen_name
            self.logger.info(f"Navegación exitosa a: {screen_name}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error al navegar a {screen_name}: {e}")
            import traceback
            self.logger.error(f"Traceback: {traceback.format_exc()}")
            return False

    def go_back(self) -> bool:
        """Navega a la pantalla anterior"""
        if not self.history:
            self.logger.warning("No hay pantalla anterior en el historial")
            return False
        
        previous_screen = self.history.pop()
        return self.navigate_to(previous_screen)
    
    def clear_history(self):
        """Limpia el historial de navegación"""
        self.history.clear()
        self.logger.info("Historial de navegación limpiado")
    
    def get_current_screen(self) -> Optional[str]:
        """Obtiene el nombre de la pantalla actual"""
        return self.current_screen
