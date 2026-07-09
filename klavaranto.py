########################################################
##                    MAIN.PY                         ##
##   Punto de entrada del programa.                   ##
##   Constantes, creación de clases y arranque.       ##
##   Este archivo casi nunca se modifica.             ##
########################################################

from config      import Config
from imagenes    import Imagenes
from teclado     import Teclado
from interfaz    import Interfaz
from acerca      import AcercaDe
from app         import App
from central     import Central
from telefonista import Telefonista

import logger


##############################################################
##              CONSTANTES DEL PROGRAMA                     ##
##   Datos que se reflejan en toda la interfaz              ##
##############################################################

NOMBRE       = "Klavaranto"
VERSION      = "1.1.2"
AUTOR        = "Gonzalo AB, Doble TK (Kroko)"
DESCRIPCION  = "Programa para escribir caracteres especiales del Esperanto"
CARACTERES   = "cx→ĉ  gx→ĝ  hx→ĥ  jx→ĵ  sx→ŝ  ux→ŭ"

LINK_WEB      = "https://github.com/Double-TK/Klavaranto"
LINK_ISSUES   = "https://github.com/Double-TK/Klavaranto/issues"
LINK_SPONSOR  = "https://ko-fi.com/doubletk"
LINK_LICENCIA = "https://www.gnu.org/licenses/gpl-3.0.html"


##############################################################
##              CREACIÓN DE CLASES                          ##
##   Orden importante — las independientes primero          ##
##############################################################


# 1. Las que no dependen de nadie
config   = Config()
imagenes = Imagenes()

# 2. Las que dependen solo de Config o Imagenes
teclado  = Teclado(config)
interfaz = Interfaz(config, imagenes)

# 3. App sin Central todavía — se conecta después
app = App(config, imagenes)

# 4. Central con App y Teclado
central = Central(app, teclado)

# 5. Conectar Central a App — resuelve la dependencia circular
app.central = central

# 6. Ventana Acerca de — recibe datos estáticos del programa
acerca = AcercaDe(
    config        = config,
    imagenes      = imagenes,
    publicar      = None,           # Telefonista la asigna al arrancar
    nombre        = NOMBRE,
    version       = VERSION,
    autor         = AUTOR,
    caracteres    = CARACTERES,
    link_web      = LINK_WEB,
    link_issues   = LINK_ISSUES,
    link_sponsor  = LINK_SPONSOR,
    link_licencia = LINK_LICENCIA
)

# 7. Telefonista — conecta todo y arma las suscripciones
logger.log_sistema.debug("antes de telefonista")
telefonista = Telefonista(config, teclado, interfaz, app, acerca)



##############################################################
##              ARRANQUE                                    ##
##############################################################

logger.log_sistema.debug("antes de iniciar")
app.iniciar()

logger.log_sistema.debug("antes de mainloop")
interfaz.ventana_opciones.mainloop()