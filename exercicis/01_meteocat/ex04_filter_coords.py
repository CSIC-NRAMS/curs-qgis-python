"""Ex04 — Filtre de coordenades buides.

Fa: elimina files sense X o Y.
Llegeix: PAS2A_OUT (meteocat_pas2a.csv)
Escriu: PAS2B_OUT (meteocat_pas2b.csv)
OK esperat: missatge amb files saltades.
"""

import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from tools.config import PAS2A_OUT, PAS2B_OUT, RESULTATS_DIR
from tools.csv_utils import ensure_dir, open_csv_reader, open_csv_writer, preview_csv

columnes = ["EMA", "DATA", "X", "Y", "PPT"]
files_llegides = 0
files_escrites = 0
files_saltades = 0

ensure_dir(RESULTATS_DIR)

with open_csv_reader(PAS2A_OUT, encoding="utf-8") as lector, \
     open_csv_writer(PAS2B_OUT, fieldnames=columnes) as escriptor:

    # Rebutgem files sense coordenades, perque no es poden mapar.
    for fila in lector:
        files_llegides += 1
        x = fila.get("X")
        y = fila.get("Y")

        if x in (None, "") or y in (None, ""):
            files_saltades += 1
            continue

        escriptor.writerow(fila)
        files_escrites += 1

preview_csv(PAS2B_OUT, max_rows=5, title="Preview meteocat_pas2b.csv")
print(f"Files saltades (X o Y buits): {files_saltades}")
