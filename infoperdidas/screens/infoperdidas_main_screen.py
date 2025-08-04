"""
Pantalla principal del módulo InfoPérdidas
Muestra cálculos de pérdidas por municipio y provincia
"""

import flet as ft
from datetime import datetime
from typing import List, Dict, Any
from infoperdidas.services import get_perdidas_service
from infoperdidas.models import PerdidasCalculoModel, PerdidasResumenModel
from core.logger import get_logger

class InfoPerdidasMainScreen:
    """Pantalla principal de InfoPérdidas"""
    
    def __init__(self, app):
        self.app = app
        self.page = app.page
        self.logger = get_logger(__name__)
        self.perdidas_service = get_perdidas_service()
        
        # Estado
        self.resumen_provincial = None
        self.municipios_data = []
        
        # Fechas actuales
        now = datetime.now()
        self.current_año = now.year
        self.current_mes = now.month
        
        # Controles
        self.año_field = None
        self.mes_dropdown = None
        self.data_table = None
        self.resumen_card = None
        self.status_card = None
    
    def build(self) -> ft.Control:
        """Construye la interfaz"""
        return ft.Container(
            content=ft.Column([
                self._build_header(),
                self._build_filters(),
                self._build_status_card(),
                self._build_resumen_provincial(),
                self._build_data_table(),
                self._build_actions()
            ], spacing=25),
            padding=25,
            expand=True,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=[ft.Colors.GREY_50, ft.Colors.WHITE]
            )
        )
    
    def _build_header(self) -> ft.Control:
        """Construye el header de la pantalla"""
        return ft.Container(
            content=ft.Row([
                ft.Row([
                    ft.Container(
                        content=ft.Icon(ft.Icons.ELECTRIC_BOLT, size=40, color=ft.Colors.WHITE),
                        bgcolor=ft.Colors.ORANGE,
                        border_radius=50,
                        padding=15,
                        shadow=ft.BoxShadow(
                            spread_radius=1,
                            blur_radius=10,
                            color=ft.Colors.ORANGE_200,
                            offset=ft.Offset(0, 4)
                        )
                    ),
                    ft.Column([
                        ft.Text(
                            "Información de Pérdidas Eléctricas", 
                            size=28, 
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.WHITE
                        ),
                        ft.Text(
                            "Análisis integral de pérdidas por municipio y provincia", 
                            size=16, 
                            color=ft.Colors.WHITE70
                        )
                    ], spacing=5)
                ], spacing=20),
                ft.Container(expand=True),
                ft.Row([
                    ft.Container(
                        content=ft.IconButton(
                            ft.Icons.REFRESH,
                            icon_color=ft.Colors.WHITE,
                            tooltip="Actualizar datos",
                            on_click=self._load_data,
                            icon_size=24
                        ),
                        bgcolor=ft.Colors.WHITE24,
                        border_radius=30,
                        padding=5
                    ),
                    ft.Container(
                        content=ft.IconButton(
                            ft.Icons.SETTINGS,
                            icon_color=ft.Colors.WHITE,
                            tooltip="Gestionar Planes",
                            on_click=lambda _: self.app.navigate_to("infoperdidas_planes"),
                            icon_size=24
                        ),
                        bgcolor=ft.Colors.WHITE24,
                        border_radius=30,
                        padding=5
                    ),
                    ft.Container(
                        content=ft.IconButton(
                            ft.Icons.ARROW_BACK,
                            icon_color=ft.Colors.WHITE,
                            tooltip="Volver al Dashboard",
                            on_click=lambda _: self.app.navigate_to("dashboard"),
                            icon_size=24
                        ),
                        bgcolor=ft.Colors.WHITE24,
                        border_radius=30,
                        padding=5
                    )
                ], spacing=10)
            ]),
            gradient=ft.LinearGradient(
                begin=ft.alignment.center_left,
                end=ft.alignment.center_right,
                colors=[ft.Colors.ORANGE_600, ft.Colors.DEEP_ORANGE_400]
            ),
            padding=30,
            border_radius=15,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=ft.Colors.ORANGE_200,
                offset=ft.Offset(0, 5)
            )
        )
    
    def _build_filters(self) -> ft.Control:
        """Construye los filtros de período"""
        self.año_field = ft.TextField(
            label="Año",
            value=str(self.current_año),
            width=120,
            keyboard_type=ft.KeyboardType.NUMBER,
            border_radius=10,
            filled=True,
            bgcolor=ft.Colors.WHITE,
            prefix_icon=ft.Icons.CALENDAR_TODAY
        )
        
        self.mes_dropdown = ft.Dropdown(
            label="Mes",
            width=180,
            value=str(self.current_mes),
            border_radius=10,
            filled=True,
            bgcolor=ft.Colors.WHITE,
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
        
        load_button = ft.Container(
            content=ft.ElevatedButton(
                content=ft.Row([
                    ft.Icon(ft.Icons.CALCULATE, size=20),
                    ft.Text("Calcular Pérdidas", size=16, weight=ft.FontWeight.BOLD)
                ], spacing=8, tight=True),
                on_click=self._load_data,
                style=ft.ButtonStyle(
                    bgcolor=ft.Colors.ORANGE_600,
                    color=ft.Colors.WHITE,
                    elevation=8,
                    shadow_color=ft.Colors.ORANGE_200,
                    shape=ft.RoundedRectangleBorder(radius=12)
                ),
                height=50
            )
        )
        
        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.FILTER_LIST, color=ft.Colors.ORANGE_600, size=24),
                        ft.Text("Período de Consulta", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_800)
                    ], spacing=10),
                    ft.Container(height=15),
                    ft.Row([
                        self.año_field,
                        self.mes_dropdown,
                        load_button,
                        ft.Container(expand=True)
                    ], spacing=20, alignment=ft.MainAxisAlignment.START)
                ], spacing=10),
                padding=25
            ),
            elevation=5,
            shadow_color=ft.Colors.GREY_300,
            surface_tint_color=ft.Colors.ORANGE_50
        )
    
    def _build_status_card(self) -> ft.Control:
        """Construye la tarjeta de estado de datos"""
        self.status_card = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.INFO_OUTLINE, color=ft.Colors.BLUE_600, size=24),
                        ft.Text("Estado del Sistema", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_800)
                    ], spacing=10),
                    ft.Container(height=10),
                    ft.Text("Verificando disponibilidad de datos...", size=14, color=ft.Colors.GREY_600)
                ]),
                padding=20
            ),
            elevation=3,
            surface_tint_color=ft.Colors.BLUE_50
        )
        return self.status_card
    
    def _build_resumen_provincial(self) -> ft.Control:
        """Construye el resumen provincial"""
        self.resumen_card = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.ANALYTICS, color=ft.Colors.GREEN_600, size=28),
                        ft.Text("Resumen Provincial", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_800)
                    ], spacing=12),
                    ft.Container(height=15),
                    ft.Container(
                        content=ft.Text(
                            "Seleccione un período para visualizar los cálculos detallados", 
                            size=16, 
                            color=ft.Colors.GREY_600,
                            text_align=ft.TextAlign.CENTER
                        ),
                        alignment=ft.alignment.center,
                        padding=20
                    )
                ]),
                padding=25
            ),
            elevation=8,
            shadow_color=ft.Colors.GREEN_200,
            surface_tint_color=ft.Colors.GREEN_50
        )
        return self.resumen_card
    

    def _build_actions(self) -> ft.Control:
        """Construye las acciones"""
        return ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.ElevatedButton(
                        content=ft.Row([
                            ft.Icon(ft.Icons.EDIT_NOTE, size=20),
                            ft.Text("Gestionar Planes", size=16, weight=ft.FontWeight.BOLD)
                        ], spacing=8, tight=True),
                        on_click=lambda _: self.app.navigate_to("infoperdidas_planes"),
                        style=ft.ButtonStyle(
                            bgcolor=ft.Colors.BLUE_600,
                            color=ft.Colors.WHITE,
                            elevation=6,
                            shadow_color=ft.Colors.BLUE_200,
                            shape=ft.RoundedRectangleBorder(radius=12)
                        ),
                        height=50
                    )
                ),
                ft.Container(expand=True),
                ft.Container(
                    content=ft.ElevatedButton(
                        content=ft.Row([
                            ft.Icon(ft.Icons.DOWNLOAD, size=20),
                            ft.Text("Exportar Excel", size=16, weight=ft.FontWeight.BOLD)
                        ], spacing=8, tight=True),
                        on_click=self._export_to_excel,
                        disabled=True,
                        style=ft.ButtonStyle(
                            bgcolor=ft.Colors.GREEN_600,
                            color=ft.Colors.WHITE,
                            elevation=6,
                            shadow_color=ft.Colors.GREEN_200,
                            shape=ft.RoundedRectangleBorder(radius=12)
                        ),
                        height=50
                    )
                )
            ], spacing=15),
            padding=ft.padding.only(top=25)
        )
    
    def _load_data(self, e=None):
        """Carga y calcula los datos de pérdidas"""
        try:
            # Obtener período
            año = int(self.año_field.value) if self.año_field.value else self.current_año
            mes = int(self.mes_dropdown.value) if self.mes_dropdown.value else self.current_mes
            
            # Verificar disponibilidad de datos
            disponibilidad = self.perdidas_service.verificar_datos_disponibles(año, mes)
            self._update_status_card(disponibilidad)
            
            if not disponibilidad['calculo_posible']:
                self._show_warning("No hay suficientes datos para realizar el cálculo")
                return
            
            # CAMBIO: Usar el nuevo método que calcula Y guarda
            self.resumen_provincial = self.perdidas_service.calcular_y_guardar_perdidas_provincia(
                año, mes, self.app.current_user['id']  # Pasar ID del usuario actual
            )
            
            if self.resumen_provincial:
                self.municipios_data = self.resumen_provincial.municipios
                self._update_resumen_card()
                self._update_data_table()
                self._show_success(f"Cálculos actualizados y guardados para {mes:02d}/{año}")
                
                # Habilitar botón de exportar
                self._enable_export_button()
            else:
                self._show_error("Error al calcular las pérdidas")
            
        except Exception as e:
            self.logger.error(f"Error cargando datos: {e}")
            self._show_error("Error al cargar los datos de pérdidas")

    def _update_status_card(self, disponibilidad: Dict[str, Any]):
        """Actualiza la tarjeta de estado"""
        status_items = []
        
        # Estado de energía
        energia_status = self._create_status_indicator(
            disponibilidad['energia_disponible'],
            f"Energía en Barra: {disponibilidad['energia_registros']} registros",
            ft.Icons.ELECTRIC_METER
        )
        status_items.append(energia_status)
        
        # Estado de facturación
        fac_status = self._create_status_indicator(
            disponibilidad['facturacion_disponible'],
            f"Facturación: {disponibilidad['facturacion_registros']} registros",
            ft.Icons.RECEIPT_LONG
        )
        status_items.append(fac_status)
        
        # Estado de planes
        plan_status = self._create_status_indicator(
            disponibilidad['planes_disponibles'],
            f"Planes: {disponibilidad['planes_registros']} registros",
            ft.Icons.ASSIGNMENT,
            warning_mode=True
        )
        status_items.append(plan_status)
        
        # Estado general
        general_color = ft.Colors.GREEN_600 if disponibilidad['calculo_posible'] else ft.Colors.RED_600
        general_icon = ft.Icons.CHECK_CIRCLE if disponibilidad['calculo_posible'] else ft.Icons.ERROR
        general_text = "Sistema listo para cálculos" if disponibilidad['calculo_posible'] else "Faltan datos para el cálculo"
        
        self.status_card.content = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.DASHBOARD, color=ft.Colors.BLUE_600, size=24),
                    ft.Text("Estado del Sistema", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_800)
                ], spacing=10),
                ft.Divider(color=ft.Colors.GREY_300),
                ft.Column(status_items, spacing=12),
                ft.Divider(color=ft.Colors.GREY_300),
                ft.Container(
                    content=ft.Row([
                        ft.Icon(general_icon, color=general_color, size=20),
                        ft.Text(general_text, color=general_color, weight=ft.FontWeight.BOLD, size=14)
                    ], spacing=8),
                    bgcolor=ft.Colors.with_opacity(0.1, general_color),  # CORREGIR: pasar opacity primero
                    padding=12,
                    border_radius=8,
                    border=ft.border.all(1, ft.Colors.with_opacity(0.3, general_color))  # CORREGIR: pasar opacity primero
                )
            ], spacing=15),
            padding=20
        )
        
        self.page.update()

    def _create_status_indicator(self, is_available: bool, text: str, icon: ft.Icons, warning_mode: bool = False):
        """Crea un indicador de estado visual"""
        if is_available:
            color = ft.Colors.GREEN_600
            status_icon = ft.Icons.CHECK_CIRCLE
            bg_color = ft.Colors.GREEN_50
        elif warning_mode and not is_available:
            color = ft.Colors.ORANGE_600
            status_icon = ft.Icons.WARNING
            bg_color = ft.Colors.ORANGE_50
        else:
            color = ft.Colors.RED_600
            status_icon = ft.Icons.ERROR
            bg_color = ft.Colors.RED_50
        
        return ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Icon(icon, color=color, size=18),
                    bgcolor=bg_color,
                    border_radius=20,
                    padding=8
                ),
                ft.Column([
                    ft.Text(text, size=13, color=ft.Colors.GREY_800),
                    ft.Container(
                        content=ft.Icon(status_icon, color=color, size=16),
                        alignment=ft.alignment.center_left
                    )
                ], spacing=2, expand=True)
            ], spacing=12),
            padding=8,
            border_radius=8,
            bgcolor=ft.Colors.with_opacity(0.3, bg_color)  # CORREGIR: pasar opacity primero
        )

    def _update_resumen_card(self):
        """Actualiza la tarjeta de resumen provincial"""
        if not self.resumen_provincial:
            return
        
        r = self.resumen_provincial
        
        # Crear métricas destacadas
        metricas_mensuales = [
            self._create_metric_card("Energía Total", f"{r.total_energia_barra:,.1f} MWh", ft.Icons.ELECTRIC_METER, ft.Colors.BLUE_600),
            self._create_metric_card("Total Ventas", f"{r.total_ventas:,.1f} MWh", ft.Icons.POINT_OF_SALE, ft.Colors.GREEN_600),
            self._create_metric_card("Pérdidas", f"{r.total_perdidas_mwh:,.1f} MWh", ft.Icons.TRENDING_DOWN, ft.Colors.RED_600),
            self._create_metric_card("% Pérdidas", f"{r.total_perdidas_pct:.2f}%", ft.Icons.PERCENT, ft.Colors.RED_600)
        ]
        
        metricas_acumuladas = [
            self._create_metric_card("Energía Acum.", f"{r.total_energia_acumulada:,.1f} MWh", ft.Icons.STACKED_BAR_CHART, ft.Colors.PURPLE_600),  # Cambiar CUMULATIVE
            self._create_metric_card("Pérdidas Acum.", f"{r.total_perdidas_acumuladas_mwh:,.1f} MWh", ft.Icons.TRENDING_DOWN, ft.Colors.ORANGE_600),
            self._create_metric_card("% Pérdidas Acum.", f"{r.total_perdidas_acumuladas_pct:.2f}%", ft.Icons.PERCENT, ft.Colors.ORANGE_600),
            self._create_metric_card("Plan Acum.", f"{r.total_plan_acumulado_pct:.2f}%", ft.Icons.TRACK_CHANGES, ft.Colors.INDIGO_600)  # Cambiar TARGET
        ]
        
        # Comparación Plan vs Real
        plan_comparison = self._create_plan_comparison(r.total_perdidas_pct, r.total_plan_perdidas_pct)
        
        self.resumen_card.content = ft.Container(
            content=ft.Column([
                # Header
                ft.Row([
                    ft.Icon(ft.Icons.ANALYTICS, color=ft.Colors.GREEN_600, size=28),
                    ft.Text(f"Resumen Provincial - {r.mes:02d}/{r.año}", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_800)
                ], spacing=12),
                
                ft.Container(height=10),
                
                # Métricas mensuales
                ft.Text("📊 Datos del Mes", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700),
                ft.Row(metricas_mensuales, spacing=15),
                
                ft.Container(height=15),
                
                # Métricas acumuladas
                ft.Text("📈 Datos Acumulados", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.PURPLE_700),
                ft.Row(metricas_acumuladas, spacing=15),
                
                ft.Container(height=15),
                
                # Comparación Plan vs Real
                plan_comparison
                
            ], spacing=15),
            padding=25
        )
        
        self.page.update()

    def _create_metric_card(self, title: str, value: str, icon: ft.Icons, color: ft.Colors):
        """Crea una tarjeta de métrica"""
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(icon, color=color, size=20),
                    ft.Text(title, size=12, color=ft.Colors.GREY_600, weight=ft.FontWeight.BOLD)
                ], spacing=8),
                ft.Text(value, size=16, weight=ft.FontWeight.BOLD, color=color)
            ], spacing=8, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=ft.Colors.with_opacity(0.1, color),  # CORREGIR: pasar opacity primero
            border=ft.border.all(1, ft.Colors.with_opacity(0.3, color)),  # CORREGIR: pasar opacity primero
            border_radius=10,
            padding=15,
            expand=True,
            alignment=ft.alignment.center
        )

    def _create_plan_comparison(self, real_pct: float, plan_pct: float):
        """Crea la comparación entre plan y real"""
        diferencia = real_pct - plan_pct
        is_better = diferencia <= 0
        
        color = ft.Colors.GREEN_600 if is_better else ft.Colors.RED_600
        icon = ft.Icons.TRENDING_DOWN if is_better else ft.Icons.TRENDING_UP
        status_text = "Dentro del Plan" if is_better else "Sobre el Plan"
        
        return ft.Container(
            content=ft.Column([
                ft.Text("🎯 Comparación Plan vs Real", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.INDIGO_700),
                ft.Container(height=5),
                ft.Row([
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Plan", size=12, color=ft.Colors.GREY_600),
                            ft.Text(f"{plan_pct:.2f}%", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_600)
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        expand=True
                    ),
                    ft.Container(
                        content=ft.Column([
                            ft.Icon(icon, color=color, size=24),
                            ft.Text(f"{abs(diferencia):.2f}%", size=14, weight=ft.FontWeight.BOLD, color=color),
                            ft.Text(status_text, size=10, color=color)
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        expand=True
                    ),
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Real", size=12, color=ft.Colors.GREY_600),
                            ft.Text(f"{real_pct:.2f}%", size=18, weight=ft.FontWeight.BOLD, color=color)
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        expand=True
                    )
                ])
            ]),
            bgcolor=ft.Colors.INDIGO_50,
            border=ft.border.all(1, ft.Colors.INDIGO_200),
            border_radius=10,
            padding=15
        )
    
    def _build_data_table(self) -> ft.Control:
        """Construye la tabla de datos por municipio"""
        # Headers con mejor diseño - CORREGIR ICONOS
        headers = [
            ("Municipio", ft.Icons.LOCATION_CITY),
            ("Energía Barra\n(MWh)", ft.Icons.ELECTRIC_METER),
            ("Fact. Mayor\n(MWh)", ft.Icons.BUSINESS),
            ("Fact. Menor\n(MWh)", ft.Icons.HOME),
            ("Total Ventas\n(MWh)", ft.Icons.POINT_OF_SALE),
            ("Pérdidas\n(MWh)", ft.Icons.TRENDING_DOWN),
            ("Pérdidas\n(%)", ft.Icons.PERCENT),
            ("Plan\n(%)", ft.Icons.TRACK_CHANGES),
            ("Energía Acum.\n(MWh)", ft.Icons.STACKED_BAR_CHART),
            ("Pérdidas Acum.\n(MWh)", ft.Icons.TRENDING_DOWN),
            ("Pérdidas Acum.\n(%)", ft.Icons.PERCENT),
            ("Plan Acum.\n(%)", ft.Icons.TRACK_CHANGES)
        ]
        
        columns = []
        for header_text, icon in headers:
            columns.append(
                ft.DataColumn(
                    ft.Container(
                        content=ft.Column([
                            ft.Icon(icon, size=16, color=ft.Colors.ORANGE_600),
                            ft.Text(
                                header_text, 
                                size=11, 
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.GREY_800,
                                text_align=ft.TextAlign.CENTER
                            )
                        ], spacing=3, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        padding=ft.padding.symmetric(horizontal=4, vertical=8),
                        width=120  # Ancho fijo para cada columna
                    )
                )
            )
        
        self.data_table = ft.DataTable(
            columns=columns,
            rows=[],
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=10,
            data_row_min_height=45,
            data_row_max_height=50,
            heading_row_color=ft.Colors.ORANGE_50,
            heading_row_height=60,
            column_spacing=5,  # Espaciado entre columnas
            horizontal_margin=5,  # Margen horizontal
            show_checkbox_column=False
        )
        
        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.TABLE_CHART, color=ft.Colors.PURPLE_600, size=26),
                        ft.Text("Análisis Detallado por Municipio", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_800)
                    ], spacing=12),
                    ft.Container(height=15),
                    # Contenedor con scroll horizontal y vertical
                    ft.Container(
                        content=ft.Row([
                            ft.Container(
                                content=ft.Column([
                                    self.data_table
                                ], 
                                scroll=ft.ScrollMode.AUTO,  # Scroll vertical
                                expand=True
                                ),
                                expand=True
                            )
                        ], 
                        scroll=ft.ScrollMode.AUTO,  # Scroll horizontal
                        expand=True
                        ),
                        height=600,  # Altura fija para el contenedor de la tabla
                        border_radius=10,
                        border=ft.border.all(1, ft.Colors.GREY_200),
                        padding=5
                    )
                ]),
                padding=25
            ),
            elevation=6,
            shadow_color=ft.Colors.PURPLE_200,
            surface_tint_color=ft.Colors.PURPLE_50
        )

    def _create_data_cell(self, value: str, color: ft.Colors):
        """Crea una celda de datos con formato"""
        return ft.Container(
            content=ft.Text(
                value,
                size=12,  # Tamaño de fuente reducido
                weight=ft.FontWeight.BOLD,
                color=color,
                text_align=ft.TextAlign.RIGHT,
                overflow=ft.TextOverflow.ELLIPSIS  # Manejo de overflow
            ),
            padding=ft.padding.symmetric(horizontal=4, vertical=6),
            alignment=ft.alignment.center_right,
            width=115  # Ancho fijo para consistencia
        )

    def _create_percentage_cell(self, percentage: float, color: ft.Colors):
        """Crea una celda de porcentaje con formato especial"""
        return ft.Container(
            content=ft.Container(
                content=ft.Text(
                    f"{percentage:.2f}%",
                    size=11,  # Tamaño de fuente reducido
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE,
                    text_align=ft.TextAlign.CENTER,
                    overflow=ft.TextOverflow.ELLIPSIS
                ),
                bgcolor=color,
                border_radius=12,
                padding=ft.padding.symmetric(horizontal=6, vertical=3),
                alignment=ft.alignment.center,
                width=80  # Ancho fijo más pequeño para porcentajes
            ),
            padding=ft.padding.symmetric(horizontal=4, vertical=6),
            alignment=ft.alignment.center,
            width=115
        )

    def _update_data_table(self):
        """Actualiza la tabla de datos por municipio"""
        if not self.municipios_data:
            return
        
        self.data_table.rows.clear()
        
        for i, municipio in enumerate(self.municipios_data):
            # Colores alternados para las filas
            row_color = ft.Colors.GREY_50 if i % 2 == 0 else ft.Colors.WHITE
            
            # Colores condicionales para pérdidas
            perdidas_color = ft.Colors.RED_600 if municipio.perdidas_pct > municipio.plan_perdidas_pct else ft.Colors.GREEN_600
            perdidas_acum_color = ft.Colors.RED_600 if municipio.perdidas_acumuladas_pct > municipio.plan_perdidas_acumulado_pct else ft.Colors.GREEN_600
            
            self.data_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(
                            ft.Container(
                                content=ft.Text(
                                    municipio.municipio_nombre or "N/A", 
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.GREY_800,
                                    size=12,
                                    overflow=ft.TextOverflow.ELLIPSIS
                                ),
                                padding=ft.padding.symmetric(horizontal=4, vertical=6),
                                width=115,
                                alignment=ft.alignment.center_left
                            )
                        ),
                        ft.DataCell(self._create_data_cell(f"{municipio.energia_barra_mwh:,.1f}", ft.Colors.BLUE_600)),
                        ft.DataCell(self._create_data_cell(f"{municipio.facturacion_mayor:,.1f}", ft.Colors.GREEN_600)),
                        ft.DataCell(self._create_data_cell(f"{municipio.facturacion_menor:,.1f}", ft.Colors.GREEN_700)),
                        ft.DataCell(self._create_data_cell(f"{municipio.total_ventas:,.1f}", ft.Colors.GREEN_800)),
                        ft.DataCell(self._create_data_cell(f"{municipio.perdidas_distribucion_mwh:,.1f}", perdidas_color)),
                        ft.DataCell(self._create_percentage_cell(municipio.perdidas_pct, perdidas_color)),
                        ft.DataCell(self._create_percentage_cell(municipio.plan_perdidas_pct, ft.Colors.BLUE_600)),
                        ft.DataCell(self._create_data_cell(f"{municipio.energia_barra_acumulada:,.1f}", ft.Colors.PURPLE_600)),
                        ft.DataCell(self._create_data_cell(f"{municipio.perdidas_acumuladas_mwh:,.1f}", perdidas_acum_color)),
                        ft.DataCell(self._create_percentage_cell(municipio.perdidas_acumuladas_pct, perdidas_acum_color)),
                        ft.DataCell(self._create_percentage_cell(municipio.plan_perdidas_acumulado_pct, ft.Colors.INDIGO_600))
                    ],
                    color=row_color
                )
            )
        
        self.page.update()

    def _enable_export_button(self):
        """Habilita el botón de exportar"""
        # Buscar el botón de exportar en las acciones y habilitarlo
        # Esto se puede hacer reconstruyendo las acciones o manteniendo una referencia
        pass  # Se implementaría si necesitas habilitar/deshabilitar dinámicamente
    
    def _export_to_excel(self, e):
        """Exporta los datos a Excel"""
        try:
            if not self.resumen_provincial or not self.municipios_data:
                self._show_warning("No hay datos para exportar")
                return
            
            import pandas as pd
            from pathlib import Path
            
            # Preparar datos para exportación
            export_data = []
            
            # Agregar resumen provincial
            r = self.resumen_provincial
            export_data.append({
                'Municipio': 'TOTAL PROVINCIAL',
                'Energía Barra (MWh)': r.total_energia_barra,
                'Facturación Mayor (MWh)': r.total_facturacion_mayor,
                'Facturación Menor (MWh)': r.total_facturacion_menor,
                'Total Ventas (MWh)': r.total_ventas,
                'Pérdidas (MWh)': r.total_perdidas_mwh,
                'Pérdidas (%)': r.total_perdidas_pct,
                'Plan (%)': r.total_plan_perdidas_pct,
                'Energía Acumulada (MWh)': r.total_energia_acumulada,
                'Pérdidas Acumuladas (MWh)': r.total_perdidas_acumuladas_mwh,
                'Pérdidas Acumuladas (%)': r.total_perdidas_acumuladas_pct,
                'Plan Acumulado (%)': r.total_plan_acumulado_pct
            })
            
            # Agregar línea separadora
            export_data.append({col: '' for col in export_data[0].keys()})
            
            # Agregar datos por municipio
            for municipio in self.municipios_data:
                export_data.append({
                    'Municipio': municipio.municipio_nombre,
                    'Energía Barra (MWh)': municipio.energia_barra_mwh,
                    'Facturación Mayor (MWh)': municipio.facturacion_mayor,
                    'Facturación Menor (MWh)': municipio.facturacion_menor,
                    'Total Ventas (MWh)': municipio.total_ventas,
                    'Pérdidas (MWh)': municipio.perdidas_distribucion_mwh,
                    'Pérdidas (%)': municipio.perdidas_pct,
                    'Plan (%)': municipio.plan_perdidas_pct,
                    'Energía Acumulada (MWh)': municipio.energia_barra_acumulada,
                    'Pérdidas Acumuladas (MWh)': municipio.perdidas_acumuladas_mwh,
                    'Pérdidas Acumuladas (%)': municipio.perdidas_acumuladas_pct,
                    'Plan Acumulado (%)': municipio.plan_perdidas_acumulado_pct
                })
            
            # Crear DataFrame y exportar
            df = pd.DataFrame(export_data)
            
            # Guardar archivo
            downloads_path = Path.home() / "Downloads"
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_path = downloads_path / f"infoperdidas_{r.mes:02d}_{r.año}_{timestamp}.xlsx"
            
            df.to_excel(file_path, index=False, sheet_name=f"Pérdidas {r.mes:02d}-{r.año}")
            
            self._show_success(f"Datos exportados a: {file_path}")
            
        except Exception as ex:
            self.logger.error(f"Error exportando a Excel: {ex}")
            self._show_error("Error al exportar los datos")
    
    def _show_success(self, message: str):
        """Muestra mensaje de éxito"""
        snack_bar = ft.SnackBar(
            content=ft.Row([
                ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.WHITE, size=20),
                ft.Text(message, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)
            ], spacing=10),
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
                ft.Text(message, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)
            ], spacing=10),
            bgcolor=ft.Colors.RED_600,
            behavior=ft.SnackBarBehavior.FLOATING,
            margin=ft.margin.all(10),
            padding=ft.padding.symmetric(horizontal=20, vertical=15),
            shape=ft.RoundedRectangleBorder(radius=10)
        )
        self.page.snack_bar = snack_bar
        snack_bar.open = True
        self.page.update()
    
    def _show_warning(self, message: str):
        """Muestra mensaje de advertencia"""
        snack_bar = ft.SnackBar(
            content=ft.Row([
                ft.Icon(ft.Icons.WARNING, color=ft.Colors.WHITE, size=20),
                ft.Text(message, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)
            ], spacing=10),
            bgcolor=ft.Colors.ORANGE_600,
            behavior=ft.SnackBarBehavior.FLOATING,
            margin=ft.margin.all(10),
            padding=ft.padding.symmetric(horizontal=20, vertical=15),
            shape=ft.RoundedRectangleBorder(radius=10)
        )
        self.page.snack_bar = snack_bar
        snack_bar.open = True
        self.page.update()
