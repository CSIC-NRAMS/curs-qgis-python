# OBJECTIU:
#   Crear el mòdul utils/parse_utils.py amb funcions de neteja.
#
# ENTRADA:
#   Cap (crea el fitxer dins utils/)
#
# SORTIDA:
#   utils/parse_utils.py amb funcions reutilitzables.
#
# QUÈ APRENEM:
#   - Netejar números amb coma decimal.
#   - Parsejar dates en formats diferents.
#   - Validar dates construïdes.

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

content = '''"""Funcions reutilitzables per netejar números i dates."""

from datetime import datetime, date
from typing import Optional


def to_float(value) -> Optional[float]:
    """Converteix a float de manera segura (accepta comes com a separador)."""
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    s = str(value).strip()
    if s == "":
        return None
    s = s.replace(",", ".")
    try:
        return float(s)
    except Exception:
        return None


def parse_date(value) -> Optional[date]:
    """Parseja una data en formats DD/MM/YYYY, YYYY-MM-DD o DD-MM-YYYY."""
    s = (value or "").strip()
    if s == "":
        return None
    for fmt in ("%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y"):
        try:
            return datetime.strptime(s, fmt).date()
        except Exception:
            continue
    return None


def build_date(year, month, day) -> Optional[date]:
    """Construeix una data a partir d'any, mes i dia amb validació."""
    try:
        y = int(str(year).strip())
        m = int(str(month).strip())
        d = int(str(day).strip())
        return datetime(y, m, d).date()
    except Exception:
        return None
'''

write_text(utils_dir / "parse_utils.py", content)
print("OK -> creat utils/parse_utils.py")
