##################################################
##           DATOS DEL PROGRAMA                 ##
##################################################

#Los datos son variables que se pueden cambiar, se reflejan en todo el código

NOMBRE       = "Project NT"
VERSION      = "0.99 preview"
AUTOR        = "GAB"
CORREO       = ""
DESCRIPCION  = "Programa para escribir caracteres especiales del Esperanto"
CARACTERES   = "cx→ĉ  gx→ĝ  hx→ĥ  jx→ĵ  sx→ŝ  ux→ŭ"





##################################################
##        LIBRERIAS Y OBJETOS DE CONTROL        ##
##################################################
from pynput import keyboard            #Control de teclado

import tkinter as tk                   #Entorno gráfico
from tkinter import ttk
from tkinter import font

import pystray                         #Poner icono en la bandeja del sistema

import threading                       #Tareas en distintos hilos

import os                              #Acceso al sistema operativo (rutas, matar proceso)
import psutil                          #Verificar si un proceso está corriendo (instancia única)
import time                            #Controla tiempos (de espera)
import sys


import configparser                    #Para administrar archivos de configuración


from PIL import Image, ImageDraw       #Este controla el dibujado (exactametne de los iconos)
from PIL import ImageTk                #Poner el dibujo en las ventanas

import json                            #cargar archivos json (idiomas)





#############################################################
##              CONFIGURACIÓN E IDIOMAS [CEI]              ##
#############################################################

#### SECCION CONFIGURACION CONFIG.INI ####

#[ceicd] Configuración por defecto para crear el archivo config.ini
config_defecto = {
    'general': {
        'margen': 3,
        'idioma': 'es',
    },
    'inicio': {
        'iniciar_activado': 0,
        'iniciar_con_windows': 0,
    },
    'atajo': {
        'atajo': 'none',
    },
    'entrada': {
        'afijo': '2',
        'sufijo': 'x',
        'prefijo': '',
    },
    'deshacer': {
        'deshacer_cambio': '0',
        'atajo_deshacer': 'none',
        'deshacer_tecla': '0',
    }
}


#[ceiiu] Configuración para instancia única
config = configparser.ConfigParser()
if getattr(sys, 'frozen', False):
    ruta_exe = os.path.dirname(sys.executable)
else:
    ruta_exe = os.path.dirname(os.path.abspath(__file__))

config_file = os.path.join(ruta_exe, "config.ini")

if os.name == 'nt':
    import ctypes
    mutex = ctypes.windll.kernel32.CreateMutexW(None, False, "ProyectoNT_Mutex")
    if ctypes.windll.kernel32.GetLastError() == 183:
        sys.exit()
else:
    import socket
    socket_lock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        socket_lock.bind(('localhost', 47832))
    except:
        sys.exit()

if os.path.exists(config_file):
    config.read(config_file)
else:
    config.read_dict(config_defecto)
    with open(config_file, 'w') as f:
        config.write(f)
        
        

#[ceilectura] Esta es la sección de lectura del archivo config.ini
margen = int(config['general']['margen'])
activado = int(config['inicio']['iniciar_activado'])
windows_arranque = int(config['inicio']['iniciar_con_windows'])
estilo_entrada_guardado = config['entrada']['afijo']
caracter_prefijo_guardado = config['entrada']['prefijo']
caracter_sufijo_guardado = config['entrada']['sufijo']
deshacer_cambio = int(config['deshacer']['deshacer_cambio'])
deshacer_tecla = int(config['deshacer']['deshacer_tecla'])
idioma = config['general']['idioma']


#[ceiguardado] Esta es la sección de guardado del archivo config.ini
def guardar_opciones():
    global margen
    margen = int(spinbox_margen.get())
    config['general']['margen'] = str(margen)
    config['general']['idioma'] = idiomas_codigos[lingvo.get()]
    config['inicio']['iniciar_activado'] = str(iniciar_activado.get())
    config['inicio']['iniciar_con_windows'] = str(var_windows.get())
    config['entrada']['afijo'] = estilo_entrada.get()
    config['entrada']['prefijo'] = entry_prefijo_estilo.get()
    config['entrada']['sufijo'] = entry_sufijo_estilo.get()
    config['deshacer']['deshacer_cambio'] = str(var_deshacer.get())
    config['deshacer']['atajo_deshacer'] = str(etiqueta_deshacer.cget("text"))
    config['deshacer']['deshacer_tecla'] = str(atajo_deshacer.get())
    with open(config_file, 'w') as f:
        config.write(f)
    generar_diccionario()
    inicio_arranque()
    ventana_opciones.withdraw()

def cancelar_opciones():
    ventana_opciones.withdraw()
      

##### SECCION IDIOMA #####

#[ceii] Carga el archivo de idioma idiomas.json
ruta_base = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
ruta_json = os.path.join(ruta_base, "idiomas.json")
with open(ruta_json, encoding="utf-8") as f:
    textos_idioma = json.load(f)

#[ceini] Cambia los nombres cortos a largos, para las opciones
nombres_idiomas = {
    "es": "Español",
    "en": "English",
    "eo": "Esperanto"
}
idiomas_codigos = {v: k for k, v in nombres_idiomas.items()}



#[ceiai] Ejecuta el cambio de idioma
def actualizar_idioma():
    global idioma
    global etiqueta_bandera, banderas
    
    idioma_anterior = idioma
    idioma = idiomas_codigos[lingvo.get()]
    
    for t in tooltips:
        t.texto = textos_idioma[idioma][t.clave]
    
    def recorrer(widget):
        try:
            texto_actual = widget.cget("text")
            for clave, valor in textos_idioma[idioma_anterior].items():
                if texto_actual == valor:
                    widget.config(text=textos_idioma[idioma][clave])
                    break
        except:
            pass
        for hijo in widget.winfo_children():
            recorrer(hijo)
            
    etiqueta_bandera.config(image=banderas[idioma])
    recorrer(ventana_opciones)
    crear_menu_icono()
    
nombres_teclas = {
    "ctrl_l": "Control L",
    "ctrl_r": "Control R",
    "alt_l": "Alt L",
    "alt_r": "Alt R",
    "shift": "Shift",
    "shift_l": "Shift L",
    "shift_r": "Shift R",
    "caps_lock": "Bloq Mayús",
    "tab": "Tab",
    "enter": "Enter",
    "backspace": "Retroceso",
    "delete": "Supr",
    "esc": "Escape",
    "space": "Espacio",
    "up": "Arriba",
    "down": "Abajo",
    "left": "Izquierda",
    "right": "Derecha",
}





