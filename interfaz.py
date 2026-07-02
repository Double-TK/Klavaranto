########################################################
##                   INTERFAZ.PY                      ##
##   Ventana principal de opciones del programa.      ##
##   Usa tkinter clásico.                             ##
##   Solo lógica visual — las acciones las coordina   ##
##   Telefonista.                                     ##
########################################################

import os
import logger
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk



##############################################################
##              CLASE TOOLTIP                               ##
##############################################################

class Tooltip:
    def __init__(self, widget, texto, clave=""):
        self.widget       = widget
        self.texto        = texto
        self.clave        = clave
        self.ventana_tip  = None
        self.after_id     = None
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
        tk.Label(self.ventana_tip, text=self.texto,
                 background="lightyellow", relief="solid",
                 borderwidth=1, wraplength=400).pack()

    def ocultar(self, event=None):
        if self.after_id:
            self.widget.after_cancel(self.after_id)
            self.after_id = None
        if self.ventana_tip:
            self.ventana_tip.destroy()
            self.ventana_tip = None


##############################################################
##              CLASE INTERFAZ                              ##
##############################################################

class Interfaz:

    def __init__(self, config, imagenes):
        self.config   = config
        self.imagenes = imagenes
        self.publicar = None
        self.tooltips = []

        self.var_windows      = None
        self.iniciar_activado = None
        self.var_deshacer     = None
        self.atajo_deshacer   = None
        self.estilo_entrada   = None
        self.lingvo           = None

        self.spinbox_margen       = None
        self.entry_prefijo        = None
        self.entry_sufijo         = None
        self.entry_prueba         = None
        self.etiqueta_atajo       = None
        self.etiqueta_deshacer    = None
        self.frame_atajo_captura  = None
        self.frame_atajo_deshacer = None
        self.boton_capturar       = None
        self.boton_limpiar        = None
        self.boton_ok             = None
        self.boton_cancelar       = None
        self.capturar_deshacer    = None
        self.limpiar_deshacer     = None
        self.etiqueta_bandera     = None
        self.banderas             = {}

        self._crear_ventana()


    ##############################################################
    ##              CREACIÓN DE LA VENTANA                      ##
    ##############################################################

    def _crear_ventana(self):
        t = self.config.textos[self.config.idioma]["interfaz"]

        self.ventana_opciones = tk.Tk()
        icono_tk = ImageTk.PhotoImage(self.imagenes.imagen_icono_activado)
        self.ventana_opciones.iconphoto(True, icono_tk)
        self.ventana_opciones.title(self.config.textos[self.config.idioma]["sistema"]["menu_opciones"])
        self.ventana_opciones.geometry("470x580")
        self.ventana_opciones.withdraw()
        self.ventana_opciones.protocol("WM_DELETE_WINDOW", lambda: self.publicar("cancelar_opciones") if self.publicar else self.ventana_opciones.withdraw())
        self.ventana_opciones.resizable(False, False)
        self.ventana_opciones.columnconfigure(0, weight=1)

        self._crear_variables()
        self._crear_banderas()
        self._crear_secciones()


    def _crear_variables(self):
        self.var_windows      = tk.IntVar(value=self.config.iniciar_windows)
        self.iniciar_activado = tk.IntVar(value=self.config.activado)
        self.var_deshacer     = tk.IntVar(value=self.config.deshacer_cambio)
        self.atajo_deshacer   = tk.IntVar(value=self.config.deshacer_tecla)
        self.estilo_entrada   = tk.StringVar(value=self.config.afijo)
        
        nombres               = {"es": "Español", "en": "English", "eo": "Esperanto"}
        self.lingvo           = tk.StringVar(value=nombres[self.config.idioma])


    def _crear_banderas(self):
        self.banderas = {
            "es": ImageTk.PhotoImage(self.imagenes.imagen_bandera_es),
            "en": ImageTk.PhotoImage(self.imagenes.imagen_bandera_en),
            "eo": ImageTk.PhotoImage(self.imagenes.imagen_bandera_eo)
        }


    def _crear_secciones(self):
        self._seccion_general()
        self._seccion_estilos()
        self._seccion_deshacer()
        self._seccion_prueba()
        self._seccion_sistema()
        self._seccion_atajo()
        self._seccion_botones()


    ##############################################################
    ##              SECCIONES DE LA VENTANA                     ##
    ##############################################################

    def _seccion_general(self):
        t = self.config.textos[self.config.idioma]["interfaz"]
        frame = self._crear_frame_seccion(self.ventana_opciones, t["sec_general"], 0)

        # Ajusta este número (ej. 250, 265, 280) para alinear el Idioma con lo de abajo
        frame.columnconfigure(0, minsize=185)

        sub_frame_margen = tk.Frame(frame)
        sub_frame_margen.grid(row=0, column=0, sticky="w")

        label_margen = self._crear_label(sub_frame_margen, t["margen"], 0, 0)
        self.spinbox_margen = self._crear_spinbox(sub_frame_margen, 0, 1, self.config.margen, 2, 4)
        
        self.tooltips.append(Tooltip(label_margen, self.config.textos[self.config.idioma]["tooltips"]["tooltip_margen"], "tooltip_margen"))

        self._crear_label(frame, t["idioma"], 0, 1, padx=(15, 0))
        
        combo = ttk.Combobox(frame, textvariable=self.lingvo,
                             values=["Español", "English", "Esperanto"], width=10, state="readonly")
        combo.grid(row=0, column=2)
        combo.bind("<<ComboboxSelected>>", lambda e: self.publicar("cambiar_idioma"))

        frame_bandera = tk.Frame(frame, relief="groove", borderwidth=1)
        frame_bandera.grid(row=0, column=3, padx=5)
        self.etiqueta_bandera = tk.Label(frame_bandera, image=self.banderas[self.config.idioma])
        self.etiqueta_bandera.grid(padx=2, pady=2)


    def _seccion_estilos(self):
        t  = self.config.textos[self.config.idioma]["interfaz"]   # Textos de la interfaz
        tt = self.config.textos[self.config.idioma]["tooltips"]   # Textos de los tooltips
        frame = self._crear_frame_seccion(self.ventana_opciones, t["sec_estilos"], 1)

        # Ancho fijo para la columna de radios — evita que las otras columnas se muevan
        frame.columnconfigure(0, minsize=200)

        # -- PREFIJO --
        radio_prefijo = self._crear_radio(frame, t["prefijo"], self.estilo_entrada, "1", 0, 0,
                          comando=lambda: self.publicar("actualizar_diccionario") if self.publicar else None)
        self.entry_prefijo = self._crear_entry_afijo(frame, 0, self.config.prefijo, padx=(5, 0))
        self._crear_label(frame, t["texto_prefijo"], 0, 2, sticky="w", padx=(5, 0), pady=5)
        self.tooltips.append(Tooltip(radio_prefijo,      tt["tooltip_prefijo"], "tooltip_prefijo"))
        self.tooltips.append(Tooltip(self.entry_prefijo, tt["tooltip_prefijo"], "tooltip_prefijo"))

        # -- SUFIJO --
        radio_sufijo = self._crear_radio(frame, t["sufijo"], self.estilo_entrada, "2", 1, 0,
                          comando=lambda: self.publicar("actualizar_diccionario") if self.publicar else None)
        self.entry_sufijo = self._crear_entry_afijo(frame, 1, self.config.sufijo, padx=(5, 0))
        self._crear_label(frame, t["texto_sufijo"], 1, 2, sticky="w", padx=(5, 0), pady=5)
        self.tooltips.append(Tooltip(radio_sufijo,      tt["tooltip_sufijo"], "tooltip_sufijo"))
        self.tooltips.append(Tooltip(self.entry_sufijo, tt["tooltip_sufijo"], "tooltip_sufijo"))

        # -- DOBLE TECLA — sin entry, texto explicativo alineado con los otros --
        radio_doble = self._crear_radio(frame, t["doble_tecla"], self.estilo_entrada, "3", 2, 0,
                          comando=lambda: self.publicar("actualizar_diccionario") if self.publicar else None)
        self._crear_label(frame, t["texto_doble_tecla"], 2, 1, sticky="w", padx=(5, 0), pady=5, columnspan=2)
        self.tooltips.append(Tooltip(radio_doble, tt["tooltip_doble_tecla"], "tooltip_doble_tecla"))

        # -- PERSONALIZADO — deshabilitado por ahora --
        cb_personalizado = tk.Checkbutton(frame, text=t["personalizado"], state="disabled")
        cb_personalizado.grid(row=3, column=0, sticky="w", columnspan=2)
        self.tooltips.append(Tooltip(cb_personalizado, tt["tooltip_personalizado"], "tooltip_personalizado"))

        frame_boton = tk.Frame(frame)
        frame_boton.grid(row=3, column=1, sticky="w", pady=5, columnspan=2, padx=(5, 0))
        tk.Button(frame_boton, text=t["personalizado"], state="disabled").grid(row=0, column=0)


    def _seccion_deshacer(self):
        t  = self.config.textos[self.config.idioma]["interfaz"]   # Textos de la interfaz
        tt = self.config.textos[self.config.idioma]["tooltips"]   # Textos de los tooltips
        frame = self._crear_frame_seccion(self.ventana_opciones, t["sec_deshacer"], 2)

        # -- CHECKBOXES de método de deshacer --
        cb_deshacer_afijo = self._crear_checkbox(frame, t["deshacer_afijo"], self.var_deshacer, 0, 0,
                    comando=lambda: self.publicar("actualizar_deshacer") if self.publicar else None)
        cb_deshacer_tecla = self._crear_checkbox(frame, t["deshacer_tecla"], self.atajo_deshacer, 1, 0,
                            comando=lambda: self.publicar("actualizar_deshacer") if self.publicar else None)
        self.tooltips.append(Tooltip(cb_deshacer_afijo, tt["tooltip_deshacer_afijo"], "tooltip_deshacer_afijo"))
        self.tooltips.append(Tooltip(cb_deshacer_tecla, tt["tooltip_deshacer_tecla"], "tooltip_deshacer_tecla"))

        # -- CONTROLES de captura de tecla deshacer --
        frame_controles = tk.Frame(frame)
        frame_controles.grid(row=1, column=1, sticky="e", pady=2)
        frame.columnconfigure(1, weight=1)

        # Recuadro que muestra la tecla asignada
        self.frame_atajo_deshacer = tk.Frame(frame_controles, relief="groove", borderwidth=2)
        self.frame_atajo_deshacer.grid(row=0, column=0, padx=2)
        self.etiqueta_deshacer = tk.Label(self.frame_atajo_deshacer,
                                          text=self.config.atajo_deshacer,
                                          width=8, justify="center")
        self.etiqueta_deshacer.grid(row=0, column=0, padx=2, pady=2)

        # Botones capturar y limpiar
        self.capturar_deshacer = self._crear_boton(frame_controles, t["capturar"],
                                                   lambda: self.publicar("capturar_deshacer"), 0, 1, width=8)
        self.limpiar_deshacer  = self._crear_boton(frame_controles, t["limpiar"],
                                                   lambda: self.publicar("limpiar_deshacer"), 0, 2, width=8)


    def _seccion_prueba(self):
        # Caja de texto para probar el programa sin salir de opciones
        t = self.config.textos[self.config.idioma]["interfaz"]
        frame = self._crear_frame_seccion(self.ventana_opciones, t["prueba"], 3)
        frame.columnconfigure(0, weight=1)

        entry = tk.Entry(frame, width=55, font=("Arial", 11))
        entry.bind("<FocusIn>",  lambda e: self.publicar("iniciar_prueba") if self.publicar else None)
        entry.bind("<FocusOut>", lambda e: self.publicar("fin_prueba") if self.publicar else None)
        entry.bind("<KeyRelease>", lambda e: entry.delete(0, tk.END) if len(entry.get()) >= 40 else None)  # Se borra sola al llenarse
        entry.grid(row=0, column=0, padx=5, ipady=5, pady=5)
        self.entry_prueba = entry


    def _seccion_sistema(self):
        t     = self.config.textos[self.config.idioma]["interfaz"]
        frame = self._crear_frame_seccion(self.ventana_opciones, t["sec_sistema"], 4)

        # Checkboxes de opciones del sistema
        self._crear_checkbox(frame, t["iniciar_activado"], self.iniciar_activado, 0, 0)
        self._crear_checkbox(frame, t["iniciar_windows"],  self.var_windows,      1, 0)


    def _seccion_atajo(self):
        t     = self.config.textos[self.config.idioma]["interfaz"]
        frame = self._crear_frame_seccion(self.ventana_opciones, t["sec_atajo"], 5)
        frame.columnconfigure(1, weight=1)

        # Botones capturar y limpiar atajo
        self.boton_capturar = self._crear_boton(frame, t["capturar_atajo"],
                                                lambda: self.publicar("capturar_atajo"), 0, 0, width=17)
        self.boton_limpiar  = self._crear_boton(frame, t["limpiar"],
                                                lambda: self.publicar("limpiar_atajo"), 1, 0, width=17)

        # Recuadro que muestra el atajo actual
        self.frame_atajo_captura = tk.Frame(frame, relief="groove", borderwidth=2)
        self.frame_atajo_captura.grid(row=0, column=1, padx=2, sticky="nsew", rowspan=2, ipady=5)
        self.frame_atajo_captura.columnconfigure(0, weight=1)
        self.frame_atajo_captura.rowconfigure(0, weight=1)

        self.etiqueta_atajo = tk.Label(self.frame_atajo_captura,
                                       text=self.config.atajo, width=36, justify="center")
        self.etiqueta_atajo.grid(row=0, column=0)


    def _seccion_botones(self):
        t     = self.config.textos[self.config.idioma]["interfaz"]
        frame = tk.Frame(self.ventana_opciones)
        frame.grid(row=6, column=0, pady=10)

        # Botones OK y Cancelar
        self.boton_ok       = self._crear_boton(frame, t["boton_ok"],
                                                lambda: self.publicar("guardar_opciones"), 0, 0)
        self.boton_cancelar = self._crear_boton(frame, t["boton_cancelar"],
                                                lambda: self.publicar("cancelar_opciones"), 0, 1)


    ##############################################################
    ##              MÉTODOS VISUALES                            ##
    ##############################################################

    def modo_captura(self, elemento, capturando):
        if elemento == "atajo":
            frame    = self.frame_atajo_captura
            etiqueta = self.etiqueta_atajo
            botones  = [self.boton_limpiar, self.boton_ok, self.boton_cancelar]
            texto    = self.config.textos[self.config.idioma]["interfaz"]["presione_atajo"]
        else:
            frame    = self.frame_atajo_deshacer
            etiqueta = self.etiqueta_deshacer
            botones  = [self.capturar_deshacer, self.limpiar_deshacer, self.boton_ok, self.boton_cancelar]
            texto    = self.config.textos[self.config.idioma]["interfaz"]["presione"]

        if capturando:
            frame.config(bg="yellow")
            etiqueta.config(text=texto, bg="yellow")
            for b in botones:
                b.config(state="disabled")
            # Deshabilita los botones del otro modo para evitar capturas simultáneas
            if elemento == "atajo":
                self.capturar_deshacer.config(state="disabled")
                self.limpiar_deshacer.config(state="disabled")
            else:
                self.boton_capturar.config(state="disabled")
                self.boton_limpiar.config(state="disabled")
            # El botón capturar cambia a guardar
            if elemento == "atajo":
                self.boton_capturar.config(
                    text=self.config.textos[self.config.idioma]["interfaz"]["guardar_atajo"],
                    command=lambda: self.publicar("guardar_atajo"),
                    state="normal"
                )
        else:
            frame.config(bg="SystemButtonFace")
            etiqueta.config(bg="SystemButtonFace")
            for b in botones:
                b.config(state="normal")
            # Reactiva los botones del otro modo
            if elemento == "atajo":
                self.capturar_deshacer.config(state="normal")
                self.limpiar_deshacer.config(state="normal")
            else:
                self.boton_capturar.config(state="normal")
                self.boton_limpiar.config(state="normal")
            # El botón guardar vuelve a ser capturar
            if elemento == "atajo":
                self.boton_capturar.config(
                    text=self.config.textos[self.config.idioma]["interfaz"]["capturar_atajo"],
                    command=lambda: self.publicar("capturar_atajo"),
                    state="normal"
                )

    def mostrar_sin_atajo(self):
        self.etiqueta_atajo.config(text=self.config.textos[self.config.idioma]["interfaz"]["sin_atajo"])

    def mostrar_sin_deshacer(self):
        self.etiqueta_deshacer.config(text=self.config.textos[self.config.idioma]["interfaz"]["sin_tecla"])

    def mostrar_atajo(self, partes):
        nombres = [self.config.nombres_teclas.get(p, p) for p in partes]
        self.etiqueta_atajo.config(text=" + ".join(nombres))

    def mostrar_deshacer(self, clave):
        if clave and clave != 'none':
            self.etiqueta_deshacer.config(text=self.config.nombres_teclas.get(clave, clave.upper()))
        else:
            self.mostrar_sin_deshacer()

    def actualizar_bandera(self):
        self.etiqueta_bandera.config(image=self.banderas[self.config.idioma])

    def cerrar_opciones(self):
        self.ventana_opciones.withdraw()

    def leer_valores(self):
        self.config.cfg['general']['margen']             = str(self.spinbox_margen.get())
        self.config.cfg['inicio']['iniciar_activado']    = str(self.iniciar_activado.get())
        self.config.cfg['inicio']['iniciar_con_windows'] = str(self.var_windows.get())
        self.config.cfg['entrada']['afijo']              = self.estilo_entrada.get()
        self.config.cfg['entrada']['prefijo']            = self.entry_prefijo.get()
        self.config.cfg['entrada']['sufijo']             = self.entry_sufijo.get()
        self.config.cfg['deshacer']['deshacer_cambio']   = str(self.var_deshacer.get())
        self.config.cfg['deshacer']['deshacer_tecla']    = str(self.atajo_deshacer.get())
                             
        codigos = {"Español": "es", "English": "en", "Esperanto": "eo"}
        self.config.cfg['general']['idioma'] = codigos[self.lingvo.get()]

    def traducir(self, idioma_anterior):
        t_anterior = {**self.config.textos[idioma_anterior]["interfaz"], **self.config.textos[idioma_anterior]["sistema"]}
        t_nuevo    = {**self.config.textos[self.config.idioma]["interfaz"], **self.config.textos[self.config.idioma]["sistema"]}

        def recorrer(widget):
            try:
                texto = widget.cget("text")
                for clave, valor in t_anterior.items():
                    if texto == valor:
                        widget.config(text=t_nuevo[clave])
                        break
            except:
                pass
            for hijo in widget.winfo_children():
                recorrer(hijo)

        recorrer(self.ventana_opciones)
        for t in self.tooltips:
            t.texto = self.config.textos[self.config.idioma]["tooltips"][t.clave]


    ##############################################################
    ##              VALIDACIÓN                                  ##
    ##############################################################

    def _validar_afijo(self, valor):
        if len(valor) > 1:
            return False
        letras_bloqueadas = ["c","g","h","j","s","u","C","G","H","J","S","U",
                             "ĉ","ĝ","ĥ","ĵ","ŝ","ŭ","Ĉ","Ĝ","Ĥ","Ĵ","Ŝ","Ŭ"]
        return valor not in letras_bloqueadas


    ##############################################################
    ##              AUXILIARES                                  ##
    ##############################################################

    def _crear_frame_seccion(self, parent, titulo, fila):
        # Crea un LabelFrame estándar
        frame = tk.LabelFrame(parent, text=titulo)
        frame.grid(row=fila, column=0, padx=5, pady=5, sticky="ew")
        return frame

    def _crear_label(self, parent, texto, fila, columna, padx=0, pady=2, sticky="", columnspan=1):
        label = tk.Label(parent, text=texto)
        label.grid(row=fila, column=columna, padx=padx, pady=pady, sticky=sticky, columnspan=columnspan)
        return label

    def _crear_boton(self, parent, texto, comando, fila, columna, padx=2, pady=2, width=None, state="normal", columnspan=1, sticky=""):
        boton = tk.Button(parent, text=texto, command=comando, state=state)
        if width:
            boton.config(width=width)
        boton.grid(row=fila, column=columna, padx=padx, pady=pady, columnspan=columnspan, sticky=sticky)
        return boton

    def _crear_checkbox(self, parent, texto, variable, fila, columna, comando=None):
        cb = tk.Checkbutton(parent, text=texto, variable=variable, command=comando)
        cb.grid(row=fila, column=columna, sticky="w")
        return cb

    def _crear_radio(self, parent, texto, variable, valor, fila, columna, columnspan=1, comando=None):
        radio = tk.Radiobutton(parent, text=texto, variable=variable, value=valor, command=comando)
        radio.grid(row=fila, column=columna, sticky="w", columnspan=columnspan)
        return radio

    def _crear_spinbox(self, parent, fila, columna, valor_inicial, minimo, maximo):
        # Crea un Spinbox estándar de tkinter
        spinbox = tk.Spinbox(parent, from_=minimo, to=maximo, width=3)
        spinbox.grid(row=fila, column=columna, padx=5)
        spinbox.delete(0, tk.END)
        spinbox.insert(0, valor_inicial)
        return spinbox

    def _crear_entry_afijo(self, parent, fila, valor_inicial, padx=(140, 0)):
        vcmd  = self.ventana_opciones.register(lambda P, W: self._validar_y_colorear(P, W))
        entry = tk.Entry(parent, width=3, validate="key",
                         validatecommand=(vcmd, "%P", "%W"),
                         justify="center", insertwidth=0, insertontime=0)
        entry.bind("<Key>",        lambda e: e.widget.select_range(0, tk.END))
        entry.bind("<FocusIn>",    lambda e: entry.config(bg="#f0f0f0"))
        entry.bind("<FocusOut>",   lambda e: entry.config(bg="white"))
        entry.bind("<KeyRelease>", lambda e: (self.publicar("actualizar_diccionario")) if self.publicar else None)
        entry.grid(row=fila, column=1, sticky="w", padx=padx)
        entry.config(validate="none")
        entry.insert(0, valor_inicial)
        entry.config(validate="key")
        return entry

    def _validar_y_colorear(self, P, W):
        # Valida el afijo y colorea el entry si es inválido
        if not self._validar_afijo(P):
            widget = self.ventana_opciones.nametowidget(W)
            widget.config(bg="red", fg="white")
            self.ventana_opciones.after(500, lambda: widget.config(bg="#f0f0f0", fg="black"))
            return False
        return True
    
    def mostrar_tecla_invalida(self):
        self.frame_atajo_deshacer.config(bg="red")
        self.etiqueta_deshacer.config(bg="red")
        self.ventana_opciones.after(500, lambda: (
            self.frame_atajo_deshacer.config(bg="yellow"),
            self.etiqueta_deshacer.config(bg="yellow")
        ))

    
    def mostrar_atajo_prohibido(self, tipo):
        # Muestra el cuadro rojo con mensaje de combinación prohibida
        # Después de 1 segundo vuelve al estado de captura
        if tipo == "windows" or tipo == "comun":
            mensaje = self.config.textos[self.config.idioma]["interfaz"]["atajo_prohibido_windows"]
        else:
            mensaje = self.config.textos[self.config.idioma]["interfaz"]["atajo_prohibido_linux"]

        # Cuadro rojo con texto blanco
        self.frame_atajo_captura.config(bg="red")
        self.etiqueta_atajo.config(text=mensaje, bg="red", fg="white")

        # Después de 1 segundo vuelve al estado de captura
        self.ventana_opciones.after(1000, self._restaurar_captura)

    def _restaurar_captura(self):
        # Vuelve al estado de captura normal
        self.frame_atajo_captura.config(bg="yellow")
        self.etiqueta_atajo.config(
            text=self.config.textos[self.config.idioma]["interfaz"]["presione_atajo"],
            bg="yellow",
            fg="black"
        )