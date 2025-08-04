"""
Utilidades compartidas para las pestañas de LVentas
"""

import flet as ft
from typing import List, Dict, Any
from datetime import datetime

def format_number(value: float, decimals: int = 2, unit: str = "") -> str:
    """Formatea un número con decimales y unidad"""
    try:
        if unit:
            return f"{value:.{decimals}f} {unit}"
        return f"{value:.{decimals}f}"
    except:
        return "0.00"

def format_percentage(value: float, decimals: int = 2) -> str:
    """Formatea un porcentaje"""
    try:
        return f"{value:.{decimals}f}%"
    except:
        return "0.00%"

def get_month_name(month: int) -> str:
    """Obtiene el nombre del mes"""
    months = [
        "", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ]
    return months[month] if 1 <= month <= 12 else ""

def get_period_text(year: int, month: int, is_accumulated: bool = False) -> str:
    """Obtiene el texto del período"""
    month_name = get_month_name(month)
    if is_accumulated:
        return f"Enero a {month_name} {year}"
    else:
        return f"{month_name} {year}"

def create_status_indicator(is_compliant: bool, theme: Dict[str, Any]) -> ft.Control:
    """Crea un indicador de estado"""
    if is_compliant:
        return ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.CHECK_CIRCLE, size=16, color=theme['success']),
                ft.Container(width=4),
                ft.Text("Cumple", size=10, weight=ft.FontWeight.BOLD, color=theme['success'])
            ], spacing=0),
            bgcolor=f"{theme['success']}15",
            padding=ft.padding.symmetric(horizontal=8, vertical=4),
            border_radius=12,
            border=ft.border.all(1, f"{theme['success']}30")
        )
    else:
        return ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.WARNING, size=16, color=theme['danger']),
                ft.Container(width=4),
                ft.Text("No Cumple", size=10, weight=ft.FontWeight.BOLD, color=theme['danger'])
            ], spacing=0),
            bgcolor=f"{theme['danger']}15",
            padding=ft.padding.symmetric(horizontal=8, vertical=4),
            border_radius=12,
            border=ft.border.all(1, f"{theme['danger']}30")
        )

def create_metric_card(title: str, value: str, subtitle: str = "", icon: ft.Icons = None, 
                      color: str = None, theme: Dict[str, Any] = None) -> ft.Control:
    """Crea una tarjeta de métrica"""
    if not theme:
        theme = {'white': ft.Colors.WHITE, 'text_primary': ft.Colors.GREY_800, 
                'text_secondary': ft.Colors.GREY_600, 'border': ft.Colors.GREY_200}
    
    if not color:
        color = theme.get('primary', ft.Colors.BLUE_600)
    
    return ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Container(
                    content=ft.Icon(icon or ft.Icons.INFO, size=20, color=theme['white']),
                    width=40, height=40,
                    bgcolor=color,
                    border_radius=20,
                    alignment=ft.alignment.center
                ) if icon else ft.Container(),
                ft.Container(width=12) if icon else ft.Container(),
                ft.Column([
                    ft.Text(title, size=12, weight=ft.FontWeight.BOLD, color=theme['text_primary']),
                    ft.Text(subtitle, size=10, color=theme['text_secondary']) if subtitle else ft.Container()
                ], spacing=2)
            ]),
            ft.Container(height=8),
            ft.Text(value, size=18, weight=ft.FontWeight.BOLD, color=theme['text_primary'])
        ]),
        bgcolor=theme['white'],
        padding=16,
        border_radius=12,
        border=ft.border.all(1, theme['border']),
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=4,
            color='rgba(0,0,0,0.1)',
            offset=ft.Offset(0, 2)
        ),
        width=200,
        height=120
    )

