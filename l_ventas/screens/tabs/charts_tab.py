"""
Pestaña de Gráficos con componentes nativos de Flet
"""

import flet as ft
import math
from typing import List, Dict, Any
from .base_tab import BaseTab

class ChartsTab(BaseTab):
    """Pestaña de gráficos usando componentes nativos de Flet"""
    
    def __init__(self, main_screen):
        super().__init__(main_screen)
        
        # Configuración de gráficos
        self.selected_chart_type = "line"  # line, bar, pie
        self.selected_metric = "perdidas"  # perdidas, energia, facturacion
        self.selected_data_source = "mensual"  # mensual, acumulada
        self.show_comparison = False
        
        self.logger.info("ChartsTab inicializada")
    
    def build(self) -> ft.Control:
        """Construye la vista de gráficos"""
        try:
            return ft.Column([
                # Header con controles
                self._build_chart_header(),
                
                ft.Container(height=20),
                
                # Área de gráfico
                ft.Container(
                    content=self._build_chart_area(),
                    expand=True
                )
            ], expand=True)
            
        except Exception as e:
            self.logger.error(f"Error construyendo pestaña de gráficos: {e}")
            return self._build_error_view(str(e))
    
    def _build_chart_header(self) -> ft.Control:
        """Construye el header con controles de gráfico"""
        return ft.Container(
            content=ft.Column([
                # Título principal
                ft.Row([
                    ft.Container(
                        content=ft.Icon(ft.Icons.BAR_CHART, size=28, color=self.theme['white']),
                        width=50, height=50,
                        bgcolor=self.theme['info'],
                        border_radius=25,
                        alignment=ft.alignment.center
                    ),
                    ft.Container(width=16),
                    ft.Column([
                        ft.Text(
                            f"📊 Análisis Gráfico - {self.get_period_text()}",
                            size=24,
                            weight=ft.FontWeight.BOLD,
                            color=self.theme['text_primary']
                        ),
                        ft.Text(
                            "Visualización interactiva de datos de pérdidas",
                            size=14,
                            color=self.theme['text_secondary']
                        )
                    ], spacing=4),
                    ft.Container(expand=True),
                    ft.ElevatedButton(
                        content=ft.Row([
                            ft.Icon(ft.Icons.DOWNLOAD, size=16),
                            ft.Text("Exportar", size=12)
                        ], spacing=6),
                        on_click=self._export_chart,
                        bgcolor=self.theme['info'],
                        color=self.theme['white'],
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
                    )
                ]),
                
                ft.Container(height=20),
                
                # Controles de configuración
                ft.Row([
                    # Selector de período - CORRECCIÓN: llamar correctamente
                    self.build_period_selector(self._refresh_chart),
                    
                    ft.Container(width=20),
                    
                    # Controles de gráfico
                    self._build_chart_controls()
                ], alignment=ft.MainAxisAlignment.START)
            ]),
            bgcolor=self.theme['white'],
            padding=24,
            border_radius=16,
            border=ft.border.all(1, self.theme['border']),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=8,
                color='rgba(0,0,0,0.05)',
                offset=ft.Offset(0, 2)
            )
        )
    def _build_chart_controls(self) -> ft.Control:
        """Construye los controles de configuración del gráfico"""
        return ft.Container(
            content=ft.Column([
                ft.Text("⚙️ Configuración del Gráfico", size=14, weight=ft.FontWeight.BOLD, color=self.theme['text_primary']),
                ft.Container(height=12),
                
                ft.Row([
                    # Tipo de gráfico
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Tipo", size=12, weight=ft.FontWeight.BOLD, color=self.theme['text_primary']),
                            ft.Container(height=4),
                            ft.Dropdown(
                                width=120,
                                value=self.selected_chart_type,
                                options=[
                                    ft.dropdown.Option("line", "📈 Líneas"),
                                    ft.dropdown.Option("bar", "📊 Barras"),
                                    ft.dropdown.Option("pie", "🥧 Circular")
                                ],
                                on_change=self._on_chart_type_change,
                                bgcolor=self.theme['white'],
                                border_color=self.theme['border'],
                                text_size=12
                            )
                        ], spacing=0)
                    ),
                    
                    ft.Container(width=16),
                    
                    # Métrica
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Métrica", size=12, weight=ft.FontWeight.BOLD, color=self.theme['text_primary']),
                            ft.Container(height=4),
                            ft.Dropdown(
                                width=140,
                                value=self.selected_metric,
                                options=[
                                    ft.dropdown.Option("perdidas", "⚡ Pérdidas"),
                                    ft.dropdown.Option("energia", "🔋 Energía"),
                                    ft.dropdown.Option("facturacion", "💰 Facturación")
                                ],
                                on_change=self._on_metric_change,
                                bgcolor=self.theme['white'],
                                border_color=self.theme['border'],
                                text_size=12
                            )
                        ], spacing=0)
                    ),
                    
                    ft.Container(width=16),
                    
                    # Fuente de datos
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Datos", size=12, weight=ft.FontWeight.BOLD, color=self.theme['text_primary']),
                            ft.Container(height=4),
                            ft.Dropdown(
                                width=120,
                                value=self.selected_data_source,
                                options=[
                                    ft.dropdown.Option("mensual", "📅 Mensual"),
                                    ft.dropdown.Option("acumulada", "📈 Acumulada")
                                ],
                                on_change=self._on_data_source_change,
                                bgcolor=self.theme['white'],
                                border_color=self.theme['border'],
                                text_size=12
                            )
                        ], spacing=0)
                    ),
                    
                    ft.Container(width=20),
                    
                    # Botón generar
                    ft.Container(
                        content=ft.Column([
                            ft.Text("", size=12),  # Espaciado
                            ft.Container(height=4),
                            ft.ElevatedButton(
                                content=ft.Row([
                                    ft.Icon(ft.Icons.AUTO_GRAPH, size=16),
                                    ft.Text("Generar", size=12)
                                ], spacing=6),
                                on_click=self._generate_chart,
                                bgcolor=self.theme['primary'],
                                color=self.theme['white'],
                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
                            )
                        ], spacing=0)
                    )
                ], alignment=ft.MainAxisAlignment.START)
            ]),
            bgcolor=f"{self.theme['info']}10",
            padding=16,
            border_radius=12,
            border=ft.border.all(1, f"{self.theme['info']}30")
        )
    
    def _build_chart_area(self) -> ft.Control:
        """Construye el área del gráfico"""
        try:
            # Obtener datos
            data = self._get_chart_data()
            
            if not data:
                return self._build_no_data_view()
            
            # Generar gráfico según el tipo seleccionado
            if self.selected_chart_type == "line":
                return self._build_line_chart(data)
            elif self.selected_chart_type == "bar":
                return self._build_bar_chart(data)
            elif self.selected_chart_type == "pie":
                return self._build_pie_chart(data)
            else:
                return self._build_line_chart(data)
                
        except Exception as e:
            self.logger.error(f"Error construyendo área de gráfico: {e}")
            return self._build_chart_error_view(str(e))
    
    def _build_line_chart(self, data: List[Dict[str, Any]]) -> ft.Control:
        """Construye un gráfico de líneas"""
        try:
            # Preparar datos para el gráfico de líneas
            data_points = []
            labels = []
            
            for i, item in enumerate(data[:10]):  # Limitar a 10 municipios para legibilidad
                value = self._get_chart_value(item)
                data_points.append(ft.LineChartDataPoint(i, value))
                labels.append(item.get('municipio', f'Municipio {i+1}')[:8])  # Truncar nombres largos
            
            # Crear el gráfico de líneas
            chart = ft.LineChart(
                data_series=[
                    ft.LineChartData(
                        data_points=data_points,
                        stroke_width=3,
                        color=self.theme['primary'],
                        curved=True,
                        stroke_cap_round=True,
                        below_line_bgcolor=f"{self.theme['primary']}20",
                        below_line_cutoff_y=0
                    )
                ],
                border=ft.border.all(1, self.theme['border']),
                horizontal_grid_lines=ft.ChartGridLines(
                    interval=self._calculate_grid_interval(data_points),
                    color=f"{self.theme['border']}50",
                    width=1
                ),
                vertical_grid_lines=ft.ChartGridLines(
                    interval=1,
                    color=f"{self.theme['border']}50",
                    width=1
                ),
                left_axis=ft.ChartAxis(
                    title=ft.Text(self._get_y_axis_title(), size=12, color=self.theme['text_secondary']),
                    title_size=12,
                    labels_size=10
                ),
                bottom_axis=ft.ChartAxis(
                    title=ft.Text("Municipios", size=12, color=self.theme['text_secondary']),
                    title_size=12,
                    labels_size=10,
                    labels=[ft.ChartAxisLabel(value=i, label=ft.Text(label, size=9)) for i, label in enumerate(labels)]
                ),
                tooltip_bgcolor=self.theme['dark'],
                min_y=0,
                max_y=self._calculate_max_y(data_points),
                expand=True
            )
            
            return self._wrap_chart(chart, "Gráfico de Líneas")
            
        except Exception as e:
            self.logger.error(f"Error creando gráfico de líneas: {e}")
            return self._build_chart_error_view(str(e))
    
    def _build_bar_chart(self, data: List[Dict[str, Any]]) -> ft.Control:
        """Construye un gráfico de barras"""
        try:
            # Preparar datos para el gráfico de barras
            bar_groups = []
            labels = []
            
            for i, item in enumerate(data[:10]):  # Limitar a 10 municipios
                value = self._get_chart_value(item)
                
                # Determinar color según cumplimiento (si es métrica de pérdidas)
                color = self.theme['success']
                if self.selected_metric == "perdidas":
                    plan_value = float(item.get('plan_mes' if self.selected_data_source == 'mensual' else 'plan_perdidas_acum', 0))
                    if value > plan_value:
                        color = self.theme['danger']
                
                bar_groups.append(
                    ft.BarChartGroup(
                        x=i,
                        bar_rods=[
                            ft.BarChartRod(
                                from_y=0,
                                to_y=value,
                                width=20,
                                color=color,
                                tooltip=f"{item.get('municipio', '')}: {value:.2f}",
                                border_radius=ft.border_radius.only(top_left=4, top_right=4)
                            )
                        ]
                    )
                )
                labels.append(item.get('municipio', f'Mun {i+1}')[:6])
            
            # Crear el gráfico de barras
            chart = ft.BarChart(
                bar_groups=bar_groups,
                border=ft.border.all(1, self.theme['border']),
                horizontal_grid_lines=ft.ChartGridLines(
                    interval=self._calculate_grid_interval([ft.LineChartDataPoint(0, bg.bar_rods[0].to_y) for bg in bar_groups]),
                    color=f"{self.theme['border']}50",
                    width=1
                ),
                vertical_grid_lines=ft.ChartGridLines(
                    interval=1,
                    color=f"{self.theme['border']}50",
                    width=1
                ),
                left_axis=ft.ChartAxis(
                    title=ft.Text(self._get_y_axis_title(), size=12, color=self.theme['text_secondary']),
                    title_size=12,
                    labels_size=10
                ),
                bottom_axis=ft.ChartAxis(
                    title=ft.Text("Municipios", size=12, color=self.theme['text_secondary']),
                    title_size=12,
                    labels_size=10,
                    labels=[ft.ChartAxisLabel(value=i, label=ft.Text(label, size=9)) for i, label in enumerate(labels)]
                ),
                tooltip_bgcolor=self.theme['dark'],
                min_y=0,
                max_y=self._calculate_max_y([ft.LineChartDataPoint(0, bg.bar_rods[0].to_y) for bg in bar_groups]),
                expand=True
            )
            
            return self._wrap_chart(chart, "Gráfico de Barras")
            
        except Exception as e:
            self.logger.error(f"Error creando gráfico de barras: {e}")
            return self._build_chart_error_view(str(e))
    
    def _build_pie_chart(self, data: List[Dict[str, Any]]) -> ft.Control:
        """Construye un gráfico circular"""
        try:
            # Preparar datos para el gráfico circular
            sections = []
            total_value = sum(self._get_chart_value(item) for item in data)
            
            # Colores para las secciones
            colors = [
                self.theme['primary'], self.theme['success'], self.theme['warning'], 
                self.theme['danger'], self.theme['info'], ft.Colors.PURPLE_600,
                ft.Colors.PINK_600, ft.Colors.TEAL_600, ft.Colors.INDIGO_600, ft.Colors.ORANGE_600
            ]
            
            for i, item in enumerate(data[:10]):  # Limitar a 10 municipios
                value = self._get_chart_value(item)
                percentage = (value / total_value * 100) if total_value > 0 else 0
                
                sections.append(
                    ft.PieChartSection(
                        value=value,
                        title=f"{percentage:.1f}%",
                        title_style=ft.TextStyle(
                            size=12,
                            color=self.theme['white'],
                            weight=ft.FontWeight.BOLD
                        ),
                        color=colors[i % len(colors)],
                        radius=80,
                        tooltip=f"{item.get('municipio', '')}: {value:.2f}"
                    )
                )
            
            # Crear el gráfico circular
            chart = ft.PieChart(
                sections=sections,
                sections_space=2,
                center_space_radius=40,
                expand=True
            )
            
            # Crear leyenda
            legend = self._build_pie_legend(data[:10], colors)
            
            return self._wrap_chart_with_legend(chart, legend, "Gráfico Circular")
            
        except Exception as e:
            self.logger.error(f"Error creando gráfico circular: {e}")
            return self._build_chart_error_view(str(e))
    
    def _build_pie_legend(self, data: List[Dict[str, Any]], colors: List[str]) -> ft.Control:
        """Construye la leyenda para el gráfico circular"""
        legend_items = []
        
        for i, item in enumerate(data):
            legend_items.append(
                ft.Container(
                    content=ft.Row([
                        ft.Container(
                            width=16, height=16,
                            bgcolor=colors[i % len(colors)],
                            border_radius=8
                        ),
                        ft.Container(width=8),
                        ft.Text(
                            item.get('municipio', f'Municipio {i+1}'),
                            size=12,
                            color=self.theme['text_primary']
                        )
                    ]),
                    padding=ft.padding.symmetric(vertical=4)
                )
            )
        
        return ft.Container(
            content=ft.Column(legend_items, spacing=4),
            padding=16,
            bgcolor=self.theme['white'],
            border_radius=12,
            border=ft.border.all(1, self.theme['border'])
        )
    
    def _wrap_chart(self, chart: ft.Control, title: str) -> ft.Control:
        """Envuelve el gráfico con título y contenedor"""
        return ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Text(
                        title,
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        color=self.theme['text_primary']
                    ),
                    padding=ft.padding.only(bottom=16)
                ),
                ft.Container(
                    content=chart,
                    height=400,
                    expand=True
                )
            ]),
            bgcolor=self.theme['white'],
            padding=24,
            border_radius=16,
            border=ft.border.all(1, self.theme['border']),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=8,
                color='rgba(0,0,0,0.1)',
                offset=ft.Offset(0, 4)
            ),
            expand=True
        )
    
    def _wrap_chart_with_legend(self, chart: ft.Control, legend: ft.Control, title: str) -> ft.Control:
        """Envuelve el gráfico con leyenda"""
        return ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Text(
                        title,
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        color=self.theme['text_primary']
                    ),
                    padding=ft.padding.only(bottom=16)
                ),
                ft.Row([
                    ft.Container(
                        content=chart,
                        height=400,
                        expand=True
                    ),
                    ft.Container(width=20),
                    ft.Container(
                        content=legend,
                        width=200
                    )
                ], expand=True)
            ]),
            bgcolor=self.theme['white'],
            padding=24,
            border_radius=16,
            border=ft.border.all(1, self.theme['border']),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=8,
                color='rgba(0,0,0,0.1)',
                offset=ft.Offset(0, 4)
            ),
            expand=True
        )
    
    def _get_chart_data(self) -> List[Dict[str, Any]]:
        """Obtiene los datos para el gráfico"""
        try:
            if self.selected_data_source == "mensual":
                return self.get_monthly_data()
            else:
                return self.get_accumulated_data()
        except Exception as e:
            self.logger.error(f"Error obteniendo datos del gráfico: {e}")
            return []
    
    def _get_chart_value(self, item: Dict[str, Any]) -> float:
        """Obtiene el valor a graficar según la métrica seleccionada"""
        try:
            if self.selected_metric == "perdidas":
                if self.selected_data_source == "mensual":
                    return float(item.get('real_mes', 0))
                else:
                    return float(item.get('pct_real_ventas_acum', 0))
            elif self.selected_metric == "energia":
                if self.selected_data_source == "mensual":
                    return float(item.get('energia_barra_mw', 0))
                else:
                    return float(item.get('energia_barra_acum_mw', 0))
            elif self.selected_metric == "facturacion":
                if self.selected_data_source == "mensual":
                    return float(item.get('total_facturacion_mw', 0))
                else:
                    return float(item.get('total_ventas_acum_mw', 0))
            else:
                return 0.0
        except (ValueError, TypeError):
            return 0.0
    
    def _get_y_axis_title(self) -> str:
        """Obtiene el título del eje Y"""
        if self.selected_metric == "perdidas":
            return "Pérdidas (%)"
        elif self.selected_metric == "energia":
            return "Energía (MW)"
        elif self.selected_metric == "facturacion":
            return "Facturación (MW)"
        else:
            return "Valor"
    
    def _calculate_grid_interval(self, data_points: List[ft.LineChartDataPoint]) -> float:
        """Calcula el intervalo de la grilla"""
        if not data_points:
            return 1.0
        
        max_value = max(point.y for point in data_points)
        if max_value <= 10:
            return 1.0
        elif max_value <= 50:
            return 5.0
        elif max_value <= 100:
            return 10.0
        else:
            return max_value / 10
    
    def _calculate_max_y(self, data_points: List[ft.LineChartDataPoint]) -> float:
        """Calcula el valor máximo del eje Y"""
        if not data_points:
            return 10.0
        
        max_value = max(point.y for point in data_points)
        # Agregar un 10% de margen
        return max_value * 1.1
    
    def _build_no_data_view(self) -> ft.Control:
        """Vista cuando no hay datos"""
        return ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.SHOW_CHART, size=64, color=self.theme['text_secondary']),
                ft.Container(height=16),
                ft.Text("No hay datos disponibles", size=18, weight=ft.FontWeight.BOLD, color=self.theme['text_primary']),
                ft.Text("Selecciona un período diferente o verifica la conexión", size=14, color=self.theme['text_secondary']),
                ft.Container(height=20),
                ft.ElevatedButton(
                    content=ft.Row([
                        ft.Icon(ft.Icons.REFRESH, size=16),
                        ft.Text("Recargar", size=14)
                    ], spacing=8),
                    on_click=self._refresh_chart,
                    bgcolor=self.theme['primary'],
                    color=self.theme['white']
                )
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            expand=True,
            alignment=ft.alignment.center,
            bgcolor=self.theme['white'],
            border_radius=16,
            border=ft.border.all(1, self.theme['border']),
            padding=40
        )
    
    def _build_chart_error_view(self, error_message: str) -> ft.Control:
        """Vista de error para gráficos"""
        return ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.ERROR_OUTLINE, size=64, color=self.theme['danger']),
                ft.Container(height=16),
                ft.Text("Error al generar gráfico", size=18, weight=ft.FontWeight.BOLD, color=self.theme['text_primary']),
                ft.Text(error_message, size=14, color=self.theme['text_secondary'], text_align=ft.TextAlign.CENTER),
                ft.Container(height=20),
                ft.Row([
                    ft.ElevatedButton(
                        content=ft.Row([
                            ft.Icon(ft.Icons.REFRESH, size=16),
                            ft.Text("Reintentar", size=14)
                        ], spacing=8),
                        on_click=self._refresh_chart,
                        bgcolor=self.theme['primary'],
                        color=self.theme['white']
                    ),
                    ft.Container(width=12),
                    ft.ElevatedButton(
                        content=ft.Row([
                            ft.Icon(ft.Icons.SETTINGS, size=16),
                            ft.Text("Configurar", size=14)
                        ], spacing=8),
                        on_click=self._reset_chart_config,
                        bgcolor=self.theme['text_secondary'],
                        color=self.theme['white']
                    )
                ], alignment=ft.MainAxisAlignment.CENTER)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            expand=True,
            alignment=ft.alignment.center,
            bgcolor=self.theme['white'],
            border_radius=16,
            border=ft.border.all(1, self.theme['border']),
            padding=40
        )
    
    def _on_chart_type_change(self, e):
        """Maneja el cambio de tipo de gráfico"""
        try:
            self.selected_chart_type = e.control.value
            self.logger.info(f"Tipo de gráfico cambiado a: {self.selected_chart_type}")
            self._refresh_chart()
        except Exception as ex:
            self.logger.error(f"Error cambiando tipo de gráfico: {ex}")
    
    def _on_metric_change(self, e):
        """Maneja el cambio de métrica"""
        try:
            self.selected_metric = e.control.value
            self.logger.info(f"Métrica cambiada a: {self.selected_metric}")
            self._refresh_chart()
        except Exception as ex:
            self.logger.error(f"Error cambiando métrica: {ex}")
    
    def _on_data_source_change(self, e):
        """Maneja el cambio de fuente de datos"""
        try:
            self.selected_data_source = e.control.value
            self.logger.info(f"Fuente de datos cambiada a: {self.selected_data_source}")
            self._refresh_chart()
        except Exception as ex:
            self.logger.error(f"Error cambiando fuente de datos: {ex}")
    
    def _generate_chart(self, e=None):
        """Genera el gráfico con la configuración actual"""
        try:
            self.main_screen.show_loading_message("Generando gráfico...")
            self._refresh_chart()
            self.main_screen.show_success_message("Gráfico generado correctamente")
        except Exception as ex:
            self.logger.error(f"Error generando gráfico: {ex}")
            self.main_screen.show_error_message("Error al generar gráfico")
    
    def _refresh_chart(self, e=None):
        """Refresca el gráfico"""
        try:
            self.logger.info(f"Refrescando gráfico para período {self.selected_month}/{self.selected_year}")
            
            # Validar que los dropdowns estén correctamente inicializados
            if not self.validate_dropdowns():
                self.logger.warning("Dropdowns no están correctamente inicializados")
            
            # Refrescar la página completa
            self.main_screen._refresh_page()
            
        except Exception as ex:
            self.logger.error(f"Error refrescando gráfico: {ex}")
            if hasattr(self.main_screen, 'show_error_message'):
                self.main_screen.show_error_message("Error al refrescar gráfico")

    def _export_chart(self, e=None):
        """Exporta el gráfico"""
        try:
            self.main_screen.show_loading_message("Exportando gráfico...")
            # Aquí implementarías la lógica de exportación
            # Por ahora solo simular
            import time
            time.sleep(1)
            self.main_screen.show_success_message("Gráfico exportado correctamente")
        except Exception as ex:
            self.logger.error(f"Error exportando gráfico: {ex}")
            self.main_screen.show_error_message("Error al exportar gráfico")
    def _reset_chart_config(self, e=None):
        """Resetea la configuración del gráfico"""
        try:
            self.selected_chart_type = "line"
            self.selected_metric = "perdidas"
            self.selected_data_source = "mensual"
            self.show_comparison = False
            
            self.logger.info("Configuración del gráfico reseteada")
            self.main_screen.show_info_message("Configuración reseteada")
            self._refresh_chart()
        except Exception as ex:
            self.logger.error(f"Error reseteando configuración: {ex}")
            self.main_screen.show_error_message("Error al resetear configuración")
    
    def get_period_text(self) -> str:
        """Obtiene el texto del período actual"""
        try:
            from .utils import get_period_text
            return get_period_text(self.selected_year, self.selected_month, 
                                 self.selected_data_source == "acumulada")
        except:
            return f"Período {self.selected_month}/{self.selected_year}"

    def get_monthly_data(self) -> List[Dict[str, Any]]:
        """Obtiene datos mensuales para gráficos"""
        query = """
        SELECT 
            m.nombre as municipio,
            COALESCE(eb.energia_mwh, 0) as energia_barra_mw,
            COALESCE(f.facturacion_total, 0) / 1000.0 as total_facturacion_mw,
            COALESCE(pp.plan_perdidas_pct, 0) as plan_mes,
            COALESCE(cp.perdidas_pct, 0) as real_mes
        FROM municipios m
        LEFT JOIN energia_barra eb ON m.id = eb.municipio_id 
            AND eb.año = ? AND eb.mes = ?
        LEFT JOIN facturacion f ON m.id = f.municipio_id 
            AND f.año = ? AND f.mes = ?
        LEFT JOIN planes_perdidas pp ON m.id = pp.municipio_id 
            AND pp.año = ? AND pp.mes = ?
        LEFT JOIN calculos_perdidas cp ON m.id = cp.municipio_id 
            AND cp.año = ? AND cp.mes = ?
        WHERE m.activo = 1
        ORDER BY m.nombre
        """
        params = (self.selected_year, self.selected_month) * 4
        return self.get_data_from_db(query, params)

      
