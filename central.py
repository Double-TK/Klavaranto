########################################################
##                   CENTRAL.PY                       ##
##   Núcleo inamovible del programa.                  ##
##   Solo contiene columna_vertebral.                 ##
##   No se modifica salvo causa mayor.                ##
########################################################

import logger


##############################################################
##              CLASE CENTRAL                               ##
##############################################################

class Central:

    def __init__(self, app, teclado):
        self.app     = app      # Conexión directa — activa/desactiva y detecta atajo
        self.teclado = teclado  # Conexión directa — procesa cada tecla


    def columna_vertebral(self, tecla):
        logger.log_sistema.debug(f"columna tecla={tecla} deshacer={self.teclado.buffer_deshacer} tipeo={[t.char for t in self.teclado.buffer_tipeo]}")
        # Árbitro principal — decide qué pasa con cada tecla presionada
        try:
            
            # Paso 0 — modo prueba: procesar directo, sin tocar activado ni atajo
            # Paso 0 — modo prueba
            if self.app.config.en_prueba:
                if self.app.detectar_atajo(tecla):
                    if self.app.config.activado == 1:
                        self.app.desactivar()
                    else:
                        self.app.activar()
                    return
                self.teclado.procesar(tecla)
                return

            # Paso 1 — si el programa está escribiendo solo, dejar pasar solo a verificar_deshacer
            # También deja pasar si está en modo captura (estado 4), aunque el programa esté desactivado
            if self.teclado.buffer_deshacer and self.teclado.buffer_deshacer[2] != 0:
                if self.app.config.activado >= 1 or self.teclado.buffer_deshacer[2] == 4:
                    self.teclado.procesar(tecla)
                return

            # Paso 2 — verificar si es el atajo de activación
            if self.app.detectar_atajo(tecla):
                if self.app.config.activado == 1:
                    self.app.desactivar()
                else:
                    self.app.activar()
                return

            # Paso 3 — si el programa está activo, pasarle la tecla a Teclado
            if self.app.config.activado >= 1:
                if self.teclado.procesar(tecla):
                    return False

        except Exception as e:
            logger.log_errores.debug(f"ERROR en columna_vertebral: {e}")