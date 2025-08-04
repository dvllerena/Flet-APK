import flet as ft

def main(page: ft.Page):
    page.title = "App de Prueba Flet"  # Título de la app
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"
    
    # Contador
    txt_number = ft.TextField(value="0", text_align="right", width=100)
    
    def minus_click(e):
        txt_number.value = str(int(txt_number.value) - 1)
        page.update()
    
    def plus_click(e):
        txt_number.value = str(int(txt_number.value) + 1)
        page.update()
    
    # Saludo
    txt_name = ft.TextField(label="Tu nombre")
    greetings = ft.Column()
    
    def say_hello(e):
        greetings.controls.append(ft.Text(f"¡Hola, {txt_name.value}!"))
        txt_name.value = ""
        page.update()
    
    # Diseño de la interfaz
    page.add(
        ft.Row(
            [
                ft.IconButton(ft.icons.REMOVE, on_click=minus_click),
                txt_number,
                ft.IconButton(ft.icons.ADD, on_click=plus_click),
            ],
            alignment="center",
        ),
        ft.Text("¡Prueba CodeMagic con Flet!", size=20),
        txt_name,
        ft.ElevatedButton("Saludar", on_click=say_hello),
        greetings,
    )

# Ejecutar la app (modo escritorio o móvil)
ft.app(target=main)