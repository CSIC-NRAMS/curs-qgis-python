# OBJECTIU:
#   Fer un primer "peek" del CSV d'AEMET.
#
# ENTRADA:
#   ./dades/entrada/Precipitació_Olot_AEMET.csv
#
# SORTIDA:
#   Cap fitxer; mostrem informació per pantalla.
#
# QUÈ APRENEM:
#   - Reutilitzar preview_csv per entendre l'estructura d'un CSV.

import os  # Per gestionar rutes
import sys  # Per ajustar el path d'importació

# Afegim la carpeta arrel del projecte al sys.path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

# Importem configuració i utilitats
from utils.config import AEMET_INPUT
from utils.csv_utils import preview_csv

# Mostrem el preview
preview_csv(AEMET_INPUT, max_rows=5, title="Preview AEMET")

print("OK -> Previsualització AEMET feta.")
