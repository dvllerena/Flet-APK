"""
Pantalla de gestión de planes de pérdidas
Permite crear, editar y gestionar los planes de pérdidas por municipio y mes
"""

import flet as ft
import pandas as pd
from datetime import datetime
from typing import List, Dict, Any, Optional
from infoperdidas.services import get_perdidas_service
from infoperdidas.models import PlanPerdidasModel
from core.logger import get_logger

class InfoPerdidasPlanesScreen:
    """Pantalla de gestión de planes de pérdidas"""
    
    def __init__(self, app):
        self.app = app
        self.page = app.page
        self.logger = get_logger(__name__)
        self.perdidas_service = get_perdidas_service()
        
        # Estado
        self.planes_data = []
        self.municipios = []
        self.current_año = datetime.now().year
        
        # Controles
        self.año_field = None
        self.mes_dropdown = None
        self.data_table = None
        self.edit_dialog = None
        
        # Cargar municipios
        self._load_municipios()
    
    def _load_municipios(self):
        """Carga la lista de municipios"""
        try:
            self.municipios = self.perdidas_service.get_municipios_activos()
            self.logger.info(f"Municipios cargados: {len(self.municipios)}")
        except Exception as e:
            self.logger.error(f"Error cargando municipios: {e}")
            self.municipios = []
    
    def build(self) -> ft.Control:
        """Construye la interfaz"""
        return ft.Container(
            content=ft.Column([
                self._build_header(),
                self._build_filters(),
                self._build_actions_bar(),
                self._build_data_table(),
                self._build_bulk_actions()
            ], spacing=20),
            padding=20,
            expand=True
        )
    
    def _build_header(self) -> ft.Control:
        """Construye el header de la pantalla"""
        return ft.Container(
            content=ft.Row([
                ft.Column([
                    ft.Text("Gestión de Planes de Pérdidas", size=24, weight=ft.FontWeight.BOLD),
                    ft.Text("Administración de planes de pérdidas por municipio y período", 
                           size=14, color=ft.Colors.GREY_600)
                ], expand=True),
                ft.Row([
                    ft.IconButton(
                        ft.Icons.REFRESH,
                        tooltip="Actualizar",
                        on_click=self._load_data
                    ),
                    ft.IconButton(
                        ft.Icons.ARROW_BACK,
                        tooltip="Volver",
                        on_click=lambda _: self.app.navigate_to("infoperdidas")
                    )
                ])
            ]),
            bgcolor=ft.Colors.ORANGE_50,
            padding=20,
            border_radius=10
        )
    
    def _build_filters(self) -> ft.Control:
        """Construye los filtros de búsqueda"""
        self.año_field = ft.TextField(
            label="Año",
            value=str(self.current_año),
            width=100,
            keyboard_type=ft.KeyboardType.NUMBER
        )
        
        self.mes_dropdown = ft.Dropdown(
            label="Mes",
            width=150,
            value="",  # Valor vacío por defecto
            options=[
                ft.dropdown.Option("", "Todos los meses"),  # Valor vacío para "todos"
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
        
        # Nuevo filtro por municipio
        self.municipio_dropdown = ft.Dropdown(
            label="Municipio",
            width=200,
            value="",  # Ensure this is empty string by default
            options=[ft.dropdown.Option("", "Todos los municipios")] + 
                    [ft.dropdown.Option("provincial", "PROVINCIAL")] +
                    [ft.dropdown.Option(str(m['id']), m['nombre']) for m in self.municipios]
        )
        
        load_button = ft.ElevatedButton(
            "Cargar Planes",
            icon=ft.Icons.SEARCH,
            on_click=self._load_data,
            bgcolor=ft.Colors.ORANGE,
            color=ft.Colors.WHITE
        )
        
        clear_button = ft.IconButton(
            icon=ft.Icons.CLEAR,
            tooltip="Limpiar filtros",
            on_click=self._clear_filters
        )
        
        return ft.Container(
            content=ft.Column([
                ft.Text("Filtros de Búsqueda", size=16, weight=ft.FontWeight.BOLD),
                ft.Row([
                    self.año_field,
                    self.mes_dropdown,
                    self.municipio_dropdown,
                    load_button,
                    clear_button,
                    ft.Container(expand=True),
                    ft.Text(f"Planes encontrados: {len(self.planes_data)}", 
                        size=12, color=ft.Colors.GREY_600)
                ], spacing=15)
            ], spacing=10),
            bgcolor=ft.Colors.GREY_50,
            padding=15,
            border_radius=10
        )

    def _build_actions_bar(self) -> ft.Control:
        """Construye la barra de acciones"""
        return ft.Container(
            content=ft.Row([
                ft.ElevatedButton(
                    "Nuevo Plan",
                    icon=ft.Icons.ADD,
                    on_click=self._new_plan,
                    bgcolor=ft.Colors.GREEN,
                    color=ft.Colors.WHITE
                ),
                ft.ElevatedButton(
                    "Importar desde Excel",
                    icon=ft.Icons.UPLOAD_FILE,
                    on_click=self._import_from_excel,
                    bgcolor=ft.Colors.BLUE,
                    color=ft.Colors.WHITE
                ),
                ft.Container(expand=True),
                
            ], spacing=10)
        )
    
    def _build_data_table(self) -> ft.Control:
        """Construye la tabla de datos"""
        self.data_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Municipio")),
                ft.DataColumn(ft.Text("Año")),
                ft.DataColumn(ft.Text("Mes")),
                ft.DataColumn(ft.Text("Plan (%)")),
                ft.DataColumn(ft.Text("Observaciones")),
                ft.DataColumn(ft.Text("Usuario")),
                ft.DataColumn(ft.Text("Fecha Modificación")),
                ft.DataColumn(ft.Text("Acciones"))
            ],
            rows=[]
        )
        
        return ft.Container(
            content=ft.Column([
                ft.Text("Planes de Pérdidas", size=18, weight=ft.FontWeight.BOLD),
                ft.Container(
                    content=self.data_table,
                    border=ft.border.all(1, ft.Colors.GREY_300),
                    border_radius=5,
                    padding=10
                )
            ]),
            expand=True
        )
    
    def _build_bulk_actions(self) -> ft.Control:
        """Construye las acciones masivas"""
        return ft.Container(
            content=ft.Row([
                ft.ElevatedButton(
                    "Copiar Planes a Otro Año",
                    icon=ft.Icons.COPY,
                    on_click=self._copy_plans_to_year,
                    bgcolor=ft.Colors.PURPLE,
                    color=ft.Colors.WHITE
                ),
                ft.ElevatedButton(
                    "Crear Planes para Todo el Año",
                    icon=ft.Icons.CALENDAR_VIEW_MONTH,
                    on_click=self._create_yearly_plans,
                    bgcolor=ft.Colors.INDIGO,
                    color=ft.Colors.WHITE
                ),
                ft.Container(expand=True),
                ft.Text("Acciones Masivas", size=12, color=ft.Colors.GREY_600)
            ], spacing=10),
            padding=ft.padding.only(top=20)
        )
    
    def _load_data(self, e=None):
        """Carga los planes de pérdidas con filtros aplicados"""
        try:
            año = int(self.año_field.value) if self.año_field.value else self.current_año
            
            # Corregir la lógica para el mes - verificar si es un número válido
            mes = None
            if self.mes_dropdown.value and self.mes_dropdown.value.isdigit():
                mes = int(self.mes_dropdown.value)
            
            # Obtener filtro de municipio - FIX: Verificar que el valor no esté vacío y sea válido
            municipio_filter = self.municipio_dropdown.value
            municipio_id = None
            
            # FIX: Verificar que municipio_filter no esté vacío y no sea el texto de display
            if municipio_filter and municipio_filter != "" and municipio_filter != "Todos los municipios":
                if municipio_filter == "provincial":
                    municipio_id = "provincial"  # Indicador especial para provincial
                else:
                    try:
                        municipio_id = int(municipio_filter)
                    except ValueError:
                        # Si no se puede convertir a int, es probablemente texto de display
                        self.logger.warning(f"Valor de municipio inválido: {municipio_filter}")
                        municipio_id = None
            
            # Cargar planes con filtros
            self.planes_data = self.perdidas_service.get_planes_by_periodo_filtered(año, mes, municipio_id)
            self._update_data_table()
            
            # Mensaje de resultado
            filter_msg = f"año {año}"
            if mes:
                filter_msg += f", mes {self._get_month_name(mes)}"
            if municipio_id:
                if municipio_id == "provincial":
                    filter_msg += ", PROVINCIAL"
                else:
                    municipio_nombre = next((m['nombre'] for m in self.municipios if m['id'] == municipio_id), "")
                    filter_msg += f", {municipio_nombre}"
            
            self._show_success(f"Se cargaron {len(self.planes_data)} planes para {filter_msg}")
            
        except Exception as e:
            self.logger.error(f"Error cargando planes: {e}")
            self._show_error("Error al cargar los planes de pérdidas")

    def _update_data_table(self):
        """Actualiza la tabla de datos"""
        self.data_table.rows.clear()
        
        for plan in self.planes_data:
            # Determinar nombre del municipio
            municipio_nombre = plan.municipio_nombre if plan.municipio_nombre else "PROVINCIAL"
            
            # Formatear fecha
            fecha_mod = ""
            if plan.fecha_modificacion:
                try:
                    if isinstance(plan.fecha_modificacion, str):
                        fecha_mod = plan.fecha_modificacion[:16]  # YYYY-MM-DD HH:MM
                    else:
                        fecha_mod = plan.fecha_modificacion.strftime("%Y-%m-%d %H:%M")
                except:
                    fecha_mod = str(plan.fecha_modificacion)[:16]
            
            self.data_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(municipio_nombre, weight=ft.FontWeight.BOLD if not plan.municipio_id else None)),
                        ft.DataCell(ft.Text(str(plan.año))),
                        ft.DataCell(ft.Text(self._get_month_name(plan.mes))),
                        ft.DataCell(ft.Text(f"{plan.plan_perdidas_pct:.2f}%", 
                                          color=ft.Colors.BLUE, weight=ft.FontWeight.BOLD)),
                        ft.DataCell(ft.Text(plan.observaciones or "", max_lines=2)),
                        ft.DataCell(ft.Text(plan.usuario_nombre or "")),
                        ft.DataCell(ft.Text(fecha_mod)),
                        ft.DataCell(
                            ft.Row([
                                ft.IconButton(
                                    icon=ft.Icons.EDIT,
                                    tooltip="Editar",
                                    on_click=lambda e, p=plan: self._edit_plan(p)
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.DELETE,
                                    tooltip="Eliminar",
                                    on_click=lambda e, p=plan: self._delete_plan(p)
                                )
                            ], spacing=5)
                        )
                    ]
                )
            )
        
        self.page.update()
    
    def _get_month_name(self, mes: int) -> str:
        """Obtiene el nombre del mes"""
        months = {
            1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
            5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
            9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
        }
        return months.get(mes, str(mes))
    
    def _new_plan(self, e):
        """Crea un nuevo plan"""
        self._show_edit_dialog()
    
    def _edit_plan(self, plan: PlanPerdidasModel):
        """Edita un plan existente"""
        self._show_edit_dialog(plan)
    
    def _show_edit_dialog(self, plan: Optional[PlanPerdidasModel] = None):
        """Muestra el diálogo de edición"""
        is_edit = plan is not None
        
        if not is_edit:
            plan = PlanPerdidasModel(
                año=int(self.año_field.value) if self.año_field.value else self.current_año,
                mes=1
            )
        
        # Controles del diálogo
        municipio_dropdown = ft.Dropdown(
            label="Municipio",
            width=250,
            value=str(plan.municipio_id) if plan.municipio_id else "",
            options=[ft.dropdown.Option("", "PROVINCIAL")] + [
                ft.dropdown.Option(str(m['id']), m['nombre']) 
                for m in self.municipios
            ]
        )
        
        año_field = ft.TextField(
            label="Año",
            value=str(plan.año),
            width=100,
            keyboard_type=ft.KeyboardType.NUMBER
        )
        
        mes_dropdown = ft.Dropdown(
            label="Mes",
            width=150,
            value=str(plan.mes),
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
        
        plan_field = ft.TextField(
            label="Plan de Pérdidas (%)",
            value=str(plan.plan_perdidas_pct),
            width=150,
            keyboard_type=ft.KeyboardType.NUMBER,
            suffix_text="%"
        )
        
        observaciones_field = ft.TextField(
            label="Observaciones",
            value=plan.observaciones or "",
            multiline=True,
            min_lines=2,
            max_lines=4,
            expand=True
        )
        
        def save_plan(e):
            try:
                # Validar campos
                if not año_field.value or not mes_dropdown.value or not plan_field.value:
                    self._show_error("Todos los campos son obligatorios")
                    return
                
                # Actualizar modelo
                plan.municipio_id = int(municipio_dropdown.value) if municipio_dropdown.value else None
                plan.año = int(año_field.value)
                plan.mes = int(mes_dropdown.value)
                plan.plan_perdidas_pct = float(plan_field.value)
                plan.observaciones = observaciones_field.value
                
                # Establecer usuario actual
                if self.app.current_user:
                    plan.usuario_id = self.app.current_user['id']
                
                # Guardar
                if self.perdidas_service.save_plan_perdidas(plan):
                    self._show_success("Plan guardado correctamente")
                    self._load_data()
                    self.edit_dialog.open = False
                    self.page.update()
                else:
                    self._show_error("Error al guardar el plan")
                    
            except ValueError:
                self._show_error("Por favor ingrese valores numéricos válidos")
            except Exception as ex:
                self.logger.error(f"Error guardando plan: {ex}")
                self._show_error("Error al guardar el plan")
        
        def cancel_edit(e):
            self.edit_dialog.open = False
            self.page.update()
        
        # Crear diálogo
        self.edit_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Editar Plan" if is_edit else "Nuevo Plan"),
            content=ft.Container(
                content=ft.Column([
                    ft.Row([municipio_dropdown]),
                    ft.Row([año_field, mes_dropdown, plan_field], spacing=15),
                    ft.Text("Observaciones:"),
                    observaciones_field
                ], spacing=10),
                width=500,
                height=300
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=cancel_edit),
                ft.ElevatedButton("Guardar", on_click=save_plan)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        
        self.page.overlay.append(self.edit_dialog)
        self.edit_dialog.open = True
        self.page.update()
    
    def _delete_plan(self, plan: PlanPerdidasModel):
        """Elimina un plan"""
        def confirm_delete(e):
            if self.perdidas_service.delete_plan_perdidas(plan.id):
                self._show_success("Plan eliminado correctamente")
                self._load_data()
            else:
                self._show_error("Error al eliminar el plan")
            dialog.open = False
            self.page.update()
        
        def cancel_delete(e):
            dialog.open = False
            self.page.update()
        
        municipio_name = plan.municipio_nombre if plan.municipio_nombre else "PROVINCIAL"
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmar Eliminación"),
            content=ft.Text(f"¿Está seguro de eliminar el plan de {municipio_name} para {self._get_month_name(plan.mes)}/{plan.año}?"),
            actions=[
                ft.TextButton("Cancelar", on_click=cancel_delete),
                ft.TextButton("Eliminar", on_click=confirm_delete)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        
        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()
    
    def _copy_plans_to_year(self, e):
        """Copia planes de un año a otro"""
        año_origen_field = ft.TextField(
            label="Año Origen",
            value=str(self.current_año - 1),
            width=120,
            keyboard_type=ft.KeyboardType.NUMBER
        )
        
        año_destino_field = ft.TextField(
            label="Año Destino",
            value=str(self.current_año),
            width=120,
            keyboard_type=ft.KeyboardType.NUMBER
        )
        
        def copy_plans(e):
            try:
                año_origen = int(año_origen_field.value)
                año_destino = int(año_destino_field.value)
                
                if año_origen == año_destino:
                    self._show_error("Los años deben ser diferentes")
                    return
                
                user_id = self.app.current_user['id'] if self.app.current_user else 1
                
                if self.perdidas_service.copy_planes_to_year(año_origen, año_destino, user_id):
                    self._show_success(f"Planes copiados de {año_origen} a {año_destino}")
                    self._load_data()
                    dialog.open = False
                    self.page.update()
                else:
                    self._show_error("Error al copiar planes. Verifique que no existan planes en el año destino.")
                    
            except ValueError:
                self._show_error("Por favor ingrese años válidos")
            except Exception as ex:
                self.logger.error(f"Error copiando planes: {ex}")
                self._show_error("Error al copiar los planes")
        
        def cancel_copy(e):
            dialog.open = False
            self.page.update()
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Copiar Planes a Otro Año"),
            content=ft.Container(
                content=ft.Column([
                    ft.Text("Seleccione los años para copiar los planes:"),
                    ft.Row([año_origen_field, año_destino_field], spacing=15),
                    ft.Text("⚠️ Esta acción copiará todos los planes del año origen al año destino.", 
                           color=ft.Colors.ORANGE, size=12)
                ]),
                width=350,
                height=120
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=cancel_copy),
                ft.ElevatedButton("Copiar", on_click=copy_plans)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        
        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()
    
    def _create_yearly_plans(self, e):
        """Crea planes para todo el año"""
        año_field = ft.TextField(
            label="Año",
            value=str(self.current_año),
            width=120,
            keyboard_type=ft.KeyboardType.NUMBER
        )
        
        plan_field = ft.TextField(
            label="Plan de Pérdidas (%)",
            value="8.5",
            width=150,
            keyboard_type=ft.KeyboardType.NUMBER,
            suffix_text="%"
        )
        
        incluir_provincial = ft.Checkbox(
            label="Incluir plan provincial",
            value=True
        )
        
        def create_plans(e):
            try:
                año = int(año_field.value)
                plan_pct = float(plan_field.value)
                
                if plan_pct < 0 or plan_pct > 100:
                    self._show_error("El porcentaje debe estar entre 0 y 100")
                    return
                
                user_id = self.app.current_user['id'] if self.app.current_user else 1
                created_count = 0
                
                # Crear planes para cada mes (1-12)
                for mes in range(1, 13):
                    # Plan provincial si está marcado
                    if incluir_provincial.value:
                        plan_provincial = PlanPerdidasModel(
                            municipio_id=None,
                            año=año,
                            mes=mes,
                            plan_perdidas_pct=plan_pct,
                            observaciones=f"Plan creado automáticamente para {año}",
                            usuario_id=user_id
                        )
                        
                        if self.perdidas_service.save_plan_perdidas(plan_provincial):
                            created_count += 1
                    
                    # Planes por municipio
                    for municipio in self.municipios:
                        plan_municipio = PlanPerdidasModel(
                            municipio_id=municipio['id'],
                            año=año,
                            mes=mes,
                            plan_perdidas_pct=plan_pct,
                            observaciones=f"Plan creado automáticamente para {año}",
                            usuario_id=user_id
                        )
                        
                        if self.perdidas_service.save_plan_perdidas(plan_municipio):
                            created_count += 1
                
                if created_count > 0:
                    self._show_success(f"Se crearon {created_count} planes para el año {año}")
                    self._load_data()
                    dialog.open = False
                    self.page.update()
                else:
                    self._show_error("No se pudieron crear los planes")
                    
            except ValueError:
                self._show_error("Por favor ingrese valores válidos")
            except Exception as ex:
                self.logger.error(f"Error creando planes anuales: {ex}")
                self._show_error("Error al crear los planes")
        
        def cancel_create(e):
            dialog.open = False
            self.page.update()
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Crear Planes para Todo el Año"),
            content=ft.Container(
                content=ft.Column([
                    ft.Text("Configure los planes que se crearán:"),
                    ft.Row([año_field, plan_field], spacing=15),
                    incluir_provincial,
                    ft.Text("⚠️ Se crearán planes para todos los municipios y meses del año.", 
                           color=ft.Colors.ORANGE, size=12)
                ]),
                width=400,
                height=150
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=cancel_create),
                ft.ElevatedButton("Crear", on_click=create_plans)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        
        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()
    
    def _import_from_excel(self, e):
        """Importa planes desde un archivo Excel"""
        def on_file_selected(e: ft.FilePickerResultEvent):
            if e.files:
                file_path = e.files[0].path
                self._process_excel_file(file_path)
        
        # Crear file picker
        file_picker = ft.FilePicker(on_result=on_file_selected)
        self.page.overlay.append(file_picker)
        self.page.update()
        
        # Abrir diálogo de selección de archivo
        file_picker.pick_files(
            dialog_title="Seleccionar archivo Excel de Planes",
            file_type=ft.FilePickerFileType.CUSTOM,
            allowed_extensions=["xlsx", "xls"]
        )
    
    def _process_sheet_data(self, df: 'pd.DataFrame', año: int, user_id: int, tipo: str, results: dict):
        """Procesa los datos de una hoja específica"""
        
        
        try:
            # Validar que el DataFrame no esté vacío
            if df.empty:
                
                results[tipo]['errors'] += 1
                results[tipo]['warnings'].append(f"La hoja de planes {tipo} está vacía")
                return
            
            
            
            # Obtener nombres de columnas (meses)
            meses_columnas = df.columns[1:13]  # Columnas B-M (12 meses)
            
            
            meses_nombres = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                            'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
            
            # Procesar cada fila (municipio)
            for index, row in df.iterrows():
               
                
                try:
                    municipio_nombre = str(row.iloc[0]).strip()
                   
                    
                    if not municipio_nombre or municipio_nombre.lower() in ['nan', 'none', '']:
                        
                        continue
                    
                    # Identificar si es provincial o municipal
                    municipio_id = None
                    if municipio_nombre.lower() == 'provincia':
                        
                        municipio_id = None
                    else:
                       
                        municipio = self._find_municipio_by_name(municipio_nombre)
                        if not municipio:
                           
                            results[tipo]['warnings'].append(
                                f"Municipio '{municipio_nombre}' no encontrado"
                            )
                            results[tipo]['errors'] += 1
                            continue
                        municipio_id = municipio['id']
                        
                    
                    # Procesar cada mes
                    for mes_idx, mes_col in enumerate(meses_columnas):
                        mes_numero = mes_idx + 1
                        mes_nombre = meses_nombres[mes_idx]
                        valor_celda = row[mes_col]
                        
                        
                        
                        # Verificar celdas vacías
                        if pd.isna(valor_celda) or valor_celda == '':
                            
                            results['empty_cells'].append(
                                f"{municipio_nombre} - {mes_nombre} ({tipo})"
                            )
                            plan_pct = 0.0
                        else:
                            try:
                                plan_pct = float(valor_celda)
                               
                            except (ValueError, TypeError):
                                
                                results[tipo]['warnings'].append(
                                    f"Valor inválido en {municipio_nombre} - {mes_nombre}: {valor_celda}"
                                )
                                plan_pct = 0.0
                        
                        # Verificar si ya existe el plan
                        existing_plan = self.perdidas_service.get_plan_by_municipio_periodo(municipio_id, año, mes_numero)
                        
                        if existing_plan:
                            
                            # Actualizar plan existente
                            existing_plan.plan_perdidas_pct = plan_pct
                            existing_plan.observaciones = f"Actualizado desde Excel - Plan {tipo} {año}"
                            existing_plan.usuario_id = user_id
                            plan = existing_plan
                        else:
                           
                            # Crear nuevo plan
                            plan = PlanPerdidasModel(
                                municipio_id=municipio_id,
                                año=año,
                                mes=mes_numero,
                                plan_perdidas_pct=plan_pct,
                                observaciones=f"Importado desde Excel - Plan {tipo} {año}",
                                usuario_id=user_id
                            )
                        
                        
                        
                        # Guardar plan
                        
                        try:
                            save_result = self.perdidas_service.save_plan_perdidas(plan)
                           
                            
                            if save_result:
                                results[tipo]['success'] += 1
                                
                            else:
                                results[tipo]['errors'] += 1
                                error_msg = f"Error guardando {municipio_nombre} - {mes_nombre}"
                                results[tipo]['warnings'].append(error_msg)
                                
                                
                        except Exception as save_ex:
                           
                            import traceback
                            traceback.print_exc()
                            results[tipo]['errors'] += 1
                            results[tipo]['warnings'].append(
                                f"Excepción guardando {municipio_nombre} - {mes_nombre}: {str(save_ex)}"
                            )
                            
                except Exception as ex:
                    
                    import traceback
                    traceback.print_exc()
                    results[tipo]['errors'] += 1
                    results[tipo]['warnings'].append(
                        f"Error procesando fila {index + 3}: {str(ex)}"
                    )
                    
        except Exception as e:
            
            import traceback
            traceback.print_exc()
            self.logger.error(f"Error procesando hoja {tipo}: {e}")
            results[tipo]['errors'] += 1
            results[tipo]['warnings'].append(f"Error general en hoja {tipo}: {str(e)}")

    def _import_from_excel(self, e):
        """Importa planes desde un archivo Excel"""
        def on_file_selected(e: ft.FilePickerResultEvent):
            if e.files:
                file_path = e.files[0].path
                self._process_excel_file(file_path)
        
        # Crear file picker
        file_picker = ft.FilePicker(on_result=on_file_selected)
        self.page.overlay.append(file_picker)
        self.page.update()
        
        # Abrir diálogo de selección de archivo
        file_picker.pick_files(
            dialog_title="Seleccionar archivo Excel de Planes",
            file_type=ft.FilePickerFileType.CUSTOM,
            allowed_extensions=["xlsx", "xls"]
        )

    def _process_excel_file(self, file_path: str):
        """Procesa el archivo Excel con planes mensuales y acumulados"""
        try:
            import pandas as pd
            
            # Mostrar diálogo de progreso
            progress_dialog = self._show_progress_dialog("Procesando archivo Excel...")
            
            try:
                # Leer ambas hojas
                planes_mensuales = pd.read_excel(file_path, sheet_name='Planes2', header=1)
                planes_acumulados = pd.read_excel(file_path, sheet_name='Planes', header=1)
                
            except Exception as e:
                progress_dialog.open = False
                self.page.update()
                self._show_error(f"Error al leer el archivo Excel: {str(e)}")
                return
            
            # Obtener año para la importación
            año = self._get_import_year()
            
            if not año:
                progress_dialog.open = False
                self.page.update()
                return
            
            # Preguntar si sobrescribir datos existentes
            if not self._confirm_overwrite(año):
                progress_dialog.open = False
                self.page.update()
                return
            
            # Procesar datos
            results = {
                'mensuales': {'success': 0, 'errors': 0, 'warnings': []},
                'acumulados': {'success': 0, 'errors': 0, 'warnings': []},
                'empty_cells': []
            }
            
            user_id = self.app.current_user['id'] if self.app.current_user else 1
            
            # Procesar planes mensuales
            self._process_sheet_data(planes_mensuales, año, user_id, "mensuales", results)
            
            # Procesar planes acumulados
            self._process_sheet_data(planes_acumulados, año, user_id, "acumulados", results)
            
            # Cerrar diálogo de progreso
            progress_dialog.open = False
            self.page.update()
            
            # Mostrar resultados
            self._show_import_results_detailed(results)
            
            # Recargar datos si hubo éxito
            if results['mensuales']['success'] > 0 or results['acumulados']['success'] > 0:
                self._load_data()
                
        except ImportError:
            self._show_error("pandas no está instalado. Instale con: pip install pandas openpyxl")
        except Exception as e:
            self.logger.error(f"Error procesando archivo Excel: {e}")
            if 'progress_dialog' in locals() and progress_dialog.open:
                progress_dialog.open = False
                self.page.update()
            self._show_error(f"Error al procesar el archivo: {str(e)}")

    def _confirm_overwrite(self, año: int) -> bool:
        """Confirma si se deben sobrescribir los datos existentes"""
        result = {"confirmed": False}
        
        def confirm_overwrite(e):
            result["confirmed"] = True
            dialog.open = False
            self.page.update()
        
        def cancel_overwrite(e):
            result["confirmed"] = False
            dialog.open = False
            self.page.update()
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("⚠️ Datos Existentes"),
            content=ft.Container(
                content=ft.Column([
                    ft.Text(f"Ya existen planes para el año {año} en la base de datos."),
                    ft.Text("¿Desea sobrescribir los datos existentes?"),
                    ft.Text("Esta acción no se puede deshacer.", color=ft.Colors.RED, size=12)
                ]),
                width=400,
                height=100
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=cancel_overwrite),
                ft.ElevatedButton("Sobrescribir", on_click=confirm_overwrite, bgcolor=ft.Colors.RED, color=ft.Colors.WHITE)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        
        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()
        
        # Esperar decisión
        import time
        timeout = 30
        elapsed = 0
        
        while dialog.open and elapsed < timeout:
            time.sleep(0.1)
            elapsed += 0.1
        
        if dialog in self.page.overlay:
            self.page.overlay.remove(dialog)
            self.page.update()
        
        return result["confirmed"]

    def _find_municipio_by_name(self, nombre: str) -> Optional[Dict[str, Any]]:
        """Busca un municipio por nombre"""
        nombre_clean = nombre.lower().strip()
        
        # Búsqueda exacta
        for municipio in self.municipios:
            municipio_clean = municipio['nombre'].lower().strip()
            if municipio_clean == nombre_clean:
                return municipio
        
        # Búsqueda parcial
        for municipio in self.municipios:
            municipio_clean = municipio['nombre'].lower()
            if nombre_clean in municipio_clean or municipio_clean in nombre_clean:
                return municipio
        
        return None


    def _get_import_year(self) -> Optional[int]:
        """Obtiene el año para la importación"""
        año_field = ft.TextField(
            label="Año para importar",
            value=str(self.current_año),
            width=120,
            keyboard_type=ft.KeyboardType.NUMBER
        )
        
        result = {"año": None, "confirmed": False}
        
        def confirm_year(e):
            try:
                año_val = int(año_field.value)
                if año_val < 2000 or año_val > 2100:
                    self._show_error("El año debe estar entre 2000 y 2100")
                    return
                result["año"] = año_val
                result["confirmed"] = True
                dialog.open = False
                self.page.update()
            except ValueError:
                self._show_error("Por favor ingrese un año válido")
        
        def cancel_year(e):
            result["confirmed"] = False
            dialog.open = False
            self.page.update()
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Año para Importación"),
            content=ft.Container(
                content=ft.Column([
                    ft.Text("Ingrese el año para los planes a importar:"),
                    año_field,
                    ft.Text("⚠️ Se importarán planes mensuales y acumulados", 
                        color=ft.Colors.ORANGE, size=12)
                ]),
                width=300,
                height=120
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=cancel_year),
                ft.ElevatedButton("Confirmar", on_click=confirm_year)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        
        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()
        
        # Esperar decisión
        import time
        timeout = 30
        elapsed = 0
        
        while dialog.open and elapsed < timeout:
            time.sleep(0.1)
            elapsed += 0.1
        
        if dialog in self.page.overlay:
            self.page.overlay.remove(dialog)
            self.page.update()
        
        return result["año"] if result["confirmed"] else None

    def _show_import_results_detailed(self, results: dict):
        """Muestra los resultados detallados de la importación"""
        def close_dialog(e):
            dialog.open = False
            self.page.update()
        
        content_items = [
            ft.Text("📊 Resultados de Importación", size=18, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            
            # Planes mensuales
            ft.Row([
                ft.Icon(ft.Icons.CALENDAR_MONTH, color=ft.Colors.BLUE, size=20),
                ft.Text("Planes Mensuales:", weight=ft.FontWeight.BOLD)
            ]),
            ft.Row([
                ft.Text(f"  ✅ Importados: {results['mensuales']['success']}", color=ft.Colors.GREEN),
                ft.Text(f"  ❌ Errores: {results['mensuales']['errors']}", color=ft.Colors.RED)
            ]),
            
            ft.Container(height=10),
            
            # Planes acumulados
            ft.Row([
                ft.Icon(ft.Icons.TRENDING_UP, color=ft.Colors.PURPLE, size=20),
                ft.Text("Planes Acumulados:", weight=ft.FontWeight.BOLD)
            ]),
            ft.Row([
                ft.Text(f"  ✅ Importados: {results['acumulados']['success']}", color=ft.Colors.GREEN),
                ft.Text(f"  ❌ Errores: {results['acumulados']['errors']}", color=ft.Colors.RED)
            ]),
            
            ft.Divider()
        ]
        
        # Celdas vacías
        if results['empty_cells']:
            content_items.extend([
                ft.Text("⚠️ Celdas Vacías Encontradas:", weight=ft.FontWeight.BOLD, color=ft.Colors.ORANGE),
                ft.Container(
                    content=ft.Column([
                        ft.Text(f"• {cell}", size=11) for cell in results['empty_cells'][:10]
                    ], scroll=ft.ScrollMode.AUTO),
                    height=100,
                    bgcolor=ft.Colors.ORANGE_50,
                    padding=10,
                    border_radius=5
                )
            ])
            
            if len(results['empty_cells']) > 10:
                content_items.append(
                    ft.Text(f"... y {len(results['empty_cells']) - 10} celdas vacías más", 
                        size=11, color=ft.Colors.GREY)
                )
        
        # Advertencias
        all_warnings = results['mensuales']['warnings'] + results['acumulados']['warnings']
        if all_warnings:
            content_items.extend([
                ft.Container(height=10),
                ft.Text("⚠️ Advertencias:", weight=ft.FontWeight.BOLD, color=ft.Colors.ORANGE),
                ft.Container(
                    content=ft.Column([
                        ft.Text(f"• {warning}", size=11) for warning in all_warnings[:5]
                    ], scroll=ft.ScrollMode.AUTO),
                    height=100,
                    bgcolor=ft.Colors.ORANGE_50,
                    padding=10,
                    border_radius=5
                )
            ])
            
            if len(all_warnings) > 5:
                content_items.append(
                    ft.Text(f"... y {len(all_warnings) - 5} advertencias más", 
                        size=11, color=ft.Colors.GREY)
                )
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Resultados de Importación"),
            content=ft.Container(
                content=ft.Column(content_items, scroll=ft.ScrollMode.AUTO),
                width=600,
                height=500
            ),
            actions=[
                ft.TextButton("Cerrar", on_click=close_dialog)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        
        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()
    
    def _clear_filters(self, e=None):
        """Limpia todos los filtros"""
        self.año_field.value = str(self.current_año)
        self.mes_dropdown.value = ""
        self.municipio_dropdown.value = ""
        self.planes_data = []
        self._update_data_table()
        self.page.update()

    def _get_import_period(self) -> tuple:
        """Obtiene el período para la importación"""
        año_field = ft.TextField(
            label="Año por defecto",
            value=str(self.current_año),
            width=120,
            keyboard_type=ft.KeyboardType.NUMBER
        )
        
        mes_dropdown = ft.Dropdown(
            label="Mes por defecto",
            width=180,
            value="1",
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
                result["año"] = int(año_field.value)
                result["mes"] = int(mes_dropdown.value)
                result["confirmed"] = True
                dialog.open = False
                self.page.update()
            except ValueError:
                self._show_error("Por favor ingrese valores válidos")
        
        def cancel_period(e):
            result["confirmed"] = False
            dialog.open = False
            self.page.update()
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Período por Defecto"),
            content=ft.Container(
                content=ft.Column([
                    ft.Text("Valores por defecto para registros sin año/mes:"),
                    ft.Row([año_field, mes_dropdown], spacing=15)
                ]),
                width=350,
                height=100
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
        
        # Esperar decisión
        import time
        timeout = 30
        elapsed = 0
        
        while dialog.open and elapsed < timeout:
            time.sleep(0.1)
            elapsed += 0.1
        
        if dialog in self.page.overlay:
            self.page.overlay.remove(dialog)
            self.page.update()
        
        if result["confirmed"]:
            return result["año"], result["mes"]
        else:
            return None, None
    
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
    
    def _show_import_results(self, success_count: int, error_count: int, errors: List[str]):
        """Muestra los resultados de la importación"""
        def close_dialog(e):
            dialog.open = False
            self.page.update()
        
        content_items = [
            ft.Row([
                ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN, size=24),
                ft.Text(f"Planes importados: {success_count}", size=16, color=ft.Colors.GREEN)
            ]),
            ft.Row([
                ft.Icon(ft.Icons.ERROR, color=ft.Colors.RED, size=24),
                ft.Text(f"Errores encontrados: {error_count}", size=16, color=ft.Colors.RED)
            ]),
            ft.Divider()
        ]
        
        if errors:
            content_items.append(ft.Text("❌ Errores:", weight=ft.FontWeight.BOLD, color=ft.Colors.RED))
            for error in errors[:5]:  # Mostrar máximo 5 errores
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
    
    def _export_to_excel(self, e):
        """Exporta los planes a Excel"""
        try:
            if not self.planes_data:
                self._show_warning("No hay planes para exportar")
                return
            
            import pandas as pd
            from pathlib import Path
            # Preparar datos para exportación
            export_data = []
            for plan in self.planes_data:
                export_data.append({
                    'municipio': plan.municipio_nombre if plan.municipio_nombre else 'PROVINCIAL',
                    'año': plan.año,
                    'mes': plan.mes,
                    'mes_nombre': self._get_month_name(plan.mes),
                    'plan_perdidas_pct': plan.plan_perdidas_pct,
                    'observaciones': plan.observaciones or '',
                    'usuario': plan.usuario_nombre or '',
                    'fecha_modificacion': plan.fecha_modificacion
                })
            
            # Crear DataFrame
            df = pd.DataFrame(export_data)
            
            # Guardar archivo
            downloads_path = Path.home() / "Downloads"
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_path = downloads_path / f"planes_perdidas_{timestamp}.xlsx"
            
            df.to_excel(file_path, index=False, sheet_name="Planes de Pérdidas")
            
            self._show_success(f"Planes exportados a: {file_path}")
            
        except Exception as ex:
            self.logger.error(f"Error exportando a Excel: {ex}")
            self._show_error("Error al exportar los planes")
    
    def _show_success(self, message: str):
        """Muestra mensaje de éxito"""
        snack_bar = ft.SnackBar(
            content=ft.Text(message),
            bgcolor=ft.Colors.GREEN
        )
        self.page.snack_bar = snack_bar
        snack_bar.open = True
        self.page.update()
    
    def _show_error(self, message: str):
        """Muestra mensaje de error"""
        snack_bar = ft.SnackBar(
            content=ft.Text(message),
            bgcolor=ft.Colors.RED
        )
        self.page.snack_bar = snack_bar
        snack_bar.open = True
        self.page.update()
    
    def _show_warning(self, message: str):
        """Muestra mensaje de advertencia"""
        snack_bar = ft.SnackBar(
            content=ft.Text(message),
            bgcolor=ft.Colors.ORANGE
        )
        self.page.snack_bar = snack_bar
        snack_bar.open = True
        self.page.update()
