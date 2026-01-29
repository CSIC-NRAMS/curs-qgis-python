# OBJECTIU:
#   Unir METEOCAT i AEMET estandarditzats en un sol CSV.
#
# ENTRADA:
#   ./resultats/meteocat_std.csv
#   ./resultats/aemet_std.csv
#
# SORTIDA:
#   ./resultats/precipitacio_olot_estandarditzada.csv
#
# QUÈ APRENEM:
#   - Llegir dos CSV amb el mateix esquema.
#   - Unir llistes i ordenar per data.

import os  # Per gestionar rutes
import sys  # Per ajustar el path d'importació

# Afegim la carpeta arrel del projecte al sys.path
ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

# Importem configuració i utilitats
from utils.config import STD_OUT, AEMET_STD_OUT, MERGED_STD_OUT, STD_FIELDS, RESULTATS_DIR
from utils.csv_utils import ensure_dir, open_csv_reader, open_csv_writer, preview_csv

# Comptadors
files_llegides = 0
files_escrites = 0

# Assegurem la carpeta de resultats
ensure_dir(RESULTATS_DIR)

# Llista temporal per ordenar (primer acumulem totes les files)
files_totals = []

# Llegim METEOCAT (ja està estandarditzat)
with open_csv_reader(STD_OUT, encoding="utf-8") as lector:
    for fila in lector:
        files_totals.append(fila)
        files_llegides += 1

# Llegim AEMET (ja està estandarditzat)
with open_csv_reader(AEMET_STD_OUT, encoding="utf-8") as lector:
    for fila in lector:
        files_totals.append(fila)
        files_llegides += 1

# Ordenem per data i source (així veiem la cronologia combinada)
files_totals.sort(key=lambda r: (r.get("date", ""), r.get("source", "")))

# Escrivim la sortida final amb el mateix esquema per a totes les fonts
with open_csv_writer(MERGED_STD_OUT, fieldnames=STD_FIELDS) as escriptor:
    for fila in files_totals:
        escriptor.writerow(fila)
        files_escrites += 1

# Preview del resultat
preview_csv(MERGED_STD_OUT, max_rows=5, title="Preview precipitacio_olot_estandarditzada.csv")

# Missatges finals
print(f"OK -> creat {MERGED_STD_OUT}")
print(f"Files llegides (sumades): {files_llegides}")
print(f"Files escrites: {files_escrites}")
