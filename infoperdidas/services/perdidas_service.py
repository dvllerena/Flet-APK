"""
Servicio de InfoPérdidas
Maneja todos los cálculos y operaciones de pérdidas eléctricas
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from core.database import get_db_manager
from core.logger import get_logger
from ..models.perdidas_model import PlanPerdidasModel, PerdidasCalculoModel, PerdidasResumenModel

class PerdidasService:
    """Servicio para operaciones de pérdidas eléctricas"""
    
    def __init__(self):
        self.db_manager = get_db_manager()
        self.logger = get_logger(__name__)
    
    # === OPERACIONES DE PLANES DE PÉRDIDAS ===
    
    def get_planes_by_periodo(self, año: int, mes: int = None) -> List[PlanPerdidasModel]:
        """Obtiene planes de pérdidas por período"""
        try:
            if mes:
                query = """
                    SELECT p.*, m.nombre as municipio_nombre, u.nombre_completo as usuario_nombre
                    FROM planes_perdidas p
                    LEFT JOIN municipios m ON p.municipio_id = m.id
                    LEFT JOIN usuarios u ON p.usuario_id = u.id
                    WHERE p.año = ? AND p.mes = ?
                    ORDER BY CASE WHEN p.municipio_id IS NULL THEN 0 ELSE 1 END, m.nombre
                """
                params = (año, mes)
            else:
                query = """
                    SELECT p.*, m.nombre as municipio_nombre, u.nombre_completo as usuario_nombre
                    FROM planes_perdidas p
                    LEFT JOIN municipios m ON p.municipio_id = m.id
                    LEFT JOIN usuarios u ON p.usuario_id = u.id
                    WHERE p.año = ?
                    ORDER BY p.mes, CASE WHEN p.municipio_id IS NULL THEN 0 ELSE 1 END, m.nombre
                """
                params = (año,)
            
            results = self.db_manager.execute_query(query, params)
            return [self._row_to_plan_model(row) for row in results]
            
        except Exception as e:
            self.logger.error(f"Error obteniendo planes por período: {e}")
            return []
    
    def get_plan_by_municipio_periodo(self, municipio_id: Optional[int], año: int, mes: int) -> Optional[PlanPerdidasModel]:
        """Obtiene un plan específico por municipio y período"""
        try:
            query = """
                SELECT p.*, m.nombre as municipio_nombre, u.nombre_completo as usuario_nombre
                FROM planes_perdidas p
                LEFT JOIN municipios m ON p.municipio_id = m.id
                LEFT JOIN usuarios u ON p.usuario_id = u.id
                WHERE p.año = ? AND p.mes = ? AND 
                      (p.municipio_id = ? OR (p.municipio_id IS NULL AND ? IS NULL))
            """
            
            results = self.db_manager.execute_query(query, (año, mes, municipio_id, municipio_id))
            return self._row_to_plan_model(results[0]) if results else None
            
        except Exception as e:
            self.logger.error(f"Error obteniendo plan específico: {e}")
            return None
    
    def save_plan_perdidas(self, plan: PlanPerdidasModel) -> bool:
        """Guarda o actualiza un plan de pérdidas"""
        
        
        try:
            if plan.id:
                
                # Actualizar
                query = """
                    UPDATE planes_perdidas 
                    SET plan_perdidas_pct = ?, observaciones = ?, 
                        usuario_id = ?, fecha_modificacion = CURRENT_TIMESTAMP
                    WHERE id = ?
                """
                params = (plan.plan_perdidas_pct, plan.observaciones, plan.usuario_id, plan.id)
                
            else:
                
                # Primero verificar si ya existe
                check_query = """
                    SELECT id FROM planes_perdidas 
                    WHERE municipio_id = ? AND año = ? AND mes = ?
                    OR (municipio_id IS NULL AND ? IS NULL AND año = ? AND mes = ?)
                """
                check_params = (plan.municipio_id, plan.año, plan.mes, plan.municipio_id, plan.año, plan.mes)
                
                existing = self.db_manager.execute_query(check_query, check_params)
                
                if existing:
                    
                    # Actualizar el existente
                    query = """
                        UPDATE planes_perdidas 
                        SET plan_perdidas_pct = ?, observaciones = ?, 
                            usuario_id = ?, fecha_modificacion = CURRENT_TIMESTAMP
                        WHERE id = ?
                    """
                    params = (plan.plan_perdidas_pct, plan.observaciones, plan.usuario_id, existing[0]['id'])
                    
                else:
                    
                    # Insertar nuevo
                    query = """
                        INSERT INTO planes_perdidas 
                        (municipio_id, año, mes, plan_perdidas_pct, observaciones, usuario_id)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """
                    params = (
                        plan.municipio_id, plan.año, plan.mes,
                        plan.plan_perdidas_pct, plan.observaciones, plan.usuario_id
                    )
                    
            
           
            result = self.db_manager.execute_update(query, params)
            
            
            success = result > 0
            
            
            if success:
                pass
            else:
                pass
                
            return success
            
        except Exception as e:
           
            import traceback
            traceback.print_exc()
            self.logger.error(f"Error guardando plan de pérdidas: {e}")
            return False

    def delete_plan_perdidas(self, plan_id: int) -> bool:
        """Elimina un plan de pérdidas"""
        try:
            query = "DELETE FROM planes_perdidas WHERE id = ?"
            result = self.db_manager.execute_update(query, (plan_id,))
            return result > 0
        except Exception as e:
            self.logger.error(f"Error eliminando plan de pérdidas: {e}")
            return False
    
    def copy_planes_to_year(self, año_origen: int, año_destino: int, usuario_id: int) -> bool:
        """Copia planes de un año a otro"""
        try:
            # Verificar que no existan planes en el año destino
            check_query = "SELECT COUNT(*) as count FROM planes_perdidas WHERE año = ?"
            check_result = self.db_manager.execute_query(check_query, (año_destino,))
            
            if check_result and check_result[0]['count'] > 0:
                self.logger.warning(f"Ya existen planes para el año {año_destino}")
                return False
            
            # Copiar planes
            copy_query = """
                INSERT INTO planes_perdidas (municipio_id, año, mes, plan_perdidas_pct, observaciones, usuario_id)
                SELECT municipio_id, ?, mes, plan_perdidas_pct, 
                       'Copiado desde ' || año || ' - ' || COALESCE(observaciones, ''), ?
                FROM planes_perdidas 
                WHERE año = ?
            """
            
            result = self.db_manager.execute_update(copy_query, (año_destino, usuario_id, año_origen))
            return result > 0
            
        except Exception as e:
            self.logger.error(f"Error copiando planes: {e}")
            return False
    
    # === CÁLCULOS DE PÉRDIDAS ===
    def calcular_perdidas_municipio(self, municipio_id: int, año: int, mes: int) -> Optional[PerdidasCalculoModel]:
        """Calcula pérdidas para un municipio específico"""
        try:
            # Obtener datos de energía en barra
            energia_query = """
                SELECT energia_mwh FROM energia_barra
                WHERE municipio_id = ? AND año = ? AND mes = ?
            """
            energia_result = self.db_manager.execute_query(energia_query, (municipio_id, año, mes))
            energia_barra = energia_result[0]['energia_mwh'] if energia_result else 0.0
            
            # Obtener datos de facturación
            facturacion_query = """
                SELECT facturacion_menor, facturacion_mayor FROM facturacion
                WHERE municipio_id = ? AND año = ? AND mes = ?
            """
            facturacion_result = self.db_manager.execute_query(facturacion_query, (municipio_id, año, mes))
            
            if facturacion_result:
                # Convertir de kW a MW dividiendo por 1000
                fac_menor = (facturacion_result[0]['facturacion_menor'] or 0.0) / 1000.0
                fac_mayor = (facturacion_result[0]['facturacion_mayor'] or 0.0) / 1000.0
            else:
                fac_menor = fac_mayor = 0.0
            
            # Obtener plan de pérdidas
            plan = self.get_plan_by_municipio_periodo(municipio_id, año, mes)
            plan_pct = plan.plan_perdidas_pct if plan else 0.0
            
            # Obtener nombre del municipio
            municipio_query = "SELECT nombre FROM municipios WHERE id = ?"
            municipio_result = self.db_manager.execute_query(municipio_query, (municipio_id,))
            municipio_nombre = municipio_result[0]['nombre'] if municipio_result else "Desconocido"
            
            # Calcular datos acumulados
            energia_acumulada = self._calcular_energia_acumulada(municipio_id, año, mes)
            perdidas_acumuladas = self._calcular_perdidas_acumuladas(municipio_id, año, mes)
            plan_acumulado = self._calcular_plan_acumulado(municipio_id, año, mes)
            
            # Crear modelo y calcular
            calculo = PerdidasCalculoModel(
                municipio_id=municipio_id,
                municipio_nombre=municipio_nombre,
                año=año,
                mes=mes,
                energia_barra_mwh=energia_barra,
                facturacion_mayor=fac_mayor,
                facturacion_menor=fac_menor,
                plan_perdidas_pct=plan_pct,
                energia_barra_acumulada=energia_acumulada,
                perdidas_acumuladas_mwh=perdidas_acumuladas,
                plan_perdidas_acumulado_pct=plan_acumulado
            )
            
            calculo.calcular_totales()
            return calculo
            
        except Exception as e:
            self.logger.error(f"Error calculando pérdidas municipio: {e}")
            return None

    def calcular_perdidas_provincia(self, año: int, mes: int) -> Optional[PerdidasResumenModel]:
        """Calcula pérdidas para toda la provincia"""
        try:
            # Obtener todos los municipios activos
            municipios_query = "SELECT id FROM municipios WHERE activo = 1"
            municipios_result = self.db_manager.execute_query(municipios_query)
            
            if not municipios_result:
                return None
            
            resumen = PerdidasResumenModel(año=año, mes=mes)
            municipios_detalle = []
            
            # Calcular para cada municipio
            for municipio_row in municipios_result:
                municipio_id = municipio_row['id']
                calculo = self.calcular_perdidas_municipio(municipio_id, año, mes)
                
                if calculo:
                    municipios_detalle.append(calculo)
                    
                    # Sumar a totales provinciales
                    # Los valores ya vienen convertidos a MW desde calcular_perdidas_municipio
                    resumen.total_energia_barra += calculo.energia_barra_mwh
                    resumen.total_facturacion_mayor += calculo.facturacion_mayor
                    resumen.total_facturacion_menor += calculo.facturacion_menor
                    resumen.total_energia_acumulada += calculo.energia_barra_acumulada
                    resumen.total_perdidas_acumuladas_mwh += calculo.perdidas_acumuladas_mwh
            
            # Calcular totales provinciales
            resumen.total_ventas = resumen.total_facturacion_mayor + resumen.total_facturacion_menor
            resumen.total_perdidas_mwh = resumen.total_energia_barra - resumen.total_ventas
            
            if resumen.total_energia_barra > 0:
                resumen.total_perdidas_pct = (resumen.total_perdidas_mwh / resumen.total_energia_barra) * 100
            
            if resumen.total_energia_acumulada > 0:
                resumen.total_perdidas_acumuladas_pct = (resumen.total_perdidas_acumuladas_mwh / resumen.total_energia_acumulada) * 100
            
            # Obtener plan provincial
            plan_provincial = self.get_plan_by_municipio_periodo(None, año, mes)
            resumen.total_plan_perdidas_pct = plan_provincial.plan_perdidas_pct if plan_provincial else 0.0
            
            # Calcular plan acumulado provincial
            resumen.total_plan_acumulado_pct = self._calcular_plan_acumulado(None, año, mes)
            
            resumen.municipios = municipios_detalle
            return resumen
            
        except Exception as e:
            self.logger.error(f"Error calculando pérdidas provincia: {e}")
            return None

    # === MÉTODOS AUXILIARES ===
    
    def _calcular_energia_acumulada(self, municipio_id: int, año: int, mes_hasta: int) -> float:
        """Calcula energía acumulada desde enero hasta el mes especificado"""
        try:
            query = """
                SELECT SUM(energia_mwh) as total FROM energia_barra 
                WHERE municipio_id = ? AND año = ? AND mes <= ?
            """
            result = self.db_manager.execute_query(query, (municipio_id, año, mes_hasta))
            return result[0]['total'] if result and result[0]['total'] else 0.0
        except Exception as e:
            self.logger.error(f"Error calculando energía acumulada: {e}")
            return 0.0
    
    def _calcular_perdidas_acumuladas(self, municipio_id: int, año: int, mes_hasta: int) -> float:
        """Calcula pérdidas acumuladas desde enero hasta el mes especificado"""
        try:
            # Obtener energía acumulada
            query_energia = """
                SELECT SUM(energia_mwh) as total_energia FROM energia_barra 
                WHERE municipio_id = ? AND año = ? AND mes <= ?
            """
            energia_result = self.db_manager.execute_query(query_energia, (municipio_id, año, mes_hasta))
            total_energia = energia_result[0]['total_energia'] if energia_result and energia_result[0]['total_energia'] else 0.0
            
            # Obtener facturación acumulada
            query_facturacion = """
                SELECT SUM(facturacion_menor + facturacion_mayor) as total_ventas FROM facturacion 
                WHERE municipio_id = ? AND año = ? AND mes <= ?
            """
            facturacion_result = self.db_manager.execute_query(query_facturacion, (municipio_id, año, mes_hasta))
            total_ventas_kw = facturacion_result[0]['total_ventas'] if facturacion_result and facturacion_result[0]['total_ventas'] else 0.0
            
            # Convertir facturación de kW a MW
            total_ventas_mw = total_ventas_kw / 1000.0
            
            # Calcular pérdidas acumuladas
            return total_energia - total_ventas_mw
            
        except Exception as e:
            self.logger.error(f"Error calculando pérdidas acumuladas: {e}")
            return 0.0

    
    def _calcular_plan_acumulado(self, municipio_id: Optional[int], año: int, mes_hasta: int) -> float:
        """Calcula plan de pérdidas acumulado (promedio ponderado)"""
        try:
            # Para simplificar, calculamos el promedio de los planes hasta el mes
            query = """
                SELECT AVG(plan_perdidas_pct) as promedio FROM planes_perdidas 
                WHERE año = ? AND mes <= ? AND 
                      (municipio_id = ? OR (municipio_id IS NULL AND ? IS NULL))
            """
            result = self.db_manager.execute_query(query, (año, mes_hasta, municipio_id, municipio_id))
            return result[0]['promedio'] if result and result[0]['promedio'] else 0.0
        except Exception as e:
            self.logger.error(f"Error calculando plan acumulado: {e}")
            return 0.0
    
    def _row_to_plan_model(self, row: Dict[str, Any]) -> PlanPerdidasModel:
        """Convierte una fila de BD a modelo de plan de pérdidas"""
        return PlanPerdidasModel(
            id=row.get('id'),
            municipio_id=row.get('municipio_id'),
            año=row.get('año'),
            mes=row.get('mes'),
            plan_perdidas_pct=row.get('plan_perdidas_pct', 0.0),
            observaciones=row.get('observaciones'),
            usuario_id=row.get('usuario_id'),
            fecha_creacion=row.get('fecha_creacion'),
            fecha_modificacion=row.get('fecha_modificacion'),
            municipio_nombre=row.get('municipio_nombre'),
            usuario_nombre=row.get('usuario_nombre')
        )
    
    def get_municipios_activos(self) -> List[Dict[str, Any]]:
        """Obtiene todos los municipios activos"""
        try:
            query = "SELECT id, nombre FROM municipios WHERE activo = 1 ORDER BY nombre"
            return self.db_manager.execute_query(query)
        except Exception as e:
            self.logger.error(f"Error obteniendo municipios: {e}")
            return []
    
    def verificar_datos_disponibles(self, año: int, mes: int) -> Dict[str, Any]:
        """Verifica qué datos están disponibles para el cálculo"""
        try:
            # Verificar energía en barra
            energia_query = """
                SELECT COUNT(*) as count FROM energia_barra 
                WHERE año = ? AND mes = ?
            """
            energia_result = self.db_manager.execute_query(energia_query, (año, mes))
            energia_count = energia_result[0]['count'] if energia_result else 0
            
            # Verificar facturación
            facturacion_query = """
                SELECT COUNT(*) as count FROM facturacion 
                WHERE año = ? AND mes = ?
            """
            facturacion_result = self.db_manager.execute_query(facturacion_query, (año, mes))
            facturacion_count = facturacion_result[0]['count'] if facturacion_result else 0
            
            # Verificar planes
            planes_query = """
                SELECT COUNT(*) as count FROM planes_perdidas 
                WHERE año = ? AND mes = ?
            """
            planes_result = self.db_manager.execute_query(planes_query, (año, mes))
            planes_count = planes_result[0]['count'] if planes_result else 0
            
            return {
                'energia_disponible': energia_count > 0,
                'facturacion_disponible': facturacion_count > 0,
                'planes_disponibles': planes_count > 0,
                'energia_registros': energia_count,
                'facturacion_registros': facturacion_count,
                'planes_registros': planes_count,
                'calculo_posible': energia_count > 0 and facturacion_count > 0
            }
            
        except Exception as e:
            self.logger.error(f"Error verificando datos disponibles: {e}")
            return {
                'energia_disponible': False,
                'facturacion_disponible': False,
                'planes_disponibles': False,
                'energia_registros': 0,
                'facturacion_registros': 0,
                'planes_registros': 0,
                'calculo_posible': False
            }
    
    def get_planes_by_periodo_filtered(self, año: int, mes: int = None, municipio_id = None) -> List[PlanPerdidasModel]:
        """Obtiene planes de pérdidas por período con filtro de municipio"""
        try:
            # Construir query base
            query_base = """
                SELECT p.*, m.nombre as municipio_nombre, u.nombre_completo as usuario_nombre
                FROM planes_perdidas p
                LEFT JOIN municipios m ON p.municipio_id = m.id
                LEFT JOIN usuarios u ON p.usuario_id = u.id
                WHERE p.año = ?
            """
            
            params = [año]
            
            # Agregar filtro de mes si se especifica
            if mes:
                query_base += " AND p.mes = ?"
                params.append(mes)
            
            # Agregar filtro de municipio si se especifica
            if municipio_id is not None:
                if municipio_id == "provincial":
                    query_base += " AND p.municipio_id IS NULL"
                else:
                    query_base += " AND p.municipio_id = ?"
                    params.append(municipio_id)
            
            # Ordenar resultados
            query_base += " ORDER BY p.mes, CASE WHEN p.municipio_id IS NULL THEN 0 ELSE 1 END, m.nombre"
            
            results = self.db_manager.execute_query(query_base, params)
            return [self._row_to_plan_model(row) for row in results]
            
        except Exception as e:
            self.logger.error(f"Error obteniendo planes filtrados: {e}")
            return []
    
    # Agregar estos métodos a la clase PerdidasService:

    def save_calculo_perdidas(self, calculo: PerdidasCalculoModel, usuario_id: int) -> bool:
        """Guarda un cálculo de pérdidas en la base de datos"""
        try:
            # Verificar si ya existe un cálculo para este período
            check_query = """
                SELECT id FROM calculos_perdidas 
                WHERE municipio_id = ? AND año = ? AND mes = ?
            """
            existing = self.db_manager.execute_query(
                check_query, 
                (calculo.municipio_id, calculo.año, calculo.mes)
            )
            
            if existing:
                # Actualizar existente
                query = """
                    UPDATE calculos_perdidas 
                    SET energia_barra_mwh = ?, facturacion_mayor = ?, facturacion_menor = ?,
                        total_ventas = ?, perdidas_distribucion_mwh = ?, perdidas_pct = ?,
                        plan_perdidas_pct = ?, energia_barra_acumulada = ?,
                        perdidas_acumuladas_mwh = ?, perdidas_acumuladas_pct = ?,
                        plan_perdidas_acumulado_pct = ?, usuario_id = ?,
                        fecha_actualizacion = CURRENT_TIMESTAMP
                    WHERE id = ?
                """
                params = (
                    calculo.energia_barra_mwh, calculo.facturacion_mayor, calculo.facturacion_menor,
                    calculo.total_ventas, calculo.perdidas_distribucion_mwh, calculo.perdidas_pct,
                    calculo.plan_perdidas_pct, calculo.energia_barra_acumulada,
                    calculo.perdidas_acumuladas_mwh, calculo.perdidas_acumuladas_pct,
                    calculo.plan_perdidas_acumulado_pct, usuario_id, existing[0]['id']
                )
            else:
                # Insertar nuevo
                query = """
                    INSERT INTO calculos_perdidas 
                    (municipio_id, año, mes, energia_barra_mwh, facturacion_mayor, facturacion_menor,
                    total_ventas, perdidas_distribucion_mwh, perdidas_pct, plan_perdidas_pct,
                    energia_barra_acumulada, perdidas_acumuladas_mwh, perdidas_acumuladas_pct,
                    plan_perdidas_acumulado_pct, usuario_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
                params = (
                    calculo.municipio_id, calculo.año, calculo.mes,
                    calculo.energia_barra_mwh, calculo.facturacion_mayor, calculo.facturacion_menor,
                    calculo.total_ventas, calculo.perdidas_distribucion_mwh, calculo.perdidas_pct,
                    calculo.plan_perdidas_pct, calculo.energia_barra_acumulada,
                    calculo.perdidas_acumuladas_mwh, calculo.perdidas_acumuladas_pct,
                    calculo.plan_perdidas_acumulado_pct, usuario_id
                )
            
            result = self.db_manager.execute_update(query, params)
            return result > 0
            
        except Exception as e:
            self.logger.error(f"Error guardando cálculo de pérdidas: {e}")
            return False

    def save_resumen_provincial(self, resumen: PerdidasResumenModel, usuario_id: int) -> bool:
        """Guarda el resumen provincial de pérdidas"""
        try:
            # Verificar si ya existe
            check_query = """
                SELECT id FROM resumen_perdidas_provincial 
                WHERE año = ? AND mes = ?
            """
            existing = self.db_manager.execute_query(check_query, (resumen.año, resumen.mes))
            
            if existing:
                # Actualizar
                query = """
                    UPDATE resumen_perdidas_provincial 
                    SET total_energia_barra = ?, total_facturacion_mayor = ?, total_facturacion_menor = ?,
                        total_ventas = ?, total_perdidas_mwh = ?, total_perdidas_pct = ?,
                        total_plan_perdidas_pct = ?, total_energia_acumulada = ?,
                        total_perdidas_acumuladas_mwh = ?, total_perdidas_acumuladas_pct = ?,
                        total_plan_acumulado_pct = ?, usuario_id = ?,
                        fecha_actualizacion = CURRENT_TIMESTAMP
                    WHERE id = ?
                """
                params = (
                    resumen.total_energia_barra, resumen.total_facturacion_mayor, resumen.total_facturacion_menor,
                    resumen.total_ventas, resumen.total_perdidas_mwh, resumen.total_perdidas_pct,
                    resumen.total_plan_perdidas_pct, resumen.total_energia_acumulada,
                    resumen.total_perdidas_acumuladas_mwh, resumen.total_perdidas_acumuladas_pct,
                    resumen.total_plan_acumulado_pct, usuario_id, existing[0]['id']
                )
            else:
                # Insertar
                query = """
                    INSERT INTO resumen_perdidas_provincial 
                    (año, mes, total_energia_barra, total_facturacion_mayor, total_facturacion_menor,
                    total_ventas, total_perdidas_mwh, total_perdidas_pct, total_plan_perdidas_pct,
                    total_energia_acumulada, total_perdidas_acumuladas_mwh, total_perdidas_acumuladas_pct,
                    total_plan_acumulado_pct, usuario_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
                params = (
                    resumen.año, resumen.mes, resumen.total_energia_barra,
                    resumen.total_facturacion_mayor, resumen.total_facturacion_menor,
                    resumen.total_ventas, resumen.total_perdidas_mwh, resumen.total_perdidas_pct,
                    resumen.total_plan_perdidas_pct, resumen.total_energia_acumulada,
                    resumen.total_perdidas_acumuladas_mwh, resumen.total_perdidas_acumuladas_pct,
                    resumen.total_plan_acumulado_pct, usuario_id
                )
            
            result = self.db_manager.execute_update(query, params)
            return result > 0
            
        except Exception as e:
            self.logger.error(f"Error guardando resumen provincial: {e}")
            return False

    def calcular_y_guardar_perdidas_provincia(self, año: int, mes: int, usuario_id: int) -> Optional[PerdidasResumenModel]:
        """Calcula pérdidas provinciales y las guarda en la base de datos"""
        try:
            # Calcular pérdidas (método existente)
            resumen = self.calcular_perdidas_provincia(año, mes)
            
            if not resumen:
                return None
            
            # Guardar resumen provincial
            if not self.save_resumen_provincial(resumen, usuario_id):
                self.logger.warning("No se pudo guardar el resumen provincial")
            
            # Guardar cálculos por municipio
            saved_count = 0
            for municipio_calculo in resumen.municipios:
                if self.save_calculo_perdidas(municipio_calculo, usuario_id):
                    saved_count += 1
            
            self.logger.info(f"Guardados {saved_count} cálculos de municipios para {mes:02d}/{año}")
            
            return resumen
            
        except Exception as e:
            self.logger.error(f"Error calculando y guardando pérdidas: {e}")
            return None

# Instancia global del servicio
_perdidas_service = None

def get_perdidas_service() -> PerdidasService:
    """Obtiene la instancia del servicio de pérdidas"""
    global _perdidas_service
    if _perdidas_service is None:
        _perdidas_service = PerdidasService()
    return _perdidas_service

