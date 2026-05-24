##################################################
##               ENCABEZADO                     ##
##################################################
## Projecto NT
## Descripción: Programa para poder escribir teclas especiales en Esperanto
## Versión: 0.5
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

import configparser                    #Para administrar archivos de configuración


from PIL import Image, ImageDraw       #Este controla el dibujado (exactametne de los iconos)
from PIL import ImageTk                #Poner el dibujo en las ventanas



teclado = keyboard.Controller()        #Objeto para controlar el teclado y simular teclas




##################################################
##            VARIABLES GLOBALES                ##
##################################################

teclas_especiales = {"cx":"ĉ" ,  "gx":"ĝ" , "hx":"ĥ" , "jx":"ĵ" , "sx":"ŝ" , "ux":"ŭ" , "Cx":"Ĉ" , "Gx":"Ĝ" , "Hx":"Ĥ" , "Jx":"Ĵ" , "Sx":"Ŝ" , "Ux":"Ŭ"}

buffer_lista = []  #Buffer para guardar más de una tecla en una lista

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
        'atajo' : 'none'
        
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


##################################################
##           MODULOS / FUNCIONES                ##
##################################################

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
    for combinacion in teclas_especiales:
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
            
def reemplazar_teclas(caracter_final,rango_borrado):                       #Borra/hace el cambio de los caracteres
    for _ in range(rango_borrado):
        teclado.press(keyboard.Key.backspace)
        teclado.release(keyboard.Key.backspace)
    teclado.type(teclas_especiales[caracter_final])


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
    while not icono.visible:
        pass
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


#Funciones para las Opciones

def margen_opciones():
    global margen
    margen = int(spinbox_margen.get())
    config['general']['margen'] = str(margen)
    config['general']['iniciar_activado'] = str(iniciar_activado.get())
    with open(config_file, 'w') as f:
        config.write(f)
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
    

def guardar_atajo():
    global atajo
    listener_atajo.stop()
    atajo = teclas_atajo.copy()
    texto = etiqueta_atajo.cget("text")
    config['general']['atajo'] = texto
    with open(config_file, 'w') as f:
        config.write(f)
    boton_capturar.config(text="Capturar atajo", command=activar_modo_captura)


    
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
            
def limpiar_atajo():
    teclas_atajo.clear()
    etiqueta_atajo.config(text="Sin atajo")
            
cargar_atajo_desde_config()


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
    pystray.Menu.SEPARATOR,                                                  #Línea separadora  
    pystray.MenuItem("Acerca de", lambda: ventana_acerca_de.deiconify()),
    pystray.Menu.SEPARATOR,
    pystray.MenuItem("Salir", cerrar_app)
)

icono = pystray.Icon("nombre", imagen_icono_desactivado, "tu texto aquí", menu=menu_icono)
hilo_icono = threading.Thread(target=icono.run_detached, daemon=True)

hilo_icono.start()
threading.Timer(0.25, al_iniciar_icono, args=[icono]).start()


    
#Código de la ventana Opciones
ventana_opciones = tk.Tk()                                                   #abre una ventana
iniciar_activado = tk.IntVar()

icono_tk = ImageTk.PhotoImage(imagen_icono_activado)                         #Estos dos comandos ponen el icono en las ventanas
ventana_opciones.iconphoto(True, icono_tk)

ventana_opciones.title("Opciones")                                           #título de la ventana
ventana_opciones.geometry("300x200")                                         #ancho x alto de la ventana (en píxeles)
ventana_opciones.withdraw()                                                  # La ventana no se abre directamente al correr la app
ventana_opciones.protocol("WM_DELETE_WINDOW", ventana_opciones.withdraw)     #Permite ocultar la ventana (para q abria siempre)


etiqueta_margen = tk.Label(ventana_opciones, text="Margen:")                 #esta es la opcion para el margen y como configurarlo
spinbox_margen = tk.Spinbox(ventana_opciones, from_=2, to=10, width=3)       #Configuración del Buffer 
etiqueta_margen.grid(row=0, column=0)
spinbox_margen.grid(row=0, column=1)
spinbox_margen.delete(0, tk.END)
spinbox_margen.insert(0, margen)
boton_ok = tk.Button(ventana_opciones, text="OK", command=margen_opciones)
boton_ok.grid(row=1, column=1)
boton_cancelar = tk.Button(ventana_opciones, text="Cancelar", command=cancelar_opciones)
boton_cancelar.grid(row=1, column=2)

checkbox_iniciar = tk.Checkbutton(ventana_opciones, text="Iniciar activado", variable=iniciar_activado)
checkbox_iniciar.grid(row=1, column=0)
iniciar_activado.set(activado)

boton_capturar = tk.Button(ventana_opciones, text="Capturar atajo", command=activar_modo_captura)
boton_capturar.grid(row=2, column=0)
etiqueta_atajo = tk.Label(ventana_opciones, text="Sin atajo")
etiqueta_atajo.grid(row=2, column=1)
etiqueta_atajo.config(text=config['general']['atajo'])

boton_limpiar = tk.Button(ventana_opciones, text="Limpiar", command=limpiar_atajo)
boton_limpiar.grid(row=2, column=2)


#Código del Acerca de...
ventana_acerca_de = tk.Toplevel()                                              #abre una ventana
ventana_acerca_de.title("Acerca de")                                           #título de la ventana
ventana_acerca_de.geometry("350x200")                                          #ancho x alto de la ventana (en píxeles)
ventana_acerca_de.withdraw()  
ventana_acerca_de.protocol("WM_DELETE_WINDOW", ventana_acerca_de.withdraw)     #Permite ocultar la ventana (para q abria siempre)
tk.Label(ventana_acerca_de, text="Projecto NT", font=("Arial", 14, "bold")).pack(pady=5)
tk.Label(ventana_acerca_de, text="Versión 0.5").pack()
tk.Label(ventana_acerca_de, text="Autor: GAB").pack()
tk.Label(ventana_acerca_de, text="Programa para escribir caracteres especiales del Esperanto.").pack(pady=5)
tk.Label(ventana_acerca_de, text="cx→ĉ  gx→ĝ  hx→ĥ  jx→ĵ  sx→ŝ  ux→ŭ").pack()


#################
#Si el usuario configuró iniciar activado, arranca el listener directamente

listener = keyboard.Listener(on_press=al_presionar, on_release=al_soltar)
listener.start()
#

ventana_opciones.mainloop()  # es para mantener la ventana abierta



