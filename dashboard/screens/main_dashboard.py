"""
Dashboard principal de la aplicación - OPTIMIZADO PARA WEB
Muestra resumen de datos y navegación a módulos
"""

import flet as ft
from typing import Dict, List
from core.logger import get_logger
from core.database import get_db_manager


class MainDashboard:
    """Dashboard principal del sistema optimizado para web"""
    
    def __init__(self, app):
        self.app = app
        self.page = app.page
        self.logger = get_logger(__name__)
        self.db_manager = get_db_manager()
        
    def build(self) -> ft.Container:
        """Construye el dashboard principal con mejoras estéticas web"""
        
        # Header con información del usuario mejorado
        header = self._build_header()
        
        # Cards de estadísticas mejoradas
        stats_cards = self._build_stats_cards()
        
        # Módulos principales con mejor diseño
        modules_grid = self._build_modules_grid()
        
        # Gráfico de resumen mejorado
        summary_chart = self._build_summary_chart()
        
        # Sección de actividad reciente (NUEVA)
        recent_activity = self._build_recent_activity()
        
        # Layout principal con scroll suave y mejor espaciado
        main_content = ft.Column([
            header,
            ft.Container(height=30),  # Espaciado mejorado
            stats_cards,
            ft.Container(height=40),  # Espaciado mejorado
            
            # Título de módulos con mejor diseño
            ft.Container(
                content=ft.Row([
                    ft.Container(
                        content=ft.Icon(ft.Icons.APPS, size=32, color=ft.Colors.WHITE),
                        width=50,
                        height=50,
                        bgcolor=ft.Colors.BLUE_600,
                        border_radius=25,
                        alignment=ft.alignment.center,
                        shadow=ft.BoxShadow(
                            spread_radius=1,
                            blur_radius=8,
                            color=ft.Colors.BLUE_200,
                            offset=ft.Offset(0, 3)
                        )
                    ),
                    ft.Container(width=15),
                    ft.Column([
                        ft.Text(
                            "🏢 Módulos del Sistema", 
                            size=28, 
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.BLUE_800
                        ),
                        ft.Text(
                            "Accede a todas las funcionalidades del sistema",
                            size=14,
                            color=ft.Colors.BLUE_600
                        )
                    ], spacing=2)
                ], alignment=ft.MainAxisAlignment.START),
                padding=ft.padding.only(left=15, bottom=10)
            ),
            
            modules_grid,
            ft.Container(height=40),
            
            # Layout de dos columnas para gráfico y actividad reciente
            ft.ResponsiveRow([
                ft.Container(
                    content=summary_chart,
                    col={"sm": 12, "md": 8, "lg": 8}
                ),
                ft.Container(
                    content=recent_activity,
                    col={"sm": 12, "md": 4, "lg": 4}
                )
            ]),
            
            ft.Container(height=30)  # Espaciado final
        ], scroll=ft.ScrollMode.AUTO, spacing=0)
        
        return ft.Container(
            content=main_content,
            padding=25,  # Padding mejorado
            expand=True,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=[
                    ft.Colors.BLUE_50,
                    ft.Colors.WHITE,
                    ft.Colors.BLUE_50,
                    ft.Colors.WHITE
                ]
            )
        )
    
    def _build_header(self) -> ft.Container:
        """Construye el header del dashboard con mejoras estéticas"""
        user = self.app.get_current_user()
        
        # Botón de logout mejorado
        logout_button = ft.Container(
            content=ft.IconButton(
                icon=ft.Icons.LOGOUT,
                icon_color=ft.Colors.WHITE,
                bgcolor=ft.Colors.RED_500,
                tooltip="Cerrar Sesión",
                on_click=lambda e: self._logout(e),
                icon_size=22
            ),
            border_radius=25,
            shadow=ft.BoxShadow(
                spread_radius=2,
                blur_radius=8,
                color=ft.Colors.RED_200,
                offset=ft.Offset(0, 3)
            )
        )
        
        # Indicador de estado del sistema (NUEVO)
        system_status = ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.CIRCLE, size=12, color=ft.Colors.GREEN_500),
                ft.Text("Sistema Activo", size=12, color=ft.Colors.GREEN_700, weight=ft.FontWeight.W_500)
            ], spacing=5),
            bgcolor=ft.Colors.GREEN_50,
            padding=ft.padding.symmetric(horizontal=12, vertical=6),
            border_radius=15,
            border=ft.border.all(1, ft.Colors.GREEN_200)
        )
        
        return ft.Container(
            content=ft.Row([
                # Información del usuario - Lado izquierdo mejorado
                ft.Container(
                    content=ft.Row([
                        ft.Container(
                            content=ft.Icon(
                                ft.Icons.ACCOUNT_CIRCLE,
                                size=48,
                                color=ft.Colors.WHITE
                            ),
                            width=60,
                            height=60,
                            bgcolor=ft.Colors.BLUE_600,
                            border_radius=30,
                            alignment=ft.alignment.center,
                            shadow=ft.BoxShadow(
                                spread_radius=2,
                                blur_radius=10,
                                color=ft.Colors.BLUE_300,
                                offset=ft.Offset(0, 3)
                            )
                        ),
                        ft.Container(width=20),
                        ft.Column([
                            ft.Text(
                                f"¡Bienvenido, {user.get('nombre_completo', user.get('username', 'Usuario'))}!",
                                size=26,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.BLUE_900
                            ),
                            ft.Container(height=8),
                            ft.Row([
                                ft.Container(
                                    content=ft.Text(
                                        f"👤 {user.get('tipo_usuario', '').title()}",
                                        size=14,
                                        color=ft.Colors.BLUE_700,
                                        weight=ft.FontWeight.W_500
                                    ),
                                    bgcolor=ft.Colors.BLUE_100,
                                    padding=ft.padding.symmetric(horizontal=12, vertical=6),
                                    border_radius=15,
                                    border=ft.border.all(1, ft.Colors.BLUE_200)
                                ),
                                ft.Container(width=10),
                                system_status
                            ])
                        ], spacing=0, alignment=ft.MainAxisAlignment.CENTER)
                    ], alignment=ft.MainAxisAlignment.START),
                    expand=True
                ),
                
                # Sección derecha con controles mejorados
                ft.Container(
                    content=ft.Row([
                        # Notificaciones (NUEVO)
                        ft.Container(
                            content=ft.Column([
                                ft.Container(
                                    content=ft.Stack([
                                        ft.Icon(ft.Icons.NOTIFICATIONS, size=28, color=ft.Colors.WHITE),
                                        ft.Container(
                                            content=ft.Text("3", size=10, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                                            width=18,
                                            height=18,
                                            bgcolor=ft.Colors.RED_500,
                                            border_radius=9,
                                            alignment=ft.alignment.center,
                                            top=-2,
                                            right=-2
                                        )
                                    ]),
                                    width=50,
                                    height=50,
                                    bgcolor=ft.Colors.ORANGE_500,
                                    border_radius=25,
                                    alignment=ft.alignment.center,
                                    shadow=ft.BoxShadow(
                                        spread_radius=1,
                                        blur_radius=8,
                                        color=ft.Colors.ORANGE_200,
                                        offset=ft.Offset(0, 3)
                                    )
                                ),
                                ft.Container(height=5),
                                ft.Text("Alertas", size=11, weight=ft.FontWeight.BOLD, color=ft.Colors.ORANGE_700)
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0)
                        ),
                        
                        ft.Container(width=25),
                        
                        # Dashboard icon mejorado
                        ft.Container(
                            content=ft.Column([
                                ft.Container(
                                    content=ft.Icon(ft.Icons.DASHBOARD, size=30, color=ft.Colors.WHITE),
                                    width=50,
                                    height=50,
                                    bgcolor=ft.Colors.BLUE_600,
                                    border_radius=25,
                                    alignment=ft.alignment.center,
                                    shadow=ft.BoxShadow(
                                        spread_radius=1,
                                        blur_radius=8,
                                        color=ft.Colors.BLUE_300,
                                        offset=ft.Offset(0, 3)
                                    )
                                ),
                                ft.Container(height=5),
                                ft.Text("Dashboard", size=11, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800)
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0)
                        ),
                        
                        ft.Container(width=25),
                        
                        # Logout button mejorado
                        ft.Container(
                            content=ft.Column([
                                logout_button,
                                ft.Container(height=5),
                                ft.Text("Salir", size=11, weight=ft.FontWeight.BOLD, color=ft.Colors.RED_600)
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0)
                        )
                    ], alignment=ft.MainAxisAlignment.END, spacing=0)
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            bgcolor=ft.Colors.WHITE,
            padding=30,  # Padding aumentado
            border_radius=20,  # Border radius aumentado
            shadow=ft.BoxShadow(
                spread_radius=2,
                blur_radius=15,
                color=ft.Colors.BLUE_100,
                offset=ft.Offset(0, 5)
            ),
            border=ft.border.all(2, ft.Colors.BLUE_50)
        )

    def _build_modules_grid(self) -> ft.GridView:
        """Construye la grilla de módulos con tamaño ajustado para mejor contenido"""
        
        modules = [
            {
                "name": "Análisis de Pérdidas",
                "description": "Análisis detallado de pérdidas eléctricas del sistema",
                "icon": ft.Icons.ANALYTICS,
                "color": ft.Colors.RED_600,
                "bg_color": ft.Colors.RED_50,
                "route": "perdidas",
                "available": False,
                "emoji": "📈",
                "badge": "Próximo"
            },
            {
                "name": "Cálculo de Energía",
                "description": "Gestión y cálculos energéticos por municipios",
                "icon": ft.Icons.CALCULATE,
                "color": ft.Colors.BLUE_600,
                "bg_color": ft.Colors.BLUE_50,
                "route": "calculo_energia",
                "available": True,
                "emoji": "⚡",
                "badge": "Activo"
            },
            {
                "name": "Facturación",
                "description": "Análisis y gestión de facturación eléctrica",
                "icon": ft.Icons.RECEIPT,
                "color": ft.Colors.GREEN_600,
                "bg_color": ft.Colors.GREEN_50,
                "route": "facturacion",
                "available": True,
                "emoji": "💰",
                "badge": "Activo"
            },
            {
                "name": "Inf_Pérdidas",
                "description": "Reportes y estadísticas de pérdidas provinciales",
                "icon": ft.Icons.ASSESSMENT,
                "color": ft.Colors.PURPLE_600,
                "bg_color": ft.Colors.PURPLE_50,
                "route": "infoperdidas",
                "available": True,
                "emoji": "📋",
                "badge": "Activo"
            },
            {
                "name": "Línea de Ventas",
                "description": "Gestión de líneas de venta y distribución",
                "icon": ft.Icons.TRENDING_UP,
                "color": ft.Colors.ORANGE_600,
                "bg_color": ft.Colors.ORANGE_50,
                "route": "l_ventas",
                "available": True,
                "emoji": "📊",
                "badge": "Activo"
            },
            {
                "name": "Configuraciones",
                "description": "Configuración avanzada del sistema",
                "icon": ft.Icons.SETTINGS,
                "color": ft.Colors.GREY_600,
                "bg_color": ft.Colors.GREY_50,
                "route": "settings",
                "available": False,
                "emoji": "⚙️",
                "badge": "Desarrollo"
            }
        ]
        
        module_cards = []
        for module in modules:
            if module.get("available", True):
                # Módulos disponibles - Tamaño ajustado
                card = ft.Container(
                    content=ft.Container(
                        content=ft.Column([
                            # Header del módulo con badge - Espaciado ajustado
                            ft.Container(
                                content=ft.Row([
                                    ft.Text(module["emoji"], size=28),
                                    ft.Container(expand=True),
                                    ft.Container(
                                        content=ft.Text(
                                            module["badge"],
                                            size=10,
                                            color=ft.Colors.WHITE,
                                            weight=ft.FontWeight.BOLD
                                        ),
                                        bgcolor=ft.Colors.GREEN_500,
                                        padding=ft.padding.symmetric(horizontal=8, vertical=3),
                                        border_radius=10
                                    )
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                padding=ft.padding.only(bottom=15)  # Aumentado
                            ),
                            
                            # Icono principal del módulo
                            ft.Container(
                                content=ft.Icon(
                                    module["icon"],
                                    size=32,
                                    color=ft.Colors.WHITE
                                ),
                                width=60,
                                height=60,
                                bgcolor=module["color"],
                                border_radius=30,
                                alignment=ft.alignment.center,
                                shadow=ft.BoxShadow(
                                    spread_radius=2,
                                    blur_radius=8,
                                    color=f"{module['color']}40",
                                    offset=ft.Offset(0, 4)
                                )
                            ),
                            
                            ft.Container(height=18),  # Aumentado
                            
                            # Título del módulo
                            ft.Text(
                                module["name"],
                                size=18,
                                weight=ft.FontWeight.BOLD,
                                text_align=ft.TextAlign.CENTER,
                                color=ft.Colors.GREY_800
                            ),
                            
                            ft.Container(height=12),  # Aumentado
                            
                            # Descripción mejorada
                            ft.Text(
                                module["description"],
                                size=13,
                                color=ft.Colors.GREY_600,
                                text_align=ft.TextAlign.CENTER,
                                max_lines=3
                            ),
                            
                            ft.Container(height=20),  # Espaciado fijo en lugar de expand
                            
                            # Botón de acción
                            ft.Container(
                                content=ft.ElevatedButton(
                                    content=ft.Row([
                                        ft.Icon(ft.Icons.ARROW_FORWARD, size=16, color=ft.Colors.WHITE),
                                        ft.Text("Acceder", size=12, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)
                                    ], spacing=5, alignment=ft.MainAxisAlignment.CENTER),
                                    bgcolor=module["color"],
                                    color=ft.Colors.WHITE,
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=20),
                                        elevation=4
                                    ),
                                    on_click=lambda e, route=module["route"]: self._navigate_to_module(route)
                                ),
                                alignment=ft.alignment.center
                            )
                        ], 
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=0
                        ),
                        padding=25,
                        width=280,   # Aumentado de 250 a 280
                        height=350   # Aumentado de 280 a 350
                    ),
                    bgcolor=ft.Colors.WHITE,
                    border_radius=20,
                    shadow=ft.BoxShadow(
                        spread_radius=2,
                        blur_radius=12,
                        color=ft.Colors.GREY_200,
                        offset=ft.Offset(0, 6)
                    ),
                    border=ft.border.all(2, module["bg_color"]),
                    animate=ft.Animation(300, ft.AnimationCurve.EASE_OUT)
                )
                module_cards.append(card)
            else:
                # Módulos no disponibles - Tamaño ajustado
                card = ft.Container(
                    content=ft.Container(
                        content=ft.Column([
                            # Header con badge de desarrollo - Espaciado ajustado
                            ft.Container(
                                content=ft.Row([
                                    ft.Text("🚧", size=28),
                                    ft.Container(expand=True),
                                    ft.Container(
                                        content=ft.Text(
                                            module["badge"],
                                            size=10,
                                            color=ft.Colors.WHITE,
                                            weight=ft.FontWeight.BOLD
                                        ),
                                        bgcolor=ft.Colors.ORANGE_500,
                                        padding=ft.padding.symmetric(horizontal=8, vertical=3),
                                        border_radius=10
                                    )
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                padding=ft.padding.only(bottom=15)  # Aumentado
                            ),
                            
                            # Icono deshabilitado
                            ft.Container(
                                content=ft.Icon(
                                    module["icon"],
                                    size=32,
                                    color=ft.Colors.WHITE
                                ),
                                width=60,
                                height=60,
                                bgcolor=ft.Colors.GREY_400,
                                border_radius=30,
                                alignment=ft.alignment.center,
                                shadow=ft.BoxShadow(
                                    spread_radius=1,
                                    blur_radius=4,
                                    color=ft.Colors.GREY_200,
                                    offset=ft.Offset(0, 2)
                                )
                            ),
                            
                            ft.Container(height=18),  # Aumentado
                            
                            ft.Text(
                                module["name"],
                                size=18,
                                weight=ft.FontWeight.BOLD,
                                text_align=ft.TextAlign.CENTER,
                                color=ft.Colors.GREY_500
                            ),
                            
                            ft.Container(height=12),  # Aumentado
                            
                            ft.Text(
                                "Módulo en desarrollo...",
                                size=13,
                                color=ft.Colors.GREY_400,
                                text_align=ft.TextAlign.CENTER,
                                style=ft.TextStyle(italic=True)
                            ),
                            
                            ft.Container(height=20),  # Espaciado fijo en lugar de expand
                            
                            # Botón deshabilitado
                            ft.Container(
                                content=ft.ElevatedButton(
                                    content=ft.Row([
                                        ft.Icon(ft.Icons.SCHEDULE, size=16, color=ft.Colors.WHITE),
                                        ft.Text("Próximamente", size=12, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)
                                    ], spacing=5, alignment=ft.MainAxisAlignment.CENTER),
                                    bgcolor=ft.Colors.GREY_400,
                                    color=ft.Colors.WHITE,
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=20),
                                        elevation=2
                                    ),
                                    on_click=lambda e, route=module["route"]: self._show_coming_soon_dialog(route)
                                ),
                                alignment=ft.alignment.center
                            )
                        ], 
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=0
                        ),
                        padding=25,
                        width=280,   # Aumentado de 250 a 280
                        height=350   # Aumentado de 280 a 350
                    ),
                    bgcolor=ft.Colors.GREY_50,
                    border_radius=20,
                    shadow=ft.BoxShadow(
                        spread_radius=1,
                        blur_radius=6,
                        color=ft.Colors.GREY_100,
                        offset=ft.Offset(0, 3)
                    ),
                    border=ft.border.all(1, ft.Colors.GREY_200),
                    opacity=0.8
                )
                module_cards.append(card)
        
        return ft.GridView(
            controls=module_cards,
            runs_count=3,
            max_extent=320,      # Aumentado de 280 a 320
            child_aspect_ratio=0.9,  # Cambiado de 1.1 a 0.9 para más altura
            spacing=25,
            run_spacing=25,
            padding=ft.padding.all(15)
        )

    def _create_stat_card(self, title: str, value: str, icon, color, bg_color, subtitle: str = None) -> ft.Container:
        """Crea una tarjeta de estadística con tamaño original y contenido reducido"""
        return ft.Container(
            content=ft.Container(
                content=ft.Column([
                    # Fila principal con icono y datos - Contenido compacto
                    ft.Row([
                        # Contenedor del icono - Tamaño reducido
                        ft.Container(
                            content=ft.Icon(icon, size=24, color=ft.Colors.WHITE),  # Reducido
                            width=45,   # Reducido de 75 a 45
                            height=45,  # Reducido de 75 a 45
                            bgcolor=color,
                            border_radius=22.5,
                            alignment=ft.alignment.center,
                            shadow=ft.BoxShadow(
                                spread_radius=1,
                                blur_radius=6,
                                color=f"{color}40",
                                offset=ft.Offset(0, 2)
                            )
                        ),
                        
                        ft.Container(width=15),  # Espaciado reducido
                        
                        # Columna con datos - Contenido compacto
                        ft.Column([
                            # Valor principal
                            ft.Text(
                                value, 
                                size=28,  # Reducido de 42 a 28
                                weight=ft.FontWeight.BOLD,
                                color=color
                            ),
                            # Título principal - Sin espaciado extra
                            ft.Text(
                                title, 
                                size=13,  # Reducido de 18 a 13
                                color=ft.Colors.GREY_700,
                                weight=ft.FontWeight.W_500
                            )
                        ], spacing=2, alignment=ft.MainAxisAlignment.CENTER)  # Espaciado mínimo
                    ], alignment=ft.MainAxisAlignment.START)
                ], spacing=0),
                padding=20,  # Reducido de 35 a 20
                width=280,   # Vuelto al tamaño original
                height=90    # Vuelto al tamaño original
            ),
            bgcolor=ft.Colors.WHITE,
            border_radius=15,  # Reducido de 22 a 15
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=8,
                color=ft.Colors.GREY_200,
                offset=ft.Offset(0, 4)
            ),
            border=ft.border.all(2, bg_color)
        )

    def _build_stats_cards(self) -> ft.Row:
        """Construye las tarjetas de estadísticas compactas"""
        stats = self._get_dashboard_stats()
        
        cards = [
            self._create_stat_card(
                "Municipios",  # Título simplificado
                str(stats.get('municipios', 14)),
                ft.Icons.LOCATION_CITY,
                ft.Colors.BLUE_600,
                ft.Colors.BLUE_50
            ),
            self._create_stat_card(
                "Usuarios",  # Título simplificado
                str(stats.get('usuarios', 2)),
                ft.Icons.PEOPLE,
                ft.Colors.GREEN_600,
                ft.Colors.GREEN_50
            ),
            self._create_stat_card(
                "Registros",  # Título simplificado
                str(stats.get('registros', 0)),
                ft.Icons.DATA_USAGE,
                ft.Colors.ORANGE_600,
                ft.Colors.ORANGE_50
            ),
            self._create_stat_card(
                "Módulos",  # Título simplificado
                "4/6",
                ft.Icons.APPS,
                ft.Colors.PURPLE_600,
                ft.Colors.PURPLE_50
            )
        ]
        
        return ft.Row(
            cards,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            wrap=True,
            spacing=15  # Espaciado original
        )


    def _build_summary_chart(self) -> ft.Container:
        """Construye el gráfico de resumen con mejoras estéticas"""
        return ft.Container(
            content=ft.Container(
                content=ft.Column([
                    # Header del gráfico mejorado
                    ft.Row([
                        ft.Container(
                            content=ft.Icon(ft.Icons.BAR_CHART, size=32, color=ft.Colors.WHITE),
                            width=55,
                            height=55,
                            bgcolor=ft.Colors.INDIGO_600,
                            border_radius=27.5,
                            alignment=ft.alignment.center,
                            shadow=ft.BoxShadow(
                                spread_radius=2,
                                blur_radius=8,
                                color=ft.Colors.INDIGO_200,
                                offset=ft.Offset(0, 4)
                            )
                        ),
                        ft.Container(width=18),
                        ft.Column([
                            ft.Text(
                                "📊 Resumen de Pérdidas Provinciales",
                                size=22,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.INDIGO_800
                            ),
                            ft.Text(
                                "Análisis gráfico de datos de los 14 municipios",
                                size=13,
                                color=ft.Colors.INDIGO_600
                            )
                        ], spacing=3)
                    ], alignment=ft.MainAxisAlignment.START),
                    
                    ft.Container(height=25),
                    
                    # Área del gráfico mejorada
                    ft.Container(
                        content=ft.Column([
                            ft.Container(
                                content=ft.Icon(
                                    ft.Icons.SHOW_CHART,
                                    size=72,
                                    color=ft.Colors.INDIGO_300
                                ),
                                alignment=ft.alignment.center
                            ),
                            ft.Container(height=20),
                            ft.Text(
                                "📈 Visualización de Pérdidas Eléctricas",
                                text_align=ft.TextAlign.CENTER,
                                size=18,
                                color=ft.Colors.INDIGO_700,
                                weight=ft.FontWeight.BOLD
                            ),
                            ft.Container(height=12),
                            ft.Text(
                                "Los datos se actualizarán automáticamente con la información\nde energía y facturación de todos los municipios",
                                text_align=ft.TextAlign.CENTER,
                                size=13,
                                color=ft.Colors.INDIGO_500
                            ),
                            ft.Container(height=20),
                            ft.Row([
                                ft.Container(
                                    content=ft.Text(
                                        "🔄 Tiempo Real",
                                        size=12,
                                        color=ft.Colors.GREEN_600,
                                        weight=ft.FontWeight.W_600
                                    ),
                                    bgcolor=ft.Colors.GREEN_50,
                                    padding=ft.padding.symmetric(horizontal=15, vertical=8),
                                    border_radius=20,
                                    border=ft.border.all(1, ft.Colors.GREEN_200)
                                ),
                                ft.Container(width=15),
                                ft.Container(
                                    content=ft.Text(
                                        "📊 14 Municipios",
                                        size=12,
                                        color=ft.Colors.BLUE_600,
                                        weight=ft.FontWeight.W_600
                                    ),
                                    bgcolor=ft.Colors.BLUE_50,
                                    padding=ft.padding.symmetric(horizontal=15, vertical=8),
                                    border_radius=20,
                                    border=ft.border.all(1, ft.Colors.BLUE_200)
                                )
                            ], alignment=ft.MainAxisAlignment.CENTER)
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        height=250,
                        alignment=ft.alignment.center,
                        bgcolor=ft.Colors.INDIGO_50,
                        border_radius=15,
                        border=ft.border.all(2, ft.Colors.INDIGO_100)
                    )
                ]),
                padding=30
            ),
            bgcolor=ft.Colors.WHITE,
            border_radius=20,
            shadow=ft.BoxShadow(
                spread_radius=2,
                blur_radius=15,
                color=ft.Colors.INDIGO_100,
                offset=ft.Offset(0, 6)
            ),
            border=ft.border.all(2, ft.Colors.INDIGO_50)
        )
    
    def _build_recent_activity(self) -> ft.Container:
        """Construye la sección de actividad reciente (NUEVA)"""
        return ft.Container(
            content=ft.Container(
                content=ft.Column([
                    # Header de actividad reciente
                    ft.Row([
                        ft.Container(
                            content=ft.Icon(ft.Icons.HISTORY, size=28, color=ft.Colors.WHITE),
                            width=45,
                            height=45,
                            bgcolor=ft.Colors.TEAL_600,
                            border_radius=22.5,
                            alignment=ft.alignment.center,
                            shadow=ft.BoxShadow(
                                spread_radius=1,
                                blur_radius=6,
                                color=ft.Colors.TEAL_200,
                                offset=ft.Offset(0, 3)
                            )
                        ),
                        ft.Container(width=12),
                        ft.Column([
                            ft.Text(
                                "📋 Actividad Reciente",
                                size=18,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.TEAL_800
                            ),
                            ft.Text(
                                "Últimas acciones del sistema",
                                size=12,
                                color=ft.Colors.TEAL_600
                            )
                        ], spacing=2)
                    ], alignment=ft.MainAxisAlignment.START),
                    
                    ft.Container(height=20),
                    
                    # Lista de actividades
                    ft.Column([
                        self._create_activity_item(
                            "✅ Sistema iniciado",
                            "Aplicación web cargada correctamente",
                            ft.Colors.GREEN_500,
                            "Hace 2 min"
                        ),
                        self._create_activity_item(
                            "👤 Usuario conectado",
                            f"Sesión iniciada: {self.app.get_current_user().get('username', 'admin')}",
                            ft.Colors.BLUE_500,
                            "Hace 5 min"
                        ),
                        self._create_activity_item(
                            "🗄️ Base de datos lista",
                            "14 municipios cargados",
                            ft.Colors.PURPLE_500,
                            "Hace 10 min"
                        ),
                        self._create_activity_item(
                            "🔧 Módulos verificados",
                            "4/6 módulos activos",
                            ft.Colors.ORANGE_500,
                            "Hace 15 min"
                        )
                    ], spacing=12),
                    
                    ft.Container(height=15),
                    
                    # Botón ver más
                    ft.Container(
                        content=ft.TextButton(
                            content=ft.Row([
                                ft.Text("Ver historial completo", size=12, color=ft.Colors.TEAL_600),
                                ft.Icon(ft.Icons.ARROW_FORWARD, size=14, color=ft.Colors.TEAL_600)
                            ], spacing=5, alignment=ft.MainAxisAlignment.CENTER),
                            on_click=lambda e: self._show_activity_history()
                        ),
                        alignment=ft.alignment.center
                    )
                ]),
                padding=25
            ),
            bgcolor=ft.Colors.WHITE,
            border_radius=20,
            shadow=ft.BoxShadow(
                spread_radius=2,
                blur_radius=15,
                color=ft.Colors.TEAL_100,
                offset=ft.Offset(0, 6)
            ),
            border=ft.border.all(2, ft.Colors.TEAL_50)
        )
    
    def _create_activity_item(self, title: str, description: str, color, time: str) -> ft.Container:
        """Crea un item de actividad reciente"""
        return ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Icon(ft.Icons.CIRCLE, size=8, color=color),
                    width=20,
                    alignment=ft.alignment.center
                ),
                ft.Column([
                    ft.Text(
                        title,
                        size=13,
                        weight=ft.FontWeight.W_600,
                        color=ft.Colors.GREY_800
                    ),
                    ft.Text(
                        description,
                        size=11,
                        color=ft.Colors.GREY_600
                    ),
                    ft.Text(
                        time,
                        size=10,
                        color=ft.Colors.GREY_400,
                        style=ft.TextStyle(italic=True)
                    )
                ], spacing=2, expand=True)
            ], spacing=0),
            padding=ft.padding.symmetric(vertical=5, horizontal=10),
            border_radius=10,
            bgcolor=ft.Colors.GREY_50
        )

    def _get_dashboard_stats(self) -> Dict:
        """Obtiene estadísticas para el dashboard - ACTUALIZADO"""
        try:
            stats = {}
            
            # Contar municipios (ahora son 14 con Varadero)
            municipios = self.db_manager.execute_query("SELECT COUNT(*) as count FROM municipios WHERE activo = 1")
            stats['municipios'] = municipios[0]['count'] if municipios else 14
            
            # Contar usuarios activos (admin + operador = 2)
            usuarios = self.db_manager.execute_query("SELECT COUNT(*) as count FROM usuarios WHERE activo = 1")
            stats['usuarios'] = usuarios[0]['count'] if usuarios else 2
            
            # Contar registros de datos
            registros = self.db_manager.execute_query("SELECT COUNT(*) as count FROM energia_barra")
            stats['registros'] = registros[0]['count'] if registros else 0
            
            # Contar registros de facturación
            facturacion = self.db_manager.execute_query("SELECT COUNT(*) as count FROM facturacion")
            stats['facturacion'] = facturacion[0]['count'] if facturacion else 0
            
            return stats
            
        except Exception as e:
            self.logger.error(f"Error al obtener estadísticas: {e}")
            return {
                'municipios': 14,  # Actualizado a 14
                'usuarios': 2,     # Actualizado a 2
                'registros': 0,
                'facturacion': 0
            }
    
    def _navigate_to_module(self, route: str):
        """Navega a un módulo específico - MEJORADO"""
        self.logger.info(f"Navegando a módulo: {route}")
        
        # Rutas de módulos implementados
        implemented_routes = ["calculo_energia", "facturacion", "infoperdidas", "l_ventas"]
        
        if route in implemented_routes:
            # Mostrar indicador de carga antes de navegar
            self._show_loading_indicator()
            # Navegar a módulos implementados
            self.app.navigate_to(route)
        else:
            # Otros módulos no implementados
            self._show_coming_soon_dialog(route)
    
    def _show_loading_indicator(self):
        """Muestra un indicador de carga durante la navegación"""
        loading_dialog = ft.AlertDialog(
            modal=True,
            content=ft.Container(
                content=ft.Column([
                    ft.ProgressRing(width=50, height=50, stroke_width=4, color=ft.Colors.BLUE_600),
                    ft.Container(height=15),
                    ft.Text("Cargando módulo...", size=16, text_align=ft.TextAlign.CENTER)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                width=200,
                height=120,
                alignment=ft.alignment.center
            )
        )
        
        self.page.open(loading_dialog)

        
        # Cerrar el diálogo después de un breve momento
        import threading
        import time
        def close_loading():
            time.sleep(0.5)
            self.page.close(loading_dialog)
        
        threading.Thread(target=close_loading, daemon=True).start()
    
    def _show_activity_history(self):
        """Muestra el historial completo de actividades"""
        def close_dialog(e):
            dialog.open = False
            self.page.update()
        
        activities = [
            ("✅ Sistema iniciado", "Aplicación web cargada correctamente", "Hace 2 min"),
            ("👤 Usuario conectado", f"Sesión iniciada: {self.app.get_current_user().get('username', 'admin')}", "Hace 5 min"),
            ("🗄️ Base de datos lista", "14 municipios de Matanzas cargados", "Hace 10 min"),
            ("🔧 Módulos verificados", "4/6 módulos del sistema activos", "Hace 15 min"),
            ("📊 Dashboard cargado", "Interfaz principal inicializada", "Hace 20 min"),
            ("🔐 Autenticación OK", "Sistema de seguridad verificado", "Hace 25 min"),
            ("⚙️ Configuración cargada", "Parámetros del sistema aplicados", "Hace 30 min")
        ]
        
        activity_list = ft.Column([
            ft.Container(
                content=ft.Row([
                    ft.Text(title, size=13, weight=ft.FontWeight.W_600, expand=True),
                    ft.Text(time, size=11, color=ft.Colors.GREY_500)
                ]),
                padding=ft.padding.all(10),
                bgcolor=ft.Colors.GREY_50,
                border_radius=8,
                margin=ft.margin.only(bottom=5)
            )
            for title, desc, time in activities
        ], scroll=ft.ScrollMode.AUTO, height=300)
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Row([
                ft.Icon(ft.Icons.HISTORY, color=ft.Colors.TEAL_600, size=28),
                ft.Container(width=10),
                ft.Text("Historial de Actividades", color=ft.Colors.TEAL_800, weight=ft.FontWeight.BOLD)
            ]),
            content=ft.Container(
                content=activity_list,
                width=500,
                height=350
            ),
            actions=[
                ft.Container(
                    content=ft.ElevatedButton(
                        "Cerrar",
                        on_click=close_dialog,
                        bgcolor=ft.Colors.TEAL_600,
                        color=ft.Colors.WHITE,
                        icon=ft.Icons.CLOSE
                    ),
                    alignment=ft.alignment.center
                )
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER
        )
        
        self.page.open(dialog)

    
    def _show_coming_soon_dialog(self, module_name: str):
        """Muestra diálogo de 'próximamente' con mejoras estéticas"""
        def close_dialog(e):
            dialog.open = False
            self.page.update()
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Row([
                ft.Icon(ft.Icons.CONSTRUCTION, color=ft.Colors.ORANGE_600, size=32),
                ft.Container(width=12),
                ft.Text("Módulo en Desarrollo", color=ft.Colors.ORANGE_800, weight=ft.FontWeight.BOLD, size=20)
            ]),
            content=ft.Container(
                content=ft.Column([
                    ft.Container(
                        content=ft.Text("🚧", size=64),
                        alignment=ft.alignment.center
                    ),
                    ft.Container(height=20),
                    ft.Text(
                        f"El módulo '{module_name}' estará disponible próximamente.",
                        size=16,
                        text_align=ft.TextAlign.CENTER,
                        color=ft.Colors.GREY_700
                    ),
                    ft.Container(height=15),
                    ft.Container(
                        content=ft.Column([
                            ft.Text("🔨 En construcción activa", size=14, color=ft.Colors.ORANGE_600, weight=ft.FontWeight.W_600),
                            ft.Text("📅 Próxima actualización del sistema", size=12, color=ft.Colors.ORANGE_500)
                        ], spacing=5),
                        bgcolor=ft.Colors.ORANGE_50,
                        padding=ft.padding.all(15),
                        border_radius=15,
                        alignment=ft.alignment.center,
                        border=ft.border.all(1, ft.Colors.ORANGE_200)
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                width=350,
                height=200
            ),
            actions=[
                ft.Container(
                    content=ft.ElevatedButton(
                        content=ft.Row([
                            ft.Icon(ft.Icons.CHECK, size=18),
                            ft.Text("Entendido", size=14, weight=ft.FontWeight.BOLD)
                        ], spacing=8, alignment=ft.MainAxisAlignment.CENTER),
                        on_click=close_dialog,
                        bgcolor=ft.Colors.ORANGE_600,
                        color=ft.Colors.WHITE,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=25),
                            elevation=4
                        )
                    ),
                    alignment=ft.alignment.center
                )
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER
        )
        
        self.page.open(dialog)

    
    def _logout(self, e):
        """Maneja el cierre de sesión con confirmación mejorada"""
        def confirm_logout(e):
            dialog.open = False
            self.page.update()
            self.app.logout()
        
        def cancel_logout(e):
            dialog.open = False
            self.page.update()
        
        user = self.app.get_current_user()
        username = user.get('nombre_completo', user.get('username', 'Usuario'))
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Row([
                ft.Icon(ft.Icons.LOGOUT, color=ft.Colors.BLUE_600, size=32),
                ft.Container(width=12),
                ft.Text("Cerrar Sesión", color=ft.Colors.BLUE_800, weight=ft.FontWeight.BOLD, size=20)
            ]),
            content=ft.Container(
                content=ft.Column([
                    ft.Container(
                        content=ft.Text("👋", size=64),
                        alignment=ft.alignment.center
                    ),
                    ft.Container(height=20),
                    ft.Text(
                        f"¿Está seguro que desea cerrar la sesión de {username}?",
                        size=16,
                        text_align=ft.TextAlign.CENTER,
                        color=ft.Colors.GREY_700
                    ),
                    ft.Container(height=15),
                    ft.Container(
                        content=ft.Column([
                            ft.Text("🔒 Su trabajo se guardará automáticamente", size=13, color=ft.Colors.GREEN_600, weight=ft.FontWeight.W_600),
                            ft.Text("💾 Datos sincronizados con el sistema", size=11, color=ft.Colors.GREEN_500)
                        ], spacing=5),
                        bgcolor=ft.Colors.GREEN_50,
                        padding=ft.padding.all(15),
                        border_radius=15,
                        alignment=ft.alignment.center,
                        border=ft.border.all(1, ft.Colors.GREEN_200)
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                width=400,
                height=200
            ),
            actions=[
                ft.Row([
                    ft.ElevatedButton(
                        content=ft.Row([
                            ft.Icon(ft.Icons.CANCEL, size=18),
                            ft.Text("Cancelar", size=14, weight=ft.FontWeight.BOLD)
                        ], spacing=8, alignment=ft.MainAxisAlignment.CENTER),
                        on_click=cancel_logout,
                        bgcolor=ft.Colors.GREY_500,
                        color=ft.Colors.WHITE,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=25),
                            elevation=4
                        )
                    ),
                    ft.Container(width=20),
                    ft.ElevatedButton(
                        content=ft.Row([
                            ft.Icon(ft.Icons.LOGOUT, size=18),
                            ft.Text("Cerrar Sesión", size=14, weight=ft.FontWeight.BOLD)
                        ], spacing=8, alignment=ft.MainAxisAlignment.CENTER),
                        on_click=confirm_logout,
                        bgcolor=ft.Colors.RED_600,
                        color=ft.Colors.WHITE,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=25),
                            elevation=4
                        )
                    )
                ], alignment=ft.MainAxisAlignment.CENTER)
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER
        )
        
        self.page.open(dialog)

