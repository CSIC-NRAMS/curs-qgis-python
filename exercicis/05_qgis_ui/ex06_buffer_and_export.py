# OBJECTIU:
#   Crear buffers sobre alertes >= 40 mm i exportar-los al GPKG de risc.
#
# ENTRADA:
#   resultats/risc_precipitacio_olot.gpkg (capa dies_alerta_40mm)
#
# SORTIDA:
#   resultats/risc_precipitacio_olot.gpkg (capa buffer_alerta_40mm)
#
# QUÈ APRENEM:
#   - Reprojectar per fer buffers en metres.
#   - Aplicar Processing (buffer).
#   - Exportar capes resultants.

import os  # Per gestionar rutes
import sys  # Per ajustar el path d'importació

# Afegim la carpeta arrel del projecte al sys.path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from qgis.core import QgsVectorLayer, QgsProject

from utils.config import (
    RESULTATS_DIR, RISC_GPKG_OUT, RISC_LAYER_ALERTA_40, RISC_LAYER_BUFFER_ALERTA_40
)
from utils.csv_utils import ensure_dir
from utils.processing_utils import run_processing_algorithm, export_layer_to_gpkg

# Assegurem la carpeta de resultats
ensure_dir(RESULTATS_DIR)

# Carreguem la capa d’alerta 40 mm
uri = f"{RISC_GPKG_OUT}|layername={RISC_LAYER_ALERTA_40}"
layer = QgsVectorLayer(uri, "dies_alerta_40mm", "ogr")

if not layer.isValid():
    print("ERROR -> No s'ha pogut carregar dies_alerta_40mm. Executa ex15.")
else:
    # Si estem en EPSG:4326, reprojectem a UTM 25831 per fer buffers en metres
    if layer.crs().authid() == "EPSG:4326":
        print("AVÍS -> CRS en graus. Reprojectem a EPSG:25831 per fer buffers en metres.")
        reproj = run_processing_algorithm(
            "native:reprojectlayer",
            {
                "INPUT": layer,
                "TARGET_CRS": "EPSG:25831",
                "OUTPUT": "memory:"
            }
        )["OUTPUT"]
        layer_to_buffer = reproj
    else:
        layer_to_buffer = layer

    # Apliquem buffer (1000 m)
    buff = run_processing_algorithm(
        "native:buffer",
        {
            "INPUT": layer_to_buffer,
            "DISTANCE": 1000,
            "SEGMENTS": 8,
            "DISSOLVE": False,
            "OUTPUT": "memory:"
        }
    )["OUTPUT"]

    # Si hem reprojectat, tornem a EPSG:4326 per coherència
    if buff.crs().authid() != "EPSG:4326":
        buff = run_processing_algorithm(
            "native:reprojectlayer",
            {
                "INPUT": buff,
                "TARGET_CRS": "EPSG:4326",
                "OUTPUT": "memory:"
            }
        )["OUTPUT"]

    # Exportem el buffer
    export_layer_to_gpkg(buff, RISC_GPKG_OUT, RISC_LAYER_BUFFER_ALERTA_40)
    QgsProject.instance().addMapLayer(buff)

    print(f"OK -> Buffer creat: {RISC_LAYER_BUFFER_ALERTA_40}")
