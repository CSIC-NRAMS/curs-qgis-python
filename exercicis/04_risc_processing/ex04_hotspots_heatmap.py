# OBJECTIU:
#   Generar un heatmap de dies d’alerta >= 40 mm i afegir-lo al projecte.
#
# ENTRADA:
#   resultats/risc_precipitacio_olot.gpkg (capa dies_alerta_40mm)
#
# SORTIDA:
#   resultats/hotspots_heatmap_40mm.tif (raster) o capa vectorial de grid com a alternativa.
#
# QUÈ APRENEM:
#   - Fer un heatmap amb Processing.
#   - Entendre hotspots com zones de recurrència de precipitació intensa.
#   - Afegir raster o vector al projecte.

import os  # Per gestionar rutes
import sys  # Per ajustar el path d'importació

# Afegim la carpeta arrel del projecte al sys.path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

# Imports de QGIS
from qgis.core import QgsVectorLayer, QgsProject, QgsRasterLayer

# Importem configuració i utilitats
from utils.config import (
    MERGED_STD_OUT, GPKG_OUT, GPKG_LAYER, RESULTATS_DIR,
    RISC_GPKG_OUT, RISC_LAYER_ALERTA_40, RISC_LAYER_HOTSPOTS_40, HEATMAP_OUT_TIF
)
from utils.csv_utils import ensure_dir
from utils.processing_utils import run_processing_algorithm, extract_by_expression, export_layer_to_gpkg

# Assegurem la carpeta de resultats
ensure_dir(RESULTATS_DIR)

# Funció per carregar la capa base de punts
def load_base_points_layer():
    if os.path.exists(GPKG_OUT):
        uri = f"{GPKG_OUT}|layername={GPKG_LAYER}"
        layer = QgsVectorLayer(uri, "precip_std_points", "ogr")
        if layer.isValid():
            return layer
    if os.path.exists(MERGED_STD_OUT):
        uri = f"file:///{MERGED_STD_OUT}?delimiter=,&xField=lon&yField=lat&crs=EPSG:4326"
        layer = QgsVectorLayer(uri, "precip_std_points", "delimitedtext")
        if layer.isValid():
            return layer
    return None

# Funció per carregar o crear la capa de dies d’alerta 40 mm
def load_or_create_alerta_40():
    if os.path.exists(RISC_GPKG_OUT):
        uri = f"{RISC_GPKG_OUT}|layername={RISC_LAYER_ALERTA_40}"
        layer = QgsVectorLayer(uri, "dies_alerta_40mm", "ogr")
        if layer.isValid():
            return layer

    base_layer = load_base_points_layer()
    if base_layer is None:
        return None

    expr = "\"precip_mm\" >= 40"
    alert_layer = extract_by_expression(base_layer, expr)
    export_layer_to_gpkg(alert_layer, RISC_GPKG_OUT, RISC_LAYER_ALERTA_40)
    return alert_layer

# Carreguem la capa d’alerta 40 mm
alert_layer = load_or_create_alerta_40()
if alert_layer is None:
    print("ERROR -> No s'ha pogut obtenir la capa dies_alerta_40mm.")
else:
    # Intent principal: generar heatmap raster amb Processing
    try:
        params = {
            "INPUT": alert_layer,
            "RADIUS": 0.02,  # unitats del CRS (graus, perquè estem en EPSG:4326)
            "PIXEL_SIZE": 0.002,
            "WEIGHT_FIELD": "precip_mm",
            "KERNEL": 0,
            "DECAY": 0,
            "OUTPUT": HEATMAP_OUT_TIF
        }

        # Algoritme de heatmap (pot variar segons la versió de QGIS)
        run_processing_algorithm("native:heatmap", params)

        # Afegim el raster al projecte
        raster = QgsRasterLayer(HEATMAP_OUT_TIF, "hotspots_heatmap_40mm")
        if raster.isValid():
            QgsProject.instance().addMapLayer(raster)
            print(f"OK -> Heatmap raster creat: {HEATMAP_OUT_TIF}")
        else:
            print("AVÍS -> Heatmap creat però no s'ha pogut carregar al projecte.")

    except Exception as exc:
        # Alternativa: crear grid i comptar punts
        print(f"AVÍS -> Heatmap raster no disponible ({exc}).")
        print("Alternativa -> Creem un grid i comptem punts per cel·la.")

        # Extensió de la capa
        extent = alert_layer.extent()
        extent_str = f"{extent.xMinimum()},{extent.xMaximum()},{extent.yMinimum()},{extent.yMaximum()}"

        # Creem un grid
        grid = run_processing_algorithm(
            "native:creategrid",
            {
                "TYPE": 2,
                "EXTENT": extent_str,
                "HSPACING": 0.01,
                "VSPACING": 0.01,
                "HOVERLAY": 0,
                "VOVERLAY": 0,
                "CRS": alert_layer.crs(),
                "OUTPUT": "memory:"
            }
        )["OUTPUT"]

        # Comptem punts dins de cada cel·la
        grid_count = run_processing_algorithm(
            "native:countpointsinpolygon",
            {
                "POLYGONS": grid,
                "POINTS": alert_layer,
                "FIELD": "n_points",
                "OUTPUT": "memory:"
            }
        )["OUTPUT"]

        # Exportem la capa de hotspots vectorials al GPKG
        export_layer_to_gpkg(grid_count, RISC_GPKG_OUT, RISC_LAYER_HOTSPOTS_40)
        QgsProject.instance().addMapLayer(grid_count)

        print(f"OK -> Hotspots vectorial creat: {RISC_LAYER_HOTSPOTS_40}")
