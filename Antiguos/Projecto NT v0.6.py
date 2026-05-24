##################################################
##               ENCABEZADO                     ##
##################################################
## Projecto NT
## Descripción: Programa para poder escribir teclas especiales en Esperanto
## Versión: 0.6
## Autor: GAB


##################################################
##        LIBRERIAS Y OBJETOS DE CONTROL        ##
##################################################
from pynput import keyboard            #Control de teclado
import tkinter as tk                   #Entorno gráfico

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




##################################################
##            VARIABLES GLOBALES                ##
##################################################

diccionario_defecto = {"cx":"ĉ", "gx":"ĝ", "hx":"ĥ", "jx":"ĵ", "sx":"ŝ", "ux":"ŭ", "Cx":"Ĉ", "Gx":"Ĝ", "Hx":"Ĥ", "Jx":"Ĵ", "Sx":"Ŝ", "Ux":"Ŭ", "CX":"Ĉ", "GX":"Ĝ", "HX":"Ĥ", "JX":"Ĵ", "SX":"Ŝ", "UX":"Ŭ"}
diccionario = diccionario_defecto

buffer_lista = []

listener = None

atajo = None
teclas_atajo = []
listener_atajo = None
teclas_presionadas_atajo = []




    
##################################################
##              CONFIGURACION                   ##
##################################################

#Esta es la configuración por defecto para crear el archivo config.ini
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


#Este es el cuerpo principal de la configuración
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



margen = int(config['general']['margen'])
activado = int(config['general']['iniciar_activado'])
windows_arranque = int(config['general']['iniciar_con_windows'])
estilo_entrada_guardado = config['general']['afijo']
caracter_prefijo_guardado = config['general']['prefijo'] 
caracter_sufijo_guardado = config['general']['sufijo']
#deshacer_cambio = int(config['general']['deshacer_cambio'])
#deshacer_tecla = int(config['general']['deshacer_tecla'])


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
    for _ in range(rango_borrado):
        teclado.press(keyboard.Key.backspace)
        teclado.release(keyboard.Key.backspace)
    buffer_lista.clear()
    teclado.type(diccionario[caracter_final])

#Funcion para deshacer los cambios
"""
def deshacer():
    global buffer_deshacer
    global buffer_lista
    global deshaciendo
    global listener
    deshaciendo = True
    listener.stop()
    for _ in range(buffer_deshacer[2]):
        teclado.press(keyboard.Key.backspace)
        teclado.release(keyboard.Key.backspace)
    for tecla in buffer_deshacer[0][-buffer_deshacer[2]:]:
        teclado.type(tecla.char)
    buffer_deshacer.clear()
    buffer_lista.clear()
    deshaciendo = False
    listener = keyboard.Listener(on_press=al_presionar, on_release=al_soltar)
    listener.start()"""



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


#Funcion para el guardado de las opciones

def margen_opciones():
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
    with open(config_file, 'w') as f:
        config.write(f)
    generar_diccionario()
    inicio_arranque()
    ventana_opciones.withdraw()

def cancelar_opciones():
    ventana_opciones.withdraw()
    

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
            
"""def cargar_tecla_deshacer():
    global teclas_atajo_deshacer
    texto = config['general']['atajo_deshacer']
    if texto == 'none' or texto == '':
        teclas_atajo_deshacer = []
        return
    try:
        teclas_atajo_deshacer = [keyboard.Key[texto]]
    except KeyError:
        teclas_atajo_deshacer = [keyboard.KeyCode.from_char(texto.lower())]
    
cargar_tecla_deshacer()"""

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
    

##Funcion para capturar el boton para deshacer

"""def activar_captura_deshacer():
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
    etiqueta_deshacer.config(bg="SystemButtonFace")"""


##################################################
##            CODIGO PRINCIPAL                  ##
##################################################

#Código del cambio de los caracteres

def al_presionar(tecla):
    global teclas_presionadas_atajo
    try:
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


##################################################
##            CODIGO INTERFAZ GRAFICA           ##
##################################################

#Codigo para dejarlo en la barra de tareas
menu_icono = pystray.Menu(
    pystray.MenuItem(lambda item: "Desactivar" if activado == 1 else "Activar", lambda: activar_script()),
    pystray.MenuItem("Opciones", lambda: ventana_opciones.deiconify()),
    pystray.Menu.SEPARATOR,                                                                                #Línea separadora  
    pystray.MenuItem("Acerca de", lambda: ventana_acerca_de.deiconify()),
    pystray.Menu.SEPARATOR,
    pystray.MenuItem("Salir", cerrar_app)
)

