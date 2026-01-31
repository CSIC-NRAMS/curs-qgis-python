"""Funcions reutilitzables per netejar números i dates."""

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
