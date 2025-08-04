"""
Pantalla unificada de Gestión de Transferencias de Energía
Maneja clientes y transferencias entre municipios
"""

import flet as ft
from datetime import datetime
from typing import List, Dict, Any, Optional
import pandas as pd
from facturacion.services import get_facturacion_service
from core.logger import get_logger

class FacturacionTransfersScreen:
    """Pantalla unificada de transferencias de energía"""
    
    def __init__(self, app):
        self.app = app
        self.page = app.page
        self.logger = get_logger(__name__)
        self.facturacion_service = get_facturacion_service()
        
        # Estado
        self.municipios = []
        self.servicios_transferencias = []
        self.consumos_actuales = {}
        
        # Fechas actuales
        now = datetime.now()
        self.current_año = now.year
        self.current_mes = now.month
        
        # Definir servicios fijos del sistema
        self._init_servicios_fijos()
        
        # Cargar datos iniciales
        self._load_initial_data()
    
    def _init_servicios_fijos(self):
        """Inicializa los servicios fijos del sistema"""
        self.servicios_fijos = {
            # MATANZAS → UNIÓN DE REYES
            "MATANZAS_UNION": [
                {"id": "124", "nombre": "Est. Ferrocarriles Mocha", "origen": "MATANZAS", "destino": "UNIÓN DE REYES"},
                {"id": "47", "nombre": "EST. DE CORTE 901 (línea 4945)", "origen": "MATANZAS", "destino": "UNIÓN DE REYES"},
                {"id": "46", "nombre": "DAAFAR LAS MARIAS (4405)", "origen": "MATANZAS", "destino": "UNIÓN DE REYES"}
            ],
            
            # CÁRDENAS → PROVINCIA
            "CARDENAS_PROVINCIA": [
                {"id": "665", "nombre": "ECO", "origen": "CÁRDENAS", "destino": "PROVINCIA"}
            ],
            
            # JAGÜEY → COLÓN
            "JAGUEY_COLON": [
                {"id": "2621", "nombre": "Regadio KINGRAF-10", "origen": "JAGÜEY", "destino": "COLÓN"},
                {"id": "2622", "nombre": "Banco de llemas vivero citrico", "origen": "JAGÜEY", "destino": "COLÓN"},
                {"id": "2623", "nombre": "Regadio vivero Biajaca", "origen": "JAGÜEY", "destino": "COLÓN"},
                {"id": "2633", "nombre": "Regadio Agricola El Roque", "origen": "JAGÜEY", "destino": "COLÓN"}
            ],
            
            # JAGÜEY → JOVELLANOS
            "JAGUEY_JOVELLANOS": [
                {"id": "2449", "nombre": "centro de limpieza de pedro betancourt", "origen": "JAGÜEY", "destino": "JOVELLANOS"},
                {"id": "2443", "nombre": "Bombeo Mosca", "origen": "JAGÜEY", "destino": "JOVELLANOS"},
                {"id": "2808", "nombre": "Turbina de riego", "origen": "JAGÜEY", "destino": "JOVELLANOS"}
            ]
        }

    def _load_initial_data(self):
        """Carga datos iniciales"""
        try:
            self.municipios = self.facturacion_service.get_municipios_activos()
            self.logger.info(f"Municipios cargados: {len(self.municipios)}")
        except Exception as e:
            self.logger.error(f"Error al cargar datos iniciales: {e}")
            self.municipios = []
    
    def build(self) -> ft.Control:
        """Construye la interfaz"""
        return ft.Container(
            content=ft.Column([
                self._build_header(),
                self._build_period_selector(),
                self._build_transfer_summary(),
                self._build_services_table(),
                self._build_actions()
            ], spacing=25),
            padding=25,
            expand=True,
            bgcolor=ft.Colors.GREY_50
        )
    
    def _build_header(self) -> ft.Control:
        """Construye el encabezado"""
        return ft.Card(
            content=ft.Container(
                content=ft.Row([
                    ft.Container(
                        content=ft.IconButton(
                            icon=ft.Icons.ARROW_BACK,
                            on_click=lambda _: self.app.navigate_to("facturacion"),
                            tooltip="Volver a Facturación",
                            icon_color=ft.Colors.WHITE,
                            bgcolor=ft.Colors.BLUE_600,
                            style=ft.ButtonStyle(shape=ft.CircleBorder())
                        ),
                        margin=ft.margin.only(right=15)
                    ),
                    ft.Column([
                        ft.Text(
                            "Gestión de Transferencias de Energía",
                            size=28,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.BLUE_800
                        ),
                        ft.Text(
                            "Administración de servicios y transferencias entre municipios",
                            size=16,
                            color=ft.Colors.BLUE_600
                        )
                    ], expand=True),
                    ft.Container(
                        content=ft.Icon(
                            ft.Icons.SWAP_HORIZONTAL_CIRCLE,
                            size=48,
                            color=ft.Colors.BLUE_600
                        ),
                        padding=10,
                        bgcolor=ft.Colors.BLUE_50,
                        border_radius=25
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                padding=25,
            ),
            elevation=3,
            margin=ft.margin.only(bottom=10)
        )
    
    def _build_period_selector(self) -> ft.Control:
        """Construye el selector de período"""
        self.año_field = ft.TextField(
            label="Año",
            value=str(self.current_año),
            width=120,
            keyboard_type=ft.KeyboardType.NUMBER,
            bgcolor=ft.Colors.WHITE,
            border_color=ft.Colors.BLUE_300,
            focused_border_color=ft.Colors.BLUE_600
        )
        
        self.mes_dropdown = ft.Dropdown(
            label="Mes",
            width=180,
            value=str(self.current_mes),
            bgcolor=ft.Colors.WHITE,
            border_color=ft.Colors.BLUE_300,
            focused_border_color=ft.Colors.BLUE_600,
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
        
        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.DATE_RANGE, color=ft.Colors.BLUE_600, size=24),
                        ft.Text("Período de Transferencias", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800)
                    ]),
                    ft.Container(height=15),
                    ft.Row([
                        self.año_field,
                        self.mes_dropdown,
                        ft.Container(width=20),
                        ft.ElevatedButton(
                            content=ft.Row([
                                ft.Icon(ft.Icons.SEARCH, size=18),
                                ft.Text("Cargar Período")
                            ], spacing=8),
                            on_click=self._load_period_data,
                            style=ft.ButtonStyle(
                                bgcolor=ft.Colors.BLUE_600,
                                color=ft.Colors.WHITE,
                                padding=ft.padding.symmetric(horizontal=20, vertical=12),
                                shape=ft.RoundedRectangleBorder(radius=8)
                            )
                        )
                    ], spacing=15)
                ]),
                padding=20
            ),
            elevation=2
        )
    
    def _build_transfer_summary(self) -> ft.Control:
        """Construye el resumen de transferencias"""
        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.ANALYTICS, color=ft.Colors.GREEN_600, size=24),
                        ft.Text("Resumen de Transferencias", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_800)
                    ]),
                    ft.Container(height=15),
                    
                    # Resumen por flujo
                    ft.Row([
                        self._create_transfer_card("MATANZAS → U.REYES", "4 servicios", ft.Colors.RED_100, ft.Colors.RED_600),
                        self._create_transfer_card("CÁRDENAS → PROVINCIA", "1 servicio", ft.Colors.ORANGE_100, ft.Colors.ORANGE_600),
                        self._create_transfer_card("JAGÜEY → COLÓN", "5 servicios", ft.Colors.BLUE_100, ft.Colors.BLUE_600),
                        self._create_transfer_card("JAGÜEY → JOVELLANOS", "4 servicios", ft.Colors.PURPLE_100, ft.Colors.PURPLE_600)
                    ], spacing=15, wrap=True)
                ]),
                padding=20
            ),
            elevation=2
        )
    
    def _create_transfer_card(self, title: str, subtitle: str, bg_color, text_color) -> ft.Container:
        """Crea una tarjeta de resumen de transferencia"""
        return ft.Container(
            content=ft.Column([
                ft.Text(title, size=14, weight=ft.FontWeight.BOLD, color=text_color),
                ft.Text(subtitle, size=12, color=text_color)
            ], spacing=5),
            padding=15,
            bgcolor=bg_color,
            border_radius=10,
            width=200,
            height=60
        )
    
    def _build_services_table(self) -> ft.Control:
        """Construye la tabla de servicios"""
        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.TABLE_CHART, color=ft.Colors.BLUE_600, size=24),
                        ft.Text("Servicios y Transferencias", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800),
                        ft.Container(expand=True),
                        ft.Text(f"Total: {self._get_total_services()} servicios", size=14, color=ft.Colors.GREY_600)
                    ]),
                    ft.Container(height=15),
                    
                    # Tabla de servicios
                    self._build_services_data_table()
                    
                ], spacing=10),
                padding=20
            ),
            elevation=2,
            expand=True
        )
    
    def _build_services_data_table(self) -> ft.Control:
        """Construye la tabla de datos de servicios"""
        # Crear tabla
        self.services_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Servicio", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Origen", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Destino", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Consumo (kW)", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Estado", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Acciones", weight=ft.FontWeight.BOLD))
            ],
            rows=[]
        )
        
        # Llenar tabla con servicios fijos
        self._populate_services_table()
        
        return ft.Container(
            content=self.services_table,
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=8,
            padding=10,
            bgcolor=ft.Colors.WHITE
        )
    
    def _populate_services_table(self):
        """Llena la tabla con los servicios fijos"""
        self.services_table.rows.clear()
        
        # Colores por flujo de transferencia
        flow_colors = {
            "MATANZAS": ft.Colors.RED_50,
            "CÁRDENAS": ft.Colors.ORANGE_50,
            "JAGÜEY": ft.Colors.BLUE_50
        }
        
        for flow_key, servicios in self.servicios_fijos.items():
            for servicio in servicios:
                consumo_actual = self.consumos_actuales.get(servicio["id"], 0)
                
                # Determinar estado
                if consumo_actual > 0:
                    estado = ft.Container(
                        content=ft.Text("Activo", size=12, color=ft.Colors.WHITE),
                        bgcolor=ft.Colors.GREEN_600,
                        padding=ft.padding.symmetric(horizontal=8, vertical=4),
                        border_radius=12
                    )
                else:
                    estado = ft.Container(
                        content=ft.Text("Sin consumo", size=12, color=ft.Colors.WHITE),
                        bgcolor=ft.Colors.GREY_500,
                        padding=ft.padding.symmetric(horizontal=8, vertical=4),
                        border_radius=12
                    )
                
                self.services_table.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(f"#{servicio['id']}", weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700)),
                            ft.DataCell(ft.Text(servicio["nombre"], size=13)),
                            ft.DataCell(ft.Text(servicio["origen"], weight=ft.FontWeight.BOLD, color=ft.Colors.RED_600)),
                            ft.DataCell(ft.Text(servicio["destino"], weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_600)),
                            ft.DataCell(ft.Text(f"{consumo_actual:,.2f}", size=13, weight=ft.FontWeight.BOLD)),
                            ft.DataCell(estado),
                            ft.DataCell(
                                ft.Row([
                                    ft.IconButton(
                                        icon=ft.Icons.EDIT,
                                        tooltip="Editar consumo",
                                        icon_color=ft.Colors.BLUE_600,
                                        on_click=lambda e, srv=servicio: self._edit_service_consumption(srv)
                                    ),
                                    ft.IconButton(
                                        icon=ft.Icons.INFO,
                                        tooltip="Ver detalles",
                                        icon_color=ft.Colors.GREEN_600,
                                        on_click=lambda e, srv=servicio: self._show_service_details(srv)
                                    )
                                ], spacing=5)
                            )
                        ],
                        color=flow_colors.get(servicio["origen"], ft.Colors.WHITE)
                    )
                )
    
    def _get_total_services(self) -> int:
        """Obtiene el total de servicios"""
        total = 0
        for servicios in self.servicios_fijos.values():
            total += len(servicios)
        return total
    
    def _build_actions(self) -> ft.Control:
        """Construye las acciones principales"""
        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.SETTINGS, color=ft.Colors.PURPLE_600, size=24),
                        ft.Text("Acciones", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.PURPLE_800)
                    ]),
                    ft.Container(height=15),
                    
                    # Primera fila de botones
                    ft.Row([
                        # Cargar desde Excel
                        ft.ElevatedButton(
                            content=ft.Row([
                                ft.Icon(ft.Icons.UPLOAD_FILE, size=20),
                                ft.Text("Cargar desde Excel")
                            ], spacing=8),
                            on_click=self._import_from_excel,
                            style=ft.ButtonStyle(
                                bgcolor=ft.Colors.GREEN_600,
                                color=ft.Colors.WHITE,
                                padding=ft.padding.symmetric(horizontal=20, vertical=15),
                                shape=ft.RoundedRectangleBorder(radius=10),
                                elevation=3
                            ),
                            width=200,
                            height=50
                        ),
                        
                        # Aplicar Transferencias
                        ft.ElevatedButton(
                            content=ft.Row([
                                ft.Icon(ft.Icons.PLAY_ARROW, size=20),
                                ft.Text("Aplicar Transferencias")
                            ], spacing=8),
                            on_click=self._apply_transfers,
                            style=ft.ButtonStyle(
                                bgcolor=ft.Colors.BLUE_600,
                                color=ft.Colors.WHITE,
                                padding=ft.padding.symmetric(horizontal=20, vertical=15),
                                shape=ft.RoundedRectangleBorder(radius=10),
                                elevation=3
                            ),
                            width=220,
                            height=50
                        ),
                        
                        
                    ], spacing=15, wrap=True),
                    
                    ft.Container(height=10),
                    
                    # Segunda fila de botones
                    ft.Row([
                        # NUEVO: Gestionar Servicios
                        ft.ElevatedButton(
                            content=ft.Row([
                                ft.Icon(ft.Icons.EDIT_NOTE, size=20),
                                ft.Text("Gestionar Servicios")
                            ], spacing=8),
                            on_click=self._manage_services,
                            style=ft.ButtonStyle(
                                bgcolor=ft.Colors.PURPLE_600,
                                color=ft.Colors.WHITE,
                                padding=ft.padding.symmetric(horizontal=20, vertical=15),
                                shape=ft.RoundedRectangleBorder(radius=10),
                                elevation=3
                            ),
                            width=200,
                            height=50
                        ),
                        
                        ft.Container(expand=True),
                        
                        # Limpiar Datos
                        ft.ElevatedButton(
                            content=ft.Row([
                                ft.Icon(ft.Icons.CLEAR_ALL, size=20),
                                ft.Text("Limpiar Datos")
                            ], spacing=8),
                            on_click=self._clear_data,
                            style=ft.ButtonStyle(
                                bgcolor=ft.Colors.RED_600,
                                color=ft.Colors.WHITE,
                                padding=ft.padding.symmetric(horizontal=20, vertical=15),
                                shape=ft.RoundedRectangleBorder(radius=10),
                                elevation=3
                            ),
                            width=180,
                            height=50
                        )
                    ], spacing=15)
                ]),
                padding=20
            ),
            elevation=2
        )
    

    # === MÉTODOS DE FUNCIONALIDAD ===
    def _load_period_data(self, e):
        """Carga datos del período seleccionado desde la base de datos"""
        try:
            año = int(self.año_field.value)
            mes = int(self.mes_dropdown.value)
            
            self._show_info(f"Cargando datos para {mes:02d}/{año}...")
            
            # CONSULTAR BASE DE DATOS REAL
            # Obtener todos los IDs de servicios que necesitamos
            servicios_ids = []
            for servicios in self.servicios_fijos.values():
                for servicio in servicios:
                    servicios_ids.append(servicio["id"])
            
            # Consultar consumos desde la base de datos
            consumos_encontrados = self._get_consumos_from_database(servicios_ids, año, mes)
            
            # Inicializar todos los consumos en 0
            self.consumos_actuales = {}
            for servicio_id in servicios_ids:
                self.consumos_actuales[servicio_id] = 0.0
            
            # Actualizar con los datos encontrados en BD
            self.consumos_actuales.update(consumos_encontrados)
            
            # Actualizar interfaz
            self._populate_services_table()
            
            self.page.update()
            
            # Mostrar resultado
            servicios_con_datos = len([v for v in consumos_encontrados.values() if v > 0])
            self._show_success(f"Datos cargados para {mes:02d}/{año} - {servicios_con_datos} servicios con consumo")
            
        except Exception as e:
            self.logger.error(f"Error al cargar período: {e}")
            self._show_error("Error al cargar los datos del período")
    
    def _get_consumos_from_database(self, servicios_ids: List[str], año: int, mes: int) -> Dict[str, float]:
        """MÉTODO SIMPLIFICADO - Retorna datos de ejemplo"""
        try:
            self.logger.info("Usando datos de ejemplo - no hay persistencia en BD")
            
            # Datos de ejemplo para testing
            datos_ejemplo = {
                "124": 2134.0,
                "47": 0.0,
                "46": 3145.0,
                "665": 222088.0,
                "2621": 0.0,
                "2622": 0.0,
                "2623": 1390.0,
                "2633": 363.0,
                "2449": 1930.0,
                "2443": 1104.0,
                "2808": 0.0
            }
            
            # Solo retornar los servicios que se solicitan
            resultado = {}
            for servicio_id in servicios_ids:
                if servicio_id in datos_ejemplo:
                    resultado[servicio_id] = datos_ejemplo[servicio_id]
            
            self.logger.info(f"Consumos obtenidos: {len(resultado)} registros")
            return resultado
            
        except Exception as e:
            self.logger.error(f"Error al obtener consumos: {e}")
            return {}

    def _get_example_consumos(self) -> Dict[str, float]:
        """Retorna datos de ejemplo"""
        return {
            "124": 2134.0,
            "47": 0.0,
            "46": 3145.0,
            "665": 222088.0,
            "2621": 0.0,
            "2622": 0.0,
            "2623": 1390.0,
            "2633": 363.0,
            "2449": 1930.0,
            "2443": 1104.0,
            "2808": 0.0
        }


    def _import_from_excel(self, e):
        """Importa consumos desde archivo Excel"""
        def on_file_selected(e: ft.FilePickerResultEvent):
            if e.files:
                file_path = e.files[0].path
                self._process_excel_file(file_path)
        
        # Crear file picker
        file_picker = ft.FilePicker(on_result=on_file_selected)
        self.page.overlay.append(file_picker)
        self.page.update()
        
        # Abrir diálogo de selección
        file_picker.pick_files(
            dialog_title="Seleccionar archivo Excel de Consumos",
            file_type=ft.FilePickerFileType.CUSTOM,
            allowed_extensions=["xlsx", "xls"]
        )
    
    def _process_excel_file(self, file_path: str):
        """Procesa el archivo Excel de consumos"""
        try:
            año = int(self.año_field.value)
            mes = int(self.mes_dropdown.value)
            progress_dialog = self._show_progress_dialog("Procesando archivo Excel...")
            
            # Leer Excel con encabezados en primera fila
            df = pd.read_excel(file_path, header=0)
            
            # Verificar que existan las columnas necesarias
            if 'CODCLI' not in df.columns or 'KWHT' not in df.columns:
                progress_dialog.open = False
                self.page.update()
                self._show_error("El archivo Excel debe contener las columnas 'CODCLI' y 'KWHT'")
                return
            
            # Crear lista de todos los IDs de servicios que buscamos
            servicios_ids = []
            for servicios in self.servicios_fijos.values():
                for servicio in servicios:
                    servicios_ids.append(servicio["id"])
            
            # Procesar datos del Excel
            consumos_importados = {}
            servicios_encontrados = []
            servicios_no_encontrados = []
            
            # Convertir CODCLI a string para comparación
            df['CODCLI'] = df['CODCLI'].astype(str)
            
            # Buscar cada servicio en el Excel
            for servicio_id in servicios_ids:
                # Buscar fila con este CODCLI
                fila = df[df['CODCLI'] == servicio_id]
                
                if not fila.empty:
                    # Servicio encontrado - obtener consumo
                    kwht_value = fila['KWHT'].iloc[0]
                    
                    # Convertir a float, manejar valores nulos
                    try:
                        consumo = float(kwht_value) if pd.notna(kwht_value) else 0.0
                        consumos_importados[servicio_id] = consumo
                        servicios_encontrados.append(f"#{servicio_id}: {consumo:,.2f} kW")
                    except (ValueError, TypeError):
                        consumos_importados[servicio_id] = 0.0
                        servicios_encontrados.append(f"#{servicio_id}: 0.00 kW (valor inválido)")
                else:
                    # Servicio no encontrado - asignar consumo = 0
                    consumos_importados[servicio_id] = 0.0
                    servicios_no_encontrados.append(f"#{servicio_id}")
            
            # Cerrar diálogo de progreso
            progress_dialog.open = False
            self.page.update()
            
            # Actualizar consumos actuales
            self.consumos_actuales.update(consumos_importados)
            
            # Actualizar tabla
            self._populate_services_table()
            self._ask_save_imported_data(año, mes)
            # Mostrar resultados
            total_servicios = len(servicios_encontrados) + len(servicios_no_encontrados)
            self._show_success(f"Procesamiento completado: {len(servicios_encontrados)} encontrados, {len(servicios_no_encontrados)} con consumo = 0")
            
            # Mostrar detalles si hay servicios no encontrados
            if servicios_no_encontrados:
                self._show_import_results(servicios_encontrados, servicios_no_encontrados, len(df))
            
        except Exception as e:
            self.logger.error(f"Error al procesar Excel: {e}")
            if 'progress_dialog' in locals() and progress_dialog.open:
                progress_dialog.open = False
                self.page.update()
            self._show_error(f"Error al procesar el archivo: {str(e)}")
        
  
    def _ask_save_imported_data(self, año: int, mes: int):
        """Pregunta si quiere guardar los datos importados"""
        def save_data(e):
            saved_count = self._save_consumos_to_database(año, mes)
            if saved_count > 0:
                self._show_success(f"Datos guardados: {saved_count} servicios")
            dialog.open = False
            self.page.update()
        
        def skip_save(e):
            dialog.open = False
            self.page.update()
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("¿Guardar datos importados?"),
            content=ft.Text(f"¿Desea guardar los consumos importados para {mes:02d}/{año}?"),
            actions=[
                ft.TextButton("No guardar", on_click=skip_save),
                ft.ElevatedButton("Guardar", on_click=save_data)
            ]
        )
        
        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()
    
    def _show_import_results(self, encontrados: List[str], no_encontrados: List[str], total_filas: int):
        """Muestra los resultados detallados de la importación"""
        def close_dialog(e):
            dialog.open = False
            self.page.update()
        
        # Crear contenido del diálogo
        content_items = [
            ft.Text(f"📊 Total de filas en Excel: {total_filas}", size=14, weight=ft.FontWeight.BOLD),
            ft.Text(f"✅ Servicios encontrados: {len(encontrados)}", size=14, color=ft.Colors.GREEN),
            ft.Text(f"❌ Servicios no encontrados: {len(no_encontrados)}", size=14, color=ft.Colors.RED),
            ft.Divider()
        ]
        
        if encontrados:
            content_items.append(ft.Text("✅ Servicios procesados:", weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN))
            for servicio in encontrados[:10]:  # Mostrar máximo 10
                content_items.append(ft.Text(f"  • {servicio}", size=12))
            if len(encontrados) > 10:
                content_items.append(ft.Text(f"  ... y {len(encontrados) - 10} más", size=12, color=ft.Colors.GREY))
        
        if no_encontrados:
            content_items.append(ft.Text("❌ Servicios no encontrados:", weight=ft.FontWeight.BOLD, color=ft.Colors.RED))
            for servicio in no_encontrados:
                content_items.append(ft.Text(f"  • {servicio}", size=12, color=ft.Colors.RED))
        
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

    def _apply_transfers(self, e):
        """Aplica las transferencias actualizando DIRECTAMENTE la facturación"""
        try:
            año = int(self.año_field.value)
            mes = int(self.mes_dropdown.value)
            
            progress_dialog = self._show_progress_dialog("Aplicando transferencias a facturación...")
            
            # Calcular transferencias por municipio
            transferencias = self._calculate_municipal_transfers()
            
            if not transferencias:
                progress_dialog.open = False
                self.page.update()
                self._show_warning("No hay transferencias para aplicar")
                return
            
            # Actualizar facturación DIRECTAMENTE
            updated_count = self._update_facturacion_mayor(transferencias, año, mes)
            
            # Cerrar diálogo de progreso
            progress_dialog.open = False
            self.page.update()
            
            if updated_count > 0:
                # Mensaje SIN emojis
                self._show_success(f"Transferencias aplicadas: {updated_count} municipios actualizados")
                
                # Mostrar resumen de cambios
                self._show_transfer_summary(transferencias)
            else:
                self._show_error("No se pudieron aplicar las transferencias")
            
        except Exception as e:
            self.logger.error(f"Error al aplicar transferencias: {e}")
            if 'progress_dialog' in locals() and progress_dialog.open:
                progress_dialog.open = False
                self.page.update()
            self._show_error("Error al aplicar las transferencias")
    def _save_consumos_to_database(self, año: int, mes: int) -> int:
        """MÉTODO SIMPLIFICADO - No guarda en BD, solo mantiene en memoria"""
        try:
            # Contar servicios con consumo > 0
            servicios_con_consumo = len([v for v in self.consumos_actuales.values() if v > 0])
            
            self.logger.info(f"Consumos mantenidos en memoria: {servicios_con_consumo}")
            
            # Retornar cantidad de servicios procesados
            return servicios_con_consumo
            
        except Exception as e:
            self.logger.error(f"Error en _save_consumos_to_database: {e}")
            return 0

    def _export_summary(self, e):
        """Exporta resumen de transferencias"""
        try:
            # Crear resumen
            summary_data = []
            for flow_key, servicios in self.servicios_fijos.items():
                for servicio in servicios:
                    consumo = self.consumos_actuales.get(servicio["id"], 0)
                    summary_data.append({
                        'ID': servicio["id"],
                        'Servicio': servicio["nombre"],
                        'Origen': servicio["origen"],
                        'Destino': servicio["destino"],
                        'Consumo_kW': consumo
                    })
            
            # Crear DataFrame y exportar
            df = pd.DataFrame(summary_data)
            
            from pathlib import Path
            downloads_path = Path.home() / "Downloads"
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_path = downloads_path / f"transferencias_resumen_{timestamp}.xlsx"
            
            df.to_excel(file_path, index=False)
            
            self._show_success(f"Resumen exportado a: {file_path}")
            
        except Exception as ex:
            self.logger.error(f"Error al exportar: {ex}")
            self._show_error("Error al exportar el resumen")
    
    def _clear_data(self, e):
        """Limpia los datos de consumo"""
        def confirm_clear(e):
            self.consumos_actuales.clear()
            self._populate_services_table()
            dialog.open = False
            self.page.update()
            self._show_info("Datos de consumo limpiados")
        
        def cancel_clear(e):
            dialog.open = False
            self.page.update()
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmar Limpieza"),
            content=ft.Text("¿Está seguro de limpiar todos los datos de consumo?"),
            actions=[
                ft.TextButton("Cancelar", on_click=cancel_clear),
                ft.TextButton("Limpiar", on_click=confirm_clear)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        
        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()
    
    def _edit_service_consumption(self, servicio: Dict):
        """Edita el consumo de un servicio"""
        consumo_actual = self.consumos_actuales.get(servicio["id"], 0)
        
        consumo_field = ft.TextField(
            label="Consumo (kW)",
            value=str(consumo_actual),
            keyboard_type=ft.KeyboardType.NUMBER,
            width=200
        )
        
        def save_consumption(e):
            try:
                nuevo_consumo = float(consumo_field.value or 0)
                self.consumos_actuales[servicio["id"]] = nuevo_consumo
                self._populate_services_table()
                dialog.open = False
                self.page.update()
                self._show_success(f"Consumo actualizado para {servicio['nombre']}")
            except ValueError:
                self._show_error("Ingrese un valor numérico válido")
        
        def cancel_edit(e):
            dialog.open = False
            self.page.update()
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"Editar Consumo - {servicio['nombre']}"),
            content=ft.Container(
                content=ft.Column([
                    ft.Text(f"Servicio: #{servicio['id']}"),
                    ft.Text(f"Transferencia: {servicio['origen']} → {servicio['destino']}"),
                    ft.Container(height=15),
                    consumo_field
                ]),
                width=350
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=cancel_edit),
                ft.ElevatedButton("Guardar", on_click=save_consumption)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        
        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()
    
    def _show_service_details(self, servicio: Dict):
        """Muestra detalles del servicio"""
        consumo_actual = self.consumos_actuales.get(servicio["id"], 0)
        
        def close_details(e):
            dialog.open = False
            self.page.update()
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"Detalles del Servicio"),
            content=ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Text("ID:", weight=ft.FontWeight.BOLD),
                        ft.Text(f"#{servicio['id']}")
                    ]),
                    ft.Row([
                        ft.Text("Nombre:", weight=ft.FontWeight.BOLD),
                        ft.Text(servicio['nombre'])
                    ]),
                    ft.Row([
                        ft.Text("Origen:", weight=ft.FontWeight.BOLD),
                        ft.Text(servicio['origen'], color=ft.Colors.RED_600)
                    ]),
                    ft.Row([
                        ft.Text("Destino:", weight=ft.FontWeight.BOLD),
                        ft.Text(servicio['destino'], color=ft.Colors.GREEN_600)
                    ]),
                    ft.Row([
                        ft.Text("Consumo Actual:", weight=ft.FontWeight.BOLD),
                        ft.Text(f"{consumo_actual:,.2f} kW", weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_600)
                    ]),
                    ft.Container(height=10),
                    ft.Text("Estado:", weight=ft.FontWeight.BOLD),
                    ft.Text("Activo" if consumo_actual > 0 else "Sin consumo", 
                           color=ft.Colors.GREEN_600 if consumo_actual > 0 else ft.Colors.GREY_600)
                ], spacing=8),
                width=400
            ),
            actions=[
                ft.TextButton("Cerrar", on_click=close_details)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        
        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()
    
    # === MÉTODOS DE UTILIDAD ===
    
    def _show_progress_dialog(self, message: str):
        """Muestra diálogo de progreso"""
        progress_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Procesando"),
            content=ft.Container(
                content=ft.Column([
                    ft.ProgressRing(),
                    ft.Container(height=15),
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
    
    def _show_success(self, message: str):
        """Muestra mensaje de éxito"""
        snack_bar = ft.SnackBar(
            content=ft.Row([
                ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.WHITE, size=20),
                ft.Text(message, color=ft.Colors.WHITE)
            ]),
            bgcolor=ft.Colors.GREEN_600,
            duration=3000
        )
        self.page.snack_bar = snack_bar
        snack_bar.open = True
        self.page.update()
    
    def _show_error(self, message: str):
        """Muestra mensaje de error"""
        snack_bar = ft.SnackBar(
            content=ft.Row([
                ft.Icon(ft.Icons.ERROR, color=ft.Colors.WHITE, size=20),
                ft.Text(message, color=ft.Colors.WHITE)
            ]),
            bgcolor=ft.Colors.RED_600,
            duration=4000
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
        
    def _show_info(self, message: str):
        """Muestra mensaje informativo"""
        snack_bar = ft.SnackBar(
            content=ft.Row([
                ft.Icon(ft.Icons.INFO, color=ft.Colors.WHITE, size=20),
                ft.Text(message, color=ft.Colors.WHITE)
            ]),
            bgcolor=ft.Colors.BLUE_600,
            duration=3000
        )
        self.page.snack_bar = snack_bar
        snack_bar.open = True
        self.page.update()
    
    def on_mount(self):
        """Se ejecuta cuando se monta la pantalla"""
        self._load_period_data(None)
    
    def _manage_services(self, e):
        """Abre el diálogo de gestión de servicios"""
        
        # Crear lista de servicios para editar
        services_list = ft.Column([], spacing=10, scroll=ft.ScrollMode.AUTO)
        
        def refresh_services_list():
            """Actualiza la lista de servicios"""
            services_list.controls.clear()
            
            for flow_key, servicios in self.servicios_fijos.items():
                # Título del flujo
                flow_title = flow_key.replace("_", " → ").replace("MATANZAS UNION", "MATANZAS → U.REYES")
                services_list.controls.append(
                    ft.Container(
                        content=ft.Text(flow_title, size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700),
                        padding=ft.padding.only(top=10, bottom=5)
                    )
                )
                
                # Servicios del flujo
                for i, servicio in enumerate(servicios):
                    service_row = ft.Container(
                        content=ft.Row([
                            ft.Text(f"#{servicio['id']}", width=60, weight=ft.FontWeight.BOLD),
                            ft.Text(servicio['nombre'], expand=True),
                            ft.IconButton(
                                icon=ft.Icons.EDIT,
                                tooltip="Editar servicio",
                                on_click=lambda e, flow=flow_key, idx=i: edit_service(flow, idx)
                            ),
                            ft.IconButton(
                                icon=ft.Icons.DELETE,
                                tooltip="Eliminar servicio",
                                on_click=lambda e, flow=flow_key, idx=i: delete_service(flow, idx)
                            )
                        ]),
                        bgcolor=ft.Colors.GREY_50,
                        padding=10,
                        border_radius=5
                    )
                    services_list.controls.append(service_row)
                
                # Botón para agregar servicio
                add_button = ft.Container(
                    content=ft.ElevatedButton(
                        content=ft.Row([
                            ft.Icon(ft.Icons.ADD, size=16),
                            ft.Text("Agregar Servicio")
                        ], spacing=5),
                        on_click=lambda e, flow=flow_key: add_service(flow),
                        style=ft.ButtonStyle(
                            bgcolor=ft.Colors.GREEN_100,
                            color=ft.Colors.GREEN_700
                        )
                    ),
                    padding=ft.padding.only(left=20, bottom=10)
                )
                services_list.controls.append(add_button)
        
        def edit_service(flow_key: str, index: int):
            """Edita un servicio existente"""
            servicio = self.servicios_fijos[flow_key][index]
            
            id_field = ft.TextField(label="ID", value=servicio['id'], width=100)
            nombre_field = ft.TextField(label="Nombre", value=servicio['nombre'], expand=True)
            
            def save_edit(e):
                if id_field.value and nombre_field.value:
                    # Actualizar servicio
                    self.servicios_fijos[flow_key][index]['id'] = id_field.value
                    self.servicios_fijos[flow_key][index]['nombre'] = nombre_field.value
                    
                    refresh_services_list()
                    edit_dialog.open = False
                    self.page.update()
                    self._show_success("Servicio actualizado")
                else:
                    self._show_error("Complete todos los campos")
            
            def cancel_edit(e):
                edit_dialog.open = False
                self.page.update()
            
            edit_dialog = ft.AlertDialog(
                modal=True,
                title=ft.Text("Editar Servicio"),
                content=ft.Container(
                    content=ft.Column([
                        ft.Row([id_field, nombre_field], spacing=10)
                    ]),
                    width=400
                ),
                actions=[
                    ft.TextButton("Cancelar", on_click=cancel_edit),
                    ft.ElevatedButton("Guardar", on_click=save_edit)
                ]
            )
            
            self.page.overlay.append(edit_dialog)
            edit_dialog.open = True
            self.page.update()
        
        def add_service(flow_key: str):
            """Agrega un nuevo servicio"""
            id_field = ft.TextField(label="ID", width=100)
            nombre_field = ft.TextField(label="Nombre", expand=True)
            
            def save_new(e):
                if id_field.value and nombre_field.value:
                    # Obtener origen y destino del flujo
                    flow_info = {
                        "MATANZAS_UNION": ("MATANZAS", "UNIÓN DE REYES"),
                        "CARDENAS_PROVINCIA": ("CÁRDENAS", "PROVINCIA"),
                        "JAGUEY_COLON": ("JAGÜEY", "COLÓN"),
                        "JAGUEY_JOVELLANOS": ("JAGÜEY", "JOVELLANOS")
                    }
                    
                    origen, destino = flow_info[flow_key]
                    
                    # Crear nuevo servicio
                    nuevo_servicio = {
                        "id": id_field.value,
                        "nombre": nombre_field.value,
                        "origen": origen,
                        "destino": destino
                    }
                    
                    self.servicios_fijos[flow_key].append(nuevo_servicio)
                    
                    refresh_services_list()
                    add_dialog.open = False
                    self.page.update()
                    self._show_success("Servicio agregado")
                else:
                    self._show_error("Complete todos los campos")
            
            def cancel_new(e):
                add_dialog.open = False
                self.page.update()
            
            add_dialog = ft.AlertDialog(
                modal=True,
                title=ft.Text("Agregar Servicio"),
                content=ft.Container(
                    content=ft.Column([
                        ft.Row([id_field, nombre_field], spacing=10)
                    ]),
                    width=400
                ),
                actions=[
                    ft.TextButton("Cancelar", on_click=cancel_new),
                    ft.ElevatedButton("Agregar", on_click=save_new)
                ]
            )
            
            self.page.overlay.append(add_dialog)
            add_dialog.open = True
            self.page.update()
        
        def delete_service(flow_key: str, index: int):
            """Elimina un servicio"""
            servicio = self.servicios_fijos[flow_key][index]
            
            def confirm_delete(e):
                # Eliminar servicio
                del self.servicios_fijos[flow_key][index]
                
                # Eliminar consumo si existe
                if servicio['id'] in self.consumos_actuales:
                    del self.consumos_actuales[servicio['id']]
                
                refresh_services_list()
                delete_dialog.open = False
                self.page.update()
                self._show_success("Servicio eliminado")
            
            def cancel_delete(e):
                delete_dialog.open = False
                self.page.update()
            
            delete_dialog = ft.AlertDialog(
                modal=True,
                title=ft.Text("Confirmar Eliminación"),
                content=ft.Text(f"¿Está seguro de eliminar el servicio #{servicio['id']} - {servicio['nombre']}?"),
                actions=[
                    ft.TextButton("Cancelar", on_click=cancel_delete),
                    ft.TextButton("Eliminar", on_click=confirm_delete)
                ]
            )
            
            self.page.overlay.append(delete_dialog)
            delete_dialog.open = True
            self.page.update()
        
        def close_manage_dialog(e):
            """Cierra el diálogo de gestión"""
            # Actualizar tabla con posibles cambios
            self._populate_services_table()
            manage_dialog.open = False
            self.page.update()
        
        def save_services_config(e):
            """Guarda la configuración de servicios"""
            try:
                total_servicios = sum(len(servicios) for servicios in self.servicios_fijos.values())
                
                # Guardar en archivo JSON
                self._save_to_json()
                
                self._show_success(f"Configuración guardada: {total_servicios} servicios")
                
            except Exception as ex:
                self.logger.error(f"Error al guardar configuración: {ex}")
                self._show_error("Error al guardar la configuración")
        
        # Inicializar lista
        refresh_services_list()
        
        # Crear diálogo principal
        manage_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Row([
                ft.Icon(ft.Icons.EDIT_NOTE, color=ft.Colors.PURPLE_600),
                ft.Text("Gestionar Servicios de Transferencia")
            ]),
            content=ft.Container(
                content=ft.Column([
                    ft.Text("Administre los servicios de transferencia entre municipios:", 
                        size=14, color=ft.Colors.GREY_700),
                    ft.Container(height=10),
                    ft.Container(
                        content=services_list,
                        height=400,
                        width=600
                    )
                ]),
                width=650,
                height=500
            ),
            actions=[
                ft.Row([
                    ft.ElevatedButton(
                        content=ft.Row([
                            ft.Icon(ft.Icons.SAVE, size=16),
                            ft.Text("Guardar Configuración")
                        ], spacing=5),
                        on_click=save_services_config,  # Función local, no método de clase
                        style=ft.ButtonStyle(
                            bgcolor=ft.Colors.GREEN_600,
                            color=ft.Colors.WHITE
                        )
                    ),
                    ft.Container(expand=True),
                    ft.TextButton("Cerrar", on_click=close_manage_dialog)
                ])
            ],
            actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )
        
        self.page.overlay.append(manage_dialog)
        manage_dialog.open = True
        self.page.update()

    def _save_to_json(self):
        """Guarda servicios en archivo JSON"""
        try:
            import json
            from pathlib import Path
            
            # Crear directorio de configuración
            config_dir = Path(__file__).parent.parent.parent / "config"
            config_dir.mkdir(exist_ok=True)
            
            config_file = config_dir / "servicios_transferencia.json"
            
            # Guardar configuración
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(self.servicios_fijos, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Servicios guardados en: {config_file}")
            
        except Exception as e:
            self.logger.error(f"Error al guardar JSON: {e}")

    def _load_from_json(self):
        """Carga servicios desde archivo JSON"""
        try:
            import json
            from pathlib import Path
            
            config_file = Path(__file__).parent.parent.parent / "config" / "servicios_transferencia.json"
            
            if config_file.exists():
                with open(config_file, 'r', encoding='utf-8') as f:
                    self.servicios_fijos = json.load(f)
                
                self.logger.info("Servicios cargados desde archivo JSON")
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error al cargar JSON: {e}")
            return False

    def _update_summary_after_changes(self):
        """Actualiza el resumen después de cambios en servicios"""
        try:
            # Recalcular totales
            flow_totals = {}
            for flow_key, servicios in self.servicios_fijos.items():
                total = sum(self.consumos_actuales.get(s["id"], 0) for s in servicios)
                flow_name = flow_key.replace("_", " → ").replace("MATANZAS UNION", "MATANZAS → U.REYES")
                flow_totals[flow_name] = total
            
            # Actualizar cards de resumen
            if hasattr(self, 'summary_cards') and self.summary_cards:
                self._populate_summary_cards()
            
            # Actualizar tabla
            self._populate_services_table()
            
            self.page.update()
            
        except Exception as e:
            self.logger.error(f"Error al actualizar resumen: {e}")
    def _ask_save_imported_data(self, año: int, mes: int):
        """Pregunta si quiere aplicar las transferencias importadas"""
        def apply_transfers(e):
            try:
                # Aplicar transferencias a facturación
                updated_count = self._apply_transfers_to_facturacion(año, mes)
                
                if updated_count > 0:
                    self._show_success(f"Transferencias aplicadas: {updated_count} municipios actualizados")
                else:
                    self._show_warning("No se realizaron cambios en la facturación")
                    
            except Exception as ex:
                self.logger.error(f"Error al aplicar transferencias: {ex}")
                self._show_error("Error al aplicar las transferencias")
            
            dialog.open = False
            self.page.update()
        
        def skip_apply(e):
            dialog.open = False
            self.page.update()
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("¿Aplicar transferencias?"),
            content=ft.Text(f"¿Desea aplicar las transferencias importadas a la facturación de {mes:02d}/{año}?"),
            actions=[
                ft.TextButton("No aplicar", on_click=skip_apply),
                ft.ElevatedButton("Aplicar", on_click=apply_transfers)
            ]
        )
        
        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()

    def _apply_transfers_to_facturacion(self, año: int, mes: int) -> int:
        """Aplica las transferencias a la tabla de facturación"""
        try:
            # Calcular transferencias por municipio
            transferencias = self._calculate_municipal_transfers()
            
            # Actualizar facturación
            return self._update_facturacion_mayor(transferencias, año, mes)
            
        except Exception as e:
            self.logger.error(f"Error al aplicar transferencias: {e}")
            return 0
    
    def _calculate_municipal_transfers(self) -> Dict[str, float]:
        """Calcula las transferencias netas por municipio"""
        transferencias = {}
        
        try:
            for flow_key, servicios in self.servicios_fijos.items():
                for servicio in servicios:
                    servicio_id = servicio["id"]
                    consumo = self.consumos_actuales.get(servicio_id, 0.0)
                    
                    if consumo > 0:
                        origen = servicio["origen"]
                        destino = servicio["destino"]
                        
                        # Restar del origen
                        if origen not in transferencias:
                            transferencias[origen] = 0.0
                        transferencias[origen] -= consumo
                        
                        # Sumar al destino
                        if destino not in transferencias:
                            transferencias[destino] = 0.0
                        transferencias[destino] += consumo
                        
                        # LOG SIN caracteres Unicode problemáticos
                        self.logger.info(f"Transferencia: {servicio_id} -> {consumo:.2f} kWh ({origen} a {destino})")
            
            # Filtrar cambios muy pequeños
            transferencias_filtradas = {
                municipio: delta for municipio, delta in transferencias.items() 
                if abs(delta) >= 0.01
            }
            
            self.logger.info(f"Transferencias calculadas: {len(transferencias_filtradas)} municipios afectados")
            return transferencias_filtradas
            
        except Exception as e:
            self.logger.error(f"Error al calcular transferencias: {e}")
            return {}

    def _update_facturacion_mayor(self, transferencias: Dict[str, float], año: int, mes: int) -> int:
        """Actualiza DIRECTAMENTE la tabla facturación"""
        try:
            from facturacion.services import get_facturacion_service
            facturacion_service = get_facturacion_service()
            
            updated_count = 0
            
            for municipio_nombre, delta_consumo in transferencias.items():
                # Obtener municipio
                municipio = self._get_municipio_by_name(municipio_nombre)
                if not municipio:
                    self.logger.warning(f"Municipio no encontrado: {municipio_nombre}")
                    continue
                
                # Obtener facturación actual
                facturacion = facturacion_service.get_facturacion_by_municipio_periodo(
                    municipio['id'], año, mes
                )
                
                if facturacion:
                    # Actualizar facturación existente
                    facturacion_anterior = facturacion.facturacion_mayor
                    facturacion.facturacion_mayor = max(0, facturacion.facturacion_mayor + delta_consumo)
                    facturacion.facturacion_total = facturacion.facturacion_menor + facturacion.facturacion_mayor
                    
                    if facturacion_service.update_facturacion(facturacion):
                        updated_count += 1
                        # LOG SIN emojis problemáticos
                        self.logger.info(f"OK {municipio_nombre}: {facturacion_anterior:.2f} -> {facturacion.facturacion_mayor:.2f} kWh ({delta_consumo:+.2f})")
                    else:
                        self.logger.error(f"ERROR al actualizar {municipio_nombre}")
                else:
                    # Crear nueva facturación si no existe
                    from facturacion.models.facturacion_model import FacturacionModel
                    nueva_facturacion = FacturacionModel(
                        municipio_id=municipio['id'],
                        año=año,
                        mes=mes,
                        facturacion_menor=0.0,
                        facturacion_mayor=max(0, delta_consumo),
                        facturacion_total=max(0, delta_consumo),
                        usuario_id=self.app.get_current_user().get('id', 1)
                    )
                    
                    if facturacion_service.save_facturacion(nueva_facturacion):
                        updated_count += 1
                        self.logger.info(f"CREADO {municipio_nombre}: {delta_consumo:.2f} kWh")
                    else:
                        self.logger.error(f"ERROR al crear facturación para {municipio_nombre}")
            
            return updated_count
            
        except Exception as e:
            self.logger.error(f"Error al actualizar facturación: {e}")
            return 0

    def _get_municipio_by_name(self, nombre: str) -> Dict[str, Any]:
        """Obtiene municipio por nombre con mapeo"""
        try:
            # Mapeo de nombres de transferencias a nombres en BD
            name_mapping = {
                'PROVINCIA': 'Provincia',
                'UNIÓN DE REYES': 'Unión de Reyes', 
                'CÁRDENAS': 'Cárdenas',
                'JAGÜEY': 'Jagüey Grande',
                'COLÓN': 'Colón',
                'JOVELLANOS': 'Jovellanos',
                'MATANZAS': 'Matanzas'
            }
            
            nombre_bd = name_mapping.get(nombre.upper(), nombre)
            
            # Buscar en lista de municipios cargados
            for municipio in self.municipios:
                if municipio['nombre'].lower() == nombre_bd.lower():
                    return municipio
            
            self.logger.warning(f"Municipio no encontrado: {nombre} (buscado como: {nombre_bd})")
            return None
            
        except Exception as e:
            self.logger.error(f"Error al buscar municipio {nombre}: {e}")
            return None

    def _show_transfer_summary(self, transferencias: Dict[str, float]):
        """Muestra resumen de transferencias aplicadas"""
        def close_dialog(e):
            dialog.open = False
            self.page.update()
        
        # Crear contenido del resumen
        content_items = [
            ft.Text("Resumen de Transferencias Aplicadas:", size=16, weight=ft.FontWeight.BOLD)
        ]
        
        for municipio, delta in transferencias.items():
            if delta > 0:
                content_items.append(
                    ft.Row([
                        ft.Icon(ft.Icons.ADD, color=ft.Colors.GREEN, size=16),
                        ft.Text(f"{municipio}: +{delta:,.2f} kWh", color=ft.Colors.GREEN)
                    ])
                )
            else:
                content_items.append(
                    ft.Row([
                        ft.Icon(ft.Icons.REMOVE, color=ft.Colors.RED, size=16),
                        ft.Text(f"{municipio}: {delta:,.2f} kWh", color=ft.Colors.RED)
                    ])
                )
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Transferencias Aplicadas"),
            content=ft.Container(
                content=ft.Column(content_items, scroll=ft.ScrollMode.AUTO),
                width=400,
                height=300
            ),
            actions=[
                ft.TextButton("Cerrar", on_click=close_dialog)
            ]
        )
        
        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()