#### SECCION INTERFAZ GRAFICA ####
    
#[ceicm] Crea el menu del boton derecho
def crear_menu_icono():
    global menu_icono
    menu_icono = pystray.Menu(
        pystray.MenuItem(lambda item: textos_idioma[idioma]["menu_desactivar"] if activado == 1 else textos_idioma[idioma]["menu_activar"], lambda: activar_script()),
        pystray.MenuItem(lambda item: textos_idioma[idioma]["menu_opciones"], lambda: ventana_opciones.deiconify()),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem(lambda item: textos_idioma[idioma]["menu_acerca"], lambda: ventana_acerca_de.deiconify()),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem(lambda item: textos_idioma[idioma]["menu_salir"], cerrar_app)
    )
    try:
        icono.menu = menu_icono
        icono.update_menu()
    except:
        pass
    
    
    
    
    
##################################################
##            VARIABLES GLOBALES                ##
##################################################

## Control del teclado
teclado = keyboard.Controller()        # Objeto para simular teclas

## Diccionario de reemplazos
diccionario_defecto = {"cx":"ĉ", "gx":"ĝ", "hx":"ĥ", "jx":"ĵ", "sx":"ŝ", "ux":"ŭ", "Cx":"Ĉ", "Gx":"Ĝ", "Hx":"Ĥ", "Jx":"Ĵ", "Sx":"Ŝ", "Ux":"Ŭ", "CX":"Ĉ", "GX":"Ĝ", "HX":"Ĥ", "JX":"Ĵ", "SX":"Ŝ", "UX":"Ŭ"}
diccionario = diccionario_defecto

## Buffer de teclas
buffer_lista = []                      # Guarda las últimas teclas presionadas

## Listener principal
listener = None

## Atajo de activación
atajo = None
teclas_atajo = []
listener_atajo = None
teclas_presionadas_atajo = []

## Deshacer
teclas_atajo_deshacer = []
escribiendo = False
buffer_deshacer_v2 = []
buffer_congelado = False

tooltips = []



##################################################
##           FUNCIONES GENERALES                ##
##################################################

## -- ICONOS --
## Dibuja los iconos verde y rojo que aparecen en la bandeja

