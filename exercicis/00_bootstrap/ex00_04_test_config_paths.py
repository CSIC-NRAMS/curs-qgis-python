"""Exercici 0.4 — Test de config mínim viable.

Objectiu:
- Importar tools.config.
- Mostrar les 4 rutes base.
- Avisar si falten carpetes (sense crear-les automàticament).
"""

# (Primer cop: import) Importar vol dir portar codi d'un altre fitxer.
from pathlib import Path

try:
    from tools import config
except Exception as exc:
    print("ERROR -> No s'ha pogut importar tools.config")
    print("Causa probable:", exc)
    print("SOLUCIÓ -> Verifica Project Home i l'estructura de carpetes.")
    raise

print("ROOT_DIR:", config.ROOT_DIR)
print("DADES_DIR:", config.DADES_DIR)
print("ENTRADA_DIR:", config.ENTRADA_DIR)
print("RESULTATS_DIR:", config.RESULTATS_DIR)

# Comprovem que les carpetes existeixen
entrada = Path(config.ENTRADA_DIR)
resultats = Path(config.RESULTATS_DIR)

if not entrada.exists():
    print("AVÍS -> No existeix dades/entrada")
    print("SOLUCIÓ -> Crea la carpeta des del panell Navegador de QGIS.")

if not resultats.exists():
    print("AVÍS -> No existeix resultats")
    print("SOLUCIÓ -> Crea la carpeta des del panell Navegador de QGIS.")

print("OK -> Config mínim validat.")
