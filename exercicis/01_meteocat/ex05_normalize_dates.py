"""Ex05 — Normalització de dates.

Fa: converteix DATA a format ISO.
Llegeix: PAS2B_OUT (meteocat_pas2b.csv)
Escriu: PAS3_OUT (meteocat_pas3.csv)
OK esperat: missatge amb files descartades per data invàlida.
"""

import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from tools.config import PAS2B_OUT, PAS3_OUT, RESULTATS_DIR
from tools.csv_utils import ensure_dir, open_csv_reader, open_csv_writer, preview_csv
from tools.parse_utils import parse_date

columnes = ["EMA", "DATA", "X", "Y", "PPT"]
files_llegides = 0
files_escrites = 0
files_saltades = 0

ensure_dir(RESULTATS_DIR)

with open_csv_reader(PAS2B_OUT, encoding="utf-8") as lector, \
     open_csv_writer(PAS3_OUT, fieldnames=columnes) as escriptor:

    # Convertim dates a format ISO i descartem les invalides.
    for fila in lector:
        files_llegides += 1
        data = parse_date(fila.get("DATA"))

        if data is None:
            files_saltades += 1
            continue

        nova_fila = dict(fila)
        nova_fila["DATA"] = data.isoformat()
        escriptor.writerow(nova_fila)
        files_escrites += 1

preview_csv(PAS3_OUT, max_rows=5, title="Preview meteocat_pas3.csv")
print(f"Files saltades (data invàlida): {files_saltades}")
