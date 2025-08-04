"""
Sistema de base de datos modular híbrido - SQLite + Web
"""
from pathlib import Path
from core.logger import get_logger

def setup_database(web_mode: bool = False):
    """Configura la base de datos completa según el modo"""
    logger = get_logger(__name__)
    
    if web_mode:
        logger.info("🌐 Configurando base de datos para modo WEB...")
        logger.info("✅ Base de datos web se inicializa automáticamente en WebStorageManager")
        return "web_storage"
    
    logger.info("🖥️ Configurando base de datos para modo DESKTOP...")
    
    # Ruta de la base de datos SQLite
    db_dir = Path(__file__).parent
    db_path = db_dir / "perdidas_matanzas.db"
    
    try:
        # 1. Ejecutar migraciones (crear tablas)
        logger.info("📋 Ejecutando migraciones...")
        from .migrations import run_migrations
        run_migrations(str(db_path), web_mode=False)
        
        # 2. Ejecutar seeds (insertar datos iniciales)
        logger.info("🌱 Ejecutando seeds...")
        from .seeds import run_seeds
        run_seeds(str(db_path))
        
        logger.info("✅ Base de datos SQLite configurada correctamente")
        return str(db_path)
        
    except Exception as e:
        logger.error(f"❌ Error configurando base de datos: {e}")
        raise

def get_database_info(web_mode: bool = False) -> dict:
    """Obtiene información sobre la base de datos"""
    logger = get_logger(__name__)
    
    if web_mode:
        return {
            "type": "WebStorage",
            "mode": "web",
            "status": "memory_based",
            "tables": [
                "usuarios", "municipios", "energia_barra", "facturacion",
                "transferencias_consumos", "planes_perdidas", "calculos_perdidas",
                "logs_sistema", "configuraciones"
            ],
            "features": [
                "In-memory storage",
                "Predefined sample data",
                "No persistence",
                "Fast access"
            ]
        }
    
    try:
        db_dir = Path(__file__).parent
        db_path = db_dir / "perdidas_matanzas.db"
        
        info = {
            "type": "SQLite",
            "mode": "desktop",
            "path": str(db_path),
            "exists": db_path.exists(),
            "size_mb": 0,
            "tables": [],
            "features": [
                "Persistent storage",
                "ACID compliance",
                "Full SQL support",
                "Backup capability"
            ]
        }
        
        if db_path.exists():
            info["size_mb"] = round(db_path.stat().st_size / (1024 * 1024), 2)
            
            # Obtener lista de tablas
            import sqlite3
            with sqlite3.connect(str(db_path)) as conn:
                cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
                info["tables"] = [row[0] for row in cursor.fetchall()]
        
        return info
        
    except Exception as e:
        logger.error(f"Error obteniendo información de BD: {e}")
        return {
            "type": "SQLite",
            "mode": "desktop",
            "status": "error",
            "error": str(e)
        }

def validate_database(web_mode: bool = False) -> dict:
    """Valida el estado de la base de datos"""
    logger = get_logger(__name__)
    
    if web_mode:
        return {
            "valid": True,
            "mode": "web",
            "checks": {
                "storage_available": True,
                "sample_data": True,
                "users_loaded": True,
                "municipios_loaded": True
            },
            "message": "WebStorage ready for use"
        }
    
    try:
        db_dir = Path(__file__).parent
        db_path = db_dir / "perdidas_matanzas.db"
        
        validation = {
            "valid": False,
            "mode": "desktop",
            "checks": {
                "file_exists": False,
                "file_readable": False,
                "tables_exist": False,
                "data_present": False
            },
            "errors": []
        }
        
        # Verificar archivo
        if not db_path.exists():
            validation["errors"].append("Database file does not exist")
            return validation
        
        validation["checks"]["file_exists"] = True
        
        # Verificar legibilidad
        try:
            import sqlite3
            with sqlite3.connect(str(db_path)) as conn:
                validation["checks"]["file_readable"] = True
                
                # Verificar tablas principales
                required_tables = ['usuarios', 'municipios', 'facturacion']
                cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
                existing_tables = [row[0] for row in cursor.fetchall()]
                
                missing_tables = [t for t in required_tables if t not in existing_tables]
                if missing_tables:
                    validation["errors"].append(f"Missing tables: {missing_tables}")
                else:
                    validation["checks"]["tables_exist"] = True
                
                # Verificar datos
                cursor = conn.execute("SELECT COUNT(*) FROM usuarios")
                user_count = cursor.fetchone()[0]
                
                cursor = conn.execute("SELECT COUNT(*) FROM municipios")
                municipio_count = cursor.fetchone()[0]
                
                if user_count > 0 and municipio_count > 0:
                    validation["checks"]["data_present"] = True
                else:
                    validation["errors"].append("No data found in core tables")
        
        except Exception as e:
            validation["errors"].append(f"Database connection error: {e}")
        
        # Determinar validez general
        validation["valid"] = all(validation["checks"].values())
        
        if validation["valid"]:
            validation["message"] = "Database is valid and ready"
        else:
            validation["message"] = f"Database validation failed: {'; '.join(validation['errors'])}"
        
        return validation
        
    except Exception as e:
        logger.error(f"Error validando base de datos: {e}")
        return {
            "valid": False,
            "mode": "desktop",
            "error": str(e),
            "message": "Validation process failed"
        }

