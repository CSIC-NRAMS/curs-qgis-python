# OBJECTIU:
#   Seleccionar features per expressió i exportar la selecció.
#
# ENTRADA:
#   resultats/precipitacio_olot_estandarditzada.gpkg (capa base)
#
# SORTIDA:
#   resultats/risc_precipitacio_olot.gpkg (capa seleccio_aemet_40mm)
#   resultats/seleccio_aemet_40mm.csv
#
# QUÈ APRENEM:
#   - Fer seleccions per expressió.
#   - Exportar seleccions a GPKG i CSV.

import os  # Per gestionar rutes
import sys  # Per ajustar el path d'importació

# Afegim la carpeta arrel del projecte al sys.path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from qgis.core import QgsVectorLayer

from utils.config import (
    GPKG_OUT, GPKG_LAYER, RESULTATS_DIR, RISC_GPKG_OUT,
    RISC_LAYER_SELECCIO_AEMET_40, SELECCIO_AEMET_40_CSV
)
from utils.csv_utils import ensure_dir
from utils.gui_utils import export_selected_to_gpkg, export_selected_to_csv

# Assegurem la carpeta de resultats
ensure_dir(RESULTATS_DIR)

# Carreguem la capa base
uri = f"{GPKG_OUT}|layername={GPKG_LAYER}"
layer = QgsVectorLayer(uri, "base_points", "ogr")

if not layer.isValid():
    print("ERROR -> No s'ha pogut carregar la capa base.")
else:
    # Selecció per expressió
    expr = "\"precip_mm\" >= 40 AND \"source\" = 'AEMET'"
    layer.selectByExpression(expr)

    selected_count = layer.selectedFeatureCount()
    print(f"Seleccionades: {selected_count}")

    if selected_count == 0:
        print("AVÍS -> Cap feature seleccionada.")
    else:
        # Exportem la selecció a GPKG
        export_selected_to_gpkg(layer, RISC_GPKG_OUT, RISC_LAYER_SELECCIO_AEMET_40)
        print(f"OK -> Capa selecció exportada: {RISC_LAYER_SELECCIO_AEMET_40}")

        # Exportem la selecció a CSV
        export_selected_to_csv(layer, SELECCIO_AEMET_40_CSV)
        print(f"OK -> CSV selecció exportat: {SELECCIO_AEMET_40_CSV}")
