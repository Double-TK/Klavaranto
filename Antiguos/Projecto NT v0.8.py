##################################################
##               ENCABEZADO                     ##
##################################################
## Projecto NT
## Descripción: Programa para poder escribir teclas especiales en Esperanto
## Versión: 0.8
## Autor: GAB


##################################################
##        LIBRERIAS Y OBJETOS DE CONTROL        ##
##################################################
from pynput import keyboard            #Control de teclado

import tkinter as tk                   #Entorno gráfico
from tkinter import ttk

import pystray                         #Poner icono en la bandeja del sistema

import threading                       #Tareas en distintos hilos

import os                              #Acceso al sistema operativo (rutas, PID, matar proceso)
import psutil                          #Verificar si un proceso está corriendo (instancia única)
import time                            #Controla tiempos (de espera)
import sys

import configparser                    #Para administrar archivos de configuración


from PIL import Image, ImageDraw       #Este controla el dibujado (exactametne de los iconos)
from PIL import ImageTk                #Poner el dibujo en las ventanas



teclado = keyboard.Controller()        #Objeto para controlar el teclado y simular teclas




#######################################################
##              IDIOMAS / TEXTOS [IT]                ##
#######################################################

#[itti] Este es el diccionario con los textos y los idiomas
textos_idioma = {
    "es": {
        # Títulos de secciones
        "sec_general": "General",
        "sec_estilos": "Estilos de Entrada",
        "sec_sistema": "Sistema",
        "sec_atajo": "Atajo",

        # Sección General
        "margen": "Margen:",
        "idioma": "Idioma:",

        # Sección Estilos de Entrada
        "prefijo": "Prefijo",
        "sufijo": "Sufijo",
        "personalizado": "Personalizado",
        "texto_prefijo": "Escribe el carácter antes → xc, xg, xs...",
        "texto_sufijo": "Escribe el carácter después → cx, gx, sx...",

        # Sección Deshacer
        "sec_deshacer": "Deshacer",
        "deshacer_afijo": "Repetir el afijo deshace el cambio",
        "deshacer_tecla": "Personalizar tecla para deshacer",
        "sin_tecla": "Sin tecla",
        "presione": "Presione",
        "capturar": "Capturar",
        "guardar": "Guardar",
        "limpiar": "Limpiar",

        # Sección Sistema
        "iniciar_activado": "Iniciar activado",
        "iniciar_windows": "Iniciar con Windows",

        # Sección Atajo
        "capturar_atajo": "Capturar atajo",
        "guardar_atajo": "Guardar atajo",
        "sin_atajo": "Sin atajo",
        "presione_atajo": "Presione los botones",

        # Botones OK y Cancelar
        "boton_ok": "OK",
        "boton_cancelar": "Cancelar",

        # Menú botón derecho
        "menu_activar": "Activar",
        "menu_desactivar": "Desactivar",
        "menu_opciones": "Opciones",
        "menu_acerca": "Acerca de",
        "menu_salir": "Salir",

        # Ícono en bandeja
        "icono_activo": "Proyecto NT (Activo)",
        "icono_inactivo": "Proyecto NT (Inactivo)",
        
        # Tooltips
        "tooltip_margen": "Cantidad de letras que el programa recuerda al buscar combinaciones. Valor recomendado: 3",
        "tooltip_prefijo": "Escribe el carácter especial ANTES de la letra. Ejemplo: xc → ĉ",
        "tooltip_sufijo": "Escribe el carácter especial DESPUÉS de la letra. Ejemplo: cx → ĉ",
        "tooltip_personalizado": "Opción no disponible en esta versión",
        "tooltip_deshacer_afijo": "Al escribir el afijo dos veces seguidas, deshace el último cambio. Ejemplo: cxx → cx",
        "tooltip_deshacer_tecla": "Asigna una tecla personalizada para deshacer el último cambio",
        
    },
    "en": {
        # Títulos de secciones
        "sec_general": "General",
        "sec_estilos": "Input Styles",
        "sec_sistema": "System",
        "sec_atajo": "Shortcut",

        # Sección General
        "margen": "Margin:",
        "idioma": "Language:",

        # Sección Estilos de Entrada
        "prefijo": "Prefix",
        "sufijo": "Suffix",
        "personalizado": "Custom",
        "texto_prefijo": "Type the character before → xc, xg, xs...",
        "texto_sufijo": "Type the character after → cx, gx, sx...",

        # Sección Deshacer
        "sec_deshacer": "Undo",
        "deshacer_afijo": "Repeating the affix undoes the change",
        "deshacer_tecla": "Custom key to undo",
        "sin_tecla": "No key",
        "presione": "Press",
        "capturar": "Capture",
        "guardar": "Save",
        "limpiar": "Clear",

        # Sección Sistema
        "iniciar_activado": "Start enabled",
        "iniciar_windows": "Start with Windows",

        # Sección Atajo
        "capturar_atajo": "Capture shortcut",
        "guardar_atajo": "Save shortcut",
        "sin_atajo": "No shortcut",
        "presione_atajo": "Press the buttons",

        # Botones OK y Cancelar
        "boton_ok": "OK",
        "boton_cancelar": "Cancel",

        # Menú botón derecho
        "menu_activar": "Enable",
        "menu_desactivar": "Disable",
        "menu_opciones": "Options",
        "menu_acerca": "About",
        "menu_salir": "Exit",

        # Ícono en bandeja
        "icono_activo": "Project NT (Active)",
        "icono_inactivo": "Project NT (Inactive)",
        
        # Tooltips
        "tooltip_margen": "Number of letters the program remembers when searching for combinations. Recommended value: 3",
        "tooltip_prefijo": "Type the special character BEFORE the letter. Example: xc → ĉ",
        "tooltip_sufijo": "Type the special character AFTER the letter. Example: cx → ĉ",
        "tooltip_personalizado": "Option not available in this version",
        "tooltip_deshacer_afijo": "Typing the affix twice undoes the last change. Example: cxx → cx",
        "tooltip_deshacer_tecla": "Assign a custom key to undo the last change",
        
    },
    "eo": {
        # Titoloj de sekcioj
        "sec_general": "Ĝenerala",
        "sec_estilos": "Enigstiloj",
        "sec_sistema": "Sistemo",
        "sec_atajo": "Klavoŝparvojo",

        # Sekcio Ĝenerala
        "margen": "Marĝeno:",
        "idioma": "Lingvo:",

        # Sekcio Enigstiloj
        "prefijo": "Prefikso",
        "sufijo": "Sufikso",
        "personalizado": "Propra",
        "texto_prefijo": "Tajpu la signon antaŭ → xc, xg, xs...",
        "texto_sufijo": "Tajpu la signon post → cx, gx, xs...",

        # Sekcio Malfari
        "sec_deshacer": "Malfari",
        "deshacer_afijo": "Ripeti la afikson malfaras la ŝanĝon",
        "deshacer_tecla": "Propra klavo por malfari",
        "sin_tecla": "Sen klavo",
        "presione": "Premu",
        "capturar": "Kaptu",
        "guardar": "Konservi",
        "limpiar": "Viŝi",

        # Sekcio Sistemo
        "iniciar_activado": "Starti aktiva",
        "iniciar_windows": "Starti kun Vindozo",

        # Sekcio Klavoŝparvojo
        "capturar_atajo": "Kaptu klavoŝparvon",
        "guardar_atajo": "Konservi klavoŝparvon",
        "sin_atajo": "Sen klavoŝparvoj",
        "presione_atajo": "Premu la klavojn",

        # Butonoj OK kaj Nuligi
        "boton_ok": "OK",
        "boton_cancelar": "Nuligi",

        # Menuo dekstra klako
        "menu_activar": "Aktivigi",
        "menu_desactivar": "Malaktivigi",
        "menu_opciones": "Agordoj",
        "menu_acerca": "Pri la programo",
        "menu_salir": "Eliri",

        # Ikono en taskobaro
        "icono_activo": "Projekto NT (Aktiva)",
        "icono_inactivo": "Projekto NT (Neaktiva)",
        
        # Iluminaretoj
        "tooltip_margen": "Nombro de literoj kiujn la programo memoras dum serĉado. Rekomendata valoro: 3",
        "tooltip_prefijo": "Tajpu la specialan signon ANTAŬ la litero. Ekzemplo: xc → ĉ",
        "tooltip_sufijo": "Tajpu la specialan signon POST la litero. Ekzemplo: cx → ĉ",
        "tooltip_personalizado": "Opcio ne disponebla en ĉi tiu versio",
        "tooltip_deshacer_afijo": "Tajpante la afikson dufoje malfaras la lastan ŝanĝon. Ekzemplo: cxx → cx",
        "tooltip_deshacer_tecla": "Asignu propran klavon por malfari la lastan ŝanĝon",
    }
}


