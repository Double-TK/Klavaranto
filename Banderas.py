from PIL import Image, ImageDraw
import math

# --- CONFIGURACIÓN DE TAMAÑOS ---
# Alto base para el supermuestreo (antialiasing)
ALTO_BASE_HD = 256
# Alto base para el tamaño final en tu aplicación
ALTO_BASE_APP = 64
# Proporción fija 3:2 para que todos los iconos midan lo mismo (96x64 px)
RATIO_UNIFICADO = 3/2


def crear_bandera_unificada(dibujar_funcion, nombre_archivo):
    """
    Función principal constructora. 
    Dibuja en alta resolución y encoge con filtro Lanczos para bordes perfectos.
    """
    ancho_hd = int(ALTO_BASE_HD * RATIO_UNIFICADO)  # 384 px
    alto_hd = ALTO_BASE_HD                          # 256 px
    
    ancho_app = int(ALTO_BASE_APP * RATIO_UNIFICADO) # 96 px
    alto_app = ALTO_BASE_APP                         # 64 px
    
    # Crear lienzo HD transparente
    img_hd = Image.new("RGBA", (ancho_hd, alto_hd), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img_hd)
    
    # Ejecutar el dibujo de la bandera seleccionada
    dibujar_funcion(draw, ancho_hd, alto_hd)
    
    # Reducir con filtro Lanczos para eliminar el pixelado
    bandera_final = img_hd.resize((ancho_app, alto_app), Image.Resampling.LANCZOS)
    bandera_final.save(nombre_archivo)
    print(f"¡Bandera generada con éxito!: {nombre_archivo} ({ancho_app}x{alto_app}px)")


# --- 1. BANDERA DE ESPAÑA (Escudo Detallado) ---
def dibujar_espana_detallada(draw, ancho, alto):
    alto_franja = alto // 4
    
    # Franjas rojas y amarilla de fondo
    draw.rectangle([0, 0, ancho, alto_franja], fill="#AA151B")
    draw.rectangle([0, alto_franja, ancho, alto_franja * 3], fill="#F1BF00")
    draw.rectangle([0, alto_franja * 3, ancho, alto], fill="#AA151B")
    
    # Coordenadas base del escudo (centrado en el tercio izquierdo)
    x_centro = ancho // 3
    y_centro = alto // 2
    w_escudo = 24  
    h_escudo = 32  
    
    # Cuerpo del escudo (Fondo rojo)
    draw.rectangle([x_centro - w_escudo, y_centro - h_escudo, x_centro + w_escudo, y_centro + h_escudo], fill="#A60D12")
    
    # Cuarteles cruzados amarillos (Aragón / León)
    draw.rectangle([x_centro, y_centro - h_escudo, x_centro + w_escudo, y_centro], fill="#F1BF00")
    draw.rectangle([x_centro - w_escudo, y_centro, x_centro, y_centro + h_escudo], fill="#F1BF00")
    
    # Barras de Aragón (líneas rojas)
    draw.line([x_centro + 8, y_centro - h_escudo, x_centro + 8, y_centro], fill="#A60D12", width=3)
    draw.line([x_centro + 16, y_centro - h_escudo, x_centro + 16, y_centro], fill="#A60D12", width=3)
    
    # Castillo de Castilla (cuadrado amarillo)
    draw.rectangle([x_centro - 16, y_centro - 24, x_centro - 8, y_centro - 8], fill="#F1BF00")
    
    # Óvalo central azul (Borbón-Anjou)
    draw.ellipse([x_centro - 5, y_centro - 6, x_centro + 5, y_centro + 6], fill="#0033A0")
    
    # Silueta exterior y divisiones de los cuarteles
    draw.rectangle([x_centro - w_escudo, y_centro - h_escudo, x_centro + w_escudo, y_centro + h_escudo], outline="#000000", width=2)
    draw.line([x_centro - w_escudo, y_centro, x_centro + w_escudo, y_centro], fill="#000000", width=1)
    draw.line([x_centro, y_centro - h_escudo, x_centro, y_centro + h_escudo], fill="#000000", width=1)

    # Columnas de Hércules (A los lados del escudo)
    ancho_columna = 4
    separacion_columnas = 36
    
    # Columna Izquierda
    x_col_izq = x_centro - separacion_columnas
    draw.rectangle([x_col_izq, y_centro - 18, x_col_izq + ancho_columna, y_centro + 18], fill="#FFFFFF") 
    draw.rectangle([x_col_izq - 2, y_centro - 22, x_col_izq + ancho_columna + 2, y_centro - 18], fill="#F1BF00") 
    draw.rectangle([x_col_izq - 2, y_centro + 18, x_col_izq + ancho_columna + 2, y_centro + 22], fill="#FFFFFF") 
    
    # Columna Derecha
    x_col_der = x_centro + separacion_columnas - ancho_columna
    draw.rectangle([x_col_der, y_centro - 18, x_col_der + ancho_columna, y_centro + 18], fill="#FFFFFF") 
    draw.rectangle([x_col_der - 2, y_centro - 22, x_col_der + ancho_columna + 2, y_centro - 18], fill="#F1BF00") 
    draw.rectangle([x_col_der - 2, y_centro + 18, x_col_der + ancho_columna + 2, y_centro + 22], fill="#FFFFFF")

    # Corona Real Superior
    y_corona_base = y_centro - h_escudo - 3
    draw.rectangle([x_centro - 18, y_corona_base - 6, x_centro + 18, y_corona_base], fill="#A60D12")
    draw.rectangle([x_centro - 18, y_corona_base - 6, x_centro + 18, y_corona_base], outline="#F1BF00", width=2)
    
    puntos_corona = [
        (x_centro - 18, y_corona_base - 6),
        (x_centro - 12, y_corona_base - 14), 
        (x_centro - 6, y_corona_base - 6),
        (x_centro, y_corona_base - 18),     
        (x_centro + 6, y_corona_base - 6),
        (x_centro + 12, y_corona_base - 14), 
        (x_centro + 18, y_corona_base - 6)
    ]
    draw.polygon(puntos_corona, fill="#F1BF00")
    draw.ellipse([x_centro - 2, y_corona_base - 22, x_centro + 2, y_corona_base - 18], fill="#F1BF00")


