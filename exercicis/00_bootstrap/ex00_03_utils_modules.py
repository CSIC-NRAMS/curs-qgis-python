"""Exercici 0.3 — Funcions + mòduls: per què existeix tools.

Objectiu:
- Entendre què és un mòdul i per què el reutilitzem.
- Comprovar que tools/__init__.py existeix.
- Intentar importar tools.config i donar instruccions clares si falla.
"""

# (Primer cop: mòdul) Un modul es un fitxer .py que podem importar des d'altres scripts.
# (Primer cop: Path) Path ens ajuda a construir rutes de forma segura.
from pathlib import Path

# Intentem usar QGIS per trobar l'arrel del projecte (Project Home)
try:
    from qgis.core import QgsProject
except Exception:
    QgsProject = None


def print_header(text):
    # Fem un separador visual per llegir millor la sortida a consola.
    print("=" * 60)
    print(text)
    print("=" * 60)


print_header("EXERCICI 0.3 — tools i imports")

# 1) Localitzem l'arrel del projecte.
#    Si QGIS està obert, prioritzem Project Home.
root = None
if QgsProject is not None:
    try:
        home = QgsProject.instance().homePath()
        if home:
            root = Path(home)
    except Exception:
        root = None

# Fallback suau: pujem des de la ubicació de l'script
if root is None:
    root = Path(__file__).resolve().parents[2]

tools_dir = root / "tools"
init_file = tools_dir / "__init__.py"

print("Arrel del projecte:", root)
print("Carpeta tools:", tools_dir)

# 2) Comprovem que la carpeta tools existeix
if not tools_dir.exists():
    print("ERROR -> No existeix la carpeta tools")
    print("SOLUCIÓ -> Crea-la des del panell Navegador de QGIS.")
    raise SystemExit(1)

# 3) Comprovem si existeix tools/__init__.py
if not init_file.exists():
    print("ERROR -> No s'ha trobat tools/__init__.py")
    print("SOLUCIÓ -> Crea el fitxer des del panell Navegador de QGIS:")
    print("  1) Clic dret a la carpeta tools")
    print("  2) Nou fitxer")
    print("  3) Nom del fitxer: __init__.py")
    raise SystemExit(1)
else:
    print("OK -> tools/__init__.py existeix")



print("OK -> Exercici 0.3 completat.")
