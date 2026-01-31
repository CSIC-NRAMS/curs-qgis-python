# OBJECTIU:
#   Provar que utils/processing_utils.py es pot importar correctament.
#
# ENTRADA:
#   Cap fitxer; només comprovem que el mòdul és accessible.
#
# SORTIDA:
#   Cap fitxer; mostrem funcions disponibles.
#
# QUÈ APRENEM:
#   - Verificar que el mòdul existeix.
#   - Identificar funcions clau del helper.

import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

import utils.processing_utils as pu

print("OK -> processing_utils importat.")
print("Funcions disponibles:", [name for name in dir(pu) if name.endswith("_utils") is False and name.startswith("_") is False])
