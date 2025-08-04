"""
Servicios del módulo de Cálculo de Energía
"""

from .energia_service import EnergiaService

__all__ = ['EnergiaService']

# Información de los servicios - CORREGIDA
SERVICES_INFO = {
    'EnergiaService': {
        'description': 'Servicio para gestión de registros de energía',
        'methods': [
            'get_energia_list',                 # ✅ Existe
            'get_energia_by_periodo',           # ✅ Existe  
            'get_energia_by_id',                # ✅ Existe
            'crear_energia',                    # ✅ Existe
            'actualizar_energia',               # ✅ Existe
            'eliminar_energia',                 # ✅ Existe
            'get_municipios',                   # ✅ Existe
            'get_resumen_periodo',              # ✅ Existe
            'get_periodos_disponibles',         # ✅ Existe
            'validar_periodo_completo',         # ✅ Existe
            'importar_desde_excel',             # ✅ Existe
            'exportar_a_excel',                 # ✅ Existe
            'validar_datos_periodo',            # ✅ Existe
            'get_estadisticas_anuales',         # ✅ Existe
            'buscar_registros',                 # ✅ Existe
            'duplicar_periodo',                 # ✅ Existe
            'generar_plantilla_excel',          # ✅ Existe
            'get_historial_cambios',            # ✅ Existe
            'calcular_tendencias'               # ✅ Existe
        ],
        'dependencies': ['core.database', 'core.logger'],
        'excel_support': True,
        'validation': True
    }
}

def get_services_info():
    """Retorna información de los servicios"""
    return SERVICES_INFO

def get_service_methods(service_name: str):
    """Retorna los métodos disponibles de un servicio"""
    return SERVICES_INFO.get(service_name, {}).get('methods', [])

def create_energia_service():
    """Factory method para crear instancia del servicio"""
    return EnergiaService()
