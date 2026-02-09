"""Ex05 — Transformar coordenades AEMET (UTM -> WGS84).

Fa: crea lon/lat a partir de coordenades UTM.
Llegeix: AEMET_PAS3_OUT (aemet_pas3_precip.csv)
Escriu: AEMET_PAS4_OUT (aemet_pas4_coords.csv)
OK esperat: missatge d'OK i preview del pas 4.
"""

import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from tools.config import AEMET_PAS3_OUT, AEMET_PAS4_OUT, RESULTATS_DIR
from tools.csv_utils import ensure_dir, open_csv_reader, open_csv_writer, preview_csv
from tools.parse_utils import to_float
from tools.qgis_utils import get_utm31_to_wgs84_transformer, transform_utm_to_lonlat

columnes = [
    "INDICATIVO", "NOMBRE", "ALTITUD",
    "x_utm", "y_utm", "lon", "lat",
    "date", "precip_mm"
]
files_llegides = 0
files_escrites = 0

ensure_dir(RESULTATS_DIR)
xform = get_utm31_to_wgs84_transformer()

with open_csv_reader(AEMET_PAS3_OUT, encoding="utf-8") as lector, \
     open_csv_writer(AEMET_PAS4_OUT, fieldnames=columnes) as escriptor:

    # Les columnes LONGITUD/LATITUD son UTM en metres, no graus.
    for fila in lector:
        files_llegides += 1
        x = to_float(fila.get("LONGITUD"))
        y = to_float(fila.get("LATITUD"))

        if x is None or y is None:
            continue

        try:
            lon, lat = transform_utm_to_lonlat(x, y, xform)
        except:
            continue

        nova_fila = {
            "INDICATIVO": fila.get("INDICATIVO", ""),
            "NOMBRE": fila.get("NOMBRE", ""),
            "ALTITUD": fila.get("ALTITUD", ""),
            "x_utm": x,
            "y_utm": y,
            "lon": lon,
            "lat": lat,
            "date": fila.get("date", ""),
            "precip_mm": fila.get("precip_mm", "")
        }
        escriptor.writerow(nova_fila)
        files_escrites += 1

preview_csv(AEMET_PAS4_OUT, max_rows=5, title="Preview aemet_pas4_coords.csv")
print(f"OK -> creat {AEMET_PAS4_OUT}")
