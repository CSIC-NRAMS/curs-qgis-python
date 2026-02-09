"""tools/parse_utils.py — utilitats de parseig.

Fa: convertir textos a float i dates.
Inclou: parseig de data completa i construcció de dates a partir d'any/mes/dia.
Llegeix: valors en memòria.
Escriu: res.
OK esperat: import correcte (sense errors).
"""

# Aquest mòdul centralitza conversions perquè no repetim codi als exercicis.

from datetime import datetime, date
from typing import Optional


def to_float(value) -> Optional[float]:
    """Converteix a float de manera segura (accepta comes com a separador)."""
    # (Ja explicat abans: funcio)
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
    # Acceptem diversos formats per reduir errors quan els CSV no son homogenis.
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
    """Construeix una data segura a partir d'any/mes/dia separats."""
    # Tornem None si la data es impossible (ex. 30/02).
    try:
        y = int(str(year).strip())
        m = int(str(month).strip())
        d = int(str(day).strip())
        return date(y, m, d)
    except Exception:
        return None
