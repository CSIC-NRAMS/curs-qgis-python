"""tools/qgis_utils.py — utilitats PyQGIS mínimes.

Fa: transforma UTM31 a WGS84.
Llegeix: res (paràmetres en memòria).
Escriu: res.
OK esperat: import correcte dins QGIS.
"""

# Aquest mòdul depen de PyQGIS, per tant nomes funciona dins QGIS.


def _require_qgis():
    # Comprovem que PyQGIS esta disponible i expliquem l'error si no ho esta.
    try:
        from qgis.core import (
            QgsCoordinateReferenceSystem,
            QgsCoordinateTransform,
            QgsProject,
            QgsPointXY,
        )
        return QgsCoordinateReferenceSystem, QgsCoordinateTransform, QgsProject, QgsPointXY
    except Exception as exc:
        raise RuntimeError("PyQGIS no està disponible. Executa aquest script dins QGIS.") from exc


def get_utm31_to_wgs84_transformer():
    """Retorna un QgsCoordinateTransform EPSG:25831 -> EPSG:4326."""
    # (Primer cop: CRS) Un CRS defineix com s'interpreten les coordenades.
    QgsCoordinateReferenceSystem, QgsCoordinateTransform, QgsProject, _ = _require_qgis()
    crs_src = QgsCoordinateReferenceSystem("EPSG:25831")
    crs_dst = QgsCoordinateReferenceSystem("EPSG:4326")
    return QgsCoordinateTransform(crs_src, crs_dst, QgsProject.instance().transformContext())


def transform_utm_to_lonlat(x, y, xform):
    """Transforma coordenades UTM a lon/lat amb un QgsCoordinateTransform."""
    # Rebem X/Y en metres i retornem lon/lat en graus.
    _, _, _, QgsPointXY = _require_qgis()
    pt = QgsPointXY(x, y)
    pt_ll = xform.transform(pt)
    return pt_ll.x(), pt_ll.y()
