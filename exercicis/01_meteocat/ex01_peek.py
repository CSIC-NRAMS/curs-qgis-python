"""Ex01 — Preview del CSV Meteocat.

Fa: mostra capçaleres i 5 files.
Llegeix: METEOCAT_INPUT
Escriu: res (només consola)
OK esperat: missatge d'OK i preview a la consola.
"""

import os
import sys

# Afegim l'arrel del projecte al sys.path per poder importar tools/.
ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from tools.config import METEOCAT_INPUT
from tools.csv_utils import preview_csv

# Llegim i mostrem un preview sense modificar cap fitxer.
preview_csv(METEOCAT_INPUT, max_rows=5, title="Preview del CSV METEOCAT")
print("OK -> Mostrades capçaleres i 5 files del CSV.")
