"""
Seeds para datos de facturación
"""
from core.logger import get_logger
from core.database import get_db_manager

def seed_facturacion_data():
    """Inserta datos de ejemplo para facturación"""
    logger = get_logger(__name__)
    db_manager = get_db_manager()
    
    # Aquí irían los datos de ejemplo de facturación si los necesitas
    logger.info("Seeds de facturación - listo para datos")
    pass

def seed_tipos_facturacion():
    """Inserta tipos de facturación si tienes una tabla para eso"""
    logger = get_logger(__name__)
    db_manager = get_db_manager()
    
    # Si tienes tabla de tipos de facturación, aquí van los datos
    pass

def seed_configuraciones_facturacion():
    """Inserta configuraciones específicas de facturación"""
    logger = get_logger(__name__)
    db_manager = get_db_manager()
    
    # Configuraciones específicas de facturación
    configuraciones_facturacion = [
        ('facturacion_menor_defecto', '0', 'Valor por defecto facturación menor'),
        ('facturacion_mayor_defecto', '0', 'Valor por defecto facturación mayor'),
        ('moneda_facturacion', 'CUP', 'Moneda para facturación'),
    ]
    
    for clave, valor, descripcion in configuraciones_facturacion:
        # Verificar si ya existe
        existing = db_manager.execute_query(
            "SELECT id FROM configuraciones WHERE clave = ?", 
            (clave,)
        )
        
        if not existing:
            db_manager.execute_update(
                "INSERT INTO configuraciones (clave, valor, descripcion) VALUES (?, ?, ?)",
                (clave, valor, descripcion)
            )
            logger.info(f"Configuración de facturación creada: {clave}")
