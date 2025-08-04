"""
Migración: Crear tabla de transferencias de consumos
Fecha: 2024-10-XX
Descripción: Tabla para almacenar consumos importados desde Excel
"""

import sqlite3
from core.logger import get_logger

def up(conn: sqlite3.Connection):
    """Ejecuta la migración - crear tabla"""
    logger = get_logger(__name__)
    
    try:
        # Crear tabla principal
        conn.execute("""
            CREATE TABLE IF NOT EXISTS transferencias_consumos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                servicio_id TEXT NOT NULL,
                año INTEGER NOT NULL,
                mes INTEGER NOT NULL,
                consumo_kwh REAL DEFAULT 0.0,
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                usuario_id INTEGER,
                observaciones TEXT,
                origen TEXT,
                destino TEXT,
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id),
                UNIQUE(servicio_id, año, mes)
            )
        """)
        
        # Crear índices para optimizar consultas
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_transferencias_periodo 
            ON transferencias_consumos (año, mes)
        """)
        
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_transferencias_servicio 
            ON transferencias_consumos (servicio_id)
        """)
        
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_transferencias_usuario 
            ON transferencias_consumos (usuario_id)
        """)
        
        conn.commit()
        logger.info("✅ Tabla transferencias_consumos creada exitosamente")
        
    except Exception as e:
        logger.error(f"❌ Error al crear tabla transferencias_consumos: {e}")
        raise

def down(conn: sqlite3.Connection):
    """Revierte la migración - eliminar tabla"""
    logger = get_logger(__name__)
    
    try:
        # Eliminar índices
        conn.execute("DROP INDEX IF EXISTS idx_transferencias_periodo")
        conn.execute("DROP INDEX IF EXISTS idx_transferencias_servicio") 
        conn.execute("DROP INDEX IF EXISTS idx_transferencias_usuario")
        
        # Eliminar tabla
        conn.execute("DROP TABLE IF EXISTS transferencias_consumos")
        
        conn.commit()
        logger.info("✅ Tabla transferencias_consumos eliminada exitosamente")
        
    except Exception as e:
        logger.error(f"❌ Error al eliminar tabla transferencias_consumos: {e}")
        raise
