# OBJECTIU:
#   Presentar funcions de parseig reutilitzables (números i dates).
#
# ENTRADA:
#   Cap fitxer; només provem funcions amb exemples.
#
# SORTIDA:
#   Cap fitxer; mostrem resultats per pantalla.
#
# QUÈ APRENEM:
#   - to_float per netejar números.
#   - parse_date per dates en formats diferents.
#   - build_date per crear dates a partir d'any/mes/dia.

import os  # Per gestionar rutes
import sys  # Per ajustar el path d'importació

# Afegim la carpeta arrel del projecte al sys.path
ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

# Importem utilitats de parseig
from utils.parse_utils import to_float, parse_date, build_date

# Exemples de números
print("to_float('3,5') ->", to_float("3,5"))
print("to_float('') ->", to_float(""))
print("to_float('abc') ->", to_float("abc"))

# Exemples de dates
print("parse_date('31/12/2024') ->", parse_date("31/12/2024"))
print("parse_date('2024-12-31') ->", parse_date("2024-12-31"))
print("parse_date('31-12-2024') ->", parse_date("31-12-2024"))

# Exemples de build_date
print("build_date(2024, 2, 29) ->", build_date(2024, 2, 29))
print("build_date(2024, 2, 30) ->", build_date(2024, 2, 30))

print("OK -> Funcions de parseig provades.")
