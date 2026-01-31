# OBJECTIU:
#   Preparar l'estructura del projecte i normalitzar els CSV d'entrada.
#
# ENTRADA:
#   ./dades/entrada/* (CSV originals del curs)
#
# SORTIDA:
#   Carpetes creades: dades/entrada, resultats, utils, exercicis, projectes
#   CSV renombrats/copiat a noms ASCII si cal
#
# QUÈ APRENEM:
#   - Fer servir el Project Home de QGIS.
#   - Crear una estructura mínima.
#   - Evitar problemes d'encoding en noms de fitxer.

from pathlib import Path
import shutil


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

    print("AVÍS -> Project Home no definit. Guarda el projecte a QGIS.")
    try:
        return Path(__file__).resolve().parents[2]
    except Exception:
        return Path.cwd()


def ensure_dirs(root: Path) -> dict:
    """Crea directoris mínims i retorna un diccionari de paths."""
    entrada = root / "dades" / "entrada"
    resultats = root / "resultats"
    utils_dir = root / "utils"
    exercicis_dir = root / "exercicis"
    projectes_dir = root / "projectes"

    entrada.mkdir(parents=True, exist_ok=True)
    resultats.mkdir(parents=True, exist_ok=True)
    utils_dir.mkdir(parents=True, exist_ok=True)
    exercicis_dir.mkdir(parents=True, exist_ok=True)
    projectes_dir.mkdir(parents=True, exist_ok=True)

    return {
        "root": root,
        "entrada": entrada,
        "resultats": resultats,
        "utils": utils_dir,
        "exercicis": exercicis_dir,
        "projectes": projectes_dir,
    }


def normalize_inputs(entrada_dir: Path) -> dict:
    """Normalitza noms de CSV i retorna l'estat de cada fitxer esperat."""
    expected = {
        "Precipitacio_Olot_METEOCAT.csv": None,
        "Precipitacio_Olot_AEMET.csv": None,
    }

    variants = {
        "Precipitacio_Olot_METEOCAT.csv": [
            "Precipitaci#U00f3_Olot_METEOCAT.csv",
            "Precipitació_Olot_METEOCAT.csv",
            "PrecipitaciÃ³_Olot_METEOCAT.csv",
        ],
        "Precipitacio_Olot_AEMET.csv": [
            "Precipitaci#U00f3_Olot_AEMET.csv",
            "Precipitació_Olot_AEMET.csv",
            "PrecipitaciÃ³_Olot_AEMET.csv",
        ],
    }

    for target, names in variants.items():
        target_path = entrada_dir / target
        if target_path.exists():
            expected[target] = target_path
            continue

        for name in names:
            candidate = entrada_dir / name
            if candidate.exists():
                if "#U00f3" in name or "Ã" in name:
                    candidate.rename(target_path)
                else:
                    shutil.copy2(candidate, target_path)
                expected[target] = target_path
                break

    return expected


def print_summary(paths: dict, expected: dict) -> None:
    print("PROJECT ROOT:", paths["root"].resolve().as_posix())
    print("ENTRADA_DIR:", paths["entrada"].resolve().as_posix())
    print("RESULTATS_DIR:", paths["resultats"].resolve().as_posix())
    print("UTILS_DIR:", paths["utils"].resolve().as_posix())

    print("\nCSV d'entrada:")
    for name, path in expected.items():
        if path is None:
            print(f"  MISSING -> {name}")
        else:
            print(f"  OK -> {path.name}")

    if any(v is None for v in expected.values()):
        print("\nAVÍS: Copia els CSV originals a dades/entrada i torna a executar.")
    else:
        print("\nOK -> Setup complet.")


if __name__ == "__main__":
    root = get_project_root()
    paths = ensure_dirs(root)
    expected = normalize_inputs(paths["entrada"])
    print_summary(paths, expected)
