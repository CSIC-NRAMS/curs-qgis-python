"""Ex01 — Merge Meteocat i AEMET.

Fa: uneix dos CSV estandarditzats i els ordena per data.
Llegeix: STD_OUT i AEMET_STD_OUT
Escriu: MERGED_STD_OUT
OK esperat: missatge d'OK i preview del fitxer fusionat.
"""

import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from tools.config import STD_OUT, AEMET_STD_OUT, MERGED_STD_OUT, STD_FIELDS, RESULTATS_DIR
from tools.csv_utils import ensure_dir, open_csv_reader, open_csv_writer, preview_csv

files_llegides = 0
files_escrites = 0

ensure_dir(RESULTATS_DIR)
files_totals = []

# Llegim METEOCAT
with open_csv_reader(STD_OUT, encoding="utf-8") as lector:
    # Afegim totes les files del Meteocat a una llista comuna.
    for fila in lector:
        files_totals.append(fila)
        files_llegides += 1

# Llegim AEMET
with open_csv_reader(AEMET_STD_OUT, encoding="utf-8") as lector:
    # Afegim totes les files d'AEMET a la mateixa llista.
    for fila in lector:
        files_totals.append(fila)
        files_llegides += 1

# Ordenem per data i source
# (Primer cop: lambda) Una lambda es una funcio curta per definir claus d'ordenacio.
files_totals.sort(key=lambda r: (r.get("date", ""), r.get("source", "")))

with open_csv_writer(MERGED_STD_OUT, fieldnames=STD_FIELDS) as escriptor:
    # Escrivim totes les files fusionades amb l'esquema estandard.
    for fila in files_totals:
        escriptor.writerow(fila)
        files_escrites += 1

preview_csv(MERGED_STD_OUT, max_rows=5, title="Preview precipitacio_olot_estandarditzada.csv")
print(f"OK -> creat {MERGED_STD_OUT}")
