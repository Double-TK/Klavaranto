########################################################
##                   IMAGENES.PY                      ##
##   Genera todos los íconos y banderas del programa  ##
##   desde código — sin archivos externos             ##
########################################################

from PIL import Image, ImageDraw
import math
import os


##############################################################
##              CONFIGURACIÓN DE EXPORTACIÓN               ##
##   0 = no exportar                                        ##
##   1 = exportar como PNG                                  ##
##   2 = exportar como ICO                                  ##
##   3 = exportar como PNG e ICO                            ##
##   Si el archivo ya existe, agrega un número al nombre    ##
##############################################################

EXPORTAR_ICONO_VERDE   = 0
EXPORTAR_ICONO_ROJO    = 0
EXPORTAR_ICONO_GRANDE  = 0
EXPORTAR_BANDERA_ES    = 0
EXPORTAR_BANDERA_EN    = 0
EXPORTAR_BANDERA_EO    = 0


##############################################################
##              CONFIGURACIÓN DE TAMAÑOS                    ##
##############################################################

TAMAÑO_ICONO_NORMAL = 64     # Tamaño del ícono en bandeja
TAMAÑO_ICONO_GRANDE = 100    # Tamaño del ícono en ventana Acerca de
TAMAÑO_ICONO_HD     = 512    # Tamaño interno de dibujo — se reduce con Lanczos

ALTO_BANDERA_HD  = 256       # Alto interno de dibujo para banderas
ALTO_BANDERA_APP = 16        # Alto final de las banderas en la interfaz
RATIO_BANDERA    = 3 / 2     # Proporción ancho:alto de las banderas


##############################################################
##              CLASE IMAGENES                              ##
##############################################################

