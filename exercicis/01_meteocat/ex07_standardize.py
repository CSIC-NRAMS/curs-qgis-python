"""Ex07 — Estandardització final.

Fa: mapeja camps al format estàndard.
Llegeix: PAS4_OUT (meteocat_pas4.csv)
Escriu: STD_OUT (meteocat_std.csv)
OK esperat: missatge d'OK i preview del fitxer final.
"""

import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from tools.config import PAS4_OUT, STD_OUT, STD_FIELDS, RESULTATS_DIR
from tools.csv_utils import ensure_dir, open_csv_reader, open_csv_writer, preview_csv

files_llegides = 0
files_escrites = 0
files_saltades = 0

ensure_dir(RESULTATS_DIR)

with open_csv_reader(PAS4_OUT, encoding="utf-8") as lector, \
     open_csv_writer(STD_OUT, fieldnames=STD_FIELDS) as escriptor:

    # Mapejem camps del Meteocat al model estandard del curs.
    for fila in lector:
        files_llegides += 1

        ema = (fila.get("EMA") or "").strip()
        data = (fila.get("DATA") or "").strip()
        ppt = fila.get("PPT")
        lon = fila.get("lon")
        lat = fila.get("lat")
        x_utm = fila.get("X")
        y_utm = fila.get("Y")

        if not (ema and data and lon and lat and x_utm and y_utm):
            files_saltades += 1
            continue

        nova_fila = {
            "source": "METEOCAT",
            "station_id": ema,
            "station_name": f"Olot (Meteocat EMA {ema})",
            "date": data,
            "precip_mm": ppt,
            "lon": lon,
            "lat": lat,
            "x_utm": x_utm,
            "y_utm": y_utm,
            "alt_m": ""
        }
        escriptor.writerow(nova_fila)
        files_escrites += 1

preview_csv(STD_OUT, max_rows=5, title="Preview meteocat_std.csv")
print(f"OK -> creat {STD_OUT}")
