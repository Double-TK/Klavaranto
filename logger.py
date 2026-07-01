########################################################
##                    LOGGER.PY                       ##
##   Sistema de registro de eventos del programa      ##
##   Se importa directamente desde cualquier archivo  ##
##   Config lo configura al arrancar                  ##
########################################################

import logging


##############################################################
##              LOGGERS DISPONIBLES                         ##
##                                                          ##
##   log_sistema    — arranque, activar, desactivar, atajo  ##
##   log_reemplazos — cada reemplazo de letra               ##
##   log_errores    — excepciones y errores                 ##
##   log_atajo      — detección del hotkey de activación    ##
##############################################################

log_sistema    = logging.getLogger("sistema")
log_reemplazos = logging.getLogger("reemplazos")
log_errores    = logging.getLogger("errores")
log_atajo      = logging.getLogger("atajo")

# Por defecto todos usan NullHandler — no escriben nada
# Config los activa al arrancar según config.ini
for _log in [log_sistema, log_reemplazos, log_errores, log_atajo]:
    _log.addHandler(logging.NullHandler())


##############################################################
##              CONFIGURACIÓN                               ##
##   Llamado una sola vez desde Config al arrancar          ##
##############################################################

def configurar(ruta_archivo, sistema=0, reemplazos=0, errores=1, atajo=0):
    # Formato de cada línea del log: hora [categoria] mensaje
    formato = logging.Formatter('%(asctime)s [%(name)s] %(message)s', datefmt='%H:%M:%S')

    def activar(logger, activo):
        # Si activo=1, conecta el logger al archivo. Si no, no hace nada.
        if activo:
            handler = logging.FileHandler(ruta_archivo, encoding="utf-8", delay=True)
            handler.setFormatter(formato)
            logger.addHandler(handler)
            logger.setLevel(logging.DEBUG)

    activar(log_sistema,    sistema)
    activar(log_reemplazos, reemplazos)
    activar(log_errores,    errores)
    activar(log_atajo,      atajo)
    

    log_sistema.debug("=== PROGRAMA INICIADO ===")