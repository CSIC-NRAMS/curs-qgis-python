# OBJECTIU:
#   Convertir precipitació d'AEMET de dècimes de mm a mm i netejar valors.
#
# ENTRADA:
#   ./resultats/aemet_pas2_dates.csv
#
# SORTIDA:
#   ./resultats/aemet_pas3_precip.csv
#
# QUÈ APRENEM:
#   - Convertir valors numèrics amb to_float.
#   - Eliminar valors negatius o buits.
#   - Convertir dècimes de mm a mm.

import os  # Per gestionar rutes
import sys  # Per ajustar el path d'importació

# Afegim la carpeta arrel del projecte al sys.path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

# Importem configuració i utilitats
from utils.config import AEMET_PAS2_OUT, AEMET_PAS3_OUT, RESULTATS_DIR
from utils.csv_utils import ensure_dir, open_csv_reader, open_csv_writer, preview_csv
from utils.parse_utils import to_float

# Columnes de sortida
columnes = [
    "INDICATIVO", "NOMBRE", "ALTITUD", "LONGITUD", "LATITUD",
    "date", "precip_mm"
]

# Comptadors
files_llegides = 0
files_escrites = 0
files_saltades = 0

# Assegurem la carpeta de resultats
ensure_dir(RESULTATS_DIR)

# Obrim CSV d'entrada i sortida
with open_csv_reader(AEMET_PAS2_OUT, encoding="utf-8") as lector, \
     open_csv_writer(AEMET_PAS3_OUT, fieldnames=columnes) as escriptor:

    for fila in lector:
        files_llegides += 1

        # Llegim la precipitació en dècimes de mm
        p_tenths = to_float(fila.get("P_TENTHS"))

        # Si no és vàlid o és negatiu, saltem la fila
        if p_tenths is None or p_tenths < 0:
            files_saltades += 1
            # Comentari: valors negatius o buits no són vàlids
            continue

        # Convertim a mm
        precip_mm = p_tenths / 10.0

        # Creem la nova fila neta
        nova_fila = {
            "INDICATIVO": fila.get("INDICATIVO", ""),
            "NOMBRE": fila.get("NOMBRE", ""),
            "ALTITUD": fila.get("ALTITUD", ""),
            "LONGITUD": fila.get("LONGITUD", ""),
            "LATITUD": fila.get("LATITUD", ""),
            "date": fila.get("date", ""),
            "precip_mm": precip_mm
        }

        # Escrivim la fila
        escriptor.writerow(nova_fila)
        files_escrites += 1

# Preview del resultat
preview_csv(AEMET_PAS3_OUT, max_rows=5, title="Preview aemet_pas3_precip.csv")

# Missatges finals
print(f"OK -> creat {AEMET_PAS3_OUT}")
print(f"Files llegides: {files_llegides}")
print(f"Files escrites: {files_escrites}")
print(f"Files saltades (precipitació invàlida): {files_saltades}")