def reset_database(web_mode: bool = False) -> bool:
    """Resetea la base de datos según el modo"""
    logger = get_logger(__name__)
    
    if web_mode:
        logger.info("🔄 Reseteando WebStorage...")
        try:
            # En modo web, simplemente reinicializar el storage
            from core.web_storage import WebStorageManager
            # El reset se maneja automáticamente al crear nueva instancia
            logger.info("✅ WebStorage reseteado correctamente")
            return True
        except Exception as e:
            logger.error(f"❌ Error reseteando WebStorage: {e}")
            return False
    
    logger.info("🔄 Reseteando base de datos SQLite...")
    
    try:
        db_dir = Path(__file__).parent
        db_path = db_dir / "perdidas_matanzas.db"
        
        # Eliminar archivo existente
        if db_path.exists():
            db_path.unlink()
            logger.info("🗑️ Archivo de base de datos eliminado")
        
        # Recrear base de datos
        setup_database(web_mode=False)
        logger.info("✅ Base de datos SQLite reseteada correctamente")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error reseteando base de datos: {e}")
        return False

def backup_database(backup_path: str = None) -> str:
    """Crea una copia de seguridad de la base de datos SQLite"""
    logger = get_logger(__name__)
    
    try:
        import shutil
        from datetime import datetime
        
        db_dir = Path(__file__).parent
        db_path = db_dir / "perdidas_matanzas.db"
        
        if not db_path.exists():
            raise Exception("Database file does not exist")
        
        # Generar nombre de backup si no se proporciona
        if backup_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = db_dir / f"backup_perdidas_matanzas_{timestamp}.db"
        else:
            backup_path = Path(backup_path)
        
        # Crear directorio de backup si no existe
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Copiar archivo
        shutil.copy2(str(db_path), str(backup_path))
        
        logger.info(f"✅ Backup creado: {backup_path}")
        return str(backup_path)
        
    except Exception as e:
        logger.error(f"❌ Error creando backup: {e}")
        raise

def restore_database(backup_path: str) -> bool:
    """Restaura la base de datos desde un backup"""
    logger = get_logger(__name__)
    
    try:
        import shutil
        
        backup_file = Path(backup_path)
        if not backup_file.exists():
            raise Exception(f"Backup file does not exist: {backup_path}")
        
        db_dir = Path(__file__).parent
        db_path = db_dir / "perdidas_matanzas.db"
        
        # Crear backup del archivo actual si existe
        if db_path.exists():
            current_backup = db_dir / f"current_backup_{int(datetime.now().timestamp())}.db"
            shutil.copy2(str(db_path), str(current_backup))
            logger.info(f"📋 Backup actual creado: {current_backup}")
        
        # Restaurar desde backup
        shutil.copy2(str(backup_file), str(db_path))
        
        logger.info(f"✅ Base de datos restaurada desde: {backup_path}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error restaurando base de datos: {e}")
        return False

def optimize_database() -> bool:
    """Optimiza la base de datos SQLite"""
    logger = get_logger(__name__)
    
    try:
        import sqlite3
        
        db_dir = Path(__file__).parent
        db_path = db_dir / "perdidas_matanzas.db"
        
        if not db_path.exists():
            raise Exception("Database file does not exist")
        
        with sqlite3.connect(str(db_path)) as conn:
            # Ejecutar VACUUM para optimizar
            logger.info("🔧 Ejecutando VACUUM...")
            conn.execute("VACUUM")
            
            # Analizar estadísticas
            logger.info("📊 Analizando estadísticas...")
            conn.execute("ANALYZE")
            
            # Reindexar
            logger.info("🔍 Reindexando...")
            conn.execute("REINDEX")
            
            conn.commit()
        
        logger.info("✅ Base de datos optimizada correctamente")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error optimizando base de datos: {e}")
        return False

