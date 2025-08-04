"""
Pantallas del módulo de Cálculo de Energía
"""

from .energia_main_screen import EnergiaMainScreen
from .energia_edit_screen import EnergiaEditScreen  
from .energia_view_screen import EnergiaViewScreen

__all__ = [
    'EnergiaMainScreen',
    'EnergiaEditScreen', 
    'EnergiaViewScreen'
]

# Información de las pantallas
SCREENS_INFO = {
    'EnergiaMainScreen': {
        'route': 'energia_main',
        'title': 'Gestión de Energía',
        'description': 'Pantalla principal para gestión de registros de energía',
        'icon': 'electric_bolt',
        'permissions': ['energia.view', 'energia.create', 'energia.edit', 'energia.delete'],
        'features': [
            'Listado de registros',
            'Filtros por período',
            'Búsqueda por municipio', 
            'Resumen estadístico',
            'Importación Excel',
            'Exportación Excel',
            'CRUD completo'
        ]
    },
    'EnergiaEditScreen': {
        'route': 'energia_edit',
        'title': 'Editar Energía',
        'description': 'Pantalla para crear/editar registros de energía',
        'icon': 'edit',
        'permissions': ['energia.create', 'energia.edit'],
        'modes': ['create', 'edit'],
        'validation': True,
        'features': [
            'Formulario validado',
            'Selección de municipio',
            'Validación de duplicados',
            'Campos obligatorios',
            'Observaciones opcionales'
        ]
    },
    'EnergiaViewScreen': {
        'route': 'energia_view', 
        'title': 'Ver Energía',
        'description': 'Pantalla para visualizar registros de energía',
        'icon': 'visibility',
        'permissions': ['energia.view'],
        'read_only': True,
        'features': [
            'Vista detallada',
            'Información completa',
            'Estadísticas del período',
            'Acciones rápidas',
            'Exportación individual'
        ]
    }
}

def get_screens_info():
    """Retorna información de las pantallas"""
    return SCREENS_INFO

def get_screen_info(screen_name: str):
    """Retorna información de una pantalla específica"""
    return SCREENS_INFO.get(screen_name, {})

def get_screen_routes():
    """Retorna las rutas disponibles"""
    return {name: info['route'] for name, info in SCREENS_INFO.items()}

def get_screens_by_permission(permission: str):
    """Retorna pantallas que requieren un permiso específico"""
    result = []
    for name, info in SCREENS_INFO.items():
        if permission in info.get('permissions', []):
            result.append({
                'name': name,
                'route': info['route'],
                'title': info['title']
            })
    return result

def create_screen(screen_name: str, app, params=None):
    """Factory method para crear instancias de pantallas"""
    screens = {
        'EnergiaMainScreen': EnergiaMainScreen,
        'EnergiaEditScreen': EnergiaEditScreen,
        'EnergiaViewScreen': EnergiaViewScreen
    }
    
    screen_class = screens.get(screen_name)
    if screen_class:
        if screen_name == 'EnergiaMainScreen':
            return screen_class(app)
        else:
            return screen_class(app, params)
    
    raise ValueError(f"Pantalla no encontrada: {screen_name}")

