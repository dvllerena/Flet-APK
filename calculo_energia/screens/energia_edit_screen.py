"""
Pantalla de edición/creación de registros de energía
"""

import flet as ft
from typing import Dict, Any, Optional, Callable
from datetime import datetime
import calendar

from calculo_energia.services.energia_service import EnergiaService
from calculo_energia.models.energia_barra_model import EnergiaBarra
from core.logger import get_logger


class EnergiaEditScreen:
    """Pantalla para editar/crear registros de energía"""
    
    def __init__(self, app, params: Dict[str, Any] = None):
        self.app = app
        self.page = app.page
        self.logger = get_logger(__name__)
        self.energia_service = EnergiaService()
        
        # Parámetros
        self.params = params or {}
        self.mode = self.params.get('mode', 'create')  # 'create' o 'edit'
        self.registro_id = self.params.get('registro_id')
        self.callback = self.params.get('callback')
        
        # Estado
        self.current_registro: Optional[EnergiaBarra] = None
        self.municipios = []
        self.is_loading = False
        
        # Controles de interfaz
        self.municipio_dropdown = None
        self.año_field = None
        self.mes_dropdown = None
        self.energia_field = None
        self.observaciones_field = None
        self.save_button = None
        self.cancel_button = None
        self.loading_indicator = None
        
        # Cargar datos iniciales
        self._load_initial_data()
    
    def _load_initial_data(self):
        """Carga datos iniciales"""
        try:
            # Cargar municipios
            self.municipios = self.energia_service.get_municipios()
            
            # Si es modo edición, cargar el registro
            if self.mode == 'edit' and self.registro_id:
                self.current_registro = self.energia_service.get_energia_by_id(self.registro_id)
                if not self.current_registro:
                    self.logger.error(f"Registro no encontrado: {self.registro_id}")
            
            self.logger.info(f"Datos iniciales cargados - Modo: {self.mode}")
            
        except Exception as e:
            self.logger.error(f"Error cargando datos iniciales: {e}")
    
    def build(self) -> ft.Container:
        """Construye la interfaz de edición"""
        
        # Header
        header = self._build_header()
        
        # Formulario
        form = self._build_form()
        
        # Botones de acción
        actions = self._build_actions()
        
        # Indicador de carga
        self.loading_indicator = ft.Container(
            content=ft.Column([
                ft.ProgressRing(width=40, height=40, color=ft.Colors.BLUE_500),
                ft.Text("Procesando...", size=14, color=ft.Colors.BLUE_600)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            alignment=ft.alignment.center,
            visible=False,
            padding=20
        )
        
        # Contenedor principal
        main_content = ft.Column([
            header,
            ft.Container(height=20),
            form,
            ft.Container(height=30),
            actions,
            self.loading_indicator
        ], 
        scroll=ft.ScrollMode.AUTO,
        expand=True
        )
        
        return ft.Container(
            content=main_content,
            padding=20,
            expand=True,
            bgcolor=ft.Colors.GREY_50
        )
    
    def _build_header(self) -> ft.Container:
        """Construye el header"""
        title = "Nuevo Registro de Energía" if self.mode == 'create' else "Editar Registro de Energía"
        icon = ft.Icons.ADD_CIRCLE if self.mode == 'create' else ft.Icons.EDIT
        
        return ft.Container(
            content=ft.Row([
                ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    tooltip="Volver",
                    on_click=self._on_back_click,
                    icon_color=ft.Colors.BLUE_600
                ),
                ft.Icon(icon, size=32, color=ft.Colors.BLUE_600),
                ft.Text(
                    title,
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE_800
                ),
                ft.Container(expand=True),
                ft.Chip(
                    label=ft.Text(self.mode.upper(), size=12, weight=ft.FontWeight.BOLD),
                    bgcolor=ft.Colors.BLUE_100 if self.mode == 'create' else ft.Colors.ORANGE_100,
                    color=ft.Colors.BLUE_800 if self.mode == 'create' else ft.Colors.ORANGE_800
                )
            ], alignment=ft.MainAxisAlignment.START, spacing=15),
            padding=ft.padding.symmetric(horizontal=20, vertical=15),
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            border=ft.border.all(1, ft.Colors.BLUE_100)
        )
    
    def _build_form(self) -> ft.Container:
        """Construye el formulario"""
        
        # Dropdown de municipio
        municipio_options = [
            ft.dropdown.Option(key=str(m['id']), text=f"{m['nombre']} ({m['codigo']})")
            for m in self.municipios
        ]
        
        self.municipio_dropdown = ft.Dropdown(
            label="Municipio *",
            options=municipio_options,
            width=400,
            disabled=self.mode == 'edit',  # No se puede cambiar en edición
            hint_text="Seleccione un municipio"
        )
        
        # Campo de año
        self.año_field = ft.TextField(
            label="Año *",
            width=150,
            keyboard_type=ft.KeyboardType.NUMBER,
            hint_text="2024"
        )
        
        # Dropdown de mes
        meses = [
            ("1", "Enero"), ("2", "Febrero"), ("3", "Marzo"), ("4", "Abril"),
            ("5", "Mayo"), ("6", "Junio"), ("7", "Julio"), ("8", "Agosto"),
            ("9", "Septiembre"), ("10", "Octubre"), ("11", "Noviembre"), ("12", "Diciembre")
        ]
        
        self.mes_dropdown = ft.Dropdown(
            label="Mes *",
            options=[ft.dropdown.Option(key=mes[0], text=mes[1]) for mes in meses],
            width=200,
            disabled=self.mode == 'edit'  # No se puede cambiar en edición
        )
        
        # Campo de energía
        self.energia_field = ft.TextField(
            label="Energía (MWh) *",
            width=200,
            keyboard_type=ft.KeyboardType.NUMBER,
            hint_text="0.0",
            suffix_text="MWh"
        )
        
        # Campo de observaciones
        self.observaciones_field = ft.TextField(
            label="Observaciones",
            width=600,
            multiline=True,
            min_lines=3,
            max_lines=5,
            hint_text="Observaciones adicionales (opcional)"
        )
        
        # Llenar campos si es modo edición
        if self.mode == 'edit' and self.current_registro:
            self._populate_form()
        elif self.mode == 'create':
            # Valores por defecto para creación
            self.año_field.value = str(self.params.get('año', datetime.now().year))
            self.mes_dropdown.value = str(self.params.get('mes', datetime.now().month))
        
        # Layout del formulario
        form_content = ft.Column([
            ft.Text(
                "Información del Registro",
                size=18,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLUE_800
            ),
            ft.Container(height=15),
            
            # Fila 1: Municipio
            ft.Row([
                self.municipio_dropdown
            ]),
            ft.Container(height=15),
            
            # Fila 2: Período
            ft.Row([
                self.año_field,
                ft.Container(width=20),
                self.mes_dropdown
            ]),
            ft.Container(height=15),
            
            # Fila 3: Energía
            ft.Row([
                self.energia_field
            ]),
            ft.Container(height=15),
            
            # Fila 4: Observaciones
            ft.Row([
                self.observaciones_field
            ]),
            
            ft.Container(height=20),
            
            # Información adicional
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.INFO_OUTLINE, size=16, color=ft.Colors.BLUE_500),
                        ft.Text("Campos marcados con * son obligatorios", size=12, color=ft.Colors.BLUE_600)
                    ], spacing=5),
                    ft.Container(height=5),
                    ft.Row([
                        ft.Icon(ft.Icons.WARNING_OUTLINED, size=16, color=ft.Colors.ORANGE_500),
                        ft.Text("No se puede duplicar municipio y período", size=12, color=ft.Colors.ORANGE_600)
                    ], spacing=5)
                ]),
                padding=15,
                bgcolor=ft.Colors.BLUE_50,
                border_radius=8,
                border=ft.border.all(1, ft.Colors.BLUE_200)
            )
        ])
        
        return ft.Container(
            content=form_content,
            padding=30,
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            border=ft.border.all(1, ft.Colors.BLUE_100)
        )
    
    def _build_actions(self) -> ft.Container:
        """Construye los botones de acción"""
        
        self.cancel_button = ft.ElevatedButton(
            content=ft.Row([
                ft.Icon(ft.Icons.CANCEL, size=18),
                ft.Text("Cancelar")
            ], spacing=8),
            on_click=self._on_cancel_click,
            bgcolor=ft.Colors.GREY_600,
            color=ft.Colors.WHITE,
            width=150
        )
        
        save_text = "Crear Registro" if self.mode == 'create' else "Guardar Cambios"
        save_icon = ft.Icons.ADD if self.mode == 'create' else ft.Icons.SAVE
        
        self.save_button = ft.ElevatedButton(
            content=ft.Row([
                ft.Icon(save_icon, size=18),
                ft.Text(save_text)
            ], spacing=8),
            on_click=self._on_save_click,
            bgcolor=ft.Colors.BLUE_600,
            color=ft.Colors.WHITE,
            width=180
        )
        
        return ft.Container(
            content=ft.Row([
                ft.Container(expand=True),  # Spacer
                self.cancel_button,
                ft.Container(width=20),
                self.save_button
            ], alignment=ft.MainAxisAlignment.END),
            padding=20,
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            border=ft.border.all(1, ft.Colors.BLUE_100)
        )
    
    def _populate_form(self):
        """Llena el formulario con datos del registro actual"""
        if not self.current_registro:
            return
        
        try:
            self.municipio_dropdown.value = str(self.current_registro.municipio_id)
            self.año_field.value = str(self.current_registro.año)
            self.mes_dropdown.value = str(self.current_registro.mes)
            self.energia_field.value = str(self.current_registro.energia_mwh)
            self.observaciones_field.value = self.current_registro.observaciones or ""
            
            self.logger.info("Formulario poblado con datos existentes")
            
        except Exception as e:
            self.logger.error(f"Error poblando formulario: {e}")
    
    def _validate_form(self) -> tuple[bool, str]:
        """Valida el formulario"""
        try:
            # Validar campos obligatorios
            if not self.municipio_dropdown.value:
                return False, "Debe seleccionar un municipio"
            
            if not self.año_field.value:
                return False, "Debe ingresar el año"
            
            if not self.mes_dropdown.value:
                return False, "Debe seleccionar el mes"
            
            if not self.energia_field.value:
                return False, "Debe ingresar la energía"
            
            # Validar tipos de datos
            try:
                año = int(self.año_field.value)
                if año < 2000 or año > 2100:
                    return False, "Año debe estar entre 2000 y 2100"
            except ValueError:
                return False, "Año debe ser un número válido"
            
            try:
                mes = int(self.mes_dropdown.value)
                if mes < 1 or mes > 12:
                    return False, "Mes debe estar entre 1 y 12"
            except ValueError:
                return False, "Mes debe ser un número válido"
            
            try:
                energia = float(self.energia_field.value)
                if energia < 0:
                    return False, "Energía no puede ser negativa"
            except ValueError:
                return False, "Energía debe ser un número válido"
            
            # Validar duplicados solo en modo creación
            if self.mode == 'create':
                municipio_id = int(self.municipio_dropdown.value)
                existing = self.energia_service.get_energia_by_municipio_periodo(municipio_id, año, mes)
                if existing:
                    municipio_nombre = next((m['nombre'] for m in self.municipios if m['id'] == municipio_id), 'Desconocido')
                    return False, f"Ya existe un registro para {municipio_nombre} en {mes:02d}/{año}"
            
            return True, ""
            
        except Exception as e:
            self.logger.error(f"Error validando formulario: {e}")
            return False, "Error en validación"
    
    def _on_save_click(self, e):
        """Maneja el clic del botón guardar"""
        try:
            # Validar formulario
            is_valid, error_message = self._validate_form()
            if not is_valid:
                self._show_error(error_message)
                return
            
            self._set_loading(True)
            
            # Obtener usuario actual
            current_user = self.app.get_current_user()
            user_id = current_user.get('id', 1) if current_user else 1
            
            # Crear objeto EnergiaBarra
            energia = EnergiaBarra(
                id=self.current_registro.id if self.current_registro else None,
                municipio_id=int(self.municipio_dropdown.value),
                año=int(self.año_field.value),
                mes=int(self.mes_dropdown.value),
                energia_mwh=float(self.energia_field.value),
                observaciones=self.observaciones_field.value.strip() or None
            )
            
            # Guardar según el modo
            success = False
            if self.mode == 'create':
                success = self.energia_service.crear_energia(energia, user_id)
                action = "creado"
            else:
                success = self.energia_service.actualizar_energia(energia, user_id)
                action = "actualizado"
            
            if success:
                municipio_nombre = next((m['nombre'] for m in self.municipios if m['id'] == energia.municipio_id), 'Desconocido')
                self._show_success(f"Registro {action} exitosamente para {municipio_nombre}")
                
                # Llamar callback si existe
                if self.callback:
                    self.callback()
                
                # Volver a la pantalla anterior
                self._navigate_back()
            else:
                self._show_error(f"Error al {action.replace('ado', 'ar')} el registro")
                
        except Exception as ex:
            self.logger.error(f"Error guardando registro: {ex}")
            self._show_error("Error del sistema al guardar")
        finally:
            self._set_loading(False)
    
    def _on_cancel_click(self, e):
        """Maneja el clic del botón cancelar"""
        self._navigate_back()
    
    def _on_back_click(self, e):
        """Maneja el clic del botón volver"""
        self._navigate_back()
    
    def _navigate_back(self):
        """Navega de vuelta - CORREGIDO"""
        try:
            # ✅ USAR NOMBRE CORRECTO
            self.app.navigate_to("calculo_energia")
        except Exception as e:
            self.logger.error(f"Error navegando de vuelta: {e}") 
    def _set_loading(self, loading: bool):
        """Controla el estado de carga"""
        self.is_loading = loading
        self.loading_indicator.visible = loading
        
        # Deshabilitar controles durante carga
        self.municipio_dropdown.disabled = loading or (self.mode == 'edit')
        self.año_field.disabled = loading
        self.mes_dropdown.disabled = loading or (self.mode == 'edit')
        self.energia_field.disabled = loading
        self.observaciones_field.disabled = loading
        self.save_button.disabled = loading
        self.cancel_button.disabled = loading
        
        if loading:
            self.save_button.content = ft.Row([
                ft.ProgressRing(width=14, height=14, stroke_width=2, color=ft.Colors.WHITE),
                ft.Text("Guardando...")
            ], spacing=8)
        else:
            save_text = "Crear Registro" if self.mode == 'create' else "Guardar Cambios"
            save_icon = ft.Icons.ADD if self.mode == 'create' else ft.Icons.SAVE
            self.save_button.content = ft.Row([
                ft.Icon(save_icon, size=18),
                ft.Text(save_text)
            ], spacing=8)
        
        self.page.update()
    
    def _show_success(self, message: str):
        """Muestra mensaje de éxito"""
        try:
            snack_bar = ft.SnackBar(
                content=ft.Row([
                    ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.WHITE),
                    ft.Text(message, color=ft.Colors.WHITE)
                ]),
                bgcolor=ft.Colors.GREEN_600
            )
            self.page.snack_bar = snack_bar
            snack_bar.open = True
            self.page.update()
        except Exception as e:
            self.logger.error(f"Error mostrando mensaje de éxito: {e}")
    
    def _show_error(self, message: str):
        """Muestra mensaje de error"""
        try:
            snack_bar = ft.SnackBar(
                content=ft.Row([
                    ft.Icon(ft.Icons.ERROR, color=ft.Colors.WHITE),
                    ft.Text(message, color=ft.Colors.WHITE)
                ]),
                bgcolor=ft.Colors.RED_600
            )
            self.page.snack_bar = snack_bar
            snack_bar.open = True
            self.page.update()
        except Exception as e:
            self.logger.error(f"Error mostrando mensaje de error: {e}")
    
    def get_form_data(self) -> Dict[str, Any]:
        """Obtiene los datos actuales del formulario"""
        try:
            return {
                'municipio_id': int(self.municipio_dropdown.value) if self.municipio_dropdown.value else None,
                'año': int(self.año_field.value) if self.año_field.value else None,
                'mes': int(self.mes_dropdown.value) if self.mes_dropdown.value else None,
                'energia_mwh': float(self.energia_field.value) if self.energia_field.value else None,
                'observaciones': self.observaciones_field.value.strip() or None
            }
        except Exception as e:
            self.logger.error(f"Error obteniendo datos del formulario: {e}")
            return {}
    
    def reset_form(self):
        """Resetea el formulario"""
        try:
            self.municipio_dropdown.value = None
            self.año_field.value = ""
            self.mes_dropdown.value = None
            self.energia_field.value = ""
            self.observaciones_field.value = ""
            self.page.update()
        except Exception as e:
            self.logger.error(f"Error reseteando formulario: {e}")
