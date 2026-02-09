"""Ex01 — Preview del CSV AEMET.

Fa: mostra capçaleres i 5 files.
Llegeix: AEMET_INPUT
Escriu: res (nomes consola)
OK esperat: missatge d'OK i preview a la consola.
"""

import os
import sys

# Afegim l'arrel del projecte al sys.path per poder importar tools/.
ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from tools.config import AEMET_INPUT
from tools.csv_utils import preview_csv

# Llegim i mostrem un preview sense modificar cap fitxer.
preview_csv(AEMET_INPUT, max_rows=5, title="Preview AEMET")
print("OK -> Previsualització AEMET feta.")
