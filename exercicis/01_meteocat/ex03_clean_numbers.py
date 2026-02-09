"""Ex03 — Neteja de números.

Fa: converteix X/Y/PPT a float.
Llegeix: PAS1_OUT (meteocat_pas1.csv)
Escriu: PAS2A_OUT (meteocat_pas2a.csv)
OK esperat: missatge d'OK i preview del pas 2a.
"""

import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from tools.config import PAS1_OUT, PAS2A_OUT, RESULTATS_DIR
from tools.csv_utils import ensure_dir, open_csv_reader, open_csv_writer, preview_csv
from tools.parse_utils import to_float

columnes = ["EMA", "DATA", "X", "Y", "PPT"]
files_llegides = 0
files_escrites = 0

ensure_dir(RESULTATS_DIR)

with open_csv_reader(PAS1_OUT, encoding="utf-8") as lector, \
     open_csv_writer(PAS2A_OUT, fieldnames=columnes) as escriptor:

    # Convertim textos a numeros reals quan es pot.
    for fila in lector:
        files_llegides += 1
        x = to_float(fila.get("X"))
        y = to_float(fila.get("Y"))
        ppt = to_float(fila.get("PPT"))

        nova_fila = {
            "EMA": fila.get("EMA", ""),
            "DATA": fila.get("DATA", ""),
            "X": x,
            "Y": y,
            "PPT": ppt
        }
        escriptor.writerow(nova_fila)
        files_escrites += 1

preview_csv(PAS2A_OUT, max_rows=5, title="Preview meteocat_pas2a.csv")
print(f"OK -> creat {PAS2A_OUT}")
