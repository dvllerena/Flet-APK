import flet as ft
import sqlite3
from docxtpl import DocxTemplate
import pandas as pd
from datetime import datetime
from pathlib import Path
import os

def main(page: ft.Page):
    # Configuración con tema y colores
    page.title = "Aviso de Corte"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 15
    page.scroll = ft.ScrollMode.AUTO
    
    # Tema de colores
    COLOR_PRIMARIO = ft.Colors.BLUE_700
    COLOR_SECUNDARIO = ft.Colors.GREEN_700
    COLOR_TERCIARIO = ft.Colors.PURPLE_700
    COLOR_FONDO = ft.Colors.GREY_50
    
    # Variables globales
    DB_PATH = "avisos_corte.db"
    PLANTILLA_PATH = "assets/plantilla_aviso.docx"
    cuentas_data = []
    controles_cuentas = {}
    filtro_actual = "ninguno"  # "ninguno", "facturas", "importe"

    # Funciones principales
    def obtener_cuentas_bancarias():
        """Obtiene cuentas desde SQLite"""
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='servicios'")
            if not cursor.fetchone():
                return []
            
            cursor.execute('''
                SELECT 
                    "CTA BANCARIA",
                    COUNT(*) as total_servicios,
                    SUM(IMPORTE) as total_importe,
                    GROUP_CONCAT(JUCEPLAN) as juceplans,
                    GROUP_CONCAT(CARGOS_EMPRESA) as cargos
                FROM servicios 
                GROUP BY "CTA BANCARIA"
                ORDER BY "CTA BANCARIA"
            ''')
            
            return cursor.fetchall()
            
        except Exception as e:
            print(f"Error al obtener cuentas: {e}")
            return []
        finally:
            conn.close()

    def aplicar_filtro(filtro):
        """Aplica el filtro seleccionado a las cuentas"""
        nonlocal filtro_actual, cuentas_data
        filtro_actual = filtro
        
        if not cuentas_data:
            return  # No hacer nada si no hay datos
        
        if filtro == "ninguno":
            cuentas_data.sort(key=lambda x: x[0])
            filtro_btn.text = "🔻 Filtrar"
        elif filtro == "facturas":
            cuentas_data.sort(key=lambda x: x[1], reverse=True)
            filtro_btn.text = "🔻 Facturas"
        elif filtro == "importe":
            cuentas_data.sort(key=lambda x: x[2] if x[2] is not None else 0, reverse=True)
            filtro_btn.text = "🔻 Importe"
        
        cuentas_container.controls.clear()
        for cuenta in cuentas_data:
            cuentas_container.controls.append(crear_item_cuenta(cuenta))
        
        page.update()
    
    def mostrar_menu_filtro(e):
        """Cicla entre las opciones de filtro al hacer clic"""
        if filtro_actual == "ninguno":
            aplicar_filtro("facturas")
        elif filtro_actual == "facturas":
            aplicar_filtro("importe")
        elif filtro_actual == "importe":
            aplicar_filtro("ninguno")
         
    def filtrar_cuentas(e):
        """Filtra cuentas basado en búsqueda"""
        termino = search_field.value.lower()
        cuentas_container.controls.clear()
        
        for cuenta in cuentas_data:
            if termino in str(cuenta[0]).lower():
                cuentas_container.controls.append(crear_item_cuenta(cuenta))
        
        page.update()

    def crear_item_cuenta(cuenta):
        """Crea un item de cuenta bancaria con checkbox expandible"""
        cuenta_numero, total_servicios, total_importe, juceplans, cargos = cuenta
        
        checkbox = ft.Checkbox(
            value=False,
            on_change=lambda e: actualizar_contadores()
        )
        
        controles_cuentas[cuenta_numero] = checkbox
        
        servicios = obtener_servicios_por_cuenta(cuenta_numero)
        
        # Badge indicador de filtro
        badge_text = ""
        if filtro_actual == "facturas":
            badge_text = f"📋 {total_servicios} facturas"
        elif filtro_actual == "importe":
            badge_text = f"💰 ${total_importe:,.2f}"
        
        # TABLA MODIFICADA: Eliminamos JUCEPLAN y CARGOS_EMPRESA
        # y mostramos información diferente
        tabla_servicios = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Cuenta Bancaria", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Empresa/Concepto", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Factura", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Importe", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Fecha", weight=ft.FontWeight.BOLD)),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(serv[1])),  # CTA BANCARIA (ahora visible)
                        ft.DataCell(ft.Text(serv[2])),  # CARGOS_EMPRESA (ahora visible)
                        ft.DataCell(ft.Text(serv[3])),  # FACT
                        ft.DataCell(ft.Text(f"${serv[4]:,.2f}")),  # IMPORTE
                        ft.DataCell(ft.Text(serv[5])),  # FECHA
                    ]
                ) for serv in servicios
            ],
            vertical_lines=ft.BorderSide(1, ft.Colors.GREY_300),
            horizontal_lines=ft.BorderSide(1, ft.Colors.GREY_300),
        )
        
        expansion_tile = ft.ExpansionTile(
            title=ft.Row([
                checkbox,
                ft.Icon(ft.Icons.ACCOUNT_BALANCE, color=COLOR_PRIMARIO),
                ft.Column([
                    ft.Text(f"Cuenta: {cuenta_numero}", size=16, weight=ft.FontWeight.BOLD),
                    ft.Text(badge_text, size=12, color=COLOR_TERCIARIO) if badge_text else ft.Container()
                ], spacing=2)
            ], spacing=10),
            subtitle=ft.Text(
                f"{total_servicios} servicios - Total: ${total_importe:,.2f}",
                size=14,
                color=COLOR_SECUNDARIO
            ),
            controls=[
                ft.Container(
                    content=ft.Column([
                        ft.Text("Detalles de servicios:", weight=ft.FontWeight.BOLD, color=COLOR_PRIMARIO),
                        ft.Container(
                            content=tabla_servicios,
                            padding=10,
                            border=ft.border.all(1, ft.Colors.GREY_300),
                            border_radius=5,
                            bgcolor=ft.Colors.WHITE
                        )
                    ], spacing=10),
                    padding=10
                )
            ],
            initially_expanded=False,
        )
        
        return ft.Container(
            content=expansion_tile,
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=10,
            padding=5,
            bgcolor=ft.Colors.BLUE_50 if checkbox.value else None,
        )

    def obtener_servicios_por_cuenta(cuenta_numero):
        """Obtiene los servicios detallados para una cuenta específica"""
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT JUCEPLAN, "CTA BANCARIA", CARGOS_EMPRESA, FACT, IMPORTE, FECHA
                FROM servicios WHERE "CTA BANCARIA" = ?
                ORDER BY FECHA DESC
            ''', (cuenta_numero,))
            
            servicios = cursor.fetchall()
            conn.close()
            return servicios
            
        except Exception as e:
            print(f"Error al obtener servicios: {e}")
            return []

    def toggle_seleccion_cuenta(cuenta_numero):
        """Toggle de selección para cuenta específica"""
        checkbox = controles_cuentas.get(cuenta_numero)
        if checkbox:
            checkbox.value = not checkbox.value
            actualizar_contadores()
            page.update()

    def actualizar_contadores():
        """Actualiza contadores de selección"""
        selected = sum(1 for checkbox in controles_cuentas.values() if checkbox.value)
        selected_counter.value = f"{selected} cuentas seleccionadas"
        
        if cuentas_data:
            progress_bar.value = selected / len(cuentas_data)
        
        page.update()

    def cargar_datos_desde_excel(e: ft.FilePickerResultEvent):
        """Carga datos desde archivo Excel seleccionado"""
        if not e.files:
            return
            
        file_path = e.files[0].path
        progress_bar.visible = True
        loading_text.value = "Cargando datos desde Excel..."
        page.update()
        
        try:
            conn = sqlite3.connect(DB_PATH)
            
            df = pd.read_excel(file_path)
            df.to_sql('servicios', conn, if_exists='replace', index=False)
            conn.close()
            
            inicializar_app()
            
            page.snack_bar = ft.SnackBar(
                ft.Text("Datos cargados exitosamente desde Excel"),
                bgcolor=COLOR_SECUNDARIO
            )
            page.snack_bar.open = True
            
        except Exception as ex:
            error_msg = f"Error al cargar Excel: {str(ex)}"
            page.snack_bar = ft.SnackBar(
                ft.Text(error_msg),
                bgcolor=ft.Colors.RED
            )
            page.snack_bar.open = True
        
        progress_bar.visible = False
        loading_text.value = ""
        page.update()

    def generar_documento(e):
        """Genera documento Word para cuentas seleccionadas"""
        if not os.path.exists(PLANTILLA_PATH):
            page.snack_bar = ft.SnackBar(
                ft.Text("Plantilla Word no encontrada"),
                bgcolor=ft.Colors.RED
            )
            page.snack_bar.open = True
            page.update()
            return
            
        progress_bar.visible = True
        page.update()
        
        try:
            cuentas_seleccionadas = [
                cuenta for cuenta in cuentas_data 
                if controles_cuentas.get(cuenta[0]) and controles_cuentas[cuenta[0]].value
            ]
            
            if not cuentas_seleccionadas:
                page.snack_bar = ft.SnackBar(
                    ft.Text("Selecciona al menos una cuenta"),
                    bgcolor=ft.Colors.ORANGE
                )
                page.snack_bar.open = True
                progress_bar.visible = False
                page.update()
                return
            
            print("=== GENERANDO DOCUMENTOS ===")
            print(f"Cuentas seleccionadas: {len(cuentas_seleccionadas)}")
            
            for i, cuenta in enumerate(cuentas_seleccionadas):
                print(f"Generando documento {i+1}/{len(cuentas_seleccionadas)}")
                generar_doc_individual(cuenta)
            
            page.snack_bar = ft.SnackBar(
                ft.Text(f"Se generaron {len(cuentas_seleccionadas)} documentos"),
                bgcolor=COLOR_SECUNDARIO
            )
            page.snack_bar.open = True
            
        except Exception as ex:
            print(f"ERROR: {str(ex)}")
            page.snack_bar = ft.SnackBar(
                ft.Text(f"Error: {str(ex)}"),
                bgcolor=ft.Colors.RED
            )
            page.snack_bar.open = True
        
        progress_bar.visible = False
        page.update()

    def generar_doc_individual(cuenta):
        """Genera documento individual para una cuenta"""
        cuenta_numero = cuenta[0]
        
        try:
            print(f"Generando documento para cuenta: {cuenta_numero}")
            
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT JUCEPLAN, "CTA BANCARIA", CARGOS_EMPRESA, FACT, IMPORTE, FECHA
                FROM servicios WHERE "CTA BANCARIA" = ?
            ''', (cuenta_numero,))
            
            servicios = cursor.fetchall()
            conn.close()
            
            print(f"Servicios encontrados: {len(servicios)}")
            
            context = {
                'cuenta_bancaria': cuenta_numero,
                'fecha_generacion': datetime.now().strftime("%d/%m/%Y"),
                'total_importe': cuenta[2],
                'total_servicios': cuenta[1],
                'servicios': servicios,
                'detalles_servicios': [
                    {
                        'juceplan': serv[0],
                        'cargo_empresa': serv[2],
                        'fact': serv[3],
                        'importe': serv[4],
                        'fecha': serv[5]
                    } for serv in servicios
                ]
            }
            
            doc = DocxTemplate(PLANTILLA_PATH)
            doc.render(context)
            os.makedirs("output", exist_ok=True)
            filename = f"output/Aviso_Corte_{cuenta_numero}.docx"
            doc.save(filename)
            
            print(f"Documento guardado: {filename}")
            
        except Exception as e:
            print(f"ERROR generando documento: {e}")
            raise

    # FilePicker para cargar Excel
    file_picker = ft.FilePicker(on_result=cargar_datos_desde_excel)
    page.overlay.append(file_picker)

    # Controles de interfaz
    search_field = ft.TextField(
        label="🔍 Buscar cuenta bancaria",
        on_change=filtrar_cuentas,
        expand=True,
        height=50,
        border_color=COLOR_PRIMARIO
    )

    upload_btn = ft.ElevatedButton(
        "📊 Cargar Excel",
        icon=ft.Icons.UPLOAD_FILE,
        on_click=lambda _: file_picker.pick_files(
            allow_multiple=False,
            allowed_extensions=["xlsx", "xls"]
        ),
        width=150,
        height=50,
        style=ft.ButtonStyle(
            color=ft.Colors.WHITE,
            bgcolor=COLOR_PRIMARIO,
            shape=ft.RoundedRectangleBorder(radius=10)
        )
    )

    generate_btn = ft.ElevatedButton(
        "📄 Exportar Word",
        icon=ft.Icons.DESCRIPTION,
        on_click=generar_documento,
        width=150,
        height=50,
        style=ft.ButtonStyle(
            color=ft.Colors.WHITE,
            bgcolor=COLOR_SECUNDARIO,
            shape=ft.RoundedRectangleBorder(radius=10)
        )
    )

    filtro_btn = ft.ElevatedButton(
        "🔻 Filtrar",
        icon=ft.Icons.FILTER_LIST,
        on_click=mostrar_menu_filtro,
        width=150,
        height=50,
        style=ft.ButtonStyle(
            color=ft.Colors.WHITE,
            bgcolor=COLOR_TERCIARIO,
            shape=ft.RoundedRectangleBorder(radius=10)
        )
    )

    cuentas_container = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=True
    )

    selected_counter = ft.Text(
        "0 cuentas seleccionadas", 
        weight=ft.FontWeight.BOLD,
        color=COLOR_PRIMARIO
    )
    
    loading_text = ft.Text("", color=COLOR_PRIMARIO)

    progress_bar = ft.ProgressBar(
        value=0,
        visible=False,
        width=400,
        color=COLOR_PRIMARIO
    )

    def inicializar_app():
        """Inicializa la aplicación"""
        nonlocal cuentas_data
        cuentas_data = obtener_cuentas_bancarias()
        controles_cuentas.clear()
        cuentas_container.controls.clear()
        
        aplicar_filtro(filtro_actual)
        actualizar_contadores()
        page.update()

    # Layout principal
    page.add(
        ft.Column([
            ft.Text("AVISO DE CORTE", 
                   size=24, 
                   weight=ft.FontWeight.BOLD,
                   color=COLOR_PRIMARIO,
                   text_align=ft.TextAlign.CENTER),
            
            ft.Row([search_field], alignment=ft.MainAxisAlignment.CENTER),
            
            ft.Row([
                upload_btn,
                generate_btn,
                filtro_btn
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
            
            loading_text,
            ft.Divider(color=COLOR_PRIMARIO),
            cuentas_container,
            ft.Divider(color=COLOR_PRIMARIO),
            selected_counter,
            progress_bar
        ], spacing=15)
    )

    # Inicializar aplicación
    inicializar_app()

if __name__ == "__main__":
    ft.app(target=main)