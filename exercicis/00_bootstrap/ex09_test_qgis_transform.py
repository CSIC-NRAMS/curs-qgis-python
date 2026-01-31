# OBJECTIU:
#   Provar la utilitat de transformació de coordenades amb PyQGIS.
#
# ENTRADA:
#   Cap fitxer; només un punt d'exemple.
#
# SORTIDA:
#   Cap fitxer; mostrem lon/lat per pantalla.
#
# QUÈ APRENEM:
#   - Crear un transformador CRS.
#   - Transformar UTM 31N a WGS84.

import os  # Per gestionar rutes
import sys  # Per ajustar el path d'importació

# Afegim la carpeta arrel del projecte al sys.path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

# Importem utilitats PyQGIS
from utils.qgis_utils import get_utm31_to_wgs84_transformer, transform_utm_to_lonlat

# Coordenades d'exemple (UTM 31N)
x_utm = 228471
y_utm = 421015

# Creem el transformador
xform = get_utm31_to_wgs84_transformer()

# Transformem el punt
lon, lat = transform_utm_to_lonlat(x_utm, y_utm, xform)

print("UTM:", x_utm, y_utm)
print("WGS84:", lon, lat)
print("OK -> Transformació feta.")
