# OBJECTIU:
#   Provar que utils/gui_utils.py es pot importar correctament.
#
# ENTRADA:
#   Cap fitxer; només comprovem que el mòdul és accessible.
#
# SORTIDA:
#   Cap fitxer; mostrem missatge de GUI requerida.
#
# QUÈ APRENEM:
#   - Verificar que el mòdul existeix.
#   - Recordar que alguns helpers necessiten QGIS obert.

import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

import utils.gui_utils as gu

print("OK -> gui_utils importat.")
print("Missatge GUI:", gu.GUI_REQUIRED_MESSAGE)
