# Python aplicat a QGIS – METEOCAT + AEMET

## Objectiu
Estandarditzar dades de precipitació de METEOCAT i AEMET amb Python de QGIS, reutilitzar codi amb utilitats pròpies i acabar visualitzant el resultat dins QGIS.

## Estructura del projecte
- dades/entrada: CSV d’entrada
- resultats: CSV de sortida i GeoPackage final
- exercicis: scripts didàctics (cada pas genera una sortida)
- utils: funcions reutilitzables (config, CSV, parseig, CRS)

## Flux recomanat d’execució
### Fase 0 – Utilitats i configuració
1. [exercicis/ex00_config.py](exercicis/ex00_config.py)
2. [exercicis/ex00_utils_preview.py](exercicis/ex00_utils_preview.py)
3. [exercicis/ex00_utils_parse.py](exercicis/ex00_utils_parse.py)
4. [exercicis/ex00_utils_qgis.py](exercicis/ex00_utils_qgis.py)

### Fase 1 – METEOCAT
5. [exercicis/ex01_peek_meteocat.py](exercicis/ex01_peek_meteocat.py)
6. [exercicis/ex02_subselect_pas1.py](exercicis/ex02_subselect_pas1.py)
7. [exercicis/ex03_neteja_numeros_pas2.py](exercicis/ex03_neteja_numeros_pas2.py)
8. [exercicis/ex04_filtra_coordenades_pas2b.py](exercicis/ex04_filtra_coordenades_pas2b.py)
9. [exercicis/ex04_dates_pas3.py](exercicis/ex04_dates_pas3.py)
10. [exercicis/ex05_transformacio_crs_pas4.py](exercicis/ex05_transformacio_crs_pas4.py)
11. [exercicis/ex06_final_estandarditzat.py](exercicis/ex06_final_estandarditzat.py)

### Fase 2 – AEMET
12. [exercicis/ex07_peek_aemet.py](exercicis/ex07_peek_aemet.py)
13. [exercicis/ex08_aemet_despivot_pas1.py](exercicis/ex08_aemet_despivot_pas1.py)
14. [exercicis/ex09_aemet_dates_pas2.py](exercicis/ex09_aemet_dates_pas2.py)
15. [exercicis/ex10_aemet_precip_pas3.py](exercicis/ex10_aemet_precip_pas3.py)
16. [exercicis/ex11_aemet_coords_pas4.py](exercicis/ex11_aemet_coords_pas4.py)
17. [exercicis/ex12_aemet_estandarditza.py](exercicis/ex12_aemet_estandarditza.py)

### Fase 3 – Fusió i visualització a QGIS
18. [exercicis/ex13_merge_std.py](exercicis/ex13_merge_std.py)
19. [exercicis/ex14_export_gpkg.py](exercicis/ex14_export_gpkg.py)

## Notes didàctiques
- Cada exercici genera un CSV nou i fa un preview de 5 files per veure el canvi.
- Les funcions reutilitzables viuen a utils/ i s’importen des dels exercicis.
- La visualització final es fa dins QGIS amb una capa de punts i export a GeoPackage.

## Resultat final esperat
- CSV combinat a resultats: precipitacio_olot_estandarditzada.csv
- GeoPackage a resultats: precipitacio_olot_estandarditzada.gpkg

## Resolució de problemes
- Si el CSV no es carrega com a capa, comprova que té columnes lon i lat i que estan plenes.
- Si la capa surt buida, revisa que el fitxer resultats/precipitacio_olot_estandarditzada.csv existeix.
- Si QGIS no troba el fitxer, revisa les rutes a utils/config.py i que la carpeta dades/entrada sigui correcta.
- Si la transformació falla, comprova que les coordenades UTM són números vàlids.

## Execució a la consola de QGIS
- Obre QGIS i ves a la consola Python.
- Executa un script amb: exec(open("ruta\al\script.py", encoding="utf-8").read())
- Recomanat: comença per ex00_config i segueix l’ordre del flux.
- Si estàs a la carpeta del projecte, un exemple seria:
	exec(open("exercicis\\ex01_peek_meteocat.py", encoding="utf-8").read())

## Camí curt per veure la capa a QGIS
Si vols arribar ràpid a la visualització final (sense fer tots els previews), executa:
1) exercicis/ex02_subselect_pas1.py
2) exercicis/ex03_neteja_numeros_pas2.py
3) exercicis/ex04_filtra_coordenades_pas2b.py
4) exercicis/ex04_dates_pas3.py
5) exercicis/ex05_transformacio_crs_pas4.py
6) exercicis/ex06_final_estandarditzat.py
7) exercicis/ex08_aemet_despivot_pas1.py
8) exercicis/ex09_aemet_dates_pas2.py
9) exercicis/ex10_aemet_precip_pas3.py
10) exercicis/ex11_aemet_coords_pas4.py
11) exercicis/ex12_aemet_estandarditza.py
12) exercicis/ex13_merge_std.py
13) exercicis/ex14_export_gpkg.py
