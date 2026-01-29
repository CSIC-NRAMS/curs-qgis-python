# OBJECTIU:
#   Crear la data completa a partir d'any, mes i dia.
#
# ENTRADA:
#   ./resultats/aemet_pas1_long.csv
#
# SORTIDA:
#   ./resultats/aemet_pas2_dates.csv
#
# QUÈ APRENEM:
#   - Crear dates vàlides amb build_date.
#   - Saltar dies inexistents (ex: 30/02).

import os  # Per gestionar rutes
import sys  # Per ajustar el path d'importació

# Afegim la carpeta arrel del projecte al sys.path
ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

# Importem configuració i utilitats
from utils.config import AEMET_PAS1_OUT, AEMET_PAS2_OUT, RESULTATS_DIR
from utils.csv_utils import ensure_dir, open_csv_reader, open_csv_writer, preview_csv
from utils.parse_utils import build_date

# Columnes de sortida
columnes = [
    "INDICATIVO", "NOMBRE", "ALTITUD", "LONGITUD", "LATITUD",
    "AÑO", "MES", "DAY", "date", "P_TENTHS"
]

# Comptadors
files_llegides = 0
files_escrites = 0
files_saltades = 0

# Assegurem la carpeta de resultats
ensure_dir(RESULTATS_DIR)

# Obrim CSV d'entrada i sortida
with open_csv_reader(AEMET_PAS1_OUT, encoding="utf-8") as lector, \
     open_csv_writer(AEMET_PAS2_OUT, fieldnames=columnes) as escriptor:

    for fila in lector:
        files_llegides += 1

        # Construïm la data
        data = build_date(fila.get("AÑO"), fila.get("MES"), fila.get("DAY"))

        # Si la data no és vàlida, saltem la fila
        if data is None:
            files_saltades += 1
            # Comentari: data impossible pel calendari
            continue

        # Creem la nova fila amb la data en ISO
        nova_fila = dict(fila)
        nova_fila["date"] = data.isoformat()

        # Escrivim la fila
        escriptor.writerow(nova_fila)
        files_escrites += 1

# Preview del resultat
preview_csv(AEMET_PAS2_OUT, max_rows=5, title="Preview aemet_pas2_dates.csv")

# Missatges finals
print(f"OK -> creat {AEMET_PAS2_OUT}")
print(f"Files llegides: {files_llegides}")
print(f"Files escrites: {files_escrites}")
print(f"Files saltades (dates invàlides): {files_saltades}")
