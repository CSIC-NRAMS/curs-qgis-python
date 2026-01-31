# OBJECTIU:
#   Passar d'un format mensual (P1..P31) a format diari (una fila per dia).
#
# ENTRADA:
#   ./dades/entrada/Precipitació_Olot_AEMET.csv
#
# SORTIDA:
#   ./resultats/aemet_pas1_long.csv
#
# QUÈ APRENEM:
#   - Recorre columnes dinàmiques (P1..P31).
#   - Crear files noves a partir d'una sola fila.
#   - Generar un dataset "long" (despivotat).

import os  # Per gestionar rutes
import sys  # Per ajustar el path d'importació

# Afegim la carpeta arrel del projecte al sys.path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

# Importem configuració i utilitats
from utils.config import AEMET_INPUT, AEMET_PAS1_OUT, RESULTATS_DIR
from utils.csv_utils import ensure_dir, open_csv_reader, open_csv_writer, preview_csv

# Columnes de sortida
columnes = [
    "INDICATIVO", "NOMBRE", "ALTITUD", "LONGITUD", "LATITUD",
    "AÑO", "MES", "DAY", "P_TENTHS"
]

# Comptadors
files_llegides = 0
files_escrites = 0
files_saltades = 0

# Assegurem la carpeta de resultats
ensure_dir(RESULTATS_DIR)

# Obrim CSV d'entrada i sortida
with open_csv_reader(AEMET_INPUT) as lector, \
     open_csv_writer(AEMET_PAS1_OUT, fieldnames=columnes) as escriptor:

    # Detectem les columnes P1..P31 a partir de la capçalera
    p_cols = [c for c in lector.fieldnames if c.startswith("P") and c[1:].isdigit()]

    for fila in lector:
        files_llegides += 1

        # Recorrem totes les columnes de precipitació diària
        for col in p_cols:
            # Obtenim el valor de precipitació
            val = fila.get(col)

            # Si el valor és buit, saltem aquesta fila diària
            if val is None or str(val).strip() == "":
                files_saltades += 1
                # Comentari: no hi ha dada per aquest dia
                continue

            # Dia del mes (P1 -> 1, P2 -> 2, ...)
            day_num = int(col.replace("P", ""))

            # Construïm la nova fila "long"
            nova_fila = {
                "INDICATIVO": fila.get("INDICATIVO", ""),
                "NOMBRE": fila.get("NOMBRE", ""),
                "ALTITUD": fila.get("ALTITUD", ""),
                "LONGITUD": fila.get("LONGITUD", ""),
                "LATITUD": fila.get("LATITUD", ""),
                "AÑO": fila.get("AÑO", ""),
                "MES": fila.get("MES", ""),
                "DAY": day_num,
                "P_TENTHS": val
            }

            # Escrivim la fila
            escriptor.writerow(nova_fila)
            files_escrites += 1

# Preview del resultat
preview_csv(AEMET_PAS1_OUT, max_rows=5, title="Preview aemet_pas1_long.csv")

# Missatges finals
print(f"OK -> creat {AEMET_PAS1_OUT}")
print(f"Files llegides: {files_llegides}")
print(f"Files escrites: {files_escrites}")
print(f"Files saltades (dies buits): {files_saltades}")
