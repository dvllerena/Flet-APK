@echo off
set "carpeta=directorio_empresas"
mkdir "%carpeta%"

setlocal enabledelayedexpansion
for %%E in (
    uneoc
    atioc
    atimac
    ati5158
    emgefoc
    eep_islajuventud
    eep_pinar
    eep_mayabeque
    eep_matanzas
    eep_sanctispiritus
    eep_ciegodeavila
    eep_camaguey
    eep_santiagodecuba
    eep_holguin
    eep_guantanamo
    cte_mariel
    cte_guiteras
    cte_cmc
    cte_10octubre
    cte_rente
) do (
    echo [ ] > "%carpeta%\directorio_%%E.json"
)
echo ✅ Archivos JSON creados en "%carpeta%"
