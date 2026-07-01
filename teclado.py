########################################################
##                   TECLADO.PY                       ##
##   Motor completo de procesamiento de teclado.      ##
##   Buffer, detección, reemplazo y deshacer.         ##
##   No se modifica salvo cambios de lógica mayor.    ##
########################################################

from pynput import keyboard
import ctypes
import logger
import os


##############################################################
##              ESTADOS DEL BUFFER_DESHACER                 ##
##                                                          ##
##   4 — modo captura, esperando tecla deshacer del usuario ##
##   3 — reemplazo recién ocurrido, espera carácter especial##
##   2 — espera el gatillante para deshacer                 ##
##   1 — contando letras originales que se reescriben       ##
##   0 — fin del ciclo, buffer limpio                       ##
##############################################################

ESTADO_CAPTURA  = 4
ESTADO_ESPECIAL = 3
ESTADO_GATILLO  = 2
ESTADO_CONTANDO = 1
ESTADO_FIN      = 0


##############################################################
##              CLASE TECLADO                               ##
##############################################################

class Teclado:

    def __init__(self, config):
        self.config   = config              # Para leer afijo, margen, opciones deshacer
        self.listener = None                # Listener principal — lo crea App

        # Controlador para simular teclas
        self.controlador = keyboard.Controller()

        # Buffer de tipeo — acumula las últimas N letras escritas por el usuario
        self.buffer_tipeo = []

        # Buffer de deshacer — guarda el estado antes del reemplazo
        # Formato: [letras_originales, caracter_resultante, estado]
        self.buffer_deshacer = []

        # Tecla configurada para deshacer
        self.tecla_deshacer = None
        
        # Para comenzar las publicaciones
        self.publicar = None

        # Diccionario de reemplazos — se genera al arrancar y al cambiar configuración
        self.diccionario = {}
        self.diccionario_defecto = {
            "cx":"ĉ", "gx":"ĝ", "hx":"ĥ", "jx":"ĵ", "sx":"ŝ", "ux":"ŭ",
            "Cx":"Ĉ", "Gx":"Ĝ", "Hx":"Ĥ", "Jx":"Ĵ", "Sx":"Ŝ", "Ux":"Ŭ",
            "CX":"Ĉ", "GX":"Ĝ", "HX":"Ĥ", "JX":"Ĵ", "SX":"Ŝ", "UX":"Ŭ",
            "cX":"ĉ", "gX":"ĝ", "hX":"ĥ", "jX":"ĵ", "sX":"ŝ", "uX":"ŭ"
        }
        self.actualizar_diccionario()
        self.cargar_tecla_deshacer()



    ##############################################################
    ##              PROCESAMIENTO PRINCIPAL                     ##
    ##############################################################

    def procesar(self, tecla):
        # Punto de entrada desde Central — decide qué hacer con cada tecla
        logger.log_sistema.debug(f"procesar tecla={tecla} buffer={self.buffer_deshacer}")
        
        # Paso 1 — estado 4: modo captura de tecla deshacer
        if self.buffer_deshacer and self.buffer_deshacer[2] == ESTADO_CAPTURA:
            logger.log_sistema.debug(f"CAPTURA: tecla={tecla} valida={self._es_valida_para_deshacer(tecla)}")
            if self._es_valida_para_deshacer(tecla):
                self.tecla_deshacer = tecla
                self.buffer_deshacer = []
                if self.publicar:
                    self.publicar("tecla_deshacer_capturada", tecla)
            else:
                if self.publicar:
                    self.publicar("tecla_deshacer_invalida")
            return
        
        # Paso 2 — si hay deshacer en curso, verificar la máquina de estados
        if self.buffer_deshacer and self.buffer_deshacer[2] != ESTADO_FIN:
            ejecutado = self._verificar_deshacer(tecla)
            if ejecutado:
                return True
            if self.buffer_deshacer and self.buffer_deshacer[2] != ESTADO_FIN:
                return
        else:
            # El buffer estaba en ESTADO_FIN — limpiar y continuar normalmente
            if self.buffer_deshacer:
                self.buffer_deshacer = []
                self.buffer_tipeo.clear()
                return

        # Paso 3 — clasificar la tecla
        tipo = self._clasificar(tecla)

        if tipo == "limpiar":
            self.buffer_tipeo.clear()
            return
        if tipo == "ignorar":
            return

        # Paso 4 — la tecla es una letra o número, agregarla al buffer_tipeo
        self.buffer_tipeo.append(tecla)
        if len(self.buffer_tipeo) > self.config.margen:
            self.buffer_tipeo.pop(0)

        # Paso 5 — buscar combinación en cada tecla
        combinacion, rango = self._buscar_combinacion()
        if combinacion is not None:
            self._transformar(combinacion, rango)
            
            
    
    ##############################################################
    ##              CLASIFICACIÓN DE TECLAS                     ##
    ##############################################################

    def _clasificar(self, tecla):
        # Determina qué hacer con la tecla antes de procesarla
        try:
            if tecla.char and tecla.char.isprintable():
                return "entrar"         # Letra, número o símbolo — entra al buffer
        except AttributeError:
            pass

        # Teclas especiales que limpian el buffer
        teclas_limpiar = {
            keyboard.Key.enter,
            keyboard.Key.tab,
            keyboard.Key.esc,
            keyboard.Key.space,
            keyboard.Key.backspace,
            keyboard.Key.up,
            keyboard.Key.down,
            keyboard.Key.left,
            keyboard.Key.right,
            keyboard.Key.home,
            keyboard.Key.end,
            keyboard.Key.page_up,
            keyboard.Key.page_down,
        }
        if tecla in teclas_limpiar:
            return "limpiar"

        # Modificadores y backspace — se ignoran
        return "ignorar"



    ##############################################################
    ##              BÚSQUEDA DE COMBINACIÓN                     ##
    ##############################################################

    def _buscar_combinacion(self):
        # Busca la combinación válida con menor rango en el buffer_tipeo
        logger.log_sistema.debug(f"buscando en buffer={[t.char for t in self.buffer_tipeo]} diccionario={list(self.diccionario.keys())[:3]}")
        mejor_combinacion = None
        mejor_rango       = None

        for combinacion in self.diccionario:
            pos_primera = None
            pos_segunda = None

            for pos, elemento in enumerate(self.buffer_tipeo):
                try:
                    if combinacion[0] == combinacion[1]:
                        # Doble tecla — busca dos posiciones distintas
                        if elemento.char == combinacion[0] and pos_primera is None:
                            pos_primera = pos
                        elif elemento.char == combinacion[1] and pos_primera is not None:
                            pos_segunda = pos
                    else:
                        # Modo normal — prefijo o sufijo
                        if elemento.char == combinacion[0]:
                            pos_primera = pos
                        if elemento.char == combinacion[1]:
                            pos_segunda = pos
                except AttributeError:
                    pass

            if pos_primera is not None and pos_segunda is not None and pos_primera < pos_segunda:
                rango = pos_segunda - pos_primera + 1
                # En modo doble tecla las letras deben ser contiguas — rango máximo 2
                if self.config.afijo == "3" and rango > 2:
                    continue
                if mejor_rango is None or rango < mejor_rango:
                    mejor_combinacion = combinacion
                    mejor_rango       = rango

        return mejor_combinacion, mejor_rango



    ##############################################################
    ##              TRANSFORMACIÓN                              ##
    ##############################################################

    def _transformar(self, combinacion, rango):
        # Guarda el estado, borra las letras originales y escribe el carácter especial
        letras_originales = self.buffer_tipeo[-rango:]
        caracter = self.diccionario[combinacion]
        if os.name == 'nt':
            if ctypes.windll.user32.GetKeyState(0x14) & 1:
                caracter = caracter.upper()

        # Guardar en buffer_deshacer antes de modificar nada
        self.buffer_deshacer = [letras_originales, caracter, ESTADO_ESPECIAL]

        # Borrar las letras originales
        for _ in range(rango):
            self.controlador.press(keyboard.Key.backspace)
            self.controlador.release(keyboard.Key.backspace)

        # Limpiar buffer_tipeo y escribir el carácter especial
        self.buffer_tipeo.clear()
        self.controlador.type(caracter)

        logger.log_reemplazos.debug(f"REEMPLAZO: {combinacion} → {caracter}")


    ##############################################################
    ##              DESHACER                                    ##
    ##############################################################

    def _verificar_deshacer(self, tecla):
        # Máquina de estados que controla el flujo del deshacer
        if tecla == keyboard.Key.backspace:
            if self.buffer_deshacer[2] == ESTADO_ESPECIAL or self.buffer_deshacer[2] == ESTADO_CONTANDO:
                return True              # Backspace del programa escribiendo solo — ignorar
            else:
                self.buffer_deshacer = []  # Backspace del usuario — cancela el deshacer
                return               # Backspace se ignora en el flujo de deshacer

        estado = self.buffer_deshacer[2]

        if estado == ESTADO_ESPECIAL:
            # Espera ver el carácter especial recién escrito (ĉ, ĝ, etc.)
            try:
                if tecla.char == self.buffer_deshacer[1]:
                    self.buffer_deshacer[2] = ESTADO_GATILLO
                else:
                    self.buffer_deshacer = []   # No coincide — cancela
            except AttributeError:
                self.buffer_deshacer = []
            return False

        if estado == ESTADO_GATILLO:
            # Espera el gatillante para ejecutar el deshacer
            if self._es_gatillante(tecla):
                self._ejecutar_deshacer(tecla)
                return True             # Se ejecutó el deshacer
            else:
                self.buffer_deshacer = []   # No es gatillante — cancela
            return False

        largo = len(self.buffer_deshacer[0])
        if ESTADO_FIN < estado <= largo - 1:
            # Cuenta las letras originales que se reescriben
            self.buffer_deshacer[2] -= 1
            return True

        if estado == ESTADO_FIN:
            # Fin del ciclo — limpia todo
            self.buffer_deshacer = []
            self.buffer_tipeo.clear()
            return True

        return False

    def _es_gatillante(self, tecla):
        # Detecta si la tecla activa el deshacer — extensible a futuro
        afijo = self.config.sufijo if self.config.afijo == "2" else self.config.prefijo

        # Método 1 — doble afijo o doble tecla
        if self.config.deshacer_cambio == 1:
            try:
                if self.config.afijo == "3":
                    # Modo doble tecla — gatilla con la misma letra base
                    letra_base = self.buffer_deshacer[0][0].char.lower()
                    if tecla.char.lower() == letra_base:
                        return True
                else:
                    # Modo prefijo/sufijo — gatilla con el afijo configurado
                    if tecla.char == afijo:
                        return True
            except AttributeError:
                pass

        # Método 2 — tecla personalizada
        if self.config.deshacer_tecla == 1 and self.tecla_deshacer:
            vk_tecla    = getattr(tecla, 'vk', None) or (tecla.value.vk if hasattr(tecla, 'value') else None)
            vk_deshacer = getattr(self.tecla_deshacer, 'vk', None) or (self.tecla_deshacer.value.vk if hasattr(self.tecla_deshacer, 'value') else None)
            if vk_tecla and vk_deshacer and vk_tecla == vk_deshacer:
                return True

        return False


    def _ejecutar_deshacer(self, tecla):
        # Borra el carácter especial y reescribe las letras originales
        caracter          = self.buffer_deshacer[1]
        letras_originales = self.buffer_deshacer[0]

        if os.name == 'nt':
            # Windows — suelta la tecla gatillante a nivel de sistema para que
            # ctrl/shift/alt no interfieran con los backspaces ni la reescritura
            if hasattr(tecla, 'name'):
                vk = tecla.value.vk if hasattr(tecla, 'value') else None
                if vk:
                    ctypes.windll.user32.keybd_event(vk, 0, 0x0002, 0)

            # Alt necesita +1 backspace igual que las letras normales
            # Ctrl y shift no lo necesitan
            teclas_sin_extra = hasattr(tecla, 'name') and tecla.name not in ['alt_l', 'alt_r', 'alt']
            backspaces = len(caracter) if teclas_sin_extra else len(caracter) + 1
            VK_BACK = 0x08
            for _ in range(backspaces):
                ctypes.windll.user32.keybd_event(VK_BACK, 0, 0, 0)
                ctypes.windll.user32.keybd_event(VK_BACK, 0, 0x0002, 0)

        else:
            # Linux — pynput nativo, el bug de modificadoras puede no existir aquí
            backspaces = len(caracter)
            for _ in range(backspaces):
                self.controlador.press(keyboard.Key.backspace)
                self.controlador.release(keyboard.Key.backspace)

        # Reescribir las letras originales
        for t in letras_originales:
            self.controlador.type(t.char)

        # Actualizar estado
        self.buffer_deshacer[2] = ESTADO_CONTANDO
        logger.log_reemplazos.debug(f"DESHACER: {caracter} → {''.join(t.char for t in letras_originales)}")



    ##############################################################
    ##              TECLA DESHACER                              ##
    ##############################################################

    def cargar_tecla_deshacer(self):
        # Lee la tecla de deshacer del config.ini — ahora guarda vk
        texto = self.config.cfg['deshacer']['atajo_deshacer']
        logger.log_sistema.debug(f"cargar_tecla_deshacer: texto={texto}")
        if texto == 'none' or texto == '':
            self.tecla_deshacer = None
            return
        if texto.isdigit():
            # Formato nuevo — vk directo
            self.tecla_deshacer = keyboard.KeyCode(vk=int(texto))
        else:
            # Formato antiguo — texto como ctrl_l
            try:
                self.tecla_deshacer = keyboard.Key[texto]
            except KeyError:
                self.tecla_deshacer = keyboard.KeyCode.from_char(texto.lower())
        logger.log_sistema.debug(f"cargar_tecla_deshacer: tecla_deshacer={self.tecla_deshacer}")

    def iniciar_captura_deshacer(self):
        # Activa el estado 4 — el listener principal captura la próxima tecla válida
        self.buffer_deshacer = [[], None, ESTADO_CAPTURA]

    def limpiar_deshacer(self):
        # Borra la tecla de deshacer asignada
        self.tecla_deshacer = None
        self.config.cfg['deshacer']['atajo_deshacer'] = 'none'
        self.config.guardar()
        logger.log_sistema.debug("TECLA DESHACER LIMPIADA")

    def _es_valida_para_deshacer(self, tecla):
        # Valida que la tecla no sea inválida para usar como deshacer
        try:
            if tecla.char and tecla.char.lower() in ["c","g","h","j","s","u","ĉ","ĝ","ĥ","ĵ","ŝ","ŭ"]:
                return False            # Letras del esperanto — bloqueadas
        except AttributeError:
            pass
        vk = getattr(tecla, 'vk', None) or (tecla.value.vk if hasattr(tecla, 'value') else None)
        if vk in [8, 37, 38, 39, 40]:  # Backspace y flechas — bloqueadas
            return False
        return True


    ##############################################################
    ##              DICCIONARIO                                 ##
    ##############################################################

    def actualizar_diccionario(self):
        # Genera el diccionario según el estilo configurado (prefijo, sufijo o doble tecla)
        estilo  = self.config.afijo
        sufijo  = self.config.sufijo
        prefijo = self.config.prefijo

        if estilo == "2":               # Modo sufijo — cx, gx, sx...
            varP, varS = "", sufijo
        elif estilo == "1":             # Modo prefijo — xc, xg, xs...
            varP, varS = prefijo, ""
        elif estilo == "3":             # Modo doble tecla — cc, gg, hh...
            self.diccionario = {
                "cc": "ĉ", "gg": "ĝ", "hh": "ĥ", "jj": "ĵ", "ss": "ŝ", "uu": "ŭ",
                "CC": "Ĉ", "GG": "Ĝ", "HH": "Ĥ", "JJ": "Ĵ", "SS": "Ŝ", "UU": "Ŭ",
                "Cc": "Ĉ", "cC": "ĉ",
                "Gg": "Ĝ", "gG": "ĝ",
                "Hh": "Ĥ", "hH": "ĥ",
                "Jj": "Ĵ", "jJ": "ĵ",
                "Ss": "Ŝ", "sS": "ŝ",
                "Uu": "Ŭ", "uU": "ŭ"
            }
            logger.log_sistema.debug(f"DICCIONARIO ACTUALIZADO: {list(self.diccionario.keys())[:3]}")
            return
        else:
            self.diccionario = self.diccionario_defecto
            return

        self.diccionario = {
            varP+"c"+varS:"ĉ", varP+"g"+varS:"ĝ", varP+"h"+varS:"ĥ",
            varP+"j"+varS:"ĵ", varP+"s"+varS:"ŝ", varP+"u"+varS:"ŭ",
            varP+"C"+varS:"Ĉ", varP+"G"+varS:"Ĝ", varP+"H"+varS:"Ĥ",
            varP+"J"+varS:"Ĵ", varP+"S"+varS:"Ŝ", varP+"U"+varS:"Ŭ",
            varP.upper()+"C"+varS.upper():"Ĉ", varP.upper()+"G"+varS.upper():"Ĝ",
            varP.upper()+"H"+varS.upper():"Ĥ", varP.upper()+"J"+varS.upper():"Ĵ",
            varP.upper()+"S"+varS.upper():"Ŝ", varP.upper()+"U"+varS.upper():"Ŭ"
        }
        logger.log_sistema.debug(f"actualizando diccionario sufijo={self.config.sufijo} prefijo={self.config.prefijo}")
        logger.log_sistema.debug(f"DICCIONARIO ACTUALIZADO: {list(self.diccionario.keys())[:3]}")