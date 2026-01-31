# OBJECTIU:
#   Generar el CSV estandarditzat final amb l'esquema requerit.
#
# ENTRADA:
#   ./resultats/meteocat_pas4.csv
#
# SORTIDA:
#   ./resultats/meteocat_std.csv
#
# QUÈ APRENEM:
#   - Crear un CSV amb un esquema final fix.
#   - Omplir camps nous a partir dels existents.
#   - Fer un resum final de processament.

import os  # Per gestionar rutes
import sys  # Per ajustar el path d'importació

# Afegim la carpeta arrel del projecte al sys.path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

# Importem configuració i utilitats
from utils.config import PAS4_OUT, STD_OUT, STD_FIELDS, RESULTATS_DIR  # Rutes i camps finals
from utils.csv_utils import ensure_dir, open_csv_reader, open_csv_writer, preview_csv

# Comptadors
files_llegides = 0
files_escrites = 0
files_saltades = 0

# Assegurem que la carpeta de resultats existeix
ensure_dir(RESULTATS_DIR)

# Obrim fitxers d'entrada i sortida
with open_csv_reader(PAS4_OUT, encoding="utf-8") as lector, \
     open_csv_writer(STD_OUT, fieldnames=STD_FIELDS) as escriptor:

    for fila in lector:
        files_llegides += 1  # Comptem la fila

        # Recuperem valors necessaris
        ema = (fila.get("EMA") or "").strip()
        data = (fila.get("DATA") or "").strip()
        ppt = fila.get("PPT")
        lon = fila.get("lon")
        lat = fila.get("lat")
        x_utm = fila.get("X")
        y_utm = fila.get("Y")

        # Si falta alguna dada essencial, saltem la fila
        if not (ema and data and lon and lat and x_utm and y_utm):
            files_saltades += 1
            # Comentari: saltem la fila perquè falten dades necessàries
            continue

        # Construïm la fila final estandarditzada
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
            "alt_m": ""  # No tenim l'altitud
        }

        escriptor.writerow(nova_fila)  # Escrivim la fila
        files_escrites += 1

# Mostrem un preview del CSV final
preview_csv(STD_OUT, max_rows=5, title="Preview meteocat_std.csv")

# Resum final
print(f"OK -> creat {STD_OUT}")
print(f"Files llegides: {files_llegides}")
print(f"Files escrites: {files_escrites}")
print(f"Files descartades (dades mancants): {files_saltades}")
