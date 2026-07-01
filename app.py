########################################################
##                     APP.PY                         ##
##   Arranque, bandeja del sistema y ciclo de vida    ##
##   del programa. Compatible con Windows y Linux.    ##
########################################################

import os
import sys
import threading
from pynput import keyboard
import pystray
import logger
import ctypes
import time


##############################################################
##              CLASE APP                                   ##
##############################################################

class App:

    def __init__(self, config, imagenes):
        self.config   = config      # Configuración del programa
        self.imagenes = imagenes    # Íconos generados en memoria
        self.central  = None        # Se asigna después desde klavaranto.py
        self.publicar = None        # Telefonista la asigna al arrancar
        self.icono    = None        # Ícono en bandeja — se crea en iniciar()
        self._lock_file = None      # Archivo de bloqueo para instancia única en Linux

        # Verifica que no haya otra instancia corriendo
        self.instancia_unica()

        # Carga el atajo de activación guardado
        self.atajo           = None      # Lista de objetos pynput con el hotkey
        self.teclas_atajo    = []        # Teclas capturadas durante la configuración
        self.teclas_presionadas = set()  # Teclas presionadas en este momento
        self.listener_captura = None     # Listener temporal durante la captura
        self._ultimo_atajo = 0           # Tiempo de enfriamiento para el atajo activado
        self.cargar_atajo()


    ##############################################################
    ##              INSTANCIA ÚNICA                             ##
    ##############################################################

    def instancia_unica(self):
        # Si está desactivado en config.ini (sección [dev]), se omite la verificación
        if self.config.instancia_unica == 0:
            return

        # Evita que se abran dos copias del programa al mismo tiempo
        if os.name == 'nt':
            # Windows — usa mutex del sistema operativo
            mutex = ctypes.windll.kernel32.CreateMutexW(None, False, "Klavaranto_Mutex")
            if ctypes.windll.kernel32.GetLastError() == 183:
                sys.exit()          # Ya hay una instancia corriendo — cierra esta
        else:
            # Linux — usa archivo de bloqueo
            self._lock_path = os.path.join(self.config.ruta_config, "klavaranto.lock")
            try:
                # Intenta crear el archivo en modo exclusivo
                self._lock_file = open(self._lock_path, 'x')
                self._lock_file.write(str(os.getpid()))
                self._lock_file.flush()
            except FileExistsError:
                sys.exit()          # Ya hay una instancia corriendo — cierra esta


    ##############################################################
    ##              ATAJO DE ACTIVACIÓN                         ##
    ##############################################################

    def traducir_tecla(self, tecla, direccion):
        # Puente entre el .ini (texto legible) y la memoria (vk)
        # Acepta objetos pynput, strings del .ini o números enteros (vk)
        # direccion="a_vk"    → convierte a número vk para guardar en memoria
        # direccion="a_texto" → convierte a texto legible para mostrar al usuario

        # Diccionario de vk que no coinciden con chr() — fallback para Linux
        vk_a_char = {
            96:  "Num 0", 97:  "Num 1", 98:  "Num 2", 99:  "Num 3",
            100: "Num 4", 101: "Num 5", 102: "Num 6", 103: "Num 7",
            104: "Num 8", 105: "Num 9",
            106: "*",     107: "+",     109: "-",     110: ".",     111: "/",
            186: ";",     187: "=",     188: ",",     189: "-",     190: ".",
            191: "/",     192: "`",     219: "[",     220: "|",     221: "]",     222: "'"
        }
        char_a_vk = {v: k for k, v in vk_a_char.items()}

        if direccion == "a_vk":
            # Si es un string (viene del .ini)
            if isinstance(tecla, str):
                if tecla == "<": return 226
                if tecla == ">": return 227
                if tecla in char_a_vk:
                    return char_a_vk[tecla]
                try:
                    return keyboard.Key[tecla].value.vk
                except KeyError:
                    pass
                if len(tecla) == 1:
                    return ord(tecla)
                return None

            # Si es un objeto pynput (viene de la captura)
            if hasattr(tecla, 'value'):
                return tecla.value.vk
            if hasattr(tecla, 'vk') and tecla.vk:
                return tecla.vk
            if hasattr(tecla, 'char') and tecla.char:
                return ord(tecla.char)
            return None

        else:  # a_texto
            # Si es un número entero (vk directo — viene de _mostrar_atajo_guardado)
            if isinstance(tecla, int):
                if os.name == 'nt':
                    # Windows — lee el nombre real según el layout del teclado del usuario
                    scan = ctypes.windll.user32.MapVirtualKeyW(tecla, 0)
                    buf  = ctypes.create_unicode_buffer(32)
                    ctypes.windll.user32.GetKeyNameTextW(scan << 16, buf, 32)
                    if buf.value:
                        return buf.value
                # Fallback para Linux o si GetKeyNameTextW falla
                if tecla in vk_a_char:
                    return vk_a_char[tecla]
                return chr(tecla) if tecla < 128 else str(tecla)

            # Si es un objeto pynput (viene de la captura)
            if hasattr(tecla, 'name') and tecla.name:          # Tecla especial → su nombre
                return tecla.name
            if hasattr(tecla, 'vk') and tecla.vk == 226:       # Tecla 
                return "<"
            if hasattr(tecla, 'vk') and tecla.vk == 227:       # Tecla >
                return ">"
            if hasattr(tecla, 'char') and tecla.char:           # Letra o número
                return tecla.char.lower()
            vk = self.traducir_tecla(tecla, "a_vk")            # Fallback — obtiene vk y llama recursivo
            if vk:
                return self.traducir_tecla(vk, "a_texto")
            return None


    def cargar_atajo(self):
        # Lee el atajo del .ini y lo convierte a lista de vk en memoria
        # Detecta automáticamente si es formato antiguo (ctrl_l + alt_l + 1)
        # o nuevo (162 164 49) y convierte en ambos casos
        texto = self.config.cfg['atajo']['atajo']
        if texto == 'none' or texto == '':
            self.atajo = None
            return

        partes = texto.split()

        # Detecta formato — si todos son números es formato nuevo, si no es antiguo
        if all(p.isdigit() for p in partes):
            # Formato nuevo — vk directos
            self.atajo = [int(p) for p in partes]
        else:
            # Formato antiguo — convertir texto a vk y reescribir el .ini
            self.atajo = []
            nombres = []
            for parte in texto.split(" + "):
                vk = self.traducir_tecla(parte, "a_vk")
                if vk:
                    self.atajo.append(vk)
                    nombre = self.config.nombres_teclas.get(str(vk), chr(vk) if vk < 128 else str(vk))
                    nombres.append(nombre)
            # Reescribe el .ini en formato nuevo
            self.config.cfg['atajo']['atajo'] = " ".join(str(v) for v in self.atajo)
            self.config.cfg['atajo']['atajo_nombre'] = " + ".join(nombres)
            self.config.guardar()

        logger.log_sistema.debug(f"ATAJO EN MEMORIA: {self.atajo}")


    def iniciar_captura_atajo(self):
        # Limpia las teclas anteriores e inicia el listener temporal
        logger.log_sistema.debug(f"iniciando captura atajo={self.atajo}")
        self.teclas_atajo.clear()
        self.atajo = []                 # Limpia memoria mientras se captura
        self.listener_captura = keyboard.Listener(on_press=self.registrar_tecla_atajo, suppress=True)
        self.listener_captura.start()
        


    def es_prohibida(self, vks):
        # Verifica si la combinación de vk está en la lista negra
        # Si es prohibida publica atajo_prohibido_X y limpia
        # Si no es prohibida publica atajo_permitido para que se guarde normalmente
        logger.log_sistema.debug(f"es_prohibida llamada con: {vks}")
        prohibidas_comunes = [
            {164, 115},   # Alt + F4
            {164, 9},     # Alt + Tab
        ]
        prohibidas_windows = [
            {162, 27},        # Ctrl + Esc
            {164, 27},        # Alt + Esc
            {162, 164, 46},   # Ctrl + Alt + Supr
        ]
        prohibidas_linux = [
            {162, 164, 84},   # Ctrl + Alt + T
            {162, 164, 8},    # Ctrl + Alt + Backspace
            {162, 164, 112},  # Ctrl + Alt + F1
            {162, 164, 113},  # Ctrl + Alt + F2
            {162, 164, 114},  # Ctrl + Alt + F3
            {162, 164, 115},  # Ctrl + Alt + F4
            {162, 164, 116},  # Ctrl + Alt + F5
            {162, 164, 117},  # Ctrl + Alt + F6
        ]

        combo = set(vks)
        tipo = None

        if combo in prohibidas_comunes:
            tipo = "comun"
        elif os.name == 'nt' and combo in prohibidas_windows:
            tipo = "windows"
        elif os.name != 'nt' and combo in prohibidas_linux:
            tipo = "linux"

        if tipo:
            if self.publicar:
                self.publicar(f"atajo_prohibido_{tipo}")
            self.teclas_atajo.clear()
            self.atajo = []
    
        else:
            # No es prohibida — publica para que se guarde normalmente
            if self.publicar:
                self.publicar("atajo_permitido")


    def registrar_tecla_atajo(self, tecla):
        # Registra cada tecla presionada durante la captura — máximo 3
        vk = self.traducir_tecla(tecla, "a_vk")
        if vk and len(self.teclas_atajo) < 3:
            if vk not in [self.traducir_tecla(t, "a_vk") for t in self.teclas_atajo]:
                self.teclas_atajo.append(tecla)
        if self.publicar:
            self.publicar("tecla_atajo_registrada")
        logger.log_sistema.debug(f"registrando vk={vk}")
        logger.log_sistema.debug(f"registrando vk={vk} teclas_atajo={[self.traducir_tecla(t, 'a_vk') for t in self.teclas_atajo]} atajo={self.atajo}")
        logger.log_sistema.debug(f"vk={vk} len={len(self.teclas_atajo)} not_in={vk not in (self.atajo or [])}")


    def guardar_atajo(self):
        # Detiene el listener y guarda el atajo en el .ini
        # La verificación de si es prohibida la hace es_prohibida antes de llegar aquí
        self.listener_captura.stop()
        self.atajo = [self.traducir_tecla(t, "a_vk") for t in self.teclas_atajo]
        if self.teclas_atajo:
            partes_vk     = []
            partes_nombre = []
            for t in self.teclas_atajo:
                vk    = self.traducir_tecla(t, "a_vk")
                texto = self.traducir_tecla(t, "a_texto")
                if vk:
                    partes_vk.append(str(vk))
                if texto:
                    nombre = self.config.nombres_teclas.get(str(vk), texto.upper())
                    partes_nombre.append(nombre)
            self.config.cfg['atajo']['atajo']        = " ".join(partes_vk)
            self.config.cfg['atajo']['atajo_nombre'] = " + ".join(partes_nombre)
        self.config.guardar()
        logger.log_sistema.debug(f"ATAJO GUARDADO: {self.config.cfg['atajo']['atajo']}")
        logger.log_sistema.debug(f"ATAJO EN MEMORIA: {self.atajo}")


    def limpiar_atajo(self):
        # Borra el atajo del .ini y de la memoria
        self.teclas_atajo.clear()
        self.atajo = None
        self.config.cfg['atajo']['atajo'] = 'none'
        self.config.cfg['atajo']['atajo_nombre'] = 'Sin atajo'
        self.config.guardar()
        logger.log_sistema.debug("ATAJO LIMPIADO")


    def detectar_atajo(self, tecla):
        # Verifica si las teclas presionadas coinciden con el atajo en memoria
        # Compara por vk — funciona aunque la tecla llegue con o sin modificadores
        if not self.atajo:
            return False
        vk = self.traducir_tecla(tecla, "a_vk")
        if vk and vk in self.atajo:
            self.teclas_presionadas.add(vk)
            if self.teclas_presionadas == set(self.atajo):
                ahora = time.time()
                if ahora - self._ultimo_atajo < 0.12:  # 300ms de cooldown
                    return False
                self._ultimo_atajo = ahora
                return True
        return False


    def soltar_atajo(self, tecla):
        # Elimina la tecla del set cuando se suelta
        vk = self.traducir_tecla(tecla, "a_vk")
        if vk:
            self.teclas_presionadas.discard(vk)


    ##############################################################
    ##              ACTIVAR Y DESACTIVAR                        ##
    ##############################################################

    def activar(self):
        # Activa el programa y actualiza el ícono
        self.config.activado = 1
        self.actualizar_icono()
        logger.log_sistema.debug("SCRIPT ACTIVADO")
        logger.log_sistema.debug(f"SCRIPT ACTIVADO — activado={self.config.activado}")

    def desactivar(self):
        # Desactiva el programa y actualiza el ícono
        self.config.activado = 0
        self.actualizar_icono()
        logger.log_sistema.debug("SCRIPT DESACTIVADO")
        logger.log_sistema.debug(f"SCRIPT DESACTIVADO — activado={self.config.activado}")

    def actualizar_icono(self):
        # Cambia el ícono y el título según el estado del programa
        if self.config.activado == 1:
            self.icono.icon  = self.imagenes.imagen_icono_activado
            self.icono.title = self.config.textos[self.config.idioma]["sistema"]["icono_activo"]
        else:
            self.icono.icon  = self.imagenes.imagen_icono_desactivado
            self.icono.title = self.config.textos[self.config.idioma]["sistema"]["icono_inactivo"]
        self.crear_menu_icono()      # Actualiza el menú también


    ##############################################################
    ##              ÍCONO EN BANDEJA                            ##
    ##############################################################

    def crear_menu_icono(self):
        # Crea el menú del botón derecho en la bandeja del sistema
        t = self.config.textos[self.config.idioma]["sistema"]
        menu = pystray.Menu(
            pystray.MenuItem(
                lambda item: t["menu_desactivar"] if self.config.activado == 1 else t["menu_activar"],
                lambda: self.desactivar() if self.config.activado == 1 else self.activar()
            ),
            pystray.MenuItem(lambda item: t["menu_opciones"],
                             lambda: self.publicar("abrir_opciones")),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem(lambda item: t["menu_acerca"],
                             lambda: self.publicar("abrir_acerca")),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem(lambda item: t["menu_salir"], self.cerrar)
        )
        if self.icono:
            self.icono.menu = menu
            self.icono.update_menu()
        else:
            self.icono = pystray.Icon(
                "Klavaranto",
                self.imagenes.imagen_icono_desactivado,
                t["icono_inactivo"],
                menu=menu
            )


    ##############################################################
    ##              ARRANCAR CON EL SISTEMA                     ##
    ##############################################################

    def inicio_arranque(self, activar):
        # Graba o borra la entrada para arrancar automáticamente con el sistema
        if os.name == 'nt':
            self._inicio_arranque_windows(activar)
        else:
            self._inicio_arranque_linux(activar)

    def _inicio_arranque_windows(self, activar):
        # Graba o borra entrada en el registro de Windows
        import winreg
        clave = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            "Software\\Microsoft\\Windows\\CurrentVersion\\Run",
            0, winreg.KEY_SET_VALUE
        )
        if activar:
            winreg.SetValueEx(clave, "Klavaranto", 0, winreg.REG_SZ, sys.argv[0])
        else:
            try:
                winreg.DeleteValue(clave, "Klavaranto")
            except FileNotFoundError:
                pass
        clave.Close()

    def _inicio_arranque_linux(self, activar):
        # Crea o borra archivo .desktop en ~/.config/autostart/
        ruta_autostart = os.path.join(os.path.expanduser("~"), ".config", "autostart")
        ruta_desktop   = os.path.join(ruta_autostart, "klavaranto.desktop")
        if activar:
            os.makedirs(ruta_autostart, exist_ok=True)
            with open(ruta_desktop, 'w') as f:
                f.write(f"""[Desktop Entry]
Type=Application
Name=Klavaranto
Exec={sys.executable}
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
""")
        else:
            try:
                os.remove(ruta_desktop)
            except FileNotFoundError:
                pass


    ##############################################################
    ##              CICLO DE VIDA                               ##
    ##############################################################

    def iniciar(self):
        # Arranca el listener de teclado en un hilo separado
        self.central.teclado.listener = keyboard.Listener(
            on_press   = self.central.columna_vertebral,
            on_release = self.soltar_atajo
        )
        self.central.teclado.listener.start()

        # Crea el menú del ícono
        self.crear_menu_icono()

        # Esta función se ejecuta sola, una sola vez, cuando el ícono ya está listo
        def cuando_listo(icono):
            icono.visible = True  # pystray no lo hace solo si usamos setup personalizado
            if self.config.activado == 1:
                self.activar()

        # Arranca el ícono en un hilo separado, avisando cuando esté listo
        hilo_icono = threading.Thread(
            target=self.icono.run_detached,
            kwargs={"setup": cuando_listo},
            daemon=True
        )
        hilo_icono.start()

        logger.log_sistema.debug("=== PROGRAMA LISTO ===")

 

    def cerrar(self):
        # Detiene el listener, cierra tkinter y mata el proceso limpiamente
        if self.central.teclado.listener:
            self.central.teclado.listener.stop()
        self.icono.stop()

        # En Linux libera el archivo de bloqueo
        if os.name != 'nt' and self._lock_file:
            self._lock_file.close()
            try:
                os.remove(self._lock_path)
            except FileNotFoundError:
                pass

        os.kill(os.getpid(), 9)