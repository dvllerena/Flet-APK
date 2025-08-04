"""
Pantalla de visualización de registros de energía
"""

import flet as ft
from typing import Dict, Any, Optional, Callable
from datetime import datetime

from calculo_energia.services.energia_service import EnergiaService
from calculo_energia.models.energia_barra_model import EnergiaBarra
from core.logger import get_logger


class EnergiaViewScreen:
    """Pantalla para visualizar registros de energía"""
    
    def __init__(self, app, params: Dict[str, Any] = None):
        self.app = app
        self.page = app.page
        self.logger = get_logger(__name__)
        self.energia_service = EnergiaService()
        
        # Parámetros
        self.params = params or {}
        self.registro_id = self.params.get('registro_id')
        self.callback = self.params.get('callback')
        
        # Estado
        self.current_registro: Optional[EnergiaBarra] = None
        self.is_loading = False
        
        # Controles de interfaz
        self.loading_indicator = None
        self.content_container = None
        
        # Cargar datos
        self._load_data()
    
    def _load_data(self):
        """Carga los datos del registro"""
        try:
            if self.registro_id:
                self.current_registro = self.energia_service.get_energia_by_id(self.registro_id)
                if not self.current_registro:
                    self.logger.error(f"Registro no encontrado: {self.registro_id}")
            
            self.logger.info(f"Datos cargados para visualización: ID {self.registro_id}")
            
        except Exception as e:
            self.logger.error(f"Error cargando datos: {e}")
    
    def build(self) -> ft.Container:
        """Construye la interfaz de visualización"""
        
        # Header
        header = self._build_header()
        
        # Indicador de carga
        self.loading_indicator = ft.Container(
            content=ft.Column([
                ft.ProgressRing(width=40, height=40, color=ft.Colors.BLUE_500),
                ft.Text("Cargando...", size=14, color=ft.Colors.BLUE_600)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            alignment=ft.alignment.center,
            visible=False,
            padding=20
        )
        
        # Contenido principal
        if self.current_registro:
            content = self._build_content()
        else:
            content = self._build_error_content()
        
        self.content_container = ft.Container(
            content=content,
            expand=True
        )
        
        # Layout principal
        main_content = ft.Column([
            header,
            ft.Container(height=20),
            self.content_container,
            self.loading_indicator
        ], 
        scroll=ft.ScrollMode.AUTO,
        expand=True
        )
        
        return ft.Container(
            content=main_content,
            padding=20,
            expand=True,
            bgcolor=ft.Colors.GREY_50
        )
    
    def _build_header(self) -> ft.Container:
        """Construye el header"""
        return ft.Container(
            content=ft.Row([
                ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    tooltip="Volver",
                    on_click=self._on_back_click,
                    icon_color=ft.Colors.BLUE_600
                ),
                ft.Icon(ft.Icons.VISIBILITY, size=32, color=ft.Colors.BLUE_600),
                ft.Text(
                    "Visualizar Registro de Energía",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE_800
                ),
                ft.Container(expand=True),
                ft.Chip(
                    label=ft.Text("SOLO LECTURA", size=12, weight=ft.FontWeight.BOLD),
                    bgcolor=ft.Colors.GREY_200,
                    color=ft.Colors.GREY_700
                )
            ], alignment=ft.MainAxisAlignment.START, spacing=15),
            padding=ft.padding.symmetric(horizontal=20, vertical=15),
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            border=ft.border.all(1, ft.Colors.BLUE_100)
        )
    
    def _build_content(self) -> ft.Column:
        """Construye el contenido principal"""
        
        # Información básica
        info_card = self._build_info_card()
        
        # Detalles del registro
        details_card = self._build_details_card()
        
        # Estadísticas
        stats_card = self._build_stats_card()
        
        # Acciones
        actions_card = self._build_actions_card()
        
        return ft.Column([
            info_card,
            ft.Container(height=20),
            details_card,
            ft.Container(height=20),
            stats_card,
            ft.Container(height=20),
            actions_card
        ])
    
    def _build_info_card(self) -> ft.Container:
        """Construye la tarjeta de información básica"""
        
        # Formatear fecha de registro
        fecha_registro = "No disponible"
        if self.current_registro.fecha_registro:
            try:
                fecha_dt = datetime.fromisoformat(self.current_registro.fecha_registro.replace('Z', '+00:00'))
                fecha_registro = fecha_dt.strftime("%d/%m/%Y a las %H:%M")
            except:
                fecha_registro = str(self.current_registro.fecha_registro)[:19]
        
        # Formatear fecha de modificación
        fecha_modificacion = "No disponible"
        if self.current_registro.fecha_modificacion:
            try:
                fecha_dt = datetime.fromisoformat(self.current_registro.fecha_modificacion.replace('Z', '+00:00'))
                fecha_modificacion = fecha_dt.strftime("%d/%m/%Y a las %H:%M")
            except:
                fecha_modificacion = str(self.current_registro.fecha_modificacion)[:19]
        
        content = ft.Column([
            ft.Text(
                "Información General",
                size=18,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLUE_800
            ),
            ft.Container(height=15),
            
            # Fila 1: Municipio y Período
            ft.Row([
                ft.Container(
                    content=ft.Column([
                        ft.Text("Municipio", size=12, color=ft.Colors.GREY_600, weight=ft.FontWeight.W_500),
                        ft.Text(
                            f"{self.current_registro.municipio_nombre} ({self.current_registro.municipio_codigo})",
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.BLUE_800
                        )
                    ], spacing=5),
                    width=300
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Text("Período", size=12, color=ft.Colors.GREY_600, weight=ft.FontWeight.W_500),
                        ft.Text(
                            self.current_registro.periodo_texto,
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.BLUE_800
                        )
                    ], spacing=5),
                    width=200
                )
            ]),
            
            ft.Container(height=20),
            
            # Fila 2: Energía
            ft.Row([
                ft.Container(
                    content=ft.Column([
                        ft.Text("Energía Consumida", size=12, color=ft.Colors.GREY_600, weight=ft.FontWeight.W_500),
                        ft.Row([
                            ft.Text(
                                f"{self.current_registro.energia_mwh:.1f}",
                                size=24,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.GREEN_600
                            ),
                            ft.Text(
                                "MWh",
                                size=16,
                                weight=ft.FontWeight.W_500,
                                color=ft.Colors.GREEN_600
                            )
                        ], spacing=5)
                    ], spacing=5),
                    width=300
                )
            ]),
            
            ft.Container(height=20),
            
            # Fila 3: Fechas
            ft.Row([
                ft.Container(
                    content=ft.Column([
                        ft.Text("Fecha de Registro", size=12, color=ft.Colors.GREY_600, weight=ft.FontWeight.W_500),
                        ft.Text(
                            fecha_registro,
                            size=14,
                            color=ft.Colors.GREY_800
                        )
                    ], spacing=5),
                    width=250
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Text("Última Modificación", size=12, color=ft.Colors.GREY_600, weight=ft.FontWeight.W_500),
                        ft.Text(
                            fecha_modificacion,
                            size=14,
                            color=ft.Colors.GREY_800
                        )
                    ], spacing=5),
                    width=250
                )
            ])
        ])
        
        return ft.Container(
            content=content,
            padding=30,
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            border=ft.border.all(1, ft.Colors.BLUE_100)
        )
    
    def _build_details_card(self) -> ft.Container:
        """Construye la tarjeta de detalles"""
        
        content = ft.Column([
            ft.Text(
                "Detalles del Registro",
                size=18,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLUE_800
            ),
            ft.Container(height=15),
            
            # ID del registro
            ft.Row([
                ft.Icon(ft.Icons.TAG, size=16, color=ft.Colors.GREY_600),
                ft.Text("ID del Registro:", size=14, color=ft.Colors.GREY_600, weight=ft.FontWeight.W_500),
                ft.Text(str(self.current_registro.id), size=14, weight=ft.FontWeight.BOLD)
            ], spacing=8),
            
            ft.Container(height=10),
            
            # ID del municipio
            ft.Row([
                ft.Icon(ft.Icons.LOCATION_CITY, size=16, color=ft.Colors.GREY_600),
                ft.Text("ID del Municipio:", size=14, color=ft.Colors.GREY_600, weight=ft.FontWeight.W_500),
                ft.Text(str(self.current_registro.municipio_id), size=14, weight=ft.FontWeight.BOLD)
            ], spacing=8),
            
            ft.Container(height=10),
            
            # Usuario
            ft.Row([
                ft.Icon(ft.Icons.PERSON, size=16, color=ft.Colors.GREY_600),
                ft.Text("Usuario:", size=14, color=ft.Colors.GREY_600, weight=ft.FontWeight.W_500),
                ft.Text(
                    str(self.current_registro.usuario_id) if self.current_registro.usuario_id else "No disponible",
                    size=14,
                    weight=ft.FontWeight.BOLD
                )
            ], spacing=8),
            
            ft.Container(height=15),
            
            # Observaciones
            ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.NOTES, size=16, color=ft.Colors.GREY_600),
                    ft.Text("Observaciones:", size=14, color=ft.Colors.GREY_600, weight=ft.FontWeight.W_500)
                ], spacing=8),
                ft.Container(height=5),
                ft.Container(
                    content=ft.Text(
                        self.current_registro.observaciones or "Sin observaciones",
                        size=14,
                        color=ft.Colors.GREY_800 if self.current_registro.observaciones else ft.Colors.GREY_500,
                        selectable=True
                    ),
                    padding=15,
                    bgcolor=ft.Colors.GREY_50,
                    border_radius=8,
                    border=ft.border.all(1, ft.Colors.GREY_200),
                    width=500
                )
            ])
        ])
        
        return ft.Container(
            content=content,
            padding=30,
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            border=ft.border.all(1, ft.Colors.BLUE_100)
        )
    
    def _build_stats_card(self) -> ft.Container:
        """Construye la tarjeta de estadísticas"""
        
        # Obtener estadísticas del período
        resumen = self.energia_service.get_resumen_periodo(
            self.current_registro.año, 
            self.current_registro.mes
        )
        
        total_provincia = resumen.get('total_energia', 0)
        porcentaje = (self.current_registro.energia_mwh / total_provincia * 100) if total_provincia > 0 else 0
        
        content = ft.Column([
            ft.Text(
                "Estadísticas del Período",
                size=18,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLUE_800
            ),
            ft.Container(height=15),
            
            ft.Row([
                # Porcentaje del total
                ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.Icons.PIE_CHART, size=24, color=ft.Colors.PURPLE_600),
                        ft.Text(f"{porcentaje:.1f}%", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.PURPLE_600),
                        ft.Text("del total provincial", size=12, color=ft.Colors.GREY_600, text_align=ft.TextAlign.CENTER)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
                    width=150,
                    padding=15,
                    bgcolor=ft.Colors.PURPLE_50,
                    border_radius=8,
                    border=ft.border.all(1, ft.Colors.PURPLE_200)
                ),
                
                ft.Container(width=20),
                
                # Total provincial
                ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.Icons.ELECTRIC_BOLT, size=24, color=ft.Colors.ORANGE_600),
                        ft.Text(f"{total_provincia:.1f}", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.ORANGE_600),
                        ft.Text("MWh total provincial", size=12, color=ft.Colors.GREY_600, text_align=ft.TextAlign.CENTER)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
                    width=150,
                    padding=15,
                    bgcolor=ft.Colors.ORANGE_50,
                    border_radius=8,
                    border=ft.border.all(1, ft.Colors.ORANGE_200)
                ),
                
                ft.Container(width=20),
                
                # Ranking
                ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.Icons.LEADERBOARD, size=24, color=ft.Colors.BLUE_600),
                        ft.Text("N/A", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_600),
                        ft.Text("posición ranking", size=12, color=ft.Colors.GREY_600, text_align=ft.TextAlign.CENTER)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
                    width=150,
                    padding=15,
                    bgcolor=ft.Colors.BLUE_50,
                    border_radius=8,
                    border=ft.border.all(1, ft.Colors.BLUE_200)
                )
            ], alignment=ft.MainAxisAlignment.START)
        ])
        
        return ft.Container(
            content=content,
            padding=30,
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            border=ft.border.all(1, ft.Colors.BLUE_100)
        )
    
    def _build_actions_card(self) -> ft.Container:
        """Construye la tarjeta de acciones"""
        
        content = ft.Column([
            ft.Text(
                "Acciones Disponibles",
                size=18,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLUE_800
            ),
            ft.Container(height=15),
            
            ft.Row([
                # Botón editar
                ft.ElevatedButton(
                    content=ft.Row([
                        ft.Icon(ft.Icons.EDIT, size=18),
                        ft.Text("Editar Registro")
                    ], spacing=8),
                    on_click=self._on_edit_click,
                    bgcolor=ft.Colors.ORANGE_600,
                    color=ft.Colors.WHITE,
                    width=180
                ),
                
                ft.Container(width=15),
                
                # Botón eliminar
                ft.ElevatedButton(
                    content=ft.Row([
                        ft.Icon(ft.Icons.DELETE, size=18),
                        ft.Text("Eliminar Registro")
                    ], spacing=8),
                    on_click=self._on_delete_click,
                    bgcolor=ft.Colors.RED_600,
                    color=ft.Colors.WHITE,
                    width=180
                ),
                
                ft.Container(width=15),
                
                # Botón exportar
                ft.ElevatedButton(
                    content=ft.Row([
                        ft.Icon(ft.Icons.DOWNLOAD, size=18),
                        ft.Text("Exportar Datos")
                    ], spacing=8),
                    on_click=self._on_export_click,
                    bgcolor=ft.Colors.GREEN_600,
                    color=ft.Colors.WHITE,
                    width=180
                )
            ], alignment=ft.MainAxisAlignment.START),
            
            ft.Container(height=15),
            
            # Información adicional
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.INFO_OUTLINE, size=16, color=ft.Colors.BLUE_500),
                    ft.Text(
                        "Use las acciones para modificar, eliminar o exportar este registro",
                        size=12,
                        color=ft.Colors.BLUE_600
                    )
                ], spacing=8),
                padding=15,
                bgcolor=ft.Colors.BLUE_50,
                border_radius=8,
                border=ft.border.all(1, ft.Colors.BLUE_200)
            )
        ])
        
        return ft.Container(
            content=content,
            padding=30,
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            border=ft.border.all(1, ft.Colors.BLUE_100)
        )
    
    def _build_error_content(self) -> ft.Container:
        """Construye el contenido de error cuando no se encuentra el registro"""
        
        return ft.Container(
            content=ft.Column([
                ft.Icon(
                    ft.Icons.ERROR_OUTLINE,
                    size=64,
                    color=ft.Colors.RED_400
                ),
                ft.Container(height=20),
                ft.Text(
                    "Registro no encontrado",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.RED_600,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Container(height=10),
                ft.Text(
                    f"No se pudo encontrar el registro con ID: {self.registro_id}",
                    size=16,
                    color=ft.Colors.GREY_600,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Container(height=30),
                ft.ElevatedButton(
                    content=ft.Row([
                        ft.Icon(ft.Icons.ARROW_BACK, size=18),
                        ft.Text("Volver al Listado")
                    ], spacing=8),
                    on_click=self._on_back_click,
                    bgcolor=ft.Colors.BLUE_600,
                    color=ft.Colors.WHITE
                )
            ], 
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER
            ),
            alignment=ft.alignment.center,
            expand=True,
            padding=50
        )
    
    def _on_edit_click(self, e):
        """Maneja el clic del botón editar"""
        try:
            if self.current_registro:
                self.app.navigate_to("energia_edit", {
                    'mode': 'edit',
                    'registro_id': self.current_registro.id,
                    'callback': self.callback
                })
        except Exception as ex:
            self.logger.error(f"Error navegando a editar: {ex}")
            self._show_error("Error navegando a edición")
    
    def _on_delete_click(self, e):
        """Maneja el clic del botón eliminar"""
        try:
            if not self.current_registro:
                return
            
            # Mostrar diálogo de confirmación
            def confirm_delete(e):
                try:
                    if self.energia_service.eliminar_energia(self.current_registro.id):
                        self._show_success(f"Registro de {self.current_registro.municipio_nombre} eliminado")
                        
                        # Llamar callback si existe
                        if self.callback:
                            self.callback()
                        
                        # Volver a la pantalla anterior
                        self._navigate_back()
                    else:
                        self._show_error("Error eliminando registro")
                except Exception as ex:
                    self.logger.error(f"Error eliminando: {ex}")
                    self._show_error("Error del sistema")
                finally:
                    dialog.open = False
                    self.page.update()
            
            def cancel_delete(e):
                dialog.open = False
                self.page.update()
            
            dialog = ft.AlertDialog(
                modal=True,
                title=ft.Text("Confirmar eliminación"),
                content=ft.Column([
                    ft.Text(f"¿Está seguro de eliminar el registro de {self.current_registro.municipio_nombre}?"),
                    ft.Container(height=10),
                    ft.Text(f"Período: {self.current_registro.periodo_texto}", size=12, color=ft.Colors.GREY_600),
                    ft.Text(f"Energía: {self.current_registro.energia_mwh:.1f} MWh", size=12, color=ft.Colors.GREY_600),
                    ft.Container(height=10),
                    ft.Container(
                        content=ft.Text(
                            "⚠️ Esta acción no se puede deshacer",
                            size=12,
                            color=ft.Colors.RED_600,
                            weight=ft.FontWeight.BOLD
                        ),
                        padding=10,
                        bgcolor=ft.Colors.RED_50,
                        border_radius=5,
                        border=ft.border.all(1, ft.Colors.RED_200)
                    )
                ], tight=True),
                actions=[
                    ft.TextButton("Cancelar", on_click=cancel_delete),
                    ft.TextButton(
                        "Eliminar", 
                        on_click=confirm_delete, 
                        style=ft.ButtonStyle(color=ft.Colors.RED_600)
                    )
                ]
            )
            
            self.page.dialog = dialog
            dialog.open = True
            self.page.update()
            
        except Exception as ex:
            self.logger.error(f"Error en eliminación: {ex}")
            self._show_error("Error preparando eliminación")
    
    def _on_export_click(self, e):
        """Maneja el clic del botón exportar"""
        try:
            if not self.current_registro:
                return
            
            # Crear diálogo de selección de ubicación
            def on_save_location(e: ft.FilePickerResultEvent):
                if e.path:
                    self._export_registro(e.path)
            
            file_picker = ft.FilePicker(on_result=on_save_location)
            self.page.overlay.append(file_picker)
            self.page.update()
            
            # Nombre sugerido
            suggested_name = f"energia_{self.current_registro.municipio_codigo}_{self.current_registro.año}_{self.current_registro.mes:02d}.xlsx"
            
            file_picker.save_file(
                dialog_title="Exportar registro",
                file_name=suggested_name,
                file_type=ft.FilePickerFileType.CUSTOM,
                allowed_extensions=["xlsx"]
            )
            
        except Exception as ex:
            self.logger.error(f"Error en exportación: {ex}")
            self._show_error("Error iniciando exportación")
    
    def _export_registro(self, file_path: str):
        """Exporta el registro actual"""
        try:
            self._set_loading(True)
            
            # Exportar solo este registro
            if self.energia_service.exportar_registro_individual(self.current_registro, file_path):
                self._show_success("Registro exportado exitosamente")
            else:
                self._show_error("Error exportando registro")
                
        except Exception as ex:
            self.logger.error(f"Error exportando registro: {ex}")
            self._show_error("Error guardando archivo")
        finally:
            self._set_loading(False)
    
    def _on_back_click(self, e):
        """Maneja el clic del botón volver"""
        self._navigate_back()
    
    def _navigate_back(self):
        """Navega de vuelta - CORREGIDO"""
        try:
            # ✅ USAR NOMBRE CORRECTO
            self.app.navigate_to("calculo_energia")
        except Exception as e:
            self.logger.error(f"Error navegando de vuelta: {e}")
    def _set_loading(self, loading: bool):
        """Controla el estado de carga"""
        self.is_loading = loading
        self.loading_indicator.visible = loading
        self.content_container.visible = not loading
        self.page.update()
    
    def _show_success(self, message: str):
        """Muestra mensaje de éxito"""
        try:
            snack_bar = ft.SnackBar(
                content=ft.Row([
                    ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.WHITE),
                    ft.Text(message, color=ft.Colors.WHITE)
                ]),
                bgcolor=ft.Colors.GREEN_600
            )
            self.page.snack_bar = snack_bar
            snack_bar.open = True
            self.page.update()
        except Exception as e:
            self.logger.error(f"Error mostrando mensaje de éxito: {e}")
    
    def _show_error(self, message: str):
        """Muestra mensaje de error"""
        try:
            snack_bar = ft.SnackBar(
                content=ft.Row([
                    ft.Icon(ft.Icons.ERROR, color=ft.Colors.WHITE),
                    ft.Text(message, color=ft.Colors.WHITE)
                ]),
                bgcolor=ft.Colors.RED_600
            )
            self.page.snack_bar = snack_bar
            snack_bar.open = True
            self.page.update()
        except Exception as e:
            self.logger.error(f"Error mostrando mensaje de error: {e}")
    
    def refresh_data(self):
        """Refresca los datos del registro"""
        try:
            self._load_data()
            if self.current_registro:
                # Reconstruir contenido
                new_content = self._build_content()
                self.content_container.content = new_content
                self.page.update()
        except Exception as e:
            self.logger.error(f"Error refrescando datos: {e}")
