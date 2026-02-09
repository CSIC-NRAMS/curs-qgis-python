"""Utilitats CSV per al curs (lectura, escriptura i preview)."""

# Aquest mòdul reuneix funcions petites i reutilitzables per treballar amb CSV.
# (Ja explicat abans: mòdul)

import csv
from contextlib import contextmanager
from pathlib import Path
from typing import Optional, Union


def ensure_dir(path: Union[str, Path]) -> None:
    """Crea la carpeta si no existeix (paths de fitxer o carpeta)."""
    # (Ja explicat abans: Path)
    p = Path(path)
    if p.suffix:
        p = p.parent
    p.mkdir(parents=True, exist_ok=True)


def _open_text_for_read(path: Union[str, Path], encoding: str):
    """Obre un fitxer amb encoding i fa fallback a utf-8-sig si hi ha BOM."""
    # Obrim el fitxer amb codificació; si falla, provem un encoding alternatiu.
    try:
        return open(path, "r", encoding=encoding, newline="")
    except UnicodeDecodeError:
        if encoding.lower() != "utf-8-sig":
            return open(path, "r", encoding="utf-8-sig", newline="")
        raise


@contextmanager
def open_csv_reader(path: Union[str, Path], encoding: str = "utf-8"):
    """Obre un CSV com a DictReader (context manager)."""
    # (Primer cop: context manager) Permet obrir/tancar el fitxer automàticament amb "with".
    f = _open_text_for_read(path, encoding=encoding)
    try:
        yield csv.DictReader(f, delimiter=",")
    finally:
        f.close()


@contextmanager
def open_csv_writer(path: Union[str, Path], fieldnames, encoding: str = "utf-8"):
    """Obre un CSV per escriure amb capçaleres (context manager)."""
    # Escriure CSV amb capçaleres assegura un esquema consistent per a cada pas.
    ensure_dir(path)
    f = open(path, "w", encoding=encoding, newline="")
    try:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        yield writer
    finally:
        f.close()


def preview_csv(path: Union[str, Path], max_rows: int = 5, title: Optional[str] = "") -> None:
    """Mostra columnes i les primeres files d'un CSV.

    - No carrega tot el fitxer a memòria.
    - Gestiona encoding amb fallback.
    - Si el fitxer no existeix, mostra un missatge didàctic.
    """
    if title:
        print(title)

    # Validem l'existència del fitxer per donar un missatge clar si falta.
    p = Path(path)
    if not p.exists():
        print(f"AVÍS -> No existeix el fitxer: {p}")
        print("SOLUCIÓ -> Copia el CSV a dades/entrada i torna-ho a provar.")
        print("-" * 60)
        return

    # Llegim només unes quantes files per no carregar-ho tot a memòria.
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
