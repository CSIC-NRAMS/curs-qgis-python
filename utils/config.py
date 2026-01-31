"""Configuració centralitzada (rutes i constants) per al curs PyQGIS."""

"""Configuració mínima del curs (rutes base).

Aquest fitxer és deliberadament petit i didàctic.
No crea carpetes ni fitxers automàticament.
"""

from pathlib import Path


def _get_project_root() -> Path:
    """Detecta l'arrel del projecte (prioritza QGIS Project Home)."""
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

    # Fallback: puja des de utils/ cap a l'arrel del projecte
    try:
        return Path(__file__).resolve().parents[1]
    except Exception:
        return Path.cwd()


def as_posix(path: Path) -> str:
    """Converteix un Path a string absolut amb forward slashes."""
    return str(path.resolve().as_posix())


_ROOT = _get_project_root()

# Rutes base (mínim viable)
ROOT_DIR = as_posix(_ROOT)
DADES_DIR = as_posix(_ROOT / "dades")
ENTRADA_DIR = as_posix(_ROOT / "dades" / "entrada")
RESULTATS_DIR = as_posix(_ROOT / "resultats")
