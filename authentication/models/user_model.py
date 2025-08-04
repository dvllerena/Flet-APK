"""
Modelo de usuario
Define la estructura y validaciones para usuarios
OPTIMIZADO PARA WEB
"""

from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, EmailStr, validator
import re

class User(BaseModel):
    """Modelo de usuario optimizado para web"""
    
    id: Optional[int] = None
    username: str
    email: Optional[EmailStr] = None
    nombre_completo: Optional[str] = None
    tipo_usuario: str = "operador"
    activo: bool = True
    fecha_creacion: Optional[datetime] = None
    ultimo_acceso: Optional[datetime] = None
    
    @validator('username')
    def validate_username(cls, v):
        if not v or not v.strip():
            raise ValueError('El nombre de usuario es requerido')
        
        v = v.strip()
        
        if len(v) < 3:
            raise ValueError('El nombre de usuario debe tener al menos 3 caracteres')
        if len(v) > 50:
            raise ValueError('El nombre de usuario no puede tener más de 50 caracteres')
        
        # Validar caracteres permitidos (web-safe)
        if not re.match(r'^[a-zA-Z0-9_.-]+$', v):
            raise ValueError('El nombre de usuario solo puede contener letras, números, puntos, guiones y guiones bajos')
        
        return v.lower()
    
    @validator('tipo_usuario')
    def validate_tipo_usuario(cls, v):
        tipos_validos = ['administrador', 'supervisor', 'operador', 'consulta']
        if v not in tipos_validos:
            raise ValueError(f'Tipo de usuario debe ser uno de: {tipos_validos}')
        return v
    
    @validator('email')
    def validate_email_web(cls, v):
        """Validación adicional de email para web"""
        if v and len(v) > 254:  # RFC 5321 limit
            raise ValueError('El email es demasiado largo')
        return v
    
    @validator('nombre_completo')
    def validate_nombre_completo(cls, v):
        """Validación de nombre completo"""
        if v and len(v.strip()) < 2:
            raise ValueError('El nombre completo debe tener al menos 2 caracteres')
        if v and len(v) > 100:
            raise ValueError('El nombre completo no puede tener más de 100 caracteres')
        return v.strip() if v else v
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte el modelo a diccionario (útil para web)"""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "nombre_completo": self.nombre_completo,
            "tipo_usuario": self.tipo_usuario,
            "activo": self.activo,
            "fecha_creacion": self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            "ultimo_acceso": self.ultimo_acceso.isoformat() if self.ultimo_acceso else None
        }
    
    def get_display_name(self) -> str:
        """Obtiene el nombre para mostrar"""
        return self.nombre_completo or self.username.title()
    
    def is_admin(self) -> bool:
        """Verifica si el usuario es administrador"""
        return self.tipo_usuario == 'administrador'
    
    def can_manage_users(self) -> bool:
        """Verifica si puede gestionar usuarios"""
        return self.tipo_usuario in ['administrador', 'supervisor']
    
    class Config:
        from_attributes = True
        # Configuración adicional para web
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }

class UserCreate(BaseModel):
    """Modelo para crear usuarios - OPTIMIZADO PARA WEB"""
    
    username: str
    password: str
    email: Optional[EmailStr] = None
    nombre_completo: Optional[str] = None
    tipo_usuario: str = "operador"
    
    @validator('username')
    def validate_username_create(cls, v):
        if not v or not v.strip():
            raise ValueError('El nombre de usuario es requerido')
        
        v = v.strip()
        
        if len(v) < 3:
            raise ValueError('El nombre de usuario debe tener al menos 3 caracteres')
        if len(v) > 50:
            raise ValueError('El nombre de usuario no puede tener más de 50 caracteres')
        
        # Validar caracteres permitidos
        if not re.match(r'^[a-zA-Z0-9_.-]+$', v):
            raise ValueError('El nombre de usuario solo puede contener letras, números, puntos, guiones y guiones bajos')
        
        return v.lower()
    
    @validator('password')
    def validate_password(cls, v):
        if not v:
            raise ValueError('La contraseña es requerida')
        
        if len(v) < 6:
            raise ValueError('La contraseña debe tener al menos 6 caracteres')
        
        if len(v) > 128:
            raise ValueError('La contraseña no puede tener más de 128 caracteres')
        
        # Validación de seguridad básica para web
        if v.lower() in ['123456', 'password', 'admin', 'qwerty']:
            raise ValueError('La contraseña es demasiado común')
        
        return v
    
    @validator('tipo_usuario')
    def validate_tipo_usuario_create(cls, v):
        tipos_validos = ['administrador', 'supervisor', 'operador', 'consulta']
        if v not in tipos_validos:
            raise ValueError(f'Tipo de usuario debe ser uno de: {tipos_validos}')
        return v
    
    @validator('nombre_completo')
    def validate_nombre_completo_create(cls, v):
        if v and len(v.strip()) < 2:
            raise ValueError('El nombre completo debe tener al menos 2 caracteres')
        if v and len(v) > 100:
            raise ValueError('El nombre completo no puede tener más de 100 caracteres')
        return v.strip() if v else v

class UserLogin(BaseModel):
    """Modelo para login de usuarios - OPTIMIZADO PARA WEB"""
    
    username: str
    password: str
    remember_me: Optional[bool] = False  # Para web sessions
    
    @validator('username')
    def validate_username_login(cls, v):
        if not v or not v.strip():
            raise ValueError('El nombre de usuario es requerido')
        return v.strip().lower()
    
    @validator('password')
    def validate_password_login(cls, v):
        if not v:
            raise ValueError('La contraseña es requerida')
        return v

class UserUpdate(BaseModel):
    """Modelo para actualizar usuarios - NUEVO PARA WEB"""
    
    email: Optional[EmailStr] = None
    nombre_completo: Optional[str] = None
    tipo_usuario: Optional[str] = None
    activo: Optional[bool] = None
    
    @validator('tipo_usuario')
    def validate_tipo_usuario_update(cls, v):
        if v is not None:
            tipos_validos = ['administrador', 'supervisor', 'operador', 'consulta']
            if v not in tipos_validos:
                raise ValueError(f'Tipo de usuario debe ser uno de: {tipos_validos}')
        return v
    
    @validator('nombre_completo')
    def validate_nombre_completo_update(cls, v):
        if v is not None:
            if len(v.strip()) < 2:
                raise ValueError('El nombre completo debe tener al menos 2 caracteres')
            if len(v) > 100:
                raise ValueError('El nombre completo no puede tener más de 100 caracteres')
            return v.strip()
        return v

class PasswordChange(BaseModel):
    """Modelo para cambio de contraseña - NUEVO PARA WEB"""
    
    current_password: str
    new_password: str
    confirm_password: str
    
    @validator('current_password')
    def validate_current_password(cls, v):
        if not v:
            raise ValueError('La contraseña actual es requerida')
        return v
    
    @validator('new_password')
    def validate_new_password(cls, v):
        if not v:
            raise ValueError('La nueva contraseña es requerida')
        
        if len(v) < 6:
            raise ValueError('La nueva contraseña debe tener al menos 6 caracteres')
        
        if len(v) > 128:
            raise ValueError('La nueva contraseña no puede tener más de 128 caracteres')
        
        return v
    
    @validator('confirm_password')
    def validate_confirm_password(cls, v, values):
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('Las contraseñas no coinciden')
        return v

# Funciones de utilidad para web
def create_user_session_data(user: User) -> Dict[str, Any]:
    """Crea datos de sesión para web"""
    return {
        "user_id": user.id,
        "username": user.username,
        "nombre_completo": user.nombre_completo,
        "tipo_usuario": user.tipo_usuario,
        "is_admin": user.is_admin(),
        "can_manage_users": user.can_manage_users()
    }

def validate_user_permissions(user: User, required_permission: str) -> bool:
    """Valida permisos de usuario para web"""
    permission_map = {
        'administrador': ['all'],
        'supervisor': ['view', 'edit', 'create'],
        'operador': ['view', 'edit'],
        'consulta': ['view']
    }
    
    user_permissions = permission_map.get(user.tipo_usuario, [])
    return 'all' in user_permissions or required_permission in user_permissions
