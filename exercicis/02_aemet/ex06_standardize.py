# OBJECTIU:
#   Crear el CSV estandarditzat d'AEMET amb el mateix esquema final.
#
# ENTRADA:
#   ./resultats/aemet_pas4_coords.csv
#
# SORTIDA:
#   ./resultats/aemet_std.csv
#
# QUÈ APRENEM:
#   - Unificar camps entre fonts diferents.
#   - Generar el format final estàndard.

import os  # Per gestionar rutes
import sys  # Per ajustar el path d'importació

# Afegim la carpeta arrel del projecte al sys.path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

# Importem configuració i utilitats
from utils.config import AEMET_PAS4_OUT, AEMET_STD_OUT, STD_FIELDS, RESULTATS_DIR
from utils.csv_utils import ensure_dir, open_csv_reader, open_csv_writer, preview_csv

# Comptadors
files_llegides = 0
files_escrites = 0
files_saltades = 0

# Assegurem la carpeta de resultats
ensure_dir(RESULTATS_DIR)

# Obrim CSV d'entrada i sortida
with open_csv_reader(AEMET_PAS4_OUT, encoding="utf-8") as lector, \
     open_csv_writer(AEMET_STD_OUT, fieldnames=STD_FIELDS) as escriptor:

    for fila in lector:
        files_llegides += 1

        # Camps essencials
        indicatiu = (fila.get("INDICATIVO") or "").strip()
        nom = (fila.get("NOMBRE") or "").strip()
        data = (fila.get("date") or "").strip()
        precip = fila.get("precip_mm")
        lon = fila.get("lon")
        lat = fila.get("lat")
        x_utm = fila.get("x_utm")
        y_utm = fila.get("y_utm")
        alt = fila.get("ALTITUD")

        # Validem dades mínimes
        if not (indicatiu and data and lon and lat and x_utm and y_utm):
            files_saltades += 1
            # Comentari: falten camps clau
            continue

        # Construïm la fila estandarditzada
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

        # Escrivim la fila
        escriptor.writerow(nova_fila)
        files_escrites += 1

# Preview del resultat
preview_csv(AEMET_STD_OUT, max_rows=5, title="Preview aemet_std.csv")

# Resum final
print(f"OK -> creat {AEMET_STD_OUT}")
print(f"Files llegides: {files_llegides}")
print(f"Files escrites: {files_escrites}")
print(f"Files descartades (dades mancants): {files_saltades}")
