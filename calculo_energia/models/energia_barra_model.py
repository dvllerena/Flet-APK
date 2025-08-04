from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class EnergiaBarra:
    """Modelo para almacenar datos de energía por municipio"""
    id: Optional[int] = None
    municipio_id: int = 0
    municipio_nombre: str = ""
    municipio_codigo: str = ""
    año: int = 2024
    mes: int = 1
    energia_mwh: float = 0.0
    observaciones: Optional[str] = None
    usuario_id: Optional[int] = None
    fecha_registro: Optional[str] = None
    fecha_modificacion: Optional[str] = None
    
    def __post_init__(self):
        if self.fecha_registro is None:
            self.fecha_registro = datetime.now().isoformat()
        if self.fecha_modificacion is None:
            self.fecha_modificacion = datetime.now().isoformat()
    
    def to_dict(self) -> dict:
        """Convierte el modelo a diccionario"""
        return {
            'id': self.id,
            'municipio_id': self.municipio_id,
            'municipio_nombre': self.municipio_nombre,
            'municipio_codigo': self.municipio_codigo,
            'año': self.año,
            'mes': self.mes,
            'energia_mwh': self.energia_mwh,
            'observaciones': self.observaciones,
            'usuario_id': self.usuario_id,
            'fecha_registro': self.fecha_registro,
            'fecha_modificacion': self.fecha_modificacion
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'EnergiaBarra':
        """Crea una instancia desde un diccionario"""
        return cls(
            id=data.get('id'),
            municipio_id=data.get('municipio_id', 0),
            municipio_nombre=data.get('municipio_nombre', ''),
            municipio_codigo=data.get('municipio_codigo', ''),
            año=data.get('año', 2024),
            mes=data.get('mes', 1),
            energia_mwh=data.get('energia_mwh', 0.0),
            observaciones=data.get('observaciones'),
            usuario_id=data.get('usuario_id'),
            fecha_registro=data.get('fecha_registro'),
            fecha_modificacion=data.get('fecha_modificacion')
        )
    
    def __str__(self) -> str:
        return f"{self.municipio_nombre} - {self.energia_mwh} MWh ({self.mes}/{self.año})"
    
    @property
    def periodo_texto(self) -> str:
        """Retorna el período en formato texto"""
        meses = {
            1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
            5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
            9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
        }
        return f"{meses.get(self.mes, 'Mes')} {self.año}"
