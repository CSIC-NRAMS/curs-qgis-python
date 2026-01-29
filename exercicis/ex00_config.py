# OBJECTIU:
#   Entendre la configuració centralitzada (rutes i fitxers).
#
# ENTRADA:
#   Cap fitxer; només llegim constants de configuració.
#
# SORTIDA:
#   Cap fitxer; mostrem informació per pantalla.
#
# QUÈ APRENEM:
#   - On es guarden les rutes del projecte.
#   - Per què és útil centralitzar la configuració.

import os  # Per gestionar rutes
import sys  # Per ajustar el path d'importació

# Afegim la carpeta arrel del projecte al sys.path
ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

# Importem configuració
from utils import config  # Mòdul amb totes les rutes

# Mostrem rutes clau
print("RUTA ARREL:", config.ROOT_DIR)
print("DADES_DIR:", config.DADES_DIR)
print("RESULTATS_DIR:", config.RESULTATS_DIR)
print("METEOCAT_INPUT:", config.METEOCAT_INPUT)
print("AEMET_INPUT:", config.AEMET_INPUT)

# Mostrem alguns outputs
print("STD_OUT (METEOCAT):", config.STD_OUT)
print("AEMET_STD_OUT:", config.AEMET_STD_OUT)
print("MERGED_STD_OUT:", config.MERGED_STD_OUT)
print("GPKG_OUT:", config.GPKG_OUT)

# Missatge final
print("OK -> Configuració carregada correctament.")
