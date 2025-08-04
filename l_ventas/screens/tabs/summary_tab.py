"""
Pestaña de Resumen General
"""

import flet as ft
from .base_tab import BaseTab

class SummaryTab(BaseTab):
    """Pestaña de resumen general con estadísticas principales"""
    
    def __init__(self, main_screen):
        super().__init__(main_screen)
        self.logger.info("SummaryTab inicializada")
    
    def build(self) -> ft.Control:
        """Construye la vista de resumen"""
        try:
            return ft.Column([
                # Header
                self._build_header(),
                
                ft.Container(height=20),
                
                # Contenido principal
                ft.Container(
                    content=ft.Column([
                        # Cards de estadísticas principales
                        self._build_main_stats(),
                        
                        ft.Container(height=24),
                        
                        # Estado provincial
                        self._build_provincial_status(),
                        
                        ft.Container(height=24),
                        
                        # Ranking de municipios
                        self._build_municipality_ranking()
                    ], scroll=ft.ScrollMode.AUTO),
                    expand=True
                )
            ], 
            expand=True
            )
        except Exception as e:
            self.logger.error(f"Error construyendo pestaña de resumen: {e}")
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
                
                # Selector de período
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
    
    def _build_main_stats(self) -> ft.Control:
        """Construye las estadísticas principales"""
        datos = self._get_summary_data()
        
        cards = [
            # Card 1: Plan vs Real
            self._create_stat_card(
                title="📋 Plan vs Real",
                main_value=f"{datos['perdidas_reales_pct']:.2f}%",
                subtitle=f"Plan: {datos['plan_promedio_pct']:.2f}%",
                status_text=f"{'Exceso' if datos['diferencia_plan_pct'] > 0 else 'Cumple'}: {abs(datos['diferencia_plan_pct']):.2f}%",
                status_color=self.theme['danger'] if datos['diferencia_plan_pct'] > 0 else self.theme['success'],
                icon=ft.Icons.TRACK_CHANGES,
                icon_color=self.theme['warning']
            ),
            
            # Card 2: Energía Total
            self._create_stat_card(
                title="⚡ Energía Total",
                main_value=f"{datos['total_energia_mw']:.1f} MW",
                subtitle=f"Ventas: {datos['total_ventas_mw']:.1f} MW",
                status_text=f"Ahorro: {datos['total_ahorro_mw']:.1f} MW",
                status_color=self.theme['success'],
                icon=ft.Icons.BOLT,
                icon_color=self.theme['primary']
            ),
            
            # Card 3: Estado Municipios
            self._create_stat_card(
                title="🏛️ Municipios",
                main_value=f"{datos['municipios_cumplidos']}/{datos['total_municipios']}",
                subtitle="Cumplen el plan",
                status_text=f"{'Incumplen' if datos['municipios_incumplidos'] > 0 else 'Todos OK'}: {datos['municipios_incumplidos']}",
                status_color=self.theme['danger'] if datos['municipios_incumplidos'] > 0 else self.theme['success'],
                icon=ft.Icons.LOCATION_CITY,
                icon_color=self.theme['success']
            ),
            
            # Card 4: Pérdidas MW
            self._create_stat_card(
                title="📉 Pérdidas MW",
                main_value=f"{datos['perdidas_reales_mw']:.1f} MW",
                subtitle=f"Plan: {datos['plan_perdidas_mw']:.1f} MW",
                status_text=f"{'Exceso' if datos['diferencia_plan_mw'] > 0 else 'Ahorro'}: {abs(datos['diferencia_plan_mw']):.1f} MW",
                status_color=self.theme['danger'] if datos['diferencia_plan_mw'] > 0 else self.theme['success'],
                icon=ft.Icons.TRENDING_DOWN,
                icon_color=self.theme['warning']
            )
        ]
        
        return ft.Container(
            content=ft.GridView(
                controls=cards,
                runs_count=2,
                max_extent=350,
                child_aspect_ratio=1.8,
                spacing=20,
                run_spacing=20,
                padding=ft.padding.all(10)
            ),
            height=320
        )
    
    def _create_stat_card(self, title, main_value, subtitle, status_text, status_color, icon, icon_color):
        """Crea una tarjeta de estadística"""
        return ft.Container(
            content=ft.Column([
                # Header con icono y título
                ft.Row([
                    ft.Container(
                        content=ft.Icon(icon, size=24, color=self.theme['white']),
                        width=45, height=45,
                        bgcolor=icon_color,
                        border_radius=22.5,
                        alignment=ft.alignment.center
                    ),
                    ft.Container(width=12),
                    ft.Column([
                        ft.Text(title, size=14, weight=ft.FontWeight.BOLD, color=self.theme['text_primary']),
                        ft.Text(subtitle, size=12, color=self.theme['text_secondary'])
                    ], spacing=2)
                ]),
                
                ft.Container(height=12),
                
                # Valor principal
                ft.Text(
                    main_value,
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=self.theme['text_primary']
                ),
                
                ft.Container(height=8),
                
                # Estado
                ft.Container(
                    content=ft.Text(
                        status_text,
                        size=11,
                        weight=ft.FontWeight.BOLD,
                        color=status_color
                    ),
                    bgcolor=f"{status_color}15",
                    padding=ft.padding.symmetric(horizontal=10, vertical=4),
                    border_radius=12
                )
            ]),
            bgcolor=self.theme['white'],
            padding=20,
            border_radius=15,
            border=ft.border.all(1, self.theme['border']),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=4,
                color='rgba(0,0,0,0.1)',
                offset=ft.Offset(0, 2)
            ),
            width=320,
            height=140
        )
    
    def _build_provincial_status(self) -> ft.Control:
        """Construye el indicador de estado provincial"""
        datos = self._get_summary_data()
        
        estado_color = self.theme['danger'] if datos['estado_general'] == 'ALERTA' else self.theme['success']
        estado_bg = f"{estado_color}15"
        estado_icon = ft.Icons.WARNING if datos['estado_general'] == 'ALERTA' else ft.Icons.CHECK_CIRCLE
        
        return ft.Container(
            content=ft.Column([
                ft.Text("🎯 Estado Provincial", size=18, weight=ft.FontWeight.BOLD, color=self.theme['text_primary']),
                ft.Container(height=16),
                
                ft.Container(
                    content=ft.Row([
                        # Indicador visual
                        ft.Container(
                            content=ft.Icon(estado_icon, size=48, color=estado_color),
                            width=80, height=80,
                            bgcolor=estado_bg,
                            border_radius=40,
                            alignment=ft.alignment.center,
                            border=ft.border.all(3, estado_color)
                        ),
                        
                        ft.Container(width=24),
                        
                        # Información principal
                        ft.Column([
                            ft.Text(
                                f"ESTADO: {datos['estado_general']}",
                                size=24,
                                weight=ft.FontWeight.BOLD,
                                color=estado_color
                            ),
                            ft.Container(height=8),
                            ft.Text(
                                f"Período: {datos['periodo_actual']}",
                                size=14,
                                color=self.theme['text_secondary']
                            ),
                            ft.Container(height=4),
                            ft.Text(
                                f"Pérdidas: {datos['perdidas_reales_pct']:.2f}% (Plan: {datos['plan_promedio_pct']:.2f}%)",
                                size=14,
                                color=self.theme['text_primary'],
                                weight=ft.FontWeight.W_500
                            )
                        ], spacing=0),
                        
                        ft.Container(expand=True),
                        
                        # Medidor de cumplimiento
                        ft.Container(
                            content=ft.Column([
                                ft.Text("Cumplimiento", size=12, weight=ft.FontWeight.BOLD, color=self.theme['text_primary']),
                                ft.Container(height=8),
                                ft.Container(
                                    content=ft.Text(
                                        f"{((datos['municipios_cumplidos'] / datos['total_municipios']) * 100):.0f}%",
                                        size=18,
                                        weight=ft.FontWeight.BOLD,
                                        color=estado_color
                                    ),
                                    width=60, height=60,
                                    bgcolor=estado_bg,
                                    border_radius=30,
                                    alignment=ft.alignment.center,
                                    border=ft.border.all(2, estado_color)
                                )
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            padding=16
                        )
                    ], alignment=ft.MainAxisAlignment.START),
                    bgcolor=self.theme['white'],
                    padding=24,
                    border_radius=16,
                    border=ft.border.all(1, self.theme['border']),
                    shadow=ft.BoxShadow(
                        spread_radius=0,
                        blur_radius=6,
                        color='rgba(0,0,0,0.1)',
                        offset=ft.Offset(0, 3)
                    )
                )
            ])
        )
    
    def _build_municipality_ranking(self) -> ft.Control:
        """Construye el ranking de municipios"""
        datos = self._get_summary_data()
        
        # Combinar y ordenar municipios
        todos_municipios = datos['lista_incumplidos'] + datos['lista_cumplidos']
        todos_municipios.sort(key=lambda x: x['diferencia'], reverse=True)
        
        # Top 5 peores y mejores
        peores_5 = todos_municipios[:5]
        mejores_5 = todos_municipios[-5:]
        mejores_5.reverse()
        
        return ft.Container(
            content=ft.Column([
                ft.Text("📊 Ranking de Municipios", size=18, weight=ft.FontWeight.BOLD, color=self.theme['text_primary']),
                ft.Container(height=16),
                
                ft.Row([
                    # Columna de peores
                    ft.Container(
                        content=ft.Column([
                            ft.Container(
                                content=ft.Text("🔴 Mayor Incumplimiento", size=14, weight=ft.FontWeight.BOLD, color=self.theme['danger']),
                                bgcolor=f"{self.theme['danger']}15",
                                padding=ft.padding.symmetric(horizontal=16, vertical=8),
                                border_radius=8,
                                alignment=ft.alignment.center
                            ),
                            ft.Container(height=12),
                            ft.Column([
                                self._create_ranking_item(i+1, mun, self.theme['danger'])
                                for i, mun in enumerate(peores_5)
                            ], spacing=8)
                        ]),
                        expand=True,
                        bgcolor=self.theme['white'],
                        padding=16,
                        border_radius=12,
                        border=ft.border.all(1, f"{self.theme['danger']}30")
                    ),
                    
                    ft.Container(width=20),
                    
                    # Columna de mejores
                    ft.Container(
                        content=ft.Column([
                            ft.Container(
                                content=ft.Text("🟢 Mejor Cumplimiento", size=14, weight=ft.FontWeight.BOLD, color=self.theme['success']),
                                bgcolor=f"{self.theme['success']}15",
                                padding=ft.padding.symmetric(horizontal=16, vertical=8),
                                border_radius=8,
                                alignment=ft.alignment.center
                            ),
                            ft.Container(height=12),
                            ft.Column([
                                self._create_ranking_item(i+1, mun, self.theme['success'])
                                for i, mun in enumerate(mejores_5)
                            ], spacing=8)
                        ]),
                        expand=True,
                        bgcolor=self.theme['white'],
                        padding=16,
                        border_radius=12,
                        border=ft.border.all(1, f"{self.theme['success']}30")
                    )
                ], spacing=0)
            ]),
            bgcolor=self.theme['white'],
            padding=20,
            border_radius=16,
            border=ft.border.all(1, self.theme['border']),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=6,
                color='rgba(0,0,0,0.05)',
                offset=ft.Offset(0, 2)
            )
        )
    
    def _create_ranking_item(self, position, municipio, color):
        """Crea un item del ranking"""
        return ft.Container(
            content=ft.Row([
                # Posición
                ft.Container(
                    content=ft.Text(f"{position}", size=12, weight=ft.FontWeight.BOLD, color=self.theme['white']),
                    width=28, height=28,
                    bgcolor=color,
                    border_radius=14,
                    alignment=ft.alignment.center
                ),
                ft.Container(width=12),
                # Información
                ft.Column([
                    ft.Text(municipio['municipio'], size=12, weight=ft.FontWeight.BOLD, color=self.theme['text_primary']),
                    ft.Text(f"Plan: {municipio['plan']:.1f}% | Real: {municipio['real']:.1f}%", size=10, color=self.theme['text_secondary'])
                ], spacing=2),
                ft.Container(expand=True),
                # Diferencia
                ft.Container(
                    content=ft.Text(
                        f"{municipio['diferencia']:+.1f}%",
                        size=11,
                        weight=ft.FontWeight.BOLD,
                        color=color
                    ),
                    bgcolor=f"{color}15",
                    padding=ft.padding.symmetric(horizontal=8, vertical=4),
                    border_radius=8
                )
            ]),
            bgcolor=f"{color}05",
            padding=12,
            border_radius=8,
            border=ft.border.all(1, f"{color}20")
        )
    
    def _get_summary_data(self) -> dict:
        """Obtiene datos para el resumen"""
        try:
            # Obtener datos acumulados
            datos_acumulados = self._get_accumulated_summary_data()
            
            # Calcular estadísticas
            total_energia = sum(float(d.get('energia_barra_acum_mw', 0)) for d in datos_acumulados)
            total_ventas = sum(float(d.get('total_ventas_acum_mw', 0)) for d in datos_acumulados)
            total_ahorro = sum(float(d.get('ahorro_energia', 0)) for d in datos_acumulados)
            
            # Calcular pérdidas
            perdidas_reales_mw = total_energia - total_ventas
            perdidas_reales_pct = (perdidas_reales_mw / total_energia * 100) if total_energia > 0 else 0
            
            # Plan promedio
            plan_promedio = sum(float(d.get('plan_perdidas_acum', 0)) for d in datos_acumulados) / len(datos_acumulados) if datos_acumulados else 0
            plan_perdidas_mw = total_energia * (plan_promedio / 100)
            
            # Diferencias
            diferencia_plan_mw = perdidas_reales_mw - plan_perdidas_mw
            diferencia_plan_pct = perdidas_reales_pct - plan_promedio
            
            # Clasificar municipios
            municipios_incumplidos = []
            municipios_cumplidos = []
            
            for dato in datos_acumulados:
                municipio = dato.get('municipio', '')
                plan = float(dato.get('plan_perdidas_acum', 0))
                real = float(dato.get('pct_real_ventas_acum', 0))
                diferencia = real - plan
                
                municipio_data = {
                    'municipio': municipio,
                    'plan': plan,
                    'real': real,
                    'diferencia': diferencia,
                    'energia': float(dato.get('energia_barra_acum_mw', 0))
                }
                
                if real > plan:
                    municipios_incumplidos.append(municipio_data)
                else:
                    municipios_cumplidos.append(municipio_data)
            
            # Ordenar
            municipios_incumplidos.sort(key=lambda x: x['diferencia'], reverse=True)
            municipios_cumplidos.sort(key=lambda x: x['diferencia'])
            
            # Obtener período
            meses_nombres = ["", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
            
            return {
                'periodo_actual': f"Enero a {meses_nombres[self.selected_month]} {self.selected_year}",
                'total_municipios': len(datos_acumulados),
                'municipios_incumplidos': len(municipios_incumplidos),
                'municipios_cumplidos': len(municipios_cumplidos),
                'total_energia_mw': total_energia,
                'total_ventas_mw': total_ventas,
                'total_ahorro_mw': total_ahorro,
                'perdidas_reales_mw': perdidas_reales_mw,
                'perdidas_reales_pct': perdidas_reales_pct,
                'plan_promedio_pct': plan_promedio,
                'plan_perdidas_mw': plan_perdidas_mw,
                'diferencia_plan_mw': diferencia_plan_mw,
                'diferencia_plan_pct': diferencia_plan_pct,
                'lista_incumplidos': municipios_incumplidos,
                'lista_cumplidos': municipios_cumplidos,
                'estado_general': 'ALERTA' if len(municipios_incumplidos) > 0 else 'NORMAL'
            }
            
        except Exception as e:
            self.logger.error(f"Error obteniendo datos de resumen: {e}")
            return self._get_default_summary_data()
    
    def _get_accumulated_summary_data(self):
        """Obtiene datos acumulados para el resumen"""
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
    
    def _get_default_summary_data(self):
        """Datos por defecto para el resumen"""
        from datetime import datetime
        current_date = datetime.now()
        
        return {
            'periodo_actual': f"Enero a {current_date.strftime('%B')} {current_date.year}",
            'total_municipios': 13,
            'municipios_incumplidos': 0,
            'municipios_cumplidos': 13,
            'total_energia_mw': 0.0,
            'total_ventas_mw': 0.0,
            'total_ahorro_mw': 0.0,
            'perdidas_reales_mw': 0.0,
            'perdidas_reales_pct': 0.0,
            'plan_promedio_pct': 0.0,
            'plan_perdidas_mw': 0.0,
            'diferencia_plan_mw': 0.0,
            'diferencia_plan_pct': 0.0,
            'lista_incumplidos': [],
            'lista_cumplidos': [],
            'estado_general': 'NORMAL'
        }
    
    def _refresh_summary(self, e=None):
        """Refresca el resumen"""
        try:
            self.main_screen.show_loading_message("Actualizando resumen...")
            self.main_screen._refresh_page()
            self.main_screen.show_success_message("Resumen actualizado correctamente")
        except Exception as ex:
            self.logger.error(f"Error refrescando resumen: {ex}")
            self.main_screen.show_error_message("Error al actualizar resumen")
    
    def _build_error_view(self, error_message: str) -> ft.Control:
        """Vista de error para esta pestaña"""
        return ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.ERROR_OUTLINE, size=48, color=self.theme['danger']),
                ft.Container(height=16),
                ft.Text("Error en Resumen", size=18, weight=ft.FontWeight.BOLD, color=self.theme['text_primary']),
                ft.Text(error_message, size=14, color=self.theme['text_secondary'])
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            expand=True,
            alignment=ft.alignment.center
        )
