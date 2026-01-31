# OBJECTIU:
#   Transformar coordenades UTM (EPSG:25831) a lon/lat (EPSG:4326) amb PyQGIS.
#
# ENTRADA:
#   ./resultats/meteocat_pas3.csv
#
# SORTIDA:
#   ./resultats/meteocat_pas4.csv
#
# QUÈ APRENEM:
#   - Utilitzar utilitats PyQGIS reutilitzables.
#   - Transformar coordenades amb un helper.
#   - Afegir lon i lat a un CSV.

import os  # Per gestionar rutes
import sys  # Per ajustar el path d'importació

# Afegim la carpeta arrel del projecte al sys.path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

# Importem configuració i utilitats
from utils.config import PAS3_OUT, PAS4_OUT, RESULTATS_DIR  # Rutes centralitzades
from utils.csv_utils import ensure_dir, open_csv_reader, open_csv_writer, preview_csv
from utils.qgis_utils import get_utm31_to_wgs84_transformer, transform_utm_to_lonlat

# Columnes del fitxer de sortida
columnes = ["EMA", "DATA", "X", "Y", "PPT", "lon", "lat"]

# Creem el transformador de coordenades
xform = get_utm31_to_wgs84_transformer()

# Comptadors
files_llegides = 0
files_escrites = 0
files_saltades = 0

# Assegurem que la carpeta de resultats existeix
ensure_dir(RESULTATS_DIR)

# Obrim fitxers d'entrada i sortida
with open_csv_reader(PAS3_OUT, encoding="utf-8") as lector, \
     open_csv_writer(PAS4_OUT, fieldnames=columnes) as escriptor:

    for fila in lector:
        files_llegides += 1  # Comptem la fila

        # Obtenim X i Y i els convertim a float
        try:
            x = float(fila.get("X"))
            y = float(fila.get("Y"))
        except:
            files_saltades += 1
            # Comentari: saltem la fila perquè X o Y no són vàlids
            continue

        # Transformem el punt amb la utilitat reutilitzable
        try:
            lon, lat = transform_utm_to_lonlat(x, y, xform)
        except:
            files_saltades += 1
            # Comentari: saltem la fila si la transformació falla
            continue

        # Creem la nova fila amb lon i lat
        nova_fila = dict(fila)
        nova_fila["lon"] = lon
        nova_fila["lat"] = lat

        escriptor.writerow(nova_fila)  # Escrivim la fila
        files_escrites += 1

# Mostrem un preview del resultat
preview_csv(PAS4_OUT, max_rows=5, title="Preview meteocat_pas4.csv")

# Missatges finals
print(f"OK -> creat {PAS4_OUT}")
print(f"Files llegides: {files_llegides}")
print(f"Files escrites: {files_escrites}")
print(f"Files saltades (coordenades invàlides): {files_saltades}")
