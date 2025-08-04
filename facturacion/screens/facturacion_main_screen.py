"""
Pantalla principal del módulo de facturación
"""

import flet as ft
from datetime import datetime
from typing import List, Dict, Any
import pandas as pd
import time
from facturacion.services import get_facturacion_service
from facturacion.models import FacturacionModel
from core.logger import get_logger

class FacturacionMainScreen:
    """Pantalla principal de facturación"""
    
    def __init__(self, app):
        self.app = app
        self.page = app.page
        self.logger = get_logger(__name__)
        self.facturacion_service = get_facturacion_service()
        
        # Inicializar variables
        self.facturaciones = []
        self.municipios = []  # Inicializar lista vacía
        
        # Fechas actuales
        now = datetime.now()
        self.current_año = now.year
        self.current_mes = now.month
        
        # Cargar municipios al inicializar
        self._load_municipios()
    def _load_municipios(self):
        """Carga la lista de municipios"""
        try:
            self.municipios = self.facturacion_service.get_municipios_activos()
            self.logger.info(f"Municipios cargados: {len(self.municipios)}")
        except Exception as e:
            self.logger.error(f"Error al cargar municipios: {e}")
            self.municipios = []       
    def build(self) -> ft.Control:
        """Construye la interfaz"""
        return ft.Container(
            content=ft.Column([
                self._build_header(),
                ft.Container(height=15),
                self._build_filters(),
                ft.Container(height=20),
                self._build_data_table(),
                ft.Container(height=15),
                self._build_actions()
            ], spacing=0),
            padding=25,
            expand=True,
            bgcolor=ft.Colors.GREY_50
        )
    
    def _build_header(self) -> ft.Control:
        """Construye el header de la pantalla"""
        return ft.Container(
            content=ft.Row([
                ft.Row([
                    ft.Container(
                        content=ft.Icon(ft.Icons.RECEIPT_LONG, size=35, color=ft.Colors.WHITE),
                        width=50,
                        height=50,
                        bgcolor=ft.Colors.GREEN,
                        border_radius=25,
                        alignment=ft.alignment.center
                    ),
                    ft.Container(width=15),
                    ft.Column([
                        ft.Text("Gestión de Facturación", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_800),
                        ft.Text("Administración de datos de facturación eléctrica", size=15, color=ft.Colors.GREY_600)
                    ], spacing=2)
                ], expand=True),
                ft.Row([
                    ft.Container(
                        content=ft.IconButton(
                            ft.Icons.REFRESH,
                            tooltip="Actualizar datos",
                            on_click=self._load_data,
                            icon_color=ft.Colors.WHITE,
                            bgcolor=ft.Colors.BLUE,
                            style=ft.ButtonStyle(shape=ft.CircleBorder())
                        ),
                        margin=ft.margin.only(right=8)
                    ),
                    ft.Container(
                        content=ft.IconButton(
                            ft.Icons.ARROW_BACK,
                            tooltip="Volver al dashboard",
                            on_click=lambda _: self.app.navigate_to("dashboard"),
                            icon_color=ft.Colors.WHITE,
                            bgcolor=ft.Colors.GREY_600,
                            style=ft.ButtonStyle(shape=ft.CircleBorder())
                        )
                    )
                ])
            ]),
            bgcolor=ft.Colors.WHITE,
            padding=25,
            border_radius=15,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=10,
                color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                offset=ft.Offset(0, 2)
            )
        )

    def _build_filters(self) -> ft.Control:
        """Construye los filtros de búsqueda"""
        # Los municipios ya están cargados en __init__
        
        self.municipio_dropdown = ft.Dropdown(
            label="Seleccionar Municipio",
            width=220,
            bgcolor=ft.Colors.WHITE,
            border_color=ft.Colors.BLUE_200,
            focused_border_color=ft.Colors.BLUE,
            options=[ft.dropdown.Option("", "Todos los municipios")] + [
                ft.dropdown.Option(str(m['id']), m['nombre']) 
                for m in self.municipios
            ]
        )
        
        self.año_field = ft.TextField(
            label="Año",
            value=str(self.current_año),
            width=120,
            keyboard_type=ft.KeyboardType.NUMBER,
            bgcolor=ft.Colors.WHITE,
            border_color=ft.Colors.BLUE_200,
            focused_border_color=ft.Colors.BLUE
        )
        
        self.mes_dropdown = ft.Dropdown(
            label="Mes",
            width=180,
            value="",
            bgcolor=ft.Colors.WHITE,
            border_color=ft.Colors.BLUE_200,
            focused_border_color=ft.Colors.BLUE,
            options=[ft.dropdown.Option("", "Todos los meses")] + [
                ft.dropdown.Option("1", "Enero"),
                ft.dropdown.Option("2", "Febrero"),
                ft.dropdown.Option("3", "Marzo"),
                ft.dropdown.Option("4", "Abril"),
                ft.dropdown.Option("5", "Mayo"),
                ft.dropdown.Option("6", "Junio"),
                ft.dropdown.Option("7", "Julio"),
                ft.dropdown.Option("8", "Agosto"),
                ft.dropdown.Option("9", "Septiembre"),
                ft.dropdown.Option("10", "Octubre"),
                ft.dropdown.Option("11", "Noviembre"),
                ft.dropdown.Option("12", "Diciembre"),
            ]
        )
        
        # Botones de acción
        self.load_button = ft.ElevatedButton(
            "Cargar Datos",
            icon=ft.Icons.SEARCH,
            on_click=self._load_data,
            bgcolor=ft.Colors.BLUE,
            color=ft.Colors.WHITE,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8),
                elevation=2
            ),
            height=45
        )
        
        self.clear_button = ft.ElevatedButton(
            "Limpiar",
            icon=ft.Icons.CLEAR_ALL,
            on_click=self._clear_filters,
            bgcolor=ft.Colors.ORANGE,
            color=ft.Colors.WHITE,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8),
                elevation=2
            ),
            height=45
        )
        
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.FILTER_LIST, size=20, color=ft.Colors.BLUE),
                    ft.Container(width=8),
                    ft.Text("Filtros de Búsqueda", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_800)
                ]),
                ft.Container(height=15),
                ft.Row([
                    self.municipio_dropdown,
                    ft.Container(width=15),
                    self.año_field,
                    ft.Container(width=15),
                    self.mes_dropdown,
                ], wrap=True, spacing=0),
                ft.Container(height=15),
                ft.Row([
                    self.load_button,
                    ft.Container(width=10),
                    self.clear_button,
                ], spacing=0)
            ], spacing=0),
            bgcolor=ft.Colors.WHITE,
            padding=20,
            border_radius=12,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=8,
                color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK),
                offset=ft.Offset(0, 2)
            )
        )
    
    def _build_data_table(self) -> ft.Control:
        """Construye la tabla de datos"""
        
        # Crear tabla de datos
        self.data_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID", weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_700)),
                ft.DataColumn(ft.Text("Municipio", weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_700)),
                ft.DataColumn(ft.Text("Año", weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_700)),
                ft.DataColumn(ft.Text("Mes", weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_700)),
                ft.DataColumn(ft.Text("Facturación Menor", weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_700)),
                ft.DataColumn(ft.Text("Facturación Mayor", weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_700)),
                ft.DataColumn(ft.Text("Total", weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_700)),
                ft.DataColumn(ft.Text("Acciones", weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_700))
            ],
            rows=[],
            bgcolor=ft.Colors.WHITE,
            border=ft.border.all(1, ft.Colors.GREY_200),
            border_radius=8,
            divider_thickness=1,
            heading_row_color=ft.Colors.GREY_100,
            heading_row_height=50
        )
        
        # Cargar datos iniciales
        self._update_data_table()
        
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.TABLE_CHART, size=22, color=ft.Colors.GREEN),
                    ft.Container(width=8),
                    ft.Text("Datos de Facturación", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_800)
                ]),
                ft.Container(height=15),
                ft.Container(
                    content=ft.Column([
                        self.data_table
                    ], scroll=ft.ScrollMode.AUTO),
                    bgcolor=ft.Colors.WHITE,
                    border_radius=10,
                    padding=15,
                    shadow=ft.BoxShadow(
                        spread_radius=1,
                        blur_radius=8,
                        color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK),
                        offset=ft.Offset(0, 2)
                    )
                )
            ]),
            expand=True
        )
   
    def _build_actions(self) -> ft.Control:
        """Construye las acciones"""
        return ft.Container(
            content=ft.Row([
                ft.ElevatedButton(
                    "Gestionar Transferencias",
                    icon=ft.Icons.SWAP_HORIZ,
                    on_click=self._manage_clients,
                    bgcolor=ft.Colors.PURPLE,
                    color=ft.Colors.WHITE,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=10),
                        elevation=3
                    ),
                    height=50
                ),
                ft.Container(width=15),
                ft.ElevatedButton(
                    "Transferencias",
                    icon=ft.Icons.SWAP_HORIZ,
                    on_click=self._manage_transfers,
                    bgcolor=ft.Colors.INDIGO,
                    color=ft.Colors.WHITE,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=10),
                        elevation=3
                    ),
                    height=50
                ),
                ft.Container(expand=True),
                ft.ElevatedButton(
                    "Cargar desde Excel",
                    icon=ft.Icons.UPLOAD_FILE,
                    on_click=self._import_from_excel,
                    bgcolor=ft.Colors.GREEN_600,
                    color=ft.Colors.WHITE,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=10),
                        elevation=3
                    ),
                    height=50
                )
            ], spacing=0),
            padding=ft.padding.only(top=10)
        )
    
    def _on_filter_change(self, e):
        """Maneja cambios en los filtros"""
        pass  # Se actualiza cuando se presiona buscar
    
    def _load_data(self, e=None):
        """Carga los datos de facturación según los filtros"""
        try:
            # Mostrar indicador de carga
            self.load_button.text = "Cargando..."
            self.load_button.disabled = True
            self.page.update()
            
            # Obtener valores de filtros - CORREGIDO
            municipio_id = None
            if self.municipio_dropdown.value and self.municipio_dropdown.value != "":
                try:
                    municipio_id = int(self.municipio_dropdown.value)
                except ValueError:
                    municipio_id = None
            
            año = None
            if self.año_field.value and self.año_field.value.strip():
                try:
                    año = int(self.año_field.value)
                except ValueError:
                    año = None
            
            mes = None
            if self.mes_dropdown.value and self.mes_dropdown.value != "":
                try:
                    mes = int(self.mes_dropdown.value)
                except ValueError:
                    mes = None
            
            # Cargar datos según los filtros disponibles
            if municipio_id and año and mes:
                # Filtro específico por municipio, año y mes
                self.facturaciones = self.facturacion_service.get_facturacion_by_municipio(municipio_id, año, mes)
            elif municipio_id:
                # Solo por municipio (todos los períodos)
                self.facturaciones = self.facturacion_service.get_facturacion_by_municipio(municipio_id)
            elif año and mes:
                # Por período (todos los municipios)
                self.facturaciones = self.facturacion_service.get_facturacion_by_periodo(año, mes)
            else:
                # Sin filtros específicos, usar período actual
                current_year = datetime.now().year
                current_month = datetime.now().month
                self.facturaciones = self.facturacion_service.get_facturacion_by_periodo(current_year, current_month)
            
            # Actualizar tabla
            self._update_data_table()
            
            # Mostrar mensaje de éxito
            self._show_success(f"Se cargaron {len(self.facturaciones)} registros")
            
            self.logger.info(f"Datos cargados: {len(self.facturaciones)} registros")
            
        except Exception as ex:
            self.logger.error(f"Error al cargar datos: {ex}")
            self._show_error("Error al cargar los datos de facturación")
        
        finally:
            # Restaurar botón
            self.load_button.text = "Cargar Datos"
            self.load_button.disabled = False
            self.page.update()

    def _update_data_table(self):
        """Actualiza la tabla de datos"""
        self.data_table.rows.clear()
        
        for facturacion in self.facturaciones:
            self.data_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(facturacion.id), color=ft.Colors.GREY_700)),
                        ft.DataCell(ft.Text(facturacion.municipio_nombre or "N/A", color=ft.Colors.GREY_800)),
                        ft.DataCell(ft.Text(str(facturacion.año), color=ft.Colors.GREY_700)),
                        ft.DataCell(ft.Text(str(facturacion.mes), color=ft.Colors.GREY_700)),
                        ft.DataCell(ft.Text(f"{facturacion.facturacion_menor:,.2f}", color=ft.Colors.GREEN_700, weight=ft.FontWeight.W_500)),
                        ft.DataCell(ft.Text(f"{facturacion.facturacion_mayor:,.2f}", color=ft.Colors.BLUE_700, weight=ft.FontWeight.W_500)),
                        ft.DataCell(ft.Text(f"{facturacion.facturacion_total:,.2f}", color=ft.Colors.PURPLE_700, weight=ft.FontWeight.BOLD)),
                        ft.DataCell(
                            ft.Row([
                                ft.IconButton(
                                    icon=ft.Icons.EDIT,
                                    tooltip="Editar facturación",
                                    on_click=lambda e, f=facturacion: self._edit_facturacion(f),
                                    icon_color=ft.Colors.BLUE,
                                    bgcolor=ft.Colors.BLUE_50,
                                    style=ft.ButtonStyle(shape=ft.CircleBorder())
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.DELETE,
                                    tooltip="Eliminar facturación",
                                    on_click=lambda e, f=facturacion: self._delete_facturacion(f),
                                    icon_color=ft.Colors.RED,
                                    bgcolor=ft.Colors.RED_50,
                                    style=ft.ButtonStyle(shape=ft.CircleBorder())
                                )
                            ], spacing=5)
                        )
                    ]
                )
            )

    def _refresh_data(self, e):
        """Actualiza los datos"""
        self._load_data()

    def _edit_facturacion(self, facturacion: FacturacionModel):
        """Edita una facturación"""
        self.app.navigate_to("facturacion_edit", facturacion=facturacion)

    def _delete_facturacion(self, facturacion: FacturacionModel):
        """Elimina una facturación"""
        def confirm_delete(e):
            if self.facturacion_service.delete_facturacion(facturacion.id):
                self._show_success("Facturación eliminada correctamente")
                self._load_data()
            else:
                self._show_error("Error al eliminar la facturación")
            dialog.open = False
            self.page.update()
        
        def cancel_delete(e):
            dialog.open = False
            self.page.update()
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmar eliminación", weight=ft.FontWeight.BOLD),
            content=ft.Text(f"¿Está seguro de eliminar la facturación de {facturacion.municipio_nombre}?"),
            actions=[
                ft.TextButton("Cancelar", on_click=cancel_delete),
                ft.ElevatedButton(
                    "Eliminar", 
                    on_click=confirm_delete,
                    bgcolor=ft.Colors.RED,
                    color=ft.Colors.WHITE
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()

    def _manage_clients(self, e):
        """Gestiona transferencias (antes clientes)"""
        self.app.navigate_to("facturacion_transfers")

    def _manage_transfers(self, e):
        """Gestiona transferencias"""
        self.app.navigate_to("facturacion_transfers")

    def _load_from_excel(self, e):
        """Carga datos desde Excel (por implementar)"""
        self._show_info("Funcionalidad de carga desde Excel en desarrollo")

    def _show_success(self, message: str):
        """Muestra mensaje de éxito"""
        snack_bar = ft.SnackBar(
            content=ft.Text(message, color=ft.Colors.WHITE),
            bgcolor=ft.Colors.GREEN,
            action="OK",
            action_color=ft.Colors.WHITE
        )
        self.page.snack_bar = snack_bar
        snack_bar.open = True
        self.page.update()

    def _show_error(self, message: str):
        """Muestra mensaje de error"""
        snack_bar = ft.SnackBar(
            content=ft.Text(message, color=ft.Colors.WHITE),
            bgcolor=ft.Colors.RED,
            action="OK",
            action_color=ft.Colors.WHITE
        )
        self.page.snack_bar = snack_bar
        snack_bar.open = True
        self.page.update()

    def _show_info(self, message: str):
        """Muestra mensaje informativo"""
        self.page.show_snack_bar(
            ft.SnackBar(
                content=ft.Text(message, color=ft.Colors.WHITE), 
                bgcolor=ft.Colors.BLUE,
                action="OK",
                action_color=ft.Colors.WHITE
            )
        )

    def on_mount(self):
        """Se ejecuta cuando se monta la pantalla"""
        self._load_data()

    def _import_from_excel(self, e):
        """Importa datos desde un archivo Excel con hojas por municipio"""
        def on_file_selected(e: ft.FilePickerResultEvent):
            if e.files:
                file_path = e.files[0].path
                self._process_municipal_excel_file(file_path)
        
        # Crear file picker
        file_picker = ft.FilePicker(on_result=on_file_selected)
        self.page.overlay.append(file_picker)
        self.page.update()
        
        # Abrir diálogo de selección de archivo
        file_picker.pick_files(
            dialog_title="Seleccionar archivo Excel de Facturación",
            file_type=ft.FilePickerFileType.CUSTOM,
            allowed_extensions=["xlsx", "xls"]
        )

    def _process_municipal_excel_file(self, file_path: str):
        """Procesa el archivo Excel con hojas por municipio"""
        try:
            # Debug del archivo
            self._debug_excel_processing(file_path)
            
            # Verificar que tenemos municipios cargados
            if not self.municipios:
                self._show_error("No se pudieron cargar los municipios de la base de datos")
                return
            
            # Obtener período para importación
            año, mes = self._get_import_period()
            if not año or not mes:
                self._show_info("Importación cancelada")
                return
            
            # Mostrar diálogo de progreso
            progress_dialog = self._show_progress_dialog("Procesando archivo Excel...")
            
            # Procesar archivo Excel
            success_count = 0
            error_count = 0
            errors = []
            processed_municipios = []
            
            try:
                excel_file = pd.ExcelFile(file_path)
                sheet_names = excel_file.sheet_names
                
                self.logger.info(f"Procesando {len(sheet_names)} hojas del Excel")
                
                for sheet_name in sheet_names:
                    try:
                        # Buscar municipio correspondiente
                        municipio = self._find_municipio_by_name(sheet_name)
                        
                        if not municipio:
                            error_msg = f"Municipio '{sheet_name}' no encontrado en la base de datos"
                            errors.append(error_msg)
                            error_count += 1
                            continue
                        
                        # Leer datos de la hoja
                        df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)
                        
                        # Verificar que la hoja tenga el tamaño esperado
                        if len(df) < 41 or len(df.columns) < 3:
                            error_msg = f"Hoja '{sheet_name}' no tiene el formato esperado"
                            errors.append(error_msg)
                            error_count += 1
                            continue
                        
                        # Extraer valores de las celdas específicas
                        facturacion_menor = self._extract_numeric_value(df.iloc[37, 2])  # C38
                        facturacion_mayor = self._extract_numeric_value(df.iloc[40, 2])  # C41
                        
                        if facturacion_menor is None or facturacion_mayor is None:
                            error_msg = f"Valores inválidos en '{sheet_name}' - Menor: {df.iloc[37, 2]}, Mayor: {df.iloc[40, 2]}"
                            errors.append(error_msg)
                            error_count += 1
                            continue
                        
                        # Calcular total
                        facturacion_total = facturacion_menor + facturacion_mayor
                        
                        # Verificar si ya existe registro para este municipio y período
                        existing = self.facturacion_service.get_facturacion_by_municipio_periodo(
                            municipio['id'], año, mes
                        )
                        
                        if existing:
                            # Actualizar registro existente
                            existing.facturacion_menor = facturacion_menor
                            existing.facturacion_mayor = facturacion_mayor
                            existing.facturacion_total = facturacion_total
                            
                            if self.facturacion_service.update_facturacion(existing):
                                success_count += 1
                                processed_municipios.append(f"{municipio['nombre']} (actualizado)")
                                self.logger.info(f"Actualizado: {municipio['nombre']}")
                            else:
                                error_msg = f"Error al actualizar '{municipio['nombre']}'"
                                errors.append(error_msg)
                                error_count += 1
                        else:
                            # Crear nuevo registro
                            from facturacion.models.facturacion_model import FacturacionModel
                            
                            nueva_facturacion = FacturacionModel(
                                municipio_id=municipio['id'],
                                año=año,
                                mes=mes,
                                facturacion_menor=facturacion_menor,
                                facturacion_mayor=facturacion_mayor,
                                facturacion_total=facturacion_total,
                                usuario_id=self.app.get_current_user().get('id', 1)
                            )
                            
                            if self.facturacion_service.save_facturacion(nueva_facturacion):
                                success_count += 1
                                processed_municipios.append(f"{municipio['nombre']} (nuevo)")
                                self.logger.info(f"Creado: {municipio['nombre']}")
                            else:
                                error_msg = f"Error al crear '{municipio['nombre']}'"
                                errors.append(error_msg)
                                error_count += 1
                    
                    except Exception as sheet_error:
                        error_msg = f"Error procesando hoja '{sheet_name}': {str(sheet_error)}"
                        errors.append(error_msg)
                        error_count += 1
                        self.logger.error(error_msg)
                
                # Cerrar diálogo de progreso
                if progress_dialog.open:
                    progress_dialog.open = False
                    self.page.update()
                
                # Mostrar resultados
                self._show_municipal_import_results(success_count, error_count, errors, processed_municipios)
                
                # Recargar datos si hubo éxitos
                if success_count > 0:
                    self._load_data()
                
            except Exception as excel_error:
                if progress_dialog.open:
                    progress_dialog.open = False
                    self.page.update()
                raise excel_error
            
        except Exception as e:
            self.logger.error(f"Error al procesar archivo Excel municipal: {e}")
            import traceback
            self.logger.error(f"Traceback completo: {traceback.format_exc()}")
            
            self._show_excel_error(f"Error al procesar el archivo: {str(e)}")

    def _extract_numeric_value(self, value):
        """Extrae valor numérico de una celda"""
        try:
            if pd.isna(value):
                return None
            
            # Si ya es numérico
            if isinstance(value, (int, float)):
                return float(value)
            
            # Si es string, limpiar y convertir
            if isinstance(value, str):
                # Remover espacios, comas, etc.
                clean_value = value.replace(',', '').replace(' ', '').strip()
                if clean_value:
                    return float(clean_value)
            
            return None
            
        except (ValueError, TypeError):
            return None

    def _get_import_period(self) -> tuple:
        """Obtiene el período (año, mes) para la importación"""
        año_field = ft.TextField(
            label="Año",
            value=str(self.current_año),
            width=120,
            keyboard_type=ft.KeyboardType.NUMBER
        )
        
        mes_dropdown = ft.Dropdown(
            label="Mes",
            width=180,
            value=str(self.current_mes),
            options=[
                ft.dropdown.Option("1", "Enero"),
                ft.dropdown.Option("2", "Febrero"),
                ft.dropdown.Option("3", "Marzo"),
                ft.dropdown.Option("4", "Abril"),
                ft.dropdown.Option("5", "Mayo"),
                ft.dropdown.Option("6", "Junio"),
                ft.dropdown.Option("7", "Julio"),
                ft.dropdown.Option("8", "Agosto"),
                ft.dropdown.Option("9", "Septiembre"),
                ft.dropdown.Option("10", "Octubre"),
                ft.dropdown.Option("11", "Noviembre"),
                ft.dropdown.Option("12", "Diciembre"),
            ]
        )
        
        result = {"año": None, "mes": None, "confirmed": False}
        
        def confirm_period(e):
            try:
                if not año_field.value or not mes_dropdown.value:
                    show_error("Por favor complete todos los campos")
                    return
                    
                result["año"] = int(año_field.value)
                result["mes"] = int(mes_dropdown.value)
                result["confirmed"] = True
                dialog.open = False
                self.page.update()
            except ValueError:
                show_error("Por favor ingrese un año válido")
        
        def cancel_period(e):
            result["confirmed"] = False
            dialog.open = False
            self.page.update()
        
        def show_error(message):
            error_text.value = message
            error_text.visible = True
            self.page.update()
        
        error_text = ft.Text("", color=ft.Colors.RED, size=12, visible=False)
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Período de Facturación"),
            content=ft.Container(
                content=ft.Column([
                    ft.Text("Seleccione el período para los datos a importar:"),
                    ft.Container(height=10),
                    ft.Row([año_field, mes_dropdown], spacing=15),
                    ft.Container(height=5),
                    error_text
                ]),
                width=350,
                height=150
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=cancel_period),
                ft.ElevatedButton("Confirmar", on_click=confirm_period)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        
        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()
        
        # Esperar hasta que se tome una decisión
        import time
        timeout = 30  # 30 segundos timeout
        elapsed = 0
        
        while dialog.open and elapsed < timeout:
            time.sleep(0.1)
            elapsed += 0.1
        
        # Limpiar overlay
        if dialog in self.page.overlay:
            self.page.overlay.remove(dialog)
            self.page.update()
        
        if result["confirmed"]:
            return result["año"], result["mes"]
        else:
            return None, None

    def _show_municipal_import_results(self, success_count: int, error_count: int, 
                                    errors: List[str], processed_municipios: List[str]):
        """Muestra los resultados de la importación municipal"""
        def close_dialog(e):
            dialog.open = False
            self.page.update()
        
        # Crear contenido del diálogo
        content_items = [
            ft.Row([
                ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN, size=24),
                ft.Text(f"Municipios procesados: {success_count}", size=16, color=ft.Colors.GREEN)
            ]),
            ft.Row([
                ft.Icon(ft.Icons.ERROR, color=ft.Colors.RED, size=24),
                ft.Text(f"Errores encontrados: {error_count}", size=16, color=ft.Colors.RED)
            ]),
            ft.Divider()
        ]
        
        if processed_municipios:
            content_items.append(ft.Text("✅ Municipios procesados exitosamente:", 
                                    weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN))
            for municipio in processed_municipios:
                content_items.append(ft.Text(f"  • {municipio}", size=12))
            content_items.append(ft.Container(height=10))
        
        if errors:
            content_items.append(ft.Text("❌ Errores encontrados:", 
                                    weight=ft.FontWeight.BOLD, color=ft.Colors.RED))
            # Mostrar máximo 5 errores para no saturar
            for error in errors[:5]:
                content_items.append(ft.Text(f"  • {error}", size=11, color=ft.Colors.RED))
            
            if len(errors) > 5:
                content_items.append(ft.Text(f"  ... y {len(errors) - 5} errores más", 
                                        size=11, color=ft.Colors.GREY))
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Resultados de Importación"),
            content=ft.Container(
                content=ft.Column(content_items, scroll=ft.ScrollMode.AUTO),
                width=500,
                height=400
            ),
            actions=[
                ft.TextButton("Cerrar", on_click=close_dialog)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        
        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()

    def _show_progress_dialog(self, message: str):
        """Muestra diálogo de progreso"""
        progress_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Procesando"),
            content=ft.Container(
                content=ft.Column([
                    ft.ProgressRing(),
                    ft.Container(height=10),
                    ft.Text(message, text_align=ft.TextAlign.CENTER)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                width=300,
                height=120
            )
        )
        
        self.page.overlay.append(progress_dialog)
        progress_dialog.open = True
        self.page.update()
        
        return progress_dialog

    def _show_excel_error(self, message: str):
        """Muestra error relacionado con Excel"""
        def close_dialog(e):
            dialog.open = False
            self.page.update()
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Error en archivo Excel"),
            content=ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.ERROR, color=ft.Colors.RED, size=48),
                    ft.Container(height=10),
                    ft.Text(message, text_align=ft.TextAlign.CENTER),
                    ft.Container(height=10),
                    ft.Text(
                        "Formato esperado:\n"
                        "• Cada hoja = un municipio\n"
                        "• Facturación Menor en celda C38\n"
                        "• Facturación Mayor en celda C41",
                        size=12,
                        color=ft.Colors.GREY_600,
                        text_align=ft.TextAlign.CENTER
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                width=400,
                height=200
            ),
            actions=[
                ft.TextButton("Entendido", on_click=close_dialog)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        
        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()

    def _find_municipio_by_name(self, nombre: str) -> Dict[str, Any]:
        """Busca un municipio por nombre con mapeo de variaciones"""
        if not self.municipios:
            self.logger.error("Lista de municipios está vacía")
            return None
        
        nombre_clean = nombre.lower().strip()
        self.logger.info(f"Buscando municipio: '{nombre_clean}'")
        
        # Mapeo de nombres del Excel a nombres en BD
        name_mapping = {
            'union': 'unión de reyes',
            'colon': 'colón',
            'arabos': 'los arabos',
            'marti': 'martí',
            'cardenas': 'cárdenas',
            'jaguey': 'jagüey grande',
            'cienaga': 'ciénaga de zapata',
            'betancourt': 'pedro betancourt'
        }
        
        # Aplicar mapeo si existe
        mapped_name = name_mapping.get(nombre_clean, nombre_clean)
        
        # Búsqueda exacta con nombre mapeado
        for municipio in self.municipios:
            municipio_name = municipio['nombre'].lower().strip()
            if municipio_name == mapped_name:
                self.logger.info(f"Municipio encontrado (mapeado): {municipio['nombre']}")
                return municipio
        
        # Búsqueda exacta con nombre original
        for municipio in self.municipios:
            municipio_name = municipio['nombre'].lower().strip()
            if municipio_name == nombre_clean:
                self.logger.info(f"Municipio encontrado (exacto): {municipio['nombre']}")
                return municipio
        
        # Búsqueda parcial
        for municipio in self.municipios:
            municipio_name = municipio['nombre'].lower().strip()
            if nombre_clean in municipio_name or municipio_name in nombre_clean:
                self.logger.info(f"Municipio encontrado (parcial): {municipio['nombre']}")
                return municipio
        
        # Mostrar municipios disponibles para debug
        municipios_disponibles = [m['nombre'] for m in self.municipios]
        self.logger.warning(f"Municipio '{nombre}' no encontrado. Disponibles: {municipios_disponibles}")
        
        return None

    def _debug_excel_processing(self, file_path: str):
        """Método de debug para verificar el procesamiento del Excel"""
        try:
            excel_file = pd.ExcelFile(file_path)
            sheet_names = excel_file.sheet_names
            
            self.logger.info(f"=== DEBUG EXCEL ===")
            self.logger.info(f"Archivo: {file_path}")
            self.logger.info(f"Hojas encontradas: {sheet_names}")
            self.logger.info(f"Municipios en BD: {[m['nombre'] for m in self.municipios]}")
            
            # Verificar primera hoja como ejemplo
            if sheet_names:
                first_sheet = sheet_names[0]
                df = pd.read_excel(file_path, sheet_name=first_sheet, header=None)
                
                self.logger.info(f"Hoja '{first_sheet}' - Dimensiones: {df.shape}")
                
                # Verificar celdas específicas
                if len(df) > 37 and len(df.columns) > 2:
                    valor_c38 = df.iloc[37, 2]
                    self.logger.info(f"Valor en C38: {valor_c38}")
                
                if len(df) > 40 and len(df.columns) > 2:
                    valor_c41 = df.iloc[40, 2]
                    self.logger.info(f"Valor en C41: {valor_c41}")
            
            self.logger.info(f"=== FIN DEBUG ===")
            
        except Exception as e:
            self.logger.error(f"Error en debug: {e}")

    def _clear_filters(self, e):
        """Limpia todos los filtros"""
        try:
            self.municipio_dropdown.value = ""
            self.año_field.value = str(self.current_año)
            self.mes_dropdown.value = ""
            
            # Limpiar datos
            self.facturaciones = []
            self._update_data_table()
            
            self.page.update()
            self._show_info("Filtros limpiados")  # Cambiar de show_info a _show_info
            
        except Exception as ex:
            self.logger.error(f"Error al limpiar filtros: {ex}")
            self._show_error("Error al limpiar filtros")

    def _export_to_excel(self, e):
        """Exporta los datos actuales a Excel"""
        try:
            if not self.facturaciones:
                self._show_warning("No hay datos para exportar")
                return
            
            # Preparar datos para exportación
            export_data = []
            for facturacion in self.facturaciones:
                export_data.append({
                    'ID': facturacion.id,
                    'Municipio': facturacion.municipio_nombre,
                    'Año': facturacion.año,
                    'Mes': facturacion.mes,
                    'Facturación Menor': facturacion.facturacion_menor,
                    'Facturación Mayor': facturacion.facturacion_mayor,
                    'Facturación Total': facturacion.facturacion_total,
                    'Fecha Creación': facturacion.fecha_creacion
                })
            
            df = pd.DataFrame(export_data)
            
            # Guardar archivo
            from pathlib import Path
            downloads_path = Path.home() / "Downloads"
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_path = downloads_path / f"facturacion_export_{timestamp}.xlsx"
            
            df.to_excel(file_path, index=False)
            
            self._show_success(f"Datos exportados a: {file_path}")
            
        except Exception as ex:
            self.logger.error(f"Error al exportar a Excel: {ex}")
            self._show_error("Error al exportar los datos")

    def _show_warning(self, message: str):
        """Muestra mensaje de advertencia"""
        snack_bar = ft.SnackBar(
            content=ft.Text(message, color=ft.Colors.WHITE),
            bgcolor=ft.Colors.ORANGE,
            action="OK",
            action_color=ft.Colors.WHITE
        )
        self.page.snack_bar = snack_bar
        snack_bar.open = True
        self.page.update()
