"""
Pantalla de edición de facturación
"""

import flet as ft
from datetime import datetime
from typing import Optional, List, Dict, Any
from facturacion.services import get_facturacion_service
from facturacion.models import FacturacionModel
from core.logger import get_logger

class FacturacionEditScreen:
    """Pantalla de edición de facturación"""
    
    def __init__(self, app, facturacion: Optional[FacturacionModel] = None, 
                 año: Optional[int] = None, mes: Optional[int] = None):
        self.app = app
        self.page = app.page
        self.logger = get_logger(__name__)
        self.facturacion_service = get_facturacion_service()
        
        # Estado
        self.facturacion = facturacion
        self.is_edit_mode = facturacion is not None
        self.municipios: List[Dict[str, Any]] = []
        
        # Valores por defecto para nueva facturación
        if not self.is_edit_mode:
            self.facturacion = FacturacionModel(
                año=año or datetime.now().year,
                mes=mes or datetime.now().month
            )
        
        # Controles
        self.municipio_dropdown = None
        self.año_field = None
        self.mes_dropdown = None
        self.facturacion_menor_field = None
        self.facturacion_mayor_field = None
        self.facturacion_total_field = None
        
    def build(self) -> ft.Control:
        """Construye la interfaz"""
        return ft.Container(
            content=ft.Column([
                self._build_header(),
                self._build_form(),
                self._build_actions()
            ], spacing=25),
            padding=25,
            expand=True,
            bgcolor=ft.Colors.GREY_50
        )
    
    def _build_header(self) -> ft.Control:
        """Construye el encabezado"""
        title = "Editar Facturación" if self.is_edit_mode else "Nueva Facturación"
        subtitle = "Modificar datos existentes" if self.is_edit_mode else "Crear nuevo registro de facturación"
        
        return ft.Card(
            content=ft.Container(
                content=ft.Row([
                    ft.Container(
                        content=ft.IconButton(
                            icon=ft.Icons.ARROW_BACK,
                            on_click=lambda _: self.app.navigate_to("facturacion"),
                            tooltip="Volver a Facturación",
                            icon_color=ft.Colors.WHITE,
                            bgcolor=ft.Colors.BLUE_600,
                            style=ft.ButtonStyle(shape=ft.CircleBorder())
                        ),
                        margin=ft.margin.only(right=15)
                    ),
                    ft.Column([
                        ft.Text(
                            title,
                            size=28,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.BLUE_800
                        ),
                        ft.Text(
                            subtitle,
                            size=16,
                            color=ft.Colors.BLUE_600
                        )
                    ], expand=True),
                    ft.Container(
                        content=ft.Icon(
                            ft.Icons.EDIT if self.is_edit_mode else ft.Icons.ADD_CIRCLE,
                            size=48,
                            color=ft.Colors.BLUE_600
                        ),
                        padding=10,
                        bgcolor=ft.Colors.BLUE_50,
                        border_radius=25
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                padding=25,
            ),
            elevation=3,
            margin=ft.margin.only(bottom=10)
        )
    
    def _build_form(self) -> ft.Control:
        """Construye el formulario"""
        # Cargar municipios
        self.municipios = self.facturacion_service.get_municipios_activos()
        
        # Dropdown de municipios
        self.municipio_dropdown = ft.Dropdown(
            label="Municipio",
            hint_text="Seleccione un municipio",
            options=[
                ft.dropdown.Option(str(m['id']), m['nombre']) 
                for m in self.municipios
            ],
            value=str(self.facturacion.municipio_id) if self.facturacion.municipio_id else None,
            width=350,
            bgcolor=ft.Colors.WHITE,
            border_color=ft.Colors.BLUE_300,
            focused_border_color=ft.Colors.BLUE_600,
            text_style=ft.TextStyle(size=16)
        )
        
        # Campo año
        self.año_field = ft.TextField(
            label="Año",
            hint_text="Ej: 2024",
            value=str(self.facturacion.año),
            width=150,
            keyboard_type=ft.KeyboardType.NUMBER,
            bgcolor=ft.Colors.WHITE,
            border_color=ft.Colors.BLUE_300,
            focused_border_color=ft.Colors.BLUE_600,
            text_style=ft.TextStyle(size=16)
        )
        
        # Dropdown mes
        self.mes_dropdown = ft.Dropdown(
            label="Mes",
            hint_text="Seleccione mes",
            width=200,
            value=str(self.facturacion.mes),
            bgcolor=ft.Colors.WHITE,
            border_color=ft.Colors.BLUE_300,
            focused_border_color=ft.Colors.BLUE_600,
            text_style=ft.TextStyle(size=16),
            options=[
                ft.dropdown.Option("1", "Enero"),
                ft.dropdown.Option("2", "Febrero"),
                ft.dropdown.Option("3", "Marzo"),
                ft.dropdown.Option("4", "Abril"),
                ft.dropdown.Option("5", "Mayo"),
                ft.dropdown.Option("6", "Junio"),
                ft.dropdown.Option("7", "Julio"),
                ft.dropdown.Option("8", "Agosto"),
                ft.dropdown.Option("9", "Septiembre"),
                ft.dropdown.Option("10", "Octubre"),
                ft.dropdown.Option("11", "Noviembre"),
                ft.dropdown.Option("12", "Diciembre"),
            ]
        )
        
        # Campo facturación menor
        self.facturacion_menor_field = ft.TextField(
            label="Facturación Menor",
            hint_text="Ingrese valor en kW",
            value=str(self.facturacion.facturacion_menor) if self.facturacion.facturacion_menor else "0",
            width=250,
            keyboard_type=ft.KeyboardType.NUMBER,
            suffix_text="kW",
            bgcolor=ft.Colors.WHITE,
            border_color=ft.Colors.GREEN_300,
            focused_border_color=ft.Colors.GREEN_600,
            text_style=ft.TextStyle(size=16),
            on_change=self._calculate_total
        )
        
        # Campo facturación mayor
        self.facturacion_mayor_field = ft.TextField(
            label="Facturación Mayor",
            hint_text="Ingrese valor en kW",
            value=str(self.facturacion.facturacion_mayor) if self.facturacion.facturacion_mayor else "0",
            width=250,
            keyboard_type=ft.KeyboardType.NUMBER,
            suffix_text="kW",
            bgcolor=ft.Colors.WHITE,
            border_color=ft.Colors.BLUE_300,
            focused_border_color=ft.Colors.BLUE_600,
            text_style=ft.TextStyle(size=16),
            on_change=self._calculate_total
        )
        
        # Campo facturación total (calculado automáticamente)
        self.facturacion_total_field = ft.TextField(
            label="Facturación Total",
            value=str(self.facturacion.facturacion_total) if self.facturacion.facturacion_total else "0",
            width=250,
            suffix_text="kW",
            read_only=True,
            bgcolor=ft.Colors.PURPLE_50,
            border_color=ft.Colors.PURPLE_300,
            text_style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.PURPLE_700)
        )
        
        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    # Título de sección
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.DESCRIPTION, color=ft.Colors.BLUE_600, size=24),
                            ft.Text("Datos de Facturación", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800)
                        ]),
                        margin=ft.margin.only(bottom=20)
                    ),
                    
                    # Sección: Ubicación y Período
                    ft.Container(
                        content=ft.Column([
                            ft.Text("📍 Ubicación y Período", size=16, weight=ft.FontWeight.W_600, color=ft.Colors.GREY_700),
                            ft.Container(height=10),
                            self.municipio_dropdown,
                            ft.Container(height=15),
                            ft.Row([
                                self.año_field,
                                self.mes_dropdown
                            ], spacing=20),
                        ]),
                        padding=20,
                        bgcolor=ft.Colors.BLUE_50,
                        border_radius=12,
                        margin=ft.margin.only(bottom=20)
                    ),
                    
                    # Sección: Valores de Facturación
                    ft.Container(
                        content=ft.Column([
                            ft.Text("⚡ Valores de Facturación", size=16, weight=ft.FontWeight.W_600, color=ft.Colors.GREY_700),
                            ft.Container(height=15),
                            
                            # Fila de campos de facturación
                            ft.Row([
                                ft.Container(
                                    content=ft.Column([
                                        ft.Container(
                                            content=ft.Row([
                                                ft.Icon(ft.Icons.TRENDING_DOWN, color=ft.Colors.GREEN_600, size=20),
                                                ft.Text("Menor", weight=ft.FontWeight.W_500, color=ft.Colors.GREEN_700)
                                            ]),
                                            margin=ft.margin.only(bottom=5)
                                        ),
                                        self.facturacion_menor_field
                                    ]),
                                    expand=True
                                ),
                                
                                ft.Container(
                                    content=ft.Column([
                                        ft.Container(
                                            content=ft.Row([
                                                ft.Icon(ft.Icons.TRENDING_UP, color=ft.Colors.BLUE_600, size=20),
                                                ft.Text("Mayor", weight=ft.FontWeight.W_500, color=ft.Colors.BLUE_700)
                                            ]),
                                            margin=ft.margin.only(bottom=5)
                                        ),
                                        self.facturacion_mayor_field
                                    ]),
                                    expand=True
                                ),
                                
                                ft.Container(
                                    content=ft.Column([
                                        ft.Container(
                                            content=ft.Row([
                                                ft.Icon(ft.Icons.CALCULATE, color=ft.Colors.PURPLE_600, size=20),
                                                ft.Text("Total", weight=ft.FontWeight.W_500, color=ft.Colors.PURPLE_700)
                                            ]),
                                            margin=ft.margin.only(bottom=5)
                                        ),
                                        self.facturacion_total_field
                                    ]),
                                    expand=True
                                )
                            ], spacing=20),
                            
                            # Nota informativa
                            ft.Container(
                                content=ft.Row([
                                    ft.Icon(ft.Icons.INFO_OUTLINE, color=ft.Colors.BLUE_600, size=16),
                                    ft.Text(
                                        "El total se calcula automáticamente sumando Menor + Mayor",
                                        size=12,
                                        color=ft.Colors.BLUE_600,
                                        italic=True
                                    )
                                ]),
                                margin=ft.margin.only(top=10),
                                padding=10,
                                bgcolor=ft.Colors.BLUE_50,
                                border_radius=8
                            )
                        ]),
                        padding=20,
                        bgcolor=ft.Colors.GREEN_50,
                        border_radius=12
                    )
                    
                ], spacing=0),
                padding=25
            ),
            elevation=2,
            margin=ft.margin.only(bottom=10)
        )
    
    def _calculate_total(self, e):
        """Calcula automáticamente el total"""
        try:
            menor = float(self.facturacion_menor_field.value or 0)
            mayor = float(self.facturacion_mayor_field.value or 0)
            total = menor + mayor
            
            self.facturacion_total_field.value = str(total)
            self.page.update()
            
        except ValueError:
            # Si hay error en la conversión, mantener el valor actual
            pass
    
    def _build_actions(self) -> ft.Control:
        """Construye las acciones"""
        return ft.Card(
            content=ft.Container(
                content=ft.Row([
                    ft.ElevatedButton(
                        content=ft.Row([
                            ft.Icon(ft.Icons.CANCEL, size=20),
                            ft.Text("Cancelar", size=16)
                        ], spacing=8),
                        on_click=lambda _: self.app.navigate_to("facturacion"),
                        style=ft.ButtonStyle(
                            bgcolor=ft.Colors.GREY_400,
                            color=ft.Colors.WHITE,
                            padding=ft.padding.symmetric(horizontal=25, vertical=15),
                            shape=ft.RoundedRectangleBorder(radius=10)
                        ),
                        width=150,
                        height=50
                    ),
                    
                    ft.Container(expand=True),  # Espaciador
                    
                    ft.ElevatedButton(
                        content=ft.Row([
                            ft.Icon(ft.Icons.SAVE, size=20),
                            ft.Text("Guardar Facturación", size=16, weight=ft.FontWeight.W_600)
                        ], spacing=8),
                        on_click=self._save_facturacion,
                        style=ft.ButtonStyle(
                            bgcolor=ft.Colors.BLUE_600,
                            color=ft.Colors.WHITE,
                            padding=ft.padding.symmetric(horizontal=30, vertical=15),
                            shape=ft.RoundedRectangleBorder(radius=10),
                            elevation=3
                        ),
                        width=220,
                        height=50
                    )
                ], spacing=15),
                padding=25
            ),
            elevation=2
        )

    def _save_facturacion(self, e):
        """Guarda la facturación"""
        try:
            # Validar campos
            if not self._validate_form():
                return
            
            # Actualizar modelo
            self.facturacion.municipio_id = int(self.municipio_dropdown.value)
            self.facturacion.año = int(self.año_field.value)
            self.facturacion.mes = int(self.mes_dropdown.value)
            self.facturacion.facturacion_menor = float(self.facturacion_menor_field.value or 0)
            self.facturacion.facturacion_mayor = float(self.facturacion_mayor_field.value or 0)
            self.facturacion.facturacion_total = float(self.facturacion_total_field.value or 0)
            
            # Establecer usuario actual
            if self.app.current_user:
                self.facturacion.usuario_id = self.app.current_user['id']
            
            # Verificar si ya existe (solo para nuevas)
            if not self.is_edit_mode:
                if self.facturacion_service.verificar_facturacion_existe(
                    self.facturacion.municipio_id, self.facturacion.año, 
                    self.facturacion.mes
                ):
                    self._show_error("Ya existe una facturación para este municipio y período")
                    return
            
            # Guardar
            if self.facturacion_service.save_facturacion(self.facturacion):
                self._show_success("Facturación guardada correctamente")
                # Pequeña pausa antes de navegar
                import time
                time.sleep(0.5)
                self.app.navigate_to("facturacion")
            else:
                self._show_error("Error al guardar la facturación")
                
        except Exception as e:
            self.logger.error(f"Error al guardar facturación: {e}")
            self._show_error("Error al guardar la facturación")

    def _validate_form(self) -> bool:
        """Valida el formulario"""
        if not self.municipio_dropdown.value:
            self._show_error("Debe seleccionar un municipio")
            return False
        
        if not self.año_field.value or not self.año_field.value.isdigit():
            self._show_error("Debe ingresar un año válido")
            return False
        
        if not self.mes_dropdown.value:
            self._show_error("Debe seleccionar un mes")
            return False
        
        try:
            menor = float(self.facturacion_menor_field.value or 0)
            mayor = float(self.facturacion_mayor_field.value or 0)
            
            if menor < 0 or mayor < 0:
                self._show_error("Los valores no pueden ser negativos")
                return False
                
            if menor == 0 and mayor == 0:
                self._show_error("Debe ingresar al menos un valor de facturación")
                return False
                
        except ValueError:
            self._show_error("Debe ingresar valores numéricos válidos")
            return False
        
        return True

    def _show_success(self, message: str):
        """Muestra mensaje de éxito"""
        snack_bar = ft.SnackBar(
            content=ft.Row([
                ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.WHITE, size=20),
                ft.Text(message, color=ft.Colors.WHITE, size=16)
            ]),
            bgcolor=ft.Colors.GREEN_600,
            behavior=ft.SnackBarBehavior.FLOATING,
            margin=ft.margin.all(10),
            padding=ft.padding.symmetric(horizontal=20, vertical=15),
            shape=ft.RoundedRectangleBorder(radius=10)
        )
        self.page.snack_bar = snack_bar
        snack_bar.open = True
        self.page.update()

    def _show_error(self, message: str):
        """Muestra mensaje de error"""
        snack_bar = ft.SnackBar(
            content=ft.Row([
                ft.Icon(ft.Icons.ERROR, color=ft.Colors.WHITE, size=20),
                ft.Text(message, color=ft.Colors.WHITE, size=16)
            ]),
            bgcolor=ft.Colors.RED_600,
            behavior=ft.SnackBarBehavior.FLOATING,
            margin=ft.margin.all(10),
            padding=ft.padding.symmetric(horizontal=20, vertical=15),
            shape=ft.RoundedRectangleBorder(radius=10)
        )
        self.page.snack_bar = snack_bar
        snack_bar.open = True
        self.page.update()

    def _show_info(self, message: str):
        """Muestra mensaje informativo"""
        snack_bar = ft.SnackBar(
            content=ft.Row([
                ft.Icon(ft.Icons.INFO, color=ft.Colors.WHITE, size=20),
                ft.Text(message, color=ft.Colors.WHITE, size=16)
            ]),
            bgcolor=ft.Colors.BLUE_600,
            behavior=ft.SnackBarBehavior.FLOATING,
            margin=ft.margin.all(10),
            padding=ft.padding.symmetric(horizontal=20, vertical=15),
            shape=ft.RoundedRectangleBorder(radius=10)
        )
        self.page.snack_bar = snack_bar
        snack_bar.open = True
        self.page.update()
                            
