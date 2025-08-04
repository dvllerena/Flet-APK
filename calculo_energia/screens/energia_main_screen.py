"""
Pantalla principal del módulo de Cálculo de Energía
Versión WEB con importación por Copy/Paste desde Excel
"""

import flet as ft
from typing import List, Dict, Any
from datetime import datetime
from core.logger import get_logger
from calculo_energia.services.energia_service import EnergiaService
from calculo_energia.models.energia_barra_model import EnergiaBarra

class EnergiaMainScreen:
    """Pantalla principal de gestión de energía - VERSIÓN WEB MEJORADA"""
    
    def __init__(self, app):
        self.app = app
        self.page = app.page
        self.logger = get_logger(__name__)
        self.energia_service = EnergiaService()
        
        # Estado
        self.current_data: List[EnergiaBarra] = []
        self.filtered_data: List[EnergiaBarra] = []
        self.selected_año = datetime.now().year
        self.selected_mes = datetime.now().month
        self.search_text = ""
        self.is_loading = False
        
        # ✅ FilePicker según documentación oficial de Flet
        self.file_picker = ft.FilePicker(on_result=self._on_file_result)
        self.page.overlay.append(self.file_picker)
        
        # Cargar datos iniciales
        self._load_data()
        self._load_municipios()
    
    def build(self) -> ft.Control:
        """Construye la interfaz de la pantalla"""
        return ft.Container(
            content=ft.Column([
                self._build_header(),
                self._build_filters(),
                self._build_data_table(),
                self._build_footer()
            ], spacing=20),
            padding=20,
            expand=True
        )
    
    def _build_header(self) -> ft.Control:
        """Construye el encabezado"""
        return ft.Container(
            content=ft.Row([
                ft.Column([
                    ft.Text(
                        "Gestión de Energía por Municipio",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLUE_800
                    ),
                    ft.Text(
                        f"Período: {self.selected_mes:02d}/{self.selected_año}",
                        size=16,
                        color=ft.Colors.GREY_600
                    )
                ], expand=True),
                
                # Botones de acción
                ft.Row([
                    ft.ElevatedButton(
                        "Importar Datos",
                        icon=ft.Icons.UPLOAD,
                        on_click=self._on_import_click,
                        bgcolor=ft.Colors.GREEN_600,
                        color=ft.Colors.WHITE
                    ),
                    ft.ElevatedButton(
                        "Nuevo Registro",
                        icon=ft.Icons.ADD,
                        on_click=self._on_new_click,
                        bgcolor=ft.Colors.BLUE_600,
                        color=ft.Colors.WHITE
                    ),
                    ft.IconButton(
                        icon=ft.Icons.REFRESH,
                        tooltip="Actualizar datos",
                        on_click=self._on_refresh_click
                    )
                ])
            ]),
            bgcolor=ft.Colors.BLUE_50,
            padding=20,
            border_radius=10
        )
    
    def _build_filters(self) -> ft.Control:
        """Construye los filtros"""
        return ft.Container(
            content=ft.Row([
                # Selector de año
                ft.Dropdown(
                    label="Año",
                    value=str(self.selected_año),
                    options=[
                        ft.dropdown.Option(str(year)) 
                        for year in range(2020, 2030)
                    ],
                    width=100,
                    on_change=self._on_year_change
                ),
                
                # Selector de mes
                ft.Dropdown(
                    label="Mes",
                    value=str(self.selected_mes),
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
                        ft.dropdown.Option("12", "Diciembre")
                    ],
                    width=120,
                    on_change=self._on_month_change
                ),
                
                # Buscador
                ft.TextField(
                    label="Buscar municipio",
                    hint_text="Escriba para filtrar...",
                    prefix_icon=ft.Icons.SEARCH,
                    width=200,
                    on_change=self._on_search_change
                ),
                
                # Botón aplicar filtros
                ft.ElevatedButton(
                    "Aplicar",
                    icon=ft.Icons.FILTER_LIST,
                    on_click=self._on_apply_filters
                )
            ], alignment=ft.MainAxisAlignment.START),
            padding=ft.padding.symmetric(horizontal=10)
        )
    
    def _build_data_table(self) -> ft.Control:
        """Construye la tabla de datos"""
        if self.is_loading:
            return ft.Container(
                content=ft.Column([
                    ft.ProgressRing(),
                    ft.Text("Cargando datos...")
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                height=300,
                alignment=ft.alignment.center
            )
        
        if not self.filtered_data:
            return ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.INBOX, size=64, color=ft.Colors.GREY_400),
                    ft.Text(
                        "No hay datos para el período seleccionado",
                        size=16,
                        color=ft.Colors.GREY_600
                    ),
                    ft.Container(height=20),
                    ft.ElevatedButton(
                        "Importar Datos",
                        icon=ft.Icons.UPLOAD,
                        on_click=self._on_import_click
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                height=300,
                alignment=ft.alignment.center
            )
        
        # Crear filas de la tabla
        rows = []
        for i, record in enumerate(self.filtered_data):
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(i + 1))),
                        ft.DataCell(ft.Text(record.municipio_codigo)),
                        ft.DataCell(ft.Text(record.municipio_nombre)),
                        ft.DataCell(ft.Text(f"{record.energia_mwh:,.1f}")),
                        ft.DataCell(ft.Text(record.observaciones or "")),
                        ft.DataCell(
                            ft.Row([
                                ft.IconButton(
                                    icon=ft.Icons.VISIBILITY,
                                    tooltip="Ver",
                                    on_click=lambda e, r=record: self._on_view_click(r)
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.EDIT,
                                    tooltip="Editar",
                                    on_click=lambda e, r=record: self._on_edit_click(r)
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.DELETE,
                                    tooltip="Eliminar",
                                    on_click=lambda e, r=record: self._on_delete_click(r),
                                    icon_color=ft.Colors.RED_400
                                )
                            ])
                        )
                    ]
                )
            )
        
        return ft.Container(
            content=ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("#")),
                    ft.DataColumn(ft.Text("Código")),
                    ft.DataColumn(ft.Text("Municipio")),
                    ft.DataColumn(ft.Text("Energía (MWh)")),
                    ft.DataColumn(ft.Text("Observaciones")),
                    ft.DataColumn(ft.Text("Acciones"))
                ],
                rows=rows,
                border=ft.border.all(1, ft.Colors.GREY_300),
                border_radius=10,
                vertical_lines=ft.BorderSide(1, ft.Colors.GREY_200),
                horizontal_lines=ft.BorderSide(1, ft.Colors.GREY_200)
            ),
            bgcolor=ft.Colors.WHITE,
            padding=10,
            border_radius=10
        )
    
    def _build_footer(self) -> ft.Control:
        """Construye el pie de página con estadísticas"""
        total_registros = len(self.filtered_data)
        total_energia = sum(r.energia_mwh for r in self.filtered_data)
        promedio_energia = total_energia / total_registros if total_registros > 0 else 0
        
        return ft.Container(
            content=ft.Row([
                ft.Text(f"Total registros: {total_registros}"),
                ft.Text(f"Total energía: {total_energia:,.1f} MWh"),
                ft.Text(f"Promedio: {promedio_energia:,.1f} MWh")
            ], alignment=ft.MainAxisAlignment.SPACE_AROUND),
            bgcolor=ft.Colors.GREY_100,
            padding=15,
            border_radius=10
        )
    
    # ✅ EVENTOS DE INTERFAZ
    def _on_year_change(self, e):
        """Cambio de año"""
        self.selected_año = int(e.control.value)
        self._load_data()
    
    def _on_month_change(self, e):
        """Cambio de mes"""
        self.selected_mes = int(e.control.value)
        self._load_data()
    
    def _on_search_change(self, e):
        """Cambio en búsqueda"""
        self.search_text = e.control.value.lower()
        self._apply_filters()
    
    def _on_apply_filters(self, e):
        """Aplicar filtros"""
        self._load_data()
    
    def _on_refresh_click(self, e):
        """Actualizar datos"""
        self._load_data()
    
    def _on_new_click(self, e):
        """Crear nuevo registro"""
        self.app.navigate_to("energia_edit")
    
    def _on_view_click(self, record: EnergiaBarra):
        """Ver registro"""
        self.app.navigate_to("energia_view", record_id=record.id)
    
    def _on_edit_click(self, record: EnergiaBarra):
        """Editar registro"""
        self.app.navigate_to("energia_edit", record_id=record.id)
    
    def _on_delete_click(self, record: EnergiaBarra):
        """Eliminar registro"""
        self._show_delete_confirmation(record)
    
    # ✅ IMPORTACIÓN DE DATOS - VERSIÓN COPY/PASTE
    def _on_import_click(self, e):
        """Mostrar opciones de importación"""
        try:
            self.logger.info("Mostrando opciones de importación")
            self._show_import_options()
        except Exception as ex:
            self.logger.error(f"Error mostrando importación: {ex}")
            self._show_error("Error abriendo importación")
    
    def _show_import_options(self):
        """Muestra opciones de importación para web"""
        
        def close_dlg(e):
            dlg.open = False
            self.page.update()
        
        def option_paste(e):
            close_dlg(e)
            self._show_paste_import_dialog()
        
        def option_manual(e):
            close_dlg(e)
            self._show_manual_entry_dialog()
        
        def option_file(e):
            close_dlg(e)
            self._try_file_picker()
        
        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Importar Datos de Energía"),
            content=ft.Container(
                content=ft.Column([
                    ft.Text("Seleccione el método de importación:"),
                    ft.Divider(),
                    
                    # ✅ Opción 1: Pegar desde Excel (RECOMENDADA)
                    ft.Card(
                        content=ft.Container(
                            content=ft.ListTile(
                                leading=ft.Icon(ft.Icons.CONTENT_PASTE, color=ft.Colors.GREEN),
                                title=ft.Text("Pegar desde Excel"),
                                subtitle=ft.Text("Copiar y pegar datos desde Excel (Recomendado)"),
                                on_click=option_paste
                            ),
                            bgcolor=ft.Colors.GREEN_50
                        )
                    ),
                    
                    # Opción 2: Entrada manual
                    ft.Card(
                        content=ft.Container(
                            content=ft.ListTile(
                                leading=ft.Icon(ft.Icons.EDIT_NOTE, color=ft.Colors.BLUE),
                                title=ft.Text("Entrada Manual"),
                                subtitle=ft.Text("Formulario para todos los municipios"),
                                on_click=option_manual
                            )
                        )
                    ),
                    
                    # Opción 3: Archivo (limitado)
                    ft.Card(
                        content=ft.Container(
                            content=ft.ListTile(
                                leading=ft.Icon(ft.Icons.UPLOAD_FILE, color=ft.Colors.ORANGE),
                                title=ft.Text("Archivo Excel"),
                                subtitle=ft.Text("Limitado en navegadores web"),
                                on_click=option_file
                            ),
                            bgcolor=ft.Colors.ORANGE_50
                        )
                    )
                    
                ], tight=True),
                width=450,
                height=300,
                padding=20
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=close_dlg)
            ]
        )
        
        self.page.open(dlg)
    
    def _show_paste_import_dialog(self):
        """Diálogo para importar datos pegando desde Excel"""
        
        # ✅ TextField multiline según documentación de Flet
        text_input = ft.TextField(
            label="Datos desde Excel",
            hint_text="1. Abra su archivo Excel\n2. Seleccione los datos (incluya encabezados)\n3. Copie (Ctrl+C)\n4. Pegue aquí (Ctrl+V)",
            multiline=True,
            min_lines=8,
            max_lines=15,
            width=600,
            expand=True
        )
        
        # Área de instrucciones
        instructions = ft.Container(
            content=ft.Column([
                ft.Text("📋 INSTRUCCIONES:", weight=ft.FontWeight.BOLD),
                ft.Text("1. Abra su archivo Excel"),
                ft.Text("2. Seleccione las columnas: Municipio | Energía | Observaciones"),
                ft.Text("3. Copie los datos (Ctrl+C)"),
                ft.Text("4. Pegue en el campo de abajo (Ctrl+V)"),
                ft.Text("5. Haga clic en 'Procesar Datos'"),
                ft.Divider(),
                ft.Text("📝 FORMATO ESPERADO:", weight=ft.FontWeight.BOLD),
                ft.Text("Municipio\tEnergía\tObservaciones"),
                ft.Text("Matanzas\t145.5\tDatos enero"),
                ft.Text("Cárdenas\t120.3\tDatos enero"),
                ft.Text("...", color=ft.Colors.GREY_600)
            ], tight=True),
            bgcolor=ft.Colors.BLUE_50,
            padding=15,
            border_radius=8,
            border=ft.border.all(1, ft.Colors.BLUE_200)
        )
        
        def close_dlg(e):
            dlg.open = False
            self.page.update()
        
        def process_data(e):
            if text_input.value and text_input.value.strip():
                self._process_pasted_data(text_input.value)
                close_dlg(e)
            else:
                self._show_error("Por favor, pegue los datos primero")
        
        def show_example(e):
            # Mostrar ejemplo de formato
            example_text = "Municipio\tEnergía\tObservaciones\nMatanzas\t145.5\tDatos de ejemplo\nCárdenas\t120.3\tDatos de ejemplo\nMartí\t98.7\tDatos de ejemplo"
            text_input.value = example_text
            self.page.update()
        
        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Importar Pegando Datos desde Excel"),
            content=ft.Container(
                content=ft.Column([
                    instructions,
                    ft.Container(height=10),
                    text_input,
                    ft.Container(height=10),
                    ft.Row([
                        ft.TextButton(
                            "Ver Ejemplo",
                            icon=ft.Icons.VISIBILITY,
                            on_click=show_example
                        ),
                        ft.ElevatedButton(
                            "Procesar Datos",
                            icon=ft.Icons.PLAY_ARROW,
                            on_click=process_data
                        )
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                ], scroll=ft.ScrollMode.AUTO),
                width=700,
                height=500,
                padding=20
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=close_dlg)
            ]
        )
        
        self.page.open(dlg)
    
    def _process_pasted_data(self, text_data: str):
        """Procesa datos pegados desde Excel"""
        try:
            self.logger.info("Procesando datos pegados desde Excel")
            
            # ✅ Mostrar diálogo de progreso
            self._show_processing_dialog("Procesando datos pegados...")
            
            # Procesar líneas
            lines = text_data.strip().split('\n')
            if len(lines) < 2:
                self._hide_processing_dialog()
                self._show_error("Se requieren al menos 2 líneas (encabezado + datos)")
                return
            
            # Detectar separador (tab o coma)
            separator = '\t' if '\t' in lines[0] else ','
            
            # Procesar encabezado
            headers = [h.strip().lower() for h in lines[0].split(separator)]
            self.logger.info(f"Encabezados detectados: {headers}")
            
            # Mapear columnas
            column_mapping = self._map_columns(headers)
            if not column_mapping['success']:
                self._hide_processing_dialog()
                self._show_error(column_mapping['message'])
                return
            
            # Procesar datos
            result = self._process_data_lines(lines[1:], separator, column_mapping['mapping'])
            
            self._hide_processing_dialog()
            
            if result['success']:
                self._show_success(f"✅ {result['message']}")
                self._load_data()  # Recargar datos
            else:
                self._show_error(f"❌ {result['message']}")
                
        except Exception as e:
            self._hide_processing_dialog()
            self.logger.error(f"Error procesando datos pegados: {e}")
            self._show_error(f"Error procesando datos: {str(e)}")
    
    def _map_columns(self, headers: List[str]) -> Dict[str, Any]:
        """Mapea las columnas del encabezado"""
        try:
            # Mapeo de posibles nombres de columnas
            column_patterns = {
                'municipio': ['municipio', 'municipios', 'ciudad', 'localidad', 'nombre'],
                'energia': ['energia', 'energía', 'mwh', 'energia_mwh', 'consumo', 'kwh'],
                'observaciones': ['observaciones', 'observacion', 'obs', 'notas', 'comentarios']
            }
            
            mapping = {}
            
            # Buscar columna de municipio (obligatoria)
            municipio_col = None
            for i, header in enumerate(headers):
                if any(pattern in header for pattern in column_patterns['municipio']):
                    municipio_col = i
                    mapping['municipio'] = i
                    break
            
            if municipio_col is None:
                return {
                    'success': False,
                    'message': f"No se encontró columna de municipio. Columnas disponibles: {headers}"
                }
            
            # Buscar columna de energía (obligatoria)
            energia_col = None
            for i, header in enumerate(headers):
                if any(pattern in header for pattern in column_patterns['energia']):
                    energia_col = i
                    mapping['energia'] = i
                    break
            
            if energia_col is None:
                return {
                    'success': False,
                    'message': f"No se encontró columna de energía. Columnas disponibles: {headers}"
                }
            
            # Buscar columna de observaciones (opcional)
            for i, header in enumerate(headers):
                if any(pattern in header for pattern in column_patterns['observaciones']):
                    mapping['observaciones'] = i
                    break
            
            self.logger.info(f"Mapeo de columnas: {mapping}")
            
            return {
                'success': True,
                'mapping': mapping
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f"Error mapeando columnas: {str(e)}"
            }
    
    def _process_data_lines(self, data_lines: List[str], separator: str, column_mapping: Dict[str, int]) -> Dict[str, Any]:
        """Procesa las líneas de datos"""
        try:
            # Obtener municipios para validación
            municipios = self.energia_service.get_municipios()
            municipios_dict = {m['nombre'].lower(): m['id'] for m in municipios}
            municipios_dict.update({m['codigo'].lower(): m['id'] for m in municipios})
            
            imported_count = 0
            error_count = 0
            errors = []
            updated_count = 0
            
            for line_num, line in enumerate(data_lines, start=2):  # Empezar en 2 (después del encabezado)
                try:
                    if not line.strip():
                        continue  # Saltar líneas vacías
                    
                    # Dividir la línea
                    columns = line.split(separator)
                    
                    if len(columns) < len(column_mapping):
                        error_count += 1
                        errors.append(f"Línea {line_num}: Faltan columnas")
                        continue
                    
                    # Extraer datos
                    municipio_text = columns[column_mapping['municipio']].strip()
                    energia_text = columns[column_mapping['energia']].strip()
                    
                    # Observaciones (opcional)
                    observaciones = None
                    if 'observaciones' in column_mapping and len(columns) > column_mapping['observaciones']:
                        obs_text = columns[column_mapping['observaciones']].strip()
                        if obs_text and obs_text.lower() not in ['', 'nan', 'none']:
                            observaciones = obs_text
                    
                    # Validar municipio
                    municipio_id = self._find_municipio_id(municipio_text, municipios_dict)
                    if not municipio_id:
                        error_count += 1
                        errors.append(f"Línea {line_num}: Municipio no encontrado: {municipio_text}")
                        continue
                    
                    # Validar energía
                    try:
                        energia_value = float(energia_text.replace(',', '.'))  # Manejar decimales con coma
                        if energia_value < 0:
                            error_count += 1
                            errors.append(f"Línea {line_num}: Energía no puede ser negativa: {energia_value}")
                            continue
                    except ValueError:
                        error_count += 1
                        errors.append(f"Línea {line_num}: Energía inválida: {energia_text}")
                        continue
                    
                    # Crear registro
                    data = {
                        "municipio_id": municipio_id,
                        "año": self.selected_año,
                        "mes": self.selected_mes,
                        "energia_mwh": energia_value,
                        "observaciones": observaciones,
                        "usuario_id": self.app.get_current_user()["id"]
                    }
                    
                    # Verificar si existe
                    existing = self._check_existing_record(municipio_id, self.selected_año, self.selected_mes)
                    
                    if existing:
                        # Actualizar existente
                        if self.energia_service.actualizar_energia(existing["id"], data):
                            updated_count += 1
                            imported_count += 1
                        else:
                            error_count += 1
                            errors.append(f"Línea {line_num}: Error actualizando registro existente")
                    else:
                        # Crear nuevo
                        if self.energia_service.crear_energia(data):
                            imported_count += 1
                        else:
                            error_count += 1
                            errors.append(f"Línea {line_num}: Error creando registro")
                
                except Exception as e:
                    error_count += 1
                    errors.append(f"Línea {line_num}: {str(e)}")
            
            # Resultado
            success = imported_count > 0
            message = f"Procesados: {imported_count} registros"
            
            if updated_count > 0:
                message += f" ({updated_count} actualizados, {imported_count - updated_count} nuevos)"
            
            if error_count > 0:
                message += f", {error_count} errores"
            
            self.logger.info(f"Importación completada: {imported_count} importados, {error_count} errores")
            
            return {
                'success': success,
                'message': message,
                'imported': imported_count,
                'errors': error_count,
                'error_details': errors[:5]  # Solo primeros 5 errores
            }
            
        except Exception as e:
            self.logger.error(f"Error procesando líneas de datos: {e}")
            return {
                'success': False,
                'message': f"Error procesando datos: {str(e)}"
            }
    
    def _find_municipio_id(self, municipio_text: str, municipios_dict: Dict[str, int]) -> int:
        """Busca el ID del municipio por nombre o código"""
        municipio_lower = municipio_text.lower().strip()
        
        # Búsqueda exacta
        if municipio_lower in municipios_dict:
            return municipios_dict[municipio_lower]
        
        # Búsqueda parcial
        for nombre, mid in municipios_dict.items():
            if municipio_lower in nombre or nombre in municipio_lower:
                return mid
        
        return None
    
    def _check_existing_record(self, municipio_id: int, año: int, mes: int) -> Dict[str, Any]:
        """Verifica si existe un registro"""
        try:
            records = self.energia_service.get_energia_by_periodo(año, mes)
            for record in records:
                if record.municipio_id == municipio_id:
                    return {"id": record.id}
            return None
        except:
            return None
    
    # ✅ ENTRADA MANUAL MASIVA
    def _show_manual_entry_dialog(self):
        """Diálogo para entrada manual masiva"""
        
        municipios = self.energia_service.get_municipios()
        if not municipios:
            self._show_error("No hay municipios disponibles")
            return
        
        # Crear campos para cada municipio
        energia_fields = {}
        obs_fields = {}
        municipio_rows = []
        
        for municipio in municipios:
            energia_field = ft.TextField(
                hint_text="0.0",
                width=100,
                keyboard_type=ft.KeyboardType.NUMBER,
                text_align=ft.TextAlign.RIGHT
            )
            
            obs_field = ft.TextField(
                hint_text="Observaciones...",
                width=150
            )
            
            energia_fields[municipio["id"]] = energia_field
            obs_fields[municipio["id"]] = obs_field
            
            municipio_rows.append(
                ft.Row([
                    ft.Container(
                        content=ft.Text(municipio["nombre"]),
                        width=120
                    ),
                    ft.Container(
                        content=ft.Text(municipio["codigo"]),
                        width=60
                    ),
                    energia_field,
                    obs_field
                ], alignment=ft.MainAxisAlignment.START)
            )
        
        def close_dlg(e):
            dlg.open = False
            self.page.update()
        
        def save_all(e):
            self._save_manual_data(energia_fields, obs_fields)
            close_dlg(e)
        
        def clear_all(e):
            for field in energia_fields.values():
                field.value = ""
            for field in obs_fields.values():
                field.value = ""
            self.page.update()
        
        def fill_example(e):
            # Llenar con datos de ejemplo
            import random
            for municipio_id, field in energia_fields.items():
                field.value = str(round(random.uniform(80, 200), 1))
            self.page.update()
        
        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"Entrada Manual - {self.selected_mes:02d}/{self.selected_año}"),
            content=ft.Container(
                content=ft.Column([
                    ft.Text("Ingrese la energía para cada municipio:"),
                    ft.Divider(),
                    
                    # Header
                    ft.Row([
                        ft.Container(ft.Text("Municipio", weight=ft.FontWeight.BOLD), width=120),
                        ft.Container(ft.Text("Código", weight=ft.FontWeight.BOLD), width=60),
                        ft.Container(ft.Text("Energía (MWh)", weight=ft.FontWeight.BOLD), width=100),
                        ft.Container(ft.Text("Observaciones", weight=ft.FontWeight.BOLD), width=150)
                    ]),
                    ft.Divider(),
                    
                    # Campos de municipios
                    ft.Container(
                        content=ft.Column(municipio_rows, scroll=ft.ScrollMode.AUTO),
                        height=300
                    ),
                    
                    ft.Row([
                        ft.TextButton("Limpiar", on_click=clear_all),
                        ft.TextButton("Ejemplo", on_click=fill_example),
                        ft.ElevatedButton("Guardar Todo", on_click=save_all)
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                    
                ], scroll=ft.ScrollMode.AUTO),
                width=600,
                height=500,
                padding=20
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=close_dlg)
            ]
        )
        
        self.page.open(dlg)
    
    def _save_manual_data(self, energia_fields: Dict, obs_fields: Dict):
        """Guarda datos de entrada manual"""
        try:
            self._show_processing_dialog("Guardando datos...")
            
            saved_count = 0
            error_count = 0
            errors = []
            
            for municipio_id in energia_fields.keys():
                energia_field = energia_fields[municipio_id]
                obs_field = obs_fields[municipio_id]
                
                if energia_field.value and energia_field.value.strip():
                    try:
                        energia = float(energia_field.value.replace(',', '.'))
                        
                        if energia < 0:
                            error_count += 1
                            errors.append(f"Energía negativa para municipio ID {municipio_id}")
                            continue
                        
                        observaciones = obs_field.value.strip() if obs_field.value else None
                        if observaciones and observaciones.lower() in ['', 'nan', 'none']:
                            observaciones = None
                        
                        data = {
                            "municipio_id": municipio_id,
                            "año": self.selected_año,
                            "mes": self.selected_mes,
                            "energia_mwh": energia,
                            "observaciones": observaciones,
                            "usuario_id": self.app.get_current_user()["id"]
                        }
                        
                        # Verificar si existe
                        existing = self._check_existing_record(municipio_id, self.selected_año, self.selected_mes)
                        
                        if existing:
                            if self.energia_service.actualizar_energia(existing["id"], data):
                                saved_count += 1
                            else:
                                error_count += 1
                                errors.append(f"Error actualizando municipio ID {municipio_id}")
                        else:
                            if self.energia_service.crear_energia(data):
                                saved_count += 1
                            else:
                                error_count += 1
                                errors.append(f"Error creando registro para municipio ID {municipio_id}")
                                
                    except ValueError:
                        error_count += 1
                        errors.append(f"Valor inválido para municipio ID {municipio_id}: {energia_field.value}")
            
            self._hide_processing_dialog()
            
            if saved_count > 0:
                self._show_success(f"✅ Guardados {saved_count} registros")
                self._load_data()
            
            if error_count > 0:
                error_msg = f"❌ {error_count} errores"
                if errors:
                    error_msg += f": {'; '.join(errors[:3])}"
                    if len(errors) > 3:
                        error_msg += f" y {len(errors)-3} más"
                self._show_error(error_msg)
                
        except Exception as e:
            self._hide_processing_dialog()
            self.logger.error(f"Error guardando datos manuales: {e}")
            self._show_error(f"Error guardando datos: {str(e)}")
    
    # ✅ FILEPICKER COMO FALLBACK
    def _try_file_picker(self):
        """Intenta usar FilePicker (limitado en web)"""
        try:
            self.file_picker.pick_files(
                dialog_title="Seleccionar archivo Excel (Limitado en Web)",
                file_type=ft.FilePickerFileType.CUSTOM,
                allowed_extensions=["xlsx", "xls"]
            )
        except Exception as e:
            self.logger.error(f"Error con FilePicker: {e}")
            self._show_error("FilePicker no disponible en este navegador")
    
    def _on_file_result(self, e: ft.FilePickerResultEvent):
        """Resultado del FilePicker - LIMITADO EN WEB"""
        try:
            if e.files:
                file_info = e.files[0]
                self.logger.info(f"Archivo seleccionado: {file_info.name}")
                
                # En web, mostrar limitaciones
                self._show_file_limitation_dialog(file_info)
            else:
                self.logger.info("No se seleccionó archivo")
                
        except Exception as ex:
            self.logger.error(f"Error con archivo: {ex}")
            self._show_error("Error procesando archivo seleccionado")
    
    def _show_file_limitation_dialog(self, file_info):
        """Explica las limitaciones del FilePicker en web"""
        
        def close_dlg(e):
            dlg.open = False
            self.page.update()
        
        def try_paste_instead(e):
            close_dlg(e)
            self._show_paste_import_dialog()
        
        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Archivo Seleccionado"),
            content=ft.Container(
                content=ft.Column([
                    ft.Text(f"📄 Archivo: {file_info.name}"),
                    ft.Text(f"📊 Tamaño: {file_info.size} bytes"),
                    ft.Divider(),
                    
                    ft.Icon(ft.Icons.WARNING, color=ft.Colors.ORANGE, size=48),
                    ft.Text(
                        "⚠️ Limitación del Navegador Web",
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.ORANGE
                    ),
                    ft.Text(
                        "Los navegadores web no permiten leer el contenido de archivos directamente por razones de seguridad.",
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Container(height=10),
                    ft.Text(
                        "💡 Solución Recomendada:",
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLUE
                    ),
                    ft.Text(
                        "1. Abra su archivo Excel\n2. Seleccione y copie los datos\n3. Use la opción 'Pegar desde Excel'",
                        text_align=ft.TextAlign.LEFT
                    ),
                    
                    ft.Container(height=20),
                    ft.ElevatedButton(
                        "Usar Método de Pegado",
                        icon=ft.Icons.CONTENT_PASTE,
                        on_click=try_paste_instead
                    )
                    
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                width=400,
                padding=20
            ),
            actions=[
                ft.TextButton("Entendido", on_click=close_dlg)
            ]
        )
        
        self.page.open(dlg)
    
    # ✅ MÉTODOS DE CARGA Y FILTRADO
    def _load_data(self):
        """Carga los datos del período seleccionado"""
        try:
            self.is_loading = True
            self.page.update()
            
            self.logger.info(f"Cargando datos para {self.selected_año}-{self.selected_mes:02d}")
            
            # Obtener datos del servicio
            records = self.energia_service.get_energia_by_periodo(self.selected_año, self.selected_mes)
            
            # Convertir a objetos EnergiaBarra
            self.current_data = []
            for record in records:
                energia_obj = EnergiaBarra(
                    id=record.id,
                    municipio_id=record.municipio_id,
                    municipio_nombre=record.municipio_nombre,
                    municipio_codigo=record.municipio_codigo,
                    año=record.año,
                    mes=record.mes,
                    energia_mwh=record.energia_mwh,
                    observaciones=record.observaciones,
                    usuario_id=record.usuario_id,
                    fecha_registro=record.fecha_registro,
                    fecha_modificacion=record.fecha_modificacion
                )
                self.current_data.append(energia_obj)
            
            # Aplicar filtros
            self._apply_filters()
            
            self.is_loading = False
            self.page.update()
            
            self.logger.info(f"Cargados {len(self.current_data)} registros")
            
        except Exception as e:
            self.is_loading = False
            self.logger.error(f"Error cargando datos: {e}")
            self._show_error(f"Error cargando datos: {str(e)}")
            self.page.update()
    
    def _apply_filters(self):
        """Aplica filtros a los datos"""
        try:
            self.filtered_data = self.current_data.copy()
            
            # Filtro de búsqueda
            if self.search_text:
                self.filtered_data = [
                    record for record in self.filtered_data
                    if (self.search_text in record.municipio_nombre.lower() or
                        self.search_text in record.municipio_codigo.lower())
                ]
            
            self.logger.info(f"Filtros aplicados: {len(self.filtered_data)} registros")
            
        except Exception as e:
            self.logger.error(f"Error aplicando filtros: {e}")
    
    def _load_municipios(self):
        """Carga la lista de municipios"""
        try:
            municipios = self.energia_service.get_municipios()
            self.logger.info(f"Cargados {len(municipios)} municipios")
        except Exception as e:
            self.logger.error(f"Error cargando municipios: {e}")
    
    # ✅ DIÁLOGOS DE CONFIRMACIÓN Y MENSAJES
    def _show_delete_confirmation(self, record: EnergiaBarra):
        """Muestra confirmación de eliminación"""
        
        def close_dlg(e):
            dlg.open = False
            self.page.update()
        
        def confirm_delete(e):
            close_dlg(e)
            self._delete_record(record)
        
        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmar Eliminación"),
            content=ft.Text(
                f"¿Está seguro de eliminar el registro de energía de {record.municipio_nombre} "
                f"para {record.mes:02d}/{record.año}?\n\n"
                f"Energía: {record.energia_mwh:,.1f} MWh\n"
                f"Esta acción no se puede deshacer."
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=close_dlg),
                ft.ElevatedButton(
                    "Eliminar",
                    bgcolor=ft.Colors.RED_600,
                    color=ft.Colors.WHITE,
                    on_click=confirm_delete
                )
            ]
        )
        
        self.page.open(dlg)
    
    def _delete_record(self, record: EnergiaBarra):
        """Elimina un registro"""
        try:
            if self.energia_service.eliminar_energia(record.id):
                self._show_success(f"✅ Registro eliminado: {record.municipio_nombre}")
                self._load_data()
            else:
                self._show_error("❌ Error eliminando registro")
        except Exception as e:
            self.logger.error(f"Error eliminando registro: {e}")
            self._show_error(f"Error eliminando registro: {str(e)}")
    
    # ✅ DIÁLOGOS DE PROGRESO Y MENSAJES
    def _show_processing_dialog(self, message: str = "Procesando..."):
        """Muestra diálogo de procesamiento"""
        self.processing_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Procesando"),
            content=ft.Container(
                content=ft.Column([
                    ft.ProgressRing(),
                    ft.Text(message)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                width=200,
                height=100,
                alignment=ft.alignment.center
            )
        )
        
        self.page.dialog = self.processing_dialog
        self.processing_dialog.open = True
        self.page.update()
    
    def _hide_processing_dialog(self):
        """Oculta diálogo de procesamiento"""
        if hasattr(self, 'processing_dialog'):
            self.processing_dialog.open = False
            self.page.update()
    
    def _show_success(self, message: str):
        """Muestra mensaje de éxito"""
        def close_snack(e):
            self.page.snack_bar.open = False
            self.page.update()
        
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(message),
            bgcolor=ft.Colors.GREEN_600,
            action="Cerrar",
            action_color=ft.Colors.WHITE,
            on_action=close_snack
        )
        self.page.snack_bar.open = True
        self.page.update()
    
    def _show_error(self, message: str):
        """Muestra mensaje de error"""
        def close_snack(e):
            self.page.snack_bar.open = False
            self.page.update()
        
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(message),
            bgcolor=ft.Colors.RED_600,
            action="Cerrar",
            action_color=ft.Colors.WHITE,
            on_action=close_snack
        )
        self.page.snack_bar.open = True
        self.page.update()
    
    def _show_info(self, message: str):
        """Muestra mensaje informativo"""
        def close_snack(e):
            self.page.snack_bar.open = False
            self.page.update()
        
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(message),
            bgcolor=ft.Colors.BLUE_600,
            action="Cerrar",
            action_color=ft.Colors.WHITE,
            on_action=close_snack
        )
        self.page.snack_bar.open = True
        self.page.update()
    
    # ✅ MÉTODOS ADICIONALES DE UTILIDAD
    def _export_current_data(self):
        """Exporta los datos actuales (funcionalidad futura)"""
        try:
            if not self.filtered_data:
                self._show_error("No hay datos para exportar")
                return
            
            # Por ahora, mostrar información de exportación
            self._show_export_info_dialog()
            
        except Exception as e:
            self.logger.error(f"Error exportando datos: {e}")
            self._show_error("Error exportando datos")
    
    def _show_export_info_dialog(self):
        """Muestra información sobre exportación"""
        
        def close_dlg(e):
            dlg.open = False
            self.page.update()
        
        def copy_data(e):
            # Crear texto para copiar
            export_text = "Municipio\tCódigo\tEnergía (MWh)\tObservaciones\n"
            for record in self.filtered_data:
                export_text += f"{record.municipio_nombre}\t{record.municipio_codigo}\t{record.energia_mwh}\t{record.observaciones or ''}\n"
            
            # En una aplicación real, aquí se copiaría al clipboard
            self._show_info("Datos preparados para copiar (funcionalidad en desarrollo)")
            close_dlg(e)
        
        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Exportar Datos"),
            content=ft.Container(
                content=ft.Column([
                    ft.Text(f"📊 Registros a exportar: {len(self.filtered_data)}"),
                    ft.Text(f"📅 Período: {self.selected_mes:02d}/{self.selected_año}"),
                    ft.Divider(),
                    
                    ft.Text("Opciones de exportación:", weight=ft.FontWeight.BOLD),
                    ft.Text("• Copiar datos al portapapeles"),
                    ft.Text("• Generar archivo CSV (próximamente)"),
                    ft.Text("• Exportar a Excel (próximamente)"),
                    
                    ft.Container(height=20),
                    ft.ElevatedButton(
                        "Copiar Datos",
                        icon=ft.Icons.COPY,
                        on_click=copy_data
                    )
                ]),
                width=350,
                padding=20
            ),
            actions=[
                ft.TextButton("Cerrar", on_click=close_dlg)
            ]
        )
        
        self.page.open(dlg)
    
    def _show_statistics_dialog(self):
        """Muestra estadísticas del período actual"""
        try:
            if not self.filtered_data:
                self._show_error("No hay datos para mostrar estadísticas")
                return
            
            # Calcular estadísticas
            total_registros = len(self.filtered_data)
            total_energia = sum(r.energia_mwh for r in self.filtered_data)
            promedio_energia = total_energia / total_registros if total_registros > 0 else 0
            max_energia = max(r.energia_mwh for r in self.filtered_data) if self.filtered_data else 0
            min_energia = min(r.energia_mwh for r in self.filtered_data) if self.filtered_data else 0
            
            # Municipio con mayor y menor consumo
            municipio_max = max(self.filtered_data, key=lambda x: x.energia_mwh) if self.filtered_data else None
            municipio_min = min(self.filtered_data, key=lambda x: x.energia_mwh) if self.filtered_data else None
            
            def close_dlg(e):
                dlg.open = False
                self.page.update()
            
            dlg = ft.AlertDialog(
                modal=True,
                title=ft.Text(f"Estadísticas - {self.selected_mes:02d}/{self.selected_año}"),
                content=ft.Container(
                    content=ft.Column([
                        # Estadísticas generales
                        ft.Card(
                            content=ft.Container(
                                content=ft.Column([
                                    ft.Text("📊 Estadísticas Generales", weight=ft.FontWeight.BOLD),
                                    ft.Text(f"Total registros: {total_registros}"),
                                    ft.Text(f"Total energía: {total_energia:,.1f} MWh"),
                                    ft.Text(f"Promedio: {promedio_energia:,.1f} MWh"),
                                    ft.Text(f"Máximo: {max_energia:,.1f} MWh"),
                                    ft.Text(f"Mínimo: {min_energia:,.1f} MWh")
                                ]),
                                padding=15
                            )
                        ),
                        
                        # Extremos
                        ft.Card(
                            content=ft.Container(
                                content=ft.Column([
                                    ft.Text("🏆 Extremos", weight=ft.FontWeight.BOLD),
                                    ft.Text(f"Mayor consumo: {municipio_max.municipio_nombre} ({municipio_max.energia_mwh:,.1f} MWh)" if municipio_max else "N/A"),
                                    ft.Text(f"Menor consumo: {municipio_min.municipio_nombre} ({municipio_min.energia_mwh:,.1f} MWh)" if municipio_min else "N/A")
                                ]),
                                padding=15
                            )
                        )
                    ]),
                    width=400,
                    height=300,
                    padding=20
                ),
                actions=[
                    ft.TextButton("Cerrar", on_click=close_dlg)
                ]
            )
            
            self.page.open(dlg)
            
        except Exception as e:
            self.logger.error(f"Error mostrando estadísticas: {e}")
            self._show_error("Error calculando estadísticas")
    
    # ✅ MÉTODOS DE NAVEGACIÓN MEJORADOS
    def _build_action_buttons(self) -> ft.Control:
        """Construye botones de acción adicionales"""
        return ft.Container(
            content=ft.Row([
                ft.ElevatedButton(
                    "Estadísticas",
                    icon=ft.Icons.ANALYTICS,
                    on_click=lambda e: self._show_statistics_dialog(),
                    bgcolor=ft.Colors.PURPLE_600,
                    color=ft.Colors.WHITE
                ),
                ft.ElevatedButton(
                    "Exportar",
                    icon=ft.Icons.DOWNLOAD,
                    on_click=lambda e: self._export_current_data(),
                    bgcolor=ft.Colors.ORANGE_600,
                    color=ft.Colors.WHITE
                ),
                ft.ElevatedButton(
                    "Ayuda",
                    icon=ft.Icons.HELP,
                    on_click=lambda e: self._show_help_dialog(),
                    bgcolor=ft.Colors.GREY_600,
                    color=ft.Colors.WHITE
                )
            ], alignment=ft.MainAxisAlignment.END),
            padding=ft.padding.symmetric(horizontal=10)
        )
    
    def _show_help_dialog(self):
        """Muestra diálogo de ayuda"""
        
        def close_dlg(e):
            dlg.open = False
            self.page.update()
        
        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Ayuda - Gestión de Energía"),
            content=ft.Container(
                content=ft.Column([
                    ft.Text("📋 IMPORTAR DATOS DESDE EXCEL:", weight=ft.FontWeight.BOLD),
                    ft.Text("1. Haga clic en 'Importar Datos'"),
                    ft.Text("2. Seleccione 'Pegar desde Excel'"),
                    ft.Text("3. En Excel: seleccione datos y copie (Ctrl+C)"),
                    ft.Text("4. Pegue en el campo de texto (Ctrl+V)"),
                    ft.Text("5. Haga clic en 'Procesar Datos'"),
                    ft.Divider(),
                    
                    ft.Text("📝 FORMATO REQUERIDO:", weight=ft.FontWeight.BOLD),
                    ft.Text("Municipio | Energía | Observaciones"),
                    ft.Text("Matanzas | 145.5 | Datos enero"),
                    ft.Text("Cárdenas | 120.3 | Datos enero"),
                    ft.Divider(),
                    
                    ft.Text("🔧 FUNCIONES DISPONIBLES:", weight=ft.FontWeight.BOLD),
                    ft.Text("• Importar: Pegar datos o entrada manual"),
                    ft.Text("• Filtrar: Por año, mes y búsqueda"),
                    ft.Text("• Editar: Modificar registros individuales"),
                    ft.Text("• Estadísticas: Ver resumen del período"),
                    ft.Text("• Exportar: Copiar datos (en desarrollo)")
                ], scroll=ft.ScrollMode.AUTO),
                width=500,
                height=400,
                padding=20
            ),
            actions=[
                ft.TextButton("Cerrar", on_click=close_dlg)
            ]
        )
        
        self.page.open(dlg)
    
    # ✅ ACTUALIZAR BUILD PARA INCLUIR BOTONES ADICIONALES
    def build(self) -> ft.Control:
        """Construye la interfaz de la pantalla - VERSIÓN COMPLETA"""
        return ft.Container(
            content=ft.Column([
                self._build_header(),
                self._build_filters(),
                self._build_action_buttons(),  # ✅ Botones adicionales
                self._build_data_table(),
                self._build_footer()
            ], spacing=15),
            padding=20,
            expand=True
        )
    
    # ✅ MÉTODO DE LIMPIEZA
    def cleanup(self):
        """Limpia recursos al salir de la pantalla"""
        try:
            # Cerrar diálogos abiertos
            if hasattr(self, 'processing_dialog') and self.processing_dialog:
                self.processing_dialog.open = False
            
            # Limpiar snackbars
            if self.page.snack_bar:
                self.page.snack_bar.open = False
            
            # Limpiar diálogos
            if self.page.dialog:
                self.page.dialog.open = False
            
            self.page.update()
            self.logger.info("Pantalla de energía limpiada")
            
        except Exception as e:
            self.logger.error(f"Error limpiando pantalla: {e}")
    
    def __del__(self):
        """Destructor"""
        try:
            self.cleanup()
        except:
            pass


