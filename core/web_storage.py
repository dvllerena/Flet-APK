"""
Sistema de almacenamiento web usando localStorage
SINCRONIZADO CON ESTRUCTURA DE MIGRACIONES
"""

import json
import flet as ft
from typing import List, Dict, Any, Optional
from core.logger import get_logger

class WebStorageManager:
    """Gestor de almacenamiento web usando localStorage - ESTRUCTURA REAL"""
    
    def __init__(self, page: ft.Page, prefix: str = "perdidas_matanzas_"):
        self.page = page
        self.prefix = prefix
        self.logger = get_logger(__name__)
        self._initialized = False
        
        # Inicializar datos por defecto según migraciones
        self._init_default_data()
    
    def _init_default_data(self):
        """Inicializa datos por defecto según estructura de migraciones"""
        
        # ✅ MUNICIPIOS - 14 municipios incluye Varadero
        if not self._get_raw("municipios"):
            municipios = [
                {"id": 1, "codigo": "MAT", "nombre": "Matanzas", "provincia": "Matanzas", "activo": 1, "fecha_creacion": "2024-01-01 00:00:00"},
                {"id": 2, "codigo": "CAR", "nombre": "Cárdenas", "provincia": "Matanzas", "activo": 1, "fecha_creacion": "2024-01-01 00:00:00"},
                {"id": 3, "codigo": "VAR", "nombre": "Varadero", "provincia": "Matanzas", "activo": 1, "fecha_creacion": "2024-01-01 00:00:00"},
                {"id": 4, "codigo": "MAR", "nombre": "Martí", "provincia": "Matanzas", "activo": 1, "fecha_creacion": "2024-01-01 00:00:00"},
                {"id": 5, "codigo": "COL", "nombre": "Colón", "provincia": "Matanzas", "activo": 1, "fecha_creacion": "2024-01-01 00:00:00"},
                {"id": 6, "codigo": "PER", "nombre": "Perico", "provincia": "Matanzas", "activo": 1, "fecha_creacion": "2024-01-01 00:00:00"},
                {"id": 7, "codigo": "JOV", "nombre": "Jovellanos", "provincia": "Matanzas", "activo": 1, "fecha_creacion": "2024-01-01 00:00:00"},
                {"id": 8, "codigo": "PBE", "nombre": "Pedro Betancourt", "provincia": "Matanzas", "activo": 1, "fecha_creacion": "2024-01-01 00:00:00"},
                {"id": 9, "codigo": "LIM", "nombre": "Limonar", "provincia": "Matanzas", "activo": 1, "fecha_creacion": "2024-01-01 00:00:00"},
                {"id": 10, "codigo": "URE", "nombre": "Unión de Reyes", "provincia": "Matanzas", "activo": 1, "fecha_creacion": "2024-01-01 00:00:00"},
                {"id": 11, "codigo": "CZA", "nombre": "Ciénaga de Zapata", "provincia": "Matanzas", "activo": 1, "fecha_creacion": "2024-01-01 00:00:00"},
                {"id": 12, "codigo": "JGR", "nombre": "Jagüey Grande", "provincia": "Matanzas", "activo": 1, "fecha_creacion": "2024-01-01 00:00:00"},
                {"id": 13, "codigo": "CAL", "nombre": "Calimete", "provincia": "Matanzas", "activo": 1, "fecha_creacion": "2024-01-01 00:00:00"},
                {"id": 14, "codigo": "ARA", "nombre": "Los Arabos", "provincia": "Matanzas", "activo": 1, "fecha_creacion": "2024-01-01 00:00:00"}
            ]
            self._set_raw("municipios", municipios)
        
        # ✅ USUARIOS - Estructura exacta de migraciones
        if not self._get_raw("usuarios"):
            import hashlib
            usuarios = [
                {
                    "id": 1,
                    "username": "admin",
                    "password_hash": hashlib.sha256("admin".encode()).hexdigest(),
                    "nombre_completo": "Administrador del Sistema",
                    "email": "admin@une.cu",
                    "tipo_usuario": "administrador",
                    "activo": 1,
                    "fecha_creacion": "2024-01-01 00:00:00",
                    "ultimo_acceso": None
                },
                {
                    "id": 2,
                    "username": "operador",
                    "password_hash": hashlib.sha256("operador".encode()).hexdigest(),
                    "nombre_completo": "Operador del Sistema",
                    "email": "operador@une.cu",
                    "tipo_usuario": "operador",
                    "activo": 1,
                    "fecha_creacion": "2024-01-01 00:00:00",
                    "ultimo_acceso": None
                }
            ]
            self._set_raw("usuarios", usuarios)
        
        # ✅ CONFIGURACIONES - Según seeds
        if not self._get_raw("configuraciones"):
            configuraciones = [
                {"id": 1, "clave": "facturacion_menor_defecto", "valor": "0", "descripcion": "Valor por defecto facturación menor", "fecha_modificacion": "2024-01-01 00:00:00"},
                {"id": 2, "clave": "facturacion_mayor_defecto", "valor": "0", "descripcion": "Valor por defecto facturación mayor", "fecha_modificacion": "2024-01-01 00:00:00"},
                {"id": 3, "clave": "moneda_facturacion", "valor": "CUP", "descripcion": "Moneda para facturación", "fecha_modificacion": "2024-01-01 00:00:00"}
            ]
            self._set_raw("configuraciones", configuraciones)
        
        # ✅ INICIALIZAR TABLAS VACÍAS SEGÚN MIGRACIONES
        if not self._get_raw("energia_barra"):
            self._set_raw("energia_barra", [])
        
        if not self._get_raw("facturacion"):
            self._set_raw("facturacion", [])
        
        if not self._get_raw("transferencias_consumos"):
            self._set_raw("transferencias_consumos", [])
        
        if not self._get_raw("planes_perdidas"):
            self._set_raw("planes_perdidas", [])
        
        if not self._get_raw("calculos_perdidas"):
            self._set_raw("calculos_perdidas", [])
        
        if not self._get_raw("resumen_perdidas_provincial"):
            self._set_raw("resumen_perdidas_provincial", [])
        
        if not self._get_raw("lineas_venta"):
            self._set_raw("lineas_venta", [])
        
        if not self._get_raw("mediciones_lineas"):
            self._set_raw("mediciones_lineas", [])
        
        if not self._get_raw("transformadores_linea"):
            self._set_raw("transformadores_linea", [])
        
        if not self._get_raw("clientes_municipio"):
            self._set_raw("clientes_municipio", [])
        
        if not self._get_raw("transferencias_municipios"):
            self._set_raw("transferencias_municipios", [])
        
        if not self._get_raw("logs_sistema"):
            self._set_raw("logs_sistema", [])
    
    def _get_raw(self, key: str) -> Any:
        """Obtiene datos raw del localStorage"""
        try:
            full_key = f"{self.prefix}{key}"
            data = self.page.client_storage.get(full_key)
            return json.loads(data) if data else None
        except Exception as e:
            self.logger.error(f"Error al obtener {key}: {e}")
            return None
    
    def _set_raw(self, key: str, data: Any):
        """Guarda datos raw en localStorage"""
        try:
            full_key = f"{self.prefix}{key}"
            json_data = json.dumps(data, ensure_ascii=False)
            self.page.client_storage.set(full_key, json_data)
        except Exception as e:
            self.logger.error(f"Error al guardar {key}: {e}")
    
    def initialize(self):
        """Inicializa el storage web"""
        if self._initialized:
            return
        
        try:
            if not hasattr(self.page, 'client_storage'):
                raise Exception("client_storage no disponible")
            
            self._initialized = True
            self.logger.info("✅ WebStorageManager inicializado con estructura de migraciones")
            self.logger.info("✅ 14 municipios cargados (incluye Varadero)")
            
        except Exception as e:
            self.logger.error(f"Error al inicializar WebStorageManager: {e}")
            raise
    
    def execute_query(self, query: str, params: tuple = None) -> List[Dict[str, Any]]:
        """Simula consultas SQL usando localStorage - ESTRUCTURA REAL"""
        try:
            query_lower = query.lower().strip()
            
            # ✅ CONSULTAS DE CONTEO
            if "select count(*) as count from" in query_lower:
                if "municipios" in query_lower:
                    municipios = self._get_raw("municipios") or []
                    active_count = len([m for m in municipios if m.get("activo") == 1])
                    return [{"count": active_count}]
                elif "usuarios" in query_lower:
                    usuarios = self._get_raw("usuarios") or []
                    active_count = len([u for u in usuarios if u.get("activo") == 1])
                    return [{"count": active_count}]
                elif "energia_barra" in query_lower:
                    energia = self._get_raw("energia_barra") or []
                    return [{"count": len(energia)}]
                elif "facturacion" in query_lower:
                    facturacion = self._get_raw("facturacion") or []
                    return [{"count": len(facturacion)}]
                elif "transferencias_consumos" in query_lower:
                    transferencias = self._get_raw("transferencias_consumos") or []
                    return [{"count": len(transferencias)}]
                elif "planes_perdidas" in query_lower:
                    planes = self._get_raw("planes_perdidas") or []
                    return [{"count": len(planes)}]
            
            # ✅ CONSULTAS SELECT COMPLETAS
            elif "select * from" in query_lower:
                table_name = self._extract_table_name(query_lower)
                data = self._get_raw(table_name) or []
                
                if "where activo = 1" in query_lower:
                    return [item for item in data if item.get("activo") == 1]
                
                return data
            
            # ✅ CONSULTA DE LOGIN
            elif "select id, username, nombre_completo, email, tipo_usuario, activo from usuarios" in query_lower:
                usuarios = self._get_raw("usuarios") or []
                if params and len(params) >= 2:
                    username, password_hash = params[0], params[1]
                    for user in usuarios:
                        if (user.get("username") == username and 
                            user.get("password_hash") == password_hash and 
                            user.get("activo") == 1):
                            return [user]
                return []
            
            else:
                self.logger.warning(f"Consulta no soportada: {query}")
                return []
                
        except Exception as e:
            self.logger.error(f"Error en consulta web: {e}")
            return []
    
    def _extract_table_name(self, query: str) -> str:
        """Extrae el nombre de la tabla de una consulta"""
        try:
            parts = query.split("from")
            if len(parts) > 1:
                table_part = parts[1].strip().split()[0]
                return table_part
            return ""
        except:
            return ""
    
    def execute_update(self, query: str, params: tuple = None) -> int:
        """Simula actualizaciones SQL usando localStorage - ESTRUCTURA REAL"""
        try:
            query_lower = query.lower().strip()
            
            # ✅ INSERT INTO energia_barra
            if "insert into energia_barra" in query_lower and params:
                energia = self._get_raw("energia_barra") or []
                new_id = max([e.get("id", 0) for e in energia], default=0) + 1
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
                energia.append(new_record)
                self._set_raw("energia_barra", energia)
                return 1
            
            # ✅ INSERT INTO facturacion
            elif "insert into facturacion" in query_lower and params:
                facturacion = self._get_raw("facturacion") or []
                new_id = max([f.get("id", 0) for f in facturacion], default=0) + 1
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
                facturacion.append(new_record)
                self._set_raw("facturacion", facturacion)
                return 1
            
            # ✅ INSERT INTO transferencias_consumos
            elif "insert into transferencias_consumos" in query_lower and params:
                transferencias = self._get_raw("transferencias_consumos") or []
                new_id = max([t.get("id", 0) for t in transferencias], default=0) + 1
                new_record = {
                    "id": new_id,
                    "servicio_id": params[0],
                    "año": params[1],
                    "mes": params[2],
                    "consumo_kwh": params[3],
                    "fecha_registro": self._get_current_timestamp(),
                    "fecha_actualizacion": self._get_current_timestamp(),
                    "usuario_id": params[4] if len(params) > 4 else None,
                    "observaciones": params[5] if len(params) > 5 else None,
                    "origen": params[6] if len(params) > 6 else None,
                    "destino": params[7] if len(params) > 7 else None
                }
                transferencias.append(new_record)
                self._set_raw("transferencias_consumos", transferencias)
                return 1
            
            # ✅ INSERT INTO planes_perdidas
            elif "insert into planes_perdidas" in query_lower and params:
                planes = self._get_raw("planes_perdidas") or []
                new_id = max([p.get("id", 0) for p in planes], default=0) + 1
                new_record = {
                    "id": new_id,
                    "municipio_id": params[0],
                    "año": params[1],
                    "mes": params[2],
                    "plan_perdidas_pct": params[3],
                    "observaciones": params[4] if len(params) > 4 else None,
                    "usuario_id": params[5] if len(params) > 5 else None,
                    "fecha_creacion": self._get_current_timestamp(),
                    "fecha_modificacion": self._get_current_timestamp()
                }
                planes.append(new_record)
                self._set_raw("planes_perdidas", planes)
                return 1
            
            # ✅ INSERT INTO calculos_perdidas
            elif "insert into calculos_perdidas" in query_lower and params:
                calculos = self._get_raw("calculos_perdidas") or []
                new_id = max([c.get("id", 0) for c in calculos], default=0) + 1
                new_record = {
                    "id": new_id,
                    "municipio_id": params[0],
                    "año": params[1],
                    "mes": params[2],
                    "energia_barra_mwh": params[3] if len(params) > 3 else 0,
                    "facturacion_mayor": params[4] if len(params) > 4 else 0,
                    "facturacion_menor": params[5] if len(params) > 5 else 0,
                    "total_ventas": params[6] if len(params) > 6 else 0,
                    "perdidas_distribucion_mwh": params[7] if len(params) > 7 else 0,
                    "perdidas_pct": params[8] if len(params) > 8 else 0,
                    "plan_perdidas_pct": params[9] if len(params) > 9 else 0,
                    "energia_barra_acumulada": params[10] if len(params) > 10 else 0,
                    "perdidas_acumuladas_mwh": params[11] if len(params) > 11 else 0,
                    "perdidas_acumuladas_pct": params[12] if len(params) > 12 else 0,
                    "plan_perdidas_acumulado_pct": params[13] if len(params) > 13 else 0,
                    "usuario_id": params[14] if len(params) > 14 else None,
                    "fecha_calculo": self._get_current_timestamp(),
                    "fecha_actualizacion": self._get_current_timestamp()
                }
                calculos.append(new_record)
                self._set_raw("calculos_perdidas", calculos)
                return 1
            
            # ✅ INSERT INTO lineas_venta
            elif "insert into lineas_venta" in query_lower and params:
                lineas = self._get_raw("lineas_venta") or []
                new_id = max([l.get("id", 0) for l in lineas], default=0) + 1
                new_record = {
                    "id": new_id,
                    "municipio_id": params[0],
                    "codigo_linea": params[1],
                    "nombre_linea": params[2],
                    "tension_kv": params[3] if len(params) > 3 else 0,
                    "longitud_km": params[4] if len(params) > 4 else 0,
                    "activa": params[5] if len(params) > 5 else 1,
                    "observaciones": params[6] if len(params) > 6 else None,
                    "usuario_id": params[7] if len(params) > 7 else None,
                    "fecha_creacion": self._get_current_timestamp(),
                    "fecha_modificacion": self._get_current_timestamp()
                }
                lineas.append(new_record)
                self._set_raw("lineas_venta", lineas)
                return 1
            
            # ✅ INSERT INTO clientes_municipio
            elif "insert into clientes_municipio" in query_lower and params:
                clientes = self._get_raw("clientes_municipio") or []
                new_id = max([c.get("id", 0) for c in clientes], default=0) + 1
                new_record = {
                    "id": new_id,
                    "municipio_id": params[0],
                    "codigo_cliente": params[1],
                    "nombre_cliente": params[2],
                    "consumo_kwh": params[3] if len(params) > 3 else 0,
                    "activo": params[4] if len(params) > 4 else 1,
                    "observaciones": params[5] if len(params) > 5 else None,
                    "fecha_creacion": self._get_current_timestamp()
                }
                clientes.append(new_record)
                self._set_raw("clientes_municipio", clientes)
                return 1
            
            # ✅ UPDATE queries
            elif "update" in query_lower:
                return self._handle_update_query(query, params)
            
            # ✅ DELETE queries
            elif "delete" in query_lower:
                return self._handle_delete_query(query, params)
            
            else:
                self.logger.warning(f"Actualización no soportada: {query}")
                return 0
                
        except Exception as e:
            self.logger.error(f"Error en actualización web: {e}")
            return 0
    
    def _handle_update_query(self, query: str, params: tuple = None) -> int:
        """Maneja consultas UPDATE"""
        query_lower = query.lower()
        
        if "update usuarios set ultimo_acceso" in query_lower and params:
            usuarios = self._get_raw("usuarios") or []
            user_id = params[0]
            for user in usuarios:
                if user.get("id") == user_id:
                    user["ultimo_acceso"] = self._get_current_timestamp()
                    break
            self._set_raw("usuarios", usuarios)
            return 1
        
        elif "update energia_barra set" in query_lower and params:
            energia = self._get_raw("energia_barra") or []
            # Implementar lógica de actualización específica según necesidades
            return 1
        
        elif "update facturacion set" in query_lower and params:
            facturacion = self._get_raw("facturacion") or []
            # Implementar lógica de actualización específica según necesidades
            return 1
        
        elif "update planes_perdidas set" in query_lower and params:
            planes = self._get_raw("planes_perdidas") or []
            # Implementar lógica de actualización específica según necesidades
            return 1
        
        return 0
    
    def _handle_delete_query(self, query: str, params: tuple = None) -> int:
        """Maneja consultas DELETE"""
        query_lower = query.lower()
        
        if "delete from energia_barra where" in query_lower and params:
            energia = self._get_raw("energia_barra") or []
            # Implementar lógica de eliminación específica según necesidades
            return 1
        
        elif "delete from facturacion where" in query_lower and params:
            facturacion = self._get_raw("facturacion") or []
            # Implementar lógica de eliminación específica según necesidades
            return 1
        
        return 0
    
    def _get_current_timestamp(self) -> str:
        """Obtiene timestamp actual"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    # ✅ MÉTODOS ESPECÍFICOS PARA COMPATIBILIDAD CON DatabaseManager
    def get_user_by_credentials(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """Obtiene un usuario por credenciales"""
        import hashlib
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        usuarios = self._get_raw("usuarios") or []
        for user in usuarios:
            if (user.get("username") == username and 
                user.get("password_hash") == password_hash and 
                user.get("activo") == 1):
                return {
                    "id": user["id"],
                    "username": user["username"],
                    "nombre_completo": user["nombre_completo"],
                    "email": user["email"],
                    "tipo_usuario": user["tipo_usuario"],
                    "activo": user["activo"]
                }
        return None
    
    def update_last_access(self, user_id: int):
        """Actualiza el último acceso del usuario"""
        usuarios = self._get_raw("usuarios") or []
        for user in usuarios:
            if user.get("id") == user_id:
                user["ultimo_acceso"] = self._get_current_timestamp()
                break
        self._set_raw("usuarios", usuarios)
    
    def get_municipios(self) -> List[Dict[str, Any]]:
        """Obtiene todos los municipios activos"""
        municipios = self._get_raw("municipios") or []
        return [m for m in municipios if m.get("activo") == 1]
    
    def log_action(self, user_id: int, action: str, module: str = None, details: str = None):
        """Registra una acción en el log del sistema"""
        logs = self._get_raw("logs_sistema") or []
        new_id = max([log.get("id", 0) for log in logs], default=0) + 1
        
        new_log = {
            "id": new_id,
            "usuario_id": user_id,
            "accion": action,
            "modulo": module,
            "detalles": details,
            "fecha": self._get_current_timestamp()
        }
        
        logs.append(new_log)
        # Mantener solo los últimos 1000 logs para no sobrecargar localStorage
        if len(logs) > 1000:
            logs = logs[-1000:]
        
        self._set_raw("logs_sistema", logs)
    
    # ✅ MÉTODOS ADICIONALES PARA FUNCIONALIDADES ESPECÍFICAS
    def get_energia_by_municipio_periodo(self, municipio_id: int, año: int, mes: int = None) -> List[Dict[str, Any]]:
        """Obtiene energía por municipio y período"""
        energia = self._get_raw("energia_barra") or []
        result = [e for e in energia if e.get("municipio_id") == municipio_id and e.get("año") == año]
        
        if mes is not None:
            result = [e for e in result if e.get("mes") == mes]
        
        return result
    
    def get_facturacion_by_municipio_periodo(self, municipio_id: int, año: int, mes: int = None) -> List[Dict[str, Any]]:
        """Obtiene facturación por municipio y período"""
        facturacion = self._get_raw("facturacion") or []
        result = [f for f in facturacion if f.get("municipio_id") == municipio_id and f.get("año") == año]
        
        if mes is not None:
            result = [f for f in result if f.get("mes") == mes]
        
        return result
    
    def get_planes_perdidas_by_periodo(self, año: int, mes: int = None) -> List[Dict[str, Any]]:
        """Obtiene planes de pérdidas por período"""
        planes = self._get_raw("planes_perdidas") or []
        result = [p for p in planes if p.get("año") == año]
        
        if mes is not None:
            result = [p for p in result if p.get("mes") == mes]
        
        return result
    
    def get_transferencias_by_periodo(self, año: int, mes: int = None) -> List[Dict[str, Any]]:
        """Obtiene transferencias por período"""
        transferencias = self._get_raw("transferencias_consumos") or []
        result = [t for t in transferencias if t.get("año") == año]
        
        if mes is not None:
            result = [t for t in result if t.get("mes") == mes]
        
        return result
    
    def clear_all_data(self):
        """Limpia todos los datos (para testing o reset)"""
        tables = [
            "energia_barra", "facturacion", "transferencias_consumos", 
            "planes_perdidas", "calculos_perdidas", "resumen_perdidas_provincial",
            "lineas_venta", "mediciones_lineas", "transformadores_linea",
            "clientes_municipio", "transferencias_municipios", "logs_sistema"
        ]
        
        for table in tables:
            self._set_raw(table, [])
        
        self.logger.info("✅ Todos los datos han sido limpiados")
    
    def get_database_stats(self) -> Dict[str, int]:
        """Obtiene estadísticas de la base de datos"""
        stats = {}
        tables = [
            "municipios", "usuarios", "energia_barra", "facturacion", 
            "transferencias_consumos", "planes_perdidas", "calculos_perdidas",
            "lineas_venta", "clientes_municipio", "logs_sistema"
        ]
        
        for table in tables:
            data = self._get_raw(table) or []
            stats[table] = len(data)
        
        return stats