# --- 2. BANDERA DEL REINO UNIDO (Adaptada a 3:2) ---
def dibujar_reino_unido(draw, ancho, alto):
    # Fondo azul oscuro
    draw.rectangle([0, 0, ancho, alto], fill="#012169")
    
    # Diagonales blancas
    ancho_diagonal_blanca = ancho // 13
    draw.line([0, 0, ancho, alto], fill="#FFFFFF", width=ancho_diagonal_blanca)
    draw.line([0, alto, ancho, 0], fill="#FFFFFF", width=ancho_diagonal_blanca)
    
    # Diagonales rojas
    ancho_diagonal_roja = ancho // 22
    draw.line([0, 0, ancho, alto], fill="#C8102E", width=ancho_diagonal_roja)
    draw.line([0, alto, ancho, 0], fill="#C8102E", width=ancho_diagonal_roja)
    
    # Cruz blanca central
    ancho_cruz_blanca = ancho // 5
    draw.rectangle([0, (alto - ancho_cruz_blanca)//2, ancho, (alto + ancho_cruz_blanca)//2], fill="#FFFFFF")
    draw.rectangle([(ancho - ancho_cruz_blanca)//2, 0, (ancho + ancho_cruz_blanca)//2, alto], fill="#FFFFFF")
    
    # Cruz roja central
    ancho_cruz_roja = ancho // 8
    draw.rectangle([0, (alto - ancho_cruz_roja)//2, ancho, (alto + ancho_cruz_roja)//2], fill="#C8102E")
    draw.rectangle([(ancho - ancho_cruz_roja)//2, 0, (ancho + ancho_cruz_roja)//2, alto], fill="#C8102E")


# --- 3. BANDERA DE ESPERANTO (Optimizada e Icono Grande) ---
def dibujar_esperanto_grande(draw, ancho, alto):
    # Fondo verde
    draw.rectangle([0, 0, ancho, alto], fill="#009933")
    
    # Cantón blanco ampliado al 60% de la altura (Cuadrado perfecto)
    tam_canton = int(alto * 0.5) 
    draw.rectangle([0, 0, tam_canton, tam_canton], fill="#FFFFFF")
    
    # Verda Stelo centrada y ampliada
    cx, cy = tam_canton // 2, tam_canton // 2
    r_exterior = int(tam_canton * 0.42)  
    r_interior = int(tam_canton * 0.18)  
    
    puntos_estrella = []
    for i in range(10):
        angulo = i * math.pi / 5 - math.pi / 2
        r = r_exterior if i % 2 == 0 else r_interior
        x = cx + r * math.cos(angulo)
        y = cy + r * math.sin(angulo)
        puntos_estrella.append((x, y))
        
    draw.polygon(puntos_estrella, fill="#009933")


# --- EJECUCIÓN PRINCIPAL ---
if __name__ == "__main__":
    print("Iniciando generación de banderas para la aplicación...")
    print("-" * 50)
    crear_bandera_unificada(dibujar_espana_detallada, "app_idioma_es.png")
    crear_bandera_unificada(dibujar_reino_unido, "app_idioma_en.png")
    crear_bandera_unificada(dibujar_esperanto_grande, "app_idioma_eo.png")
    print("-" * 50)
    print("¡Todo listo! Revisa tu carpeta de proyecto.")