"""Ex06 — Transformació CRS UTM → WGS84.

Fa: afegeix lon/lat a partir d'X/Y UTM.
Llegeix: PAS3_OUT (meteocat_pas3.csv)
Escriu: PAS4_OUT (meteocat_pas4.csv)
OK esperat: missatge d'OK i preview del pas 4.
"""

import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from tools.config import PAS3_OUT, PAS4_OUT, RESULTATS_DIR
from tools.csv_utils import ensure_dir, open_csv_reader, open_csv_writer, preview_csv
from tools.qgis_utils import get_utm31_to_wgs84_transformer, transform_utm_to_lonlat

# Preparem el transformador de coordenades (UTM -> lon/lat).
columnes = ["EMA", "DATA", "X", "Y", "PPT", "lon", "lat"]
xform = get_utm31_to_wgs84_transformer()
files_llegides = 0
files_escrites = 0
files_saltades = 0

ensure_dir(RESULTATS_DIR)

with open_csv_reader(PAS3_OUT, encoding="utf-8") as lector, \
     open_csv_writer(PAS4_OUT, fieldnames=columnes) as escriptor:

    # Convertim X/Y a floats i calculem lon/lat; si falla, descartem la fila.
    for fila in lector:
        files_llegides += 1
        try:
            x = float(fila.get("X"))
            y = float(fila.get("Y"))
        except:
            files_saltades += 1
            continue

        try:
            lon, lat = transform_utm_to_lonlat(x, y, xform)
        except:
            files_saltades += 1
            continue

        nova_fila = dict(fila)
        nova_fila["lon"] = lon
        nova_fila["lat"] = lat
        escriptor.writerow(nova_fila)
        files_escrites += 1

preview_csv(PAS4_OUT, max_rows=5, title="Preview meteocat_pas4.csv")
print(f"OK -> creat {PAS4_OUT}")
