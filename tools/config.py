"""Configuració del curs (rutes base i constants)."""

# Aquest fitxer centralitza rutes i noms per evitar valors duplicats als scripts.

from pathlib import Path


def _get_project_root() -> Path:
    """Detecta l'arrel del projecte (prioritza QGIS Project Home)."""
    # (Primer cop: Project Home) QGIS te un directori arrel del projecte per rutes relatives.
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

    # Fallback: puja des de tools/ cap a l'arrel del projecte
    try:
        return Path(__file__).resolve().parents[1]
    except Exception:
        return Path.cwd()


def as_posix(path: Path) -> str:
    """Converteix un Path a string absolut amb forward slashes."""
    # Fem servir barres / per evitar problemes entre Windows i altres sistemes.
    return str(path.resolve().as_posix())


_ROOT = _get_project_root()

# Rutes base
# (Primer cop: constants) Una constant es una variable que no hauria de canviar.
ROOT_DIR = as_posix(_ROOT)
DADES_DIR = as_posix(_ROOT / "dades")
ENTRADA_DIR = as_posix(_ROOT / "dades" / "entrada")
RESULTATS_DIR = as_posix(_ROOT / "resultats")

# --- Entrades base (Bloc 00) ---
METEOCAT_INPUT = as_posix(Path(ENTRADA_DIR) / "Precipitacio_Olot_METEOCAT.csv")
AEMET_INPUT = as_posix(Path(ENTRADA_DIR) / "Precipitacio_Olot_AEMET.csv")

# --- Meteocat (Bloc 01) ---
PAS1_OUT = as_posix(Path(RESULTATS_DIR) / "meteocat_pas1.csv")
PAS2A_OUT = as_posix(Path(RESULTATS_DIR) / "meteocat_pas2a.csv")
PAS2B_OUT = as_posix(Path(RESULTATS_DIR) / "meteocat_pas2b.csv")
PAS3_OUT = as_posix(Path(RESULTATS_DIR) / "meteocat_pas3.csv")
PAS4_OUT = as_posix(Path(RESULTATS_DIR) / "meteocat_pas4.csv")

STD_OUT = as_posix(Path(RESULTATS_DIR) / "meteocat_std.csv")
STD_FIELDS = [
    "source", "station_id", "station_name", "date",
    "precip_mm", "lon", "lat", "x_utm", "y_utm", "alt_m"
]

# --- AEMET (Bloc 02) ---
AEMET_PAS1_OUT = as_posix(Path(RESULTATS_DIR) / "aemet_pas1_long.csv")
AEMET_PAS2_OUT = as_posix(Path(RESULTATS_DIR) / "aemet_pas2_dates.csv")
AEMET_PAS3_OUT = as_posix(Path(RESULTATS_DIR) / "aemet_pas3_precip.csv")
AEMET_PAS4_OUT = as_posix(Path(RESULTATS_DIR) / "aemet_pas4_coords.csv")

AEMET_STD_OUT = as_posix(Path(RESULTATS_DIR) / "aemet_std.csv")

# --- Merge i export (Bloc 03) ---
MERGED_STD_OUT = as_posix(Path(RESULTATS_DIR) / "precipitacio_olot_estandarditzada.csv")
GPKG_OUT = as_posix(Path(RESULTATS_DIR) / "precipitacio_olot.gpkg")
GPKG_LAYER = "precipitacio_olot"
