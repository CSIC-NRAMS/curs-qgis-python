# OBJECTIU:
#   Crear capes de dies d’alerta per llindars de precipitació (20, 40, 80 mm).
#
# ENTRADA:
#   resultats/precipitacio_olot_estandarditzada.gpkg (capa de punts) o CSV unificat.
#
# SORTIDA:
#   resultats/risc_precipitacio_olot.gpkg amb capes:
#   - dies_alerta_20mm
#   - dies_alerta_40mm
#   - dies_alerta_80mm
#
# QUÈ APRENEM:
#   - Carregar capes i filtrar per expressió.
#   - Generar capes de risc per llindars.
#   - Exportar capes a GeoPackage.

import os  # Per gestionar rutes
import sys  # Per ajustar el path d'importació

# Afegim la carpeta arrel del projecte al sys.path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

# Imports de QGIS
from qgis.core import QgsVectorLayer, QgsProject

# Importem configuració i utilitats
from utils.config import (
    MERGED_STD_OUT, GPKG_OUT, GPKG_LAYER, RESULTATS_DIR,
    RISC_GPKG_OUT, RISC_LAYER_ALERTA_20, RISC_LAYER_ALERTA_40, RISC_LAYER_ALERTA_80
)
from utils.csv_utils import ensure_dir
from utils.processing_utils import extract_by_expression, export_layer_to_gpkg

# Assegurem la carpeta de resultats
ensure_dir(RESULTATS_DIR)

# Funció per carregar la capa base de punts
def load_base_points_layer():
    # Primer intent: carregar del GeoPackage final
    if os.path.exists(GPKG_OUT):
        uri = f"{GPKG_OUT}|layername={GPKG_LAYER}"
        layer = QgsVectorLayer(uri, "precip_std_points", "ogr")
        if layer.isValid():
            return layer

    # Segon intent: carregar del CSV unificat
    if os.path.exists(MERGED_STD_OUT):
        uri = f"file:///{MERGED_STD_OUT}?delimiter=,&xField=lon&yField=lat&crs=EPSG:4326"
        layer = QgsVectorLayer(uri, "precip_std_points", "delimitedtext")
        if layer.isValid():
            return layer

    # Si no hem pogut carregar res, retornem None
    return None

# Carreguem la capa base
base_layer = load_base_points_layer()
if base_layer is None:
    print("ERROR -> No s'ha trobat cap capa base (GPKG o CSV).")
else:
    # Afegim la capa base al projecte (opcional, per visualitzar-la)
    QgsProject.instance().addMapLayer(base_layer)

    # Llista de llindars i noms de capa
    thresholds = [
        (20, RISC_LAYER_ALERTA_20),
        (40, RISC_LAYER_ALERTA_40),
        (80, RISC_LAYER_ALERTA_80)
    ]

    # Comptadors
    files_llegides = base_layer.featureCount()

    for thresh, layer_name in thresholds:
        # Definim l’expressió de filtre
        expr = f"\"precip_mm\" >= {thresh}"

        # Generem la capa filtrada amb Processing
        alert_layer = extract_by_expression(base_layer, expr)

        # Comptem files filtrades
        files_filtrades = alert_layer.featureCount()

        # Exportem la capa al GPKG de risc
        export_layer_to_gpkg(alert_layer, RISC_GPKG_OUT, layer_name)

        # Afegim la capa al projecte
        QgsProject.instance().addMapLayer(alert_layer)

        # Missatge per capa
        print(f"OK -> Capa {layer_name} creada (llindar {thresh} mm)")
        print(f"   Files filtrades: {files_filtrades}")

    # Resum final
    print(f"Files llegides (base): {files_llegides}")
    print(f"OK -> GeoPackage risc creat/actualitzat: {RISC_GPKG_OUT}")
