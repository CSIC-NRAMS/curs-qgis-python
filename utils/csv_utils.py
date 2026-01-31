"""Funcions reutilitzables per treballar amb CSV (sense dependències externes)."""

import csv
from contextlib import contextmanager
from pathlib import Path
from typing import Optional, Sequence, Union


def ensure_dir(path: Union[str, Path]) -> Path:
    """Crea la carpeta (o la carpeta pare si és un fitxer) i retorna el Path."""
    p = Path(path)
    dir_path = p.parent if p.suffix else p
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


def _open_text_for_read(path: Union[str, Path], encoding: str):
    """Obre un fitxer amb encoding i fallback a utf-8-sig per BOM."""
    try:
        return open(path, "r", encoding=encoding, newline="")
    except UnicodeDecodeError:
        if encoding.lower() != "utf-8-sig":
            return open(path, "r", encoding="utf-8-sig", newline="")
        raise


@contextmanager
def open_csv_reader(path: Union[str, Path], encoding: str = "utf-8", delimiter: str = ","):
    """Context manager que retorna un csv.DictReader."""
    with _open_text_for_read(path, encoding) as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        yield reader


@contextmanager
def open_csv_writer(
    path: Union[str, Path],
    fieldnames: Sequence[str],
    encoding: str = "utf-8",
    delimiter: str = ",",
):
    """Context manager que retorna un csv.DictWriter i escriu la capçalera."""
    ensure_dir(path)
    with open(path, "w", encoding=encoding, newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=delimiter)
        writer.writeheader()
        yield writer


def preview_csv(path: Union[str, Path], max_rows: int = 5, title: Optional[str] = "") -> None:
    """Mostra capçaleres i primeres files sense carregar tot el CSV."""
    if title:
        print(title)

    p = Path(path)
    if not p.exists():
        print(f"AVÍS -> No existeix el fitxer: {p}")
        return

    with open_csv_reader(p) as reader:
        print("Columnes:")
        fieldnames = list(reader.fieldnames) if reader.fieldnames else []
        print(fieldnames)

        print(f"Primeres {max_rows} files:")
        for i, row in enumerate(reader):
            print(row)
            if i >= max_rows - 1:
                break

    print("-" * 60)
