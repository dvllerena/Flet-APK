"""
Configuración para las pestañas de LVentas
"""

from typing import Dict, Any, List
import flet as ft

# Configuración de temas
THEMES = {
    'default': {
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
    },
    'dark': {
        'primary': ft.Colors.BLUE_400,
        'secondary': ft.Colors.INDIGO_400,
        'success': ft.Colors.GREEN_400,
        'warning': ft.Colors.ORANGE_400,
        'danger': ft.Colors.RED_400,
        'info': ft.Colors.CYAN_400,
        'light': ft.Colors.GREY_800,
        'dark': ft.Colors.GREY_200,
        'white': ft.Colors.GREY_900,
        'black': ft.Colors.WHITE,
        'text_primary': ft.Colors.WHITE,
        'text_secondary': ft.Colors.GREY_300,
        'border': ft.Colors.GREY_700,
        'background': ft.Colors.GREY_900
    }
}

# Configuración de pestañas
TAB_CONFIG = {
    'summary': {
        'title': 'Resumen',
        'icon': ft.Icons.DASHBOARD,
        'color': ft.Colors.BLUE_600,
        'description': 'Vista general del estado de pérdidas'
    },
    'monthly': {
        'title': 'Mensual',
        'icon': ft.Icons.CALENDAR_MONTH,
        'color': ft.Colors.GREEN_600,
        'description': 'Datos de pérdidas mensuales'
    },
    'accumulated': {
        'title': 'Acumulado',
        'icon': ft.Icons.TRENDING_UP,
        'color': ft.Colors.ORANGE_600,
        'description': 'Datos de pérdidas acumuladas'
    },
    'charts': {
        'title': 'Gráficos',
        'icon': ft.Icons.BAR_CHART,
        'color': ft.Colors.PURPLE_600,
        'description': 'Visualización gráfica de datos'
    }
}

# Configuración de campos de datos
DATA_FIELDS = {
    'monthly': {
        'required': ['municipio', 'energia_barra_mw', 'total_facturacion_mw', 'plan_mes', 'real_mes'],
        'optional': ['observaciones', 'fecha_actualizacion'],
        'display_names': {
            'municipio': 'Municipio',
            'energia_barra_mw': 'Energía Barra (MW)',
            'total_facturacion_mw': 'Facturación (MW)',
            'plan_mes': 'Plan (%)',
            'real_mes': 'Real (%)'
        }
    },
    'accumulated': {
        'required': ['municipio', 'energia_barra_acum_mw', 'plan_ventas', 'plan_perdidas_acum', 
                    'total_ventas_acum_mw', 'pct_real_ventas_acum', 'ahorro_energia'],
        'optional': ['observaciones', 'fecha_actualizacion'],
        'display_names': {
            'municipio': 'Municipio',
            'energia_barra_acum_mw': 'Energía Barra (MW)',
            'plan_ventas': 'Plan Ventas (MW)',
            'plan_perdidas_acum': 'Plan Pérdidas (%)',
            'total_ventas_acum_mw': 'Ventas Reales (MW)',
            'pct_real_ventas_acum': 'Pérdidas Reales (%)',
            'ahorro_energia': 'Ahorro (MW)'
        }
    }
}
# Configuración de gráficos
CHART_CONFIG = {
    'types': {
        'line': {
            'name': 'Líneas',
            'icon': ft.Icons.SHOW_CHART,
            'description': 'Gráfico de líneas para tendencias'
        },
        'bar': {
            'name': 'Barras',
            'icon': ft.Icons.BAR_CHART,
            'description': 'Gráfico de barras para comparaciones'
        },
        'pie': {
            'name': 'Circular',
            'icon': ft.Icons.PIE_CHART,
            'description': 'Gráfico circular para proporciones'
        }
    },
    'metrics': {
        'perdidas': {
            'name': 'Pérdidas',
            'unit': '%',
            'color': ft.Colors.RED_600,
            'description': 'Porcentaje de pérdidas'
        },
        'energia': {
            'name': 'Energía',
            'unit': 'MW',
            'color': ft.Colors.BLUE_600,
            'description': 'Energía en megavatios'
        },
        'facturacion': {
            'name': 'Facturación',
            'unit': 'MW',
            'color': ft.Colors.GREEN_600,
            'description': 'Facturación en megavatios'
        }
    },
    'colors': [
        ft.Colors.BLUE_600, ft.Colors.GREEN_600, ft.Colors.ORANGE_600,
        ft.Colors.RED_600, ft.Colors.PURPLE_600, ft.Colors.CYAN_600,
        ft.Colors.PINK_600, ft.Colors.TEAL_600, ft.Colors.INDIGO_600,
        ft.Colors.AMBER_600
    ]
}

