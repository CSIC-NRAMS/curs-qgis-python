# OBJECTIU:
#   Transformar coordenades AEMET (UTM 31N) a lon/lat (WGS84).
#
# ENTRADA:
#   ./resultats/aemet_pas3_precip.csv
#
# SORTIDA:
#   ./resultats/aemet_pas4_coords.csv
#
# QUÈ APRENEM:
#   - Reutilitzar funcions de transformació CRS.
#   - Afegir lon/lat a un CSV.

import os  # Per gestionar rutes
import sys  # Per ajustar el path d'importació

# Afegim la carpeta arrel del projecte al sys.path
ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

# Importem configuració i utilitats
from utils.config import AEMET_PAS3_OUT, AEMET_PAS4_OUT, RESULTATS_DIR
from utils.csv_utils import ensure_dir, open_csv_reader, open_csv_writer, preview_csv
from utils.parse_utils import to_float
from utils.qgis_utils import get_utm31_to_wgs84_transformer, transform_utm_to_lonlat

# Columnes de sortida
columnes = [
    "INDICATIVO", "NOMBRE", "ALTITUD",
    "x_utm", "y_utm", "lon", "lat",
    "date", "precip_mm"
]

# Comptadors
files_llegides = 0
files_escrites = 0
files_saltades = 0

# Assegurem la carpeta de resultats
ensure_dir(RESULTATS_DIR)

# Transformador CRS
xform = get_utm31_to_wgs84_transformer()

# Obrim CSV d'entrada i sortida
with open_csv_reader(AEMET_PAS3_OUT, encoding="utf-8") as lector, \
     open_csv_writer(AEMET_PAS4_OUT, fieldnames=columnes) as escriptor:

    for fila in lector:
        files_llegides += 1

        # Convertim LONGITUD/LATITUD a float (són UTM X/Y)
        x = to_float(fila.get("LONGITUD"))
        y = to_float(fila.get("LATITUD"))

        # Si falta alguna coordenada, saltem
        if x is None or y is None:
            files_saltades += 1
            # Comentari: coordenades buides o incorrectes
            continue

        # Transformem a lon/lat
        try:
            lon, lat = transform_utm_to_lonlat(x, y, xform)
        except:
            files_saltades += 1
            # Comentari: transformació fallida
            continue

        # Creem la nova fila
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

        # Escrivim la fila
        escriptor.writerow(nova_fila)
        files_escrites += 1

# Preview del resultat
preview_csv(AEMET_PAS4_OUT, max_rows=5, title="Preview aemet_pas4_coords.csv")

# Missatges finals
print(f"OK -> creat {AEMET_PAS4_OUT}")
print(f"Files llegides: {files_llegides}")
print(f"Files escrites: {files_escrites}")
print(f"Files saltades (coords invàlides): {files_saltades}")
