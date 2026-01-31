# OBJECTIU:
#   Carregar capes del GPKG base i del GPKG de risc i organitzar-les en grups.
#
# ENTRADA:
#   resultats/precipitacio_olot_estandarditzada.gpkg
#   resultats/risc_precipitacio_olot.gpkg
#
# SORTIDA:
#   (Opcional) resultats/risc_project.qgz
#
# QUÈ APRENEM:
#   - Afegir capes al projecte.
#   - Crear grups al Layer Tree.
#   - Guardar un projecte QGIS.

import os  # Per gestionar rutes
import sys  # Per ajustar el path d'importació

# Afegim la carpeta arrel del projecte al sys.path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from qgis.core import QgsProject, QgsRasterLayer  # Imports de QGIS

from utils.config import (
    RESULTATS_DIR, GPKG_OUT, GPKG_LAYER, RISC_GPKG_OUT, HEATMAP_OUT_TIF,
    RISC_LAYER_ALERTA_20, RISC_LAYER_ALERTA_40, RISC_LAYER_ALERTA_80,
    RISC_LAYER_EPISODIS_20, RISC_LAYER_RESUM_20, QGZ_OUT
)
from utils.csv_utils import ensure_dir
from utils.gui_utils import load_vector_layer_gpkg, add_layer_to_group, save_project_if_needed

# Assegurem la carpeta de resultats
ensure_dir(RESULTATS_DIR)

project = QgsProject.instance()

# Grup 00 Base
base_layer = load_vector_layer_gpkg(GPKG_OUT, GPKG_LAYER, name="base_points")
if base_layer is None:
    print("ERROR -> No s'ha pogut carregar la capa base del GPKG.")
else:
    base_layer.setName("base_points")
    add_layer_to_group(base_layer, "00 Base")

# Grup 10 Alertes
for layer_name, short_name in [
    (RISC_LAYER_ALERTA_20, "alerta_20mm"),
    (RISC_LAYER_ALERTA_40, "alerta_40mm"),
    (RISC_LAYER_ALERTA_80, "alerta_80mm")
]:
    layer = load_vector_layer_gpkg(RISC_GPKG_OUT, layer_name, name=short_name)
    if layer is None:
        print(f"AVÍS -> No s'ha trobat {layer_name}.")
    else:
        layer.setName(short_name)
        add_layer_to_group(layer, "10 Alertes")

# Grup 20 Episodis
for layer_name, short_name in [
    (RISC_LAYER_EPISODIS_20, "episodis_20mm"),
    (RISC_LAYER_RESUM_20, "resum_episodis_20mm")
]:
    layer = load_vector_layer_gpkg(RISC_GPKG_OUT, layer_name, name=short_name)
    if layer is None:
        print(f"AVÍS -> No s'ha trobat {layer_name}.")
    else:
        layer.setName(short_name)
        add_layer_to_group(layer, "20 Episodis")

# Grup 30 Hotspots (raster)
if os.path.exists(HEATMAP_OUT_TIF):
    raster = QgsRasterLayer(HEATMAP_OUT_TIF, "hotspots_40mm")
    if raster.isValid():
        add_layer_to_group(raster, "30 Hotspots")
        print("OK -> Heatmap afegit al projecte.")
    else:
        print("AVÍS -> Heatmap existent però no s'ha pogut carregar.")
else:
    print("AVÍS -> No s'ha trobat el raster de hotspots.")

# Guardem el projecte com a fitxer QGZ
save_project_if_needed(QGZ_OUT)
print(f"OK -> Projecte guardat: {QGZ_OUT}")