def create_data_table(headers: List[str], rows: List[List[Any]], theme: Dict[str, Any],
                     header_color: str = None, row_colors: List[str] = None) -> ft.Control:
    """Crea una tabla de datos estilizada"""
    if not header_color:
        header_color = theme.get('primary', ft.Colors.BLUE_600)
    
    # Crear columnas
    columns = [
        ft.DataColumn(
            ft.Text(header, size=11, weight=ft.FontWeight.BOLD, color=theme['white'])
        ) for header in headers
    ]
    
    # Crear filas
    data_rows = []
    for i, row in enumerate(rows):
        row_color = row_colors[i] if row_colors and i < len(row_colors) else (
            theme.get('light', ft.Colors.GREY_50) if i % 2 == 0 else theme['white']
        )
        
        cells = [
            ft.DataCell(
                ft.Text(str(cell), size=11, color=theme['text_primary'])
                if not isinstance(cell, ft.Control) else cell
            ) for cell in row
        ]
        
        data_rows.append(ft.DataRow(cells=cells, color=row_color))
    
    return ft.Container(
        content=ft.DataTable(
            columns=columns,
            rows=data_rows,
            border=ft.border.all(1, theme['border']),
            border_radius=12,
            vertical_lines=ft.border.BorderSide(1, f"{theme['border']}50"),
            horizontal_lines=ft.border.BorderSide(1, f"{theme['border']}50"),
            heading_row_color=header_color,
            heading_row_height=45,
            data_row_min_height=40
        ),
        bgcolor=theme['white'],
        border_radius=12,
        padding=16,
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=6,
            color='rgba(0,0,0,0.1)',
            offset=ft.Offset(0, 2)
        )
    )

def validate_data(data: List[Dict[str, Any]], required_fields: List[str]) -> bool:
    """Valida que los datos tengan los campos requeridos"""
    if not data:
        return False
    
    for item in data:
        for field in required_fields:
            if field not in item:
                return False
    
    return True

def calculate_compliance_rate(data: List[Dict[str, Any]], plan_field: str, real_field: str) -> float:
    """Calcula la tasa de cumplimiento"""
    if not data:
        return 0.0
    
    compliant_count = 0
    for item in data:
        try:
            plan = float(item.get(plan_field, 0))
            real = float(item.get(real_field, 0))
            if real <= plan:
                compliant_count += 1
        except (ValueError, TypeError):
            continue
    
    return (compliant_count / len(data)) * 100

def get_current_period() -> tuple:
    """Obtiene el período actual (año, mes)"""
    now = datetime.now()
    return now.year, now.month

