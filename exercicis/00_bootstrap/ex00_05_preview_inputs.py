"""Exercici 0.5 — Preview de dades (5 files).

Objectiu:
- Mostrar capçaleres i 5 files de Meteocat i AEMET.
- Avisar clarament si falta algun fitxer.
"""

from pathlib import Path

# (Ja explicat abans: import) Reutilitzem rutes i utilitats del paquet tools.
from tools import config
from tools.csv_utils import preview_csv

meteocat = Path(config.METEOCAT_INPUT)
aemet = Path(config.AEMET_INPUT)

# Fem una llista d'inputs que falten per donar un avis clar.
missing = []
if not meteocat.exists():
    missing.append(str(meteocat))
if not aemet.exists():
    missing.append(str(aemet))

if missing:
    print("AVÍS -> Falten fitxers d'entrada:")
    for p in missing:
        print("  -", p)
    print("SOLUCIÓ -> Copia els CSV originals a dades/entrada i torna a provar.")

preview_csv(meteocat, max_rows=5, title="Preview METEOCAT")
preview_csv(aemet, max_rows=5, title="Preview AEMET")

print("OK -> Preview completat.")
