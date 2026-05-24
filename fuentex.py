import os
import subprocess
import sys

def recortar_y_renombrar_fuente():
    fuente_original = "ProtestRiot-Regular.ttf"
    fuente_salida = "ProtestRiot-Limpia.ttf"
    # Solo las letras únicas necesarias
    letras_necesarias = "Klavrnto" 

    # 1. Verificar e instalar fonttools si falta
    try:
        import fontTools
    except ImportError:
        print("Instalando 'fonttools' automáticamente...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "fonttools"])

    # 2. Verificar existencia del archivo original
    if not os.path.exists(fuente_original):
        print(f"Error: No encuentro '{fuente_original}'.")
        return

    print(f"Vaciando y destruyendo todo excepto las letras de: {letras_necesarias}")
    
    # 3. Argumentos extremos para destruir todo lo demás
    argumentos = [
        fuente_original,
        f"--text={letras_necesarias}",
        f"--output-file={fuente_salida}",
        "--no-hinting",                 # Borra instrucciones de renderizado antiguo
        "--layout-features=",           # Borra absolutamente todas las reglas de OpenType/Layout
        "--desubroutinize",             # Limpia datos internos duplicados
        "--no-glyph-names"              # Borra los nombres de texto de las letras (ahorra bytes)
    ]
    
    from fontTools import subset
    from fontTools.ttLib import TTFont
    
    sys.argv = ["pyftsubset"] + argumentos
    
    try:
        # Ejecuta el recorte extremo
        subset.main()
        
        print("Cambiando el nombre interno de la fuente a 'Protest Riot Light'...")
        # 4. Abrimos la fuente recién creada para cambiarle los metadatos de nombre
        font = TTFont(fuente_salida)
        name_table = font['name']

        # Definimos los nuevos registros de identidad
        nuevos_nombres = {
            1: "Protest Riot Light",    # Family Name
            2: "Regular",               # Al ser una familia nueva, su estilo base es Regular
            4: "Protest Riot Light",    # Full Font Name
            6: "ProtestRiot-Light",     # PostScript Name
            16: "Protest Riot Light"    # ¡CLAVE! Cambiamos la familia tipográfica para separarla de la original
        }

        # Sobrescribimos la tabla interna de nombres usando 'nameID' (con I mayúscula)
        for record in name_table.names:
            if record.nameID in nuevos_nombres:
                nuevo_texto = nuevos_nombres[record.nameID]
                try:
                    encoding = record.getEncoding()
                    record.string = nuevo_texto.encode(encoding)
                except Exception:
                    try:
                        record.string = nuevo_texto.encode('utf-16-be')
                    except Exception:
                        record.string = nuevo_texto.encode('utf-8')

        # Guardamos los cambios de nombre en el mismo archivo de salida
        font.save(fuente_salida)
        
        # 5. Calcular cuánto espacio ahorramos
        peso_original = os.path.getsize(fuente_original) / 1024
        peso_final = os.path.getsize(fuente_salida) / 1024
        
        print("-" * 50)
        print("¡OPERACIÓN DE RECORTE Y RENOMBRADO COMPLETADA!")
        print(f"Peso original: {peso_original:.2f} KB")
        print(f"Peso final:    {peso_final:.2f} KB")
        print(f"Reducción del: {((peso_original - peso_final) / peso_original) * 100:.1f}%")
        print(f"Archivo guardado como: '{fuente_salida}'")
        print("-" * 50)
        
    except Exception as e:
        print(f"Ocurrió un error en el proceso: {e}")

if __name__ == "__main__":
    recortar_y_renombrar_fuente()