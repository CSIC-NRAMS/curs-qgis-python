"""Funcions reutilitzables per treballar amb PyQGIS (CRS i transformacions)."""

from pathlib import Path

from utils.csv_utils import ensure_dir


def _require_qgis():
    try:
        from qgis.core import (
            QgsCoordinateReferenceSystem,
            QgsCoordinateTransform,
            QgsProject,
            QgsPointXY,
            QgsVectorFileWriter,
        )
        return (
            QgsCoordinateReferenceSystem,
            QgsCoordinateTransform,
            QgsProject,
            QgsPointXY,
            QgsVectorFileWriter,
        )
    except Exception as exc:
        raise RuntimeError("PyQGIS no està disponible. Executa aquest script dins QGIS.") from exc


def get_utm31_to_wgs84_transformer():
    """Retorna un QgsCoordinateTransform EPSG:25831 -> EPSG:4326."""
    QgsCoordinateReferenceSystem, QgsCoordinateTransform, QgsProject, _, _ = _require_qgis()
    crs_src = QgsCoordinateReferenceSystem("EPSG:25831")
    crs_dst = QgsCoordinateReferenceSystem("EPSG:4326")
    return QgsCoordinateTransform(crs_src, crs_dst, QgsProject.instance().transformContext())


def transform_utm_to_lonlat(x, y, xform):
    """Transforma coordenades UTM a lon/lat amb un QgsCoordinateTransform."""
    _, _, _, QgsPointXY, _ = _require_qgis()
    pt = QgsPointXY(x, y)
    pt_ll = xform.transform(pt)
    return pt_ll.x(), pt_ll.y()


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


def run_processing_algorithm(alg_id: str, params: dict) -> dict:
    """Wrapper de processing.run amb inicialització segura."""
    processing = _ensure_processing_initialized()
    return processing.run(alg_id, params)


def extract_by_expression(layer, expression: str):
    """Retorna una capa filtrada en memòria (native:extractbyexpression)."""
    result = run_processing_algorithm(
        "native:extractbyexpression",
        {"INPUT": layer, "EXPRESSION": expression, "OUTPUT": "memory:"},
    )
    return result["OUTPUT"]


def export_layer_to_gpkg(layer, gpkg_path: str, layer_name: str) -> None:
    """Exporta una capa a GeoPackage amb overwrite de la capa si existeix."""
    _, _, QgsProject, _, QgsVectorFileWriter = _require_qgis()
    ensure_dir(gpkg_path)

    options = QgsVectorFileWriter.SaveVectorOptions()
    options.driverName = "GPKG"
    options.layerName = layer_name
    options.fileEncoding = "UTF-8"
    options.actionOnExistingFile = QgsVectorFileWriter.CreateOrOverwriteLayer

    if hasattr(QgsVectorFileWriter, "writeAsVectorFormatV2"):
        QgsVectorFileWriter.writeAsVectorFormatV2(
            layer,
            gpkg_path,
            QgsProject.instance().transformContext(),
            options,
        )
    else:
        QgsVectorFileWriter.writeAsVectorFormat(
            layer,
            gpkg_path,
            options.fileEncoding,
            layer.crs(),
            options.driverName,
        )


def as_file_uri(path: Path) -> str:
    """Retorna un file:/// URI compatible amb QGIS (Windows inclòs)."""
    return path.resolve().as_uri()
