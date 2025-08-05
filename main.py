import flet as ft
import os
import json

# Paleta de colores UNE
UNE_PRIMARY = "#FF7220"
UNE_SECONDARY = "#0A079E"
UNE_ACCENT = "#F37021"
UNE_LIGHT = "#000000"
UNE_DARK = "#fffff3"
UNE_BACKGROUND = "#122DC2"

def cargar_datos():
    ruta_base = os.path.abspath(os.path.dirname(__file__))
    ruta_json = os.path.join(ruta_base, "assets", "datos.json")
    if not os.path.exists(ruta_json):
        raise FileNotFoundError(f"Archivo no encontrado: {ruta_json}")
    with open(ruta_json, encoding="utf-8") as f:
        return json.load(f)

def main(page: ft.Page):
    # Configuración básica de la página
    page.title = "Directorio UNE"
    page.theme_mode = "dark"
    page.window_width = 400
    page.window_height = 720
    page.window_resizable = False
    page.bgcolor = UNE_BACKGROUND
    page.padding = 0
    
    # Tema personalizado
    page.theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary=UNE_PRIMARY,
            secondary=UNE_SECONDARY,
            surface=UNE_DARK,
            background=UNE_BACKGROUND,
            on_primary=UNE_LIGHT,
            on_secondary=UNE_LIGHT,
            on_surface=UNE_LIGHT,
        ),
        text_theme=ft.TextTheme(
            title_large=ft.TextStyle(size=22, weight="bold", color=UNE_LIGHT),
            title_medium=ft.TextStyle(size=18, weight="w600", color=UNE_ACCENT),
            body_medium=ft.TextStyle(size=14, color=UNE_LIGHT),
            body_small=ft.TextStyle(size=12, color=UNE_LIGHT),
        ),
    )

    datos = cargar_datos()
    nombres_areas = [area["nombre"] for area in datos["areas"]]

    # Componente principal para mostrar las extensiones
    extensiones_view = ft.ListView(
        expand=True,
        spacing=10,
        padding=20,
        auto_scroll=False
    )

    def cargar_area(nombre):
        extensiones_view.controls.clear()

        # Header con logo y pizarra
        header = ft.Container(
            content=ft.Column([
                ft.Image(src="assets/logo-une.png", height=50),
                ft.Container(
                    bgcolor=UNE_PRIMARY,
                    padding=15,
                    border_radius=10,
                    content=ft.Text(
                        f"Pizarra: {datos['pizarra']}", 
                        style="title_medium",
                        text_align=ft.TextAlign.CENTER
                    ),
                )
            ], spacing=10),
            margin=ft.margin.only(bottom=20)
        )
        extensiones_view.controls.append(header)

        # Contenido del área seleccionada
        for area in datos["areas"]:
            if area["nombre"] == nombre:
                # Título del área
                extensiones_view.controls.append(
                    ft.Container(
                        padding=ft.padding.only(bottom=10),
                        content=ft.Text(
                            area["nombre"].upper(), 
                            style="title_medium",
                            text_align=ft.TextAlign.CENTER
                        )
                    )
                )
                
                # Lista de extensiones
                for ext in area["extensiones"]:
                    extensiones_view.controls.append(
                        ft.Container(
                            content=ft.Card(
                                elevation=8,
                                color=UNE_DARK,
                                shadow_color=UNE_ACCENT,
                                content=ft.Container(
                                    border=ft.border.all(1, UNE_SECONDARY),
                                    border_radius=10,
                                    padding=15,
                                    content=ft.Column([
                                        ft.Text(
                                            ext["cargo"], 
                                            style="body_medium",
                                            weight="bold"
                                        ),
                                        ft.Divider(height=10, color="transparent"),
                                        ft.Row([
                                            ft.Icon(ft.Icons.PHONE, color=UNE_ACCENT),
                                            ft.Text(
                                                f"Extensión: {ext['extension']}", 
                                                style="body_medium"
                                            ),
                                        ], spacing=10)
                                    ])
                                )
                            ),
                            margin=ft.margin.only(bottom=10)
                        )
                    )
        
        page.update()

    # Drawer de navegación
    drawer = ft.NavigationDrawer(
        bgcolor=UNE_DARK,
        indicator_color=UNE_ACCENT,
        selected_index=0,
        shadow_color=UNE_ACCENT,
        surface_tint_color=UNE_PRIMARY
    )

    def seleccionar_area(e):
        if drawer.selected_index is not None and drawer.selected_index < len(nombres_areas):
            cargar_area(nombres_areas[drawer.selected_index])

    drawer.on_change = seleccionar_area
    
    # Items del drawer - Versión corregida sin label_style
    drawer.controls = [
        ft.Container(
            height=150,
            padding=20,
            bgcolor=UNE_PRIMARY,
            content=ft.Column([
                ft.Image(src="assets/logo-une.png", height=50),
                ft.Text("Seleccione un área", style="title_medium")
            ], spacing=10, alignment=ft.MainAxisAlignment.CENTER)
        ),
        ft.Divider(thickness=1, color=UNE_ACCENT)
    ] + [
        ft.NavigationDrawerDestination(
            icon=ft.Icons.BUSINESS_OUTLINED,
            selected_icon=ft.Icons.BUSINESS,
            label=nombre
        ) for nombre in nombres_areas
    ]

    def abrir_drawer(e):
        drawer.open = True
        page.update()

    # AppBar superior
    appbar = ft.AppBar(
        title=ft.Text(datos["empresa"], style="title_large"),
        center_title=True,
        bgcolor=UNE_PRIMARY,
        toolbar_height=70,
        
    )

    # Cargar área inicial
    if nombres_areas:
        cargar_area(nombres_areas[0])

    # Añadir componentes a la página
    page.drawer = drawer
    page.appbar = appbar
    page.add(extensiones_view)

ft.app(target=main)