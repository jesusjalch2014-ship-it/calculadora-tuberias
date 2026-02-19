"""
APP DE INVENTARIO DE TUBERIAS - VERSION SIMPLE
Desarrollada para Android usando Kivy
"""

import json
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.core.window import Window
from kivy.utils import platform

# Configurar tamaño de ventana para prueba en PC
if platform == 'win' or platform == 'macosx' or platform == 'linux':
    Window.size = (400, 700)

# DATOS DE TUBERIAS (Diccionario con los pesos teóricos)
# Formato: { "diámetro_schedule": peso_kg_por_metro }
datos_tuberias = {
    # Diámetro 1/2 pulgada
    "1/2_SCH 40": 1.27, "1/2_SCH 80": 1.62, "1/2_160": 2.09, "1/2_STD": 1.27, "1/2_XS": 1.62, "1/2_XXS": 2.31,
    
    # Diámetro 3/4 pulgada
    "3/4_SCH 40": 1.69, "3/4_SCH 80": 2.20, "3/4_160": 2.90, "3/4_STD": 1.69, "3/4_XS": 2.20, "3/4_XXS": 3.09,
    
    # Diámetro 1 pulgada
    "1_SCH 40": 2.50, "1_SCH 80": 3.24, "1_160": 4.17, "1_STD": 2.50, "1_XS": 3.24, "1_XXS": 4.56,
    
    # Diámetro 1 1/2 pulgada
    "1 1/2_SCH 40": 4.05, "1 1/2_SCH 80": 5.41, "1 1/2_160": 6.97, "1 1/2_STD": 4.05, "1 1/2_XS": 5.41, "1 1/2_XXS": 7.58,
    
    # Diámetro 2 pulgadas
    "2_SCH 40": 5.44, "2_SCH 80": 7.48, "2_160": 10.11, "2_STD": 5.44, "2_XS": 7.48, "2_XXS": 12.51,
    
    # Diámetro 3 pulgadas
    "3_SCH 40": 11.29, "3_SCH 80": 15.27, "3_160": 21.22, "3_STD": 11.29, "3_XS": 15.27, "3_XXS": 22.12,
    
    # Diámetro 4 pulgadas
    "4_SCH 40": 16.07, "4_SCH 80": 21.63, "4_160": 32.13, "4_STD": 16.07, "4_XS": 21.63, "4_XXS": 31.45,
    
    # Diámetro 6 pulgadas
    "6_SCH 40": 28.26, "6_SCH 80": 37.69, "6_160": 55.86, "6_STD": 28.26, "6_XS": 37.69, "6_XXS": 50.21,
    
    # Diámetro 8 pulgadas
    "8_SCH 40": 42.55, "8_SCH 80": 55.90, "8_160": 80.62, "8_STD": 42.55, "8_XS": 55.90, "8_XXS": 69.32,
    
    # Diámetro 10 pulgadas
    "10_SCH 40": 60.28, "10_SCH 80": 78.43, "10_160": 108.9, "10_STD": 60.28, "10_XS": 78.43, "10_XXS": 94.56,
    
    # Diámetro 12 pulgadas
    "12_SCH 40": 79.45, "12_SCH 80": 102.6, "12_160": 140.5, "12_STD": 79.45, "12_XS": 102.6, "12_XXS": 119.8,
    
    # Diámetro 14 pulgadas
    "14_SCH 40": 104.1, "14_SCH 80": 133.2, "14_STD": 104.1, "14_XS": 133.2, "14_XXS": 152.3,
    
    # Diámetro 16 pulgadas
    "16_SCH 40": 119.7, "16_SCH 80": 153.6, "16_STD": 119.7, "16_XS": 153.6, "16_XXS": 173.8,
    
    # Diámetro 18 pulgadas
    "18_SCH 40": 141.5, "18_SCH 80": 182.4, "18_STD": 141.5, "18_XS": 182.4, "18_XXS": 206.9,
    
    # Diámetro 20 pulgadas
    "20_SCH 40": 166.5, "20_SCH 80": 214.2, "20_STD": 166.5, "20_XS": 214.2, "20_XXS": 242.1,
    
    # Diámetro 24 pulgadas
    "24_SCH 40": 220.3, "24_SCH 80": 283.7, "24_STD": 220.3, "24_XS": 283.7, "24_XXS": 318.5,
}

class ItemTuberia:
    """Clase para almacenar cada item agregado"""
    def __init__(self, diametro, schedule, metros, peso_por_metro):
        self.diametro = diametro
        self.schedule = schedule
        self.metros = metros
        self.peso_por_metro = peso_por_metro
        self.subtotal = metros * peso_por_metro