#[itni] Cambia los nombres cortos a largos, para las opciones
nombres_idiomas = {
    "es": "Español",
    "en": "English",
    "eo": "Esperanto"
}
idiomas_codigos = {v: k for k, v in nombres_idiomas.items()}

#[itai] Ejecuta el cambio de idioma
def actualizar_idioma():
    global idioma
    idioma_anterior = idioma
    idioma = idiomas_codigos[lingvo.get()]
    
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
    
    recorrer(ventana_opciones)
    crear_menu_icono()

#[itcm] Crea el menu del boton derecho
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

diccionario_defecto = {"cx":"ĉ", "gx":"ĝ", "hx":"ĥ", "jx":"ĵ", "sx":"ŝ", "ux":"ŭ", "Cx":"Ĉ", "Gx":"Ĝ", "Hx":"Ĥ", "Jx":"Ĵ", "Sx":"Ŝ", "Ux":"Ŭ", "CX":"Ĉ", "GX":"Ĝ", "HX":"Ĥ", "JX":"Ĵ", "SX":"Ŝ", "UX":"Ŭ"}
diccionario = diccionario_defecto

buffer_lista = []

listener = None

#Variables para el atajo de activación
atajo = None
teclas_atajo = []
listener_atajo = None
teclas_presionadas_atajo = []

#Variables para el deshacer
buffer_deshacer = []
teclas_atajo_deshacer = []
escribiendo = False


    
######################################################
##              CONFIGURACION [SC]                  ##
######################################################

#[sccd] Configuración por defecto para crear el archivo config.ini
config_defecto = {
    'general': {
        'margen': 3,
        'iniciar_activado': 0,
        'pid': 0,
        'idioma': 'es',
        'atajo' : 'none',
        'iniciar_con_windows' : '0',
        'afijo' : '2',
        'sufijo' : 'x',
        'prefijo' : '',
        'deshacer_cambio' : '0',
        'atajo_deshacer': 'none',
        'deshacer_tecla': '0'
    }
}


#[scconfig] Este es el cuerpo principal de la configuración
config = configparser.ConfigParser()

config_file = "config.ini"
if os.path.exists(config_file):
    config.read(config_file)
    pid = int(config['general']['pid'])
    if psutil.pid_exists(pid):
        sys.exit()
    config['general']['pid'] = str(os.getpid())
    with open(config_file, 'w') as f:
        config.write(f)
