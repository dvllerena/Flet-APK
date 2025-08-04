"""
Gestor de base de datos para aplicación web
Usa datos simulados en memoria - SINCRONIZADO CON MIGRACIONES
"""

from typing import List, Dict, Any, Optional
from core.logger import get_logger
import hashlib
from datetime import datetime

class WebDatabaseManager:
    """Gestor de base de datos web con datos simulados - ESTRUCTURA REAL"""
    
    def __init__(self):
        self.logger = get_logger(__name__)
        self._initialized = False
        self._setup_sample_data()
    
    def _setup_sample_data(self):
        """Configura datos de muestra en memoria"""
        # Usuarios de muestra
        self.users = [
            {
                "id": 1,
                "username": "admin",
                "password_hash": hashlib.sha256("admin".encode()).hexdigest(),
                "nombre_completo": "Administrador",
                "email": "admin@une.cu",
                "tipo_usuario": "administrador",
                "activo": 1
            },
            {
                "id": 2,
                "username": "operador",
                "password_hash": hashlib.sha256("operador".encode()).hexdigest(),
                "nombre_completo": "Operador Sistema",
                "email": "operador@une.cu",
                "tipo_usuario": "operador",
                "activo": 1
            }
        ]
        
        # Municipios de Matanzas
        self.municipios = [
            {"id": 1, "codigo": "MAT", "nombre": "Matanzas", "provincia": "Matanzas", "activo": 1},
            {"id": 2, "codigo": "CAR", "nombre": "Cárdenas", "provincia": "Matanzas", "activo": 1},
            {"id": 3, "codigo": "MAR", "nombre": "Martí", "provincia": "Matanzas", "activo": 1},
            {"id": 4, "codigo": "COL", "nombre": "Colón", "provincia": "Matanzas", "activo": 1},
            {"id": 5, "codigo": "PER", "nombre": "Perico", "provincia": "Matanzas", "activo": 1},
            {"id": 6, "codigo": "JOV", "nombre": "Jovellanos", "provincia": "Matanzas", "activo": 1},
            {"id": 7, "codigo": "PBE", "nombre": "Pedro Betancourt", "provincia": "Matanzas", "activo": 1},
            {"id": 8, "codigo": "LIM", "nombre": "Limonar", "provincia": "Matanzas", "activo": 1},
            {"id": 9, "codigo": "URE", "nombre": "Unión de Reyes", "provincia": "Matanzas", "activo": 1},
            {"id": 10, "codigo": "CZA", "nombre": "Ciénaga de Zapata", "provincia": "Matanzas", "activo": 1},
            {"id": 11, "codigo": "JGR", "nombre": "Jagüey Grande", "provincia": "Matanzas", "activo": 1},
            {"id": 12, "codigo": "CAL", "nombre": "Calimete", "provincia": "Matanzas", "activo": 1},
            {"id": 13, "codigo": "ARA", "nombre": "Los Arabos", "provincia": "Matanzas", "activo": 1}
        ]
        
        # Datos de energía de muestra más completos
        self.energia_barra = []
        
        # Generar datos para los últimos 3 meses
        import datetime
        current_date = datetime.datetime.now()
        
        # Datos base por municipio (valores realistas para Matanzas)
        datos_base = {
            1: 145.5,   # Matanzas
            2: 120.3,   # Cárdenas  
            3: 98.7,    # Martí
            4: 110.2,   # Colón
            5: 85.4,    # Perico
            6: 92.1,    # Jovellanos
            7: 78.9,    # Pedro Betancourt
            8: 88.6,    # Limonar
            9: 95.3,    # Unión de Reyes
            10: 156.8,  # Ciénaga de Zapata
            11: 102.4,  # Jagüey Grande
            12: 87.2,   # Calimete
            13: 91.7    # Los Arabos
        }
        
        # Generar registros para enero, febrero y marzo 2024
        record_id = 1
        for mes in [1, 2, 3]:
            for municipio_id in range(1, 14):
                # Variación aleatoria del ±10% para hacer datos más realistas
                import random
                base_value = datos_base.get(municipio_id, 100.0)
                variacion = random.uniform(0.9, 1.1)
                energia_value = round(base_value * variacion, 1)
                
                self.energia_barra.append({
                    "id": record_id,
                    "municipio_id": municipio_id,
                    "año": 2024,
                    "mes": mes,
                    "energia_mwh": energia_value,
                    "observaciones": f"Datos {['', 'enero', 'febrero', 'marzo'][mes]} 2024",
                    "fecha_registro": f"2024-{mes:02d}-{28 if mes == 2 else 31}T10:{(municipio_id-1)*5:02d}:00",
                    "usuario_id": 1,
                    "fecha_modificacion": f"2024-{mes:02d}-{28 if mes == 2 else 31}T10:{(municipio_id-1)*5:02d}:00"
                })
                record_id += 1
        
        # Datos de facturación de muestra
        self.facturacion = []
        facturacion_id = 1
        
        for mes in [1, 2, 3]:
            for municipio_id in range(1, 14):
                # Calcular facturación basada en energía (aproximadamente 60-70% de la energía)
                energia_base = datos_base.get(municipio_id, 100.0)
                facturacion_mayor = round(energia_base * 0.45, 1)
                facturacion_menor = round(energia_base * 0.25, 1)
                facturacion_total = facturacion_mayor + facturacion_menor
                
                self.facturacion.append({
                    "id": facturacion_id,
                    "municipio_id": municipio_id,
                    "año": 2024,
                    "mes": mes,
                    "facturacion_mayor": facturacion_mayor,
                    "facturacion_menor": facturacion_menor,
                    "facturacion_total": facturacion_total,
                    "observaciones": f"Facturación {['', 'enero', 'febrero', 'marzo'][mes]} 2024",
                    "usuario_id": 1,
                    "fecha_creacion": f"2024-{mes:02d}-{28 if mes == 2 else 31}T11:00:00",
                    "fecha_actualizacion": f"2024-{mes:02d}-{28 if mes == 2 else 31}T11:00:00"
                })
                facturacion_id += 1
        
        # Logs del sistema
        self.logs = []
        
        self.logger.info(f"Datos de muestra inicializados: {len(self.energia_barra)} registros de energía, {len(self.facturacion)} registros de facturación")

    def initialize(self):
        """Inicializa la base de datos"""
        if self._initialized:
            return
        
        self.logger.info("Inicializando base de datos web con estructura de migraciones")
        self._initialized = True
        # Debug de datos
        self.debug_data_status()
        self.logger.info("✅ Base de datos web inicializada con 14 municipios (incluye Varadero)")
    
    def execute_query(self, query: str, params: tuple = None) -> List[Dict[str, Any]]:
        """Simula consultas SELECT"""
        try:
            query_lower = query.lower().strip()
            
            # Normalizar espacios en blanco
            query_normalized = ' '.join(query_lower.split())
            
            # Consultas de conteo - más específicas
            if "select count(*) as count from municipios" in query_normalized:
                if "where activo = 1" in query_normalized:
                    return [{"count": len([m for m in self.municipios if m["activo"] == 1])}]
                return [{"count": len(self.municipios)}]
            
            elif "select count(*) as total from municipios" in query_normalized:
                if "where activo = 1" in query_normalized:
                    return [{"total": len([m for m in self.municipios if m["activo"] == 1])}]
                return [{"total": len(self.municipios)}]
            
            elif "select count(*) as count from usuarios" in query_normalized:
                if "where activo = 1" in query_normalized:
                    return [{"count": len([u for u in self.users if u["activo"] == 1])}]
                return [{"count": len(self.users)}]
            
            elif "select count(*) as count from energia_barra" in query_normalized:
                return [{"count": len(self.energia_barra)}]
            
            elif "select count(*) as count from facturacion" in query_normalized:
                return [{"count": len(self.facturacion)}]
            
            # Consultas de municipios
            elif "select * from municipios" in query_normalized:
                if "where activo = 1" in query_normalized:
                    return [m for m in self.municipios if m["activo"] == 1]
                return self.municipios
            
            elif "select * from usuarios" in query_normalized:
                if "where activo = 1" in query_normalized:
                    return [u for u in self.users if u["activo"] == 1]
                return self.users
            
            # Consultas de energía con JOIN
            elif ("select eb.*, m.nombre as municipio_nombre, m.codigo as municipio_codigo" in query_normalized and
                  "from energia_barra eb" in query_normalized and
                  "join municipios m" in query_normalized):
                
                if params and len(params) >= 2:
                    año, mes = params[0], params[1]
                    result = []
                    
                    # Buscar registros que coincidan
                    for registro in self.energia_barra:
                        if registro.get("año") == año and registro.get("mes") == mes:
                            # Buscar municipio correspondiente
                            municipio = next((m for m in self.municipios if m["id"] == registro["municipio_id"]), None)
                            if municipio:
                                registro_completo = registro.copy()
                                registro_completo["municipio_nombre"] = municipio["nombre"]
                                registro_completo["municipio_codigo"] = municipio["codigo"]
                                result.append(registro_completo)
                    
                    self.logger.info(f"Consulta JOIN energía: encontrados {len(result)} registros para {año}-{mes:02d}")
                    return result
                return []
            
            # Consultas de energía simples
            elif "select * from energia_barra" in query_normalized:
                if params and len(params) >= 2:
                    año, mes = params[0], params[1]
                    result = [e for e in self.energia_barra if e.get("año") == año and e.get("mes") == mes]
                    self.logger.info(f"Consulta simple energía: encontrados {len(result)} registros para {año}-{mes:02d}")
                    return result
                return self.energia_barra
            
            # Consulta de resumen mensual - más específica
            elif ("select" in query_normalized and 
                  "count(*) as total_registros" in query_normalized and
                  "from energia_barra" in query_normalized):
                
                if params and len(params) >= 2:
                    año, mes = params[0], params[1]
                    registros_periodo = [e for e in self.energia_barra if e.get("año") == año and e.get("mes") == mes]
                    
                    total_registros = len(registros_periodo)
                    registros_completos = len([r for r in registros_periodo if r.get("energia_mwh") is not None and r.get("energia_mwh") > 0])
                    total_energia = sum(r.get("energia_mwh", 0) for r in registros_periodo if r.get("energia_mwh") is not None)
                    
                    # Última actualización
                    ultima_actualizacion = None
                    if registros_periodo:
                        fechas = [r.get("fecha_registro") for r in registros_periodo if r.get("fecha_registro")]
                        if fechas:
                            ultima_actualizacion = max(fechas)
                    
                    result = [{
                        "total_registros": total_registros,
                        "registros_completos": registros_completos,
                        "total_energia": total_energia,
                        "ultima_actualizacion": ultima_actualizacion
                    }]
                    
                    self.logger.info(f"Consulta resumen: {total_registros} registros, {registros_completos} completos, {total_energia} MWh total")
                    return result
                return []
            
            # Consultas de facturación
            elif "select * from facturacion" in query_normalized:
                if params and len(params) >= 2:
                    año, mes = params[0], params[1]
                    return [f for f in self.facturacion if f.get("año") == año and f.get("mes") == mes]
                return self.facturacion
            
            # Consultas de login
            elif ("select id, username, nombre_completo, email, tipo_usuario, activo from usuarios" in query_normalized and
                  "where username = ? and password_hash = ?" in query_normalized):
                
                if params and len(params) >= 2:
                    username, password_hash = params[0], params[1]
                    for user in self.users:
                        if (user.get("username") == username and 
                            user.get("password_hash") == password_hash and 
                            user.get("activo") == 1):
                            return [user]
                return []
            
            # Consultas específicas por ID
            elif "where id = ?" in query_normalized and params:
                registro_id = params[0]
                
                if "from energia_barra" in query_normalized:
                    registro = next((e for e in self.energia_barra if e.get("id") == registro_id), None)
                    if registro:
                        # Agregar información del municipio
                        municipio = next((m for m in self.municipios if m["id"] == registro["municipio_id"]), None)
                        if municipio:
                            registro_completo = registro.copy()
                            registro_completo["municipio_nombre"] = municipio["nombre"]
                            registro_completo["municipio_codigo"] = municipio["codigo"]
                            return [registro_completo]
                    return []
                
                elif "from facturacion" in query_normalized:
                    registro = next((f for f in self.facturacion if f.get("id") == registro_id), None)
                    return [registro] if registro else []
            
            # Consultas con WHERE municipio_id, año, mes
            elif ("where municipio_id = ? and año = ? and mes = ?" in query_normalized and 
                  params and len(params) >= 3):
                
                municipio_id, año, mes = params[0], params[1], params[2]
                
                if "from energia_barra" in query_normalized:
                    registro = next((e for e in self.energia_barra 
                                   if e.get("municipio_id") == municipio_id and 
                                      e.get("año") == año and 
                                      e.get("mes") == mes), None)
                    if registro:
                        # Agregar información del municipio
                        municipio = next((m for m in self.municipios if m["id"] == municipio_id), None)
                        if municipio:
                            registro_completo = registro.copy()
                            registro_completo["municipio_nombre"] = municipio["nombre"]
                            registro_completo["municipio_codigo"] = municipio["codigo"]
                            return [registro_completo]
                    return []
                
                elif "from facturacion" in query_normalized:
                    registro = next((f for f in self.facturacion 
                                   if f.get("municipio_id") == municipio_id and 
                                      f.get("año") == año and 
                                      f.get("mes") == mes), None)
                    return [registro] if registro else []
            
            else:
                self.logger.warning(f"Consulta no soportada: {query[:100]}...")
                return []
                
        except Exception as e:
            self.logger.error(f"Error en consulta simulada: {e}")
            import traceback
            self.logger.error(f"Traceback: {traceback.format_exc()}")
            return []

    def execute_update(self, query: str, params: tuple = None) -> int:
        """Simula consultas INSERT/UPDATE/DELETE"""
        try:
            query_lower = query.lower().strip()
            
            # INSERT INTO energia_barra
            if "insert into energia_barra" in query_lower:
                if params and len(params) >= 4:
                    new_id = max([e.get("id", 0) for e in self.energia_barra], default=0) + 1
                    
                    new_record = {
                        "id": new_id,
                        "municipio_id": params[0],
                        "año": params[1],
                        "mes": params[2],
                        "energia_mwh": params[3],
                        "observaciones": params[4] if len(params) > 4 else None,
                        "usuario_id": params[5] if len(params) > 5 else None,
                        "fecha_registro": self._get_current_timestamp(),
                        "fecha_modificacion": self._get_current_timestamp()
                    }
                    
                    self.energia_barra.append(new_record)
                    self.logger.info(f"Registro de energía creado: ID {new_id}, Municipio {params[0]}, {params[1]}-{params[2]:02d}, {params[3]} MWh")
                    return 1
                return 0
            
            # INSERT INTO facturacion
            elif "insert into facturacion" in query_lower:
                if params and len(params) >= 6:
                    new_id = max([f.get("id", 0) for f in self.facturacion], default=0) + 1
                    new_record = {
                        "id": new_id,
                        "municipio_id": params[0],
                        "año": params[1],
                        "mes": params[2],
                        "facturacion_menor": params[3],
                        "facturacion_mayor": params[4],
                        "facturacion_total": params[5],
                        "observaciones": params[6] if len(params) > 6 else None,
                        "usuario_id": params[7] if len(params) > 7 else None,
                        "fecha_creacion": self._get_current_timestamp(),
                        "fecha_actualizacion": self._get_current_timestamp()
                    }
                    self.facturacion.append(new_record)
                    return 1
                return 0
            
            # UPDATE queries
            elif "update" in query_lower:
                return self._handle_update_query(query, params)
            
            # DELETE queries
            elif "delete" in query_lower:
                return self._handle_delete_query(query, params)
            
            else:
                self.logger.warning(f"Actualización no soportada: {query[:100]}...")
                return 0
                
        except Exception as e:
            self.logger.error(f"Error en actualización simulada: {e}")
            import traceback
            self.logger.error(f"Traceback: {traceback.format_exc()}")
            return 0
    
    def _get_current_timestamp(self) -> str:
        """Obtiene timestamp actual"""
        from datetime import datetime
        return datetime.now().isoformat()

    def get_user_by_credentials(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """Obtiene un usuario por credenciales"""
        try:
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            
            for user in self.users:
                if (user["username"] == username and 
                    user["password_hash"] == password_hash and 
                    user["activo"] == 1):
                    
                    return {
                        "id": user["id"],
                        "username": user["username"],
                        "nombre_completo": user["nombre_completo"],
                        "email": user["email"],
                        "tipo_usuario": user["tipo_usuario"],
                        "activo": user["activo"]
                    }
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error obteniendo usuario: {e}")
            return None
    
    def update_last_access(self, user_id: int):
        """Actualiza el último acceso del usuario"""
        for user in self.users:
            if user.get("id") == user_id:
                user["ultimo_acceso"] = datetime.now().isoformat()
                break
        self.logger.info(f"Actualizando último acceso para usuario {user_id}")
    
    def get_municipios(self) -> List[Dict[str, Any]]:
        """Obtiene todos los municipios activos"""
        return [m for m in self.municipios if m["activo"] == 1]
    
    def log_action(self, user_id: int, action: str, module: str = None, details: str = None):
        """Registra una acción en el log del sistema"""
        log_entry = {
            "id": len(self.logs) + 1,
            "usuario_id": user_id,
            "accion": action,
            "modulo": module,
            "detalles": details,
            "fecha": datetime.now().isoformat()
        }
        self.logs.append(log_entry)
        self.logger.info(f"Acción registrada: {action}")

    def debug_data_status(self):
        """Método de debug para verificar el estado de los datos"""
        self.logger.info("=== DEBUG: Estado de los datos ===")
        self.logger.info(f"Usuarios: {len(self.users)}")
        self.logger.info(f"Municipios: {len(self.municipios)}")
        self.logger.info(f"Registros de energía: {len(self.energia_barra)}")
        self.logger.info(f"Registros de facturación: {len(self.facturacion)}")
        
        # Mostrar algunos registros de energía
        if self.energia_barra:
            self.logger.info("Primeros 3 registros de energía:")
            for i, registro in enumerate(self.energia_barra[:3]):
                self.logger.info(f"  {i+1}: ID={registro['id']}, Municipio={registro['municipio_id']}, {registro['año']}-{registro['mes']:02d}, {registro['energia_mwh']} MWh")
        
        # Verificar datos por período
        for mes in [1, 2, 3]:
            registros_mes = [e for e in self.energia_barra if e.get("año") == 2024 and e.get("mes") == mes]
            self.logger.info(f"Registros para 2024-{mes:02d}: {len(registros_mes)}")
        
        self.logger.info("=== FIN DEBUG ===")

# Instancia global del gestor de base de datos
_db_manager = None

def get_db_manager() -> WebDatabaseManager:
    """Obtiene la instancia del gestor de base de datos"""
    global _db_manager
    if _db_manager is None:
        _db_manager = WebDatabaseManager()
    return _db_manager

def initialize_database():
    """Inicializa la base de datos"""
    db_manager = get_db_manager()
    db_manager.initialize()

