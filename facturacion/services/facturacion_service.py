"""
Servicio de facturación
Maneja todas las operaciones de datos de facturación
"""

from typing import List, Optional, Dict, Any
from core.database import get_db_manager
from core.logger import get_logger
from facturacion.models.facturacion_model import FacturacionModel

class FacturacionService:
    """Servicio para operaciones de facturación"""
    
    def __init__(self):
        self.db_manager = get_db_manager()  # Corregido: usar db_manager en lugar de db
        self.logger = get_logger(__name__)
    
    # === OPERACIONES DE FACTURACIÓN ===
    
    def get_facturacion_by_periodo(self, año: int, mes: int) -> List[FacturacionModel]:
        """Obtiene facturación por período"""
        query = """
            SELECT f.*, m.nombre as municipio_nombre, u.nombre_completo as usuario_nombre
            FROM facturacion f
            LEFT JOIN municipios m ON f.municipio_id = m.id
            LEFT JOIN usuarios u ON f.usuario_id = u.id
            WHERE f.año = ? AND f.mes = ?
            ORDER BY m.nombre, f.facturacion_menor, f.facturacion_mayor
        """
        
        results = self.db_manager.execute_query(query, (año, mes))
        return [self._row_to_facturacion_model(row) for row in results]
    
    def get_facturacion_by_municipio(self, municipio_id: int, año: int = None, mes: int = None) -> List[FacturacionModel]:
        """Obtiene facturación por municipio"""
        if año and mes:
            query = """
                SELECT f.*, m.nombre as municipio_nombre, u.nombre_completo as usuario_nombre
                FROM facturacion f
                LEFT JOIN municipios m ON f.municipio_id = m.id
                LEFT JOIN usuarios u ON f.usuario_id = u.id
                WHERE f.municipio_id = ? AND f.año = ? AND f.mes = ?
                ORDER BY f.año DESC, f.mes DESC
            """
            params = (municipio_id, año, mes)
        else:
            query = """
                SELECT f.*, m.nombre as municipio_nombre, u.nombre_completo as usuario_nombre
                FROM facturacion f
                LEFT JOIN municipios m ON f.municipio_id = m.id
                LEFT JOIN usuarios u ON f.usuario_id = u.id
                WHERE f.municipio_id = ?
                ORDER BY f.año DESC, f.mes DESC
            """
            params = (municipio_id,)
        
        results = self.db_manager.execute_query(query, params)
        return [self._row_to_facturacion_model(row) for row in results]
    
    def get_facturaciones_filtered(self, municipio_id: int = None, año: int = None, mes: int = None) -> List[FacturacionModel]:
        """Obtiene facturaciones filtradas"""
        try:
            query = """
                SELECT f.*, m.nombre as municipio_nombre, u.nombre_completo as usuario_nombre
                FROM facturacion f
                LEFT JOIN municipios m ON f.municipio_id = m.id
                LEFT JOIN usuarios u ON f.usuario_id = u.id
                WHERE 1=1
            """
            params = []
            
            if municipio_id:
                query += " AND f.municipio_id = ?"
                params.append(municipio_id)
            
            if año:
                query += " AND f.año = ?"
                params.append(año)
            
            if mes:
                query += " AND f.mes = ?"
                params.append(mes)
            
            query += " ORDER BY f.año DESC, f.mes DESC, m.nombre"
            
            results = self.db_manager.execute_query(query, tuple(params))
            return [self._row_to_facturacion_model(row) for row in results]
            
        except Exception as e:
            self.logger.error(f"Error al obtener facturaciones filtradas: {e}")
            return []
    
    def get_facturacion_by_municipio_periodo(self, municipio_id: int, año: int, mes: int) -> Optional[FacturacionModel]:
        """Obtiene facturación por municipio y período específico"""
        try:
            query = """
                SELECT f.*, m.nombre as municipio_nombre, u.nombre_completo as usuario_nombre
                FROM facturacion f
                LEFT JOIN municipios m ON f.municipio_id = m.id
                LEFT JOIN usuarios u ON f.usuario_id = u.id
                WHERE f.municipio_id = ? AND f.año = ? AND f.mes = ?
            """
            
            results = self.db_manager.execute_query(query, (municipio_id, año, mes))
            
            if results:
                return self._row_to_facturacion_model(results[0])
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error al obtener facturación por período: {e}")
            return None
    
    def save_facturacion(self, facturacion: FacturacionModel) -> bool:
        """Guarda o actualiza facturación"""
        try:
            if facturacion.id:
                # Actualizar
                return self.update_facturacion(facturacion)
            else:
                # Insertar nueva
                query = """
                    INSERT INTO facturacion 
                    (municipio_id, año, mes, facturacion_menor, facturacion_mayor, 
                     facturacion_total, usuario_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """
                params = (
                    facturacion.municipio_id, facturacion.año, facturacion.mes,
                    facturacion.facturacion_menor, facturacion.facturacion_mayor,
                    facturacion.facturacion_total, facturacion.usuario_id
                )
            
            result = self.db_manager.execute_update(query, params)
            return result > 0
            
        except Exception as e:
            self.logger.error(f"Error al guardar facturación: {e}")
            return False
    
    def update_facturacion(self, facturacion: FacturacionModel) -> bool:
        """Actualiza una facturación existente"""
        try:
            query = """
                UPDATE facturacion 
                SET facturacion_menor = ?, facturacion_mayor = ?, facturacion_total = ?,
                    fecha_actualizacion = CURRENT_TIMESTAMP
                WHERE id = ?
            """
            
            rows_affected = self.db_manager.execute_update(
                query, 
                (facturacion.facturacion_menor, facturacion.facturacion_mayor, 
                 facturacion.facturacion_total, facturacion.id)
            )
            
            return rows_affected > 0
            
        except Exception as e:
            self.logger.error(f"Error al actualizar facturación: {e}")
            return False
    
    def delete_facturacion(self, facturacion_id: int) -> bool:
        """Elimina una facturación"""
        try:
            query = "DELETE FROM facturacion WHERE id = ?"
            result = self.db_manager.execute_update(query, (facturacion_id,))
            return result > 0
        except Exception as e:
            self.logger.error(f"Error al eliminar facturación: {e}")
            return False
    
    # === OPERACIONES DE MUNICIPIOS ===
    
    def get_municipios_activos(self) -> List[Dict[str, Any]]:
        """Obtiene todos los municipios activos"""
        try:
            query = "SELECT id, nombre FROM municipios WHERE activo = 1 ORDER BY nombre"
            result = self.db_manager.execute_query(query)
            self.logger.info(f"Municipios obtenidos: {len(result)}")
            return result
        except Exception as e:
            self.logger.error(f"Error al obtener municipios: {e}")
            return []
    
    # === MÉTODOS AUXILIARES ===
    
    def get_resumen_facturacion(self, año: int, mes: int) -> Dict[str, Any]:
        """Obtiene resumen de facturación por período"""
        try:
            query = """
                SELECT 
                    COUNT(*) as total_registros,
                    SUM(facturacion_menor) as total_menor,
                    SUM(facturacion_mayor) as total_mayor,
                    SUM(facturacion_total) as total_general
                FROM facturacion 
                WHERE año = ? AND mes = ?
            """
            
            results = self.db_manager.execute_query(query, (año, mes))
            
            if results:
                row = results[0]
                return {
                    'año': año,
                    'mes': mes,
                    'total_registros': row['total_registros'] or 0,
                    'total_menor': row['total_menor'] or 0,
                    'total_mayor': row['total_mayor'] or 0,
                    'total_general': row['total_general'] or 0
                }
            
            return {
                'año': año,
                'mes': mes,
                'total_registros': 0,
                'total_menor': 0,
                'total_mayor': 0,
                'total_general': 0
            }
            
        except Exception as e:
            self.logger.error(f"Error al obtener resumen: {e}")
            return {
                'año': año,
                'mes': mes,
                'total_registros': 0,
                'total_menor': 0,
                'total_mayor': 0,
                'total_general': 0
            }
    
    def verificar_facturacion_existe(self, municipio_id: int, año: int, mes: int) -> bool:
        """Verifica si ya existe una facturación específica"""
        try:
            query = """
                SELECT COUNT(*) as count FROM facturacion 
                WHERE municipio_id = ? AND año = ? AND mes = ?
            """
            
            result = self.db_manager.execute_query(query, (municipio_id, año, mes))
            return result[0]['count'] > 0 if result else False
            
        except Exception as e:
            self.logger.error(f"Error al verificar facturación existente: {e}")
            return False
    
    def _row_to_facturacion_model(self, row: Dict[str, Any]) -> FacturacionModel:
        """Convierte una fila de BD a modelo de facturación"""
        return FacturacionModel(
            id=row.get('id'),
            municipio_id=row.get('municipio_id'),
            año=row.get('año'),
            mes=row.get('mes'),
            facturacion_menor=row.get('facturacion_menor', 0),
            facturacion_mayor=row.get('facturacion_mayor', 0),
            facturacion_total=row.get('facturacion_total', 0),
            fecha_creacion=row.get('fecha_creacion'),
            fecha_actualizacion=row.get('fecha_actualizacion'),
            usuario_id=row.get('usuario_id'),
            municipio_nombre=row.get('municipio_nombre'),
            usuario_nombre=row.get('usuario_nombre')
        )

# Instancia global del servicio
_facturacion_service = None

def get_facturacion_service() -> FacturacionService:
    """Obtiene la instancia del servicio de facturación"""
    global _facturacion_service
    if _facturacion_service is None:
        _facturacion_service = FacturacionService()
    return _facturacion_service
