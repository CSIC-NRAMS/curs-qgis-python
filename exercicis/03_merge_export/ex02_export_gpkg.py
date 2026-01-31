# OBJECTIU:
#   Visualitzar el resultat a QGIS i exportar-lo a GeoPackage.
#
# ENTRADA:
#   ./resultats/precipitacio_olot_estandarditzada.csv
#
# SORTIDA:
#   ./resultats/precipitacio_olot_estandarditzada.gpkg (capa "precip")
#
# QUÈ APRENEM:
#   - Carregar un CSV com a capa a QGIS.
#   - Exportar una capa a GeoPackage.
#   - Afegir la capa al projecte de QGIS.

import os  # Per gestionar rutes
import sys  # Per ajustar el path d'importació

# Afegim la carpeta arrel del projecte al sys.path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

# Imports de QGIS
from qgis.core import QgsVectorLayer, QgsVectorFileWriter, QgsProject

# Importem configuració i utilitats
from utils.config import MERGED_STD_OUT, GPKG_OUT, GPKG_LAYER, RESULTATS_DIR
from utils.csv_utils import ensure_dir

# Assegurem la carpeta de resultats
ensure_dir(RESULTATS_DIR)

# Construïm la URI per carregar el CSV com a capa
# Important: indiquem quines columnes són lon/lat i el CRS EPSG:4326
uri = f"file:///{MERGED_STD_OUT}?delimiter=,&xField=lon&yField=lat&crs=EPSG:4326"

# Creem la capa de punts a partir del CSV (proveïdor: delimitedtext)
layer = QgsVectorLayer(uri, "precipitacio_olot", "delimitedtext")

# Comprovem si la capa és vàlida
if not layer.isValid():
    print("ERROR -> No s'ha pogut carregar la capa del CSV.")
else:
    # Afegim la capa al projecte actual per visualitzar-la immediatament
    QgsProject.instance().addMapLayer(layer)

    # Preparem opcions d'exportació a GeoPackage
    # El nom de capa dins el GPKG serà el que definim a GPKG_LAYER
    options = QgsVectorFileWriter.SaveVectorOptions()
    options.driverName = "GPKG"
    options.layerName = GPKG_LAYER
    options.fileEncoding = "UTF-8"

    # Exportem la capa a GeoPackage
    QgsVectorFileWriter.writeAsVectorFormatV2(layer, GPKG_OUT, QgsProject.instance().transformContext(), options)

    # Missatge final
    print(f"OK -> GeoPackage creat: {GPKG_OUT}")
    print("OK -> Capa afegida al projecte QGIS.")
