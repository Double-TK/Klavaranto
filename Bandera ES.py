from PIL import Image, ImageDraw
import math

# Configuración de tamaños para el antialiasing
ALTO_BASE_HD = 256
ALTO_BASE_APP = 64
RATIO_UNIFICADO = 3/2

def crear_bandera_unificada(dibujar_funcion, nombre_archivo):
    ancho_hd = int(ALTO_BASE_HD * RATIO_UNIFICADO)  # 384 px
    alto_hd = ALTO_BASE_HD                          # 256 px
    
    ancho_app = int(ALTO_BASE_APP * RATIO_UNIFICADO) # 96 px
    alto_app = ALTO_BASE_APP                         # 64 px
    
    img_hd = Image.new("RGBA", (ancho_hd, alto_hd), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img_hd)
    
    dibujar_funcion(draw, ancho_hd, alto_hd)
    
    bandera_final = img_hd.resize((ancho_app, alto_app), Image.Resampling.LANCZOS)
    bandera_final.save(nombre_archivo)
    print(f"¡Bandera generada con éxito!: {nombre_archivo} ({ancho_app}x{alto_app}px)")

# --- BANDERA DE ESPAÑA CON ESCUDO DETALLADO ---
def dibujar_espana_detallada(draw, ancho, alto):
    alto_franja = alto // 4
    
    # 1. Franjas rojas y amarilla de fondo
    draw.rectangle([0, 0, ancho, alto_franja], fill="#AA151B")
    draw.rectangle([0, alto_franja, ancho, alto_franja * 3], fill="#F1BF00")
    draw.rectangle([0, alto_franja * 3, ancho, alto], fill="#AA151B")
    
    # 2. Coordenadas base del escudo (centrado en el tercio izquierdo)
    x_centro = ancho // 3
    y_centro = alto // 2
    
    # Dimensiones del cuerpo del escudo
    w_escudo = 24  # Mitad del ancho del escudo
    h_escudo = 32  # Mitad del alto del escudo
    
    # --- DIBUJO DEL ESCUDO (CUERPO) ---
    # Fondo rojo del escudo (Castilla / Navarra / bordes)
    draw.rectangle([x_centro - w_escudo, y_centro - h_escudo, x_centro + w_escudo, y_centro + h_escudo], fill="#A60D12")
    
    # Cuartel superior derecho / inferior izquierdo en amarillo (Aragón / León)
    draw.rectangle([x_centro, y_centro - h_escudo, x_centro + w_escudo, y_centro], fill="#F1BF00")
    draw.rectangle([x_centro - w_escudo, y_centro, x_centro, y_centro + h_escudo], fill="#F1BF00")
    
    # Detalles internos mínimos (barras de Aragón y León/Granada simplificados)
    # Barras rojas en el cuartel amarillo superior derecho
    draw.line([x_centro + 8, y_centro - h_escudo, x_centro + 8, y_centro], fill="#A60D12", width=3)
    draw.line([x_centro + 16, y_centro - h_escudo, x_centro + 16, y_centro], fill="#A60D12", width=3)
    # El castillo simplificado (un cuadro amarillo en el cuartel rojo superior izquierdo)
    draw.rectangle([x_centro - 16, y_centro - 24, x_centro - 8, y_centro - 8], fill="#F1BF00")
    
    # Óvalo central azul (Borbón-Anjou)
    draw.ellipse([x_centro - 5, y_centro - 6, x_centro + 5, y_centro + 6], fill="#0033A0")
    
    # Borde o silueta exterior del escudo para estilizarlo
    draw.rectangle([x_centro - w_escudo, y_centro - h_escudo, x_centro + w_escudo, y_centro + h_escudo], outline="#000000", width=2)
    # Línea de división de cuarteles
    draw.line([x_centro - w_escudo, y_centro, x_centro + w_escudo, y_centro], fill="#000000", width=1)
    draw.line([x_centro, y_centro - h_escudo, x_centro, y_centro + h_escudo], fill="#000000", width=1)

    # --- COLUMNAS DE HÉRCULES (A los lados) ---
    ancho_columna = 4
    alto_columna = 36
    separacion_columnas = 36
    
    # Columna Izquierda (Plata/Blanca)
    x_col_izq = x_centro - separacion_columnas
    draw.rectangle([x_col_izq, y_centro - 18, x_col_izq + ancho_columna, y_centro + 18], fill="#FFFFFF") # Base de columna
    draw.rectangle([x_col_izq - 2, y_centro - 22, x_col_izq + ancho_columna + 2, y_centro - 18], fill="#F1BF00") # Capital dorado
    draw.rectangle([x_col_izq - 2, y_centro + 18, x_col_izq + ancho_columna + 2, y_centro + 22], fill="#FFFFFF") # Base
    
    # Columna Derecha (Plata/Blanca)
    x_col_der = x_centro + separacion_columnas - ancho_columna
    draw.rectangle([x_col_der, y_centro - 18, x_col_der + ancho_columna, y_centro + 18], fill="#FFFFFF") 
    draw.rectangle([x_col_der - 2, y_centro - 22, x_col_der + ancho_columna + 2, y_centro - 18], fill="#F1BF00") 
    draw.rectangle([x_col_der - 2, y_centro + 18, x_col_der + ancho_columna + 2, y_centro + 22], fill="#FFFFFF")

    # --- CORONA REAL (Superior) ---
    y_corona_base = y_centro - h_escudo - 3
    
    # Base de la corona (rectángulo rojo con borde dorado)
    draw.rectangle([x_centro - 18, y_corona_base - 6, x_centro + 18, y_corona_base], fill="#A60D12")
    draw.rectangle([x_centro - 18, y_corona_base - 6, x_centro + 18, y_corona_base], outline="#F1BF00", width=2)
    
    # Picos/Florones de la corona (puntas doradas)
    puntos_corona = [
        (x_centro - 18, y_corona_base - 6),
        (x_centro - 12, y_corona_base - 14), # Pico izquierdo
        (x_centro - 6, y_corona_base - 6),
        (x_centro, y_corona_base - 18),     # Pico central (más alto)
        (x_centro + 6, y_corona_base - 6),
        (x_centro + 12, y_corona_base - 14), # Pico derecho
        (x_centro + 18, y_corona_base - 6)
    ]
    draw.polygon(puntos_corona, fill="#F1BF00")
    
    # El pequeño orbe y cruz arriba del todo de la corona
    draw.ellipse([x_centro - 2, y_corona_base - 22, x_centro + 2, y_corona_base - 18], fill="#F1BF00")


if __name__ == "__main__":
    # Generamos la versión mejorada reemplazando la anterior
    crear_bandera_unificada(dibujar_espana_detallada, "app_idioma_es.png")