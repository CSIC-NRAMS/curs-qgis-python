# OBJECTIU:
#   Convertir la data a format ISO (YYYY-MM-DD) i descartar dates invàlides.
#
# ENTRADA:
#   ./resultats/meteocat_pas2b.csv
#
# SORTIDA:
#   ./resultats/meteocat_pas3.csv
#
# QUÈ APRENEM:
#   - Parsejar dates amb diferents formats.
#   - Escriure dates en format ISO.
#   - Fer un preview del resultat.

import os  # Per gestionar rutes
import sys  # Per ajustar el path d'importació

# Afegim la carpeta arrel del projecte al sys.path
ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

# Importem configuració i utilitats
from utils.config import PAS2B_OUT, PAS3_OUT, RESULTATS_DIR  # Rutes centralitzades
from utils.csv_utils import ensure_dir, open_csv_reader, open_csv_writer, preview_csv
from utils.parse_utils import parse_date  # Funció reutilitzable de dates

# Columnes del fitxer
columnes = ["EMA", "DATA", "X", "Y", "PPT"]

# Comptadors
files_llegides = 0
files_escrites = 0
files_saltades = 0

# Assegurem que la carpeta de resultats existeix
ensure_dir(RESULTATS_DIR)

# Obrim fitxers d'entrada i sortida
with open_csv_reader(PAS2B_OUT, encoding="utf-8") as lector, \
     open_csv_writer(PAS3_OUT, fieldnames=columnes) as escriptor:

    for fila in lector:
        files_llegides += 1  # Comptem la fila

        # Convertim la data
        data = parse_date(fila.get("DATA"))

        # Si la data no és vàlida, saltem la fila
        if data is None:
            files_saltades += 1
            # Comentari: saltem la fila perquè la data no és vàlida
            continue

        # Creem la nova fila amb la data en format ISO
        nova_fila = dict(fila)
        nova_fila["DATA"] = data.isoformat()

        escriptor.writerow(nova_fila)  # Escrivim la fila
        files_escrites += 1

# Mostrem un preview del resultat
preview_csv(PAS3_OUT, max_rows=5, title="Preview meteocat_pas3.csv")

# Missatges finals
print(f"OK -> creat {PAS3_OUT}")
print(f"Files llegides: {files_llegides}")
print(f"Files escrites: {files_escrites}")
print(f"Files saltades (data invàlida): {files_saltades}")
