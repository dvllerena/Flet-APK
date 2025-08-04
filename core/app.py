"""
Aplicación principal web
"""

import flet as ft
from typing import Optional, Dict, Any
from core.logger import get_logger
from core.database import get_db_manager
from core.screen_manager import ScreenManager
from authentication.screens.login_screen import LoginScreen
from dashboard.screens.main_dashboard import MainDashboard
from calculo_energia.screens.energia_main_screen import EnergiaMainScreen
from calculo_energia.screens.energia_edit_screen import EnergiaEditScreen
from calculo_energia.screens.energia_view_screen import EnergiaViewScreen
from facturacion.screens.facturacion_main_screen import FacturacionMainScreen
from facturacion.screens.facturacion_edit_screen import FacturacionEditScreen
from facturacion.screens.facturacion_transfers_screen import FacturacionTransfersScreen
from infoperdidas.screens.infoperdidas_main_screen import InfoPerdidasMainScreen
from infoperdidas.screens.infoperdidas_planes_screen import InfoPerdidasPlanesScreen
from l_ventas.screens.lventas_main_screen import LVentasMainScreen

class PerdidasMatanzasApp:
    """Aplicación web de Pérdidas Matanzas"""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.logger = get_logger(__name__)
        self.current_user = None
        
        # Inicializar componentes
        self.screen_manager = ScreenManager(page)
        self.screen_manager.app_instance = self
        self.db_manager = get_db_manager()
        
        # Registrar pantallas
        self._register_screens()

    def _register_screens(self):
        """Registra todas las pantallas de la aplicación"""
        # Pantallas principales
        self.screen_manager.register_screen("login", lambda **kwargs: LoginScreen(self))
        self.screen_manager.register_screen("dashboard", lambda **kwargs: MainDashboard(self))
        
        # Pantallas de energía
        self.screen_manager.register_screen("calculo_energia", lambda **kwargs: EnergiaMainScreen(self))
        self.screen_manager.register_screen("energia_edit", lambda **kwargs: EnergiaEditScreen(self, **kwargs))
        self.screen_manager.register_screen("energia_view", lambda **kwargs: EnergiaViewScreen(self, **kwargs))
        # Pantallas de facturación
        self.screen_manager.register_screen("facturacion", lambda **kwargs: FacturacionMainScreen(self))
        self.screen_manager.register_screen("facturacion_edit", lambda **kwargs: FacturacionEditScreen(self, **kwargs))
        self.screen_manager.register_screen("facturacion_transfers", lambda **kwargs: FacturacionTransfersScreen(self, **kwargs))
        
        # Pantallas de InfoPérdidas
        self.screen_manager.register_screen("infoperdidas", lambda **kwargs: InfoPerdidasMainScreen(self))
        self.screen_manager.register_screen("infoperdidas_planes", lambda **kwargs: InfoPerdidasPlanesScreen(self))
        
        # Pantallas de LVentas
        self.screen_manager.register_screen("l_ventas", lambda **kwargs: LVentasMainScreen(self))
        
        self.logger.info("Pantallas registradas correctamente")
 
    def initialize(self):
        """Inicializa la aplicación"""
        try:
            # Inicializar base de datos
            self.db_manager.initialize()
            self.logger.info("Base de datos web inicializada")
            
            # Mostrar pantalla de login
            self.navigate_to("login")
            
            self.logger.info("Aplicación web inicializada correctamente")
            
        except Exception as e:
            self.logger.error(f"Error al inicializar aplicación: {e}")
            self._show_error_screen(str(e))
    
    def navigate_to(self, screen_name: str, **kwargs):
        """Navega a una pantalla específica"""
        try:
            self.logger.info(f"Navegando a: {screen_name}")
            
            if screen_name not in ["login"] and not self.is_authenticated():
                self.logger.warning("Intento de acceso sin autenticación")
                self.navigate_to("login")
                return
            
            success = self.screen_manager.navigate_to(screen_name, **kwargs)
            
            if success:
                self.logger.info(f"Navegación exitosa a: {screen_name}")
            else:
                self.logger.error(f"Navegación falló a: {screen_name}")
                
        except Exception as e:
            self.logger.error(f"Error en navegación a {screen_name}: {e}")
    
    def set_current_user(self, user: Dict[str, Any]):
        """Establece el usuario actual"""
        self.current_user = user
        self.logger.info(f"Usuario establecido: {user.get('username')}")
    
    def get_current_user(self) -> Optional[Dict[str, Any]]:
        """Obtiene el usuario actual"""
        return self.current_user
    
    def is_authenticated(self) -> bool:
        """Verifica si hay un usuario autenticado"""
        return self.current_user is not None
    
    def logout(self):
        """Cierra la sesión del usuario"""
        if self.current_user:
            self.logger.info(f"Cerrando sesión: {self.current_user.get('username')}")
            self.current_user = None
        
        self.screen_manager.clear_history()
        self.navigate_to("login")
    
    def _show_error_screen(self, error_message: str):
        """Muestra una pantalla de error"""
        error_content = ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.ERROR, color=ft.Colors.RED, size=64),
                ft.Text("Error de Aplicación Web", size=24, weight=ft.FontWeight.BOLD),
                ft.Text(error_message, size=16, text_align=ft.TextAlign.CENTER),
                ft.Container(height=20),
                ft.ElevatedButton(
                    "Reintentar",
                    on_click=lambda _: self.initialize()
                ),
                ft.ElevatedButton(
                    "Recargar Página",
                    on_click=lambda _: self.page.go("/")
                )
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            alignment=ft.alignment.center,
            expand=True
        )
        
        self.page.clean()
        self.page.add(error_content)
        self.page.update()
