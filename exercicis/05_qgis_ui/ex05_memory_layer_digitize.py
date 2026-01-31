# OBJECTIU:
#   Crear una capa de memòria (polígons) com a zona d’estudi i exportar-la.
#
# ENTRADA:
#   resultats/precipitacio_olot_estandarditzada.gpkg (capa base)
#
# SORTIDA:
#   resultats/risc_precipitacio_olot.gpkg (capa zona_estudi)
#
# QUÈ APRENEM:
#   - Crear una capa des de zero.
#   - Afegir geometria i camps.
#   - Exportar a GeoPackage.

import os  # Per gestionar rutes
import sys  # Per ajustar el path d'importació
from datetime import datetime  # Per timestamps

# Afegim la carpeta arrel del projecte al sys.path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from qgis.core import QgsVectorLayer, QgsField, QgsFeature, QgsGeometry, QgsPointXY, QgsFields
from qgis.PyQt.QtCore import QVariant

from utils.config import GPKG_OUT, GPKG_LAYER, RESULTATS_DIR, RISC_GPKG_OUT, RISC_LAYER_ZONA_ESTUDI
from utils.csv_utils import ensure_dir
from utils.processing_utils import export_layer_to_gpkg

# Assegurem la carpeta de resultats
ensure_dir(RESULTATS_DIR)

# Carreguem la capa base per obtenir l’extent
uri = f"{GPKG_OUT}|layername={GPKG_LAYER}"
base_layer = QgsVectorLayer(uri, "base_points", "ogr")

if not base_layer.isValid():
    print("ERROR -> No s'ha pogut carregar la capa base.")
else:
    extent = base_layer.extent()

    # Expandim l’extent un 10% per fer la zona d’estudi
    dx = (extent.xMaximum() - extent.xMinimum()) * 0.1
    dy = (extent.yMaximum() - extent.yMinimum()) * 0.1

    xmin = extent.xMinimum() - dx
    xmax = extent.xMaximum() + dx
    ymin = extent.yMinimum() - dy
    ymax = extent.yMaximum() + dy

    # Creem el polígon rectangular
    ring = [
        QgsPointXY(xmin, ymin),
        QgsPointXY(xmax, ymin),
        QgsPointXY(xmax, ymax),
        QgsPointXY(xmin, ymax),
        QgsPointXY(xmin, ymin)
    ]

    # Capa de memòria
    out_layer = QgsVectorLayer("Polygon?crs=EPSG:4326", "zona_estudi", "memory")
    fields = QgsFields()
    fields.append(QgsField("name", QVariant.String))
    fields.append(QgsField("created_at", QVariant.String))
    out_layer.dataProvider().addAttributes(fields)
    out_layer.updateFields()

    feat = QgsFeature(out_layer.fields())
    feat.setGeometry(QgsGeometry.fromPolygonXY([ring]))
    feat.setAttributes(["Zona d'estudi", datetime.now().isoformat()])
    out_layer.dataProvider().addFeature(feat)

    # Exportem a GeoPackage
    export_layer_to_gpkg(out_layer, RISC_GPKG_OUT, RISC_LAYER_ZONA_ESTUDI)
    print(f"OK -> Capa zona_estudi creada i exportada: {RISC_LAYER_ZONA_ESTUDI}")
