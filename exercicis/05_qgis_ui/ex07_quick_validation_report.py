# OBJECTIU:
#   Generar un report ràpid de qualitat de dades.
#
# ENTRADA:
#   resultats/precipitacio_olot_estandarditzada.gpkg (capa base)
#
# SORTIDA:
#   resultats/validation_report.txt
#
# QUÈ APRENEM:
#   - Comprovar buits, duplicats i rangs.
#   - Escriure un report simple per a QA/QC.

import os  # Per gestionar rutes
import sys  # Per ajustar el path d'importació

# Afegim la carpeta arrel del projecte al sys.path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from qgis.core import QgsVectorLayer

from utils.config import GPKG_OUT, GPKG_LAYER, RESULTATS_DIR, VALIDATION_REPORT_OUT
from utils.csv_utils import ensure_dir
from utils.parse_utils import to_float

# Assegurem la carpeta de resultats
ensure_dir(RESULTATS_DIR)

# Carreguem la capa base
uri = f"{GPKG_OUT}|layername={GPKG_LAYER}"
layer = QgsVectorLayer(uri, "base_points", "ogr")

if not layer.isValid():
    print("ERROR -> No s'ha pogut carregar la capa base.")
else:
    total = 0
    missing_precip = 0
    min_precip = None
    max_precip = None
    dup_key_counts = {}

    # Extent esperat (usarem l’extent actual, però el reduïm un 1% per detectar outliers)
    extent = layer.extent()
    dx = (extent.xMaximum() - extent.xMinimum()) * 0.01
    dy = (extent.yMaximum() - extent.yMinimum()) * 0.01
    xmin = extent.xMinimum() + dx
    xmax = extent.xMaximum() - dx
    ymin = extent.yMinimum() + dy
    ymax = extent.yMaximum() - dy

    out_of_bbox = 0

    for feat in layer.getFeatures():
        total += 1

        # Precipitació
        p = to_float(feat["precip_mm"])
        if p is None:
            missing_precip += 1
        else:
            min_precip = p if min_precip is None else min(min_precip, p)
            max_precip = p if max_precip is None else max(max_precip, p)

        # Duplicats per (station_id, date, source)
        key = (feat["station_id"], feat["date"], feat["source"])
        dup_key_counts[key] = dup_key_counts.get(key, 0) + 1

        # Outliers fora bbox esperat
        geom = feat.geometry()
        if geom is None or geom.isEmpty():
            continue
        pt = geom.asPoint()
        if not (xmin <= pt.x() <= xmax and ymin <= pt.y() <= ymax):
            out_of_bbox += 1

    # Comptem duplicats
    duplicates = sum(1 for k, v in dup_key_counts.items() if v > 1)

    # Escrivim report
    with open(VALIDATION_REPORT_OUT, "w", encoding="utf-8") as f:
        f.write("REPORT DE VALIDACIÓ\n")
        f.write("====================\n")
        f.write(f"Total de punts: {total}\n")
        f.write(f"Precipitació buida/no numèrica: {missing_precip}\n")
        f.write(f"Precipitació mínima: {min_precip}\n")
        f.write(f"Precipitació màxima: {max_precip}\n")
        f.write(f"Claus duplicades (station_id, date, source): {duplicates}\n")
        f.write(f"Punts fora bbox esperat: {out_of_bbox}\n")
        f.write("\nNota: el bbox esperat s'ha calculat reduint un 1% l’extent actual.\n")

    print(f"OK -> Report creat: {VALIDATION_REPORT_OUT}")