class AppTuberias(BoxLayout):
    """Clase principal de la aplicación"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10
        
        # Lista para guardar los items agregados
        self.items_tuberias = []
        
        # Título
        self.add_widget(Label(
            text='CALCULADORA DE TUBERÍAS',
            size_hint_y=0.08,
            font_size='20sp',
            bold=True
        ))
        
        # --- Área de selección y entrada de datos ---
        panel_seleccion = BoxLayout(orientation='vertical', size_hint_y=0.25, spacing=5)
        
        # Diámetro
        panel_seleccion.add_widget(Label(text='Diámetro:', halign='left', size_hint_y=0.2))
        self.spinner_diametro = Spinner(
            text='Seleccionar',
            values=('1/2', '3/4', '1', '1 1/2', '2', '3', '4', '6', '8', '10', '12', '14', '16', '18', '20', '24'),
            size_hint_y=0.2
        )
        panel_seleccion.add_widget(self.spinner_diametro)
        
        # Schedule
        panel_seleccion.add_widget(Label(text='Schedule:', halign='left', size_hint_y=0.2))
        self.spinner_schedule = Spinner(
            text='Seleccionar',
            values=('SCH 40', 'SCH 80', '160', 'STD', 'XS', 'XXS'),
            size_hint_y=0.2
        )
        panel_seleccion.add_widget(self.spinner_schedule)
        
        # Metros lineales
        panel_seleccion.add_widget(Label(text='Metros:', halign='left', size_hint_y=0.2))
        self.input_metros = TextInput(
            text='0',
            input_filter='float',
            multiline=False,
            size_hint_y=0.2
        )
        panel_seleccion.add_widget(self.input_metros)
        
        self.add_widget(panel_seleccion)
        
        # Botón Agregar
        btn_agregar = Button(
            text='AGREGAR A LA LISTA',
            size_hint_y=0.08,
            background_color=(0.2, 0.6, 1, 1)
        )
        btn_agregar.bind(on_press=self.agregar_item)
        self.add_widget(btn_agregar)
        
        # Área de resultados (tabla)
        self.add_widget(Label(
            text='LISTA DE MATERIALES:',
            size_hint_y=0.05,
            bold=True
        ))
        
        # Cabecera de la tabla
        cabecera = GridLayout(cols=4, size_hint_y=0.05)
        cabecera.add_widget(Label(text='Diámetro', bold=True))
        cabecera.add_widget(Label(text='SCH', bold=True))
        cabecera.add_widget(Label(text='Metros', bold=True))
        cabecera.add_widget(Label(text='Subtotal', bold=True))
        self.add_widget(cabecera)
        
        # ScrollView para la tabla
        self.tabla_resultados = GridLayout(cols=4, spacing=2, size_hint_y=None)
        self.tabla_resultados.bind(minimum_height=self.tabla_resultados.setter('height'))
        
        scroll = ScrollView(size_hint_y=0.4)
        scroll.add_widget(self.tabla_resultados)
        self.add_widget(scroll)
        
        # Total general
        panel_total = BoxLayout(orientation='horizontal', size_hint_y=0.08)
        panel_total.add_widget(Label(text='TOTAL:', bold=True, font_size='18sp'))
        self.label_total = Label(text='0 kg', bold=True, font_size='18sp')
        panel_total.add_widget(self.label_total)
        self.add_widget(panel_total)
        
        # Botón Limpiar
        btn_limpiar = Button(
            text='LIMPIAR TODO',
            size_hint_y=0.06,
            background_color=(1, 0.3, 0.3, 1)
        )
        btn_limpiar.bind(on_press=self.limpiar_todo)
        self.add_widget(btn_limpiar)
    
    def obtener_peso_unitario(self, diametro, schedule):
        """Obtiene el peso por metro del diccionario"""
        clave = f"{diametro}_{schedule}"
        return datos_tuberias.get(clave, 0)
    
    def agregar_item(self, instance):
        """Función para agregar un item a la lista"""
        diametro = self.spinner_diametro.text
        schedule = self.spinner_schedule.text
        metros_text = self.input_metros.text
        
        # Validaciones
        if diametro == 'Seleccionar' or schedule == 'Seleccionar':
            self.mostrar_mensaje("Error: Selecciona diámetro y schedule")
            return
        
        try:
            metros = float(metros_text)
            if metros <= 0:
                self.mostrar_mensaje("Error: Los metros deben ser mayor a 0")
                return
        except:
            self.mostrar_mensaje("Error: Ingresa un número válido")
            return
        
        peso_unitario = self.obtener_peso_unitario(diametro, schedule)
        
        if peso_unitario == 0:
            self.mostrar_mensaje("Error: Combinación no válida")
            return
        
        # Crear item y agregar a la lista
        item = ItemTuberia(diametro, schedule, metros, peso_unitario)
        self.items_tuberias.append(item)
        
        # Actualizar la tabla
        self.actualizar_tabla()
        
        # Limpiar campos
        self.input_metros.text = '0'
    
    def actualizar_tabla(self):
        """Actualiza la tabla de resultados"""
        self.tabla_resultados.clear_widgets()
        total_general = 0
        
        for item in self.items_tuberias:
            self.tabla_resultados.add_widget(Label(text=item.diametro, size_hint_y=None, height=30))
            self.tabla_resultados.add_widget(Label(text=item.schedule, size_hint_y=None, height=30))
            self.tabla_resultados.add_widget(Label(text=str(item.metros), size_hint_y=None, height=30))
            self.tabla_resultados.add_widget(Label(text=f"{item.subtotal:.1f}", size_hint_y=None, height=30))
            total_general += item.subtotal
        
        self.label_total.text = f"{total_general:.1f} kg"
    
    def limpiar_todo(self, instance):
        """Limpia toda la lista"""
        self.items_tuberias = []
        self.actualizar_tabla()
        self.spinner_diametro.text = 'Seleccionar'
        self.spinner_schedule.text = 'Seleccionar'
        self.input_metros.text = '0'
    
    def mostrar_mensaje(self, mensaje):
        """Muestra un mensaje temporal (simulado)"""
        # En una app real usaríamos popup, pero por simplicidad usamos print
        print(mensaje)
        # También podemos cambiar temporalmente el texto del botón
        original_text = self.label_total.text
        self.label_total.text = mensaje
        from kivy.clock import Clock
        Clock.schedule_once(lambda dt: setattr(self.label_total, 'text', original_text), 2)

class TuberiasApp(App):
    """Clase principal de la aplicación Kivy"""
    def build(self):
        return AppTuberias()

if __name__ == '__main__':
    TuberiasApp().run()