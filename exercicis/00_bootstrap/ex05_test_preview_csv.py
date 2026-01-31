# OBJECTIU:
#   Presentar la funció reutilitzable preview_csv.
#
# ENTRADA:
#   ./dades/entrada/Precipitacio_Olot_METEOCAT.csv
#   ./dades/entrada/Precipitacio_Olot_AEMET.csv
#
# SORTIDA:
#   Cap fitxer; fem un preview per pantalla.
#
# QUÈ APRENEM:
#   - Reutilitzar funcions d'altres mòduls.
#   - Veure ràpidament l'estructura d'un CSV.

import os  # Per gestionar rutes
import sys  # Per ajustar el path d'importació

# Afegim la carpeta arrel del projecte al sys.path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

# Importem configuració i utilitat de preview
from utils.config import METEOCAT_INPUT, AEMET_INPUT
from utils.csv_utils import preview_csv

# Preview del CSV METEOCAT
preview_csv(METEOCAT_INPUT, max_rows=5, title="Preview METEOCAT")

# Preview del CSV AEMET
preview_csv(AEMET_INPUT, max_rows=5, title="Preview AEMET")

print("OK -> Previews mostrats.")
