"""Ex02 — Selecció de columnes clau.

Fa: crea un CSV més petit amb camps essencials.
Llegeix: METEOCAT_INPUT
Escriu: PAS1_OUT (meteocat_pas1.csv)
OK esperat: missatge d'OK i preview del pas 1.
"""

import os
import sys

# (Ja explicat abans) Preparem l'import del paquet tools.
ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from tools.config import METEOCAT_INPUT, PAS1_OUT, RESULTATS_DIR
from tools.csv_utils import ensure_dir, open_csv_reader, open_csv_writer, preview_csv

# Ens assegurem que la carpeta de sortida existeix.
ensure_dir(RESULTATS_DIR)
columnes = ["EMA", "DATA", "X", "Y", "PPT"]
files = 0

with open_csv_reader(METEOCAT_INPUT) as lector, \
     open_csv_writer(PAS1_OUT, fieldnames=columnes) as escriptor:

    # Recorrem cada fila i creem una nova fila amb nomes les columnes clau.
    for fila in lector:
        nova_fila = {col: fila.get(col, "") for col in columnes}
        escriptor.writerow(nova_fila)
        files += 1

preview_csv(PAS1_OUT, max_rows=5, title="Preview meteocat_pas1.csv")
print(f"OK -> creat {PAS1_OUT}")
print(f"Files processades: {files}")