icono = pystray.Icon("nombre", imagen_icono_desactivado, "tu texto aquí", menu=menu_icono)
hilo_icono = threading.Thread(target=icono.run_detached, daemon=True)

hilo_icono.start()
al_iniciar_icono(icono)


    
###Código de la ventana Opciones
#Configuracion general
ventana_opciones = tk.Tk()                                                   #abre una ventana
var_windows = tk.IntVar()
var_windows.set(windows_arranque)
iniciar_activado = tk.IntVar()
var_deshacer = tk.IntVar()
#var_deshacer.set(deshacer_cambio)
atajo_deshacer = tk.IntVar()
#atajo_deshacer.set(deshacer_tecla)


estilo_entrada = tk.StringVar()                                              #Crea las variables para el boton ratio en los Estilos de Entrada
estilo_entrada.set(estilo_entrada_guardado)



icono_tk = ImageTk.PhotoImage(imagen_icono_activado)                         #Estos dos comandos ponen el icono en las ventanas
ventana_opciones.iconphoto(True, icono_tk)

ventana_opciones.title("Opciones")                                           #título de la ventana
ventana_opciones.geometry("500x500")                                         #ancho x alto de la ventana (en píxeles)
ventana_opciones.withdraw()                                                  # La ventana no se abre directamente al correr la app
ventana_opciones.protocol("WM_DELETE_WINDOW", ventana_opciones.withdraw)     #Permite ocultar la ventana (para q abria siempre)
ventana_opciones.columnconfigure(0, weight=1)
ventana_opciones.resizable(False, False)

#Seccion General
frame_general = tk.LabelFrame(ventana_opciones, text="General")
frame_general.grid(row=0, column=0, padx=5, pady=5,sticky="ew")

etiqueta_margen = tk.Label(frame_general, text="Margen:")                #esta es la opcion para el margen y como configurarlo
spinbox_margen = tk.Spinbox(frame_general, from_=2, to=5, width=3)      #Configuración del Buffer 
etiqueta_margen.grid(row=0, column=0)
spinbox_margen.grid(row=0, column=1)
spinbox_margen.delete(0, tk.END)
spinbox_margen.insert(0, margen)


#Seccion Estilos de Entrada
frame_estilos = tk.LabelFrame(ventana_opciones, text="Estilos de Entrada")
frame_estilos.grid(row=1, column=0, padx=5, pady=5,sticky="ew")

ratio_prefijo_estilo = tk.Radiobutton(frame_estilos, text="Prefijo", variable=estilo_entrada, value="1")
ratio_sufijo_estilo = tk.Radiobutton(frame_estilos, text="Sufijo", variable=estilo_entrada, value="2")
ratio_personalizado_estilo = tk.Radiobutton(frame_estilos, text="Personalizado", variable=estilo_entrada, value="3")
ratio_prefijo_estilo.grid(row=0, column=0, sticky="w")
ratio_sufijo_estilo.grid(row=1, column=0, sticky="w")
ratio_personalizado_estilo.grid(row=2, column=0, sticky="w")

entry_prefijo_estilo = tk.Entry(frame_estilos, width=3)
entry_prefijo_estilo.grid(row=0, column=1, sticky="w")
entry_prefijo_estilo.insert(0, caracter_prefijo_guardado)


texto_prefijo_estilo = tk.Label(frame_estilos, text="   Escribe el carácter antes → xc, xg, xs...").grid(row=0, column=2, sticky="w", pady=5)


entry_sufijo_estilo = tk.Entry(frame_estilos, width=3)
entry_sufijo_estilo.grid(row=1, column=1, sticky="w")
entry_sufijo_estilo.insert(0, caracter_sufijo_guardado)

texto_sufijo_estilo = tk.Label(frame_estilos, text="   Escribe el carácter después → cx, gx, sx...").grid(row=1, column=2, sticky="w", pady=5)


frame_boton_personalizar = tk.Frame(frame_estilos)
frame_boton_personalizar.grid(row=2, column=2, sticky="w", pady=5)

boton_personalizar = tk.Button(frame_boton_personalizar, text="Personalizar", state="disabled")
boton_personalizar.grid(row=0, column=0)

