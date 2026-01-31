# OBJECTIU:
#   Crear un layout simple i exportar un PDF (opcional/avançat).
#
# ENTRADA:
#   resultats/risc_precipitacio_olot.gpkg (capa dies_alerta_40mm)
#
# SORTIDA:
#   resultats/mapa_alerta_40mm.pdf
#
# QUÈ APRENEM:
#   - Crear un layout bàsic.
#   - Exportar un mapa a PDF.
#   - Sortida professional des de QGIS.

import os  # Per gestionar rutes
import sys  # Per ajustar el path d'importació

# Afegim la carpeta arrel del projecte al sys.path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from qgis.core import (
    QgsProject, QgsLayout, QgsLayoutItemMap, QgsLayoutItemLabel,
    QgsLayoutItemLegend, QgsLayoutExporter, QgsLayoutPoint, QgsUnitTypes,
    QgsVectorLayer
)
from qgis.PyQt.QtGui import QFont

from utils.config import RESULTATS_DIR, RISC_GPKG_OUT, RISC_LAYER_ALERTA_40, LAYOUT_PDF_OUT
from utils.csv_utils import ensure_dir

# Assegurem la carpeta de resultats
ensure_dir(RESULTATS_DIR)

# Carreguem la capa d’alerta 40 mm
uri = f"{RISC_GPKG_OUT}|layername={RISC_LAYER_ALERTA_40}"
layer = QgsVectorLayer(uri, "dies_alerta_40mm", "ogr")

if not layer.isValid():
    print("ERROR -> No s'ha pogut carregar dies_alerta_40mm. Executa ex15.")
else:
    project = QgsProject.instance()
    project.addMapLayer(layer)

    try:
        # Creem un layout nou
        layout = QgsLayout(project)
        layout.initializeDefaults()
        layout.setName("layout_alerta_40mm")

        # Mapa
        map_item = QgsLayoutItemMap(layout)
        map_item.setRect(20, 20, 200, 120)
        map_item.setExtent(layer.extent())
        layout.addLayoutItem(map_item)

        # Posició del mapa
        map_item.attemptMove(QgsLayoutPoint(10, 20, QgsUnitTypes.LayoutMillimeters))

        # Títol
        title = QgsLayoutItemLabel(layout)
        title.setText("Dies d’alerta ≥ 40 mm")
        title.setFont(QFont("Segoe UI", 16))
        title.adjustSizeToText()
        title.attemptMove(QgsLayoutPoint(10, 5, QgsUnitTypes.LayoutMillimeters))
        layout.addLayoutItem(title)

        # Llegenda
        legend = QgsLayoutItemLegend(layout)
        legend.setTitle("Llegenda")
        legend.setLinkedMap(map_item)
        legend.attemptMove(QgsLayoutPoint(220, 20, QgsUnitTypes.LayoutMillimeters))
        layout.addLayoutItem(legend)

        # Exportem a PDF
        exporter = QgsLayoutExporter(layout)
        result = exporter.exportToPdf(LAYOUT_PDF_OUT, QgsLayoutExporter.PdfExportSettings())

        if result == QgsLayoutExporter.Success:
            print(f"OK -> PDF creat: {LAYOUT_PDF_OUT}")
        else:
            print("AVÍS -> No s'ha pogut exportar el PDF.")

    except Exception as exc:
        print(f"AVÍS -> Layout no disponible o error: {exc}")
        print("Suggeriment: crea el layout des de la GUI si falla en aquest entorn.")
