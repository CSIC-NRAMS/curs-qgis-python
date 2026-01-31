# OBJECTIU:
#   Aplicar simbologia bàsica i guardar estils .qml.
#
# ENTRADA:
#   resultats/precipitacio_olot_estandarditzada.gpkg (capa base)
#
# SORTIDA:
#   resultats/styles/base_precip_graduated.qml
#   resultats/styles/base_source_categorized.qml
#
# QUÈ APRENEM:
#   - Aplicar simbologia graduada i categòrica.
#   - Guardar estils QML per reutilitzar-los.

import os  # Per gestionar rutes
import sys  # Per ajustar el path d'importació

# Afegim la carpeta arrel del projecte al sys.path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from qgis.core import (
    QgsProject, QgsSymbol, QgsGraduatedSymbolRenderer, QgsRendererRange,
    QgsCategorizedSymbolRenderer, QgsRendererCategory, QgsSingleSymbolRenderer
)
from qgis.PyQt.QtGui import QColor

from utils.config import (
    RESULTATS_DIR, STYLES_DIR, GPKG_OUT, GPKG_LAYER,
    RISC_GPKG_OUT, RISC_LAYER_ALERTA_20, RISC_LAYER_ALERTA_40, RISC_LAYER_ALERTA_80
)
from utils.csv_utils import ensure_dir
from utils.gui_utils import load_vector_layer_gpkg, add_layer_to_group

# Assegurem carpetes
ensure_dir(RESULTATS_DIR)
ensure_dir(STYLES_DIR)

# Carreguem capa base
base_layer = load_vector_layer_gpkg(GPKG_OUT, GPKG_LAYER, name="base_points")
if base_layer is None:
    print("ERROR -> No s'ha pogut carregar la capa base.")
else:
    # 1) Graduated per precip_mm
    field_name = "precip_mm"
    ranges = []
    symbol = QgsSymbol.defaultSymbol(base_layer.geometryType())

    # Fem 5 classes simples (0-10, 10-20, 20-40, 40-80, 80+)
    class_limits = [(0, 10), (10, 20), (20, 40), (40, 80), (80, 9999)]
    colors = [QColor("#dbeafe"), QColor("#93c5fd"), QColor("#60a5fa"), QColor("#3b82f6"), QColor("#1d4ed8")]

    for (low, high), color in zip(class_limits, colors):
        sym = symbol.clone()
        sym.setColor(color)
        label = f"{low}–{high} mm"
        ranges.append(QgsRendererRange(low, high, sym, label))

    renderer = QgsGraduatedSymbolRenderer(field_name, ranges)
    renderer.setMode(QgsGraduatedSymbolRenderer.EqualInterval)
    base_layer.setRenderer(renderer)

    # Guardem estil QML
    qml_precip = os.path.join(STYLES_DIR, "base_precip_graduated.qml")
    base_layer.saveNamedStyle(qml_precip)
    print(f"OK -> Estil graduat guardat: {qml_precip}")

    # 2) Categorized per source
    categories = []
    for value, color in [("METEOCAT", QColor("#10b981")), ("AEMET", QColor("#f59e0b"))]:
        sym = symbol.clone()
        sym.setColor(color)
        categories.append(QgsRendererCategory(value, sym, value))

    cat_renderer = QgsCategorizedSymbolRenderer("source", categories)
    base_layer.setRenderer(cat_renderer)

    qml_source = os.path.join(STYLES_DIR, "base_source_categorized.qml")
    base_layer.saveNamedStyle(qml_source)
    print(f"OK -> Estil categòric guardat: {qml_source}")

    # Afegim la capa base al projecte
    add_layer_to_group(base_layer, "00 Base")

# Estil simple per alertes (si existeixen)
for layer_name, color in [
    (RISC_LAYER_ALERTA_20, QColor("#fbbf24")),
    (RISC_LAYER_ALERTA_40, QColor("#f97316")),
    (RISC_LAYER_ALERTA_80, QColor("#ef4444"))
]:
    layer = load_vector_layer_gpkg(RISC_GPKG_OUT, layer_name, name=layer_name)
    if layer is None:
        continue
    sym = QgsSymbol.defaultSymbol(layer.geometryType())
    sym.setColor(color)
    layer.setRenderer(QgsSingleSymbolRenderer(sym))
    add_layer_to_group(layer, "10 Alertes")

print("OK -> Simbologia aplicada.")
print("Consell: Pots carregar els .qml des de la GUI amb 'Estil -> Carrega estil'.")
