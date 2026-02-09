"""Ex02 — Exportar CSV a GeoPackage.

Fa: carrega el CSV com a capa i el desa en GPKG.
Llegeix: MERGED_STD_OUT
Escriu: GPKG_OUT (capa GPKG_LAYER)
OK esperat: missatge d'OK i capa afegida al projecte.
"""

import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from qgis.core import QgsVectorLayer, QgsVectorFileWriter, QgsProject
from tools.config import MERGED_STD_OUT, GPKG_OUT, GPKG_LAYER, RESULTATS_DIR
from tools.csv_utils import ensure_dir

ensure_dir(RESULTATS_DIR)

# URI Màgica per carregar CSV sense GUI
# (Primer cop: URI) Aquesta cadena indica a QGIS com interpretar el CSV.
uri = f"file:///{MERGED_STD_OUT}?delimiter=,&xField=lon&yField=lat&crs=EPSG:4326"

# Creem una capa temporal de punts a partir del CSV.
layer = QgsVectorLayer(uri, "precipitacio_olot", "delimitedtext")

if not layer.isValid():
    print("ERROR -> No s'ha pogut carregar la capa del CSV.")
else:
    # Afegim la capa al projecte per visualitzar-la.
    QgsProject.instance().addMapLayer(layer)

    options = QgsVectorFileWriter.SaveVectorOptions()
    options.driverName = "GPKG"
    options.layerName = GPKG_LAYER
    options.fileEncoding = "UTF-8"

    # Escrivim la capa a un GeoPackage (format SIG professional).
    QgsVectorFileWriter.writeAsVectorFormatV2(layer, GPKG_OUT, QgsProject.instance().transformContext(), options)

    print(f"OK -> GeoPackage creat: {GPKG_OUT}")
    print("OK -> Capa afegida al projecte QGIS.")