def create_loading_indicator(message: str = "Cargando...", theme: Dict[str, Any] = None) -> ft.Control:
    """Crea un indicador de carga"""
    if not theme:
        theme = {'text_primary': ft.Colors.GREY_800, 'primary': ft.Colors.BLUE_600}
    
    return ft.Container(
        content=ft.Column([
            ft.ProgressRing(width=40, height=40, stroke_width=3, color=theme['primary']),
            ft.Container(height=16),
            ft.Text(message, size=14, color=theme['text_primary'])
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        expand=True,
        alignment=ft.alignment.center
    )

def create_empty_state(title: str, subtitle: str = "", icon: ft.Icons = None, 
                      theme: Dict[str, Any] = None) -> ft.Control:
    """Crea un estado vacío"""
    if not theme:
        theme = {'text_primary': ft.Colors.GREY_800, 'text_secondary': ft.Colors.GREY_600}
    
    return ft.Container(
        content=ft.Column([
            ft.Icon(icon or ft.Icons.INBOX, size=64, color=theme['text_secondary']),
            ft.Container(height=16),
            ft.Text(title, size=18, weight=ft.FontWeight.BOLD, color=theme['text_primary']),
            ft.Text(subtitle, size=14, color=theme['text_secondary']) if subtitle else ft.Container()
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        expand=True,
        alignment=ft.alignment.center,
        padding=40
    )

def create_period_selector(year: int, month: int, on_year_change, on_month_change, 
                          theme: Dict[str, Any], title: str = "Período") -> ft.Control:
    """Crea un selector de período reutilizable"""
    
    # Opciones de meses
    month_options = [
        ft.dropdown.Option(str(i), get_month_name(i)) 
        for i in range(1, 13)
    ]
    
    # Opciones de años
    current_year = datetime.now().year
    year_options = [
        ft.dropdown.Option(str(y), str(y)) 
        for y in range(current_year - 4, current_year + 1)
    ]
    
    return ft.Container(
        content=ft.Column([
            ft.Text(f"📅 {title}", size=14, weight=ft.FontWeight.BOLD, color=theme['text_primary']),
            ft.Container(height=8),
            ft.Row([
                ft.Container(
                    content=ft.Dropdown(
                        width=140,
                        value=str(month),
                        options=month_options,
                        on_change=on_month_change,
                        bgcolor=theme['white'],
                        border_color=theme['border'],
                        text_size=12,
                        content_padding=ft.padding.symmetric(horizontal=12, vertical=8)
                    ),
                    border_radius=8
                ),
                ft.Container(width=12),
                ft.Container(
                    content=ft.Dropdown(
                        width=100,
                        value=str(year),
                        options=year_options,
                        on_change=on_year_change,
                        bgcolor=theme['white'],
                        border_color=theme['border'],
                        text_size=12,
                        content_padding=ft.padding.symmetric(horizontal=12, vertical=8)
                    ),
                    border_radius=8
                )
            ])
        ]),
        bgcolor=f"{theme.get('primary', ft.Colors.BLUE_600)}10",
        padding=16,
        border_radius=12,
        border=ft.border.all(1, f"{theme.get('primary', ft.Colors.BLUE_600)}30")
    )

def create_export_button(on_click, theme: Dict[str, Any], text: str = "Exportar") -> ft.Control:
    """Crea un botón de exportación estilizado"""
    return ft.ElevatedButton(
        content=ft.Row([
            ft.Icon(ft.Icons.DOWNLOAD, size=16, color=theme['white']),
            ft.Container(width=6),
            ft.Text(text, size=12, color=theme['white'])
        ], spacing=0),
        on_click=on_click,
        bgcolor=theme.get('success', ft.Colors.GREEN_600),
        color=theme['white'],
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),
            elevation=2
        )
    )

def create_refresh_button(on_click, theme: Dict[str, Any], text: str = "Actualizar") -> ft.Control:
    """Crea un botón de actualización estilizado"""
    return ft.ElevatedButton(
        content=ft.Row([
            ft.Icon(ft.Icons.REFRESH, size=16, color=theme['white']),
            ft.Container(width=6),
            ft.Text(text, size=12, color=theme['white'])
        ], spacing=0),
        on_click=on_click,
        bgcolor=theme.get('primary', ft.Colors.BLUE_600),
        color=theme['white'],
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),
            elevation=2
        )
    )

def safe_float(value, default: float = 0.0) -> float:
    """Convierte un valor a float de forma segura"""
    try:
        return float(value)
    except (ValueError, TypeError):
        return default

def safe_int(value, default: int = 0) -> int:
    """Convierte un valor a int de forma segura"""
    try:
        return int(value)
    except (ValueError, TypeError):
        return default

def safe_str(value, default: str = "") -> str:
    """Convierte un valor a string de forma segura"""
    try:
        return str(value) if value is not None else default
    except:
        return default

def calculate_percentage_difference(plan: float, real: float) -> float:
    """Calcula la diferencia porcentual entre plan y real"""
    try:
        return real - plan
    except (ValueError, TypeError):
        return 0.0

def is_compliant(plan: float, real: float) -> bool:
    """Determina si un valor real cumple con el plan"""
    try:
        return float(real) <= float(plan)
    except (ValueError, TypeError):
        return False

def get_compliance_color(is_compliant: bool, theme: Dict[str, Any]) -> str:
    """Obtiene el color según el cumplimiento"""
    return theme.get('success', ft.Colors.GREEN_600) if is_compliant else theme.get('danger', ft.Colors.RED_600)

