"""Ex03 — Construir dates AEMET.

Fa: crea el camp date a partir d'any/mes/dia.
Llegeix: AEMET_PAS1_OUT (aemet_pas1_long.csv)
Escriu: AEMET_PAS2_OUT (aemet_pas2_dates.csv)
OK esperat: missatge d'OK i preview del pas 2.
"""

import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from tools.config import AEMET_PAS1_OUT, AEMET_PAS2_OUT, RESULTATS_DIR
from tools.csv_utils import ensure_dir, open_csv_reader, open_csv_writer, preview_csv
from tools.parse_utils import build_date

columnes = [
    "INDICATIVO", "NOMBRE", "ALTITUD", "LONGITUD", "LATITUD",
    "AÑO", "MES", "DAY", "date", "P_TENTHS"
]
files_llegides = 0
files_escrites = 0

ensure_dir(RESULTATS_DIR)

with open_csv_reader(AEMET_PAS1_OUT, encoding="utf-8") as lector, \
     open_csv_writer(AEMET_PAS2_OUT, fieldnames=columnes) as escriptor:

    # Unim any/mes/dia en una data ISO; descartem dates impossibles.
    for fila in lector:
        files_llegides += 1
        data = build_date(fila.get("AÑO"), fila.get("MES"), fila.get("DAY"))

        if data is None:
            continue

        nova_fila = dict(fila)
        nova_fila["date"] = data.isoformat()
        escriptor.writerow(nova_fila)
        files_escrites += 1

preview_csv(AEMET_PAS2_OUT, max_rows=5, title="Preview aemet_pas2_dates.csv")
print(f"OK -> creat {AEMET_PAS2_OUT}")
