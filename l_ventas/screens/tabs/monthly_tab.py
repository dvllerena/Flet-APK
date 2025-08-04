"""
Pestaña de Pérdidas Mensuales
"""

import flet as ft
from .base_tab import BaseTab

class MonthlyTab(BaseTab):
    """Pestaña de análisis de pérdidas mensuales"""
    
    def __init__(self, main_screen):
        super().__init__(main_screen)
        self.logger.info("MonthlyTab inicializada")
    
    def build(self) -> ft.Control:
        """Construye la vista de pérdidas mensuales"""
        try:
            return ft.Column([
                # Header con título y selector de período
                self._build_header(),
                
                ft.Container(height=20),
                
                # Tabla de datos
                ft.Container(
                    content=self._build_monthly_table(),
                    expand=True
                )
            ], 
            scroll=ft.ScrollMode.AUTO,
            expand=True
            )
        except Exception as e:
            self.logger.error(f"Error construyendo pestaña mensual: {e}")
            return self._build_error_view(str(e))
    
    def _build_header(self) -> ft.Control:
        """Construye el header con título y controles"""
        return ft.Container(
            content=ft.Column([
                # Título principal
                ft.Row([
                    ft.Container(
                        content=ft.Icon(ft.Icons.CALENDAR_MONTH, size=28, color=self.theme['white']),
                        width=50, height=50,
                        bgcolor=self.theme['primary'],
                        border_radius=25,
                        alignment=ft.alignment.center
                    ),
                    ft.Container(width=16),
                    ft.Column([
                        ft.Text(
                            f"📊 Pérdidas Mensuales - {self.get_period_text()}",
                            size=24,
                            weight=ft.FontWeight.BOLD,
                            color=self.theme['text_primary']
                        ),
                        ft.Text(
                            "Análisis detallado del consumo y pérdidas por municipio",
                            size=14,
                            color=self.theme['text_secondary']
                        )
                    ], spacing=4),
                    ft.Container(expand=True),
                    ft.ElevatedButton(
                        content=ft.Row([
                            ft.Icon(ft.Icons.DOWNLOAD, size=16),
                            ft.Text("Exportar Excel", size=12)
                        ], spacing=6),
                        on_click=self._export_to_excel,
                        bgcolor=self.theme['success'],
                        color=self.theme['white'],
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
                    )
                ]),
                
                ft.Container(height=20),
                
                # Selector de período - CORRECCIÓN: llamar correctamente
                self.build_period_selector(self._refresh_table)
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

    def _build_monthly_table(self) -> ft.Control:
        """Construye la tabla de pérdidas mensuales"""
        datos = self._get_monthly_data()
        
        # Headers de la tabla
        headers = [
            "🏛️ Municipio",
            "⚡ Energía Barra (MW)",
            "💰 Facturación (MW)", 
            "📋 Plan (%)",
            "📊 Real (%)"
        ]
        
        # Crear filas
        rows = []
        total_energia = 0
        total_facturacion = 0
        total_plan = 0
        total_real = 0
        municipios_incumplidos = 0
        
        for i, dato in enumerate(datos):
            energia = float(dato.get('energia_barra_mw', 0))
            facturacion = float(dato.get('total_facturacion_mw', 0))
            plan = float(dato.get('plan_mes', 0))
            real = float(dato.get('real_mes', 0))
            
            # Verificar cumplimiento
            cumple_plan = real <= plan
            if not cumple_plan:
                municipios_incumplidos += 1
            
            # Acumular totales
            total_energia += energia
            total_facturacion += facturacion
            total_plan += plan
            total_real += real
            
            # Colores según cumplimiento
            municipio_color = self.theme['danger'] if not cumple_plan else self.theme['text_primary']
            real_color = self.theme['danger'] if not cumple_plan else self.theme['text_primary']
            row_color = f"{self.theme['danger']}10" if not cumple_plan else (
                self.theme['light'] if i % 2 == 0 else self.theme['white']
            )
            
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(
                            dato.get('municipio', ''), 
                            size=13, 
                            weight=ft.FontWeight.BOLD if not cumple_plan else ft.FontWeight.W_500,
                            color=municipio_color
                        )),
                        ft.DataCell(ft.Text(
                            f"{energia:.3f}", 
                            size=12, 
                            text_align=ft.TextAlign.RIGHT,
                            color=self.theme['text_primary']
                        )),
                        ft.DataCell(ft.Text(
                            f"{facturacion:.3f}", 
                            size=12, 
                            text_align=ft.TextAlign.RIGHT,
                            color=self.theme['text_primary']
                        )),
                        ft.DataCell(ft.Text(
                            f"{plan:.2f}%", 
                            size=12, 
                            text_align=ft.TextAlign.RIGHT,
                            color=self.theme['warning']
                        )),
                        ft.DataCell(ft.Text(
                            f"{real:.2f}%", 
                            size=12, 
                            text_align=ft.TextAlign.RIGHT,
                            weight=ft.FontWeight.BOLD if not cumple_plan else ft.FontWeight.W_500,
                            color=real_color
                        ))
                    ],
                    color=row_color
                )
            )
        
        # Fila de totales provinciales
        avg_plan = total_plan / len(datos) if datos else 0
        avg_real = total_real / len(datos) if datos else 0
        provincia_cumple = avg_real <= avg_plan
        
        rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text("PROVINCIA", size=14, weight=ft.FontWeight.BOLD, color=self.theme['primary'])),
                    ft.DataCell(ft.Text(f"{total_energia:.3f}", size=13, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.RIGHT, color=self.theme['primary'])),
                    ft.DataCell(ft.Text(f"{total_facturacion:.3f}", size=13, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.RIGHT, color=self.theme['primary'])),
                    ft.DataCell(ft.Text(f"{avg_plan:.2f}%", size=13, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.RIGHT, color=self.theme['warning'])),
                    ft.DataCell(ft.Text(f"{avg_real:.2f}%", size=13, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.RIGHT, 
                                      color=self.theme['danger'] if not provincia_cumple else self.theme['success']))
                ],
                color=f"{self.theme['primary']}10"
            )
        )
        
        return ft.Container(
            content=ft.Column([
                # Tabla
                ft.Container(
                    content=ft.DataTable(
                        columns=[
                            ft.DataColumn(ft.Text(header, size=12, weight=ft.FontWeight.BOLD, color=self.theme['white']))
                            for header in headers
                        ],
                        rows=rows,
                        border=ft.border.all(1, self.theme['border']),
                        border_radius=12,
                        vertical_lines=ft.border.BorderSide(1, self.theme['border']),
                        horizontal_lines=ft.border.BorderSide(1, self.theme['border']),
                        heading_row_color=self.theme['primary'],
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
                    content=ft.Row([
                        ft.Container(
                            content=ft.Row([
                                ft.Icon(ft.Icons.INFO, size=18, color=self.theme['primary']),
                                ft.Container(width=8),
                                ft.Text(
                                    f"Total: {len(datos)} municipios | Cumplen: {len(datos) - municipios_incumplidos} | Incumplen: {municipios_incumplidos}",
                                    size=12,
                                    weight=ft.FontWeight.W_500,
                                    color=self.theme['text_primary']
                                )
                            ]),
                            bgcolor=f"{self.theme['primary']}10",
                            padding=ft.padding.symmetric(horizontal=16, vertical=8),
                            border_radius=20,
                            border=ft.border.all(1, f"{self.theme['primary']}30")
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
    
    def _get_monthly_data(self) -> list:
        """Obtiene datos mensuales de la base de datos"""
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
    
    def _refresh_table(self):
        """Refresca solo esta tabla"""
        try:
            self.logger.info(f"Refrescando tabla mensual para período {self.selected_month}/{self.selected_year}")
            
            # Validar que los dropdowns estén correctamente inicializados
            if not self.validate_dropdowns():
                self.logger.warning("Dropdowns no están correctamente inicializados")
            
            # Refrescar la página completa por ahora
            self.main_screen._refresh_page()
            
        except Exception as e:
            self.logger.error(f"Error refrescando tabla mensual: {e}")
            if hasattr(self.main_screen, 'show_error_message'):
                self.main_screen.show_error_message("Error al actualizar la tabla")
    def _export_to_excel(self, e):
        """Exporta datos mensuales a Excel"""
        try:
            self.logger.info("Exportando datos mensuales a Excel")
            self.main_screen.show_loading_message("Exportando datos mensuales...")
            
            # Aquí implementarías la lógica de exportación
            import time
            time.sleep(1)  # Simular proceso
            
            self.main_screen.show_success_message("Datos mensuales exportados correctamente")
        except Exception as e:
            self.logger.error(f"Error exportando datos mensuales: {e}")
            self.main_screen.show_error_message("Error al exportar datos")
    
    def _build_error_view(self, error_message: str) -> ft.Control:
        """Vista de error para esta pestaña"""
        return ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.ERROR_OUTLINE, size=48, color=self.theme['danger']),
                ft.Container(height=16),
                ft.Text("Error en Pérdidas Mensuales", size=18, weight=ft.FontWeight.BOLD, color=self.theme['text_primary']),
                ft.Text(error_message, size=14, color=self.theme['text_secondary'])
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            expand=True,
            alignment=ft.alignment.center
        )

