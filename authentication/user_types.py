"""
Tipos y constantes relacionadas con usuarios
"""

from enum import Enum

class UserType(Enum):
    """Tipos de usuario en el sistema"""
    ADMINISTRADOR = "administrador"
    SUPERVISOR = "supervisor"
    OPERADOR = "operador"
    CONSULTA = "consulta"

class UserPermissions:
    """Permisos por tipo de usuario"""
    
    ADMINISTRADOR = [
        "manage_users",
        "manage_system",
        "view_all_data",
        "export_data",
        "manage_settings",
        "view_reports",
        "manage_data"
    ]
    
    SUPERVISOR = [
        "view_all_data",
        "export_data",
        "view_reports",
        "manage_data",
        "view_dashboard"
    ]
    
    OPERADOR = [
        "view_dashboard",
        "input_data",
        "view_own_data"
    ]
    
    CONSULTA = [
        "view_dashboard",
        "view_reports"
    ]
    
    @classmethod
    def get_permissions(cls, user_type: str) -> list:
        """Obtiene los permisos para un tipo de usuario"""
        return getattr(cls, user_type.upper(), [])

# Municipios de Matanzas
MUNICIPIOS_MATANZAS = [
    {"codigo": "MAT", "nombre": "Matanzas"},
    {"codigo": "CAR", "nombre": "Cárdenas"},
    {"codigo": "VAR", "nombre": "Varadero"},
    {"codigo": "COL", "nombre": "Colón"},
    {"codigo": "JAG", "nombre": "Jagüey Grande"},
    {"codigo": "JOV", "nombre": "Jovellanos"},
    {"codigo": "LIS", "nombre": "Limonar"},
    {"codigo": "LOS", "nombre": "Los Arabos"},
    {"codigo": "MAR", "nombre": "Martí"},
    {"codigo": "PED", "nombre": "Pedro Betancourt"},
    {"codigo": "PER", "nombre": "Perico"},
    {"codigo": "UNI", "nombre": "Unión de Reyes"},
    {"codigo": "CIE", "nombre": "Ciénaga de Zapata"}
]