# Configuración de exportación
EXPORT_CONFIG = {
    'formats': {
        'excel': {
            'name': 'Excel',
            'extension': '.xlsx',
            'mime_type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        },
        'csv': {
            'name': 'CSV',
            'extension': '.csv',
            'mime_type': 'text/csv'
        },
        'pdf': {
            'name': 'PDF',
            'extension': '.pdf',
            'mime_type': 'application/pdf'
        }
    },
    'default_filename': 'lventas_data'
}

# Configuración de validación
VALIDATION_CONFIG = {
    'ranges': {
        'year': {'min': 2020, 'max': 2030},
        'month': {'min': 1, 'max': 12},
        'percentage': {'min': 0, 'max': 100},
        'energy': {'min': 0, 'max': 10000}
    },
    'required_fields': {
        'monthly': ['municipio', 'energia_barra_mw', 'plan_mes', 'real_mes'],
        'accumulated': ['municipio', 'energia_barra_acum_mw', 'plan_perdidas_acum', 'pct_real_ventas_acum']
    }
}

# Configuración de mensajes
MESSAGES = {
    'loading': {
        'data': 'Cargando datos...',
        'chart': 'Generando gráfico...',
        'export': 'Exportando datos...',
        'refresh': 'Actualizando información...'
    },
    'success': {
        'data_loaded': 'Datos cargados correctamente',
        'chart_generated': 'Gráfico generado exitosamente',
        'export_completed': 'Exportación completada',
        'refresh_completed': 'Datos actualizados'
    },
    'error': {
        'data_load_failed': 'Error al cargar los datos',
        'chart_generation_failed': 'Error al generar el gráfico',
        'export_failed': 'Error en la exportación',
        'refresh_failed': 'Error al actualizar los datos',
        'invalid_period': 'Período seleccionado no válido',
        'no_data': 'No hay datos disponibles para el período seleccionado'
    },
    'warning': {
        'no_data': 'No hay datos disponibles',
        'partial_data': 'Datos incompletos para algunos municipios',
        'old_data': 'Los datos pueden estar desactualizados'
    }
}

# Configuración de formato de números
NUMBER_FORMAT = {
    'decimals': {
        'percentage': 2,
        'energy': 3,
        'currency': 2,
        'default': 2
    },
    'separators': {
        'thousands': ',',
        'decimal': '.'
    }
}

# Configuración de municipios (puede ser cargada desde BD)
MUNICIPALITIES = [
    'Matanzas', 'Cárdenas', 'Colón', 'Jagüey Grande', 'Jovellanos',
    'Limonar', 'Los Arabos', 'Martí', 'Pedro Betancourt', 'Perico',
    'Unión de Reyes', 'Calimete', 'Ciénaga de Zapata'
]

# Configuración de períodos
PERIOD_CONFIG = {
    'months': [
        {'value': 1, 'name': 'Enero', 'short': 'Ene'},
        {'value': 2, 'name': 'Febrero', 'short': 'Feb'},
        {'value': 3, 'name': 'Marzo', 'short': 'Mar'},
        {'value': 4, 'name': 'Abril', 'short': 'Abr'},
        {'value': 5, 'name': 'Mayo', 'short': 'May'},
        {'value': 6, 'name': 'Junio', 'short': 'Jun'},
        {'value': 7, 'name': 'Julio', 'short': 'Jul'},
        {'value': 8, 'name': 'Agosto', 'short': 'Ago'},
        {'value': 9, 'name': 'Septiembre', 'short': 'Sep'},
        {'value': 10, 'name': 'Octubre', 'short': 'Oct'},
        {'value': 11, 'name': 'Noviembre', 'short': 'Nov'},
        {'value': 12, 'name': 'Diciembre', 'short': 'Dic'}
    ],
    'default_year_range': 5  # Años hacia atrás desde el actual
}

# Configuración de alertas y notificaciones
ALERT_CONFIG = {
    'thresholds': {
        'high_losses': 15.0,  # Porcentaje de pérdidas considerado alto
        'critical_losses': 20.0,  # Porcentaje crítico
        'low_compliance': 70.0  # Porcentaje de cumplimiento bajo
    },
    'colors': {
        'normal': ft.Colors.GREEN_600,
        'warning': ft.Colors.ORANGE_600,
        'critical': ft.Colors.RED_600
    }
}

# Configuración de paginación
PAGINATION_CONFIG = {
    'default_page_size': 10,
    'page_size_options': [5, 10, 20, 50, 100],
    'max_visible_pages': 5
}

# Configuración de filtros
FILTER_CONFIG = {
    'compliance': {
        'all': 'Todos',
        'compliant': 'Cumplen',
        'non_compliant': 'No cumplen'
    },
    'performance': {
        'all': 'Todos',
        'excellent': 'Excelente (< 10%)',
        'good': 'Bueno (10-15%)',
        'regular': 'Regular (15-20%)',
        'poor': 'Deficiente (> 20%)'
    }
}

# Configuración de ordenamiento
SORT_CONFIG = {
    'options': {
        'municipio': 'Municipio',
        'perdidas_asc': 'Pérdidas (menor a mayor)',
        'perdidas_desc': 'Pérdidas (mayor a menor)',
        'energia_asc': 'Energía (menor a mayor)',
        'energia_desc': 'Energía (mayor a menor)',
        'cumplimiento': 'Cumplimiento'
    },
    'default': 'municipio'
}

# Configuración de búsqueda
SEARCH_CONFIG = {
    'placeholder': 'Buscar municipio...',
    'min_chars': 2,
    'fields': ['municipio']  # Campos en los que buscar
}

# Configuración de cache
CACHE_CONFIG = {
    'enabled': True,
    'ttl': 300,  # Tiempo de vida en segundos (5 minutos)
    'max_size': 100  # Máximo número de entradas en cache
}

# Configuración de logging específica para pestañas
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': 'lventas_tabs.log'
}

