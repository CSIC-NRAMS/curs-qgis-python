"""Ex06 — Estandarditzacio AEMET.

Fa: mapeja camps al format estandard del curs.
Llegeix: AEMET_PAS4_OUT (aemet_pas4_coords.csv)
Escriu: AEMET_STD_OUT (aemet_std.csv)
OK esperat: missatge d'OK i preview del fitxer final.
"""

import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from tools.config import AEMET_PAS4_OUT, AEMET_STD_OUT, STD_FIELDS, RESULTATS_DIR
from tools.csv_utils import ensure_dir, open_csv_reader, open_csv_writer, preview_csv

files_llegides = 0
files_escrites = 0

ensure_dir(RESULTATS_DIR)

with open_csv_reader(AEMET_PAS4_OUT, encoding="utf-8") as lector, \
     open_csv_writer(AEMET_STD_OUT, fieldnames=STD_FIELDS) as escriptor:

    # Mapejem camps d'AEMET al mateix esquema que Meteocat.
    for fila in lector:
        files_llegides += 1

        indicatiu = (fila.get("INDICATIVO") or "").strip()
        nom = (fila.get("NOMBRE") or "").strip()
        data = (fila.get("date") or "").strip()
        precip = fila.get("precip_mm")
        lon = fila.get("lon")
        lat = fila.get("lat")
        x_utm = fila.get("x_utm")
        y_utm = fila.get("y_utm")
        alt = fila.get("ALTITUD")

        if not (indicatiu and data and lon and lat and x_utm and y_utm):
            continue

        nova_fila = {
            "source": "AEMET",
            "station_id": indicatiu,
            "station_name": nom,
            "date": data,
            "precip_mm": precip,
            "lon": lon,
            "lat": lat,
            "x_utm": x_utm,
            "y_utm": y_utm,
            "alt_m": alt
        }
        escriptor.writerow(nova_fila)
        files_escrites += 1

preview_csv(AEMET_STD_OUT, max_rows=5, title="Preview aemet_std.csv")
print(f"OK -> creat {AEMET_STD_OUT}")
