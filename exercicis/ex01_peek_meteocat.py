# OBJECTIU:
#   Fer un primer "peek" del CSV de METEOCAT usant una funció reutilitzable.
#
# ENTRADA:
#   ./dades/Precipitació_Olot_METEOCAT.csv
#
# SORTIDA:
#   Cap fitxer de sortida. Només mostrem informació per pantalla.
#
# QUÈ APRENEM:
#   - Importar utilitats reutilitzables.
#   - Mostrar capçaleres i un mini‑preview de 5 files.
#   - Preparar un disseny que reaprofitem als següents exercicis.

import os  # Mòdul per treballar amb rutes
import sys  # Mòdul per ajustar el path d'importació

# Afegim la carpeta arrel del projecte al sys.path
ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

# Importem configuració i utilitats reutilitzables
from utils.config import METEOCAT_INPUT  # Ruta del CSV d'entrada
from utils.csv_utils import preview_csv  # Funció de preview reutilitzable

# Mostrem un preview amable del fitxer d'entrada
preview_csv(METEOCAT_INPUT, max_rows=5, title="Preview del CSV METEOCAT")

# Missatge final informatiu
print("OK -> Mostrades capçaleres i 5 files del CSV.")
