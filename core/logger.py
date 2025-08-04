"""
Sistema de logging para aplicación web
"""

import logging
import sys
from typing import Optional

class WebLogger:
    """Logger optimizado para aplicaciones web"""
    
    def __init__(self):
        self.loggers = {}
        self.setup_done = False
    
    def setup_logger(self, name: str = "perdidas_web", level: str = "INFO") -> logging.Logger:
        """Configura el sistema de logging para web"""
        
        if name in self.loggers:
            return self.loggers[name]
        
        logger = logging.getLogger(name)
        logger.setLevel(getattr(logging, level.upper()))
        
        if logger.handlers:
            logger.handlers.clear()
        
        # Formato simple para web
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-5s | %(message)s',
            datefmt='%H:%M:%S'
        )
        
        # Solo handler de consola para web
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        
        if hasattr(console_handler.stream, 'reconfigure'):
            try:
                console_handler.stream.reconfigure(encoding='utf-8')
            except:
                pass
        
        logger.addHandler(console_handler)
        self.loggers[name] = logger
        
        if not self.setup_done:
            logger.info("=== Sistema de logging WEB inicializado ===")
            self.setup_done = True
        
        return logger
    
    def get_logger(self, name: str = "perdidas_web") -> logging.Logger:
        """Obtiene un logger existente o crea uno nuevo"""
        if name not in self.loggers:
            return self.setup_logger(name)
        return self.loggers[name]

# Instancia global del logger
_web_logger = None

def setup_logger(name: str = "perdidas_web", level: str = "INFO") -> logging.Logger:
    """Función para configurar el logger principal"""
    global _web_logger
    if _web_logger is None:
        _web_logger = WebLogger()
    
    return _web_logger.setup_logger(name, level)

def get_logger(name: str = "perdidas_web") -> logging.Logger:
    """Función para obtener un logger"""
    global _web_logger
    if _web_logger is None:
        _web_logger = WebLogger()
    
    return _web_logger.get_logger(name)
