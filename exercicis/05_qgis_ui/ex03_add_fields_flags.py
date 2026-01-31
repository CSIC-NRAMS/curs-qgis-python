# OBJECTIU:
#   Afegir camps de bandera d’alerta al layer base i exportar-lo.
#
# ENTRADA:
#   resultats/precipitacio_olot_estandarditzada.gpkg (capa base)
#
# SORTIDA:
#   resultats/risc_precipitacio_olot.gpkg (capa punts_base_flags)
#
# QUÈ APRENEM:
#   - Afegir camps nous.
#   - Actualitzar valors amb changeAttributeValue.
#   - Exportar una capa modificada.

import os  # Per gestionar rutes
import sys  # Per ajustar el path d'importació

# Afegim la carpeta arrel del projecte al sys.path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from qgis.core import QgsVectorLayer, QgsField, QgsFeature, QgsFields
from qgis.PyQt.QtCore import QVariant

from utils.config import GPKG_OUT, GPKG_LAYER, RESULTATS_DIR, RISC_GPKG_OUT, RISC_LAYER_BASE_FLAGS
from utils.csv_utils import ensure_dir
from utils.processing_utils import export_layer_to_gpkg
from utils.parse_utils import to_float

# Assegurem la carpeta de resultats
ensure_dir(RESULTATS_DIR)

# Carreguem la capa base
uri = f"{GPKG_OUT}|layername={GPKG_LAYER}"
layer = QgsVectorLayer(uri, "base_points", "ogr")

if not layer.isValid():
    print("ERROR -> No s'ha pogut carregar la capa base.")
else:
    # Creem una capa en memòria per no tocar l’original
    out_layer = QgsVectorLayer("Point?crs=EPSG:4326", "punts_base_flags", "memory")
    new_fields = QgsFields()
    for f in layer.fields():
        new_fields.append(f)

    # Afegim els nous camps
    new_fields.append(QgsField("alert_level", QVariant.String))
    new_fields.append(QgsField("is_extreme", QVariant.Int))

    out_layer.dataProvider().addAttributes(new_fields)
    out_layer.updateFields()

    # Copiem features amb els camps calculats
    for feat in layer.getFeatures():
        precip = to_float(feat["precip_mm"])
        if precip is None:
            level = "BAIX"
        elif precip < 20:
            level = "BAIX"
        elif precip < 40:
            level = "MIG"
        else:
            level = "ALT"

        is_extreme = 1 if (precip is not None and precip >= 80) else 0

        new_feat = QgsFeature(out_layer.fields())
        new_feat.setGeometry(feat.geometry())
        new_feat.setAttributes(feat.attributes() + [level, is_extreme])
        out_layer.dataProvider().addFeature(new_feat)

    # Exportem la capa al GPKG de risc
    export_layer_to_gpkg(out_layer, RISC_GPKG_OUT, RISC_LAYER_BASE_FLAGS)

    print(f"OK -> Capa creada: {RISC_LAYER_BASE_FLAGS}")
    print(f"OK -> Exportada a: {RISC_GPKG_OUT}")
