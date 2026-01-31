"""Configuració centralitzada (rutes i constants) per al curs PyQGIS."""

from pathlib import Path
import sys


def _get_project_root() -> Path:
    """Detecta l'arrel del projecte (prioritza el Project Home de QGIS)."""
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
        return Path(__file__).resolve().parents[1]
    except Exception:
        return Path.cwd()


def _to_posix(path: Path) -> str:
    """Converteix un Path a string absolut amb forward slashes."""
    return str(path.resolve().as_posix())


_ROOT = _get_project_root()

# Carpetes principals
ROOT_DIR = _to_posix(_ROOT)
DADES_DIR = _to_posix(_ROOT / "dades")
ENTRADA_DIR = _to_posix(_ROOT / "dades" / "entrada")
RESULTATS_DIR = _to_posix(_ROOT / "resultats")
STYLES_DIR = _to_posix(_ROOT / "resultats" / "styles")
EXERCICIS_DIR = _to_posix(_ROOT / "exercicis")
UTILS_DIR = _to_posix(_ROOT / "utils")

# Inputs (CSV originals, noms ASCII sense accents)
METEOCAT_INPUT = _to_posix(_ROOT / "dades" / "entrada" / "Precipitacio_Olot_METEOCAT.csv")
AEMET_INPUT = _to_posix(_ROOT / "dades" / "entrada" / "Precipitacio_Olot_AEMET.csv")

# Sortides Meteocat
PAS1_OUT = _to_posix(_ROOT / "resultats" / "meteocat_pas1.csv")
PAS2A_OUT = _to_posix(_ROOT / "resultats" / "meteocat_pas2a.csv")
PAS2B_OUT = _to_posix(_ROOT / "resultats" / "meteocat_pas2b.csv")
PAS3_OUT = _to_posix(_ROOT / "resultats" / "meteocat_pas3.csv")
PAS4_OUT = _to_posix(_ROOT / "resultats" / "meteocat_pas4.csv")
STD_OUT = _to_posix(_ROOT / "resultats" / "meteocat_std.csv")

# Sortides AEMET
AEMET_PAS1_OUT = _to_posix(_ROOT / "resultats" / "aemet_pas1_long.csv")
AEMET_PAS2_OUT = _to_posix(_ROOT / "resultats" / "aemet_pas2_dates.csv")
AEMET_PAS3_OUT = _to_posix(_ROOT / "resultats" / "aemet_pas3_precip.csv")
AEMET_PAS4_OUT = _to_posix(_ROOT / "resultats" / "aemet_pas4_coords.csv")
AEMET_STD_OUT = _to_posix(_ROOT / "resultats" / "aemet_std.csv")

# Sortides finals
MERGED_STD_OUT = _to_posix(_ROOT / "resultats" / "precipitacio_olot_estandarditzada.csv")
GPKG_OUT = _to_posix(_ROOT / "resultats" / "precipitacio_olot_estandarditzada.gpkg")
GPKG_LAYER = "precip"

# Bloc Processing i Risc
RISC_GPKG_OUT = _to_posix(_ROOT / "resultats" / "risc_precipitacio_olot.gpkg")
HEATMAP_OUT_TIF = _to_posix(_ROOT / "resultats" / "hotspots_heatmap_40mm.tif")
VALIDATION_REPORT_OUT = _to_posix(_ROOT / "resultats" / "validation_report.txt")
LAYOUT_PDF_OUT = _to_posix(_ROOT / "resultats" / "layout_export.pdf")

# Export seleccions
EXPORT_SELECTION_OUT = _to_posix(_ROOT / "resultats" / "seleccio_export.gpkg")
SELECCIO_AEMET_40_CSV = _to_posix(_ROOT / "resultats" / "seleccio_aemet_40mm.csv")

# Estils
STYLE_OUT_QML = _to_posix(_ROOT / "resultats" / "alerta_40mm_style.qml")

# Camps finals del CSV estandarditzat
STD_FIELDS = [
    "source",
    "station_id",
    "station_name",
    "date",
    "precip_mm",
    "lon",
    "lat",
    "x_utm",
    "y_utm",
    "alt_m",
]

# Noms de capes (layername)
RISC_LAYER_POINTS = "punts_base"
RISC_LAYER_ALERTA_20 = "dies_alerta_20mm"
RISC_LAYER_ALERTA_40 = "dies_alerta_40mm"
RISC_LAYER_ALERTA_80 = "dies_alerta_80mm"
RISC_LAYER_EPISODIS_20 = "episodis_alerta_20mm"
RISC_LAYER_RESUM_20 = "episodis_resum_20mm"
RISC_LAYER_HOTSPOTS_40 = "hotspots_40mm"
RISC_LAYER_BASE_FLAGS = "punts_base_flags"
RISC_LAYER_ZONA_ESTUDI = "zona_estudi"
RISC_LAYER_BUFFER_ALERTA_40 = "buffer_alerta_40mm"
RISC_LAYER_BUFFER_80 = "buffer_alerta80_1000m"
RISC_LAYER_SELECCIO_AEMET_40 = "seleccio_aemet_40mm"

# QGIS projectes i grups
QGIS_PROJECT_OUT = _to_posix(_ROOT / "projecte_curs.qgz")
_template_path = _ROOT / "projecte_template.qgz"
QGIS_PROJECT_TEMPLATE = _to_posix(_template_path) if _template_path.exists() else ""
GROUP_NAME_DATA = "Dades"
GROUP_NAME_RISC = "Risc"

# Alias per compatibilitat amb scripts existents
QGZ_OUT = QGIS_PROJECT_OUT


def ensure_project_sys_path() -> None:
    """Afegeix l'arrel del projecte al sys.path si cal."""
    root = str(_ROOT)
    if root not in sys.path:
        sys.path.append(root)