def crear_icono(color_hex, tamaño=64):
    escala = tamaño / 64
    img = Image.new('RGBA', (tamaño, tamaño), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    hexagono = [(int(x*escala), int(y*escala)) for x,y in [(16,4), (48,4), (64,32), (48,60), (16,60), (0,32)]]
    estrella_outline = [(int(x*escala), int(y*escala)) for x,y in [(32,8), (38,23), (52,23), (42,32), (46,48), (32,39), (18,48), (22,32), (12,23), (26,23)]]
    estrella = [(int(x*escala), int(y*escala)) for x,y in [(32,15), (36,27), (47,27), (39,34), (42,46), (32,39), (22,46), (25,34), (17,27), (28,27)]]
    draw.polygon(hexagono, fill=color_hex)
    draw.polygon(estrella_outline, fill='black')
    draw.polygon(estrella, fill='white')
    return img


imagen_icono_activado = crear_icono('#009000', tamaño=64)       # Ícono verde — programa activo
imagen_icono_desactivado = crear_icono('#900000', tamaño=64) # Ícono rojo — programa inactivo
imagen_icono_grande = crear_icono('#009000', tamaño=100)


crear_icono = 0                                     # Exportar icono.ico — 0=no, 1=sí
if crear_icono == 1 and not os.path.exists("icono.ico"):
    imagen_icono_activado.save("icono.ico")

def al_iniciar_icono(icono):
    global listener
    listener = keyboard.Listener(on_press=al_presionar, on_release=al_soltar)
    listener.start()
    if activado == 1:
        import time
        time.sleep(0.15)
        icono.icon = imagen_icono_activado
        icono.title = NOMBRE + " (Activo)"



## -- CONTROL DEL PROGRAMA --
## Activa/desactiva el programa y lo cierra limpiamente

def activar_script():
    global icono, activado, listener
    if activado == 0:
        activado = 1
        icono.icon = imagen_icono_activado
        icono.title = NOMBRE + " (Activo)"
    else:
        activado = 0
        icono.icon = imagen_icono_desactivado
        icono.title = NOMBRE + " (Inactivo)"

def cerrar_app():                                   # Detiene el listener, cierra tkinter y mata el proceso
    if listener is not None:
        listener.stop()
    ventana_opciones.quit()
    icono.stop()
    os.kill(os.getpid(), 9)


## -- WINDOWS --
## Graba o borra la entrada en el registro para arrancar con Windows

def inicio_arranque():
    if os.name == "nt":
        if var_windows.get() == 1:
            import winreg
            ruta_exe = sys.executable
            clave = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\\Microsoft\\Windows\\CurrentVersion\\Run", 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(clave, "ProyectoNT", 0, winreg.REG_SZ, ruta_exe)
            clave.Close()
        if var_windows.get() == 0:
            import winreg
            try:
                clave = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\\Microsoft\\Windows\\CurrentVersion\\Run", 0, winreg.KEY_SET_VALUE)
                winreg.DeleteValue(clave, "ProyectoNT")
                clave.Close()
            except:
                pass


## -- DICCIONARIO --
## Genera el diccionario de reemplazos según el estilo configurado
## Intenta leer de tkinter primero; si no puede, usa los valores del config.ini

def generar_diccionario():
    global diccionario
    try:
        estilo = estilo_entrada.get()
        afijo_sufijo = entry_sufijo_estilo.get()
        afijo_prefijo = entry_prefijo_estilo.get()
    except:
        estilo = estilo_entrada_guardado
        afijo_sufijo = caracter_sufijo_guardado
        afijo_prefijo = caracter_prefijo_guardado

    if estilo == "2":  # sufijo
        varP = ""
        varS = afijo_sufijo
        diccionario = {
    varP + "c" + varS : "ĉ", varP + "g" + varS : "ĝ", varP + "h" + varS : "ĥ", varP + "j" + varS : "ĵ", varP + "s" + varS : "ŝ", varP + "u" + varS : "ŭ",
    varP + "C" + varS : "Ĉ", varP + "G" + varS : "Ĝ", varP + "H" + varS : "Ĥ", varP + "J" + varS : "Ĵ", varP + "S" + varS : "Ŝ", varP + "U" + varS : "Ŭ",
    varP.upper() + "C" + varS.upper() : "Ĉ", varP.upper() + "G" + varS.upper() : "Ĝ", varP.upper() + "H" + varS.upper() : "Ĥ", varP.upper() + "J" + varS.upper() : "Ĵ", varP.upper() + "S" + varS.upper() : "Ŝ", varP.upper() + "U" + varS.upper() : "Ŭ"
}
    elif estilo == "1":  # prefijo
        varP = afijo_prefijo
        varS = ""
        diccionario = {
    varP + "c" + varS : "ĉ", varP + "g" + varS : "ĝ", varP + "h" + varS : "ĥ", varP + "j" + varS : "ĵ", varP + "s" + varS : "ŝ", varP + "u" + varS : "ŭ",
    varP + "C" + varS : "Ĉ", varP + "G" + varS : "Ĝ", varP + "H" + varS : "Ĥ", varP + "J" + varS : "Ĵ", varP + "S" + varS : "Ŝ", varP + "U" + varS : "Ŭ",
    varP.upper() + "C" + varS.upper() : "Ĉ", varP.upper() + "G" + varS.upper() : "Ĝ", varP.upper() + "H" + varS.upper() : "Ĥ", varP.upper() + "J" + varS.upper() : "Ĵ", varP.upper() + "S" + varS.upper() : "Ŝ", varP.upper() + "U" + varS.upper() : "Ŭ"
}
    else:
        diccionario = diccionario_defecto


## -- BUFFER --
## Guarda las últimas teclas presionadas y busca combinaciones

def buffer_tipeo(tecla):                            # Agrega teclas al buffer respetando el margen
    try:
        if buffer_congelado:
            return
        if tecla.char:
            buffer_lista.append(tecla)
            if len(buffer_lista) > margen:
                buffer_lista.pop(0)
    except Exception:
        buffer_lista.clear()

def buscar_caracteres():                            # Busca la mejor combinación en el buffer
    mejor_combinacion = None
    mejor_rango = None
    for combinacion in diccionario:
        posicion_primera_letra = None
        posicion_segunda_letra = None
        for posicion, elemento in enumerate(buffer_lista):
            if elemento.char == combinacion[0]:
                posicion_primera_letra = posicion
            if elemento.char == combinacion[1]:
                posicion_segunda_letra = posicion
        if posicion_primera_letra is not None and posicion_segunda_letra is not None and posicion_primera_letra < posicion_segunda_letra:
            rango_borrado = posicion_segunda_letra - posicion_primera_letra + 1
            if mejor_rango is None or rango_borrado < mejor_rango:
                mejor_combinacion = combinacion
                mejor_rango = rango_borrado
    return mejor_combinacion, mejor_rango


## -- BANDERAS --
## Indican si el programa está escribiendo para evitar bucles

def activar_bandera():
    global escribiendo
    escribiendo = True

def desactivar_bandera():
    global escribiendo
    escribiendo = False


## -- TOOLTIPS --
## Muestra una ventanita de ayuda al pasar el mouse por encima

class Tooltip:
    def __init__(self, widget, texto, clave=""):
        self.widget = widget
        self.texto = texto
        self.clave = clave
        self.ventana_tip = None
        self.after_id = None
        widget.bind("<Enter>", self.mostrar)
        widget.bind("<Leave>", self.ocultar)
        tooltips.append(self)

    def mostrar(self, event=None):
        self.after_id = self.widget.after(750, self._mostrar)

    def _mostrar(self):
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height()
        self.ventana_tip = tk.Toplevel(self.widget)
        self.ventana_tip.wm_overrideredirect(True)
        self.ventana_tip.wm_geometry(f"+{x}+{y}")
        label = tk.Label(self.ventana_tip, text=self.texto, background="lightyellow", relief="solid", borderwidth=1, wraplength=400)
        label.pack()

    def ocultar(self, event=None):
        if self.after_id:
            self.widget.after_cancel(self.after_id)
            self.after_id = None
        if self.ventana_tip:
            self.ventana_tip.destroy()
            self.ventana_tip = None

    

##Funciones para el entorno gráfico
def validar_afijo(P, W):
    if len(P) > 1:
        return False
    if P in ["c", "g", "h", "j", "s", "u", "C", "G", "H", "J", "S", "U", "ĉ", "ĝ", "ĥ", "ĵ", "ŝ", "ŭ", "Ĉ", "Ĝ", "Ĥ", "Ĵ", "Ŝ", "Ŭ"]:
        widget = ventana_opciones.nametowidget(W)
        widget.config(bg="red", fg="white")
        ventana_opciones.after(500, lambda: widget.config(bg="#f0f0f0", fg="black"))
        return False
    widget = ventana_opciones.nametowidget(W)
    widget.config(bg="#f0f0f0", fg="black")
    generar_diccionario()
    return True


def activar_prueba():
    global activado
    if activado == 0:
        activado = 2

def desactivar_prueba():
    global activado
    if activado == 2:
        activado = 0


##################################################
##           ATAJO DE ACTIVACIÓN                ##
##################################################
## Captura y gestiona el hotkey para activar
## o desactivar el programa

def registrar_tecla_atajo(tecla):
    global teclas_atajo
    if len(teclas_atajo) < 3 and tecla not in teclas_atajo:
        teclas_atajo.append(tecla)
    partes = []
    for t in teclas_atajo:
        if hasattr(t, 'name') and t.name:
            partes.append(nombres_teclas.get(t.name, t.name))
        elif hasattr(t, 'char') and t.char and ord(t.char) < 27:
            partes.append(chr(ord(t.char) + 64))
        elif hasattr(t, 'char') and t.char and ord(t.char) >= 27:
            partes.append(t.char.upper())
        else:
            codigos_especiales = {226: "<", 227: ">"}
            if hasattr(t, 'vk') and t.vk in codigos_especiales:
                partes.append(codigos_especiales[t.vk])
            elif hasattr(t, 'vk') and t.vk:
                try:
                    partes.append(chr(t.vk))
                except:
                    partes.append(str(t))
            else:
                partes.append(str(t))
    if partes:
        etiqueta_atajo.config(text=" + ".join(partes))
    else:
        etiqueta_atajo.config(text="Combinación no válida")

def activar_modo_captura():                        # Inicia la captura del atajo — pone fondo amarillo
    global captura_atajo, listener_atajo
    captura_atajo = True
    teclas_atajo.clear()
    listener_atajo = keyboard.Listener(on_press=registrar_tecla_atajo)
    listener_atajo.start()
    boton_capturar.config(text=textos_idioma[idioma]["guardar_atajo"], command=guardar_atajo)
    boton_ok.config(state="disabled")
    boton_cancelar.config(state="disabled")
    boton_limpiar.config(state="disabled")
    frame_atajo_captura.config(bg="yellow")
    etiqueta_atajo.config(text=textos_idioma[idioma]["presione_atajo"], bg="yellow")


def guardar_atajo():                               # Guarda el atajo en config.ini y restaura la interfaz
    global atajo
    listener_atajo.stop()
    atajo = teclas_atajo.copy()
    texto = etiqueta_atajo.cget("text")
    if teclas_atajo:
        config['atajo']['atajo'] = texto
    else:
        etiqueta_atajo.config(text=config['atajo']['atajo'])
    with open(config_file, 'w') as f:
        config.write(f)
    boton_capturar.config(text=textos_idioma[idioma]["capturar_atajo"], command=activar_modo_captura)
    boton_ok.config(state="normal")
    boton_cancelar.config(state="normal")
    boton_limpiar.config(state="normal")
    frame_atajo_captura.config(bg="SystemButtonFace")
    etiqueta_atajo.config(bg="SystemButtonFace")


def limpiar_atajo():                               # Borra el atajo guardado
    teclas_atajo.clear()
    etiqueta_atajo.config(text="Sin atajo")

def cargar_atajo_desde_config():                   # Lee el atajo del config.ini y lo convierte a objetos pynput
    global atajo
    texto_atajo = config['atajo']['atajo']
    if texto_atajo == 'none' or texto_atajo == '':
        atajo = None
        return
    nombres_teclas_inverso = {v: k for k, v in nombres_teclas.items()}
    partes = texto_atajo.split(" + ")
    atajo = []
    for parte in partes:
        try:
            parte_pynput = nombres_teclas_inverso.get(parte, parte)
            atajo.append(keyboard.Key[parte_pynput])
        except KeyError:
            try:
                if len(parte) == 1:
                    codigos_especiales = {"<": keyboard.KeyCode(vk=226), ">": keyboard.KeyCode(vk=227)}
                    if parte in codigos_especiales:
                        atajo.append(codigos_especiales[parte])
                    else:
                        atajo.append(keyboard.KeyCode.from_char(parte.lower()))
                else:
                    codigos_especiales = {"<": keyboard.KeyCode(vk=226), ">": keyboard.KeyCode(vk=227)}
                    if parte in codigos_especiales:
                        atajo.append(codigos_especiales[parte])
                    else:
                        atajo.append(keyboard.KeyCode.from_char(parte.lower()))
            except Exception as ex:
                atajo = None
                return




##################################################
##                DESHACER                      ##
##################################################
## Sistema para deshacer el último reemplazo.
## Funciona con dos métodos: doble afijo o tecla personalizada.
## Estados del buffer: 3=espera especial, 2=espera gatillante,
##                     1=contando letras, 0=fin

def cargar_tecla_deshacer():                       # Lee la tecla de deshacer del config.ini
    global teclas_atajo_deshacer
    texto = config['deshacer']['atajo_deshacer']
    if texto == 'none' or texto == '':
        teclas_atajo_deshacer = []
        return
    try:
        teclas_atajo_deshacer = [keyboard.Key[texto]]
    except KeyError:
        teclas_atajo_deshacer = [keyboard.KeyCode.from_char(texto.lower())]

def activar_captura_deshacer():                    # Inicia la captura de la tecla de deshacer
    global captura_deshacer, listener_deshacer
    teclas_atajo_deshacer.clear()
    listener_deshacer = keyboard.Listener(on_press=registrar_tecla_deshacer)
    listener_deshacer.start()
    capturar_deshacer.config(text=textos_idioma[idioma]["guardar"], command=guardar_tecla_deshacer)
    boton_ok.config(state="disabled")
    boton_cancelar.config(state="disabled")
    limpiar_deshacer.config(state="disabled")
    frame_atajo_deshacer.config(bg="yellow")
    etiqueta_deshacer.config(text=textos_idioma[idioma]["presione"], bg="yellow")


def validar_tecla_deshacer(tecla):
    if hasattr(tecla, 'char') and tecla.char and tecla.char.lower() in ["c", "g", "h", "j", "s", "u", "ĉ", "ĝ", "ĥ", "ĵ", "ŝ", "ŭ"]:
        etiqueta_deshacer.config(text=textos_idioma[idioma]["sin_tecla"], bg="red", fg="white")
        ventana_opciones.after(500, lambda: etiqueta_deshacer.config(bg="yellow", fg="black"))
        return False
    vk = getattr(tecla, 'vk', None) or (tecla.value.vk if hasattr(tecla, 'value') else None)
    if vk in [8, 37, 38, 39, 40]:
        etiqueta_deshacer.config(text=textos_idioma[idioma]["sin_tecla"], bg="red", fg="white")
        ventana_opciones.after(500, lambda: etiqueta_deshacer.config(bg="yellow", fg="black"))
        return False
    return True


def registrar_tecla_deshacer(tecla):               # Registra la tecla presionada durante la captura
    if not validar_tecla_deshacer(tecla):
        return
    teclas_atajo_deshacer.clear()
    teclas_atajo_deshacer.append(tecla)
    if hasattr(tecla, 'name') and tecla.name:
        etiqueta_deshacer.config(text=tecla.name)
    elif hasattr(tecla, 'char') and tecla.char:
        etiqueta_deshacer.config(text=tecla.char.upper())

def limpiar_deshacer_tecla():                      # Borra la tecla de deshacer asignada
    teclas_atajo_deshacer.clear()
    etiqueta_deshacer.config(text=textos_idioma[idioma]["sin_tecla"])

def guardar_tecla_deshacer():                      # Guarda la tecla en config.ini y restaura la interfaz
    global listener_deshacer
    listener_deshacer.stop()
    texto = etiqueta_deshacer.cget("text")
    if teclas_atajo_deshacer:
        config['deshacer']['atajo_deshacer'] = texto
    else:
        etiqueta_deshacer.config(text=config['deshacer']['atajo_deshacer'])
    with open(config_file, 'w') as f:
        config.write(f)
    capturar_deshacer.config(text=textos_idioma[idioma]["capturar"], command=activar_captura_deshacer)
    boton_ok.config(state="normal")
    boton_cancelar.config(state="normal")
    limpiar_deshacer.config(state="normal")
    frame_atajo_deshacer.config(bg="SystemButtonFace")
    etiqueta_deshacer.config(bg="SystemButtonFace")

def guardar_deshacer_v2(combinacion, caracter, letras_originales):   # Guarda los datos antes del reemplazo
    global buffer_deshacer_v2, buffer_congelado
    buffer_deshacer_v2 = [letras_originales, caracter, 3]
    buffer_congelado = True

def suprimir_tecla_especial(tecla):
    if os.name == 'nt':
        import ctypes
        KEYEVENTF_KEYUP = 0x0002
        vk = tecla.value.vk if hasattr(tecla, 'value') else None
        if vk:
            ctypes.windll.user32.keybd_event(vk, 0, KEYEVENTF_KEYUP, 0)
    


def es_gatillante_v2(tecla):                       # Detecta si la tecla presionada activa el deshacer
    afijo = entry_sufijo_estilo.get() or entry_prefijo_estilo.get() or "x"
    if var_deshacer.get() == 1:
        if hasattr(tecla, 'char') and tecla.char == afijo:
            return 2
    if atajo_deshacer.get() == 1:
        if teclas_atajo_deshacer and str(tecla) == str(teclas_atajo_deshacer[0]):
            if hasattr(tecla, 'char') and tecla.char:
                return 2
            else:
                suprimir_tecla_especial(tecla)
                return 2
    return False

def ejecutar_deshacer_v2(backspaces, tecla=None):
    global buffer_deshacer_v2, buffer_congelado
    if tecla and not hasattr(tecla, 'char'):
        vk = getattr(tecla, 'vk', None) or (tecla.value.vk if hasattr(tecla, 'value') else None)
        if vk == 32 or vk == 164:
            backspaces_real = len(buffer_deshacer_v2[1]) + 1
        else:
            backspaces_real = len(buffer_deshacer_v2[1])
    else:
        backspaces_real = backspaces
    for _ in range(backspaces_real):
        teclado.press(keyboard.Key.backspace)
        teclado.release(keyboard.Key.backspace)
    teclado.type(''.join(t.char for t in buffer_deshacer_v2[0]))
    desactivar_bandera()
    buffer_deshacer_v2[2] = 1
    buffer_congelado = False


def verificar_deshacer_v2(tecla):                  # Máquina de estados que controla el flujo del deshacer
    global buffer_deshacer_v2, buffer_congelado
    if not buffer_deshacer_v2:
        return False
    if tecla == keyboard.Key.backspace:
        return False
    if buffer_deshacer_v2[2] == 3:                 # Espera el carácter especial (ĉ, ĝ, etc.)
        if hasattr(tecla, 'char') and tecla.char == buffer_deshacer_v2[1]:
            buffer_deshacer_v2[2] = 2
            return False
        else:
            buffer_deshacer_v2.clear()
            buffer_congelado = False
            return False
    if buffer_deshacer_v2[2] == 2:                 # Espera el gatillante (doble afijo o tecla)
        resultado = es_gatillante_v2(tecla)
        if resultado:
            ejecutar_deshacer_v2(resultado, tecla)
            return True
        else:
            buffer_deshacer_v2.clear()
            buffer_congelado = False
            return False
    largo = len(buffer_deshacer_v2[0])             # Cuenta las letras originales escritas
    if buffer_deshacer_v2[2] > 0 and buffer_deshacer_v2[2] <= largo - 1:
        buffer_deshacer_v2[2] -= 1
        return False
    if buffer_deshacer_v2[2] == 0:                 # Fin del ciclo — limpia todo
        buffer_deshacer_v2.clear()
        buffer_lista.clear()
        buffer_congelado = False
        return False
    return False

def reemplazar_teclas(caracter_final, rango_borrado):   # Borra las letras originales y escribe el carácter especial
    global buffer_congelado
    if buffer_deshacer_v2 and buffer_deshacer_v2[2] in [0, 1]:
        return
    letras_originales = buffer_lista[-rango_borrado:]
    activar_bandera()
    guardar_deshacer_v2(caracter_final, diccionario[caracter_final], letras_originales)
    for _ in range(rango_borrado):
        teclado.press(keyboard.Key.backspace)
        teclado.release(keyboard.Key.backspace)
    buffer_lista.clear()
    teclado.type(diccionario[caracter_final])
    desactivar_bandera()
    
    
    

##################################################
##            CODIGO PRINCIPAL                  ##
##################################################

#Código del cambio de los caracteres


def al_presionar(tecla):
    global teclas_presionadas_atajo
    try:
        if escribiendo:
            return
        if atajo:
            tecla_norm = keyboard.KeyCode.from_char(tecla.char.lower()) if hasattr(tecla, 'char') and tecla.char and tecla.char.isalpha() else tecla
            if tecla_norm not in teclas_presionadas_atajo:
                teclas_presionadas_atajo.append(tecla_norm)
            if len(teclas_presionadas_atajo) > 5:
                teclas_presionadas_atajo.pop(0)
            presionadas_str = set(str(t) for t in teclas_presionadas_atajo)
            atajo_str = set(str(t) for t in atajo)
            if presionadas_str == atajo_str:
                ultima = teclas_presionadas_atajo[-1]
                teclas_presionadas_atajo.clear()
                teclas_presionadas_atajo.extend([t for t in atajo if str(t) != str(ultima)])
                activar_script()
        if activado >= 1:
            if verificar_deshacer_v2(tecla):
                return 
            buffer_tipeo(tecla)
            combinacion, rango_borrado = buscar_caracteres()
            if combinacion is not None:
                reemplazar_teclas(combinacion, rango_borrado)
    except Exception as e:
        pass
    
    
def al_soltar(tecla):
    global teclas_presionadas_atajo
    tecla_norm = keyboard.KeyCode.from_char(tecla.char.lower()) if hasattr(tecla, 'char') and tecla.char and tecla.char.isalpha() else tecla
    if tecla_norm in teclas_presionadas_atajo:
        teclas_presionadas_atajo.remove(tecla_norm)
    if len(teclas_presionadas_atajo) > 5:
        teclas_presionadas_atajo.clear()






#######################################################
##               INTERFAZ GRÁFICA [IG]               ##
#######################################################

def iniciar_interfaz():

    ##--------------------------------------------------
    ## BANDEJA DEL SISTEMA - ícono y menú
    ##--------------------------------------------------
    global icono
    crear_menu_icono()
    icono = pystray.Icon("nombre", imagen_icono_desactivado, textos_idioma[idioma]["icono_inactivo"], menu=menu_icono)
    hilo_icono = threading.Thread(target=icono.run_detached, daemon=True)
    hilo_icono.start()
    al_iniciar_icono(icono)


    ##--------------------------------------------------
    ## VENTANA OPCIONES - ventana principal
    ##--------------------------------------------------
    global ventana_opciones
    global var_windows, iniciar_activado, var_deshacer, atajo_deshacer
    global estilo_entrada, lingvo
    global spinbox_margen, entry_prefijo_estilo, entry_sufijo_estilo
    global etiqueta_deshacer, capturar_deshacer, limpiar_deshacer
    global frame_atajo_deshacer, frame_deshacer_controles
    global boton_ok, boton_cancelar, boton_capturar, boton_limpiar
    global frame_atajo_captura, etiqueta_atajo
    global ventana_acerca_de
    global etiqueta_bandera, banderas

    ventana_opciones = tk.Tk()
    icono_tk = ImageTk.PhotoImage(imagen_icono_activado)
    ventana_opciones.iconphoto(True, icono_tk)
    ventana_opciones.title(textos_idioma[idioma]["menu_opciones"])
    ventana_opciones.geometry("470x535")
    ventana_opciones.withdraw()
    ventana_opciones.protocol("WM_DELETE_WINDOW", ventana_opciones.withdraw)
    ventana_opciones.columnconfigure(0, weight=1)
    ventana_opciones.resizable(False, False)
    
    banderas = {}                                                           #Carga las banderas
    for codigo in ["es", "en", "eo"]:
        ruta_bandera = os.path.join(ruta_base, f"app_idioma_{codigo}.png")
        img = Image.open(ruta_bandera).resize((24, 16), Image.LANCZOS)
        banderas[codigo] = ImageTk.PhotoImage(img)


    ##--------------------------------------------------
    ## VARIABLES DE CONTROL - checkboxes y selectores
    ##--------------------------------------------------
    var_windows = tk.IntVar()
    var_windows.set(windows_arranque)

    iniciar_activado = tk.IntVar()
    iniciar_activado.set(activado)

    var_deshacer = tk.IntVar()
    var_deshacer.set(deshacer_cambio)

    atajo_deshacer = tk.IntVar()
    atajo_deshacer.set(deshacer_tecla)

    estilo_entrada = tk.StringVar()
    estilo_entrada.set(estilo_entrada_guardado)

    lingvo = tk.StringVar()
    lingvo.set(nombres_idiomas[idioma])


    ##--------------------------------------------------
    ## SECCIÓN GENERAL - margen e idioma
    ##--------------------------------------------------
    frame_general = tk.LabelFrame(ventana_opciones, text=textos_idioma[idioma]["sec_general"])
    frame_general.grid(row=0, column=0, padx=5, ipady=5, sticky="ew")
    frame_general.rowconfigure(0, weight=1)

    etiqueta_margen = tk.Label(frame_general, text=textos_idioma[idioma]["margen"])
    etiqueta_margen.grid(row=0, column=0)
    Tooltip(etiqueta_margen, textos_idioma[idioma]["tooltip_margen"], "tooltip_margen")

    spinbox_margen = tk.Spinbox(frame_general, from_=2, to=4, width=3)
    spinbox_margen.grid(row=0, column=1, padx=5)
    spinbox_margen.delete(0, tk.END)
    spinbox_margen.insert(0, margen)

    etiqueta_idioma = tk.Label(frame_general, text=textos_idioma[idioma]["idioma"])
    etiqueta_idioma.grid(row=0, column=2, padx=(15,0))

    combo_idioma = ttk.Combobox(frame_general, textvariable=lingvo, values=list(nombres_idiomas.values()), width=10, state="readonly")
    combo_idioma.grid(row=0, column=3)
    combo_idioma.bind("<<ComboboxSelected>>", lambda e: actualizar_idioma())
    
    frame_bandera = tk.Frame(frame_general, relief="groove", borderwidth=1)
    frame_bandera.grid(row=0, column=4, padx=5)

    etiqueta_bandera = tk.Label(frame_bandera, image=banderas[idioma])
    etiqueta_bandera.grid(padx=2, pady=2)


    ##--------------------------------------------------
    ## SECCIÓN ESTILOS DE ENTRADA - prefijo/sufijo
    ##--------------------------------------------------
    frame_estilos = tk.LabelFrame(ventana_opciones, text=textos_idioma[idioma]["sec_estilos"])
    frame_estilos.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

    ratio_prefijo_estilo = tk.Radiobutton(frame_estilos, text=textos_idioma[idioma]["prefijo"], variable=estilo_entrada, value="1")
    ratio_prefijo_estilo.grid(row=0, column=0, sticky="w")
    Tooltip(ratio_prefijo_estilo, textos_idioma[idioma]["tooltip_prefijo"], "tooltip_prefijo")

    vcmd = ventana_opciones.register(validar_afijo)
    entry_prefijo_estilo = tk.Entry(frame_estilos, width=3, validate="key", validatecommand=(vcmd, "%P", "%W"), justify="center", insertwidth=0, insertontime=0)
    entry_prefijo_estilo.bind("<Key>", lambda e: e.widget.select_range(0, tk.END))
    entry_prefijo_estilo.bind("<FocusIn>", lambda e: entry_prefijo_estilo.config(bg="#f0f0f0") if entry_prefijo_estilo.get().lower() not in ["c","g","h","j","s","u"] else None)
    entry_prefijo_estilo.bind("<FocusOut>", lambda e: entry_prefijo_estilo.config(bg="white") if entry_prefijo_estilo.get().lower() not in ["c","g","h","j","s","u"] else None)
    entry_prefijo_estilo.bind("<KeyRelease>", lambda e: generar_diccionario())
    entry_prefijo_estilo.grid(row=0, column=1, sticky="w", padx=(140,0))
    entry_prefijo_estilo.config(validate="none")
    entry_prefijo_estilo.insert(0, caracter_prefijo_guardado)
    generar_diccionario()
    entry_prefijo_estilo.config(validate="key")
    Tooltip(entry_prefijo_estilo, textos_idioma[idioma]["tooltip_afijos_no_permitidos"], "tooltip_afijos_no_permitidos")

    texto_prefijo_estilo = tk.Label(frame_estilos, text=textos_idioma[idioma]["texto_prefijo"])
    texto_prefijo_estilo.grid(row=0, column=2, sticky="w", pady=5)

    ratio_sufijo_estilo = tk.Radiobutton(frame_estilos, text=textos_idioma[idioma]["sufijo"], variable=estilo_entrada, value="2")
    ratio_sufijo_estilo.grid(row=1, column=0, sticky="w")
    Tooltip(ratio_sufijo_estilo, textos_idioma[idioma]["tooltip_sufijo"], "tooltip_sufijo")

    entry_sufijo_estilo = tk.Entry(frame_estilos, width=3, validate="key", validatecommand=(vcmd, "%P", "%W"), justify="center", insertwidth=0, insertontime=0)
    entry_sufijo_estilo.bind("<Key>", lambda e: e.widget.select_range(0, tk.END))
    entry_sufijo_estilo.bind("<FocusIn>", lambda e: entry_sufijo_estilo.config(bg="#f0f0f0") if entry_sufijo_estilo.get().lower() not in ["c","g","h","j","s","u"] else None)
    entry_sufijo_estilo.bind("<FocusOut>", lambda e: entry_sufijo_estilo.config(bg="white") if entry_sufijo_estilo.get().lower() not in ["c","g","h","j","s","u"] else None)
    entry_sufijo_estilo.bind("<KeyRelease>", lambda e: generar_diccionario())
    entry_sufijo_estilo.grid(row=1, column=1, sticky="w", padx=(140,0))
    entry_sufijo_estilo.config(validate="none")
    entry_sufijo_estilo.insert(0, caracter_sufijo_guardado)
    entry_sufijo_estilo.config(validate="key")
    generar_diccionario()
    Tooltip(entry_sufijo_estilo, textos_idioma[idioma]["tooltip_afijos_no_permitidos"], "tooltip_afijos_no_permitidos")

    texto_sufijo_estilo = tk.Label(frame_estilos, text=textos_idioma[idioma]["texto_sufijo"])
    texto_sufijo_estilo.grid(row=1, column=2, sticky="w", pady=5)

    ratio_personalizado_estilo = tk.Radiobutton(frame_estilos, text=textos_idioma[idioma]["personalizado"], variable=estilo_entrada, value="3")
    ratio_personalizado_estilo.grid(row=2, column=0, sticky="w", columnspan=2)
    Tooltip(ratio_personalizado_estilo, textos_idioma[idioma]["tooltip_personalizado"], "tooltip_personalizado")

    frame_boton_personalizar = tk.Frame(frame_estilos)
    frame_boton_personalizar.grid(row=2, column=1, sticky="w", pady=5, columnspan=2, padx=(140,0))
    boton_personalizar = tk.Button(frame_boton_personalizar, text=textos_idioma[idioma]["personalizado"], state="disabled")
    boton_personalizar.grid(row=0, column=0)


    ##--------------------------------------------------
    ## SECCIÓN DESHACER
    ##--------------------------------------------------
    frame_deshacer = tk.LabelFrame(ventana_opciones, text=textos_idioma[idioma]["sec_deshacer"])
    frame_deshacer.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

    checkbox_deshacer_afijo = tk.Checkbutton(frame_deshacer, text=textos_idioma[idioma]["deshacer_afijo"], variable=var_deshacer)
    checkbox_deshacer_afijo.grid(row=0, column=0, sticky="w")
    Tooltip(checkbox_deshacer_afijo, textos_idioma[idioma]["tooltip_deshacer_afijo"], "tooltip_deshacer_afijo")

    checkbox_deshacer_tecla = tk.Checkbutton(frame_deshacer, text=textos_idioma[idioma]["deshacer_tecla"], variable=atajo_deshacer)
    checkbox_deshacer_tecla.grid(row=1, column=0, sticky="w")
    Tooltip(checkbox_deshacer_tecla, textos_idioma[idioma]["tooltip_deshacer_tecla"], "tooltip_deshacer_tecla")

    frame_deshacer_controles = tk.Frame(frame_deshacer)
    frame_deshacer_controles.grid(row=1, column=1, sticky="e", pady=2)

    frame_atajo_deshacer = tk.Frame(frame_deshacer_controles, relief="groove", borderwidth=2)
    frame_atajo_deshacer.grid(row=0, column=0, padx=2)
    frame_deshacer.columnconfigure(1, weight=1)

    etiqueta_deshacer = tk.Label(frame_atajo_deshacer, text=config['deshacer']['atajo_deshacer'], width=8, justify="center")
    etiqueta_deshacer.grid(row=0, column=0, padx=2, pady=2)

    capturar_deshacer = tk.Button(frame_deshacer_controles, text=textos_idioma[idioma]["capturar"], command=activar_captura_deshacer, width=8)
    capturar_deshacer.grid(row=0, column=1, padx=2)

    limpiar_deshacer = tk.Button(frame_deshacer_controles, text=textos_idioma[idioma]["limpiar"], command=limpiar_deshacer_tecla, width=8)
    limpiar_deshacer.grid(row=0, column=2, padx=2)

    ##--------------------------------------------------
    ## SECCIÓN PRUEBA - campo para probar los reemplazos
    ##--------------------------------------------------
    frame_prueba = tk.LabelFrame(ventana_opciones, text="Prueba")
    frame_prueba.grid(row=3, column=0, padx=5, ipady=6, sticky="ew")
    frame_prueba.rowconfigure(0, weight=1)

    entry_prueba = tk.Entry(frame_prueba, width=55, font=("Arial", 11))
    frame_prueba.columnconfigure(0, weight=1)
    entry_prueba.bind("<FocusIn>", lambda e: activar_prueba())
    entry_prueba.bind("<FocusOut>", lambda e: desactivar_prueba())
    entry_prueba.bind("<KeyRelease>", lambda e: entry_prueba.delete(0, tk.END) if len(entry_prueba.get()) >= 60 else None)
    entry_prueba.grid(row=0, column=0, padx=5, ipady=5)


    ##--------------------------------------------------
    ## SECCIÓN SISTEMA - arranque e inicio activado
    ##--------------------------------------------------
    frame_sistema = tk.LabelFrame(ventana_opciones, text=textos_idioma[idioma]["sec_sistema"])
    frame_sistema.grid(row=4, column=0, padx=5, pady=5, sticky="ew")

    checkbox_iniciar = tk.Checkbutton(frame_sistema, text=textos_idioma[idioma]["iniciar_activado"], variable=iniciar_activado)
    checkbox_iniciar.grid(row=0, column=0, sticky="w")

    checkbox_arranque = tk.Checkbutton(frame_sistema, text=textos_idioma[idioma]["iniciar_windows"], variable=var_windows)
    checkbox_arranque.grid(row=1, column=0, sticky="w")


    ##--------------------------------------------------
    ## SECCIÓN ATAJO - captura del hotkey de activación
    ##--------------------------------------------------
    frame_atajo = tk.LabelFrame(ventana_opciones, text=textos_idioma[idioma]["sec_atajo"])
    frame_atajo.grid(row=5, column=0, padx=5, pady=5, sticky="ew")
    frame_atajo.columnconfigure(1, weight=1)

    boton_capturar = tk.Button(frame_atajo, text=textos_idioma[idioma]["capturar_atajo"], command=activar_modo_captura, width=17)
    boton_capturar.grid(row=0, column=0)

    boton_limpiar = tk.Button(frame_atajo, text=textos_idioma[idioma]["limpiar"], command=limpiar_atajo, width=17)
    boton_limpiar.grid(row=1, column=0)

    frame_atajo_captura = tk.Frame(frame_atajo, relief="groove", borderwidth=2, width=200, height=30)
    frame_atajo_captura.grid(row=0, column=1, padx=2, sticky="nsew", rowspan=2, ipady=5)
    frame_atajo_captura.columnconfigure(0, weight=1)
    frame_atajo_captura.rowconfigure(0, weight=1)

    etiqueta_atajo = tk.Label(frame_atajo_captura, text=config['atajo']['atajo'], width=20, justify="center")
    etiqueta_atajo.grid(row=0, column=0, pady=0)


    ##--------------------------------------------------
    ## BOTONES OK Y CANCELAR
    ##--------------------------------------------------
    frame_botones = tk.Frame(ventana_opciones)
    frame_botones.grid(row=6, column=0, pady=10)

    boton_ok = tk.Button(frame_botones, text=textos_idioma[idioma]["boton_ok"], command=guardar_opciones)
    boton_ok.grid(row=0, column=0, padx=2)

    boton_cancelar = tk.Button(frame_botones, text=textos_idioma[idioma]["boton_cancelar"], command=cancelar_opciones)
    boton_cancelar.grid(row=0, column=1, padx=2)


    ##--------------------------------------------------
    ## VENTANA ACERCA DE
    ##--------------------------------------------------
    
    #Configuracion de la fuente del titulo
    ruta_fuente = os.path.join(ruta_base, "ProtestRiot-Limpia.ttf")
    ctypes.windll.gdi32.AddFontResourceW(ruta_fuente)
    #ctypes.windll.gdi32.RemoveFontResourceW(os.path.join(ruta_base, "ProtestRiot-Regular.ttf"))
    fuente_titulo = ("Protest Riot", 32)
    #print(font.families())
    
    
    ventana_acerca_de = tk.Toplevel()
    ventana_acerca_de.title(textos_idioma[idioma]["menu_acerca"])
    ventana_acerca_de.withdraw()
    ventana_acerca_de.protocol("WM_DELETE_WINDOW", ventana_acerca_de.withdraw)
    ventana_acerca_de.resizable(False, False)
    ventana_acerca_de.update_idletasks()
    ancho = 350
    alto = 500
    x = (ventana_acerca_de.winfo_screenwidth() // 2) - (ancho // 2)
    y = (ventana_acerca_de.winfo_screenheight() // 2) - (alto // 2)
    ventana_acerca_de.geometry(f"{ancho}x{alto}+{x}+{y}")
    
    icono_grande = ImageTk.PhotoImage(imagen_icono_grande)

    frame_acerca_top = tk.Frame(ventana_acerca_de)
    frame_acerca_top.pack(fill="x", padx=10, pady=10)

    frame_acerca_texto = tk.Frame(frame_acerca_top)
    frame_acerca_texto.pack(side="left")
    frame_acerca_texto = tk.Frame(frame_acerca_top)
    frame_acerca_texto.pack(side="left", fill="both", expand=True)

    tk.Label(frame_acerca_texto, text=NOMBRE, font=fuente_titulo, fg="#009000").pack(anchor="center", pady=(20,0))
    tk.Label(frame_acerca_texto, text="Versión " + VERSION).pack(anchor="center")
    tk.Label(frame_acerca_texto, text="Autor: " + AUTOR).pack(anchor="center")

    frame_icono = tk.Frame(frame_acerca_top, relief="groove", borderwidth=2)
    frame_icono.pack(side="right")
    
    tk.Label(frame_icono, image=icono_grande).pack(padx=5, pady=5)
    tk.Label(ventana_acerca_de, text=textos_idioma[idioma]["descripcion"]).pack(pady=5)
    tk.Label(ventana_acerca_de, text=CARACTERES).pack()
    
    
    
    #Botones
    frame_acerca_botones = tk.Frame(ventana_acerca_de)
    frame_acerca_botones.pack(fill="x", padx=10, pady=10, side="bottom")

    boton_acerca_izq = tk.Button(frame_acerca_botones, text="Este es un botón")
    boton_acerca_izq.pack(side="left")

    boton_acerca_der = tk.Button(frame_acerca_botones, text="Este es otro botón")
    boton_acerca_der.pack(side="right")
    
    #Cosas de uso externo
    tk.Label(ventana_acerca_de, text="Fuente Protest Riot © Octavio Pardo, SIL OFL", font=("Segoe UI", 7), fg="gray").pack()
    tk.Label(ventana_acerca_de, text="Usa pynput y pystray bajo licencia LGPL", font=("Segoe UI", 7), fg="gray").pack(pady=2)


    ##--------------------------------------------------
    ## INICIO - mainloop mantiene la ventana abierta
    ##--------------------------------------------------
    cargar_atajo_desde_config()
    cargar_tecla_deshacer()
    ventana_opciones.mainloop()


## Anexo, inicia el interfaz
iniciar_interfaz()
generar_diccionario()


ventana_opciones.mainloop()


