"""Utilitats mínimes per previsualitzar CSV (sense dependències externes)."""

import csv
from pathlib import Path
from typing import Optional, Union


def _open_text_for_read(path: Union[str, Path], encoding: str):
    """Obre un fitxer amb encoding i fa fallback a utf-8-sig si hi ha BOM."""
    try:
        return open(path, "r", encoding=encoding, newline="")
    except UnicodeDecodeError:
        if encoding.lower() != "utf-8-sig":
            return open(path, "r", encoding="utf-8-sig", newline="")
        raise


def preview_csv(path: Union[str, Path], max_rows: int = 5, title: Optional[str] = "") -> None:
    """Mostra columnes i les primeres files d'un CSV.

    - No carrega tot el fitxer a memòria.
    - Gestiona encoding amb fallback.
    - Si el fitxer no existeix, mostra un missatge didàctic.
    """
    if title:
        print(title)

    p = Path(path)
    if not p.exists():
        print(f"AVÍS -> No existeix el fitxer: {p}")
        print("SOLUCIÓ -> Copia el CSV a dades/entrada i torna-ho a provar.")
        print("-" * 60)
        return

    with _open_text_for_read(p, encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=",")

        print("Columnes:")
        fieldnames = list(reader.fieldnames) if reader.fieldnames else []
        print(fieldnames)

        print(f"Primeres {max_rows} files:")
        for i, row in enumerate(reader):
            print(row)
            if i >= max_rows - 1:
                break

    print("-" * 60)
