"""Ex04 — Convertir unitats de precipitacio AEMET.

Fa: passa de decimals en decimes a mm reals.
Llegeix: AEMET_PAS2_OUT (aemet_pas2_dates.csv)
Escriu: AEMET_PAS3_OUT (aemet_pas3_precip.csv)
OK esperat: missatge d'OK i preview del pas 3.
"""

import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from tools.config import AEMET_PAS2_OUT, AEMET_PAS3_OUT, RESULTATS_DIR
from tools.csv_utils import ensure_dir, open_csv_reader, open_csv_writer, preview_csv
from tools.parse_utils import to_float

columnes = [
    "INDICATIVO", "NOMBRE", "ALTITUD", "LONGITUD", "LATITUD",
    "date", "precip_mm"
]
files_llegides = 0
files_escrites = 0

ensure_dir(RESULTATS_DIR)

with open_csv_reader(AEMET_PAS2_OUT, encoding="utf-8") as lector, \
     open_csv_writer(AEMET_PAS3_OUT, fieldnames=columnes) as escriptor:

    # Convertim P_TENTHS (decimes de mm) a mm, descartant valors invalids.
    for fila in lector:
        files_llegides += 1
        p_tenths = to_float(fila.get("P_TENTHS"))

        if p_tenths is None or p_tenths < 0:
            continue

        precip_mm = p_tenths / 10.0

        nova_fila = {
            "INDICATIVO": fila.get("INDICATIVO", ""),
            "NOMBRE": fila.get("NOMBRE", ""),
            "ALTITUD": fila.get("ALTITUD", ""),
            "LONGITUD": fila.get("LONGITUD", ""),
            "LATITUD": fila.get("LATITUD", ""),
            "date": fila.get("date", ""),
            "precip_mm": precip_mm
        }
        escriptor.writerow(nova_fila)
        files_escrites += 1

preview_csv(AEMET_PAS3_OUT, max_rows=5, title="Preview aemet_pas3_precip.csv")
print(f"OK -> creat {AEMET_PAS3_OUT}")
