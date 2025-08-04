"""
Gestor de migraciones híbrido - SQLite + Web
"""
import sqlite3
from pathlib import Path
from core.logger import get_logger

def run_migrations(db_path: str, web_mode: bool = False):
    """Ejecuta todas las migraciones según el modo"""
    logger = get_logger(__name__)
    
    if web_mode:
        logger.info("Modo web detectado - Las migraciones se manejan en WebStorageManager")
        return
    
    logger.info("Ejecutando migraciones para SQLite...")
    
    # Crear conexión SQLite
    conn = sqlite3.connect(db_path)
    
    try:
        # 1. Crear tablas del CORE
        _create_core_tables(conn)
        
        # 2. Crear tablas de CALCULO ENERGIA
        _create_energia_tables(conn)
        
        # 3. Crear tablas de FACTURACIÓN
        _create_facturacion_tables(conn)
        
        # 4. Crear tabla de transferencias de consumos
        _create_transferencias_consumos_table(conn)
        
        # 5. Crear tablas de INFOPERDIDAS
        _create_infoperdidas_tables(conn)
        
        # 6. Crear tablas de LVENTAS
        _create_lventas_tables(conn)
       
        logger.info("✅ Migraciones SQLite completadas")
        
    except Exception as e:
        logger.error(f"❌ Error en migraciones SQLite: {e}")
        raise
    finally:
        conn.close()