else:
    config.read_dict(config_defecto)
    config['general']['pid'] = str(os.getpid())
    with open(config_file, 'w') as f:
        config.write(f)


#[sclectura] Esta es la sección de lectura del archivo config.ini
margen = int(config['general']['margen'])
activado = int(config['general']['iniciar_activado'])
windows_arranque = int(config['general']['iniciar_con_windows'])
estilo_entrada_guardado = config['general']['afijo']
caracter_prefijo_guardado = config['general']['prefijo'] 
caracter_sufijo_guardado = config['general']['sufijo']
deshacer_cambio = int(config['general']['deshacer_cambio'])
deshacer_tecla = int(config['general']['deshacer_tecla'])
idioma = config['general']['idioma']



#[scguardado] Esta es la sección de lectura del archivo config.ini
def guardar_opciones():
    global margen
    margen = int(spinbox_margen.get())
    config['general']['margen'] = str(margen)
    config['general']['iniciar_activado'] = str(iniciar_activado.get())
    config['general']['iniciar_con_windows'] = str(var_windows.get())
    config['general']['afijo'] = estilo_entrada.get()
    config['general']['prefijo'] = entry_prefijo_estilo.get()
    config['general']['sufijo'] = entry_sufijo_estilo.get()
    config['general']['deshacer_cambio'] = str(var_deshacer.get())
    config['general']['atajo_deshacer'] = str(etiqueta_deshacer.cget("text"))
    config['general']['deshacer_tecla'] = str(atajo_deshacer.get())
    config['general']['idioma'] = idiomas_codigos[lingvo.get()]
    with open(config_file, 'w') as f:
        config.write(f)
    generar_diccionario()
    inicio_arranque()
    ventana_opciones.withdraw()

def cancelar_opciones():
    ventana_opciones.withdraw()
    



##################################################
##           MODULOS / FUNCIONES                ##
##################################################

def generar_diccionario():
    global diccionario
    estilo = estilo_entrada.get()
    if estilo == "2":  # sufijo
        afijo = entry_sufijo_estilo.get()
        varP = ""
        varS = afijo
        diccionario = {
    varP + "c" + varS : "ĉ", varP + "g" + varS : "ĝ", varP + "h" + varS : "ĥ", varP + "j" + varS : "ĵ", varP + "s" + varS : "ŝ", varP + "u" + varS : "ŭ",
    varP + "C" + varS : "Ĉ", varP + "G" + varS : "Ĝ", varP + "H" + varS : "Ĥ", varP + "J" + varS : "Ĵ", varP + "S" + varS : "Ŝ", varP + "U" + varS : "Ŭ",
    varP.upper() + "C" + varS.upper() : "Ĉ", varP.upper() + "G" + varS.upper() : "Ĝ", varP.upper() + "H" + varS.upper() : "Ĥ", varP.upper() + "J" + varS.upper() : "Ĵ", varP.upper() + "S" + varS.upper() : "Ŝ", varP.upper() + "U" + varS.upper() : "Ŭ"
}
    elif estilo == "1":  # prefijo
        afijo = entry_prefijo_estilo.get()
        varP = afijo
        varS = ""
        diccionario = {
    varP + "c" + varS : "ĉ", varP + "g" + varS : "ĝ", varP + "h" + varS : "ĥ", varP + "j" + varS : "ĵ", varP + "s" + varS : "ŝ", varP + "u" + varS : "ŭ",
    varP + "C" + varS : "Ĉ", varP + "G" + varS : "Ĝ", varP + "H" + varS : "Ĥ", varP + "J" + varS : "Ĵ", varP + "S" + varS : "Ŝ", varP + "U" + varS : "Ŭ",
    varP.upper() + "C" + varS.upper() : "Ĉ", varP.upper() + "G" + varS.upper() : "Ĝ", varP.upper() + "H" + varS.upper() : "Ĥ", varP.upper() + "J" + varS.upper() : "Ĵ", varP.upper() + "S" + varS.upper() : "Ŝ", varP.upper() + "U" + varS.upper() : "Ŭ"
}
    else:
        diccionario = diccionario_defecto
        



#Funciones para Teclas
def buffer_tipeo (tecla):                         #Controla el buffer
    try:
        if buffer_congelado:
            return
        if tecla.char:
            buffer_lista.append(tecla)
            if len(buffer_lista) > margen:        #Borra terminos del buffer según el margen (min 2)
                buffer_lista.pop(0)
    except Exception:
        buffer_lista.clear()



def buscar_caracteres ():                                                  #Busca coincidencias entre las letras
    for combinacion in diccionario:
        posicion_primera_letra = None 
        posicion_segunda_letra = None
        for posicion, elemento in enumerate(buffer_lista): 
            if elemento.char == combinacion[0]:
                posicion_primera_letra=posicion
            if elemento.char == combinacion[1]:
                posicion_segunda_letra=posicion
        if posicion_primera_letra is not None and posicion_segunda_letra is not None and  posicion_primera_letra  < posicion_segunda_letra:
            rango_borrado = posicion_segunda_letra - posicion_primera_letra + 1
            return combinacion, rango_borrado
    return None, None   
       
       
def reemplazar_teclas(caracter_final, rango_borrado):
    global buffer_congelado
    print(f"[REEMPLAZAR] caracter_final: {caracter_final} | buffer_deshacer: {buffer_deshacer_v2}")
    if buffer_deshacer_v2 and buffer_deshacer_v2[2] in [0, 1]:
        print("[REEMPLAZAR] estado 0 o 1 - bloqueando reemplazo")
        return
    activar_bandera()
    print(f"[REEMPLAZAR] letras originales: {[t.char for t in buffer_lista[-rango_borrado:]]}")
    guardar_deshacer_v2(caracter_final, diccionario[caracter_final])
    for _ in range(rango_borrado):
        teclado.press(keyboard.Key.backspace)
        teclado.release(keyboard.Key.backspace)
    buffer_lista.clear()
    teclado.type(diccionario[caracter_final])
    desactivar_bandera()
    

