"""
Modelo de datos para facturación
"""

from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from datetime import datetime

@dataclass
class FacturacionModel:
    """Modelo de facturación"""
    id: Optional[int] = None
    municipio_id: int = 0
    año: int = 0
    mes: int = 0
    facturacion_menor: float = 0.0
    facturacion_mayor: float = 0.0
    facturacion_total: float = 0.0
    fecha_creacion: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None
    usuario_id: Optional[int] = None
    
    # Campos adicionales para mostrar
    municipio_nombre: Optional[str] = None
    usuario_nombre: Optional[str] = None
    
    # Propiedades de compatibilidad para la pantalla de edición
    @property
    def tipo_facturacion(self) -> str:
        """Compatibilidad - siempre retorna 'total'"""
        return "total"
    
    @property
    def tipo_carga(self) -> str:
        """Compatibilidad - siempre retorna 'neta'"""
        return "neta"
    
    @property
    def valor(self) -> float:
        """Compatibilidad - retorna facturación total"""
        return self.facturacion_total
    
    @property
    def observaciones(self) -> Optional[str]:
        """Compatibilidad - campo de observaciones"""
        return None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte el modelo a diccionario"""
        return {
            'id': self.id,
            'municipio_id': self.municipio_id,
            'año': self.año,
            'mes': self.mes,
            'facturacion_menor': self.facturacion_menor,
            'facturacion_mayor': self.facturacion_mayor,
            'facturacion_total': self.facturacion_total,
            'fecha_creacion': self.fecha_creacion,
            'fecha_actualizacion': self.fecha_actualizacion,
            'usuario_id': self.usuario_id,
            'municipio_nombre': self.municipio_nombre,
            'usuario_nombre': self.usuario_nombre
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FacturacionModel':
        """Crea un modelo desde diccionario"""
        return cls(
            id=data.get('id'),
            municipio_id=data.get('municipio_id', 0),
            año=data.get('año', 0),
            mes=data.get('mes', 0),
            facturacion_menor=data.get('facturacion_menor', 0.0),
            facturacion_mayor=data.get('facturacion_mayor', 0.0),
            facturacion_total=data.get('facturacion_total', 0.0),
            fecha_creacion=data.get('fecha_creacion'),
            fecha_actualizacion=data.get('fecha_actualizacion'),
            usuario_id=data.get('usuario_id'),
            municipio_nombre=data.get('municipio_nombre'),
            usuario_nombre=data.get('usuario_nombre')
        )

@dataclass
class ClienteMunicipioModel:
    """Modelo de cliente por municipio"""
    id: Optional[int] = None
    municipio_id: int = 0
    codigo_cliente: str = ""
    nombre_cliente: str = ""
    consumo_kwh: float = 0.0
    activo: bool = True
    observaciones: Optional[str] = None
    fecha_creacion: Optional[datetime] = None
    
    # Campo adicional
    municipio_nombre: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte el modelo a diccionario"""
        return {
            'id': self.id,
            'municipio_id': self.municipio_id,
            'codigo_cliente': self.codigo_cliente,
            'nombre_cliente': self.nombre_cliente,
            'consumo_kwh': self.consumo_kwh,
            'activo': self.activo,
            'observaciones': self.observaciones,
            'fecha_creacion': self.fecha_creacion,
            'municipio_nombre': self.municipio_nombre
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ClienteMunicipioModel':
        """Crea un modelo desde diccionario"""
        return cls(
            id=data.get('id'),
            municipio_id=data.get('municipio_id', 0),
            codigo_cliente=data.get('codigo_cliente', ''),
            nombre_cliente=data.get('nombre_cliente', ''),
            consumo_kwh=data.get('consumo_kwh', 0.0),
            activo=data.get('activo', True),
            observaciones=data.get('observaciones'),
            fecha_creacion=data.get('fecha_creacion'),
            municipio_nombre=data.get('municipio_nombre')
        )

@dataclass
class TransferenciaMunicipioModel:
    """Modelo de transferencia entre municipios"""
    id: Optional[int] = None
    cliente_id: int = 0
    municipio_origen_id: int = 0
    municipio_destino_id: int = 0
    consumo_transferido: float = 0.0
    año: int = 0
    mes: int = 0
    motivo: Optional[str] = None
    usuario_id: Optional[int] = None
    fecha_transferencia: Optional[datetime] = None
    
    # Campos adicionales
    cliente_nombre: Optional[str] = None
    municipio_origen_nombre: Optional[str] = None
    municipio_destino_nombre: Optional[str] = None
    usuario_nombre: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte el modelo a diccionario"""
        return {
            'id': self.id,
            'cliente_id': self.cliente_id,
            'municipio_origen_id': self.municipio_origen_id,
            'municipio_destino_id': self.municipio_destino_id,
            'consumo_transferido': self.consumo_transferido,
            'año': self.año,
            'mes': self.mes,
            'motivo': self.motivo,
            'usuario_id': self.usuario_id,
            'fecha_transferencia': self.fecha_transferencia,
            'cliente_nombre': self.cliente_nombre,
            'municipio_origen_nombre': self.municipio_origen_nombre,
            'municipio_destino_nombre': self.municipio_destino_nombre,
            'usuario_nombre': self.usuario_nombre
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TransferenciaMunicipioModel':
        """Crea un modelo desde diccionario"""
        return cls(
            id=data.get('id'),
            cliente_id=data.get('cliente_id', 0),
            municipio_origen_id=data.get('municipio_origen_id', 0),
            municipio_destino_id=data.get('municipio_destino_id', 0),
            consumo_transferido=data.get('consumo_transferido', 0.0),
            año=data.get('año', 0),
            mes=data.get('mes', 0),
            motivo=data.get('motivo'),
            usuario_id=data.get('usuario_id'),
            fecha_transferencia=data.get('fecha_transferencia'),
            cliente_nombre=data.get('cliente_nombre'),
            municipio_origen_nombre=data.get('municipio_origen_nombre'),
            municipio_destino_nombre=data.get('municipio_destino_nombre'),
            usuario_nombre=data.get('usuario_nombre')
        )
