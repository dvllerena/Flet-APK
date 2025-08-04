"""
Pantalla principal del módulo LVentas
Visualización de datos para usuarios invitados - VERSIÓN CON PESTAÑAS
"""

import flet as ft
import sys
from typing import List, Dict, Any, Optional
from core.logger import get_logger
from datetime import datetime

# Importar las pestañas
from .tabs.summary_tab import SummaryTab
from .tabs.monthly_tab import MonthlyTab
from .tabs.accumulated_tab import AccumulatedTab
from .tabs.charts_tab import ChartsTab
from .tabs.config import get_theme, get_tab_config, get_message

class LVentasMainScreen:
    """Pantalla principal de LVentas - Visualización de datos con pestañas"""

    def __init__(self, app=None):
        self.app = app
        self.page = app.page if app else None
        self.logger = get_logger(__name__)
        
        # Configuración del tema
        self.theme = get_theme('default')
        
        # Estado de la pantalla
        self.selected_tab = 0
        self.tabs_data = {}
        
        # Período por defecto
        current_date = datetime.now()
        self.current_year = current_date.year
        self.current_month = current_date.month
        
        # Referencias a componentes
        self.tab_container = None
        self.tabs_bar = None
        
        # Inicializar pestañas
        self._initialize_tabs()
        
        self.logger.info("LVentasMainScreen inicializada con pestañas")

    def _initialize_tabs(self):
        """Inicializa las pestañas"""
        try:
            # Crear instancias de las pestañas
            self.summary_tab = SummaryTab(self)
            self.monthly_tab = MonthlyTab(self)
            self.accumulated_tab = AccumulatedTab(self)
            self.charts_tab = ChartsTab(self)
            
            # Lista de pestañas
            self.tabs = [
                {
                    'key': 'summary',
                    'instance': self.summary_tab,
                    'config': get_tab_config('summary')
                },
                {
                    'key': 'monthly',
                    'instance': self.monthly_tab,
                    'config': get_tab_config('monthly')
                },
                {
                    'key': 'accumulated',
                    'instance': self.accumulated_tab,
                    'config': get_tab_config('accumulated')
                },
                {
                    'key': 'charts',
                    'instance': self.charts_tab,
                    'config': get_tab_config('charts')
                }
            ]
            
            self.logger.info(f"Inicializadas {len(self.tabs)} pestañas")
            
        except Exception as e:
            self.logger.error(f"Error inicializando pestañas: {e}")
            import traceback
            self.logger.error(f"Traceback: {traceback.format_exc()}")

    def build(self) -> ft.Control:
        """Construye la interfaz de la pantalla"""
        try:
            # Layout principal
            main_content = ft.Column([
                # Header con título y botón de regreso
                self._build_header(),
                
                # Divisor
                ft.Divider(height=1, color=self.theme['border']),
                
                # Contenido principal con pestañas
                ft.Column([
                    # Barra de pestañas
                    self._build_tabs_bar(),
                    
                    # Contenido de la pestaña activa
                    self._build_tab_content()
                    
                ], expand=True, spacing=0)
                
            ], spacing=0, expand=True)
            
            return ft.Container(
                content=main_content,
                expand=True,
                padding=0,
                bgcolor=self.theme['background']
            )
            
        except Exception as e:
            self.logger.error(f"Error al construir LVentasMainScreen: {e}")
            import traceback
            self.logger.error(f"Traceback: {traceback.format_exc()}")
            return self._build_error_view(str(e))

    def _build_header(self) -> ft.Control:
        """Construye el header de la pantalla"""
        return ft.Container(
            content=ft.Row([
                # Botón de regreso
                ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    tooltip="Regresar al Dashboard",
                    on_click=self._on_back_click,
                    icon_color=self.theme['primary'],
                    icon_size=24
                ),
                
                # Título con icono
                ft.Row([
                    ft.Container(
                        content=ft.Icon(ft.Icons.VISIBILITY, color=self.theme['white'], size=24),
                        width=48, height=48,
                        bgcolor=self.theme['primary'],
                        border_radius=24,
                        alignment=ft.alignment.center
                    ),
                    ft.Container(width=15),
                    ft.Column([
                        ft.Text(
                            "LVentas - Visualización de Datos",
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color=self.theme['text_primary']
                        ),
                        ft.Text(
                            "Sistema de análisis de pérdidas eléctricas",
                            size=12,
                            color=self.theme['text_secondary']
                        )
                    ], spacing=2)
                ]),
                
                # Spacer
                ft.Container(expand=True),
                
                # Información del período actual
                self._build_period_info(),
                
                ft.Container(width=20),
                
                # Info del usuario
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.REMOVE_RED_EYE, size=16, color=self.theme['success']),
                        ft.Container(width=8),
                        ft.Text("Modo Visualización", size=12, color=self.theme['success'], weight=ft.FontWeight.W_500)
                    ]),
                    bgcolor=f"{self.theme['success']}15",
                    padding=ft.padding.symmetric(horizontal=12, vertical=6),
                    border_radius=15,
                    border=ft.border.all(1, f"{self.theme['success']}30")
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=ft.padding.symmetric(horizontal=20, vertical=15),
            bgcolor=self.theme['white'],
            border=ft.border.only(bottom=ft.BorderSide(1, self.theme['border']))
        )

    def _build_period_info(self) -> ft.Control:
        """Construye la información del período actual"""
        from .tabs.utils import get_month_name
        
        return ft.Container(
            content=ft.Column([
                ft.Text("Período Actual", size=10, color=self.theme['text_secondary']),
                ft.Text(f"{get_month_name(self.current_month)} {self.current_year}", 
                       size=12, weight=ft.FontWeight.BOLD, color=self.theme['text_primary'])
            ], spacing=2, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=f"{self.theme['info']}15",
            padding=ft.padding.symmetric(horizontal=12, vertical=8),
            border_radius=8,
            border=ft.border.all(1, f"{self.theme['info']}30")
        )
    
    def _build_tabs_bar(self) -> ft.Control:
        """Construye la barra de pestañas"""
        tab_buttons = []
        
        for i, tab in enumerate(self.tabs):
            is_selected = i == self.selected_tab
            config = tab['config']
            
            button = ft.Container(
                content=ft.Column([
                    ft.Icon(
                        config.get('icon', ft.Icons.TAB), 
                        size=20,
                        color=self.theme['white'] if is_selected else config.get('color', self.theme['primary'])
                    ),
                    ft.Container(height=4),
                    ft.Text(
                        config.get('title', 'Pestaña'), 
                        size=11,
                        weight=ft.FontWeight.BOLD,
                        color=self.theme['white'] if is_selected else config.get('color', self.theme['primary'])
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),
                width=120,
                height=60,
                bgcolor=config.get('color', self.theme['primary']) if is_selected else self.theme['light'],
                border_radius=12,
                border=ft.border.all(2, config.get('color', self.theme['primary'])),
                padding=8,
                on_click=lambda e, index=i: self._on_tab_click(index),
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=4,
                    color=f"{config.get('color', self.theme['primary'])}40",
                    offset=ft.Offset(0, 2)
                ) if is_selected else None
                
            )
            tab_buttons.append(button)
        
        return ft.Container(
            content=ft.Row(
                tab_buttons,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=15,
                wrap=False
            ),
            padding=ft.padding.symmetric(horizontal=20, vertical=15),
            bgcolor=self.theme['white'],
            border=ft.border.only(bottom=ft.BorderSide(1, self.theme['border']))
        )

    def _build_tab_content(self) -> ft.Control:
        """Construye el contenido de la pestaña activa"""
        try:
            if 0 <= self.selected_tab < len(self.tabs):
                active_tab = self.tabs[self.selected_tab]
                tab_instance = active_tab['instance']
                
                # Construir el contenido de la pestaña
                content = tab_instance.build()
                
                return ft.Container(
                    content=content,
                    expand=True,
                    padding=0
                    
                )
            else:
                return self._build_no_tab_view()
                
        except Exception as e:
            self.logger.error(f"Error construyendo contenido de pestaña: {e}")
            return self._build_tab_error_view(str(e))

    def _build_no_tab_view(self) -> ft.Control:
        """Vista cuando no hay pestaña seleccionada"""
        return ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.TAB, size=64, color=self.theme['text_secondary']),
                ft.Container(height=20),
                ft.Text("No hay pestaña seleccionada", size=18, weight=ft.FontWeight.BOLD, color=self.theme['text_primary']),
                ft.Text("Selecciona una pestaña para ver el contenido", size=14, color=self.theme['text_secondary'])
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            expand=True, 
            alignment=ft.alignment.center,
            bgcolor=self.theme['white'],
            padding=40
        )

    def _build_tab_error_view(self, error_message: str) -> ft.Control:
        """Vista de error para pestañas"""
        return ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.ERROR_OUTLINE, size=64, color=self.theme['danger']),
                ft.Container(height=20),
                ft.Text("Error en la pestaña", size=18, weight=ft.FontWeight.BOLD, color=self.theme['text_primary']),
                ft.Text(error_message, size=14, color=self.theme['text_secondary'], text_align=ft.TextAlign.CENTER),
                ft.Container(height=20),
                ft.ElevatedButton(
                    content=ft.Row([
                        ft.Icon(ft.Icons.REFRESH, size=16),
                        ft.Text("Recargar", size=14)
                    ], spacing=8),
                    on_click=self._refresh_current_tab,
                    bgcolor=self.theme['primary'],
                    color=self.theme['white']
                )
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            expand=True, 
            alignment=ft.alignment.center,
            bgcolor=self.theme['white'],
            padding=40
        )

    def _build_error_view(self, error_message: str) -> ft.Control:
        """Vista de error general"""
        return ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.ERROR, color=self.theme['danger'], size=48),
                ft.Container(height=20),
                ft.Text(f"Error al cargar la pantalla", size=16, color=self.theme['danger'], weight=ft.FontWeight.BOLD),
                ft.Text(error_message, size=14, color=self.theme['text_secondary'], text_align=ft.TextAlign.CENTER),
                ft.Container(height=20),
                ft.Row([
                    ft.ElevatedButton(
                        content=ft.Row([
                            ft.Icon(ft.Icons.REFRESH, size=16),
                            ft.Text("Reintentar", size=14)
                        ], spacing=8),
                        on_click=self._refresh_page,
                        bgcolor=self.theme['primary'],
                        color=self.theme['white']
                    ),
                    ft.Container(width=12),
                    ft.ElevatedButton(
                        content=ft.Row([
                            ft.Icon(ft.Icons.ARROW_BACK, size=16),
                            ft.Text("Regresar", size=14)
                        ], spacing=8),
                        on_click=self._on_back_click,
                        bgcolor=self.theme['text_secondary'],
                        color=self.theme['white']
                    )
                ], alignment=ft.MainAxisAlignment.CENTER)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=40,
            expand=True,
            alignment=ft.alignment.center,
            bgcolor=self.theme['white']
        )

    def _on_back_click(self, e):
        """Maneja el clic del botón de regreso"""
        try:
            self.logger.info("Regresando al dashboard")
            if self.app:
                self.app.navigate_to('dashboard')
            else:
                self.logger.warning("No se pudo navegar al dashboard - app no disponible")
        except Exception as ex:
            self.logger.error(f"Error al regresar al dashboard: {ex}")
    
    def _on_tab_click(self, tab_index: int):
        """Maneja el clic en una pestaña"""
        try:
            if 0 <= tab_index < len(self.tabs):
                self.logger.info(f"Cambiando a pestaña {tab_index}: {self.tabs[tab_index]['key']}")
                
                # Cambiar pestaña activa
                old_tab = self.selected_tab
                self.selected_tab = tab_index
                
                # Notificar a la pestaña anterior que se está desactivando
                if 0 <= old_tab < len(self.tabs):
                    try:
                        self.tabs[old_tab]['instance'].on_tab_deactivated()
                    except AttributeError:
                        pass  # La pestaña no tiene este método
                
                # Notificar a la nueva pestaña que se está activando
                try:
                    self.tabs[tab_index]['instance'].on_tab_activated()
                except AttributeError:
                    pass  # La pestaña no tiene este método
                
                # Reconstruir la pantalla
                if self.page:
                    self.page.clean()
                    self.page.add(self.build())
                    self.page.update()
                    
            else:
                self.logger.warning(f"Índice de pestaña inválido: {tab_index}")
                
        except Exception as e:
            self.logger.error(f"Error al cambiar a pestaña {tab_index}: {e}")
            import traceback
            self.logger.error(f"Traceback: {traceback.format_exc()}")
            self.show_error_message(f"Error al cambiar pestaña: {e}")

    def _refresh_current_tab(self, e=None):
        """Refresca la pestaña actual"""
        try:
            if 0 <= self.selected_tab < len(self.tabs):
                tab_instance = self.tabs[self.selected_tab]['instance']
                
                self.show_loading_message("Refrescando pestaña...")
                
                # Llamar al método de refresh de la pestaña
                if hasattr(tab_instance, 'refresh'):
                    tab_instance.refresh()
                
                # Reconstruir la pantalla
                if self.page:
                    self.page.clean()
                    self.page.add(self.build())
                    self.page.update()
                
                self.show_success_message("Pestaña actualizada correctamente")
                
        except Exception as e:
            self.logger.error(f"Error refrescando pestaña: {e}")
            self.show_error_message(f"Error al actualizar: {e}")

    def _refresh_page(self, e=None):
        """Refresca toda la página"""
        try:
            self.logger.info("Refrescando página completa")
            self.show_loading_message("Recargando aplicación...")
            
            # Reinicializar pestañas
            self._initialize_tabs()
            
            # Reconstruir la pantalla
            if self.page:
                self.page.clean()
                self.page.add(self.build())
                self.page.update()
            
            self.show_success_message("Aplicación recargada correctamente")
            
        except Exception as e:
            self.logger.error(f"Error refrescando página: {e}")
            self.show_error_message(f"Error al recargar: {e}")

    # Métodos de utilidad para mostrar mensajes
    def show_loading_message(self, message: str):
        """Muestra mensaje de carga"""
        try:
            if self.page:
                snack = ft.SnackBar(
                    content=ft.Row([
                        ft.ProgressRing(width=20, height=20, stroke_width=2, color=self.theme['white']),
                        ft.Container(width=10),
                        ft.Text(message, color=self.theme['white'], size=14)
                    ]),
                    bgcolor=self.theme['info'],
                    duration=2000
                )
                self.page.snack_bar = snack
                snack.open = True
                self.page.update()
        except Exception as e:
            self.logger.error(f"Error mostrando mensaje de carga: {e}")

    def show_success_message(self, message: str):
        """Muestra mensaje de éxito"""
        try:
            if self.page:
                snack = ft.SnackBar(
                    content=ft.Row([
                        ft.Icon(ft.Icons.CHECK_CIRCLE, color=self.theme['white'], size=20),
                        ft.Container(width=10),
                        ft.Text(message, color=self.theme['white'], size=14)
                    ]),
                    bgcolor=self.theme['success'],
                    duration=3000
                )
                self.page.snack_bar = snack
                snack.open = True
                self.page.update()
        except Exception as e:
            self.logger.error(f"Error mostrando mensaje de éxito: {e}")

    def show_error_message(self, message: str):
        """Muestra mensaje de error"""
        try:
            if self.page:
                snack = ft.SnackBar(
                    content=ft.Row([
                        ft.Icon(ft.Icons.ERROR, color=self.theme['white'], size=20),
                        ft.Container(width=10),
                        ft.Text(message, color=self.theme['white'], size=14)
                    ]),
                    bgcolor=self.theme['danger'],
                    duration=4000
                )
                self.page.snack_bar = snack
                snack.open = True
                self.page.update()
        except Exception as e:
            self.logger.error(f"Error mostrando mensaje de error: {e}")

    def show_warning_message(self, message: str):
        """Muestra mensaje de advertencia"""
        try:
            if self.page:
                snack = ft.SnackBar(
                    content=ft.Row([
                        ft.Icon(ft.Icons.WARNING, color=self.theme['white'], size=20),
                        ft.Container(width=10),
                        ft.Text(message, color=self.theme['white'], size=14)
                    ]),
                    bgcolor=self.theme['warning'],
                    duration=3500
                )
                self.page.snack_bar = snack
                snack.open = True
                self.page.update()
        except Exception as e:
            self.logger.error(f"Error mostrando mensaje de advertencia: {e}")

    def show_info_message(self, message: str):
        """Muestra mensaje informativo"""
        try:
            if self.page:
                snack = ft.SnackBar(
                    content=ft.Row([
                        ft.Icon(ft.Icons.INFO, color=self.theme['white'], size=20),
                        ft.Container(width=10),
                        ft.Text(message, color=self.theme['white'], size=14)
                    ]),
                    bgcolor=self.theme['info'],
                    duration=3000
                )
                self.page.snack_bar = snack
                snack.open = True
                self.page.update()
        except Exception as e:
            self.logger.error(f"Error mostrando mensaje informativo: {e}")

    # Métodos para acceso desde las pestañas
    def get_current_period(self) -> tuple:
        """Obtiene el período actual"""
        return self.current_year, self.current_month

    def set_current_period(self, year: int, month: int):
        try:
            self.current_year = year
            self.current_month = month
            self.logger.info(f"Período actualizado a: {month}/{year}")
            
            # Actualiza el contenido de la pantalla con el mes seleccionado
            self.page.clean()
            self.page.add(self.build(month))  # Pasa el mes seleccionado al método build
            self.page.update()
            
            # Notificar a todas las pestañas del cambio de período
            for tab in self.tabs:
                try:
                    if hasattr(tab['instance'], 'on_period_changed'):
                        tab['instance'].on_period_changed(year, month)
                except Exception as e:
                    self.logger.error(f"Error notificando cambio de período a pestaña {tab['key']}: {e}")
        except Exception as e:
            self.logger.error(f"Error actualizando período: {e}")       
    
    def get_theme(self) -> Dict[str, Any]:
        """Obtiene el tema actual"""
        return self.theme

    def get_tab_data(self, tab_key: str) -> Dict[str, Any]:
        """Obtiene datos compartidos de una pestaña"""
        return self.tabs_data.get(tab_key, {})

    def set_tab_data(self, tab_key: str, data: Dict[str, Any]):
        """Establece datos compartidos para una pestaña"""
        self.tabs_data[tab_key] = data

    def get_active_tab_key(self) -> str:
        """Obtiene la clave de la pestaña activa"""
        if 0 <= self.selected_tab < len(self.tabs):
            return self.tabs[self.selected_tab]['key']
        return ""

    def navigate_to_tab(self, tab_key: str):
        """Navega a una pestaña específica"""
        try:
            for i, tab in enumerate(self.tabs):
                if tab['key'] == tab_key:
                    self._on_tab_click(i)
                    return
            
            self.logger.warning(f"Pestaña no encontrada: {tab_key}")
            
        except Exception as e:
            self.logger.error(f"Error navegando a pestaña {tab_key}: {e}")

    def refresh_all_tabs(self):
        """Refresca todas las pestañas"""
        try:
            self.logger.info("Refrescando todas las pestañas")
            
            for tab in self.tabs:
                try:
                    if hasattr(tab['instance'], 'refresh'):
                        tab['instance'].refresh()
                except Exception as e:
                    self.logger.error(f"Error refrescando pestaña {tab['key']}: {e}")
            
            # Reconstruir la pantalla
            if self.page:
                self.page.clean()
                self.page.add(self.build())
                self.page.update()
            
            self.show_success_message("Todas las pestañas actualizadas")
            
        except Exception as e:
            self.logger.error(f"Error refrescando todas las pestañas: {e}")
            self.show_error_message("Error al actualizar pestañas")

    def export_current_tab_data(self, format_type: str = 'excel'):
        """Exporta los datos de la pestaña actual"""
        try:
            if 0 <= self.selected_tab < len(self.tabs):
                tab_instance = self.tabs[self.selected_tab]['instance']
                
                if hasattr(tab_instance, 'export_data'):
                    self.show_loading_message(f"Exportando datos en formato {format_type}...")
                    tab_instance.export_data(format_type)
                else:
                    self.show_warning_message("Esta pestaña no soporta exportación")
            else:
                self.show_error_message("No hay pestaña activa para exportar")
                
        except Exception as e:
            self.logger.error(f"Error exportando datos: {e}")
            self.show_error_message(f"Error en la exportación: {e}")

    def get_database_manager(self):
        """Obtiene el gestor de base de datos"""
        try:
            from core.database import get_db_manager
            return get_db_manager()
        except Exception as e:
            self.logger.error(f"Error obteniendo gestor de BD: {e}")
            return None

    def validate_user_permissions(self, action: str) -> bool:
        """Valida permisos del usuario para una acción"""
        # En modo visualización, solo permitir acciones de lectura
        read_actions = ['view', 'export', 'refresh']
        return action in read_actions

    def get_app_version(self) -> str:
        """Obtiene la versión de la aplicación"""
        try:
            if self.app and hasattr(self.app, 'version'):
                return self.app.version
            return "1.0.0"
        except:
            return "1.0.0"

    def get_user_info(self) -> Dict[str, Any]:
        """Obtiene información del usuario actual"""
        try:
            if self.app and hasattr(self.app, 'current_user'):
                return self.app.current_user
            return {
                'name': 'Usuario Invitado',
                'role': 'viewer',
                'permissions': ['view', 'export']
            }
        except:
            return {
                'name': 'Usuario Invitado',
                'role': 'viewer',
                'permissions': ['view', 'export']
            }

    def log_user_action(self, action: str, details: str = ""):
        """Registra una acción del usuario"""
        try:
            user_info = self.get_user_info()
            self.logger.info(f"Acción de usuario: {user_info.get('name', 'Desconocido')} - {action} - {details}")
        except Exception as e:
            self.logger.error(f"Error registrando acción de usuario: {e}")

    def cleanup(self):
        """Limpia recursos al cerrar la pantalla"""
        try:
            self.logger.info("Limpiando recursos de LVentasMainScreen")
            
            # Limpiar pestañas
            for tab in self.tabs:
                try:
                    if hasattr(tab['instance'], 'cleanup'):
                        tab['instance'].cleanup()
                except Exception as e:
                    self.logger.error(f"Error limpiando pestaña {tab['key']}: {e}")
            
            # Limpiar datos compartidos
            self.tabs_data.clear()
            
            self.logger.info("Recursos limpiados correctamente")
            
        except Exception as e:
            self.logger.error(f"Error en cleanup: {e}")

    def _refresh_current_tab_content_only(self):
        """Refresca solo el contenido de la pestaña actual"""
        try:
            if 0 <= self.selected_tab < len(self.tabs):
                active_tab = self.tabs[self.selected_tab]
                tab_instance = active_tab['instance']
                
                # Si la pestaña tiene un método de refresh específico, usarlo
                if hasattr(tab_instance, 'refresh_content'):
                    tab_instance.refresh_content()
                else:
                    # Fallback: reconstruir solo el contenido de la pestaña
                    self._build_tab_content()
                
                if self.page:
                    self.page.update()
                    
        except Exception as e:
            self.logger.error(f"Error refrescando contenido de pestaña: {e}")
            # Fallback: refresh completo
            self._refresh_page()

    def __del__(self):
        """Destructor de la clase"""
        try:
            self.cleanup()
        except:
            pass