##################################################################
##            FUNCION - SECCION DESHACER CAMBIOS [SF]           ##
##################################################################

#[sfgdd] Funcion para deshacer los cambios (va en reemplazar_teclas y agrega las cosas al buffer_deshacer antes de borrarlas#
def guardar_datos_deshacer(buffer_lista, caracter_final, rango_borrado): 
    global buffer_deshacer
    buffer_deshacer = [buffer_lista.copy(), diccionario[caracter_final], rango_borrado]
    
#[sfed] Funcion que ejecuta el deshacer#
def ejecutar_deshacer():
    global buffer_deshacer
    global listener
    
    listener.stop()
    time.sleep(0.1)
    
    teclado.press(keyboard.Key.backspace)
    teclado.release(keyboard.Key.backspace)
    teclado.press(keyboard.Key.backspace)
    teclado.release(keyboard.Key.backspace)  
    
    for tecla in buffer_deshacer[0]:
        teclado.type(tecla.char)
    
    buffer_deshacer.clear()
    
    listener = keyboard.Listener(on_press=al_presionar, on_release=al_soltar)
    listener.start()


#[sfet] Esta funcion ve que metodo utiliza el deshacer, el doble afijo y/o tecla personalizada
def es_tecla_deshacer(tecla):
    if var_deshacer.get() == 1:
        afijo = entry_sufijo_estilo.get() or entry_prefijo_estilo.get() or "x"
        if hasattr(tecla, 'char') and tecla.char == afijo:
            return True
    if atajo_deshacer.get() == 1:
        if teclas_atajo_deshacer and str(tecla) == str(teclas_atajo_deshacer[0]):
            return True
    return False
    

#[sfvd] Funcion que verifica y ejecuta el deshacer en el proceso principal
def verificar_deshacer(tecla):
    global buffer_deshacer
    if tecla == keyboard.Key.backspace:
        return False
    if buffer_deshacer and hasattr(tecla, 'char') and tecla.char == buffer_deshacer[1]:
        return False
    if buffer_deshacer:
        if es_tecla_deshacer(tecla):
            ejecutar_deshacer()
            return True
        else:
            buffer_deshacer.clear()
    return False


def activar_bandera():
    global escribiendo
    escribiendo = True

def desactivar_bandera():
    global escribiendo
    escribiendo = False

def cargar_tecla_deshacer():
    global teclas_atajo_deshacer
    texto = config['general']['atajo_deshacer']
    if texto == 'none' or texto == '':
        teclas_atajo_deshacer = []
        return
    try:
        teclas_atajo_deshacer = [keyboard.Key[texto]]
    except KeyError:
        teclas_atajo_deshacer = [keyboard.KeyCode.from_char(texto.lower())]
    
cargar_tecla_deshacer()



##Funcion para capturar el boton para deshacer

def activar_captura_deshacer():
    global captura_deshacer
    global listener_deshacer
    captura_atajo_deshacer = True
    teclas_atajo_deshacer.clear()
    listener_deshacer = keyboard.Listener(on_press=registrar_tecla_deshacer)
    listener_deshacer.start()
    capturar_deshacer.config(text="Guardar", command=guardar_tecla_deshacer)
    boton_ok.config(state="disabled")
    boton_cancelar.config(state="disabled")
    limpiar_deshacer.config(state="disabled")
    frame_atajo_deshacer.config(bg="yellow")
    etiqueta_deshacer.config(text="Presione", bg="yellow")
    
#Funcion para registrar el boton  para deshacer
    
def registrar_tecla_deshacer(tecla):
    teclas_atajo_deshacer.clear()
    teclas_atajo_deshacer.append(tecla)
    if hasattr(tecla, 'name') and tecla.name:
        etiqueta_deshacer.config(text=tecla.name)
    elif hasattr(tecla, 'char') and tecla.char:
        etiqueta_deshacer.config(text=tecla.char.upper())
        
def limpiar_deshacer_tecla():
    teclas_atajo_deshacer.clear()
    etiqueta_deshacer.config(text="Sin tecla")      
        
def guardar_tecla_deshacer():
    global captura_deshacer
    global listener_deshacer
    listener_deshacer.stop()
    atajo_deshacer = teclas_atajo_deshacer.copy()
    texto = etiqueta_deshacer.cget("text")
    if teclas_atajo_deshacer:
        config['general']['atajo_deshacer'] = texto
    else:
        etiqueta_deshacer.config(text=config['general']['atajo_deshacer'])
    with open(config_file, 'w') as f:
        config.write(f)
    capturar_deshacer.config(text="Capturar", command=activar_captura_deshacer)
    boton_ok.config(state="normal")
    boton_cancelar.config(state="normal")
    limpiar_deshacer.config(state="normal")
    frame_atajo_deshacer.config(bg="SystemButtonFace")
    etiqueta_deshacer.config(bg="SystemButtonFace")


####################################################################
#################################################################### 

#Función que dibuja y crea los iconos de activado/desactivado

def crear_icono(color_hex):
    img = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    hexagono = [(16,4), (48,4), (64,32), (48,60), (16,60), (0,32)]
    estrella_outline = [(32,8), (38,23), (52,23), (42,32), (46,48), (32,39), (18,48), (22,32), (12,23), (26,23)]
    estrella = [(32,15), (36,27), (47,27), (39,34), (42,46), (32,39), (22,46), (25,34), (17,27), (28,27)]
    
    draw.polygon(hexagono, fill=color_hex)
    draw.polygon(estrella_outline, fill='black')
    draw.polygon(estrella, fill='white')
    
    return img

