"""
Clase base para todas las pestañas - VERSIÓN CORREGIDA
"""

import flet as ft
from datetime import datetime
from core.logger import get_logger

class BaseTab:
    """Clase base para todas las pestañas"""
    
    def __init__(self, main_screen):
        self.main_screen = main_screen
        self.page = main_screen.page
        self.theme = main_screen.theme
        self.logger = get_logger(self.__class__.__name__)
        
        # Variables de período independientes para cada pestaña
        current_date = datetime.now()
        self.selected_year = current_date.year
        self.selected_month = current_date.month
        
        # Inicializar referencias a controles como None
        self.month_dropdown = None
        self.year_dropdown = None
        self.period_callback = None
        self.period_container = None
        
        # Flag para evitar loops infinitos en actualizaciones
        self._updating_period = False
    
    def build(self) -> ft.Control:
        """Método abstracto para construir la pestaña"""
        raise NotImplementedError("Subclases deben implementar build()")
    
    def build_period_selector(self, on_change_callback=None) -> ft.Control:
        """Construye selector de período para la pestaña"""
        try:
            self.period_callback = on_change_callback
            
            meses = [
                "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
            ]
            
            # Crear dropdowns y asignarlos a las variables de instancia
            self.month_dropdown = ft.Dropdown(
                value=str(self.selected_month),
                options=[
                    ft.dropdown.Option(str(i+1), mes) 
                    for i, mes in enumerate(meses)
                ],
                on_change=self._on_month_change,
                width=120,
                text_size=13,
                bgcolor=self.theme['white'],
                border_color=self.theme['border'],
                border_radius=8,
                content_padding=ft.padding.symmetric(horizontal=12, vertical=8)
            )
            
            self.year_dropdown = ft.Dropdown(
                value=str(self.selected_year),
                options=[
                    ft.dropdown.Option(str(year), str(year))
                    for year in range(2023, 2027)
                ],
                on_change=self._on_year_change,
                width=80,
                text_size=13,
                bgcolor=self.theme['white'],
                border_color=self.theme['border'],
                border_radius=8,
                content_padding=ft.padding.symmetric(horizontal=12, vertical=8)
            )
            
            # Crear el contenedor del selector de período
            self.period_container = ft.Container(
                content=ft.Row([
                    ft.Icon(
                        ft.Icons.CALENDAR_TODAY,
                        size=18,
                        color=self.theme['secondary']
                    ),
                    ft.Container(width=8),
                    ft.Text(
                        "Período:",
                        size=14,
                        weight=ft.FontWeight.W_500,
                        color=self.theme['text_secondary']
                    ),
                    ft.Container(width=12),
                    
                    # Selector de mes
                    ft.Container(
                        content=self.month_dropdown,
                        height=40,
                        alignment=ft.alignment.center
                    ),
                    
                    ft.Container(width=8),
                    
                    # Selector de año
                    ft.Container(
                        content=self.year_dropdown,
                        height=40,
                        alignment=ft.alignment.center
                    ),
                    
                    ft.Container(width=12),
                    
                    # Botón actualizar
                    ft.ElevatedButton(
                        content=ft.Row([
                            ft.Icon(ft.Icons.REFRESH, size=16),
                            ft.Text("Actualizar", size=12)
                        ], spacing=6),
                        on_click=self._on_refresh_data,
                        bgcolor=self.theme['primary'],
                        color=self.theme['white'],
                        height=40,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=8)
                        )
                    )
                ], spacing=0),
                padding=ft.padding.symmetric(horizontal=16, vertical=8),
                bgcolor=f"{self.theme['secondary']}05",
                border_radius=12,
                border=ft.border.all(1, self.theme['border'])
            )
            
            self.logger.info(f"Selector de período creado para {self.__class__.__name__}")
            return self.period_container
            
        except Exception as e:
            self.logger.error(f"Error creando selector de período: {e}")
            return ft.Container(
                content=ft.Text(f"Error creando selector: {e}", color=self.theme['danger']),
                padding=20
            )
    
    def _on_month_change(self, e):
        """Maneja el cambio de mes"""
        if self._updating_period:
            return
            
        try:
            old_month = self.selected_month
            new_month = int(e.control.value)
            
            self.logger.info(f"Mes cambiado de {old_month} a {new_month}")
            
            self.selected_month = new_month
            
            # Actualizar automáticamente los datos
            self._auto_refresh_data()
            
        except Exception as ex:
            self.logger.error(f"Error al cambiar mes: {ex}")
            if hasattr(self.main_screen, 'show_error_message'):
                self.main_screen.show_error_message(f"Error al cambiar mes: {ex}")
    
    def _on_year_change(self, e):
        """Maneja el cambio de año"""
        if self._updating_period:
            return
            
        try:
            old_year = self.selected_year
            new_year = int(e.control.value)
            
            self.logger.info(f"Año cambiado de {old_year} a {new_year}")
            
            self.selected_year = new_year
            
            # Actualizar automáticamente los datos
            self._auto_refresh_data()
            
        except Exception as ex:
            self.logger.error(f"Error al cambiar año: {ex}")
            if hasattr(self.main_screen, 'show_error_message'):
                self.main_screen.show_error_message(f"Error al cambiar año: {ex}")
    
    def _auto_refresh_data(self):
        """Actualiza datos automáticamente al cambiar período"""
        try:
            self.logger.info(f"Auto-actualizando datos para período {self.selected_month}/{self.selected_year}")
            
            # Mostrar mensaje de carga
            if hasattr(self.main_screen, 'show_loading_message'):
                self.main_screen.show_loading_message("Actualizando datos...")
            
            # Llamar al callback específico de la pestaña si existe
            if self.period_callback:
                self.period_callback()
            else:
                # Fallback: refrescar la pestaña actual
                self._refresh_current_tab_only()
                
        except Exception as ex:
            self.logger.error(f"Error en auto-actualización: {ex}")
            if hasattr(self.main_screen, 'show_error_message'):
                self.main_screen.show_error_message("Error al actualizar datos automáticamente")
    
    def _on_refresh_data(self, e=None):
        """Maneja la actualización manual de datos"""
        try:
            self.logger.info(f"Actualización manual solicitada para período {self.selected_month}/{self.selected_year}")
            
            if hasattr(self.main_screen, 'show_loading_message'):
                self.main_screen.show_loading_message("Actualizando datos...")
            
            # Actualizar solo el contenido de la pestaña actual
            self._refresh_current_tab_only()
            
            if hasattr(self.main_screen, 'show_success_message'):
                self.main_screen.show_success_message("Datos actualizados correctamente")
            
        except Exception as ex:
            self.logger.error(f"Error al actualizar datos: {ex}")
            if hasattr(self.main_screen, 'show_error_message'):
                self.main_screen.show_error_message("Error al actualizar datos")
    
    def _refresh_current_tab_only(self):
        """Refresca solo la pestaña actual sin reconstruir toda la página"""
        try:
            # Por ahora, usar el método de refresh de la pantalla principal
            # Esto se puede optimizar más adelante
            if hasattr(self.main_screen, '_refresh_page'):
                self.main_screen._refresh_page()
            else:
                self.logger.warning("No se pudo refrescar: método _refresh_page no disponible")
                
        except Exception as ex:
            self.logger.error(f"Error refrescando pestaña: {ex}")
    
    def update_period_display(self):
        """Actualiza la visualización de los selectores de período"""
        try:
            self._updating_period = True
            
            if self.month_dropdown is not None:
                self.month_dropdown.value = str(self.selected_month)
                self.logger.debug(f"Month dropdown actualizado a: {self.selected_month}")
            else:
                self.logger.warning("month_dropdown es None, no se puede actualizar")
            
            if self.year_dropdown is not None:
                self.year_dropdown.value = str(self.selected_year)
                self.logger.debug(f"Year dropdown actualizado a: {self.selected_year}")
            else:
                self.logger.warning("year_dropdown es None, no se puede actualizar")
            
            # Actualizar la página si es necesario
            if hasattr(self, 'page') and self.page:
                self.page.update()
                
            self._updating_period = False
                
        except Exception as ex:
            self._updating_period = False
            self.logger.error(f"Error actualizando visualización de período: {ex}")
    
    def set_period(self, year: int, month: int, update_display: bool = True):
        """Establece el período programáticamente"""
        try:
            self.selected_year = year
            self.selected_month = month
            
            if update_display:
                self.update_period_display()
                
            self.logger.info(f"Período establecido a {month}/{year}")
            
        except Exception as ex:
            self.logger.error(f"Error estableciendo período: {ex}")
    
    def get_period_text(self) -> str:
        """Obtiene texto del período actual"""
        meses = [
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ]
        try:
            return f"{meses[self.selected_month - 1]} {self.selected_year}"
        except IndexError:
            return f"Mes {self.selected_month} {self.selected_year}"
    
    def get_data_from_db(self, query: str, params: tuple) -> list:
        """Obtiene datos de la base de datos"""
        try:
            from core.database import get_db_manager
            db_manager = get_db_manager()
            results = db_manager.execute_query(query, params)
            return results if results else []
        except Exception as e:
            self.logger.error(f"Error obteniendo datos: {e}")
            return []
    
    def on_tab_activated(self):
        """Llamado cuando la pestaña se activa"""
        try:
            self.logger.info(f"Pestaña {self.__class__.__name__} activada")
            # Actualizar la visualización del período
            self.update_period_display()
        except Exception as ex:
            self.logger.error(f"Error en activación de pestaña: {ex}")
    
    def on_tab_deactivated(self):
        """Llamado cuando la pestaña se desactiva"""
        try:
            self.logger.info(f"Pestaña {self.__class__.__name__} desactivada")
        except Exception as ex:
            self.logger.error(f"Error en desactivación de pestaña: {ex}")
    
    def refresh(self):
        """Método para refrescar la pestaña"""
        try:
            self.logger.info(f"Refrescando pestaña {self.__class__.__name__}")
            self._refresh_current_tab_only()
        except Exception as ex:
            self.logger.error(f"Error en refresh: {ex}")
    
    def cleanup(self):
        """Limpia recursos de la pestaña"""
        try:
            self.month_dropdown = None
            self.year_dropdown = None
            self.period_callback = None
            self.period_container = None
            self.logger.info(f"Recursos de {self.__class__.__name__} limpiados")
        except Exception as ex:
            self.logger.error(f"Error en cleanup: {ex}")
    
    def validate_dropdowns(self):
        """Valida que los dropdowns estén correctamente inicializados"""
        issues = []
        
        if self.month_dropdown is None:
            issues.append("month_dropdown es None")
        
        if self.year_dropdown is None:
            issues.append("year_dropdown es None")
            
        if issues:
            self.logger.warning(f"Problemas con dropdowns en {self.__class__.__name__}: {issues}")
            return False
        
        return True
