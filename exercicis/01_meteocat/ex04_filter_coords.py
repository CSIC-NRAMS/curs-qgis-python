# OBJECTIU:
#   Filtrar les files que no tenen coordenades X/Y vàlides.
#
# ENTRADA:
#   ./resultats/meteocat_pas2a.csv
#
# SORTIDA:
#   ./resultats/meteocat_pas2b.csv
#
# QUÈ APRENEM:
#   - Separar el filtre de la conversió de números.
#   - Saltar files amb dades mancants.
#   - Veure un preview del resultat net.

import os  # Mòdul per gestionar rutes
import sys  # Mòdul per ajustar el path d'importació

# Afegim la carpeta arrel del projecte al sys.path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

# Importem configuració i utilitats
from utils.config import PAS2A_OUT, PAS2B_OUT, RESULTATS_DIR  # Rutes centralitzades
from utils.csv_utils import ensure_dir, open_csv_reader, open_csv_writer, preview_csv

# Columnes del fitxer
columnes = ["EMA", "DATA", "X", "Y", "PPT"]

# Comptadors
files_llegides = 0
files_escrites = 0
files_saltades = 0

# Assegurem que la carpeta de resultats existeix
ensure_dir(RESULTATS_DIR)

# Obrim fitxers d'entrada i sortida
with open_csv_reader(PAS2A_OUT, encoding="utf-8") as lector, \
     open_csv_writer(PAS2B_OUT, fieldnames=columnes) as escriptor:

    for fila in lector:
        files_llegides += 1  # Comptem la fila

        # Llegim X i Y tal com venen del pas anterior
        x = fila.get("X")
        y = fila.get("Y")

        # Si falta X o Y, saltem la fila
        if x in (None, "") or y in (None, ""):
            files_saltades += 1
            # Comentari: saltem la fila perquè no tenim coordenades vàlides
            continue

        # Escrivim la fila neta
        escriptor.writerow(fila)
        files_escrites += 1

# Mostrem un preview de l'output net
preview_csv(PAS2B_OUT, max_rows=5, title="Preview meteocat_pas2b.csv")

# Missatges finals
print(f"OK -> creat {PAS2B_OUT}")
print(f"Files llegides: {files_llegides}")
print(f"Files escrites: {files_escrites}")
print(f"Files saltades (X o Y buits): {files_saltades}")
