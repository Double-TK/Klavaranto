########################################################
##                   ACERCA.PY                        ##
##   Ventana "Acerca de" del programa.                ##
##   No se modifica salvo cambios visuales.           ##
########################################################

import tkinter as tk
import webbrowser
import os
import sys
from PIL import ImageTk
from build_info import COMPILADOR, PYTHON


##############################################################
##              CLASE ACERCA DE                             ##
##############################################################

class AcercaDe:

    def __init__(self, config, imagenes, publicar, nombre, version, autor, caracteres,
                 link_web, link_issues, link_sponsor, link_licencia):
        self.config   = config      # Para textos traducidos
        self.imagenes = imagenes    # Para el ícono grande
        self.publicar = publicar    # Para el botón "Opciones"

        # Datos del programa — vienen de klavaranto.py
        self.nombre       = nombre
        self.version      = version
        self.autor        = autor
        self.caracteres   = caracteres
        self.link_web     = link_web
        self.link_issues  = link_issues
        self.link_sponsor = link_sponsor
        self.link_licencia = link_licencia

        # Crea la ventana
        self.ventana = None
        self._crear_ventana()


    ##############################################################
    ##              CREACIÓN DE LA VENTANA                      ##
    ##############################################################

    def _crear_ventana(self):
        t = self.config.textos[self.config.idioma]["interfaz"]


        # Configuración de la ventana
        self.ventana = tk.Toplevel()
        self.ventana.title(self.config.textos[self.config.idioma]["sistema"]["menu_acerca"])
        self.ventana.withdraw()
        self.ventana.protocol("WM_DELETE_WINDOW", self.ventana.withdraw)
        self.ventana.resizable(False, False)

        # Centrar en pantalla
        ancho, alto = 378, 410
        x = (self.ventana.winfo_screenwidth()  // 2) - (ancho // 2)
        y = (self.ventana.winfo_screenheight() // 2) - (alto  // 2)
        self.ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

        # Fuente del título — Protest Riot en Windows, Arial en Linux
        if os.name == 'nt':
            import ctypes
            ruta_base   = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
            ruta_fuente = os.path.join(ruta_base, "ProtestRiot-Limpia.ttf")
            ctypes.windll.gdi32.AddFontResourceW(ruta_fuente)
            fuente_titulo = ("Protest Riot Light", 32)
        else:
            fuente_titulo = ("Arial", 32)

        # -- ENCABEZADO --
        frame_top = tk.Frame(self.ventana)
        frame_top.pack(fill="x", padx=10, pady=10)

        frame_texto = tk.Frame(frame_top)
        frame_texto.pack(side="left", fill="both", expand=True)

        tk.Label(frame_texto, text=self.nombre, font=fuente_titulo, fg="#009000").pack(anchor="center")

        frame_version = tk.Frame(frame_texto)
        frame_version.pack(anchor="center")
        tk.Label(frame_version, text=t["version"]).grid(row=0, column=0)
        tk.Label(frame_version, text=self.version).grid(row=0, column=1)

        frame_autor = tk.Frame(frame_texto)
        frame_autor.pack(anchor="center")
        tk.Label(frame_autor, text=t["autor"]).grid(row=0, column=0)
        tk.Label(frame_autor, text=self.autor).grid(row=0, column=1)

        # Ícono grande
        frame_icono = tk.Frame(frame_top, relief="groove", borderwidth=2)
        frame_icono.pack(side="right", anchor="center")
        self._icono_grande_ref = ImageTk.PhotoImage(self.imagenes.imagen_icono_grande)
        tk.Label(frame_icono, image=self._icono_grande_ref).pack(padx=5, pady=5)

        # -- DESCRIPCIÓN --
        tk.Label(self.ventana, text=t["descripcion"]).pack(pady=5)
        tk.Label(self.ventana, text=self.caracteres).pack()

        # -- LINKS --
        frame_links = tk.Frame(self.ventana)
        frame_links.pack(pady=(15, 5))

        for fila, (clave, url) in enumerate([
            ("pagina_web",     self.link_web),
            ("reportar_error", self.link_issues),
            ("sponsor",        self.link_sponsor)
        ]):
            tk.Label(frame_links, text=t[clave]).grid(row=fila, column=0, sticky="e")
            link = tk.Label(frame_links, text=url, fg="blue", cursor="hand2")
            link.grid(row=fila, column=1, sticky="w")
            link.bind("<Button-1>", lambda e, u=url: webbrowser.open(u))

        # -- LICENCIA --
        frame_licencia = tk.Frame(self.ventana)
        frame_licencia.pack(pady=(15, 0))
        tk.Label(frame_licencia, text=" © 2026 GAB. Klavaranto is free software:",
                 font=("Segoe UI", 7), fg="gray").pack(side="left")
                       
        link_lic = tk.Label(frame_licencia, text="GNU GPL v3",
                 font=("Segoe UI", 7), fg="blue", cursor="hand2")
        link_lic.pack(side="left")
        link_lic.bind("<Button-1>", lambda e: webbrowser.open(self.link_licencia))
        

        # -- BOTONES --
        frame_botones = tk.Frame(self.ventana)
        frame_botones.pack(fill="x", padx=10, pady=10, side="bottom")

        tk.Button(frame_botones, text=self.config.textos[self.config.idioma]["sistema"]["menu_opciones"],
                  command=lambda: self.publicar("abrir_opciones")).pack(side="left")
        tk.Button(frame_botones, text=t["cerrar"],
                  command=self.ventana.withdraw).pack(side="right")

        # -- PIE --
        tk.Label(self.ventana, text="Uses pynput and pystray under LGPL license",
                 font=("Segoe UI", 7), fg="gray").pack()
        tk.Label(self.ventana, text="Font Protest Riot © Octavio Pardo, SIL OFL",
                 font=("Segoe UI", 7), fg="gray").pack()
        tk.Label(self.ventana, text=f"Built with {COMPILADOR} / Python {PYTHON}",
                 font=("Segoe UI", 7), fg="gray").pack()
        
        
        
        