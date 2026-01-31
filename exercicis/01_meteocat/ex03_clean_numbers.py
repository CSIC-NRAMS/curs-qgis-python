# OBJECTIU:
#   Convertir X, Y i PPT a float (sense filtrar encara).
#
# ENTRADA:
#   ./resultats/meteocat_pas1.csv
#
# SORTIDA:
#   ./resultats/meteocat_pas2a.csv
#
# QUÈ APRENEM:
#   - Reutilitzar to_float per netejar números.
#   - Separar el "parseig" de la validació.
#   - Veure un preview del resultat parcial.

import os  # Mòdul per gestionar rutes
import sys  # Mòdul per ajustar el path d'importació

# Afegim la carpeta arrel del projecte al sys.path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

# Importem configuració i utilitats
from utils.config import PAS1_OUT, PAS2A_OUT, RESULTATS_DIR  # Rutes centralitzades
from utils.csv_utils import ensure_dir, open_csv_reader, open_csv_writer, preview_csv
from utils.parse_utils import to_float  # Funció reutilitzable de conversió

# Columnes del fitxer
columnes = ["EMA", "DATA", "X", "Y", "PPT"]

# Comptadors
files_llegides = 0
files_escrites = 0

# Assegurem que la carpeta de resultats existeix
ensure_dir(RESULTATS_DIR)

# Obrim fitxers d'entrada i sortida
with open_csv_reader(PAS1_OUT, encoding="utf-8") as lector, \
     open_csv_writer(PAS2A_OUT, fieldnames=columnes) as escriptor:

    for fila in lector:
        files_llegides += 1  # Comptem la fila

        # Convertim X, Y i PPT a float (encara podem tenir None)
        x = to_float(fila.get("X"))
        y = to_float(fila.get("Y"))
        ppt = to_float(fila.get("PPT"))

        # Creem la nova fila amb valors convertits
        nova_fila = {
            "EMA": fila.get("EMA", ""),
            "DATA": fila.get("DATA", ""),
            "X": x,
            "Y": y,
            "PPT": ppt
        }

        escriptor.writerow(nova_fila)  # Escrivim la fila
        files_escrites += 1

# Mostrem un preview de l'output parcial
preview_csv(PAS2A_OUT, max_rows=5, title="Preview meteocat_pas2a.csv")

# Missatges finals
print(f"OK -> creat {PAS2A_OUT}")
print(f"Files llegides: {files_llegides}")
print(f"Files escrites: {files_escrites}")
