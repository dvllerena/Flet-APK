"""
Modelos de datos para InfoPérdidas
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any
from datetime import datetime

@dataclass
class PlanPerdidasModel:
    """Modelo para planes de pérdidas"""
    id: Optional[int] = None
    municipio_id: Optional[int] = None  # None para plan provincial
    año: int = 0
    mes: int = 0
    plan_perdidas_pct: float = 0.0
    observaciones: Optional[str] = None
    usuario_id: Optional[int] = None
    fecha_creacion: Optional[datetime] = None
    fecha_modificacion: Optional[datetime] = None
    
    # Campos adicionales para mostrar
    municipio_nombre: Optional[str] = None
    usuario_nombre: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte el modelo a diccionario"""
        return {
            'id': self.id,
            'municipio_id': self.municipio_id,
            'año': self.año,
            'mes': self.mes,
            'plan_perdidas_pct': self.plan_perdidas_pct,
            'observaciones': self.observaciones,
            'usuario_id': self.usuario_id,
            'fecha_creacion': self.fecha_creacion,
            'fecha_modificacion': self.fecha_modificacion,
            'municipio_nombre': self.municipio_nombre,
            'usuario_nombre': self.usuario_nombre
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PlanPerdidasModel':
        """Crea un modelo desde diccionario"""
        return cls(
            id=data.get('id'),
            municipio_id=data.get('municipio_id'),
            año=data.get('año', 0),
            mes=data.get('mes', 0),
            plan_perdidas_pct=data.get('plan_perdidas_pct', 0.0),
            observaciones=data.get('observaciones'),
            usuario_id=data.get('usuario_id'),
            fecha_creacion=data.get('fecha_creacion'),
            fecha_modificacion=data.get('fecha_modificacion'),
            municipio_nombre=data.get('municipio_nombre'),
            usuario_nombre=data.get('usuario_nombre')
        )

@dataclass
class PerdidasCalculoModel:
    """Modelo para cálculos de pérdidas mensuales"""
    municipio_id: Optional[int] = None
    municipio_nombre: Optional[str] = None
    año: int = 0
    mes: int = 0
    
    # Datos base
    energia_barra_mwh: float = 0.0
    facturacion_mayor: float = 0.0
    facturacion_menor: float = 0.0
    
    # Cálculos mensuales
    total_ventas: float = 0.0
    perdidas_distribucion_mwh: float = 0.0
    perdidas_pct: float = 0.0
    plan_perdidas_pct: float = 0.0
    
    # Cálculos acumulados
    energia_barra_acumulada: float = 0.0
    perdidas_acumuladas_mwh: float = 0.0
    perdidas_acumuladas_pct: float = 0.0
    plan_perdidas_acumulado_pct: float = 0.0
    
    def calcular_totales(self):
        """Calcula los totales basados en los datos base"""
        self.total_ventas = self.facturacion_mayor + self.facturacion_menor
        self.perdidas_distribucion_mwh = self.energia_barra_mwh - self.total_ventas
        
        if self.energia_barra_mwh > 0:
            self.perdidas_pct = (self.perdidas_distribucion_mwh / self.energia_barra_mwh) * 100
        
        if self.energia_barra_acumulada > 0:
            self.perdidas_acumuladas_pct = (self.perdidas_acumuladas_mwh / self.energia_barra_acumulada) * 100

@dataclass
class PerdidasResumenModel:
    """Modelo para resumen de pérdidas"""
    año: int = 0
    mes: int = 0
    
    # Totales provinciales mensuales
    total_energia_barra: float = 0.0
    total_facturacion_mayor: float = 0.0
    total_facturacion_menor: float = 0.0
    total_ventas: float = 0.0
    total_perdidas_mwh: float = 0.0
    total_perdidas_pct: float = 0.0
    total_plan_perdidas_pct: float = 0.0
    
    # Totales provinciales acumulados
    total_energia_acumulada: float = 0.0
    total_perdidas_acumuladas_mwh: float = 0.0
    total_perdidas_acumuladas_pct: float = 0.0
    total_plan_acumulado_pct: float = 0.0
    
    # Detalles por municipio
    municipios: list = None
    
    def __post_init__(self):
        if self.municipios is None:
            self.municipios = []
