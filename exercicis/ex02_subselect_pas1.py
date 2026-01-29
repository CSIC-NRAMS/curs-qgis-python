# OBJECTIU:
#   Crear un CSV nou amb només EMA, DATA, X, Y, PPT.
#
# ENTRADA:
#   ./dades/Precipitació_Olot_METEOCAT.csv
#
# SORTIDA:
#   ./resultats/meteocat_pas1.csv
#
# QUÈ APRENEM:
#   - Seleccionar columnes d'un CSV.
#   - Escriure un CSV amb utilitats reutilitzables.
#   - Crear una carpeta de sortida si no existeix.

import os  # Mòdul per gestionar rutes
import sys  # Mòdul per ajustar el path d'importació

# Afegim la carpeta arrel del projecte al sys.path
ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

# Importem configuració i utilitats
from utils.config import METEOCAT_INPUT, PAS1_OUT, RESULTATS_DIR  # Rutes centralitzades
from utils.csv_utils import ensure_dir, open_csv_reader, open_csv_writer, preview_csv

# Assegurem que la carpeta de resultats existeix
ensure_dir(RESULTATS_DIR)

# Definim les columnes que volem conservar
columnes = ["EMA", "DATA", "X", "Y", "PPT"]

# Comptador de files
files = 0

# Obrim el CSV d'entrada i el CSV de sortida amb utilitats reutilitzables
with open_csv_reader(METEOCAT_INPUT) as lector, \
     open_csv_writer(PAS1_OUT, fieldnames=columnes) as escriptor:

    for fila in lector:
        # Creem una nova fila només amb les columnes desitjades
        nova_fila = {col: fila.get(col, "") for col in columnes}
        # Escrivim la nova fila
        escriptor.writerow(nova_fila)
        # Incrementem el comptador
        files += 1

# Mostrem un preview de l'output per veure el resultat
preview_csv(PAS1_OUT, max_rows=5, title="Preview meteocat_pas1.csv")

# Missatges finals
print(f"OK -> creat {PAS1_OUT}")
print(f"Files processades: {files}")
