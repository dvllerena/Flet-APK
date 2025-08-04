"""
Pantalla de login para aplicación web
"""

import flet as ft
from typing import Optional
from authentication.services.auth_service import AuthService
from core.logger import get_logger

class LoginScreen:
    """Pantalla de login web"""
    
    def __init__(self, app):
        self.app = app
        self.page = app.page
        self.logger = get_logger(__name__)
        self.auth_service = AuthService()
        
        # Controles de la interfaz
        self.username_field = None
        self.password_field = None
        self.login_button = None
        self.error_text = None
        self.loading_ring = None
        
    def build(self) -> ft.Container:
        """Construye la interfaz de login web"""
        
        # Configuración para web
        field_width = 350
        card_width = 420
        card_padding = 40
        logo_size = 70
        title_size = 28
        subtitle_size = 18
        field_height = 55
        button_height = 50
        spacing_large = 25
        spacing_medium = 18
        spacing_small = 12
        
        # Campo de usuario
        self.username_field = ft.TextField(
            label="Usuario",
            prefix_icon=ft.Icons.PERSON_OUTLINE,
            width=field_width,
            height=field_height,
            text_size=14,
            on_submit=self._on_login_click,
            border_radius=10,
            filled=True,
            bgcolor=ft.Colors.WHITE,
            border_color=ft.Colors.BLUE_200,
            focused_border_color=ft.Colors.BLUE_500,
            cursor_color=ft.Colors.BLUE_500,
            selection_color=ft.Colors.BLUE_100,
            value="admin"  # Valor por defecto para facilitar testing
        )
        
        # Campo de contraseña
        self.password_field = ft.TextField(
            label="Contraseña",
            prefix_icon=ft.Icons.LOCK_OUTLINE,
            password=True,
            can_reveal_password=True,
            width=field_width,
            height=field_height,
            text_size=14,
            on_submit=self._on_login_click,
            border_radius=10,
            filled=True,
            bgcolor=ft.Colors.WHITE,
            border_color=ft.Colors.BLUE_200,
            focused_border_color=ft.Colors.BLUE_500,
            cursor_color=ft.Colors.BLUE_500,
            selection_color=ft.Colors.BLUE_100,
            value="admin"  # Valor por defecto para facilitar testing
        )
        
        # Botón de login
        self.login_button = ft.ElevatedButton(
            content=ft.Row([
                ft.Icon(ft.Icons.LOGIN, color=ft.Colors.WHITE, size=18),
                ft.Text("Iniciar Sesión", color=ft.Colors.WHITE, size=14, weight=ft.FontWeight.W_600)
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=6),
            width=field_width,
            height=button_height,
            on_click=self._on_login_click,
            bgcolor=ft.Colors.BLUE_600,
            color=ft.Colors.WHITE,
            elevation=3
        )
        
        # Texto de error
        self.error_text = ft.Container(
            content=ft.Text(
                "",
                color=ft.Colors.RED_600,
                size=12,
                text_align=ft.TextAlign.CENTER,
                weight=ft.FontWeight.W_500
            ),
            width=field_width,
            visible=False,
            bgcolor=ft.Colors.RED_50,
            border_radius=6,
            padding=ft.padding.symmetric(horizontal=10, vertical=6),
            border=ft.border.all(1, ft.Colors.RED_200)
        )
        
        # Indicador de carga
        self.loading_ring = ft.Container(
            content=ft.Column([
                ft.ProgressRing(
                    width=25,
                    height=25,
                    stroke_width=2,
                    color=ft.Colors.BLUE_500
                ),
                ft.Container(height=5),
                ft.Text(
                    "Verificando...",
                    size=10,
                    color=ft.Colors.BLUE_600,
                    text_align=ft.TextAlign.CENTER
                )
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            visible=False
        )
        
        # Logo y título
        logo_section = ft.Column([
            ft.Container(
                content=ft.Icon(
                    ft.Icons.ELECTRIC_BOLT,
                    size=logo_size,
                    color=ft.Colors.WHITE
                ),
                width=logo_size + 20,
                height=logo_size + 20,
                bgcolor=ft.Colors.BLUE_600,
                border_radius=(logo_size + 20) // 2,
                alignment=ft.alignment.center
            ),
            ft.Container(height=spacing_medium),
            ft.Text(
                "Pérdidas Eléctricas",
                size=title_size,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER,
                color=ft.Colors.BLUE_800
            ),
            ft.Text(
                "Provincia de Matanzas",
                size=subtitle_size,
                color=ft.Colors.BLUE_600,
                text_align=ft.TextAlign.CENTER,
                weight=ft.FontWeight.W_500
            )
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0)
        
        # Formulario de login
        login_form = ft.Column([
            self.username_field,
            ft.Container(height=spacing_medium),
            self.password_field,
            ft.Container(height=spacing_large),
            self.login_button,
            ft.Container(height=spacing_small),
            self.error_text,
            ft.Container(height=spacing_small),
            self.loading_ring
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0)
        
        # Información adicional
        info_section = ft.Column([
            ft.Divider(color=ft.Colors.BLUE_100, thickness=1),
            ft.Container(height=spacing_small),
            ft.Row([
                ft.Icon(ft.Icons.INFO_OUTLINE, size=14, color=ft.Colors.BLUE_500),
                ft.Text(
                    "Sistema UNE v1.0 - Web",
                    size=10,
                    color=ft.Colors.BLUE_600,
                    weight=ft.FontWeight.W_500
                )
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=6),
            ft.Container(height=4),
            ft.Row([
                ft.Icon(ft.Icons.SECURITY, size=14, color=ft.Colors.GREEN_500),
                ft.Text(
                    "Conexión Segura",
                    size=10,
                    color=ft.Colors.GREEN_600,
                    weight=ft.FontWeight.W_500
                )
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=6),
            ft.Container(height=spacing_small),
            ft.Container(
                content=ft.Text(
                    "👤 Usuario: admin | 🔑 Contraseña: admin",
                    size=10,
                    color=ft.Colors.ORANGE_600,
                    weight=ft.FontWeight.W_500,
                    text_align=ft.TextAlign.CENTER
                ),
                bgcolor=ft.Colors.ORANGE_50,
                padding=ft.padding.symmetric(horizontal=12, vertical=6),
                border_radius=15,
                border=ft.border.all(1, ft.Colors.ORANGE_200)
            )
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0)
        
        # Contenedor principal
        main_content = ft.Column([
            logo_section,
            ft.Container(height=spacing_large),
            login_form,
            ft.Container(height=spacing_medium),
            info_section
        ], 
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=0,
        scroll=ft.ScrollMode.AUTO
        )
        
        # Card contenedor
        content_container = ft.Container(
            content=main_content,
            padding=card_padding,
            width=card_width,
            bgcolor=ft.Colors.WHITE,
            border_radius=15,
            border=ft.border.all(1, ft.Colors.BLUE_50)
        )
        
        # Contenedor principal con gradiente
        return ft.Container(
            content=ft.Column([
                content_container
            ], 
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO
            ),
            alignment=ft.alignment.center,
            expand=True,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[
                    ft.Colors.BLUE_50,
                    ft.Colors.BLUE_100,
                    ft.Colors.INDIGO_50,
                    ft.Colors.BLUE_50
                ]
            ),
            padding=20
        )
    
    def _on_login_click(self, e):
        """Maneja el clic del botón de login"""
        username = self.username_field.value
        password = self.password_field.value
        
        self.logger.info(f"Intento de login web - Usuario: '{username}'")
        
        if not username or not password:
            self._show_error("Complete todos los campos")
            return
        
        self._set_loading(True)
        
        try:
            result = self.auth_service.login(username, password)
            
            self.logger.info(f"Resultado de autenticación: {result}")
            
            if result["success"]:
                self.logger.info(f"Login exitoso para: {username}")
                
                self.app.set_current_user(result["user"])
                self.app.navigate_to("dashboard")
                
            else:
                self._show_error(result["message"])
                
        except Exception as ex:
            self.logger.error(f"Error en login: {ex}")
            self._show_error("Error del sistema")
        
        finally:
            self._set_loading(False)
    
    def _show_error(self, message: str):
        """Muestra un mensaje de error"""
        self.error_text.content.value = f"⚠️ {message}"
        self.error_text.visible = True
        self.page.update()
        
        # Limpiar error después de 4 segundos
        import threading
        def clear_error():
            if self.error_text:
                self.error_text.visible = False
                if self.page:
                    self.page.update()
        
        timer = threading.Timer(4.0, clear_error)
        timer.start()
    
    def _set_loading(self, loading: bool):
        """Controla el estado de carga"""
        self.loading_ring.visible = loading
        self.login_button.disabled = loading
        
        if loading:
            self.login_button.content = ft.Row([
                ft.ProgressRing(width=14, height=14, stroke_width=2, color=ft.Colors.WHITE),
                ft.Text("Iniciando...", color=ft.Colors.WHITE, size=14, weight=ft.FontWeight.W_600)
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=6)
            
            self.username_field.disabled = True
            self.password_field.disabled = True
        else:
            self.login_button.content = ft.Row([
                ft.Icon(ft.Icons.LOGIN, color=ft.Colors.WHITE, size=18),
                ft.Text("Iniciar Sesión", color=ft.Colors.WHITE, size=14, weight=ft.FontWeight.W_600)
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=6)
            
            self.username_field.disabled = False
            self.password_field.disabled = False
        
        self.page.update()
