"""Ex02 — Despivotar AEMET (wide -> long).

Fa: converteix columnes P1..P31 en files diaries.
Llegeix: AEMET_INPUT
Escriu: AEMET_PAS1_OUT (aemet_pas1_long.csv)
OK esperat: missatge d'OK i preview del pas 1.
"""

import os
import sys

# (Ja explicat abans) Preparem l'import del paquet tools.
ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from tools.config import AEMET_INPUT, AEMET_PAS1_OUT, RESULTATS_DIR
from tools.csv_utils import ensure_dir, open_csv_reader, open_csv_writer, preview_csv

columnes = [
    "INDICATIVO", "NOMBRE", "ALTITUD", "LONGITUD", "LATITUD",
    "AÑO", "MES", "DAY", "P_TENTHS"
]
files_llegides = 0
files_escrites = 0

ensure_dir(RESULTATS_DIR)

with open_csv_reader(AEMET_INPUT) as lector, \
     open_csv_writer(AEMET_PAS1_OUT, fieldnames=columnes) as escriptor:

    # Detectem totes les columnes P* (dies del mes) del CSV original.
    p_cols = [c for c in lector.fieldnames if c.startswith("P") and c[1:].isdigit()]
    print(f"Columnes P* detectades: {len(p_cols)} -> {p_cols}")

    # Per cada fila mensual, creem una fila per cada dia amb valor.
    for fila in lector:
        files_llegides += 1
        for col in p_cols:
            val = fila.get(col)
            if val is None or str(val).strip() == "":
                continue

            day_num = int(col.replace("P", ""))
            
            nova_fila = {
                "INDICATIVO": fila.get("INDICATIVO", ""),
                "NOMBRE": fila.get("NOMBRE", ""),
                "ALTITUD": fila.get("ALTITUD", ""),
                "LONGITUD": fila.get("LONGITUD", ""),
                "LATITUD": fila.get("LATITUD", ""),
                "AÑO": fila.get("AÑO", ""),
                "MES": fila.get("MES", ""),
                "DAY": day_num,
                "P_TENTHS": val
            }
            escriptor.writerow(nova_fila)
            files_escrites += 1

print(f"Dies generats (files escrites): {files_escrites}")
preview_csv(AEMET_PAS1_OUT, max_rows=5, title="Preview aemet_pas1_long.csv")
print(f"OK -> creat {AEMET_PAS1_OUT}")
