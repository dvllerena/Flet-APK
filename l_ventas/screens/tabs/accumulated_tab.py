"""
Pestaña de Pérdidas Acumuladas
"""

import flet as ft
from .base_tab import BaseTab

class AccumulatedTab(BaseTab):
    """Pestaña de análisis de pérdidas acumuladas"""
    
    def __init__(self, main_screen):
        super().__init__(main_screen)
        self.logger.info("AccumulatedTab inicializada")
    
    def build(self) -> ft.Control:
        """Construye la vista de pérdidas acumuladas"""
        try:
            return ft.Column([
                # Header con título y selector de período
                self._build_header(),
                
                ft.Container(height=20),
                
                # Tabla de datos
                ft.Container(
                    content=self._build_accumulated_table(),
                    expand=True
                )
            ], 
            scroll=ft.ScrollMode.AUTO,
            expand=True
            )
        except Exception as e:
            self.logger.error(f"Error construyendo pestaña acumulada: {e}")
            return self._build_error_view(str(e))
    
    def _build_header(self) -> ft.Control:
        """Construye el header"""
        return ft.Container(
        content=ft.Column([
            # Título principal
            ft.Row([
                ft.Container(
                    content=ft.Icon(ft.Icons.DASHBOARD, size=28, color=self.theme['white']),
                    width=50, height=50,
                    bgcolor=self.theme['primary'],
                    border_radius=25,
                    alignment=ft.alignment.center
                ),
                ft.Container(width=16),
                ft.Column([
                    ft.Text(
                        f"📊 Resumen General - {self.get_period_text()}",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color=self.theme['text_primary']
                    ),
                    ft.Text(
                        "Estado actual del sistema de pérdidas eléctricas",
                        size=14,
                        color=self.theme['text_secondary']
                    )
                ], spacing=4),
                ft.Container(expand=True),
                ft.ElevatedButton(
                    content=ft.Row([
                        ft.Icon(ft.Icons.REFRESH, size=16),
                        ft.Text("Actualizar", size=12)
                    ], spacing=6),
                    on_click=self._refresh_summary,
                    bgcolor=self.theme['primary'],
                    color=self.theme['white'],
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
                )
            ]),
            
            ft.Container(height=20),
            
            # Selector de período - CORRECCIÓN: llamar correctamente
            self.build_period_selector(self._refresh_summary)
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
    def _build_accumulated_table(self) -> ft.Control:
        """Construye la tabla de pérdidas acumuladas"""
        datos = self._get_accumulated_data()
        
        # Headers de la tabla
        headers = [
            "🏛️ Municipio",
            "⚡ Energía Barra (MW)",
            "📋 Plan Ventas (MW)",
            "📊 Plan Pérdidas (%)",
            "💰 Ventas Reales (MW)",
            "📈 Pérdidas Reales (%)",
            "💡 Ahorro (MW)"
        ]
        
        # Crear filas
        rows = []
        total_energia = 0
        total_plan_ventas = 0
        total_plan_perdidas = 0
        total_ventas = 0
        total_perdidas_reales = 0
        total_ahorro = 0
        municipios_incumplidos = 0
        
        for i, dato in enumerate(datos):
            energia = float(dato.get('energia_barra_acum_mw', 0))
            plan_ventas = float(dato.get('plan_ventas', 0))
            plan_perdidas = float(dato.get('plan_perdidas_acum', 0))
            ventas_reales = float(dato.get('total_ventas_acum_mw', 0))
            perdidas_reales = float(dato.get('pct_real_ventas_acum', 0))
            ahorro = float(dato.get('ahorro_energia', 0))
            
            # Verificar cumplimiento
            cumple_plan = perdidas_reales <= plan_perdidas
            if not cumple_plan:
                municipios_incumplidos += 1
            
            # Acumular totales
            total_energia += energia
            total_plan_ventas += plan_ventas
            total_plan_perdidas += plan_perdidas
            total_ventas += ventas_reales
            total_perdidas_reales += perdidas_reales
            total_ahorro += ahorro
            
            # Colores según cumplimiento
            municipio_color = self.theme['danger'] if not cumple_plan else self.theme['text_primary']
            perdidas_color = self.theme['danger'] if not cumple_plan else self.theme['text_primary']
            row_color = f"{self.theme['danger']}10" if not cumple_plan else (
                self.theme['light'] if i % 2 == 0 else self.theme['white']
            )
            
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(
                            dato.get('municipio', ''), 
                            size=12, 
                            weight=ft.FontWeight.BOLD if not cumple_plan else ft.FontWeight.W_500,
                            color=municipio_color
                        )),
                        ft.DataCell(ft.Text(f"{energia:.3f}", size=11, text_align=ft.TextAlign.RIGHT, color=self.theme['text_primary'])),
                        ft.DataCell(ft.Text(f"{plan_ventas:.3f}", size=11, text_align=ft.TextAlign.RIGHT, color=self.theme['text_primary'])),
                        ft.DataCell(ft.Text(f"{plan_perdidas:.2f}%", size=11, text_align=ft.TextAlign.RIGHT, color=self.theme['warning'])),
                        ft.DataCell(ft.Text(f"{ventas_reales:.3f}", size=11, text_align=ft.TextAlign.RIGHT, color=self.theme['text_primary'])),
                        ft.DataCell(ft.Text(
                            f"{perdidas_reales:.2f}%", 
                            size=11, 
                            text_align=ft.TextAlign.RIGHT,
                            weight=ft.FontWeight.BOLD if not cumple_plan else ft.FontWeight.W_500,
                            color=perdidas_color
                        )),
                        ft.DataCell(ft.Text(f"{ahorro:.3f}", size=11, text_align=ft.TextAlign.RIGHT, color=self.theme['success']))
                    ],
                    color=row_color
                )
            )
        
        # Fila de totales provinciales
        avg_plan_perdidas = total_plan_perdidas / len(datos) if datos else 0
        avg_perdidas_reales = total_perdidas_reales / len(datos) if datos else 0
        provincia_cumple = avg_perdidas_reales <= avg_plan_perdidas
        
        rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text("PROVINCIA", size=13, weight=ft.FontWeight.BOLD, color=self.theme['success'])),
                    ft.DataCell(ft.Text(f"{total_energia:.3f}", size=12, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.RIGHT, color=self.theme['success'])),
                    ft.DataCell(ft.Text(f"{total_plan_ventas:.3f}", size=12, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.RIGHT, color=self.theme['success'])),
                    ft.DataCell(ft.Text(f"{avg_plan_perdidas:.2f}%", size=12, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.RIGHT, color=self.theme['warning'])),
                    ft.DataCell(ft.Text(f"{total_ventas:.3f}", size=12, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.RIGHT, color=self.theme['success'])),
                    ft.DataCell(ft.Text(f"{avg_perdidas_reales:.2f}%", size=12, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.RIGHT, 
                                      color=self.theme['danger'] if not provincia_cumple else self.theme['success'])),
                    ft.DataCell(ft.Text(f"{total_ahorro:.3f}", size=12, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.RIGHT, color=self.theme['success']))
                ],
                color=f"{self.theme['success']}10"
            )
        )
        
        return ft.Container(
            content=ft.Column([
                # Tabla
                ft.Container(
                    content=ft.DataTable(
                        columns=[
                            ft.DataColumn(ft.Text(header, size=11, weight=ft.FontWeight.BOLD, color=self.theme['white']))
                            for header in headers
                        ],
                        rows=rows,
                        border=ft.border.all(1, self.theme['border']),
                        border_radius=12,
                        vertical_lines=ft.border.BorderSide(1, self.theme['border']),
                        horizontal_lines=ft.border.BorderSide(1, self.theme['border']),
                        heading_row_color=self.theme['success'],
                        heading_row_height=50,
                        data_row_min_height=45
                    ),
                    bgcolor=self.theme['white'],
                    border_radius=12,
                    padding=16
                ),
                
                ft.Container(height=16),
                
                # Resumen estadístico
                ft.Container(
                    content=ft.Column([
                        # Primera fila de estadísticas
                        ft.Row([
                            ft.Container(
                                content=ft.Row([
                                    ft.Icon(ft.Icons.INFO, size=18, color=self.theme['success']),
                                    ft.Container(width=8),
                                    ft.Text(
                                        f"Total: {len(datos)} municipios | Cumplen: {len(datos) - municipios_incumplidos} | Incumplen: {municipios_incumplidos}",
                                        size=12,
                                        weight=ft.FontWeight.W_500,
                                        color=self.theme['text_primary']
                                    )
                                ]),
                                bgcolor=f"{self.theme['success']}10",
                                padding=ft.padding.symmetric(horizontal=16, vertical=8),
                                border_radius=20,
                                border=ft.border.all(1, f"{self.theme['success']}30")
                            ),
                            ft.Container(expand=True),
                            ft.Container(
                                content=ft.Row([
                                    ft.Icon(
                                        ft.Icons.WARNING if municipios_incumplidos > 0 else ft.Icons.CHECK_CIRCLE,
                                        size=16,
                                        color=self.theme['danger'] if municipios_incumplidos > 0 else self.theme['success']
                                    ),
                                    ft.Container(width=6),
                                    ft.Text(
                                        f"Estado: {'ALERTA' if municipios_incumplidos > 0 else 'NORMAL'}",
                                        size=12,
                                        weight=ft.FontWeight.BOLD,
                                        color=self.theme['danger'] if municipios_incumplidos > 0 else self.theme['success']
                                    )
                                ]),
                                bgcolor=f"{self.theme['danger'] if municipios_incumplidos > 0 else self.theme['success']}10",
                                padding=ft.padding.symmetric(horizontal=12, vertical=6),
                                border_radius=15,
                                border=ft.border.all(1, f"{self.theme['danger'] if municipios_incumplidos > 0 else self.theme['success']}30")
                            )
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        
                        ft.Container(height=12),
                        
                        # Segunda fila con métricas adicionales
                        ft.Row([
                            ft.Container(
                                content=ft.Row([
                                    ft.Icon(ft.Icons.ENERGY_SAVINGS_LEAF, size=16, color=self.theme['success']),
                                    ft.Container(width=6),
                                    ft.Text(
                                        f"Ahorro Total: {total_ahorro:.2f} MW",
                                        size=11,
                                        weight=ft.FontWeight.W_600,
                                        color=self.theme['success']
                                    )
                                ]),
                                bgcolor=f"{self.theme['success']}10",
                                padding=ft.padding.symmetric(horizontal=12, vertical=6),
                                border_radius=15,
                                border=ft.border.all(1, f"{self.theme['success']}30")
                            ),
                            ft.Container(width=12),
                            ft.Container(
                                content=ft.Row([
                                    ft.Icon(ft.Icons.TRENDING_DOWN, size=16, color=self.theme['warning']),
                                    ft.Container(width=6),
                                    ft.Text(
                                        f"Pérdidas Promedio: {avg_perdidas_reales:.2f}%",
                                        size=11,
                                        weight=ft.FontWeight.W_600,
                                        color=self.theme['warning']
                                    )
                                ]),
                                bgcolor=f"{self.theme['warning']}10",
                                padding=ft.padding.symmetric(horizontal=12, vertical=6),
                                border_radius=15,
                                border=ft.border.all(1, f"{self.theme['warning']}30")
                            ),
                            ft.Container(expand=True)
                        ], alignment=ft.MainAxisAlignment.START)
                    ]),
                    padding=ft.padding.only(top=8)
                )
            ]),
            bgcolor=self.theme['white'],
            border_radius=16,
            padding=20,
            border=ft.border.all(1, self.theme['border']),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=8,
                color='rgba(0,0,0,0.05)',
                offset=ft.Offset(0, 2)
            )
        )
    
    def _get_accumulated_data(self) -> list:
        """Obtiene datos acumulados de la base de datos"""
        query = """
        SELECT 
            m.nombre as municipio,
            COALESCE(SUM(eb.energia_mwh), 0) as energia_barra_acum_mw,
            COALESCE(SUM(f.facturacion_total), 0) / 1000.0 as plan_ventas,
            COALESCE(AVG(pp.plan_perdidas_pct), 0) as plan_perdidas_acum,
            COALESCE(SUM(f.facturacion_total), 0) / 1000.0 as total_ventas_acum_mw,
            COALESCE(AVG(cp.perdidas_pct), 0) as pct_real_ventas_acum,
            COALESCE(SUM(eb.energia_mwh) - SUM(f.facturacion_total) / 1000.0, 0) as ahorro_energia
        FROM municipios m
        LEFT JOIN energia_barra eb ON m.id = eb.municipio_id 
            AND eb.año = ? AND eb.mes BETWEEN 1 AND ?
        LEFT JOIN facturacion f ON m.id = f.municipio_id 
            AND f.año = ? AND f.mes BETWEEN 1 AND ?
        LEFT JOIN planes_perdidas pp ON m.id = pp.municipio_id 
            AND pp.año = ? AND pp.mes BETWEEN 1 AND ?
        LEFT JOIN calculos_perdidas cp ON m.id = cp.municipio_id 
            AND cp.año = ? AND cp.mes BETWEEN 1 AND ?
        WHERE m.activo = 1
        GROUP BY m.id, m.nombre
        ORDER BY m.nombre
        """
        
        params = (self.selected_year, self.selected_month) * 4
        return self.get_data_from_db(query, params)
    
    def _refresh_summary(self, e=None):
        """Refresca el resumen"""
        try:
            self.logger.info(f"Refrescando resumen para período {self.selected_month}/{self.selected_year}")
            
            # Validar que los dropdowns estén correctamente inicializados
            if not self.validate_dropdowns():
                self.logger.warning("Dropdowns no están correctamente inicializados")
            
            if hasattr(self.main_screen, 'show_loading_message'):
                self.main_screen.show_loading_message("Actualizando resumen...")
            
            # Refrescar la página completa
            self.main_screen._refresh_page()
            
            if hasattr(self.main_screen, 'show_success_message'):
                self.main_screen.show_success_message("Resumen actualizado correctamente")
                
        except Exception as ex:
            self.logger.error(f"Error refrescando resumen: {ex}")
            if hasattr(self.main_screen, 'show_error_message'):
                self.main_screen.show_error_message("Error al actualizar resumen")
    def _export_to_excel(self, e):
        """Exporta datos acumulados a Excel"""
        try:
            self.logger.info("Exportando datos acumulados a Excel")
            self.main_screen.show_loading_message("Exportando datos acumulados...")
            
            # Aquí implementarías la lógica de exportación
            import time
            time.sleep(1)  # Simular proceso
            
            self.main_screen.show_success_message("Datos acumulados exportados correctamente")
        except Exception as e:
            self.logger.error(f"Error exportando datos acumulados: {e}")
            self.main_screen.show_error_message("Error al exportar datos")
    
    def _build_error_view(self, error_message: str) -> ft.Control:
        """Vista de error para esta pestaña"""
        return ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.ERROR_OUTLINE, size=48, color=self.theme['danger']),
                ft.Container(height=16),
                ft.Text("Error en Pérdidas Acumuladas", size=18, weight=ft.FontWeight.BOLD, color=self.theme['text_primary']),
                ft.Text(error_message, size=14, color=self.theme['text_secondary'])
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            expand=True,
            alignment=ft.alignment.center
        )
                