# Configuración de animaciones
ANIMATION_CONFIG = {
    'enabled': True,
    'duration': 300,  # Duración en milisegundos
    'curve': ft.AnimationCurve.EASE_IN_OUT
}

# Configuración de responsive design
RESPONSIVE_CONFIG = {
    'breakpoints': {
        'mobile': 600,
        'tablet': 900,
        'desktop': 1200
    },
    'grid_columns': {
        'mobile': 1,
        'tablet': 2,
        'desktop': 3
    }
}

# Configuración de accesibilidad
ACCESSIBILITY_CONFIG = {
    'high_contrast': False,
    'large_text': False,
    'screen_reader_support': True
}

def get_theme(theme_name: str = 'default') -> Dict[str, Any]:
    """Obtiene la configuración del tema"""
    return THEMES.get(theme_name, THEMES['default'])

def get_tab_config(tab_name: str) -> Dict[str, Any]:
    """Obtiene la configuración de una pestaña"""
    return TAB_CONFIG.get(tab_name, {})

def get_chart_colors(count: int) -> List[str]:
    """Obtiene una lista de colores para gráficos"""
    colors = CHART_CONFIG['colors']
    return [colors[i % len(colors)] for i in range(count)]

def get_message(category: str, key: str) -> str:
    """Obtiene un mensaje de la configuración"""
    return MESSAGES.get(category, {}).get(key, f"Mensaje no encontrado: {category}.{key}")

