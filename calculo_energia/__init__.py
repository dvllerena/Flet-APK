"""
Módulo de Cálculo de Energía
Sistema de gestión de pérdidas eléctricas - Provincia de Matanzas
"""

from .models.energia_barra_model import EnergiaBarra
from .services.energia_service import EnergiaService
from .screens.energia_main_screen import EnergiaMainScreen
from .screens.energia_edit_screen import EnergiaEditScreen
from .screens.energia_view_screen import EnergiaViewScreen

__version__ = "1.0.0"
__author__ = "Sistema UNE Matanzas"

# Exportar clases principales
__all__ = [
    'EnergiaBarra',
    'EnergiaService', 
    'EnergiaMainScreen',
    'EnergiaEditScreen',
    'EnergiaViewScreen'
]

# Información del módulo
MODULE_INFO = {
    'name': 'Cálculo de Energía',
    'description': 'Gestión de registros de energía por municipio',
    'version': __version__,
    'screens': [
        {
            'name': 'energia_main',
            'title': 'Gestión de Energía',
            'description': 'Listado y gestión de registros de energía',
            'class': 'EnergiaMainScreen'
        },
        {
            'name': 'energia_edit', 
            'title': 'Editar Energía',
            'description': 'Crear/editar registros de energía',
            'class': 'EnergiaEditScreen'
        },
        {
            'name': 'energia_view',
            'title': 'Ver Energía', 
            'description': 'Visualizar registro de energía',
            'class': 'EnergiaViewScreen'
        }
    ]
}

def get_module_info():
    """Retorna información del módulo"""
    return MODULE_INFO

def get_available_screens():
    """Retorna las pantallas disponibles del módulo"""
    return MODULE_INFO['screens']