imagen_icono_activado = crear_icono('#009000')
imagen_icono_desactivado = crear_icono('#900000')

crear_icono = 0                                                 #con esto creo los iconos si lo necesito.
if crear_icono ==1 and not os.path.exists("icono.ico"):
    imagen_icono_activado.save("icono.ico")


##Funcion que crea la bandera del esperanto
def crear_bandera_esperanto():
    ancho, alto = 20 , 20
    img = Image.new('RGBA', (ancho, alto), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Fondo verde
    draw.rectangle([0, 0, ancho, alto], fill='#009000')
    # Cuadrado blanco arriba izquierda
    draw.rectangle([0, 0, ancho//2, alto//2], fill='white')
    # Estrella verde (pequeña)
    cx, cy = ancho//4, alto//4
    estrella = [
        (cx, cy-6), (cx+2, cy-2), (cx+6, cy-2),
        (cx+3, cy+1), (cx+4, cy+5), (cx, cy+3),
        (cx-4, cy+5), (cx-3, cy+1), (cx-6, cy-2),
        (cx-2, cy-2)
    ]
    draw.polygon(estrella, fill='#009000')
    
    return ImageTk.PhotoImage(img)   



#Funcion para iniciar activado
    
def al_iniciar_icono(icono):
    time.sleep(0.5)
    if activado == 1:
        icono.icon = imagen_icono_activado
        icono.title = "Proyecto NT (Activo)"


#Función de activación/desactivación del código
    
def activar_script ():
    global activado
    global listener
    if activado == 0:
        activado = 1
        icono.icon = imagen_icono_activado
        listener = keyboard.Listener(on_press=al_presionar)
        icono.title = "Proyecto NT (Activo)"
    else:
        activado = 0
        icono.icon = imagen_icono_desactivado
        icono.title = "Proyecto NT (Inactivo)"
       
    

#Función para cerrar el programa

def cerrar_app():
    if listener is not None:
        listener.stop()
    ventana_opciones.quit()  
    icono.stop()
    os.kill(os.getpid(), 9)




#Funciones para la captura del Atajo (Hotkey)

def registrar_tecla_atajo(tecla):
    global teclas_atajo
    if len(teclas_atajo) < 3 and tecla not in teclas_atajo:
        teclas_atajo.append(tecla)
    partes = []
    for t in teclas_atajo:
        if hasattr(t, 'name') and t.name:
            partes.append(t.name)
        elif hasattr(t, 'char') and t.char and ord(t.char) < 27:
            partes.append(chr(ord(t.char) + 64))
        elif hasattr(t, 'char') and t.char and ord(t.char) >= 27:
            partes.append(t.char.upper())
        else:
            partes = None
            break
    if partes is None:
        teclas_atajo.clear()
        etiqueta_atajo.config(text="Combinación no válida")
    else:
        etiqueta_atajo.config(text=" + ".join(partes))
      
def activar_modo_captura():
    global captura_atajo
    global listener_atajo
    captura_atajo = True
    teclas_atajo.clear()
    listener_atajo = keyboard.Listener(on_press=registrar_tecla_atajo)
    listener_atajo.start()
    boton_capturar.config(text="Guardar atajo", command=guardar_atajo)
    boton_ok.config(state="disabled")
    boton_cancelar.config(state="disabled")
    boton_limpiar.config(state="disabled")
    frame_atajo_captura.config(bg="yellow")
    etiqueta_atajo.config(text="Presione los botones",bg="yellow")

    

def guardar_atajo():
    global atajo
    listener_atajo.stop()
    atajo = teclas_atajo.copy()
    texto = etiqueta_atajo.cget("text")
    if teclas_atajo:
        config['general']['atajo'] = texto
    else:
        etiqueta_atajo.config(text=config['general']['atajo'])
    with open(config_file, 'w') as f:
        config.write(f)
    boton_capturar.config(text="Capturar atajo", command=activar_modo_captura)
    boton_ok.config(state="normal")
    boton_cancelar.config(state="normal")
    boton_limpiar.config(state="normal")
    frame_atajo_captura.config(bg="SystemButtonFace")
    etiqueta_atajo.config(bg="SystemButtonFace")


def limpiar_atajo():
    teclas_atajo.clear()
    etiqueta_atajo.config(text="Sin atajo")

    
def cargar_atajo_desde_config():
    global atajo
    texto_atajo = config['general']['atajo']
    if texto_atajo == 'none' or texto_atajo == '':
        atajo = None
        return
    partes = texto_atajo.split(" + ")
    atajo = []
    for parte in partes:
        try:
            atajo.append(keyboard.Key[parte])
        except KeyError:
            atajo.append(keyboard.KeyCode.from_char(chr(ord(parte.lower()) - 96)))
            


#Codigo para comenzar con windows
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
    else:
        pass
    



##Clase para los tooltip (ni idea que es)
class Tooltip:
    def __init__(self, widget, texto):
        self.widget = widget
        self.texto = texto
        self.ventana_tip = None
        self.after_id = None
        widget.bind("<Enter>", self.mostrar)
        widget.bind("<Leave>", self.ocultar)

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


##################################################################
##            DESHACER V2 [SF2]                                 ##
##################################################################

# Variables nuevas
buffer_deshacer_v2 = []      # [caracter_final, caracter_especial, estado]
                              # estado: 3 = esperando especial
                              #         2 = esperando gatillante
                              #         1 = esperando c (primera letra combinacion)
                              #         0 = esperando x (segunda letra combinacion)
buffer_congelado = False

def guardar_deshacer_v2(combinacion, caracter, letras_originales):
    global buffer_deshacer_v2, buffer_congelado
    print(f"[GUARDAR] combinacion: {combinacion} | caracter: {caracter} | letras: {[t.char for t in letras_originales]}")
    buffer_deshacer_v2 = [letras_originales, caracter, 3]
    buffer_congelado = True
    print(f"[GUARDAR] buffer: {buffer_deshacer_v2}")

def es_gatillante_v2(tecla):
    afijo = entry_sufijo_estilo.get() or entry_prefijo_estilo.get() or "x"
    print(f"[GATILLANTE] tecla: {tecla} | afijo: {afijo} | var_deshacer: {var_deshacer.get()}")
    if var_deshacer.get() == 1:
        if hasattr(tecla, 'char') and tecla.char == afijo:
            print("[GATILLANTE] es doble afijo -> retorna 2")
            return 2
    if atajo_deshacer.get() == 1:
        if teclas_atajo_deshacer and str(tecla) == str(teclas_atajo_deshacer[0]):
            if hasattr(tecla, 'char') and tecla.char:
                print("[GATILLANTE] es tecla personalizada con char -> retorna 2")
                return 2
            else:
                print("[GATILLANTE] es tecla personalizada sin char -> retorna 1")
                return 1
    print("[GATILLANTE] no es gatillante -> retorna False")
    return False

def ejecutar_deshacer_v2(backspaces):
    global buffer_deshacer_v2, buffer_congelado
    print(f"[EJECUTAR] backspaces: {backspaces} | combinacion: {buffer_deshacer_v2[0]}")
    activar_bandera()
    for _ in range(backspaces):
        teclado.press(keyboard.Key.backspace)
        teclado.release(keyboard.Key.backspace)
    teclado.type(buffer_deshacer_v2[0])
    desactivar_bandera()
    buffer_deshacer_v2[2] = 1
    buffer_congelado = False
    print(f"[EJECUTAR] estado cambiado a 1 | buffer: {buffer_deshacer_v2}")

def verificar_deshacer_v2(tecla):
    global buffer_deshacer_v2, buffer_congelado

    if not buffer_deshacer_v2:
        return False

    if tecla == keyboard.Key.backspace:
        return False

    print(f"[VERIFICAR] tecla: {tecla} | estado: {buffer_deshacer_v2[2]} | buffer: {buffer_deshacer_v2}")

    # Estado 3 - esperamos el caracter especial
    if buffer_deshacer_v2[2] == 3:
        if hasattr(tecla, 'char') and tecla.char == buffer_deshacer_v2[1]:
            print("[VERIFICAR] llego el caracter especial, cambiando a estado 2")
            buffer_deshacer_v2[2] = 2
            return False
        else:
            print("[VERIFICAR] llego otra cosa en estado 3, cancelando")
            buffer_deshacer_v2.clear()
            buffer_congelado = False
            return False

    # Estado 2 - esperamos el gatillante
    if buffer_deshacer_v2[2] == 2:
        resultado = es_gatillante_v2(tecla)
        if resultado:
            print(f"[VERIFICAR] gatillante detectado, ejecutando deshacer")
            ejecutar_deshacer_v2(resultado)
            return True
        else:
            print("[VERIFICAR] no es gatillante en estado 2, cancelando")
            buffer_deshacer_v2.clear()
            buffer_congelado = False
            return False

    # Estado 1 - esperando primera letra de la combinacion
    if buffer_deshacer_v2[2] == 1:
        print("[VERIFICAR] estado 1 - llego primera letra, cambiando a estado 0")
        buffer_deshacer_v2[2] = 0
        return False

    # Estado 0 - esperando segunda letra de la combinacion, luego limpia
    if buffer_deshacer_v2[2] == 0:
        print("[VERIFICAR] estado 0 - llego segunda letra, limpiando buffer")
        buffer_deshacer_v2.clear()
        buffer_lista.clear()
        buffer_congelado = False
        return False

    return False


def reemplazar_teclas(caracter_final, rango_borrado):
    global buffer_congelado
    print(f"[REEMPLAZAR] caracter_final: {caracter_final} | buffer_deshacer: {buffer_deshacer_v2}")
    if buffer_deshacer_v2 and buffer_deshacer_v2[2] in [0, 1]:
        print("[REEMPLAZAR] bloqueando reemplazo")
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
            if tecla not in teclas_presionadas_atajo:
                teclas_presionadas_atajo.append(tecla)
            presionadas_str = set(str(t) for t in teclas_presionadas_atajo)
            atajo_str = set(str(t) for t in atajo)
            if presionadas_str == atajo_str:
                ultima = teclas_presionadas_atajo[-1]
                teclas_presionadas_atajo.clear()
                teclas_presionadas_atajo.extend([t for t in atajo if str(t) != str(ultima)])
                activar_script()
        if activado == 1:
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
    if tecla in teclas_presionadas_atajo:
        teclas_presionadas_atajo.remove(tecla)


######################################################
##            CODIGO INTERFAZ GRAFICA [IG]          ##
######################################################

#[igbi] Bandeja del sistema - ícono y menú
crear_menu_icono()
icono = pystray.Icon("nombre", imagen_icono_desactivado, textos_idioma[idioma]["icono_inactivo"], menu=menu_icono)
hilo_icono = threading.Thread(target=icono.run_detached, daemon=True)
hilo_icono.start()
al_iniciar_icono(icono)

#[igvo] Ventana Opciones - configuración general
ventana_opciones = tk.Tk()
var_windows = tk.IntVar()
var_windows.set(windows_arranque)
iniciar_activado = tk.IntVar()
var_deshacer = tk.IntVar()
var_deshacer.set(deshacer_cambio)
atajo_deshacer = tk.IntVar()
atajo_deshacer.set(deshacer_tecla)
estilo_entrada = tk.StringVar()
estilo_entrada.set(estilo_entrada_guardado)
lingvo = tk.StringVar()
lingvo.set(nombres_idiomas[idioma])

icono_tk = ImageTk.PhotoImage(imagen_icono_activado)
ventana_opciones.iconphoto(True, icono_tk)
ventana_opciones.title(textos_idioma[idioma]["menu_opciones"])
ventana_opciones.geometry("500x600")
ventana_opciones.withdraw()
ventana_opciones.protocol("WM_DELETE_WINDOW", ventana_opciones.withdraw)
ventana_opciones.columnconfigure(0, weight=1)
ventana_opciones.resizable(False, False)

#[igsg] Sección General - margen e idioma
frame_general = tk.LabelFrame(ventana_opciones, text=textos_idioma[idioma]["sec_general"])
frame_general.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

etiqueta_margen = tk.Label(frame_general, text=textos_idioma[idioma]["margen"])
spinbox_margen = tk.Spinbox(frame_general, from_=2, to=4, width=3)
etiqueta_margen.grid(row=0, column=0)
spinbox_margen.grid(row=0, column=1, padx=5)
spinbox_margen.delete(0, tk.END)
spinbox_margen.insert(0, margen)

etiqueta_idioma = tk.Label(frame_general, text=textos_idioma[idioma]["idioma"])
etiqueta_margen.grid(row=0, column=0)
Tooltip(etiqueta_margen, textos_idioma[idioma]["tooltip_margen"])
spinbox_margen.grid(row=0, column=1, padx=5)
etiqueta_idioma.grid(row=0, column=2, padx=(15,0))
combo_idioma = ttk.Combobox(frame_general, textvariable=lingvo, values=list(nombres_idiomas.values()), width=10, state="readonly")
combo_idioma.grid(row=0, column=3)
combo_idioma.bind("<<ComboboxSelected>>", lambda e: actualizar_idioma())



#[igse] Sección Estilos de Entrada - radiobuttons y entradas
frame_estilos = tk.LabelFrame(ventana_opciones, text=textos_idioma[idioma]["sec_estilos"])
frame_estilos.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

ratio_prefijo_estilo = tk.Radiobutton(frame_estilos, text=textos_idioma[idioma]["prefijo"], variable=estilo_entrada, value="1")
ratio_sufijo_estilo = tk.Radiobutton(frame_estilos, text=textos_idioma[idioma]["sufijo"], variable=estilo_entrada, value="2")

ratio_personalizado_estilo = tk.Radiobutton(frame_estilos, text=textos_idioma[idioma]["personalizado"], variable=estilo_entrada, value="3")
ratio_personalizado_estilo.grid(row=2, column=0, sticky="w")
Tooltip(ratio_personalizado_estilo, textos_idioma[idioma]["tooltip_personalizado"])

ratio_prefijo_estilo.grid(row=0, column=0, sticky="w")
ratio_sufijo_estilo.grid(row=1, column=0, sticky="w")
Tooltip(ratio_prefijo_estilo, textos_idioma[idioma]["tooltip_prefijo"])

entry_prefijo_estilo = tk.Entry(frame_estilos, width=3)
entry_prefijo_estilo.grid(row=0, column=1, sticky="w")
entry_prefijo_estilo.insert(0, caracter_prefijo_guardado)
texto_prefijo_estilo = tk.Label(frame_estilos, text=textos_idioma[idioma]["texto_prefijo"])
texto_prefijo_estilo.grid(row=0, column=2, sticky="w", pady=5)
entry_prefijo_estilo.bind("<KeyRelease>", lambda e: generar_diccionario())

entry_sufijo_estilo = tk.Entry(frame_estilos, width=3)
entry_sufijo_estilo.grid(row=1, column=1, sticky="w")
entry_sufijo_estilo.insert(0, caracter_sufijo_guardado)
texto_sufijo_estilo = tk.Label(frame_estilos, text=textos_idioma[idioma]["texto_sufijo"])
texto_sufijo_estilo.grid(row=1, column=2, sticky="w", pady=5)
entry_sufijo_estilo.bind("<KeyRelease>", lambda e: generar_diccionario())
Tooltip(ratio_sufijo_estilo, textos_idioma[idioma]["tooltip_sufijo"])

frame_boton_personalizar = tk.Frame(frame_estilos)
frame_boton_personalizar.grid(row=2, column=2, sticky="w", pady=5)
boton_personalizar = tk.Button(frame_boton_personalizar, text=textos_idioma[idioma]["personalizado"], state="disabled")
boton_personalizar.grid(row=0, column=0)

#[igd] Sección Deshacer - checkboxes y captura de tecla
texto_deshacer_estilo = tk.Label(frame_estilos, text=textos_idioma[idioma]["sec_deshacer"])
texto_deshacer_estilo.grid(row=3, column=0, sticky="w", pady=5)

checkbox_deshacer_estilo = tk.Checkbutton(frame_estilos, text=textos_idioma[idioma]["deshacer_afijo"], variable=var_deshacer)
checkbox_deshacer_estilo.grid(row=4, column=0)
Tooltip(checkbox_deshacer_estilo, textos_idioma[idioma]["tooltip_deshacer_afijo"])

checkbox_deshacer_estilo = tk.Checkbutton(frame_estilos, text=textos_idioma[idioma]["deshacer_tecla"], variable=atajo_deshacer)
checkbox_deshacer_estilo.grid(row=5, column=0, sticky="w")
Tooltip(checkbox_deshacer_estilo, textos_idioma[idioma]["tooltip_deshacer_tecla"])


frame_deshacer_controles = tk.Frame(frame_estilos)
frame_deshacer_controles.grid(row=5, column=1, columnspan=3, sticky="w", pady=2)
frame_atajo_deshacer = tk.Frame(frame_deshacer_controles, relief="groove", borderwidth=2)
frame_atajo_deshacer.grid(row=0, column=0, padx=2)
etiqueta_deshacer = tk.Label(frame_atajo_deshacer, text=textos_idioma[idioma]["sin_tecla"], width=8, justify="center")
etiqueta_deshacer.grid(row=0, column=0, padx=2, pady=2)
etiqueta_deshacer.config(text=config['general']['atajo_deshacer'])
capturar_deshacer = tk.Button(frame_deshacer_controles, text=textos_idioma[idioma]["capturar"], command=activar_captura_deshacer, width=8)
capturar_deshacer.grid(row=0, column=1, padx=2)
limpiar_deshacer = tk.Button(frame_deshacer_controles, text=textos_idioma[idioma]["limpiar"], command=limpiar_deshacer_tecla, width=8)
limpiar_deshacer.grid(row=0, column=2, padx=2)

frame_prueba = tk.LabelFrame(ventana_opciones, text="Prueba")
frame_prueba.grid(row=2, column=0, padx=5, pady=5, sticky="ew")
entry_prueba = tk.Entry(frame_prueba, width=40)
entry_prueba.grid(row=0, column=0, padx=5, pady=5)

#[igss] Sección Sistema - checkboxes de inicio
frame_sistema = tk.LabelFrame(ventana_opciones, text=textos_idioma[idioma]["sec_sistema"])
frame_sistema.grid(row=3, column=0, padx=5, pady=5, sticky="ew")
checkbox_iniciar = tk.Checkbutton(frame_sistema, text=textos_idioma[idioma]["iniciar_activado"], variable=iniciar_activado)
checkbox_iniciar.grid(row=0, column=0, sticky="w")
iniciar_activado.set(activado)
checkbox_arranque = tk.Checkbutton(frame_sistema, text=textos_idioma[idioma]["iniciar_windows"], variable=var_windows)
checkbox_arranque.grid(row=1, column=0, sticky="w")

#[igsa] Sección Atajo - captura del hotkey
frame_atajo = tk.LabelFrame(ventana_opciones, text=textos_idioma[idioma]["sec_atajo"])
frame_atajo.grid(row=4, column=0, padx=5, pady=5, sticky="ew")
frame_atajo.columnconfigure(1, weight=1)
boton_capturar = tk.Button(frame_atajo, text=textos_idioma[idioma]["capturar_atajo"], command=activar_modo_captura, width=12)
boton_capturar.grid(row=0, column=0)
boton_limpiar = tk.Button(frame_atajo, text=textos_idioma[idioma]["limpiar"], command=limpiar_atajo, width=12)
boton_limpiar.grid(row=1, column=0)
frame_atajo_captura = tk.Frame(frame_atajo, relief="groove", borderwidth=2, width=200, height=30)
frame_atajo_captura.grid(row=0, column=1, padx=2, sticky="nsew", rowspan=2, ipady=5)
frame_atajo_captura.columnconfigure(0, weight=1)
frame_atajo_captura.rowconfigure(0, weight=1)
etiqueta_atajo = tk.Label(frame_atajo_captura, text=textos_idioma[idioma]["sin_atajo"], width=20, justify="center")
etiqueta_atajo.grid(row=0, column=0, pady=0)
etiqueta_atajo.config(text=config['general']['atajo'])

#[igbok] Botones OK y Cancelar
frame_botones = tk.Frame(ventana_opciones)
frame_botones.grid(row=5, column=0, pady=10)
boton_ok = tk.Button(frame_botones, text=textos_idioma[idioma]["boton_ok"], command=guardar_opciones)
boton_ok.grid(row=0, column=0, padx=2)
boton_cancelar = tk.Button(frame_botones, text=textos_idioma[idioma]["boton_cancelar"], command=cancelar_opciones)
boton_cancelar.grid(row=0, column=1, padx=2)

#[igad] Ventana Acerca de
ventana_acerca_de = tk.Toplevel()
ventana_acerca_de.title(textos_idioma[idioma]["menu_acerca"])
ventana_acerca_de.geometry("350x200")
ventana_acerca_de.withdraw()
ventana_acerca_de.protocol("WM_DELETE_WINDOW", ventana_acerca_de.withdraw)
tk.Label(ventana_acerca_de, text="Projecto NT", font=("Arial", 14, "bold")).pack(pady=5)
tk.Label(ventana_acerca_de, text="Versión 0.8").pack()
tk.Label(ventana_acerca_de, text="Autor: GAB").pack()
tk.Label(ventana_acerca_de, text="Programa para escribir caracteres especiales del Esperanto.").pack(pady=5)
tk.Label(ventana_acerca_de, text="cx→ĉ  gx→ĝ  hx→ĥ  jx→ĵ  sx→ŝ  ux→ŭ").pack()


#######################
#Si el usuario configuró iniciar activado, arranca el listener directamente

generar_diccionario()              #Carga el diccionario predeterminado
cargar_atajo_desde_config()        #Carga el atajo de activación guardado


listener = keyboard.Listener(on_press=al_presionar, on_release=al_soltar)        #Codigo para leer las teclas
listener.start()


ventana_opciones.mainloop()  # es para mantener la ventana abierta