def create_summary_card(title: str, value: str, change: str = "", 
                       change_positive: bool = True, icon: ft.Icons = None,
                       theme: Dict[str, Any] = None) -> ft.Control:
    """Crea una tarjeta de resumen con cambio"""
    if not theme:
        theme = {
            'white': ft.Colors.WHITE,
            'text_primary': ft.Colors.GREY_800,
            'text_secondary': ft.Colors.GREY_600,
            'success': ft.Colors.GREEN_600,
            'danger': ft.Colors.RED_600,
            'border': ft.Colors.GREY_200
        }
    
    change_color = theme['success'] if change_positive else theme['danger']
    change_icon = ft.Icons.TRENDING_UP if change_positive else ft.Icons.TRENDING_DOWN
    
    return ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Icon(icon or ft.Icons.ANALYTICS, size=24, color=theme['text_primary']),
                ft.Container(expand=True),
                ft.Icon(change_icon, size=16, color=change_color) if change else ft.Container()
            ]),
            ft.Container(height=12),
            ft.Text(title, size=12, color=theme['text_secondary']),
            ft.Container(height=4),
            ft.Text(value, size=20, weight=ft.FontWeight.BOLD, color=theme['text_primary']),
            ft.Container(height=4),
            ft.Text(change, size=11, color=change_color, weight=ft.FontWeight.W_500) if change else ft.Container()
        ]),
        bgcolor=theme['white'],
        padding=20,
        border_radius=16,
        border=ft.border.all(1, theme['border']),
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=8,
            color='rgba(0,0,0,0.06)',
            offset=ft.Offset(0, 2)
        ),
        width=200,
        height=140
    )

def create_alert_banner(message: str, alert_type: str = "info", 
                       theme: Dict[str, Any] = None) -> ft.Control:
    """Crea un banner de alerta"""
    if not theme:
        theme = {
            'info': ft.Colors.BLUE_600,
            'success': ft.Colors.GREEN_600,
            'warning': ft.Colors.ORANGE_600,
            'danger': ft.Colors.RED_600,
            'white': ft.Colors.WHITE
        }
    
    colors = {
        'info': {'bg': theme['info'], 'icon': ft.Icons.INFO},
        'success': {'bg': theme['success'], 'icon': ft.Icons.CHECK_CIRCLE},
        'warning': {'bg': theme['warning'], 'icon': ft.Icons.WARNING},
        'danger': {'bg': theme['danger'], 'icon': ft.Icons.ERROR}
    }
    
    config = colors.get(alert_type, colors['info'])
    
    return ft.Container(
        content=ft.Row([
            ft.Icon(config['icon'], size=20, color=theme['white']),
            ft.Container(width=12),
            ft.Text(message, size=14, color=theme['white'], weight=ft.FontWeight.W_500)
        ]),
        bgcolor=config['bg'],
        padding=ft.padding.symmetric(horizontal=16, vertical=12),
        border_radius=8,
        margin=ft.margin.only(bottom=16)
    )