class Imagenes:

    def __init__(self):
        # Genera todas las imágenes en memoria al arrancar
        self.imagen_icono_activado   = self._crear_icono('#009000', tamaño=TAMAÑO_ICONO_NORMAL)
        self.imagen_icono_desactivado = self._crear_icono('#900000', tamaño=TAMAÑO_ICONO_NORMAL)
        self.imagen_icono_grande     = self._crear_icono('#009000', tamaño=TAMAÑO_ICONO_GRANDE)

        self.imagen_bandera_es = self._crear_bandera(self._dibujar_espana)
        self.imagen_bandera_en = self._crear_bandera(self._dibujar_reino_unido)
        self.imagen_bandera_eo = self._crear_bandera(self._dibujar_esperanto)

        # Exportar si está configurado
        if EXPORTAR_ICONO_VERDE:
            self._exportar(self.imagen_icono_activado,    "icono_verde",   EXPORTAR_ICONO_VERDE)
        if EXPORTAR_ICONO_ROJO:
            self._exportar(self.imagen_icono_desactivado, "icono_rojo",    EXPORTAR_ICONO_ROJO)
        if EXPORTAR_ICONO_GRANDE:
            self._exportar(self.imagen_icono_grande,      "icono_grande",  EXPORTAR_ICONO_GRANDE)
        if EXPORTAR_BANDERA_ES:
            self._exportar(self.imagen_bandera_es,        "app_idioma_es", EXPORTAR_BANDERA_ES)
        if EXPORTAR_BANDERA_EN:
            self._exportar(self.imagen_bandera_en,        "app_idioma_en", EXPORTAR_BANDERA_EN)
        if EXPORTAR_BANDERA_EO:
            self._exportar(self.imagen_bandera_eo,        "app_idioma_eo", EXPORTAR_BANDERA_EO)


    ##############################################################
    ##              EXPORTACIÓN                                 ##
    ##############################################################

    def _exportar(self, imagen, nombre_base, modo):
        # Genera nombre único si el archivo ya existe
        def nombre_unico(ruta):
            if not os.path.exists(ruta):
                return ruta
            base, ext = os.path.splitext(ruta)
            contador = 2
            while os.path.exists(f"{base}_{contador}{ext}"):
                contador += 1
            return f"{base}_{contador}{ext}"

        if modo == 1 or modo == 3:
            ruta = nombre_unico(f"{nombre_base}.png")
            imagen.save(ruta)
            print(f"Exportado: {ruta}")

        if modo == 2 or modo == 3:
            ruta = nombre_unico(f"{nombre_base}.ico")
            imagen.save(ruta, format="ICO")
            print(f"Exportado: {ruta}")


    ##############################################################
    ##              ÍCONOS DEL PROGRAMA                         ##
    ##############################################################

    def _crear_icono(self, color_hex, tamaño=64):
        # Dibuja en HD y reduce con Lanczos para mejor calidad
        escala_hd = TAMAÑO_ICONO_HD / 64
        img_hd = Image.new('RGBA', (TAMAÑO_ICONO_HD, TAMAÑO_ICONO_HD), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img_hd)

        hexagono = [(int(x * escala_hd), int(y * escala_hd)) for x, y in
                    [(16, 4), (48, 4), (64, 32), (48, 60), (16, 60), (0, 32)]]
        estrella_outline = [(int(x * escala_hd), int(y * escala_hd)) for x, y in
                            [(32, 8), (38, 23), (52, 23), (42, 32), (46, 48),
                             (32, 39), (18, 48), (22, 32), (12, 23), (26, 23)]]
        estrella = [(int(x * escala_hd), int(y * escala_hd)) for x, y in
                    [(32, 15), (36, 27), (47, 27), (39, 34), (42, 46),
                     (32, 39), (22, 46), (25, 34), (17, 27), (28, 27)]]

        draw.polygon(hexagono, fill=color_hex)
        draw.polygon(estrella_outline, fill='black')
        draw.polygon(estrella, fill='white')

        return img_hd.resize((tamaño, tamaño), Image.Resampling.LANCZOS)


    ##############################################################
    ##              BANDERAS                                    ##
    ##############################################################

    def _crear_bandera(self, dibujar_funcion):
        # Dibuja en HD y reduce con Lanczos para mejor calidad
        ancho_hd  = int(ALTO_BANDERA_HD * RATIO_BANDERA)
        ancho_app = int(ALTO_BANDERA_APP * RATIO_BANDERA)

        img_hd = Image.new("RGBA", (ancho_hd, ALTO_BANDERA_HD), (0, 0, 0, 0))
        draw   = ImageDraw.Draw(img_hd)
        dibujar_funcion(draw, ancho_hd, ALTO_BANDERA_HD)

        return img_hd.resize((ancho_app, ALTO_BANDERA_APP), Image.Resampling.LANCZOS)


    def _dibujar_espana(self, draw, ancho, alto):
        franja = alto // 4
        draw.rectangle([0, 0,          ancho, franja],      fill="#AA151B")
        draw.rectangle([0, franja,     ancho, franja * 3],  fill="#F1BF00")
        draw.rectangle([0, franja * 3, ancho, alto],        fill="#AA151B")

        cx, cy = ancho // 3, alto // 2
        w, h   = 24, 32

        draw.rectangle([cx - w, cy - h, cx + w, cy + h], fill="#A60D12")
        draw.rectangle([cx,     cy - h, cx + w, cy],     fill="#F1BF00")
        draw.rectangle([cx - w, cy,     cx,     cy + h], fill="#F1BF00")
        draw.rectangle([cx - w, cy - h, cx + w, cy + h], outline="#000000", width=2)
        draw.line([cx - w, cy, cx + w, cy], fill="#000000", width=1)
        draw.line([cx, cy - h, cx, cy + h], fill="#000000", width=1)

        y_corona = cy - h - 3
        puntos_corona = [
            (cx - 18, y_corona - 6), (cx - 12, y_corona - 14),
            (cx - 6,  y_corona - 6), (cx,      y_corona - 18),
            (cx + 6,  y_corona - 6), (cx + 12, y_corona - 14),
            (cx + 18, y_corona - 6)
        ]
        draw.polygon(puntos_corona, fill="#F1BF00")


    def _dibujar_reino_unido(self, draw, ancho, alto):
        draw.rectangle([0, 0, ancho, alto], fill="#012169")

        ancho_blanca = ancho // 13
        ancho_roja   = ancho // 22
        draw.line([0, 0,    ancho, alto], fill="#FFFFFF", width=ancho_blanca)
        draw.line([0, alto, ancho, 0],    fill="#FFFFFF", width=ancho_blanca)
        draw.line([0, 0,    ancho, alto], fill="#C8102E", width=ancho_roja)
        draw.line([0, alto, ancho, 0],    fill="#C8102E", width=ancho_roja)

        ancho_cruz_blanca = ancho // 5
        ancho_cruz_roja   = ancho // 8
        draw.rectangle([0, (alto - ancho_cruz_blanca) // 2, ancho, (alto + ancho_cruz_blanca) // 2], fill="#FFFFFF")
        draw.rectangle([(ancho - ancho_cruz_blanca) // 2, 0, (ancho + ancho_cruz_blanca) // 2, alto], fill="#FFFFFF")
        draw.rectangle([0, (alto - ancho_cruz_roja) // 2,   ancho, (alto + ancho_cruz_roja) // 2],   fill="#C8102E")
        draw.rectangle([(ancho - ancho_cruz_roja) // 2, 0,  (ancho + ancho_cruz_roja) // 2, alto],   fill="#C8102E")


    def _dibujar_esperanto(self, draw, ancho, alto):
        draw.rectangle([0, 0, ancho, alto], fill="#009933")

        tam = int(alto * 0.5)
        draw.rectangle([0, 0, tam, tam], fill="#FFFFFF")

        cx, cy     = tam // 2, tam // 2
        r_exterior = int(tam * 0.42)
        r_interior = int(tam * 0.18)

        puntos = []
        for i in range(10):
            angulo = i * math.pi / 5 - math.pi / 2
            r = r_exterior if i % 2 == 0 else r_interior
            puntos.append((cx + r * math.cos(angulo), cy + r * math.sin(angulo)))

        draw.polygon(puntos, fill="#009933")