texto_deshacer_estilo = tk.Label(frame_estilos, text="Deshacer").grid(row=3, column=0, sticky="w", pady=5)
checkbox_deshacer_estilo = tk.Checkbutton(frame_estilos, text="Repetir el afijo deshace el cambio", variable=var_deshacer)
checkbox_deshacer_estilo.grid(row=4, column=0)




checkbox_deshacer_estilo = tk.Checkbutton(frame_estilos, text="Personalizar tecla para deshacer", variable=atajo_deshacer)
checkbox_deshacer_estilo.grid(row=5, column=0, sticky="w")

frame_deshacer_controles = tk.Frame(frame_estilos)
frame_deshacer_controles.grid(row=5, column=1, columnspan=3, sticky="w", pady=2)

frame_atajo_deshacer = tk.Frame(frame_deshacer_controles, relief="groove", borderwidth=2)
frame_atajo_deshacer.grid(row=0, column=0, padx=2)

etiqueta_deshacer = tk.Label(frame_atajo_deshacer, text="Sin tecla", width=8, justify="center")
etiqueta_deshacer.grid(row=0, column=0, padx=2, pady=2)
etiqueta_deshacer.config(text=config['general']['atajo_deshacer'])

capturar_deshacer = tk.Button(frame_deshacer_controles, text="Capturar", state="disabled", width=8)
capturar_deshacer.grid(row=0, column=1, padx=2)

limpiar_deshacer = tk.Button(frame_deshacer_controles, text="Limpiar", state="disabled", width=8)
limpiar_deshacer.grid(row=0, column=2, padx=2)














#Seccion Sistema
frame_sistema = tk.LabelFrame(ventana_opciones, text="Sistema")
frame_sistema.grid(row=2, column=0, padx=5, pady=5,sticky="ew")

checkbox_iniciar = tk.Checkbutton(frame_sistema, text="Iniciar activado", variable=iniciar_activado)
checkbox_iniciar.grid(row=0, column=0, sticky="w")
iniciar_activado.set(activado)

checkbox_arranque = tk.Checkbutton(frame_sistema, text="Iniciar con Windows", variable=var_windows)
checkbox_arranque.grid(row=1, column=0, sticky="w")


#Captura del atajo (Hotkey)
frame_atajo = tk.LabelFrame(ventana_opciones, text="Atajo")
frame_atajo.grid(row=3, column=0, padx=5, pady=5,sticky="ew")
frame_atajo.columnconfigure(1, weight=1)

boton_capturar = tk.Button(frame_atajo, text="Capturar atajo", command=activar_modo_captura, width=12)
boton_capturar.grid(row=0, column=0)

boton_limpiar = tk.Button(frame_atajo, text="Limpiar", command=limpiar_atajo, width=12)
boton_limpiar.grid(row=1, column=0)

frame_atajo_captura = tk.Frame(frame_atajo, relief="groove", borderwidth=2, width=200, height=30)
frame_atajo_captura.grid(row=0, column=1, padx=2, sticky="nsew", rowspan=2, ipady=5)
frame_atajo_captura.columnconfigure(0, weight=1)
frame_atajo_captura.rowconfigure(0, weight=1)

etiqueta_atajo = tk.Label(frame_atajo_captura, text="ctrl + shift + A", width=20, justify="center")
etiqueta_atajo.grid(row=0, column=0, pady=0)
etiqueta_atajo.config(text=config['general']['atajo'])





#Boton ok y cancelar
frame_botones = tk.Frame(ventana_opciones)
frame_botones.grid(row=4, column=0, pady=10)

boton_ok = tk.Button(frame_botones, text="OK", command=margen_opciones)
boton_ok.grid(row=0, column=0, padx=2)

boton_cancelar = tk.Button(frame_botones, text="Cancelar", command=cancelar_opciones)
boton_cancelar.grid(row=0, column=1, padx=2)






#Código del Acerca de...
ventana_acerca_de = tk.Toplevel()                                              #abre una ventana
ventana_acerca_de.title("Acerca de")                                           #título de la ventana
ventana_acerca_de.geometry("350x200")                                          #ancho x alto de la ventana (en píxeles)
ventana_acerca_de.withdraw()  
ventana_acerca_de.protocol("WM_DELETE_WINDOW", ventana_acerca_de.withdraw)     #Permite ocultar la ventana (para q abria siempre)
tk.Label(ventana_acerca_de, text="Projecto NT", font=("Arial", 14, "bold")).pack(pady=5)
tk.Label(ventana_acerca_de, text="Versión 0.6").pack()
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










