# Python aplicat a QGIS – METEOCAT + AEMET

## Objectiu
Estandarditzar dades de precipitació de METEOCAT i AEMET amb Python de QGIS, reutilitzar codi amb utilitats pròpies i acabar visualitzant el resultat dins QGIS.

## Estructura del projecte
- dades/entrada: CSV d’entrada
- resultats: CSV de sortida i GeoPackage final
- exercicis: scripts didàctics (cada pas genera una sortida)
- utils: funcions reutilitzables (config, CSV, parseig, CRS)

## Flux recomanat d’execució
### Fase 0 – Bootstrap (crear i provar utils)
1. [exercicis/00_bootstrap/ex01_setup_project.py](exercicis/00_bootstrap/ex01_setup_project.py)
2. [exercicis/00_bootstrap/ex02_utils_config.py](exercicis/00_bootstrap/ex02_utils_config.py)
3. [exercicis/00_bootstrap/ex03_test_config.py](exercicis/00_bootstrap/ex03_test_config.py)
4. [exercicis/00_bootstrap/ex04_utils_csv_utils.py](exercicis/00_bootstrap/ex04_utils_csv_utils.py)
5. [exercicis/00_bootstrap/ex05_test_preview_csv.py](exercicis/00_bootstrap/ex05_test_preview_csv.py)
6. [exercicis/00_bootstrap/ex06_utils_parse_utils.py](exercicis/00_bootstrap/ex06_utils_parse_utils.py)
7. [exercicis/00_bootstrap/ex07_test_parse_utils.py](exercicis/00_bootstrap/ex07_test_parse_utils.py)
8. [exercicis/00_bootstrap/ex08_utils_qgis_utils.py](exercicis/00_bootstrap/ex08_utils_qgis_utils.py)
9. [exercicis/00_bootstrap/ex09_test_qgis_transform.py](exercicis/00_bootstrap/ex09_test_qgis_transform.py)
10. [exercicis/00_bootstrap/ex10_utils_processing_utils.py](exercicis/00_bootstrap/ex10_utils_processing_utils.py)
11. [exercicis/00_bootstrap/ex11_test_processing_utils.py](exercicis/00_bootstrap/ex11_test_processing_utils.py)
12. [exercicis/00_bootstrap/ex12_utils_gui_utils.py](exercicis/00_bootstrap/ex12_utils_gui_utils.py)
13. [exercicis/00_bootstrap/ex13_test_gui_utils.py](exercicis/00_bootstrap/ex13_test_gui_utils.py)

### Fase 1 – METEOCAT
14. [exercicis/01_meteocat/ex01_peek.py](exercicis/01_meteocat/ex01_peek.py)
15. [exercicis/01_meteocat/ex02_select_columns.py](exercicis/01_meteocat/ex02_select_columns.py)
16. [exercicis/01_meteocat/ex03_clean_numbers.py](exercicis/01_meteocat/ex03_clean_numbers.py)
17. [exercicis/01_meteocat/ex04_filter_coords.py](exercicis/01_meteocat/ex04_filter_coords.py)
18. [exercicis/01_meteocat/ex05_normalize_dates.py](exercicis/01_meteocat/ex05_normalize_dates.py)
19. [exercicis/01_meteocat/ex06_transform_crs.py](exercicis/01_meteocat/ex06_transform_crs.py)
20. [exercicis/01_meteocat/ex07_standardize.py](exercicis/01_meteocat/ex07_standardize.py)

### Fase 2 – AEMET
21. [exercicis/02_aemet/ex01_peek.py](exercicis/02_aemet/ex01_peek.py)
22. [exercicis/02_aemet/ex02_despivot.py](exercicis/02_aemet/ex02_despivot.py)
23. [exercicis/02_aemet/ex03_build_dates.py](exercicis/02_aemet/ex03_build_dates.py)
24. [exercicis/02_aemet/ex04_precip_units.py](exercicis/02_aemet/ex04_precip_units.py)
25. [exercicis/02_aemet/ex05_transform_coords.py](exercicis/02_aemet/ex05_transform_coords.py)
26. [exercicis/02_aemet/ex06_standardize.py](exercicis/02_aemet/ex06_standardize.py)

### Fase 3 – Fusió i visualització a QGIS
27. [exercicis/03_merge_export/ex01_merge.py](exercicis/03_merge_export/ex01_merge.py)
28. [exercicis/03_merge_export/ex02_export_gpkg.py](exercicis/03_merge_export/ex02_export_gpkg.py)

### Fase 4 – Risc (Processing)
29. [exercicis/04_risc_processing/ex01_thresholds.py](exercicis/04_risc_processing/ex01_thresholds.py)
30. [exercicis/04_risc_processing/ex02_episodes.py](exercicis/04_risc_processing/ex02_episodes.py)
31. [exercicis/04_risc_processing/ex03_episode_summary.py](exercicis/04_risc_processing/ex03_episode_summary.py)
32. [exercicis/04_risc_processing/ex04_hotspots_heatmap.py](exercicis/04_risc_processing/ex04_hotspots_heatmap.py)
33. [exercicis/04_risc_processing/ex05_export_risc_gpkg.py](exercicis/04_risc_processing/ex05_export_risc_gpkg.py)

### Fase 5 – QGIS UI
34. [exercicis/05_qgis_ui/ex01_load_and_group.py](exercicis/05_qgis_ui/ex01_load_and_group.py)
35. [exercicis/05_qgis_ui/ex02_apply_symbology.py](exercicis/05_qgis_ui/ex02_apply_symbology.py)
36. [exercicis/05_qgis_ui/ex03_add_fields_flags.py](exercicis/05_qgis_ui/ex03_add_fields_flags.py)
37. [exercicis/05_qgis_ui/ex04_select_export_selection.py](exercicis/05_qgis_ui/ex04_select_export_selection.py)
38. [exercicis/05_qgis_ui/ex05_memory_layer_digitize.py](exercicis/05_qgis_ui/ex05_memory_layer_digitize.py)
39. [exercicis/05_qgis_ui/ex06_buffer_and_export.py](exercicis/05_qgis_ui/ex06_buffer_and_export.py)
40. [exercicis/05_qgis_ui/ex07_quick_validation_report.py](exercicis/05_qgis_ui/ex07_quick_validation_report.py)
41. [exercicis/05_qgis_ui/ex08_export_layout_pdf_optional.py](exercicis/05_qgis_ui/ex08_export_layout_pdf_optional.py)

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
- Recomanat: comença per ex01_setup_project i segueix l’ordre del flux.
- Si estàs a la carpeta del projecte, un exemple seria:
	exec(open("exercicis\\00_bootstrap\\ex01_setup_project.py", encoding="utf-8").read())

## Camí curt per veure la capa a QGIS
Si vols arribar ràpid a la visualització final (sense fer tots els previews), executa:
1) exercicis/01_meteocat/ex02_select_columns.py
2) exercicis/01_meteocat/ex03_clean_numbers.py
3) exercicis/01_meteocat/ex04_filter_coords.py
4) exercicis/01_meteocat/ex05_normalize_dates.py
5) exercicis/01_meteocat/ex06_transform_crs.py
6) exercicis/01_meteocat/ex07_standardize.py
7) exercicis/02_aemet/ex02_despivot.py
8) exercicis/02_aemet/ex03_build_dates.py
9) exercicis/02_aemet/ex04_precip_units.py
10) exercicis/02_aemet/ex05_transform_coords.py
11) exercicis/02_aemet/ex06_standardize.py
12) exercicis/03_merge_export/ex01_merge.py
13) exercicis/03_merge_export/ex02_export_gpkg.py
