########################################################
##                  TELEFONISTA.PY                    ##
##   Canal de eventos del programa.                   ##
##   Recibe llamadas y las redirige a quien           ##
##   corresponde. Es el único que conoce a todos.     ##
########################################################

import logger


##############################################################
##              CLASE TELEFONISTA                           ##
##############################################################

class Telefonista:

    def __init__(self, config, teclado, interfaz, app, acerca):
        self.config   = config
        self.teclado  = teclado
        self.interfaz = interfaz
        self.app      = app
        self.acerca   = acerca

        # Canal de eventos — {evento: [funciones suscritas]}
        self._canal = {}

        # Arma todas las suscripciones al arrancar
        self._suscribir_todo()

        # Le pasa la función publicar a quien la necesita
        self.interfaz.publicar = self.publicar
        self.app.publicar      = self.publicar
        self.acerca.publicar   = self.publicar

        # Teclado necesita publicar eventos de captura
        self.teclado.publicar = self.publicar
        
        # Muestra los nombres bonitos al arrancar
        self._mostrar_deshacer_guardado()
        self._mostrar_atajo_guardado()
        

    ##############################################################
    ##              CANAL DE EVENTOS                            ##
    ##############################################################

    def suscribir(self, evento, funcion):
        # Registra una función para que sea llamada cuando ocurra el evento
        if evento not in self._canal:
            self._canal[evento] = []
        self._canal[evento].append(funcion)

    def publicar(self, evento, datos=None):
        # Llama a todas las funciones suscritas al evento
        if evento not in self._canal:
            logger.log_errores.debug(f"TELEFONISTA: evento desconocido '{evento}'")
            return
        for funcion in self._canal[evento]:
            if datos is not None:
                funcion(datos)
            else:
                funcion()


    ##############################################################
    ##              SUSCRIPCIONES                               ##
    ##   Aquí se define quién reacciona a qué evento.          ##
    ##   Este es el único lugar que se modifica cuando         ##
    ##   cambia la comunicación entre clases.                  ##
    ##############################################################

    def _suscribir_todo(self):
        logger.log_sistema.debug("suscribiendo todo")

        # -- Opciones --
        self.suscribir("guardar_opciones",  self.interfaz.leer_valores)
        self.suscribir("guardar_opciones",  self.config.guardar)
        self.suscribir("guardar_opciones",  self.teclado.actualizar_diccionario)
        self.suscribir("guardar_opciones",  self._guardar_arranque)
        self.suscribir("guardar_opciones",  self.interfaz.cerrar_opciones)
        self.suscribir("guardar_opciones", self.teclado.cargar_tecla_deshacer)
        self.suscribir("cancelar_opciones", self.interfaz.cerrar_opciones)
        self.suscribir("guardar_opciones",  lambda: self.interfaz.entry_prueba.delete(0, "end"))
        self.suscribir("cancelar_opciones", lambda: self.interfaz.entry_prueba.delete(0, "end"))
        self.suscribir("actualizar_diccionario", lambda: setattr(self.teclado, 'buffer_deshacer', []))
        self.suscribir("actualizar_diccionario", self.interfaz.leer_valores)
        self.suscribir("actualizar_diccionario", self.config.guardar)
        self.suscribir("actualizar_diccionario", self.teclado.actualizar_diccionario)
        self.suscribir("actualizar_diccionario", self.teclado.buffer_tipeo.clear)
        self.suscribir("actualizar_diccionario", self._actualizar_spinbox_margen)
        logger.log_sistema.debug("opciones ok")

        # -- Idioma --
        self.suscribir("cambiar_idioma",    self._cambiar_idioma)
        logger.log_sistema.debug("idioma ok")

        # -- Atajo de activación --
        self.suscribir("capturar_atajo",    self.app.iniciar_captura_atajo)
        self.suscribir("capturar_atajo",    lambda: self.interfaz.modo_captura("atajo", True))
        self.suscribir("guardar_atajo",     lambda: self.app.es_prohibida([self.app.traducir_tecla(t, "a_vk") for t in self.app.teclas_atajo]))
        self.suscribir("atajo_permitido",   self.app.guardar_atajo)
        self.suscribir("atajo_permitido",   self.app.cargar_atajo)
        self.suscribir("atajo_permitido",   lambda: self.interfaz.modo_captura("atajo", False))
        self.suscribir("atajo_permitido",   self._mostrar_atajo_guardado)
        self.suscribir("limpiar_atajo",     self.app.limpiar_atajo)
        self.suscribir("limpiar_atajo",     self.interfaz.mostrar_sin_atajo)
        self.suscribir("tecla_atajo_registrada", self._mostrar_atajo_capturando)
        self.suscribir("atajo_prohibido_comun",   lambda: self.interfaz.mostrar_atajo_prohibido("comun"))
        self.suscribir("atajo_prohibido_windows", lambda: self.interfaz.mostrar_atajo_prohibido("windows"))
        self.suscribir("atajo_prohibido_linux",   lambda: self.interfaz.mostrar_atajo_prohibido("linux"))

        # -- Tecla de deshacer --
        self.suscribir("capturar_deshacer",          self.teclado.iniciar_captura_deshacer)
        self.suscribir("capturar_deshacer",          lambda: self.interfaz.modo_captura("deshacer", True))
        self.suscribir("actualizar_deshacer",        self.interfaz.leer_valores)
        self.suscribir("actualizar_deshacer",        self.config.guardar)
        self.suscribir("tecla_deshacer_capturada",   lambda t: self._mostrar_deshacer_capturada(t))
        self.suscribir("tecla_deshacer_capturada",   lambda t: self.interfaz.modo_captura("deshacer", False))
        self.suscribir("limpiar_deshacer",           self.teclado.limpiar_deshacer)
        self.suscribir("limpiar_deshacer",           self.interfaz.mostrar_sin_deshacer)
        self.suscribir("tecla_deshacer_invalida",    self.interfaz.mostrar_tecla_invalida)
        logger.log_sistema.debug("deshacer ok")

        # -- Programa --
        self.suscribir("activar",           self.app.activar)
        self.suscribir("desactivar",        self.app.desactivar)
        self.suscribir("cerrar",            self.app.cerrar)
        self.suscribir("cerrar",            self.interfaz.ventana_opciones.quit)
        self.suscribir("abrir_opciones",    self.interfaz.ventana_opciones.deiconify)
        self.suscribir("abrir_acerca",      self.acerca.ventana.deiconify)
        logger.log_sistema.debug("programa ok")

        # -- Modo prueba --
        self.suscribir("iniciar_prueba", self._iniciar_prueba)
        self.suscribir("fin_prueba",     self._fin_prueba)

        # Refuerzo — pase lo que pase (X, Cancelar u OK) siempre se limpia el modo prueba
        self.suscribir("cancelar_opciones", lambda: self.publicar("fin_prueba"))
        self.suscribir("guardar_opciones",  lambda: self.publicar("fin_prueba"))

        # -- Mouse --
        self.suscribir("clic_mouse", lambda pos: (logger.log_sistema.debug(f"EVENTO clic_mouse RECIBIDO: {pos}"), self.teclado.verificar_clic_lejano(*pos)))
        self.suscribir("arrastre_mouse", lambda pos: (setattr(self.teclado, 'buffer_tipeo', []), setattr(self.teclado, 'buffer_deshacer', [])))

    ##############################################################
    ##              ACCIONES COMPUESTAS                         ##
    ##   Acciones que coordinan varias clases a la vez.        ##
    ##############################################################

    def _cambiar_idioma(self):
        codigos = {"Español": "es", "English": "en", "Esperanto": "eo"}
        idioma_anterior = self.config.idioma
        idioma_nuevo = codigos[self.interfaz.lingvo.get()]
        self.config.cambiar_idioma(idioma_nuevo)
        self.interfaz.traducir(idioma_anterior)
        self.interfaz.actualizar_bandera()
        self.app.crear_menu_icono()
        self.app.actualizar_icono()
        self._mostrar_atajo_guardado()
        self.interfaz.ventana_opciones.title(self.config.textos[self.config.idioma]["sistema"]["menu_opciones"])
        self.acerca.ventana.title(self.config.textos[self.config.idioma]["sistema"]["menu_acerca"])

    def _guardar_arranque(self):
        # Actualiza el registro/autostart según el checkbox de la interfaz
        self.app.inicio_arranque(self.interfaz.var_windows.get() == 1)

    def _mostrar_atajo_guardado(self):
        # Muestra el atajo con nombres bonitos después de guardar, cargar o cambiar idioma
        texto = self.config.cfg['atajo']['atajo']
        if texto == 'none' or texto == '':
            self.interfaz.mostrar_sin_atajo()
            return
        partes = texto.split()
        nombres = []
        for parte in partes:
            if parte.isdigit():
                vk = int(parte)
                # Busca primero en nombres_teclas del JSON, luego usa traducir_tecla
                nombre = self.config.nombres_teclas.get(str(vk)) or self.app.traducir_tecla(vk, "a_texto")
                nombres.append(nombre)
        self.interfaz.etiqueta_atajo.config(text=" + ".join(nombres))

    def _mostrar_deshacer_guardado(self):
        # Muestra la tecla de deshacer con nombre bonito al arrancar o al cambiar idioma
        texto = self.config.cfg['deshacer']['atajo_deshacer']
        if texto == 'none' or texto == '':
            self.interfaz.mostrar_sin_deshacer()
            return
        if texto.isdigit():
            # Formato nuevo — vk
            vk = int(texto)
            nombre = self.config.nombres_teclas.get(str(vk)) or self.app.traducir_tecla(vk, "a_texto")
        else:
            # Formato antiguo — texto como ctrl_l
            nombre = self.config.nombres_teclas.get(texto, texto.upper())
        self.interfaz.etiqueta_deshacer.config(text=nombre)

    def _mostrar_deshacer_capturada(self, tecla):
        # Recibe la tecla capturada, la convierte a vk y guarda en config
        vk = self.app.traducir_tecla(tecla, "a_vk")
        nombre = self.config.nombres_teclas.get(str(vk)) or self.app.traducir_tecla(vk, "a_texto")
        
        # Guarda el vk en config
        self.config.cfg['deshacer']['atajo_deshacer'] = str(vk)
        self.config.cfg['deshacer']['atajo_deshacer_nombre'] = nombre
        self.config.guardar()
        
        # Muestra el nombre bonito en interfaz
        self.interfaz.etiqueta_deshacer.config(text=nombre)
        
    def _mostrar_atajo_capturando(self):
        partes = []
        for t in self.app.teclas_atajo:
            vk = self.app.traducir_tecla(t, "a_vk")
            if vk:
                nombre = self.config.nombres_teclas.get(str(vk)) or self.app.traducir_tecla(vk, "a_texto")
                partes.append(nombre)
        if partes:
            texto = " + ".join(partes)
            self.interfaz.etiqueta_atajo.config(text=texto, bg="yellow")
                                  
    def _actualizar_spinbox_margen(self):
        # Deshabilita el spinbox de margen en modo doble tecla
        if self.config.afijo == "3":
            self.interfaz.spinbox_margen.config(state="disabled")
        else:
            self.interfaz.spinbox_margen.config(state="normal")

    def _iniciar_prueba(self):
        self._activado_antes_prueba = self.config.activado
        self.config.activado = 2

    def _fin_prueba(self):
        self.config.activado = getattr(self, '_activado_antes_prueba', 0)
        self.teclado.buffer_deshacer = []
        self.teclado.buffer_tipeo.clear()
        self.app.actualizar_icono()
