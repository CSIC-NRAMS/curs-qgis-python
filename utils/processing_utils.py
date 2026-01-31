"""Utilitats per a QGIS Processing i operacions comunes de capes."""

from __future__ import annotations

from typing import Callable

from utils.csv_utils import ensure_dir


def _require_qgis():
    try:
        from qgis.core import QgsVectorFileWriter, QgsProject, QgsField
        return QgsVectorFileWriter, QgsProject, QgsField
    except Exception as exc:
        raise RuntimeError("PyQGIS no està disponible. Executa aquest script dins QGIS.") from exc


def _ensure_processing_initialized():
    """Inicialitza Processing si cal i retorna el mòdul processing."""
    try:
        import processing
        try:
            from processing.core.Processing import Processing
            Processing.initialize()
        except Exception:
            pass
        return processing
    except Exception as exc:
        raise RuntimeError(f"Processing no està disponible: {exc}")


def run_processing_algorithm(algo_id: str, params: dict) -> dict:
    """Executa un algoritme de Processing i retorna el dict de resultats."""
    processing = _ensure_processing_initialized()
    return processing.run(algo_id, params)


def run_processing(algo_id: str, params: dict) -> dict:
    """Alias didàctic per a processing.run."""
    return run_processing_algorithm(algo_id, params)


def extract_by_expression(layer, expression: str):
    """Filtra una capa amb una expressió i retorna una capa en memòria."""
    result = run_processing_algorithm(
        "native:extractbyexpression",
        {"INPUT": layer, "EXPRESSION": expression, "OUTPUT": "memory:"},
    )
    return result["OUTPUT"]


def _write_vector_layer(layer, out_path: str, layer_name: str):
    QgsVectorFileWriter, QgsProject, _ = _require_qgis()
    ensure_dir(out_path)
    options = QgsVectorFileWriter.SaveVectorOptions()
    options.driverName = "GPKG"
    options.layerName = layer_name
    options.fileEncoding = "UTF-8"
    options.actionOnExistingFile = QgsVectorFileWriter.CreateOrOverwriteLayer
    if hasattr(QgsVectorFileWriter, "writeAsVectorFormatV2"):
        return QgsVectorFileWriter.writeAsVectorFormatV2(
            layer,
            out_path,
            QgsProject.instance().transformContext(),
            options,
        )
    return QgsVectorFileWriter.writeAsVectorFormat(
        layer,
        out_path,
        options.fileEncoding,
        layer.crs(),
        options.driverName,
    )


def export_layer_to_gpkg(layer, gpkg_path: str, layer_name: str) -> None:
    """Exporta una capa a GeoPackage (sobreescriu la capa si existeix)."""
    _write_vector_layer(layer, gpkg_path, layer_name)


def add_field_if_missing(layer, field_name: str, qvariant_type, default_value=None) -> None:
    """Afegeix un camp si no existeix i assigna un valor per defecte."""
    _, _, QgsField = _require_qgis()
    if layer.fields().indexFromName(field_name) != -1:
        return

    was_editing = layer.isEditable()
    if not was_editing:
        layer.startEditing()

    layer.dataProvider().addAttributes([QgsField(field_name, qvariant_type)])
    layer.updateFields()

    idx = layer.fields().indexFromName(field_name)
    if idx != -1:
        for feat in layer.getFeatures():
            layer.changeAttributeValue(feat.id(), idx, default_value)

    if not was_editing:
        layer.commitChanges()


def update_field_values(layer, field_name: str, compute_func: Callable) -> None:
    """Actualitza un camp amb una funció compute_func(feature)."""
    idx = layer.fields().indexFromName(field_name)
    if idx == -1:
        return

    was_editing = layer.isEditable()
    if not was_editing:
        layer.startEditing()

    for feat in layer.getFeatures():
        layer.changeAttributeValue(feat.id(), idx, compute_func(feat))

    if not was_editing:
        layer.commitChanges()


def add_or_update_field(layer, field_name: str, qvariant_type, default_value=None) -> None:
    """Afegeix un camp si no existeix; si existeix, actualitza valor per defecte."""
    add_field_if_missing(layer, field_name, qvariant_type, default_value)


def update_features_expression(layer, field_name: str, expression_string: str, only_selected: bool = False) -> None:
    """Actualitza un camp usant una expressió QGIS (Processing)."""
    params = {
        "INPUT": layer,
        "FIELD_NAME": field_name,
        "FIELD_TYPE": 0,
        "FIELD_LENGTH": 0,
        "FIELD_PRECISION": 0,
        "NEW_FIELD": False,
        "FORMULA": expression_string,
        "OUTPUT": "memory:",
    }
    if only_selected:
        params["ONLY_SELECTED"] = True
    result = run_processing_algorithm("native:fieldcalculator", params)
    return result.get("OUTPUT")


def open_attribute_table(layer) -> None:
    """Obre la taula d'atributs si hi ha GUI; si no, imprimeix un missatge."""
    try:
        from qgis.utils import iface

        if iface is None:
            raise RuntimeError("No hi ha iface")
        iface.showAttributeTable(layer)
    except Exception:
        print("AVÍS -> No es pot obrir la taula d'atributs (iface no disponible).")
