"""
Servicio de autenticación - OPTIMIZADO PARA WEB
Maneja login, logout y validación de usuarios
"""

import hashlib
import json
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from core.logger import get_logger

# Para web, usaremos almacenamiento en memoria en lugar de SQLite
class WebStorageManager:
    """Gestor de almacenamiento para web (reemplaza SQLite)"""
    
    def __init__(self):
        # Usuarios por defecto para web
        self._users = {
            "admin": {
                "id": 1,
                "username": "admin",
                "password_hash": hashlib.sha256("admin".encode('utf-8')).hexdigest(),
                "nombre_completo": "Administrador del Sistema",
                "email": "admin@matanzas.une.cu",
                "tipo_usuario": "administrador",
                "activo": True,
                "fecha_creacion": datetime.now(),
                "ultimo_acceso": None
            },
            "operador": {
                "id": 2,
                "username": "operador",
                "password_hash": hashlib.sha256("operador123".encode('utf-8')).hexdigest(),
                "nombre_completo": "Operador del Sistema",
                "email": "operador@matanzas.une.cu",
                "tipo_usuario": "operador",
                "activo": True,
                "fecha_creacion": datetime.now(),
                "ultimo_acceso": None
            },
            "supervisor": {
                "id": 3,
                "username": "supervisor",
                "password_hash": hashlib.sha256("supervisor123".encode('utf-8')).hexdigest(),
                "nombre_completo": "Supervisor del Sistema",
                "email": "supervisor@matanzas.une.cu",
                "tipo_usuario": "supervisor",
                "activo": True,
                "fecha_creacion": datetime.now(),
                "ultimo_acceso": None
            }
        }
        
        # Logs de acciones
        self._logs = []
        
        # Municipios por defecto
        self._municipios = [
            {"id": 1, "codigo": "MAT", "nombre": "Matanzas", "activo": True},
            {"id": 2, "codigo": "CAR", "nombre": "Cárdenas", "activo": True},
            {"id": 3, "codigo": "VAR", "nombre": "Varadero", "activo": True},
            {"id": 4, "codigo": "COL", "nombre": "Colón", "activo": True},
            {"id": 5, "codigo": "JAG", "nombre": "Jagüey Grande", "activo": True},
            {"id": 6, "codigo": "JOV", "nombre": "Jovellanos", "activo": True},
            {"id": 7, "codigo": "LIS", "nombre": "Limonar", "activo": True},
            {"id": 8, "codigo": "MAR", "nombre": "Martí", "activo": True},
            {"id": 9, "codigo": "PED", "nombre": "Pedro Betancourt", "activo": True},
            {"id": 10, "codigo": "PER", "nombre": "Perico", "activo": True},
            {"id": 11, "codigo": "UNI", "nombre": "Unión de Reyes", "activo": True},
            {"id": 12, "codigo": "CAL", "nombre": "Calimete", "activo": True},
            {"id": 13, "codigo": "LOS", "nombre": "Los Arabos", "activo": True}
        ]
    
    def get_user_by_credentials(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """Obtiene usuario por credenciales"""
        password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
        
        user = self._users.get(username.lower())
        if user and user["password_hash"] == password_hash and user["activo"]:
            # Crear copia sin password_hash
            user_copy = user.copy()
            del user_copy["password_hash"]
            return user_copy
        return None
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Obtiene usuario por ID"""
        for user in self._users.values():
            if user["id"] == user_id and user["activo"]:
                user_copy = user.copy()
                del user_copy["password_hash"]
                return user_copy
        return None
    
    def update_last_access(self, user_id: int):
        """Actualiza último acceso"""
        for user in self._users.values():
            if user["id"] == user_id:
                user["ultimo_acceso"] = datetime.now()
                break
    
    def update_user_password(self, user_id: int, new_password_hash: str) -> bool:
        """Actualiza contraseña de usuario"""
        try:
            for user in self._users.values():
                if user["id"] == user_id:
                    user["password_hash"] = new_password_hash
                    return True
            return False
        except:
            return False
    
    def log_action(self, user_id: int, action: str, module: str = None, details: str = None):
        """Registra acción en logs"""
        log_entry = {
            "id": len(self._logs) + 1,
            "usuario_id": user_id,
            "accion": action,
            "modulo": module,
            "detalles": details,
            "fecha": datetime.now()
        }
        self._logs.append(log_entry)
    
    def get_municipios(self) -> List[Dict[str, Any]]:
        """Obtiene municipios activos"""
        return [m for m in self._municipios if m["activo"]]
    
    def execute_query(self, query: str, params: tuple = None) -> List[Dict[str, Any]]:
        """Simula consultas SQL básicas para web"""
        query_lower = query.lower().strip()
        
        if "count(*)" in query_lower and "municipios" in query_lower:
            return [{"count": len([m for m in self._municipios if m["activo"]])}]
        elif "count(*)" in query_lower and "usuarios" in query_lower:
            return [{"count": len([u for u in self._users.values() if u["activo"]])}]
        elif "count(*)" in query_lower:
            return [{"count": 0}]
        
        return []

# Instancia global para web
_web_storage = WebStorageManager()

class AuthService:
    """Servicio de autenticación optimizado para web"""
    
    def __init__(self):
        self.storage = _web_storage  # Usar storage web en lugar de DB
        self.logger = get_logger(__name__)
        self.session_timeout = 3600  # 1 hora en segundos
        self._active_sessions = {}  # Sesiones activas en memoria
    
    def login(self, username: str, password: str) -> Dict[str, Any]:
        """
        Autentica un usuario - OPTIMIZADO PARA WEB
        
        Args:
            username: Nombre de usuario
            password: Contraseña en texto plano
            
        Returns:
            Dict con resultado de autenticación
        """
        try:
            self.logger.info(f"Intento de login web para usuario: {username}")
            
            # Validar entrada
            if not username or not password:
                return {
                    "success": False,
                    "message": "Usuario y contraseña son requeridos",
                    "user": None
                }
            
            # Limpiar espacios
            username = username.strip()
            password = password.strip()
            
            self.logger.info(f"Buscando usuario web: '{username}'")
            
            # Buscar usuario en storage web
            user = self.storage.get_user_by_credentials(username, password)
            
            if user:
                # Actualizar último acceso
                self.storage.update_last_access(user["id"])
                
                # Crear sesión web
                session_id = self._create_session(user["id"])
                
                # Log de acción
                self.storage.log_action(
                    user["id"], 
                    "LOGIN_SUCCESS", 
                    "AUTH", 
                    f"Login web exitoso - Sesión: {session_id[:8]}"
                )
                
                self.logger.info(f"Login web exitoso para: {username}")
                
                # Agregar información de sesión
                user["session_id"] = session_id
                user["session_expires"] = (datetime.now() + timedelta(seconds=self.session_timeout)).isoformat()
                
                return {
                    "success": True,
                    "message": "Login exitoso",
                    "user": user
                }
            else:
                # Log de intento fallido
                self.logger.warning(f"Login web fallido para: {username}")
                
                return {
                    "success": False,
                    "message": "Usuario o contraseña incorrectos",
                    "user": None
                }
                
        except Exception as e:
            self.logger.error(f"Error en autenticación web: {e}")
            return {
                "success": False,
                "message": "Error interno del sistema",
                "user": None
            }
    
    def logout(self, user_id: int, session_id: str = None) -> bool:
        """
        Cierra la sesión de un usuario - OPTIMIZADO PARA WEB
        
        Args:
            user_id: ID del usuario
            session_id: ID de sesión web
            
        Returns:
            True si el logout fue exitoso
        """
        try:
            # Eliminar sesión activa
            if session_id and session_id in self._active_sessions:
                del self._active_sessions[session_id]
            
            # Log de acción
            self.storage.log_action(
                user_id, 
                "LOGOUT", 
                "AUTH", 
                f"Logout web - Sesión: {session_id[:8] if session_id else 'N/A'}"
            )
            
            self.logger.info(f"Logout web exitoso para usuario ID: {user_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error en logout web: {e}")
            return False
    
    def validate_session(self, user_id: int, session_id: str = None) -> bool:
        """
        Valida si una sesión web es válida
        
        Args:
            user_id: ID del usuario
            session_id: ID de sesión web
            
        Returns:
            True si la sesión es válida
        """
        try:
            # Verificar que el usuario existe y está activo
            user = self.storage.get_user_by_id(user_id)
            if not user or not user.get("activo", False):
                return False
            
            # Verificar sesión si se proporciona
            if session_id:
                session_data = self._active_sessions.get(session_id)
                if not session_data:
                    return False
                
                # Verificar que la sesión no haya expirado
                if datetime.now() > session_data["expires"]:
                    del self._active_sessions[session_id]
                    return False
                
                # Verificar que la sesión pertenece al usuario
                if session_data["user_id"] != user_id:
                    return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error validando sesión web: {e}")
            return False
    
    def change_password(self, user_id: int, old_password: str, new_password: str) -> Dict[str, Any]:
        """
        Cambia la contraseña de un usuario - OPTIMIZADO PARA WEB
        
        Args:
            user_id: ID del usuario
            old_password: Contraseña actual
            new_password: Nueva contraseña
            
        Returns:
            Dict con resultado de la operación
        """
        try:
            # Obtener usuario (con password_hash)
            user_with_password = None
            for user in self.storage._users.values():
                if user["id"] == user_id:
                    user_with_password = user
                    break
            
            if not user_with_password:
                return {
                    "success": False,
                    "message": "Usuario no encontrado"
                }
            
            # Verificar contraseña actual
            old_hash = hashlib.sha256(old_password.encode('utf-8')).hexdigest()
            if user_with_password["password_hash"] != old_hash:
                return {
                    "success": False,
                    "message": "Contraseña actual incorrecta"
                }
            
            # Validar nueva contraseña
            if len(new_password) < 6:
                return {
                    "success": False,
                    "message": "La nueva contraseña debe tener al menos 6 caracteres"
                }
            
            if len(new_password) > 128:
                return {
                    "success": False,
                    "message": "La nueva contraseña es demasiado larga"
                }
            
            # Actualizar contraseña
            new_hash = hashlib.sha256(new_password.encode('utf-8')).hexdigest()
            success = self.storage.update_user_password(user_id, new_hash)
            
            if success:
                # Log de acción
                self.storage.log_action(
                    user_id, 
                    "PASSWORD_CHANGE", 
                    "AUTH", 
                    "Contraseña cambiada exitosamente en web"
                )
                
                return {
                    "success": True,
                    "message": "Contraseña actualizada exitosamente"
                }
            else:
                return {
                    "success": False,
                    "message": "Error al actualizar contraseña"
                }
                
        except Exception as e:
            self.logger.error(f"Error cambiando contraseña web: {e}")
            return {
                "success": False,
                "message": "Error interno del sistema"
            }
    
    def get_user_permissions(self, user_id: int) -> List[str]:
        """
        Obtiene los permisos de un usuario - CORREGIDO PARA WEB
        
        Args:
            user_id: ID del usuario
            
        Returns:
            Lista de permisos del usuario
        """
        try:
            user = self.storage.get_user_by_id(user_id)
            if not user:
                return []
            
            # Permisos basados en tipo_usuario (corregido)
            tipo_usuario = user.get("tipo_usuario", "consulta")
            
            if tipo_usuario == "administrador":
                return [
                    "view_dashboard",
                    "manage_users",
                    "view_reports",
                    "export_data",
                    "manage_system",
                    "view_logs",
                    "edit_all_data",
                    "delete_data",
                    "manage_config"
                ]
            elif tipo_usuario == "supervisor":
                return [
                    "view_dashboard",
                    "view_reports",
                    "export_data",
                    "edit_data",
                    "view_logs",
                    "manage_users_limited"
                ]
            elif tipo_usuario == "operador":
                return [
                    "view_dashboard",
                    "view_reports",
                    "export_data",
                    "edit_data"
                ]
            else:  # consulta
                return [
                    "view_dashboard",
                    "view_reports"
                ]
                
        except Exception as e:
            self.logger.error(f"Error obteniendo permisos web: {e}")
            return []
    
    def has_permission(self, user_id: int, permission: str) -> bool:
        """
        Verifica si un usuario tiene un permiso específico - OPTIMIZADO PARA WEB
        
        Args:
            user_id: ID del usuario
            permission: Permiso a verificar
            
        Returns:
            True si el usuario tiene el permiso
        """
        permissions = self.get_user_permissions(user_id)
        return permission in permissions
    
    def get_current_user_info(self, user_id: int) -> Optional[Dict[str, Any]]:
        """
        Obtiene información completa del usuario actual - NUEVO PARA WEB
        
        Args:
            user_id: ID del usuario
            
        Returns:
            Información del usuario o None
        """
        try:
            user = self.storage.get_user_by_id(user_id)
            if not user:
                return None
            
            # Agregar información adicional
            user["permissions"] = self.get_user_permissions(user_id)
            user["is_admin"] = user.get("tipo_usuario") == "administrador"
            user["can_manage_users"] = user.get("tipo_usuario") in ["administrador", "supervisor"]
            
            return user
            
        except Exception as e:
            self.logger.error(f"Error obteniendo info de usuario web: {e}")
            return None
    
    def get_all_users(self) -> List[Dict[str, Any]]:
        """
        Obtiene todos los usuarios - NUEVO PARA WEB
        
        Returns:
            Lista de usuarios (sin contraseñas)
        """
        try:
            users = []
            for user in self.storage._users.values():
                if user["activo"]:
                    user_copy = user.copy()
                    del user_copy["password_hash"]
                    users.append(user_copy)
            
            return sorted(users, key=lambda x: x["username"])
            
        except Exception as e:
            self.logger.error(f"Error obteniendo usuarios web: {e}")
            return []
    
    def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crea un nuevo usuario - NUEVO PARA WEB
        
        Args:
            user_data: Datos del usuario
            
        Returns:
            Resultado de la operación
        """
        try:
            username = user_data.get("username", "").strip().lower()
            password = user_data.get("password", "")
            
            # Validaciones
            if not username or not password:
                return {"success": False, "message": "Usuario y contraseña son requeridos"}
            
            if username in self.storage._users:
                return {"success": False, "message": "El usuario ya existe"}
            
            if len(password) < 6:
                return {"success": False, "message": "La contraseña debe tener al menos 6 caracteres"}
            
            # Crear usuario
            new_id = max([u["id"] for u in self.storage._users.values()]) + 1
            password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
            
            new_user = {
                "id": new_id,
                "username": username,
                "password_hash": password_hash,
                "nombre_completo": user_data.get("nombre_completo", ""),
                "email": user_data.get("email", ""),
                "tipo_usuario": user_data.get("tipo_usuario", "operador"),
                "activo": True,
                "fecha_creacion": datetime.now(),
                "ultimo_acceso": None
            }
            
            self.storage._users[username] = new_user
            
            return {"success": True, "message": "Usuario creado exitosamente", "user_id": new_id}
            
        except Exception as e:
            self.logger.error(f"Error creando usuario web: {e}")
            return {"success": False, "message": "Error interno del sistema"}
    
    def update_user(self, user_id: int, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Actualiza un usuario - NUEVO PARA WEB
        
        Args:
            user_id: ID del usuario
            user_data: Datos a actualizar
            
        Returns:
            Resultado de la operación
        """
        try:
            # Encontrar usuario
            target_user = None
            target_username = None
            
            for username, user in self.storage._users.items():
                if user["id"] == user_id:
                    target_user = user
                    target_username = username
                    break
            
            if not target_user:
                return {"success": False, "message": "Usuario no encontrado"}
            
            # Actualizar campos permitidos
            if "nombre_completo" in user_data:
                target_user["nombre_completo"] = user_data["nombre_completo"]
            
            if "email" in user_data:
                target_user["email"] = user_data["email"]
            
            if "tipo_usuario" in user_data:
                tipos_validos = ["administrador", "supervisor", "operador", "consulta"]
                if user_data["tipo_usuario"] in tipos_validos:
                    target_user["tipo_usuario"] = user_data["tipo_usuario"]
            
            if "activo" in user_data:
                target_user["activo"] = bool(user_data["activo"])
            
            return {"success": True, "message": "Usuario actualizado exitosamente"}
            
        except Exception as e:
            self.logger.error(f"Error actualizando usuario web: {e}")
            return {"success": False, "message": "Error interno del sistema"}
    
    def get_login_attempts(self, username: str = None) -> List[Dict[str, Any]]:
        """
        Obtiene intentos de login - NUEVO PARA WEB
        
        Args:
            username: Filtrar por usuario (opcional)
            
        Returns:
            Lista de intentos de login
        """
        try:
            login_logs = []
            for log in self.storage._logs:
                if log["accion"] in ["LOGIN_SUCCESS", "LOGIN_FAILED"]:
                    if not username or username.lower() in log.get("detalles", "").lower():
                        login_logs.append(log)
            
            return sorted(login_logs, key=lambda x: x["fecha"], reverse=True)
            
        except Exception as e:
            self.logger.error(f"Error obteniendo intentos de login web: {e}")
            return []
    
    def cleanup_expired_sessions(self):
        """
        Limpia sesiones expiradas - NUEVO PARA WEB
        """
        try:
            now = datetime.now()
            expired_sessions = []
            
            for session_id, session_data in self._active_sessions.items():
                if now > session_data["expires"]:
                    expired_sessions.append(session_id)
            
            for session_id in expired_sessions:
                del self._active_sessions[session_id]
            
            if expired_sessions:
                self.logger.info(f"Limpiadas {len(expired_sessions)} sesiones expiradas")
                
        except Exception as e:
            self.logger.error(f"Error limpiando sesiones web: {e}")
    
    def extend_session(self, session_id: str) -> bool:
        """
        Extiende una sesión activa - NUEVO PARA WEB
        
        Args:
            session_id: ID de la sesión
            
        Returns:
            True si se extendió exitosamente
        """
        try:
            if session_id in self._active_sessions:
                self._active_sessions[session_id]["expires"] = datetime.now() + timedelta(seconds=self.session_timeout)
                return True
            return False
            
        except Exception as e:
            self.logger.error(f"Error extendiendo sesión web: {e}")
            return False
    
    def get_active_sessions_count(self) -> int:
        """
        Obtiene el número de sesiones activas - NUEVO PARA WEB
        
        Returns:
            Número de sesiones activas
        """
        try:
            # Limpiar sesiones expiradas primero
            self.cleanup_expired_sessions()
            return len(self._active_sessions)
            
        except Exception as e:
            self.logger.error(f"Error obteniendo sesiones activas web: {e}")
            return 0
    
    def _create_session(self, user_id: int) -> str:
        """
        Crea una nueva sesión web - MÉTODO PRIVADO
        
        Args:
            user_id: ID del usuario
            
        Returns:
            ID de la sesión creada
        """
        import uuid
        
        session_id = str(uuid.uuid4())
        session_data = {
            "user_id": user_id,
            "created": datetime.now(),
            "expires": datetime.now() + timedelta(seconds=self.session_timeout),
            "last_activity": datetime.now()
        }
        
        self._active_sessions[session_id] = session_data
        return session_id
    
    def _get_client_ip(self) -> str:
        """
        Obtiene la IP del cliente - OPTIMIZADO PARA WEB
        
        Returns:
            IP del cliente o 'web-client'
        """
        # En web, esto podría obtener la IP real del request
        # Por ahora, retornamos un identificador web
        return "web-client"
    
    def get_system_stats(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas del sistema - NUEVO PARA WEB
        
        Returns:
            Estadísticas del sistema
        """
        try:
            active_users = len([u for u in self.storage._users.values() if u["activo"]])
            total_logins = len([l for l in self.storage._logs if l["accion"] == "LOGIN_SUCCESS"])
            active_sessions = self.get_active_sessions_count()
            
            return {
                "usuarios_activos": active_users,
                "total_usuarios": len(self.storage._users),
                "sesiones_activas": active_sessions,
                "total_logins": total_logins,
                "municipios": len(self.storage.get_municipios()),
                "logs_total": len(self.storage._logs)
            }
            
        except Exception as e:
            self.logger.error(f"Error obteniendo estadísticas web: {e}")
            return {}

# Función de utilidad para obtener el servicio de auth
def get_auth_service() -> AuthService:
    """
    Obtiene una instancia del servicio de autenticación
    
    Returns:
        Instancia de AuthService
    """
    return AuthService()

# Función para inicializar datos de prueba adicionales
def initialize_test_data():
    """
    Inicializa datos de prueba adicionales para web
    """
    try:
        # Agregar más usuarios de prueba si es necesario
        auth_service = get_auth_service()
        
        # Ejemplo: crear usuario de prueba adicional
        test_user_data = {
            "username": "test",
            "password": "test123",
            "nombre_completo": "Usuario de Prueba",
            "email": "test@matanzas.une.cu",
            "tipo_usuario": "consulta"
        }
        
        # Solo crear si no existe
        if "test" not in auth_service.storage._users:
            result = auth_service.create_user(test_user_data)
            if result["success"]:
                print("Usuario de prueba 'test' creado exitosamente")
        
    except Exception as e:
        print(f"Error inicializando datos de prueba: {e}")

# Inicializar datos de prueba al importar el módulo
initialize_test_data()