def validate_period_range(year: int, month: int) -> bool:
    """Valida que el período esté en el rango permitido"""
    year_range = VALIDATION_CONFIG['ranges']['year']
    month_range = VALIDATION_CONFIG['ranges']['month']
    
    return (year_range['min'] <= year <= year_range['max'] and 
            month_range['min'] <= month <= month_range['max'])

def get_municipality_list() -> List[str]:
    """Obtiene la lista de municipios"""
    return MUNICIPALITIES.copy()

def get_month_name(month: int) -> str:
    """Obtiene el nombre del mes"""
    for m in PERIOD_CONFIG['months']:
        if m['value'] == month:
            return m['name']
    return f"Mes {month}"

def get_month_short_name(month: int) -> str:
    """Obtiene el nombre corto del mes"""
    for m in PERIOD_CONFIG['months']:
        if m['value'] == month:
            return m['short']
    return f"M{month}"

def get_alert_level(losses_percentage: float) -> str:
    """Determina el nivel de alerta según el porcentaje de pérdidas"""
    thresholds = ALERT_CONFIG['thresholds']
    
    if losses_percentage >= thresholds['critical_losses']:
        return 'critical'
    elif losses_percentage >= thresholds['high_losses']:
        return 'warning'
    else:
        return 'normal'

def get_alert_color(alert_level: str) -> str:
    """Obtiene el color según el nivel de alerta"""
    return ALERT_CONFIG['colors'].get(alert_level, ALERT_CONFIG['colors']['normal'])

def format_number_by_type(value: float, number_type: str = 'default') -> str:
    """Formatea un número según su tipo"""
    decimals = NUMBER_FORMAT['decimals'].get(number_type, NUMBER_FORMAT['decimals']['default'])
    
    try:
        # Formatear con separadores de miles
        formatted = f"{value:,.{decimals}f}"
        
        # Reemplazar separadores según configuración
        thousands_sep = NUMBER_FORMAT['separators']['thousands']
        decimal_sep = NUMBER_FORMAT['separators']['decimal']
        
        if decimal_sep != '.':
            formatted = formatted.replace('.', '|TEMP|')
            formatted = formatted.replace(',', thousands_sep)
            formatted = formatted.replace('|TEMP|', decimal_sep)
        elif thousands_sep != ',':
            formatted = formatted.replace(',', thousands_sep)
            
        return formatted
    except:
        return str(value)

def get_default_page_size() -> int:
    """Obtiene el tamaño de página por defecto"""
    return PAGINATION_CONFIG['default_page_size']

def get_page_size_options() -> List[int]:
    """Obtiene las opciones de tamaño de página"""
    return PAGINATION_CONFIG['page_size_options'].copy()

def is_cache_enabled() -> bool:
    """Verifica si el cache está habilitado"""
    return CACHE_CONFIG['enabled']

def get_cache_ttl() -> int:
    """Obtiene el tiempo de vida del cache"""
    return CACHE_CONFIG['ttl']

def are_animations_enabled() -> bool:
    """Verifica si las animaciones están habilitadas"""
    return ANIMATION_CONFIG['enabled']

def get_animation_duration() -> int:
    """Obtiene la duración de las animaciones"""
    return ANIMATION_CONFIG['duration']

def get_responsive_columns(screen_width: int) -> int:
    """Obtiene el número de columnas según el ancho de pantalla"""
    breakpoints = RESPONSIVE_CONFIG['breakpoints']
    columns = RESPONSIVE_CONFIG['grid_columns']
    
    if screen_width < breakpoints['mobile']:
        return columns['mobile']
    elif screen_width < breakpoints['tablet']:
        return columns['tablet']
    else:
        return columns['desktop']