def truncate_text(text: str, max_length: int = 20) -> str:
    """Trunca texto si es muy largo"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."

def format_large_number(value: float, decimals: int = 1) -> str:
    """Formatea números grandes con sufijos"""
    try:
        if value >= 1_000_000:
            return f"{value/1_000_000:.{decimals}f}M"
        elif value >= 1_000:
            return f"{value/1_000:.{decimals}f}K"
        else:
            return f"{value:.{decimals}f}"
    except:
        return "0"

def get_status_text(is_compliant: bool) -> str:
    """Obtiene el texto de estado"""
    return "Cumple" if is_compliant else "No Cumple"

def get_status_emoji(is_compliant: bool) -> str:
    """Obtiene el emoji de estado"""
    return "✅" if is_compliant else "❌"

def create_progress_bar(value: float, max_value: float, theme: Dict[str, Any],
                       show_percentage: bool = True) -> ft.Control:
    """Crea una barra de progreso"""
    try:
        progress = min(value / max_value, 1.0) if max_value > 0 else 0.0
        percentage = progress * 100
        
        # Determinar color según el progreso
        if percentage <= 50:
            color = theme.get('success', ft.Colors.GREEN_600)
        elif percentage <= 80:
            color = theme.get('warning', ft.Colors.ORANGE_600)
        else:
            color = theme.get('danger', ft.Colors.RED_600)
        
        return ft.Column([
            ft.ProgressBar(
                value=progress,
                color=color,
                bgcolor=f"{color}20",
                height=8,
                border_radius=4
            ),
            ft.Text(
                f"{percentage:.1f}%",
                size=10,
                color=theme.get('text_secondary', ft.Colors.GREY_600)
            ) if show_percentage else ft.Container()
        ], spacing=4)
        
    except Exception:
        return ft.Container()

def sort_data(data: List[Dict[str, Any]], sort_field: str, 
              ascending: bool = True) -> List[Dict[str, Any]]:
    """Ordena una lista de diccionarios por un campo"""
    try:
        return sorted(data, key=lambda x: safe_float(x.get(sort_field, 0)), reverse=not ascending)
    except Exception:
        return data

def filter_data(data: List[Dict[str, Any]], filter_field: str, 
                filter_value: Any) -> List[Dict[str, Any]]:
    """Filtra una lista de diccionarios"""
    try:
        return [item for item in data if item.get(filter_field) == filter_value]
    except Exception:
        return data

def group_data_by_field(data: List[Dict[str, Any]], group_field: str) -> Dict[str, List[Dict[str, Any]]]:
    """Agrupa datos por un campo"""
    try:
        groups = {}
        for item in data:
            key = item.get(group_field, 'Sin clasificar')
            if key not in groups:
                groups[key] = []
            groups[key].append(item)
        return groups
    except Exception:
        return {}

def calculate_totals(data: List[Dict[str, Any]], fields: List[str]) -> Dict[str, float]:
    """Calcula totales para campos específicos"""
    try:
        totals = {}
        for field in fields:
            totals[field] = sum(safe_float(item.get(field, 0)) for item in data)
        return totals
    except Exception:
        return {field: 0.0 for field in fields}

def calculate_averages(data: List[Dict[str, Any]], fields: List[str]) -> Dict[str, float]:
    """Calcula promedios para campos específicos"""
    try:
        if not data:
            return {field: 0.0 for field in fields}
        
        averages = {}
        for field in fields:
            total = sum(safe_float(item.get(field, 0)) for item in data)
            averages[field] = total / len(data)
        return averages
    except Exception:
        return {field: 0.0 for field in fields}

def create_tooltip(text: str, theme: Dict[str, Any] = None) -> str:
    """Crea un tooltip con texto formateado"""
    return text

def get_period_text_for_charts(year: int, month: int, is_accumulated: bool = False) -> str:
    """Obtiene el texto del período para gráficos"""
    month_name = get_month_name(month)
    if is_accumulated:
        return f"Enero a {month_name} {year}"
    else:
        return f"{month_name} {year}"

def validate_period(year: int, month: int) -> bool:
    """Valida que el período sea válido"""
    try:
        current_year = datetime.now().year
        return (2020 <= year <= current_year + 1) and (1 <= month <= 12)
    except:
        return False

def get_default_theme() -> Dict[str, Any]:
    """Obtiene el tema por defecto"""
    return {
        'primary': ft.Colors.BLUE_600,
        'secondary': ft.Colors.INDIGO_600,
        'success': ft.Colors.GREEN_600,
        'warning': ft.Colors.ORANGE_600,
        'danger': ft.Colors.RED_600,
        'info': ft.Colors.CYAN_600,
        'light': ft.Colors.GREY_50,
        'dark': ft.Colors.GREY_800,
        'white': ft.Colors.WHITE,
        'black': ft.Colors.BLACK,
        'text_primary': ft.Colors.GREY_800,
        'text_secondary': ft.Colors.GREY_600,
        'border': ft.Colors.GREY_200,
        'background': ft.Colors.GREY_50
    }