def _create_core_tables(conn):
    """Crea las tablas básicas del sistema"""
    logger = get_logger(__name__)
    logger.info("Creando tablas del core...")
    
    # Tabla de usuarios
    conn.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            nombre_completo TEXT NOT NULL,
            email TEXT,
            tipo_usuario TEXT NOT NULL DEFAULT 'operador',
            activo INTEGER DEFAULT 1,
            fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
            ultimo_acceso DATETIME
        )
    """)
    
    # Tabla de municipios
    conn.execute("""
        CREATE TABLE IF NOT EXISTS municipios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT UNIQUE NOT NULL,
            nombre TEXT NOT NULL,
            provincia TEXT DEFAULT 'Matanzas',
            activo INTEGER DEFAULT 1,
            fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Tabla de configuraciones
    conn.execute("""
        CREATE TABLE IF NOT EXISTS configuraciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            clave TEXT UNIQUE NOT NULL,
            valor TEXT,
            descripcion TEXT,
            fecha_modificacion DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Tabla de logs
    conn.execute("""
        CREATE TABLE IF NOT EXISTS logs_sistema (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            accion TEXT NOT NULL,
            modulo TEXT,
            detalles TEXT,
            fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
        )
    """)
    
    # Índices para optimización
    conn.execute("CREATE INDEX IF NOT EXISTS idx_usuarios_username ON usuarios (username)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_municipios_codigo ON municipios (codigo)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_logs_fecha ON logs_sistema (fecha)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_logs_usuario ON logs_sistema (usuario_id)")
    
    conn.commit()
    logger.info("✅ Tablas del core creadas")

def _create_energia_tables(conn):
    """Crea las tablas del módulo de energía"""
    logger = get_logger(__name__)
    logger.info("Creando tablas de energía...")
    
    # Tabla de energía en barra
    conn.execute("""
        CREATE TABLE IF NOT EXISTS energia_barra (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            municipio_id INTEGER NOT NULL,
            año INTEGER NOT NULL,
            mes INTEGER NOT NULL,
            energia_mwh REAL DEFAULT 0.0,
            observaciones TEXT,
            usuario_id INTEGER,
            fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
            fecha_modificacion DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (municipio_id) REFERENCES municipios (id),
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id),
            UNIQUE(municipio_id, año, mes)
        )
    """)
    
    # Índices para energía
    conn.execute("CREATE INDEX IF NOT EXISTS idx_energia_periodo ON energia_barra (año, mes)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_energia_municipio ON energia_barra (municipio_id)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_energia_usuario ON energia_barra (usuario_id)")
    
    conn.commit()
    logger.info("✅ Tablas de energía creadas")

def _create_facturacion_tables(conn):
    """Crea las tablas del módulo de facturación"""
    logger = get_logger(__name__)
    logger.info("Creando tablas de facturación...")
    
    # Tabla principal de facturación
    conn.execute("""
        CREATE TABLE IF NOT EXISTS facturacion (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            municipio_id INTEGER NOT NULL,
            año INTEGER NOT NULL,
            mes INTEGER NOT NULL,
            facturacion_menor REAL DEFAULT 0,
            facturacion_mayor REAL DEFAULT 0,
            facturacion_total REAL DEFAULT 0,
            observaciones TEXT,
            usuario_id INTEGER,
            fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
            fecha_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (municipio_id) REFERENCES municipios(id),
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
            UNIQUE(municipio_id, año, mes)
        )
    """)
    
    # Tabla de clientes por municipio
    conn.execute("""
        CREATE TABLE IF NOT EXISTS clientes_municipio (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            municipio_id INTEGER NOT NULL,
            codigo_cliente TEXT NOT NULL,
            nombre_cliente TEXT NOT NULL,
            consumo_kwh REAL DEFAULT 0,
            activo INTEGER DEFAULT 1,
            observaciones TEXT,
            fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (municipio_id) REFERENCES municipios (id),
            UNIQUE(municipio_id, codigo_cliente)
        )
    """)
    
    # Tabla de transferencias entre municipios
    conn.execute("""
        CREATE TABLE IF NOT EXISTS transferencias_municipios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER NOT NULL,
            municipio_origen_id INTEGER NOT NULL,
            municipio_destino_id INTEGER NOT NULL,
            consumo_transferido REAL NOT NULL,
            año INTEGER NOT NULL,
            mes INTEGER NOT NULL,
            motivo TEXT,
            usuario_id INTEGER,
            fecha_transferencia DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (cliente_id) REFERENCES clientes_municipio (id),
            FOREIGN KEY (municipio_origen_id) REFERENCES municipios (id),
            FOREIGN KEY (municipio_destino_id) REFERENCES municipios (id),
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
        )
    """)
    
    # Índices para facturación
    conn.execute("CREATE INDEX IF NOT EXISTS idx_facturacion_periodo ON facturacion (año, mes)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_facturacion_municipio ON facturacion (municipio_id)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_clientes_municipio ON clientes_municipio (municipio_id)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_transferencias_periodo ON transferencias_municipios (año, mes)")
    
    conn.commit()
    logger.info("✅ Tablas de facturación creadas")

def _create_transferencias_consumos_table(conn):
    """Crea la tabla de transferencias de consumos"""
    logger = get_logger(__name__)
    logger.info("Creando tabla de transferencias de consumos...")
    
    try:
        # Tabla principal de consumos de transferencias
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

def _create_infoperdidas_tables(conn):
    """Crea las tablas del módulo de InfoPérdidas"""
    logger = get_logger(__name__)
    logger.info("Creando tablas de InfoPérdidas...")
    
    try:
        # Tabla de planes de pérdidas
        conn.execute("""
            CREATE TABLE IF NOT EXISTS planes_perdidas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                municipio_id INTEGER,
                año INTEGER NOT NULL,
                mes INTEGER NOT NULL,
                plan_perdidas_pct REAL NOT NULL DEFAULT 0,
                observaciones TEXT,
                usuario_id INTEGER,
                fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
                fecha_modificacion DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (municipio_id) REFERENCES municipios (id),
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id),
                UNIQUE(municipio_id, año, mes)
            )
        """)
        
        # Tabla de cálculos de pérdidas
        conn.execute("""
            CREATE TABLE IF NOT EXISTS calculos_perdidas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                municipio_id INTEGER NOT NULL,
                año INTEGER NOT NULL,
                mes INTEGER NOT NULL,
                energia_barra_mwh REAL DEFAULT 0,
                facturacion_mayor REAL DEFAULT 0,
                facturacion_menor REAL DEFAULT 0,
                total_ventas REAL DEFAULT 0,
                perdidas_distribucion_mwh REAL DEFAULT 0,
                perdidas_pct REAL DEFAULT 0,
                plan_perdidas_pct REAL DEFAULT 0,
                energia_barra_acumulada REAL DEFAULT 0,
                perdidas_acumuladas_mwh REAL DEFAULT 0,
                perdidas_acumuladas_pct REAL DEFAULT 0,
                plan_perdidas_acumulado_pct REAL DEFAULT 0,
                usuario_id INTEGER,
                fecha_calculo DATETIME DEFAULT CURRENT_TIMESTAMP,
                fecha_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (municipio_id) REFERENCES municipios (id),
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id),
                UNIQUE(municipio_id, año, mes)
            )
        """)
        
        # Tabla de resumen provincial de pérdidas
        conn.execute("""
            CREATE TABLE IF NOT EXISTS resumen_perdidas_provincial (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                año INTEGER NOT NULL,
                mes INTEGER NOT NULL,
                total_energia_barra REAL DEFAULT 0,
                total_facturacion_mayor REAL DEFAULT 0,
                total_facturacion_menor REAL DEFAULT 0,
                total_ventas REAL DEFAULT 0,
                total_perdidas_mwh REAL DEFAULT 0,
                total_perdidas_pct REAL DEFAULT 0,
                total_plan_perdidas_pct REAL DEFAULT 0,
                total_energia_acumulada REAL DEFAULT 0,
                total_perdidas_acumuladas_mwh REAL DEFAULT 0,
                total_perdidas_acumuladas_pct REAL DEFAULT 0,
                total_plan_acumulado_pct REAL DEFAULT 0,
                usuario_id INTEGER,
                fecha_calculo DATETIME DEFAULT CURRENT_TIMESTAMP,
                fecha_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id),
                UNIQUE(año, mes)
            )
        """)
        
        # Crear índices para optimizar consultas
        conn.execute("CREATE INDEX IF NOT EXISTS idx_planes_perdidas_periodo ON planes_perdidas (año, mes)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_planes_perdidas_municipio ON planes_perdidas (municipio_id)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_calculos_perdidas_periodo ON calculos_perdidas (año, mes)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_calculos_perdidas_municipio ON calculos_perdidas (municipio_id)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_resumen_provincial_periodo ON resumen_perdidas_provincial (año, mes)")
        
        conn.commit()
        logger.info("✅ Tablas de InfoPérdidas creadas exitosamente")
        
    except Exception as e:
        logger.error(f"❌ Error creando tablas de InfoPérdidas: {e}")
        raise

def _create_lventas_tables(conn):
    """Crea las tablas del módulo de Línea de Ventas"""
    logger = get_logger(__name__)
    logger.info("Creando tablas de Línea de Ventas...")
    
    try:
        # Tabla de líneas de venta
        conn.execute("""
            CREATE TABLE IF NOT EXISTS lineas_venta (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                municipio_id INTEGER NOT NULL,
                codigo_linea TEXT NOT NULL,
                nombre_linea TEXT NOT NULL,
                tension_kv REAL DEFAULT 0,
                longitud_km REAL DEFAULT 0,
                activa INTEGER DEFAULT 1,
                observaciones TEXT,
                usuario_id INTEGER,
                fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
                fecha_modificacion DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (municipio_id) REFERENCES municipios (id),
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id),
                UNIQUE(municipio_id, codigo_linea)
            )
        """)
        
        # Tabla de mediciones de líneas
        conn.execute("""
            CREATE TABLE IF NOT EXISTS mediciones_lineas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                linea_id INTEGER NOT NULL,
                año INTEGER NOT NULL,
                mes INTEGER NOT NULL,
                energia_entregada_mwh REAL DEFAULT 0,
                energia_facturada_mwh REAL DEFAULT 0,
                perdidas_mwh REAL DEFAULT 0,
                perdidas_pct REAL DEFAULT 0,
                observaciones TEXT,
                usuario_id INTEGER,
                fecha_medicion DATETIME DEFAULT CURRENT_TIMESTAMP,
                fecha_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (linea_id) REFERENCES lineas_venta (id),
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id),
                UNIQUE(linea_id, año, mes)
            )
        """)
        
        # Tabla de transformadores por línea
        conn.execute("""
            CREATE TABLE IF NOT EXISTS transformadores_linea (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                linea_id INTEGER NOT NULL,
                codigo_transformador TEXT NOT NULL,
                potencia_kva REAL DEFAULT 0,
                ubicacion TEXT,
                activo INTEGER DEFAULT 1,
                observaciones TEXT,
                usuario_id INTEGER,
                fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (linea_id) REFERENCES lineas_venta (id),
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id),
                UNIQUE(linea_id, codigo_transformador)
            )
        """)
        
        # Crear índices para optimizar consultas
        conn.execute("CREATE INDEX IF NOT EXISTS idx_lineas_municipio ON lineas_venta (municipio_id)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_lineas_codigo ON lineas_venta (codigo_linea)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_mediciones_periodo ON mediciones_lineas (año, mes)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_mediciones_linea ON mediciones_lineas (linea_id)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_transformadores_linea ON transformadores_linea (linea_id)")
        
        conn.commit()
        logger.info("✅ Tablas de Línea de Ventas creadas exitosamente")
        
    except Exception as e:
        logger.error(f"❌ Error creando tablas de Línea de Ventas: {e}")
        raise

# ✅ FUNCIONES DE UTILIDAD PARA MIGRACIONES
def check_table_exists(conn, table_name: str) -> bool:
    """Verifica si una tabla existe en la base de datos"""
    try:
        cursor = conn.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name=?
        """, (table_name,))
        return cursor.fetchone() is not None
    except Exception:
        return False

