########################################################
##                    CONFIG.PY                       ##
##   Maneja la configuración del programa y los       ##
##   textos traducidos de la interfaz                 ##
########################################################

import configparser
import os
import sys
import json
import logger


##############################################################
##              CLASE CONFIG                                ##
##############################################################

class Config:

    # Valores por defecto — se usan si no existe config.ini
    CONFIG_DEFECTO = {
        'general': {
            'margen': '3',
            'idioma': 'es',
        },
        'inicio': {
            'iniciar_activado': '0',
            'iniciar_con_windows': '0',
        },
        'atajo': {
            'atajo': 'none',
        },
        'entrada': {
            'afijo': '2',
            'sufijo': 'x',
            'prefijo': '',
        },
        'deshacer': {
            'deshacer_cambio': '0',
            'atajo_deshacer': 'none',
            'deshacer_tecla': '0',
        },
        'dev': {
            'log_sistema':    '0',
            'log_reemplazos': '0',
            'log_errores':    '1',
            'log_atajo':      '0',
            'instancia_unica': '1',
        }
    }

    def __init__(self):

        # Determina la carpeta donde está el .exe (o el .py si corre sin compilar)
        
        ruta_exe = os.path.dirname(os.path.abspath(sys.argv[0]))

        # Decide dónde guardar el config.ini
        # Si está en Program Files → AppData (instalado)
        # Si no → junto al ejecutable (portable)
        
        if "Program Files" in ruta_exe:
            self.ruta_config = os.path.join(os.environ["APPDATA"], "Klavaranto")
            os.makedirs(self.ruta_config, exist_ok=True)
        else:
            self.ruta_config = ruta_exe

        # Rutas de archivos importantes
        self.ruta_base    = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))  # Recursos como idiomas.json
        self.config_file  = os.path.join(self.ruta_config, "config.ini")
        self.log_file     = os.path.join(self.ruta_config, "klavaranto_log.txt")

        # Crea el objeto que lee y escribe el config.ini
        self.cfg = configparser.ConfigParser()
        self.cfg.read_dict(self.CONFIG_DEFECTO)         # Carga valores por defecto
        if os.path.exists(self.config_file):
            self.cfg.read(self.config_file, encoding="utf-8")  # Sobreescribe con los guardados
        self.guardar()                                  # Crea el archivo si no existía

        # Lee los valores a variables propias
        self.leer()

        # Configura los loggers según config.ini
        logger.configurar(
            ruta_archivo = self.log_file,
            sistema      = int(self.cfg['dev']['log_sistema']),
            reemplazos   = int(self.cfg['dev']['log_reemplazos']),
            errores      = int(self.cfg['dev']['log_errores']),
            atajo        = int(self.cfg['dev']['log_atajo'])
        )

        # Carga los textos traducidos desde idiomas.json
        ruta_json = os.path.join(self.ruta_base, "idiomas.json")
        with open(ruta_json, encoding="utf-8") as f:
            self.textos = json.load(f)

        # Construye el diccionario de nombres de teclas en el idioma activo
        self.construir_nombres_teclas()


    ##############################################################
    ##              LECTURA Y ESCRITURA                         ##
    ##############################################################

    def leer(self):
        # Lee todos los valores del config.ini a variables propias
        self.idioma          = self.cfg['general']['idioma']
        self.margen          = int(self.cfg['general']['margen'])
        self.activado = int(self.cfg['inicio']['iniciar_activado'])
        logger.log_sistema.debug(f"leer() activado={self.activado}")
        self.iniciar_windows = int(self.cfg['inicio']['iniciar_con_windows'])
        self.afijo           = self.cfg['entrada']['afijo']
        self.prefijo         = self.cfg['entrada']['prefijo']
        self.sufijo          = self.cfg['entrada']['sufijo']
        self.deshacer_cambio = int(self.cfg['deshacer']['deshacer_cambio'])
        self.deshacer_tecla  = int(self.cfg['deshacer']['deshacer_tecla'])
        self.atajo_deshacer  = self.cfg['deshacer']['atajo_deshacer']
        self.atajo           = self.cfg['atajo']['atajo']
        self.instancia_unica = int(self.cfg['dev']['instancia_unica'])
        self.en_prueba = False        


    def guardar(self):
        logger.log_sistema.debug(f"guardando: afijo={self.cfg['entrada']['afijo']}")
        activado_actual = getattr(self, 'activado', 0)
        
        # 1. Guardamos los nombres en variables limpias
        nombre_atajo    = self.cfg['atajo'].get('atajo_nombre', 'Sin atajo')
        nombre_deshacer = self.cfg['deshacer'].get('atajo_deshacer_nombre', 'Sin tecla')
        
        # 2. Borramos los datos temporales de la memoria
        if 'atajo_nombre' in self.cfg['atajo']:
            del self.cfg['atajo']['atajo_nombre']
        if 'atajo_deshacer_nombre' in self.cfg['deshacer']:
            del self.cfg['deshacer']['atajo_deshacer_nombre']
        
        # 3. Guardamos el archivo limpio
        with open(self.config_file, 'w', encoding="utf-8") as f:
            self.cfg.write(f)
        
        # 4. Leemos el archivo para poner los comentarios
        with open(self.config_file, 'r', encoding="utf-8") as f:
            contenido = f.read()
        
        # Comentario del atajo de activación
        contenido = contenido.replace('[atajo]', f'[atajo]\n# Su atajo actual es: {nombre_atajo}')
        
        # Comentario del atajo de deshacer
        contenido = contenido.replace('[deshacer]', f'[deshacer]\n# Su tecla de deshacer es: {nombre_deshacer}')
        
        with open(self.config_file, 'w', encoding="utf-8") as f:
            f.write(contenido)
        
        # 5. Reconstruimos la memoria
        self.leer()
        self.cfg['atajo']['atajo_nombre']             = nombre_atajo
        self.cfg['deshacer']['atajo_deshacer_nombre'] = nombre_deshacer
        
        if activado_actual >= 1:
            self.activado = activado_actual
            
        self.en_prueba = False


    ##############################################################
    ##              IDIOMAS Y TECLAS                            ##
    ##############################################################

    def construir_nombres_teclas(self):
        # Traduce los nombres de teclas especiales según el idioma activo
        # Ahora lee desde la sección "teclas" del JSON
        # Se llama al arrancar y cada vez que el usuario cambia de idioma
        self.nombres_teclas = self.textos[self.idioma]["teclas"]


    def cambiar_idioma(self, idioma_nuevo):
        # Cambia el idioma activo y reconstruye los nombres de teclas
        self.idioma = idioma_nuevo
        self.cfg['general']['idioma'] = idioma_nuevo
        self.construir_nombres_teclas()
        logger.log_sistema.debug(f"IDIOMA CAMBIADO: {idioma_nuevo}")
        

