# OBJECTIU:
#   Crear episodis d’alerta (dies consecutius) per a llindar 20 mm.
#
# ENTRADA:
#   resultats/risc_precipitacio_olot.gpkg (capa dies_alerta_20mm)
#   o capa base per generar-la si no existeix.
#
# SORTIDA:
#   resultats/risc_precipitacio_olot.gpkg (capa episodis_alerta_20mm)
#
# QUÈ APRENEM:
#   - Ordenar per data i detectar salts > 1 dia.
#   - Crear un camp episode_id.
#   - Exportar capes amb nou camp.

import os  # Per gestionar rutes
import sys  # Per ajustar el path d'importació
from datetime import datetime  # Per treballar amb dates

# Afegim la carpeta arrel del projecte al sys.path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

# Imports de QGIS
from qgis.core import (
    QgsVectorLayer, QgsProject, QgsField, QgsFields, QgsFeature
)
from qgis.PyQt.QtCore import QVariant

# Importem configuració i utilitats
from utils.config import (
    MERGED_STD_OUT, GPKG_OUT, GPKG_LAYER, RESULTATS_DIR,
    RISC_GPKG_OUT, RISC_LAYER_ALERTA_20, RISC_LAYER_EPISODIS_20
)
from utils.csv_utils import ensure_dir
from utils.processing_utils import extract_by_expression, export_layer_to_gpkg

# Assegurem la carpeta de resultats
ensure_dir(RESULTATS_DIR)

# Funció per carregar la capa base de punts
def load_base_points_layer():
    if os.path.exists(GPKG_OUT):
        uri = f"{GPKG_OUT}|layername={GPKG_LAYER}"
        layer = QgsVectorLayer(uri, "precip_std_points", "ogr")
        if layer.isValid():
            return layer
    if os.path.exists(MERGED_STD_OUT):
        uri = f"file:///{MERGED_STD_OUT}?delimiter=,&xField=lon&yField=lat&crs=EPSG:4326"
        layer = QgsVectorLayer(uri, "precip_std_points", "delimitedtext")
        if layer.isValid():
            return layer
    return None

# Funció per carregar o crear la capa de dies d’alerta (>=20 mm)
def load_or_create_alerta_20():
    # Intentem carregar del GPKG de risc
    if os.path.exists(RISC_GPKG_OUT):
        uri = f"{RISC_GPKG_OUT}|layername={RISC_LAYER_ALERTA_20}"
        layer = QgsVectorLayer(uri, "dies_alerta_20mm", "ogr")
        if layer.isValid():
            return layer

    # Si no existeix, la creem a partir de la capa base
    base_layer = load_base_points_layer()
    if base_layer is None:
        return None

    expr = "\"precip_mm\" >= 20"
    alert_layer = extract_by_expression(base_layer, expr)

    # Exportem i retornem
    export_layer_to_gpkg(alert_layer, RISC_GPKG_OUT, RISC_LAYER_ALERTA_20)
    return alert_layer

# Carreguem la capa d’alerta 20 mm
alert_layer = load_or_create_alerta_20()
if alert_layer is None:
    print("ERROR -> No s'ha pogut obtenir la capa dies_alerta_20mm.")
else:
    # Preparem el camp nou episode_id
    new_fields = QgsFields()
    for f in alert_layer.fields():
        new_fields.append(f)
    new_fields.append(QgsField("episode_id", QVariant.Int))

    # Creem la capa de sortida en memòria
    out_layer = QgsVectorLayer("Point?crs=EPSG:4326", "episodis_alerta_20mm", "memory")
    out_layer.dataProvider().addAttributes(new_fields)
    out_layer.updateFields()

    # Construïm una llista de features amb (station_id, date, feature)
    feats = []
    for feat in alert_layer.getFeatures():
        station_id = feat["station_id"]
        date_str = feat["date"]
        try:
            date_obj = datetime.fromisoformat(date_str).date()
        except:
            # Si la data no és vàlida, la saltem
            continue
        feats.append((station_id, date_obj, feat))

    # Ordenem per estació i data
    feats.sort(key=lambda x: (x[0], x[1]))

    # Comptadors
    episode_id = 0
    last_date_by_station = {}
    current_episode_by_station = {}
    total_days = 0
    first_date = None
    last_date = None

    # Iterem i creem episodis
    for station_id, date_obj, feat in feats:
        if station_id not in last_date_by_station:
            episode_id += 1
            current_episode_by_station[station_id] = episode_id
        else:
            gap = (date_obj - last_date_by_station[station_id]).days
            if gap > 1:
                episode_id += 1
                current_episode_by_station[station_id] = episode_id

        # Actualitzem la data anterior
        last_date_by_station[station_id] = date_obj

        # Actualitzem dates globals
        first_date = date_obj if first_date is None else min(first_date, date_obj)
        last_date = date_obj if last_date is None else max(last_date, date_obj)

        # Creem la nova feature amb episode_id
        new_feat = QgsFeature(out_layer.fields())
        new_feat.setGeometry(feat.geometry())
        attrs = feat.attributes() + [current_episode_by_station[station_id]]
        new_feat.setAttributes(attrs)
        out_layer.dataProvider().addFeature(new_feat)
        total_days += 1

    # Exportem la capa amb episodis
    export_layer_to_gpkg(out_layer, RISC_GPKG_OUT, RISC_LAYER_EPISODIS_20)

    # Afegim la capa al projecte
    QgsProject.instance().addMapLayer(out_layer)

    # Missatges finals
    print(f"OK -> Capa episodis creada: {RISC_LAYER_EPISODIS_20}")
    print(f"Nombre d’episodis: {episode_id}")
    print(f"Nombre de dies en alerta: {total_days}")
    print(f"Dates primer/últim episodi: {first_date} / {last_date}")