def get_table_info(conn, table_name: str) -> List[Dict[str, Any]]:
    """Obtiene información sobre las columnas de una tabla"""
    try:
        cursor = conn.execute(f"PRAGMA table_info({table_name})")
        columns = []
        for row in cursor.fetchall():
            columns.append({
                "cid": row[0],
                "name": row[1],
                "type": row[2],
                "notnull": row[3],
                "dflt_value": row[4],
                "pk": row[5]
            })
        return columns
    except Exception:
        return []

def backup_table(conn, table_name: str) -> bool:
    """Crea una copia de seguridad de una tabla"""
    try:
        backup_name = f"{table_name}_backup_{int(datetime.now().timestamp())}"
        conn.execute(f"CREATE TABLE {backup_name} AS SELECT * FROM {table_name}")
        conn.commit()
        return True
    except Exception as e:
        logger = get_logger(__name__)
        logger.error(f"Error creando backup de {table_name}: {e}")
        return False

def drop_table_if_exists(conn, table_name: str) -> bool:
    """Elimina una tabla si existe"""
    try:
        conn.execute(f"DROP TABLE IF EXISTS {table_name}")
        conn.commit()
        return True
    except Exception as e:
        logger = get_logger(__name__)
        logger.error(f"Error eliminando tabla {table_name}: {e}")
        return False

def get_migration_status() -> Dict[str, Any]:
    """Obtiene el estado de las migraciones"""
    return {
        "version": "1.0.0",
        "last_migration": "2024-01-01",
        "tables_created": [
            "usuarios", "municipios", "configuraciones", "logs_sistema",
            "energia_barra", "facturacion", "clientes_municipio", 
            "transferencias_municipios", "transferencias_consumos",
            "planes_perdidas", "calculos_perdidas", "resumen_perdidas_provincial",
            "lineas_venta", "mediciones_lineas", "transformadores_linea"
        ],
        "indexes_created": [
            "idx_usuarios_username", "idx_municipios_codigo", "idx_logs_fecha",
            "idx_energia_periodo", "idx_facturacion_municipio", 
            "idx_transferencias_servicio", "idx_planes_perdidas_periodo",
            "idx_lineas_municipio", "idx_mediciones_periodo"
        ]
    }
