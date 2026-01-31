# OBJECTIU:
#   Crear el mòdul utils/gui_utils.py amb helpers de GUI de QGIS.
#
# ENTRADA:
#   Cap (crea el fitxer dins utils/)
#
# SORTIDA:
#   utils/gui_utils.py amb funcions reutilitzables.
#
# QUÈ APRENEM:
#   - Operar capes des de la GUI (iface).
#   - Afegir capes a grups i exportar seleccions.
#   - Guardar projectes QGIS des de Python.

from pathlib import Path


def get_project_root() -> Path:
    """Detecta l'arrel del projecte (prioritza Project Home de QGIS)."""
    try:
        from qgis.core import QgsProject

        project = QgsProject.instance()
        home = project.homePath()
        if home:
            return Path(home)
        project_file = project.fileName()
        if project_file:
            return Path(project_file).parent
    except Exception:
        pass

    try:
        return Path(__file__).resolve().parents[2]
    except Exception:
        return Path.cwd()


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


ROOT = get_project_root()
utils_dir = ROOT / "utils"
utils_dir.mkdir(parents=True, exist_ok=True)

content = '''"""Utilitats per a operacions típiques de la GUI de QGIS via Python."""

import os
from typing import Optional

from utils.csv_utils import ensure_dir


GUI_REQUIRED_MESSAGE = "Aquest exercici necessita QGIS obert (iface)."


def _require_iface():
    try:
        from qgis.utils import iface
    except Exception as exc:
        raise RuntimeError(GUI_REQUIRED_MESSAGE) from exc

    if iface is None:
        raise RuntimeError(GUI_REQUIRED_MESSAGE)

    return iface


def _require_qgis_core():
    try:
        from qgis.core import QgsVectorLayer, QgsProject, QgsLayerTreeGroup, QgsVectorFileWriter
        return QgsVectorLayer, QgsProject, QgsLayerTreeGroup, QgsVectorFileWriter
    except Exception as exc:
        raise RuntimeError("PyQGIS no està disponible. Executa aquest script dins QGIS.") from exc


def load_project_from_template(template_path: Optional[str]) -> bool:
    _require_iface()
    _, QgsProject, _, _ = _require_qgis_core()
    project = QgsProject.instance()
    if template_path and os.path.exists(template_path):
        return project.read(template_path)
    project.clear()
    return True


def create_or_get_group(group_name: str):
    _require_iface()
    _, QgsProject, _, _ = _require_qgis_core()
    root = QgsProject.instance().layerTreeRoot()
    group = root.findGroup(group_name)
    if group is None:
        group = root.addGroup(group_name)
    return group


def add_layer_to_group(layer, group_name: str, add_to_legend: bool = True) -> None:
    _require_iface()
    _, QgsProject, _, _ = _require_qgis_core()
    if layer is None:
        return
    project = QgsProject.instance()
    project.addMapLayer(layer, False)
    if add_to_legend:
        group = create_or_get_group(group_name)
        group.addLayer(layer)


def save_project_if_needed(out_path: str) -> bool:
    _require_iface()
    _, QgsProject, _, _ = _require_qgis_core()
    project = QgsProject.instance()
    if project.fileName():
        return True
    ensure_dir(out_path)
    return project.write(out_path)


def load_vector_layer_gpkg(
    gpkg_path: str,
    layer_name: str,
    name_in_legend: Optional[str] = None,
    **kwargs,
):
    _require_iface()
    QgsVectorLayer, _, _, _ = _require_qgis_core()
    if not os.path.exists(gpkg_path):
        return None
    if name_in_legend is None and "name" in kwargs:
        name_in_legend = kwargs.get("name")
    uri = f"{gpkg_path}|layername={layer_name}"
    layer = QgsVectorLayer(uri, name_in_legend or layer_name, "ogr")
    return layer if layer.isValid() else None


def export_selected_to_gpkg(layer, out_gpkg: str, out_layer_name: str) -> bool:
    _require_iface()
    _, QgsProject, _, QgsVectorFileWriter = _require_qgis_core()
    if layer is None:
        return False
    if layer.selectedFeatureCount() == 0:
        print("AVÍS -> No hi ha selecció activa.")
        return False
    ensure_dir(out_gpkg)

    options = QgsVectorFileWriter.SaveVectorOptions()
    options.driverName = "GPKG"
    options.layerName = out_layer_name
    options.fileEncoding = "UTF-8"
    options.onlySelectedFeatures = True
    options.actionOnExistingFile = QgsVectorFileWriter.CreateOrOverwriteLayer

    if hasattr(QgsVectorFileWriter, "writeAsVectorFormatV2"):
        err = QgsVectorFileWriter.writeAsVectorFormatV2(
            layer,
            out_gpkg,
            QgsProject.instance().transformContext(),
            options,
        )
    else:
        err = QgsVectorFileWriter.writeAsVectorFormat(
            layer,
            out_gpkg,
            options.fileEncoding,
            layer.crs(),
            options.driverName,
            onlySelected=True,
        )

    return err == QgsVectorFileWriter.NoError


def export_selected_to_csv(layer, out_csv: str) -> bool:
    _require_iface()
    _, QgsProject, _, QgsVectorFileWriter = _require_qgis_core()
    if layer is None:
        return False
    if layer.selectedFeatureCount() == 0:
        print("AVÍS -> No hi ha selecció activa.")
        return False
    ensure_dir(out_csv)

    options = QgsVectorFileWriter.SaveVectorOptions()
    options.driverName = "CSV"
    options.fileEncoding = "UTF-8"
    options.onlySelectedFeatures = True

    if hasattr(QgsVectorFileWriter, "writeAsVectorFormatV2"):
        err = QgsVectorFileWriter.writeAsVectorFormatV2(
            layer,
            out_csv,
            QgsProject.instance().transformContext(),
            options,
        )
    else:
        err = QgsVectorFileWriter.writeAsVectorFormat(
            layer,
            out_csv,
            options.fileEncoding,
            layer.crs(),
            options.driverName,
            onlySelected=True,
        )

    return err == QgsVectorFileWriter.NoError
'''

write_text(utils_dir / "gui_utils.py", content)
print("OK -> creat utils/gui_utils.py")
