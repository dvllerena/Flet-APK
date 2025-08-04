"""
Configuración del módulo de Cálculo de Energía
"""

# Configuración de la tabla
TABLE_CONFIG = {
    'name': 'energia_barra',
    'display_name': 'Energía por Barra',
    'description': 'Registros de energía consumida por municipio',
    'icon': 'electric_bolt',
    'color': 'blue'
}

# Configuración de campos
FIELD_CONFIG = {
    'energia_mwh': {
        'label': 'Energía (MWh)',
        'type': 'float',
        'required': True,
        'min_value': 0,
        'max_value': 10000,
        'decimal_places': 1,
        'suffix': 'MWh'
    },
    'observaciones': {
        'label': 'Observaciones',
        'type': 'text',
        'required': False,
        'max_length': 500,
        'multiline': True
    }
}

# Configuración de validación
VALIDATION_CONFIG = {
    'allow_duplicates': False,
    'unique_fields': ['municipio_id', 'año', 'mes'],
    'required_fields': ['municipio_id', 'año', 'mes', 'energia_mwh'],
    'date_range': {
        'min_year': 2000,
        'max_year': 2100
    }
}

# Configuración de Excel
EXCEL_CONFIG = {
    'import': {
        'supported_formats': ['.xlsx', '.xls'],
        'required_columns': ['Municipio', 'Año', 'Mes', 'Energía'],
        'optional_columns': ['Observaciones'],
        'sheet_name': 'Energía',
        'start_row': 2
    },
    'export': {
        'default_format': '.xlsx',
        'include_headers': True,
        'sheet_name': 'Energía',
        'columns': [
            'ID', 'Municipio', 'Código', 'Año', 'Mes', 
            'Energía (MWh)', 'Observaciones', 'Fecha Registro'
        ]
    }
}

# Configuración de permisos
PERMISSIONS_CONFIG = {
    'energia.view': 'Ver registros de energía',
    'energia.create': 'Crear registros de energía', 
    'energia.edit': 'Editar registros de energía',
    'energia.delete': 'Eliminar registros de energía',
    'energia.import': 'Importar desde Excel',
    'energia.export': 'Exportar a Excel'
}

def get_table_config():
    """Retorna configuración de la tabla"""
    return TABLE_CONFIG

def get_field_config(field_name: str = None):
    """Retorna configuración de campos"""
    if field_name:
        return FIELD_CONFIG.get(field_name, {})
    return FIELD_CONFIG

def get_validation_config():
    """Retorna configuración de validación"""
    return VALIDATION_CONFIG

def get_excel_config():
    """Retorna configuración de Excel"""
    return EXCEL_CONFIG

def get_permissions_config():
    """Retorna configuración de permisos"""
    return PERMISSIONS_CONFIG
