"""
Módulo de Facturación
Gestiona la facturación menor, mayor y total por municipios
Incluye gestión de clientes y transferencias entre municipios
"""

from .models import (
    FacturacionModel,
    ClienteMunicipioModel, 
    TransferenciaMunicipioModel
)

from .services import (
    FacturacionService,
    get_facturacion_service
)

from .screens import (
    FacturacionMainScreen,
    FacturacionEditScreen,
    FacturacionTransfersScreen  # CORREGIDO: era FacturacionTransfersScreen
)

__all__ = [
    # Modelos
    'FacturacionModel',
    'ClienteMunicipioModel',
    'TransferenciaMunicipioModel',
    
    # Servicios
    'FacturacionService',
    'get_facturacion_service',
    
    # Pantallas
    'FacturacionMainScreen',
    'FacturacionEditScreen',
    'FacturacionTransfersScreen'  # CORREGIDO: era FacturacionTransfersScreen
]

# Información del módulo
__version__ = "1.0.0"
__author__ = "Sistema de Pérdidas Eléctricas - Matanzas"
__description__ = "Módulo para gestión de facturación eléctrica por municipios"

# Configuración del módulo
MODULE_CONFIG = {
    'name': 'Facturación',
    'description': 'Gestión de facturación eléctrica',
    'version': __version__,
    'screens': [
        {
            'name': 'facturacion',
            'title': 'Gestión de Facturación',
            'screen_class': 'FacturacionMainScreen',
            'icon': 'receipt_long'
        },
        {
            'name': 'facturacion_edit',
            'title': 'Editar Facturación',
            'screen_class': 'FacturacionEditScreen',
            'icon': 'edit'
        },
        {
            'name': 'facturacion_transfer',
            'title': 'Transferir Facturación',
            'screen_class': 'FacturacionTransfersScreen',  # CORREGIDO: era FacturacionTransferScreen
            'icon': 'swap_horiz'  # CORREGIDO: cambié el icono a uno más apropiado para transferencias
        }
    ],
    'permissions': [
        'facturacion_read',
        'facturacion_write',
        'facturacion_delete',
        'clientes_manage',
        'transferencias_manage'
    ]
}

def get_module_info():
    """Retorna información del módulo"""
    return MODULE_CONFIG

def register_screens(app):
    """Registra las pantallas del módulo en la aplicación"""
    from .screens import (
        FacturacionMainScreen,
        FacturacionEditScreen,
        FacturacionTransfersScreen  # AGREGADO: importar la pantalla de transferencias
    )
    
    # Registrar pantallas principales
    app.screen_manager.register_screen(
        "facturacion", 
        lambda **kwargs: FacturacionMainScreen(app, **kwargs)
    )
    
    app.screen_manager.register_screen(
        "facturacion_edit", 
        lambda **kwargs: FacturacionEditScreen(app, **kwargs)
    )
    
    # AGREGADO: Registrar pantalla de transferencias
    app.screen_manager.register_screen(
        "facturacion_transfer", 
        lambda **kwargs: FacturacionTransfersScreen(app, **kwargs)
    )
    
    return True

def initialize_module(db_manager):
    """Inicializa el módulo de facturación"""
    try:
        # Verificar que las tablas existan
        required_tables = [
            'facturacion',
            'clientes_municipio', 
            'transferencias_municipios'
        ]
        
        # Aquí podrías agregar validaciones adicionales
        # Por ejemplo, verificar permisos, configuraciones, etc.
        
        return True
        
    except Exception as e:
        print(f"Error al inicializar módulo de facturación: {e}")
        return False
