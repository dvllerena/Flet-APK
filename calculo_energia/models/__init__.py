"""
Modelos del módulo de Cálculo de Energía
"""

from .energia_barra_model import EnergiaBarra

__all__ = ['EnergiaBarra']

# Información de los modelos
MODELS_INFO = {
    'EnergiaBarra': {
        'description': 'Modelo para registros de energía por municipio',
        'table': 'energia_barra',
        'fields': [
            'id', 'municipio_id', 'año', 'mes', 'energia_mwh',
            'observaciones', 'fecha_registro', 'fecha_modificacion', 'usuario_id'
        ],
        'required_fields': ['municipio_id', 'año', 'mes', 'energia_mwh'],
        'relationships': {
            'municipio': 'municipios.id',
            'usuario': 'usuarios.id'
        }
    }
}

def get_models_info():
    """Retorna información de los modelos"""
    return MODELS_INFO

def get_model_fields(model_name: str):
    """Retorna los campos de un modelo específico"""
    return MODELS_INFO.get(model_name, {}).get('fields', [])

def get_required_fields(model_name: str):
    """Retorna los campos requeridos de un modelo"""
    return MODELS_INFO.get(model_name, {}).get('required_fields', [])