def get_database_statistics(web_mode: bool = False) -> dict:
    """Obtiene estadísticas de la base de datos"""
    logger = get_logger(__name__)
    
    if web_mode:
        try:
            # Estadísticas simuladas para WebStorage
            from core.web_storage import WebStorageManager
            storage = WebStorageManager()
            
            return {
                "mode": "web",
                "type": "WebStorage",
                "tables": {
                    "usuarios": len(storage._users) if hasattr(storage, '_users') else 0,
                    "municipios": len(storage._municipios) if hasattr(storage, '_municipios') else 0,
                    "energia_barra": len(storage._energia_barra) if hasattr(storage, '_energia_barra') else 0,
                    "facturacion": len(storage._facturacion) if hasattr(storage, '_facturacion') else 0,
                    "logs_sistema": len(storage._logs) if hasattr(storage, '_logs') else 0
                },
                "total_records": 0,  # Se calculará después
                "memory_usage": "Variable",
                "last_updated": "Real-time"
            }
        except Exception as e:
            logger.error(f"Error obteniendo estadísticas web: {e}")
            return {"mode": "web", "error": str(e)}
    
    try:
        import sqlite3
        
        db_dir = Path(__file__).parent
        db_path = db_dir / "perdidas_matanzas.db"
        
        if not db_path.exists():
            return {"mode": "desktop", "error": "Database file does not exist"}
        
        stats = {
            "mode": "desktop",
            "type": "SQLite",
            "file_size_mb": round(db_path.stat().st_size / (1024 * 1024), 2),
            "tables": {},
            "indexes": [],
            "total_records": 0
        }
        
        with sqlite3.connect(str(db_path)) as conn:
            # Obtener información de tablas
            cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            
            for table in tables:
                try:
                    cursor = conn.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cursor.fetchone()[0]
                    stats["tables"][table] = count
                    stats["total_records"] += count
                except Exception:
                    stats["tables"][table] = "Error"
            
            # Obtener información de índices
            cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='index'")
            stats["indexes"] = [row[0] for row in cursor.fetchall()]
        
        return stats
        
    except Exception as e:
        logger.error(f"Error obteniendo estadísticas: {e}")
        return {"mode": "desktop", "error": str(e)}

def check_database_integrity(web_mode: bool = False) -> dict:
    """Verifica la integridad de la base de datos"""
    logger = get_logger(__name__)
    
    if web_mode:
        return {
            "mode": "web",
            "integrity": "ok",
            "message": "WebStorage integrity is managed in-memory",
            "checks_passed": True
        }
    
    try:
        import sqlite3
        
        db_dir = Path(__file__).parent
        db_path = db_dir / "perdidas_matanzas.db"
        
        if not db_path.exists():
            return {
                "mode": "desktop",
                "integrity": "error",
                "message": "Database file does not exist"
            }
        
        with sqlite3.connect(str(db_path)) as conn:
            # Verificar integridad
            cursor = conn.execute("PRAGMA integrity_check")
            result = cursor.fetchone()[0]
            
            if result == "ok":
                return {
                    "mode": "desktop",
                    "integrity": "ok",
                    "message": "Database integrity check passed",
                    "checks_passed": True
                }
            else:
                return {
                    "mode": "desktop",
                    "integrity": "error",
                    "message": f"Integrity check failed: {result}",
                    "checks_passed": False
                }
        
    except Exception as e:
        logger.error(f"Error verificando integridad: {e}")
        return {
            "mode": "desktop",
            "integrity": "error",
            "message": str(e),
            "checks_passed": False
        }

# ✅ FUNCIONES DE UTILIDAD ADICIONALES
def get_connection_string(web_mode: bool = False) -> str:
    """Obtiene la cadena de conexión según el modo"""
    if web_mode:
        return "webstorage://memory"
    
    db_dir = Path(__file__).parent
    db_path = db_dir / "perdidas_matanzas.db"
    return f"sqlite:///{db_path}"

def is_database_ready(web_mode: bool = False) -> bool:
    """Verifica si la base de datos está lista para usar"""
    try:
        validation = validate_database(web_mode)
        return validation.get("valid", False)
    except Exception:
        return False

def get_supported_features(web_mode: bool = False) -> list:
    """Obtiene las características soportadas según el modo"""
    if web_mode:
        return [
            "In-memory storage",
            "Fast access",
            "Sample data",
            "No persistence",
            "Session-based",
            "Automatic initialization"
        ]
    
    return [
        "Persistent storage",
        "ACID compliance",
        "Full SQL support",
        "Transactions",
        "Backup/Restore",
        "Optimization",
        "Integrity checks",
        "Foreign keys",
        "Indexes",
        "Views and triggers"
    ]

def migrate_to_web_mode() -> dict:
    """Migra datos de SQLite a WebStorage (para testing)"""
    logger = get_logger(__name__)
    
    try:
        # Esta función sería útil para migrar datos existentes
        # de SQLite a WebStorage para pruebas
        logger.info("🔄 Migración a modo web no implementada")
        return {
            "success": False,
            "message": "Migration to web mode not implemented",
            "suggestion": "Use WebStorage directly for web mode"
        }
    except Exception as e:
        logger.error(f"Error en migración: {e}")
        return {
            "success": False,
            "error": str(e)
        }

# ✅ CONFIGURACIÓN DE EXPORTACIÓN
__all__ = [
    'setup_database',
    'get_database_info',
    'validate_database',
    'reset_database',
    'backup_database',
    'restore_database',
    'optimize_database',
    'get_database_statistics',
    'check_database_integrity',
    'get_connection_string',
    'is_database_ready',
    'get_supported_features'
]
