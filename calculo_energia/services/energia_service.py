"""
Servicio para gestión de datos de energía eléctrica
Maneja operaciones CRUD y lógica de negocio para energía por barra
"""

from typing import List, Dict, Any, Optional, TYPE_CHECKING
from dataclasses import dataclass
from datetime import datetime
from core.logger import get_logger
from core.database import get_db_manager

# Import condicional para type hints
if TYPE_CHECKING:
    import pandas as pd

@dataclass
class EnergiaRecord:
    """Clase para representar un registro de energía"""
    id: int
    municipio_id: int
    municipio_nombre: str
    municipio_codigo: str
    año: int
    mes: int
    energia_mwh: float
    observaciones: Optional[str]
    fecha_registro: str
    fecha_modificacion: str
    usuario_id: int
    
    @property
    def periodo_texto(self) -> str:
        """Retorna el período en formato texto"""
        meses = ['', 'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        return f"{meses[self.mes]} {self.año}"
    
    @property
    def energia_formateada(self) -> str:
        """Retorna la energía formateada"""
        return f"{self.energia_mwh:,.1f} MWh"


class EnergiaService:
    """Servicio para gestión de datos de energía eléctrica"""
    
    def __init__(self):
        self.logger = get_logger(__name__)
        self.db_manager = get_db_manager()

    def get_energia_by_periodo(self, año: int, mes: int) -> List[EnergiaRecord]:
        """Obtiene registros de energía por período"""
        try:
            query = """
            SELECT eb.*, m.nombre as municipio_nombre, m.codigo as municipio_codigo
            FROM energia_barra eb
            JOIN municipios m ON eb.municipio_id = m.id
            WHERE eb.año = ? AND eb.mes = ?
            ORDER BY m.nombre
            """
            
            results = self.db_manager.execute_query(query, (año, mes))
            
            records = []
            for row in results:
                record = EnergiaRecord(
                    id=row['id'],
                    municipio_id=row['municipio_id'],
                    municipio_nombre=row['municipio_nombre'],
                    municipio_codigo=row['municipio_codigo'],
                    año=row['año'],
                    mes=row['mes'],
                    energia_mwh=row['energia_mwh'],
                    observaciones=row.get('observaciones'),
                    fecha_registro=row['fecha_registro'],
                    fecha_modificacion=row.get('fecha_modificacion', row['fecha_registro']),
                    usuario_id=row['usuario_id']
                )
                records.append(record)
            
            self.logger.info(f"Obtenidos {len(records)} registros para {año}-{mes:02d}")
            return records
            
        except Exception as e:
            self.logger.error(f"Error obteniendo energía por período: {e}")
            return []
    
    def get_energia_by_id(self, energia_id: int) -> Optional[EnergiaRecord]:
        """Obtiene un registro de energía por ID"""
        try:
            query = """
            SELECT eb.*, m.nombre as municipio_nombre, m.codigo as municipio_codigo
            FROM energia_barra eb
            JOIN municipios m ON eb.municipio_id = m.id
            WHERE eb.id = ?
            """
            
            results = self.db_manager.execute_query(query, (energia_id,))
            
            if results:
                row = results[0]
                return EnergiaRecord(
                    id=row['id'],
                    municipio_id=row['municipio_id'],
                    municipio_nombre=row['municipio_nombre'],
                    municipio_codigo=row['municipio_codigo'],
                    año=row['año'],
                    mes=row['mes'],
                    energia_mwh=row['energia_mwh'],
                    observaciones=row.get('observaciones'),
                    fecha_registro=row['fecha_registro'],
                    fecha_modificacion=row.get('fecha_modificacion', row['fecha_registro']),
                    usuario_id=row['usuario_id']
                )
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error obteniendo energía por ID: {e}")
            return None
    
    def crear_energia(self, data: Dict[str, Any]) -> bool:
        """Crea un nuevo registro de energía"""
        try:
            # Validar datos requeridos
            required_fields = ['municipio_id', 'año', 'mes', 'energia_mwh', 'usuario_id']
            for field in required_fields:
                if field not in data:
                    self.logger.error(f"Campo requerido faltante: {field}")
                    return False
            
            # Verificar que no existe un registro para el mismo período
            existing = self._get_energia_by_periodo(
                data['municipio_id'], 
                data['año'], 
                data['mes']
            )
            
            if existing:
                self.logger.warning(f"Ya existe registro para municipio {data['municipio_id']}, {data['año']}-{data['mes']:02d}")
                return False
            
            # Insertar nuevo registro
            query = """
            INSERT INTO energia_barra (municipio_id, año, mes, energia_mwh, observaciones, usuario_id, fecha_registro, fecha_modificacion)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """
            
            fecha_actual = datetime.now().isoformat()
            
            rows_affected = self.db_manager.execute_update(
                query,
                (
                    data['municipio_id'],
                    data['año'],
                    data['mes'],
                    data['energia_mwh'],
                    data.get('observaciones'),
                    data['usuario_id'],
                    fecha_actual,
                    fecha_actual
                )
            )
            
            success = rows_affected > 0
            if success:
                self.logger.info(f"Registro de energía creado: Municipio {data['municipio_id']}, {data['año']}-{data['mes']:02d}")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Error creando registro de energía: {e}")
            return False
    
    def actualizar_energia(self, energia_id: int, data: Dict[str, Any]) -> bool:
        """Actualiza un registro de energía existente"""
        try:
            # Verificar que el registro existe
            existing = self.get_energia_by_id(energia_id)
            if not existing:
                self.logger.error(f"Registro no encontrado: {energia_id}")
                return False
            
            # Actualizar registro
            query = """
            UPDATE energia_barra 
            SET energia_mwh = ?, observaciones = ?, fecha_modificacion = ?, usuario_id = ?
            WHERE id = ?
            """
            
            fecha_modificacion = datetime.now().isoformat()
            
            rows_affected = self.db_manager.execute_update(
                query,
                (
                    data.get('energia_mwh', existing.energia_mwh),
                    data.get('observaciones', existing.observaciones),
                    fecha_modificacion,
                    data.get('usuario_id', existing.usuario_id),
                    energia_id
                )
            )
            
            success = rows_affected > 0
            if success:
                self.logger.info(f"Registro de energía actualizado: ID {energia_id}")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Error actualizando registro de energía: {e}")
            return False
    
    def eliminar_energia(self, energia_id: int) -> bool:
        """Elimina un registro de energía"""
        try:
            # Verificar que el registro existe
            existing = self.get_energia_by_id(energia_id)
            if not existing:
                self.logger.error(f"Registro no encontrado: {energia_id}")
                return False
            
            # Eliminar registro
            query = "DELETE FROM energia_barra WHERE id = ?"
            rows_affected = self.db_manager.execute_update(query, (energia_id,))
            
            success = rows_affected > 0
            if success:
                self.logger.info(f"Registro de energía eliminado: ID {energia_id}")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Error eliminando registro de energía: {e}")
            return False
    
    def get_municipios(self) -> List[Dict[str, Any]]:
        """Obtiene la lista de municipios activos"""
        try:
            query = "SELECT * FROM municipios WHERE activo = 1 ORDER BY nombre"
            results = self.db_manager.execute_query(query)
            
            self.logger.info(f"Obtenidos {len(results)} municipios")
            return results
            
        except Exception as e:
            self.logger.error(f"Error obteniendo municipios: {e}")
            return []
    
    def get_resumen_periodo(self, año: int, mes: int) -> Dict[str, Any]:
        """Obtiene resumen estadístico de un período"""
        try:
            query = """
            SELECT 
                COUNT(*) as total_registros,
                COUNT(CASE WHEN energia_mwh > 0 THEN 1 END) as registros_completos,
                SUM(energia_mwh) as total_energia,
                AVG(energia_mwh) as promedio_energia,
                MIN(energia_mwh) as min_energia,
                MAX(energia_mwh) as max_energia,
                MAX(fecha_modificacion) as ultima_actualizacion
            FROM energia_barra 
            WHERE año = ? AND mes = ?
            """
            
            results = self.db_manager.execute_query(query, (año, mes))
            
            if results:
                row = results[0]
                
                # Obtener total de municipios para calcular completitud
                municipios = self.get_municipios()
                total_municipios = len(municipios)
                
                completitud = (row['registros_completos'] / total_municipios * 100) if total_municipios > 0 else 0
                
                return {
                    'año': año,
                    'mes': mes,
                    'total_municipios': total_municipios,
                    'total_registros': row['total_registros'],
                    'registros_completos': row['registros_completos'],
                    'completitud_porcentaje': completitud,
                    'total_energia': row['total_energia'] or 0,
                    'promedio_energia': row['promedio_energia'] or 0,
                    'min_energia': row['min_energia'] or 0,
                    'max_energia': row['max_energia'] or 0,
                    'ultima_actualizacion': row['ultima_actualizacion']
                }
            
            return {
                'año': año,
                'mes': mes,
                'total_municipios': len(self.get_municipios()),
                'total_registros': 0,
                'registros_completos': 0,
                'completitud_porcentaje': 0,
                'total_energia': 0,
                'promedio_energia': 0,
                'min_energia': 0,
                'max_energia': 0,
                'ultima_actualizacion': None
            }
            
        except Exception as e:
            self.logger.error(f"Error obteniendo resumen del período: {e}")
            return {
                'año': año,
                'mes': mes,
                'error': str(e)
            }

    def get_periodos_disponibles(self) -> List[Dict[str, Any]]:
        """Obtiene lista de períodos con datos disponibles"""
        try:
            query = """
            SELECT DISTINCT año, mes, COUNT(*) as registros
            FROM energia_barra 
            GROUP BY año, mes
            ORDER BY año DESC, mes DESC
            """
            
            results = self.db_manager.execute_query(query)
            
            periodos = []
            meses_nombres = ['', 'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                           'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
            
            for row in results:
                periodos.append({
                    'año': row['año'],
                    'mes': row['mes'],
                    'mes_nombre': meses_nombres[row['mes']],
                    'periodo_texto': f"{meses_nombres[row['mes']]} {row['año']}",
                    'registros': row['registros']
                })
            
            self.logger.info(f"Encontrados {len(periodos)} períodos con datos")
            return periodos
            
        except Exception as e:
            self.logger.error(f"Error obteniendo períodos disponibles: {e}")
            return []

    def validar_periodo_completo(self, año: int, mes: int) -> Dict[str, Any]:
        """Valida si un período tiene datos completos para todos los municipios"""
        try:
            municipios = self.get_municipios()
            registros = self.get_energia_by_periodo(año, mes)
            
            # Crear mapas para comparación
            municipios_sistema = {m['id']: m['nombre'] for m in municipios}
            municipios_con_datos = {r.municipio_id: r.municipio_nombre for r in registros}
            
            # Encontrar municipios faltantes
            municipios_faltantes = []
            for mun_id, mun_nombre in municipios_sistema.items():
                if mun_id not in municipios_con_datos:
                    municipios_faltantes.append({
                        'id': mun_id,
                        'nombre': mun_nombre
                    })
            
            # Validar calidad de datos
            registros_con_problemas = []
            for registro in registros:
                problemas = []
                
                if registro.energia_mwh <= 0:
                    problemas.append("Energía igual o menor a cero")
                
                if registro.energia_mwh > 500:  # Umbral alto para detectar posibles errores
                    problemas.append("Energía muy alta (>500 MWh)")
                
                if problemas:
                    registros_con_problemas.append({
                        'municipio': registro.municipio_nombre,
                        'energia': registro.energia_mwh,
                        'problemas': problemas
                    })
            
            # Calcular métricas
            total_municipios = len(municipios)
            municipios_con_datos_count = len(municipios_con_datos)
            completitud = (municipios_con_datos_count / total_municipios * 100) if total_municipios > 0 else 0
            
            es_completo = len(municipios_faltantes) == 0
            tiene_problemas = len(registros_con_problemas) > 0
            
            return {
                'año': año,
                'mes': mes,
                'es_completo': es_completo,
                'tiene_problemas': tiene_problemas,
                'total_municipios': total_municipios,
                'municipios_con_datos': municipios_con_datos_count,
                'completitud_porcentaje': completitud,
                'municipios_faltantes': municipios_faltantes,
                'registros_con_problemas': registros_con_problemas,
                'total_energia': sum(r.energia_mwh for r in registros),
                'promedio_energia': sum(r.energia_mwh for r in registros) / len(registros) if registros else 0
            }
            
        except Exception as e:
            self.logger.error(f"Error validando período completo: {e}")
            return {
                'año': año,
                'mes': mes,
                'error': str(e),
                'es_completo': False,
                'tiene_problemas': True
            }

    def importar_desde_excel(self, file_path: str, usuario_id: int, año: int = None, mes: int = None) -> Dict[str, Any]:
        """Importa datos de energía desde un archivo Excel"""
        try:
            import pandas as pd
            import os
            
            # Verificar que el archivo existe
            if not os.path.exists(file_path):
                return {"success": False, "message": "Archivo no encontrado", "imported": 0, "errors": 0}
            
            self.logger.info(f"Iniciando importación desde: {file_path}")
            
            # Leer el archivo Excel
            try:
                df = pd.read_excel(file_path)
                self.logger.info(f"Archivo leído: {len(df)} filas, columnas: {list(df.columns)}")
            except Exception as e:
                self.logger.error(f"Error leyendo Excel: {e}")
                return {"success": False, "message": f"Error leyendo Excel: {str(e)}", "imported": 0, "errors": 0}
            
            # Validar y normalizar columnas
            result = self._validate_excel_columns(df)
            if not result["success"]:
                return result
            
            df = result["dataframe"]
            
            # Procesar registros
            return self._process_excel_records(df, usuario_id, año, mes)
            
        except ImportError:
            return {"success": False, "message": "pandas no está instalado. Instale con: pip install pandas openpyxl", "imported": 0, "errors": 0}
        except Exception as e:
            self.logger.error(f"Error en importación Excel: {e}")
            return {"success": False, "message": f"Error del sistema: {str(e)}", "imported": 0, "errors": 0}

    def _validate_excel_columns(self, df: Any) -> Dict[str, Any]:
        """Valida y normaliza las columnas del Excel"""
        try:
            # Import local de pandas
            try:
                import pandas as pd
            except ImportError:
                return {"success": False, "message": "pandas no está instalado. Instale con: pip install pandas openpyxl"}
            
            # Mapeo de posibles nombres de columnas
            column_mapping = {
                'municipio': ['municipio', 'municipios', 'municipality', 'ciudad', 'localidad', 'nombre'],
                'año': ['año', 'year', 'anio', 'anos', 'ano'],
                'mes': ['mes', 'month', 'meses'],
                'energia': ['energia', 'energia_mwh', 'energy', 'mwh', 'megawatt', 'consumo', 'kwh'],
                'observaciones': ['observaciones', 'observacion', 'notas', 'comentarios', 'obs', 'observ']
            }
            
            # Normalizar nombres de columnas (minúsculas, sin espacios)
            df.columns = df.columns.str.lower().str.strip().str.replace(' ', '_').str.replace('.', '_')
            
            self.logger.info(f"Columnas normalizadas: {list(df.columns)}")
            
            # Encontrar columnas requeridas
            found_columns = {}
            for required_col, possible_names in column_mapping.items():
                found = None
                for col in df.columns:
                    if any(possible in col for possible in possible_names):
                        found = col
                        break
                
                if required_col in ['municipio', 'energia'] and found is None:
                    return {
                        "success": False, 
                        "message": f"Columna requerida no encontrada: {required_col}. Columnas disponibles: {list(df.columns)}"
                    }
                
                found_columns[required_col] = found
            
            self.logger.info(f"Columnas encontradas: {found_columns}")
            
            # Renombrar columnas
            rename_dict = {v: k for k, v in found_columns.items() if v is not None}
            df = df.rename(columns=rename_dict)
            
            # Validar que hay datos
            if df.empty:
                return {"success": False, "message": "El archivo está vacío"}
            
            # Eliminar filas completamente vacías
            df = df.dropna(how='all')
            
            if df.empty:
                return {"success": False, "message": "No hay datos válidos en el archivo"}
            
            return {"success": True, "dataframe": df}
            
        except Exception as e:
            self.logger.error(f"Error validando columnas: {e}")
            return {"success": False, "message": f"Error validando columnas: {str(e)}"}

    def _process_excel_records(self, df: Any, usuario_id: int, año: int = None, mes: int = None) -> Dict[str, Any]:
        """Procesa los registros del Excel"""
        try:
            # Import local de pandas
            try:
                import pandas as pd
            except ImportError:
                return {"success": False, "message": "pandas no está instalado"}
            
            imported_count = 0
            error_count = 0
            errors = []
            updated_count = 0
            
            # Obtener municipios para validación
            municipios = self.get_municipios()
            municipios_dict = {m['nombre'].lower(): m['id'] for m in municipios}
            municipios_dict.update({m['codigo'].lower(): m['id'] for m in municipios})
            
            self.logger.info(f"Procesando {len(df)} filas del Excel")
            
            for index, row in df.iterrows():
                try:
                    # Validar y obtener datos de la fila
                    record_data = self._extract_record_from_row(row, municipios_dict, año, mes, index)
                    
                    if record_data["success"]:
                        # Agregar usuario_id
                        record_data["data"]["usuario_id"] = usuario_id
                        
                        # Verificar si ya existe el registro
                        existing = self._get_energia_by_periodo(
                            record_data["data"]["municipio_id"],
                            record_data["data"]["año"],
                            record_data["data"]["mes"]
                        )
                        
                        if existing:
                            # Actualizar registro existente
                            if self._update_energia_record(existing["id"], record_data["data"]):
                                updated_count += 1
                                imported_count += 1
                            else:
                                error_count += 1
                                errors.append(f"Fila {index + 2}: Error actualizando registro existente")
                        else:
                            # Crear nuevo registro
                            if self.crear_energia(record_data["data"]):
                                imported_count += 1
                            else:
                                error_count += 1
                                errors.append(f"Fila {index + 2}: Error creando registro")
                    else:
                        error_count += 1
                        errors.append(f"Fila {index + 2}: {record_data['message']}")
                        
                except Exception as e:
                    error_count += 1
                    errors.append(f"Fila {index + 2}: Error procesando - {str(e)}")
                    self.logger.error(f"Error procesando fila {index + 2}: {e}")
            
            # Resultado final
            success = imported_count > 0
            message = f"Procesados: {imported_count} registros"
            
            if updated_count > 0:
                message += f" ({updated_count} actualizados, {imported_count - updated_count} nuevos)"
            
            if error_count > 0:
                message += f", {error_count} errores"
            
            if errors and len(errors) <= 5:  # Mostrar solo primeros 5 errores
                message += f". Errores: {'; '.join(errors[:5])}"
            elif len(errors) > 5:
                message += f". Primeros errores: {'; '.join(errors[:3])}... y {len(errors)-3} más"
            
            self.logger.info(f"Importación completada: {imported_count} importados, {error_count} errores")
            
            return {
                "success": success,
                "message": message,
                "imported": imported_count,
                "errors": error_count,
                "updated": updated_count,
                "error_details": errors
            }
            
        except Exception as e:
            self.logger.error(f"Error procesando registros: {e}")
            return {"success": False, "message": f"Error procesando datos: {str(e)}", "imported": 0, "errors": 0}

    def _extract_record_from_row(self, row: Any, municipios_dict: Dict[str, int], año_default: int = None, mes_default: int = None, row_index: int = 0) -> Dict[str, Any]:
        """Extrae y valida datos de una fila del Excel"""
        try:
            # Import local de pandas
            try:
                import pandas as pd
            except ImportError:
                return {"success": False, "message": "pandas no está instalado"}
            
            # Obtener municipio
            municipio_text = str(row.get('municipio', '')).strip()
            if not municipio_text or municipio_text.lower() in ['nan', 'none', '']:
                return {"success": False, "message": "Municipio vacío o inválido"}
            
            # Buscar ID del municipio
            municipio_id = None
            municipio_lower = municipio_text.lower()
            
            # Buscar por nombre exacto
            if municipio_lower in municipios_dict:
                municipio_id = municipios_dict[municipio_lower]
            else:
                # Buscar por coincidencia parcial
                for nombre, mid in municipios_dict.items():
                    if municipio_lower in nombre or nombre in municipio_lower:
                        municipio_id = mid
                        break
            
            if not municipio_id:
                return {"success": False, "message": f"Municipio no encontrado: {municipio_text}"}
            
            # Obtener año
            año = año_default
            if 'año' in row and pd.notna(row['año']):
                try:
                    año = int(float(row['año']))
                except (ValueError, TypeError):
                    return {"success": False, "message": f"Año inválido: {row.get('año')}"}
            
            if not año or año < 2020 or año > 2030:
                return {"success": False, "message": f"Año fuera de rango: {año}"}
            
            # Obtener mes
            mes = mes_default
            if 'mes' in row and pd.notna(row['mes']):
                try:
                    mes = int(float(row['mes']))
                except (ValueError, TypeError):
                    return {"success": False, "message": f"Mes inválido: {row.get('mes')}"}
            
            if not mes or mes < 1 or mes > 12:
                return {"success": False, "message": f"Mes fuera de rango: {mes}"}
            
            # Obtener energía
            if 'energia' not in row or pd.isna(row['energia']):
                return {"success": False, "message": "Energía vacía"}
            
            try:
                energia = float(row['energia'])
                if energia < 0:
                    return {"success": False, "message": f"Energía negativa: {energia}"}
            except (ValueError, TypeError):
                return {"success": False, "message": f"Energía inválida: {row.get('energia')}"}
            
            # Obtener observaciones
            observaciones = None
            if 'observaciones' in row and pd.notna(row['observaciones']):
                observaciones = str(row['observaciones']).strip()
                if observaciones.lower() in ['nan', 'none', '']:
                    observaciones = None
            
            return {
                "success": True,
                "data": {
                    "municipio_id": municipio_id,
                    "año": año,
                    "mes": mes,
                    "energia_mwh": energia,
                    "observaciones": observaciones
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error extrayendo datos de fila {row_index}: {e}")
            return {"success": False, "message": f"Error extrayendo datos: {str(e)}"}

    def _get_energia_by_periodo(self, municipio_id: int, año: int, mes: int) -> Optional[Dict[str, Any]]:
        """Busca un registro existente por municipio, año y mes"""
        try:
            query = """
            SELECT * FROM energia_barra 
            WHERE municipio_id = ? AND año = ? AND mes = ?
            """
            results = self.db_manager.execute_query(query, (municipio_id, año, mes))
            return results[0] if results else None
        except Exception as e:
            self.logger.error(f"Error buscando registro existente: {e}")
            return None

    def _update_energia_record(self, record_id: int, data: Dict[str, Any]) -> bool:
        """Actualiza un registro existente de energía"""
        try:
            query = """
            UPDATE energia_barra 
            SET energia_mwh = ?, observaciones = ?, fecha_modificacion = ?, usuario_id = ?
            WHERE id = ?
            """
            
            fecha_modificacion = datetime.now().isoformat()
            
            rows_affected = self.db_manager.execute_update(
                query, 
                (data["energia_mwh"], data.get("observaciones"), fecha_modificacion, data["usuario_id"], record_id)
            )
            
            return rows_affected > 0
            
        except Exception as e:
            self.logger.error(f"Error actualizando registro: {e}")
            return False

    def exportar_a_excel(self, año: int, mes: int, file_path: str) -> bool:
        """Exporta datos de energía a Excel"""
        try:
            # Import local de pandas
            try:
                import pandas as pd
            except ImportError:
                self.logger.error("pandas no está instalado. Instale con: pip install pandas openpyxl")
                return False
            
            # Obtener datos
            records = self.get_energia_by_periodo(año, mes)
            
            if not records:
                self.logger.warning(f"No hay datos para exportar: {año}-{mes:02d}")
                return False
            
            # Convertir a DataFrame
            data = []
            for record in records:
                data.append({
                    'Municipio': record.municipio_nombre,
                    'Código': record.municipio_codigo,
                    'Año': record.año,
                    'Mes': record.mes,
                    'Energía (MWh)': record.energia_mwh,
                    'Observaciones': record.observaciones or '',
                    'Fecha Registro': record.fecha_registro,
                    'Fecha Modificación': record.fecha_modificacion
                })
            
            df = pd.DataFrame(data)
            
            # Exportar a Excel
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name=f'Energía {año}-{mes:02d}', index=False)
                
                # Formatear hoja
                worksheet = writer.sheets[f'Energía {año}-{mes:02d}']
                
                # Ajustar ancho de columnas
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    adjusted_width = min(max_length + 2, 50)
                    worksheet.column_dimensions[column_letter].width = adjusted_width
            
            self.logger.info(f"Datos exportados a: {file_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error exportando a Excel: {e}")
            return False

    def validar_datos_periodo(self, año: int, mes: int) -> Dict[str, Any]:
        """Valida la consistencia de datos de un período"""
        try:
            records = self.get_energia_by_periodo(año, mes)
            municipios = self.get_municipios()
            
            # Estadísticas de validación
            total_municipios = len(municipios)
            registros_existentes = len(records)
            municipios_faltantes = []
            registros_con_errores = []
            
            # Buscar municipios sin datos
            municipios_con_datos = {r.municipio_id for r in records}
            for municipio in municipios:
                if municipio['id'] not in municipios_con_datos:
                    municipios_faltantes.append(municipio['nombre'])
            
            # Validar registros existentes
            for record in records:
                errores = []
                
                if record.energia_mwh <= 0:
                    errores.append("Energía debe ser mayor a 0")
                
                if record.energia_mwh > 1000:  # Valor muy alto, posible error
                    errores.append("Energía muy alta (>1000 MWh)")
                
                if errores:
                    registros_con_errores.append({
                        'municipio': record.municipio_nombre,
                        'energia': record.energia_mwh,
                        'errores': errores
                    })
            
            # Calcular porcentaje de completitud
            completitud = (registros_existentes / total_municipios) * 100 if total_municipios > 0 else 0
            
            return {
                'total_municipios': total_municipios,
                'registros_existentes': registros_existentes,
                'municipios_faltantes': municipios_faltantes,
                'registros_con_errores': registros_con_errores,
                'completitud_porcentaje': completitud,
                'es_valido': len(municipios_faltantes) == 0 and len(registros_con_errores) == 0
            }
            
        except Exception as e:
            self.logger.error(f"Error validando datos: {e}")
            return {
                'total_municipios': 0,
                'registros_existentes': 0,
                'municipios_faltantes': [],
                'registros_con_errores': [],
                'completitud_porcentaje': 0,
                'es_valido': False,
                'error': str(e)
            }

    def get_estadisticas_anuales(self, año: int) -> Dict[str, Any]:
        """Obtiene estadísticas anuales de energía"""
        try:
            query = """
            SELECT 
                mes,
                COUNT(*) as registros,
                SUM(energia_mwh) as total_energia,
                AVG(energia_mwh) as promedio_energia,
                MIN(energia_mwh) as min_energia,
                MAX(energia_mwh) as max_energia
            FROM energia_barra 
            WHERE año = ?
            GROUP BY mes
            ORDER BY mes
            """
            
            results = self.db_manager.execute_query(query, (año,))
            
            # Procesar resultados
            estadisticas_mensuales = {}
            total_anual = 0
            
            for row in results:
                mes = row['mes']
                estadisticas_mensuales[mes] = {
                    'registros': row['registros'],
                    'total_energia': row['total_energia'],
                    'promedio_energia': row['promedio_energia'],
                    'min_energia': row['min_energia'],
                    'max_energia': row['max_energia']
                }
                total_anual += row['total_energia']
            
            # Calcular estadísticas generales
            meses_con_datos = len(estadisticas_mensuales)
            promedio_mensual = total_anual / meses_con_datos if meses_con_datos > 0 else 0
            
            return {
                'año': año,
                'estadisticas_mensuales': estadisticas_mensuales,
                'total_anual': total_anual,
                'promedio_mensual': promedio_mensual,
                'meses_con_datos': meses_con_datos,
                'completitud_anual': (meses_con_datos / 12) * 100
            }
            
        except Exception as e:
            self.logger.error(f"Error obteniendo estadísticas anuales: {e}")
            return {
                'año': año,
                'estadisticas_mensuales': {},
                'total_anual': 0,
                'promedio_mensual': 0,
                'meses_con_datos': 0,
                'completitud_anual': 0,
                'error': str(e)
            }

    def buscar_registros(self, filtros: Dict[str, Any]) -> List[EnergiaRecord]:
        """Busca registros con filtros específicos"""
        try:
            conditions = []
            params = []
            
            # Construir condiciones WHERE
            if filtros.get('municipio_id'):
                conditions.append("eb.municipio_id = ?")
                params.append(filtros['municipio_id'])
            
            if filtros.get('año'):
                conditions.append("eb.año = ?")
                params.append(filtros['año'])
            
            if filtros.get('mes'):
                conditions.append("eb.mes = ?")
                params.append(filtros['mes'])
            
            if filtros.get('energia_min'):
                conditions.append("eb.energia_mwh >= ?")
                params.append(filtros['energia_min'])
            
            if filtros.get('energia_max'):
                conditions.append("eb.energia_mwh <= ?")
                params.append(filtros['energia_max'])
            
            if filtros.get('municipio_nombre'):
                conditions.append("LOWER(m.nombre) LIKE ?")
                params.append(f"%{filtros['municipio_nombre'].lower()}%")
            
            # Construir query
            base_query = """
            SELECT eb.*, m.nombre as municipio_nombre, m.codigo as municipio_codigo
            FROM energia_barra eb
            JOIN municipios m ON eb.municipio_id = m.id
            """
            
            if conditions:
                query = base_query + " WHERE " + " AND ".join(conditions)
            else:
                query = base_query
            
            query += " ORDER BY eb.año DESC, eb.mes DESC, m.nombre"
            
            # Aplicar límite si se especifica
            if filtros.get('limite'):
                query += f" LIMIT {filtros['limite']}"
            
            results = self.db_manager.execute_query(query, tuple(params))
            
            # Convertir a objetos EnergiaRecord
            records = []
            for row in results:
                record = EnergiaRecord(
                    id=row['id'],
                    municipio_id=row['municipio_id'],
                    municipio_nombre=row['municipio_nombre'],
                    municipio_codigo=row['municipio_codigo'],
                    año=row['año'],
                    mes=row['mes'],
                    energia_mwh=row['energia_mwh'],
                    observaciones=row.get('observaciones'),
                    fecha_registro=row['fecha_registro'],
                    fecha_modificacion=row.get('fecha_modificacion', row['fecha_registro']),
                    usuario_id=row['usuario_id']
                )
                records.append(record)
            
            self.logger.info(f"Búsqueda completada: {len(records)} registros encontrados")
            return records
            
        except Exception as e:
            self.logger.error(f"Error en búsqueda: {e}")
            return []

    def duplicar_periodo(self, año_origen: int, mes_origen: int, año_destino: int, mes_destino: int, usuario_id: int) -> Dict[str, Any]:
        """Duplica registros de un período a otro"""
        try:
            # Obtener registros del período origen
            registros_origen = self.get_energia_by_periodo(año_origen, mes_origen)
            
            if not registros_origen:
                return {
                    "success": False,
                    "message": f"No hay datos en el período origen {año_origen}-{mes_origen:02d}",
                    "duplicados": 0
                }
            
            # Verificar si ya existen datos en el período destino
            registros_destino = self.get_energia_by_periodo(año_destino, mes_destino)
            if registros_destino:
                return {
                    "success": False,
                    "message": f"Ya existen datos en el período destino {año_destino}-{mes_destino:02d}",
                    "duplicados": 0
                }
            
            # Duplicar registros
            duplicados = 0
            errores = 0
            
            for record in registros_origen:
                data = {
                    "municipio_id": record.municipio_id,
                    "año": año_destino,
                    "mes": mes_destino,
                    "energia_mwh": record.energia_mwh,
                    "observaciones": f"Duplicado de {año_origen}-{mes_origen:02d}",
                    "usuario_id": usuario_id
                }
                
                if self.crear_energia(data):
                    duplicados += 1
                else:
                    errores += 1
            
            success = duplicados > 0
            message = f"Duplicados {duplicados} registros"
            if errores > 0:
                message += f", {errores} errores"
            
            self.logger.info(f"Duplicación completada: {duplicados} registros duplicados")
            
            return {
                "success": success,
                "message": message,
                "duplicados": duplicados,
                "errores": errores
            }
            
        except Exception as e:
            self.logger.error(f"Error duplicando período: {e}")
            return {
                "success": False,
                "message": f"Error del sistema: {str(e)}",
                "duplicados": 0
            }

    def generar_plantilla_excel(self, file_path: str, año: int = None, mes: int = None) -> bool:
        """Genera una plantilla Excel para importación"""
        try:
            # Import local de pandas
            try:
                import pandas as pd
            except ImportError:
                self.logger.error("pandas no está instalado. Instale con: pip install pandas openpyxl")
                return False
            
            # Obtener municipios
            municipios = self.get_municipios()
            
            # Crear datos de ejemplo
            data = []
            año_ejemplo = año or 2024
            mes_ejemplo = mes or 1
            
            for municipio in municipios:
                data.append({
                    'Municipio': municipio['nombre'],
                    'Año': año_ejemplo,
                    'Mes': mes_ejemplo,
                    'Energía': 0.0,  # Valor por defecto
                    'Observaciones': ''
                })
            
            df = pd.DataFrame(data)
            
            # Crear archivo Excel con formato
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Plantilla Energía', index=False)
                
                # Formatear hoja
                worksheet = writer.sheets['Plantilla Energía']
                
                # Ajustar ancho de columnas
                column_widths = {
                    'A': 20,  # Municipio
                    'B': 10,  # Año
                    'C': 10,  # Mes
                    'D': 15,  # Energía
                    'E': 30   # Observaciones
                }
                
                for col, width in column_widths.items():
                    worksheet.column_dimensions[col].width = width
                
                # Agregar hoja de instrucciones
                instrucciones = [
                    ['INSTRUCCIONES PARA IMPORTACIÓN DE DATOS DE ENERGÍA'],
                    [''],
                    ['1. Complete la columna "Energía" con los valores en MWh'],
                    ['2. La columna "Observaciones" es opcional'],
                    ['3. NO modifique las columnas Municipio, Año y Mes'],
                    ['4. Guarde el archivo y use la función "Importar Excel"'],
                    [''],
                    ['FORMATO REQUERIDO:'],
                    ['- Municipio: Nombre completo del municipio'],
                    ['- Año: Año en formato YYYY (ej: 2024)'],
                    ['- Mes: Número del mes (1-12)'],
                    ['- Energía: Valor numérico en MWh'],
                    ['- Observaciones: Texto libre (opcional)'],
                    [''],
                    ['MUNICIPIOS VÁLIDOS:'] + [m['nombre'] for m in municipios]
                ]
                
                df_instrucciones = pd.DataFrame(instrucciones)
                df_instrucciones.to_excel(writer, sheet_name='Instrucciones', index=False, header=False)
            
            self.logger.info(f"Plantilla Excel generada: {file_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error generando plantilla: {e}")
            return False

    def get_historial_cambios(self, municipio_id: int = None, limite: int = 50) -> List[Dict[str, Any]]:
        """Obtiene el historial de cambios en los registros"""
        try:
            # Esta función requeriría una tabla de auditoría
            # Por ahora, retornamos los registros más recientes ordenados por fecha de modificación
            
            base_query = """
            SELECT eb.*, m.nombre as municipio_nombre, m.codigo as municipio_codigo,
                   u.nombre_completo as usuario_nombre
            FROM energia_barra eb
            JOIN municipios m ON eb.municipio_id = m.id
            LEFT JOIN usuarios u ON eb.usuario_id = u.id
            """
            
            params = []
            if municipio_id:
                base_query += " WHERE eb.municipio_id = ?"
                params.append(municipio_id)
            
            query = base_query + " ORDER BY eb.fecha_modificacion DESC"
            
            if limite:
                query += f" LIMIT {limite}"
            
            results = self.db_manager.execute_query(query, tuple(params))
            
            historial = []
            for row in results:
                historial.append({
                    'id': row['id'],
                    'municipio_nombre': row['municipio_nombre'],
                    'año': row['año'],
                    'mes': row['mes'],
                    'energia_mwh': row['energia_mwh'],
                    'fecha_modificacion': row.get('fecha_modificacion', row['fecha_registro']),
                    'usuario_nombre': row.get('usuario_nombre', 'Sistema'),
                    'accion': 'Modificación'  # En una implementación completa, esto vendría de la tabla de auditoría
                })
            
            return historial
            
        except Exception as e:
            self.logger.error(f"Error obteniendo historial: {e}")
            return []

    def calcular_tendencias(self, municipio_id: int, meses: int = 12) -> Dict[str, Any]:
        """Calcula tendencias de consumo para un municipio"""
        try:
            query = """
            SELECT año, mes, energia_mwh, fecha_registro
            FROM energia_barra 
            WHERE municipio_id = ?
            ORDER BY año DESC, mes DESC
            LIMIT ?
            """
            
            results = self.db_manager.execute_query(query, (municipio_id, meses))
            
            if len(results) < 2:
                return {
                    'municipio_id': municipio_id,
                    'datos_insuficientes': True,
                    'mensaje': 'Se requieren al menos 2 registros para calcular tendencias'
                }
            
            # Calcular estadísticas básicas
            valores = [r['energia_mwh'] for r in results]
            promedio = sum(valores) / len(valores)
            maximo = max(valores)
            minimo = min(valores)
            
            # Calcular tendencia simple (comparar últimos 3 con anteriores)
            if len(valores) >= 6:
                ultimos_3 = sum(valores[:3]) / 3
                anteriores_3 = sum(valores[3:6]) / 3
                tendencia = 'creciente' if ultimos_3 > anteriores_3 else 'decreciente'
                variacion_porcentual = ((ultimos_3 - anteriores_3) / anteriores_3) * 100
            else:
                tendencia = 'estable'
                variacion_porcentual = 0
            
            return {
                'municipio_id': municipio_id,
                'registros_analizados': len(results),
                'promedio': promedio,
                'maximo': maximo,
                'minimo': minimo,
                'tendencia': tendencia,
                'variacion_porcentual': variacion_porcentual,
                'datos_historicos': results
            }
            
        except Exception as e:
            self.logger.error(f"Error calculando tendencias: {e}")
            return {
                'municipio_id': municipio_id,
                'error': str(e)
            }

    def get_energia_list(self, año: int = None, mes: int = None, municipio_id: int = None) -> List[Dict[str, Any]]:
        """Obtiene lista de registros de energía con filtros"""
        try:
            # Base query
            query = """
            SELECT eb.*, m.nombre as municipio_nombre, m.codigo as municipio_codigo
            FROM energia_barra eb
            JOIN municipios m ON eb.municipio_id = m.id
            WHERE 1=1
            """
            params = []
            
            # Add filters
            if año:
                query += " AND eb.año = ?"
                params.append(año)
            
            if mes:
                query += " AND eb.mes = ?"
                params.append(mes)
                
            if municipio_id:
                query += " AND eb.municipio_id = ?"
                params.append(municipio_id)
            
            query += " ORDER BY eb.año DESC, eb.mes DESC, m.nombre ASC"
            
            result = self.db_manager.execute_query(query, tuple(params))
            self.logger.info(f"Obtenidos {len(result)} registros de energía")
            return result
            
        except Exception as e:
            self.logger.error(f"Error obteniendo lista de energía: {e}")
            return []
