# OBJECTIU:
#   Crear un resum per episode_id (inici, final, durada, màxim, suma, nombre de dies).
#
# ENTRADA:
#   resultats/risc_precipitacio_olot.gpkg (capa episodis_alerta_20mm)
#
# SORTIDA:
#   resultats/risc_precipitacio_olot.gpkg (taula episodis_resum_20mm)
#
# QUÈ APRENEM:
#   - Agregar estadístiques per grup.
#   - Crear una taula sense geometria.
#   - Fer un preview de resultats a consola.

import os  # Per gestionar rutes
import sys  # Per ajustar el path d'importació
from datetime import datetime  # Per dates

# Afegim la carpeta arrel del projecte al sys.path
ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

# Imports de QGIS
from qgis.core import QgsVectorLayer, QgsField, QgsFeature, QgsFields, QgsProject
from qgis.PyQt.QtCore import QVariant

# Importem configuració i utilitats
from utils.config import RISC_GPKG_OUT, RISC_LAYER_EPISODIS_20, RISC_LAYER_RESUM_20, RESULTATS_DIR
from utils.csv_utils import ensure_dir
from utils.parse_utils import to_float
from utils.processing_utils import export_layer_to_gpkg

# Assegurem la carpeta de resultats
ensure_dir(RESULTATS_DIR)

# Carreguem la capa d’episodis
uri = f"{RISC_GPKG_OUT}|layername={RISC_LAYER_EPISODIS_20}"
layer = QgsVectorLayer(uri, "episodis_alerta_20mm", "ogr")

if not layer.isValid():
    print("ERROR -> No s'ha pogut carregar la capa episodis_alerta_20mm.")
else:
    # Diccionari per acumular estadístiques per episode_id
    stats = {}

    for feat in layer.getFeatures():
        episode_id = feat["episode_id"]
        date_str = feat["date"]
        precip = to_float(feat["precip_mm"])

        try:
            date_obj = datetime.fromisoformat(date_str).date()
        except:
            continue

        if episode_id not in stats:
            stats[episode_id] = {
                "start": date_obj,
                "end": date_obj,
                "max": precip if precip is not None else 0,
                "sum": precip if precip is not None else 0,
                "n": 1
            }
        else:
            stats[episode_id]["start"] = min(stats[episode_id]["start"], date_obj)
            stats[episode_id]["end"] = max(stats[episode_id]["end"], date_obj)
            if precip is not None:
                stats[episode_id]["max"] = max(stats[episode_id]["max"], precip)
                stats[episode_id]["sum"] += precip
            stats[episode_id]["n"] += 1

    # Creem una capa sense geometria per al resum
    out_layer = QgsVectorLayer("None", "episodis_resum_20mm", "memory")
    fields = QgsFields()
    fields.append(QgsField("episode_id", QVariant.Int))
    fields.append(QgsField("start_date", QVariant.String))
    fields.append(QgsField("end_date", QVariant.String))
    fields.append(QgsField("duration_days", QVariant.Int))
    fields.append(QgsField("max_precip", QVariant.Double))
    fields.append(QgsField("sum_precip", QVariant.Double))
    fields.append(QgsField("n_days", QVariant.Int))
    out_layer.dataProvider().addAttributes(fields)
    out_layer.updateFields()

    # Afegim features de resum
    for episode_id in sorted(stats.keys()):
        s = stats[episode_id]
        duration = (s["end"] - s["start"]).days + 1

        feat = QgsFeature(out_layer.fields())
        feat.setAttributes([
            episode_id,
            s["start"].isoformat(),
            s["end"].isoformat(),
            duration,
            s["max"],
            s["sum"],
            s["n"]
        ])
        out_layer.dataProvider().addFeature(feat)

    # Exportem la taula al GeoPackage
    export_layer_to_gpkg(out_layer, RISC_GPKG_OUT, RISC_LAYER_RESUM_20)

    # Afegim la taula al projecte (si QGIS ho permet)
    QgsProject.instance().addMapLayer(out_layer)

    # Preview per consola (primeres 10 files)
    print("Preview episodis_resum_20mm (primeres 10 files):")
    count = 0
    for episode_id in sorted(stats.keys()):
        s = stats[episode_id]
        duration = (s["end"] - s["start"]).days + 1
        print({
            "episode_id": episode_id,
            "start_date": s["start"].isoformat(),
            "end_date": s["end"].isoformat(),
            "duration_days": duration,
            "max_precip": s["max"],
            "sum_precip": s["sum"],
            "n_days": s["n"]
        })
        count += 1
        if count == 10:
            break

    print(f"OK -> Taula creada: {RISC_LAYER_RESUM_20}")
    print(f"Nombre d’episodis resumits: {len(stats)}")
