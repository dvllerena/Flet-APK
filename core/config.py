"""
Configuración de la aplicación web - SINCRONIZADA CON MIGRACIONES
"""

import os
from pathlib import Path
from typing import Dict, Any, List
from dotenv import load_dotenv

class Config:
    """Clase de configuración para aplicación web"""
    
    def __init__(self):
        try:
            load_dotenv()
        except:
            pass
        
        self.ROOT_DIR = Path(__file__).parent.parent
        
        # Configuraciones básicas
        self.APP_NAME = "Análisis de Pérdidas Eléctricas - Matanzas"
        self.APP_VERSION = "1.0.0"
        self.DEBUG = os.getenv("DEBUG", "False").lower() == "true"
        
        # Configuraciones web
        self.WEB_PORT = int(os.getenv("PORT", "8080"))
        self.WEB_HOST = os.getenv("HOST", "0.0.0.0")
        self.SESSION_TIMEOUT = int(os.getenv("SESSION_TIMEOUT", "1800"))
        
        # Configuraciones de seguridad
        self.SECRET_KEY = os.getenv("SECRET_KEY", "tu-clave-secreta-perdidas-matanzas-2024")
        
        # Configuraciones de tema
        self.THEME_MODE = os.getenv("THEME_MODE", "light")
        
        # ✅ MUNICIPIOS DE MATANZAS - SINCRONIZADO CON MIGRACIONES (14 municipios + Varadero)
        self.MUNICIPIOS_MATANZAS = [
            "Matanzas", "Cárdenas", "Varadero", "Martí", "Colón", "Perico", 
            "Jovellanos", "Pedro Betancourt", "Limonar", "Unión de Reyes", 
            "Ciénaga de Zapata", "Jagüey Grande", "Calimete", "Los Arabos"
        ]
        
        self.DEFAULT_YEAR = 2024
        self.MONTHS = [
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ]
        
        # Características web
        self.FEATURES = {
            "file_operations": False,
            "excel_export": False,
            "backup_restore": False,
            "offline_mode": False,
            "real_time_updates": True,
            "responsive_design": True,
            "sample_data": True,
            "database_migrations": True,
            "full_crud": True
        }
    
    def get_app_config(self) -> Dict[str, Any]:
        """Obtiene la configuración de la aplicación"""
        return {
            "name": self.APP_NAME,
            "version": self.APP_VERSION,
            "theme_mode": self.THEME_MODE,
            "debug": self.DEBUG,
            "port": self.WEB_PORT,
            "host": self.WEB_HOST,
            "responsive": True,
            "features": self.FEATURES,
            "municipios": self.MUNICIPIOS_MATANZAS,
            "municipios_count": len(self.MUNICIPIOS_MATANZAS),
            "default_year": self.DEFAULT_YEAR,
            "months": self.MONTHS
        }
    
    def get_security_config(self) -> Dict[str, Any]:
        """Obtiene la configuración de seguridad"""
        return {
            "secret_key": self.SECRET_KEY,
            "session_timeout": self.SESSION_TIMEOUT
        }
    
    def get_features(self) -> Dict[str, bool]:
        """Obtiene las características disponibles"""
        return self.FEATURES.copy()
    
    def is_feature_enabled(self, feature: str) -> bool:
        """Verifica si una característica está habilitada"""
        return self.FEATURES.get(feature, False)
    
    def get_municipios_info(self) -> List[Dict[str, Any]]:
        """Obtiene información detallada de municipios"""
        municipios_info = [
            {"codigo": "MAT", "nombre": "Matanzas", "orden": 1},
            {"codigo": "CAR", "nombre": "Cárdenas", "orden": 2},
            {"codigo": "VAR", "nombre": "Varadero", "orden": 3},
            {"codigo": "MAR", "nombre": "Martí", "orden": 4},
            {"codigo": "COL", "nombre": "Colón", "orden": 5},
            {"codigo": "PER", "nombre": "Perico", "orden": 6},
            {"codigo": "JOV", "nombre": "Jovellanos", "orden": 7},
            {"codigo": "PBE", "nombre": "Pedro Betancourt", "orden": 8},
            {"codigo": "LIM", "nombre": "Limonar", "orden": 9},
            {"codigo": "URE", "nombre": "Unión de Reyes", "orden": 10},
            {"codigo": "CZA", "nombre": "Ciénaga de Zapata", "orden": 11},
            {"codigo": "JGR", "nombre": "Jagüey Grande", "orden": 12},
            {"codigo": "CAL", "nombre": "Calimete", "orden": 13},
            {"codigo": "ARA", "nombre": "Los Arabos", "orden": 14}
        ]
        return municipios_info

# Instancia global de configuración
_config = None

def get_config() -> Config:
    """Obtiene la instancia de configuración"""
    global _config
    if _config is None:
        _config = Config()
    return _config

def load_config() -> Config:
    """Carga y retorna la configuración"""
    return get_config()
