# OBJECTIU:
#   Crear/actualitzar el GeoPackage final de risc amb totes les capes.
#
# ENTRADA:
#   - resultats/precipitacio_olot_estandarditzada.gpkg (capa base)
#   - capes de risc (si existeixen) al risc_precipitacio_olot.gpkg
#
# SORTIDA:
#   resultats/risc_precipitacio_olot.gpkg amb totes les capes de risc.
#
# QUÈ APRENEM:
#   - Consolidar capes en un sol GeoPackage.
#   - Validar CRS i camps clau.
#   - Generar un resum final del paquet.

import os  # Per gestionar rutes
import sys  # Per ajustar el path d'importació
from datetime import datetime  # Per timestamps del resum

# Afegim la carpeta arrel del projecte al sys.path
ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

# Imports de QGIS
from qgis.core import QgsVectorLayer, QgsProject

# Importem configuració i utilitats
from utils.config import (
    MERGED_STD_OUT, GPKG_OUT, GPKG_LAYER, RESULTATS_DIR,
    RISC_GPKG_OUT, HEATMAP_OUT_TIF,
    RISC_LAYER_POINTS, RISC_LAYER_ALERTA_20, RISC_LAYER_ALERTA_40, RISC_LAYER_ALERTA_80,
    RISC_LAYER_EPISODIS_20, RISC_LAYER_RESUM_20, RISC_LAYER_HOTSPOTS_40
)
from utils.csv_utils import ensure_dir
from utils.processing_utils import extract_by_expression, export_layer_to_gpkg

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

# Carreguem la capa base
base_layer = load_base_points_layer()
if base_layer is None:
    print("ERROR -> No s'ha pogut carregar la capa base de precipitació.")
else:
    # Exportem la capa base al GPKG de risc
    export_layer_to_gpkg(base_layer, RISC_GPKG_OUT, RISC_LAYER_POINTS)
    QgsProject.instance().addMapLayer(base_layer)

    # Generem capes per llindars
    layers_exportades = [RISC_LAYER_POINTS]

    for thresh, layer_name in [(20, RISC_LAYER_ALERTA_20), (40, RISC_LAYER_ALERTA_40), (80, RISC_LAYER_ALERTA_80)]:
        expr = f"\"precip_mm\" >= {thresh}"
        alert_layer = extract_by_expression(base_layer, expr)
        export_layer_to_gpkg(alert_layer, RISC_GPKG_OUT, layer_name)
        QgsProject.instance().addMapLayer(alert_layer)
        layers_exportades.append(layer_name)

    # Carreguem episodis si existeixen (sinó avisem)
    uri_episodis = f"{RISC_GPKG_OUT}|layername={RISC_LAYER_EPISODIS_20}"
    episodis_layer = QgsVectorLayer(uri_episodis, "episodis_alerta_20mm", "ogr")
    if episodis_layer.isValid():
        export_layer_to_gpkg(episodis_layer, RISC_GPKG_OUT, RISC_LAYER_EPISODIS_20)
        QgsProject.instance().addMapLayer(episodis_layer)
        layers_exportades.append(RISC_LAYER_EPISODIS_20)
    else:
        print("AVÍS -> No s'ha trobat episodis_alerta_20mm. Executa ex16 si cal.")

    # Carreguem resum d'episodis si existeix
    uri_resum = f"{RISC_GPKG_OUT}|layername={RISC_LAYER_RESUM_20}"
    resum_layer = QgsVectorLayer(uri_resum, "episodis_resum_20mm", "ogr")
    if resum_layer.isValid():
        export_layer_to_gpkg(resum_layer, RISC_GPKG_OUT, RISC_LAYER_RESUM_20)
        QgsProject.instance().addMapLayer(resum_layer)
        layers_exportades.append(RISC_LAYER_RESUM_20)
    else:
        print("AVÍS -> No s'ha trobat episodis_resum_20mm. Executa ex17 si cal.")

    # Hotspots (raster extern)
    if os.path.exists(HEATMAP_OUT_TIF):
        print(f"OK -> Raster hotspots disponible: {HEATMAP_OUT_TIF}")
    else:
        print("AVÍS -> No s'ha trobat hotspots_heatmap_40mm.tif. Executa ex18 si cal.")

    # Validació bàsica de CRS
    if base_layer.crs().authid() != "EPSG:4326":
        print("AVÍS -> La capa base no és EPSG:4326.")

    # Resum final
    print("\nRESUM FINAL DEL PAQUET DE RISC")
    print("GeoPackage:", RISC_GPKG_OUT)
    print("Capes exportades:")
    for name in layers_exportades:
        print("-", name)
    print("Timestamp:", datetime.now().isoformat())
