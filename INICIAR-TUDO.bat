@echo off
chcp 65001 >nul
title Portfolio - Iniciar todos os apps
echo.
echo Abrindo os apps (cada um em sua janela).
echo Na primeira vez, cada um prepara o ambiente (pode demorar alguns minutos).
echo O navegador abre sozinho quando ficar pronto.
echo.
start "MTG Deck Lab"         "%~dp0mtg-deck-lab\EXECUTAR.bat"
start "FestPro Suite"        "%~dp0festpro-suite\EXECUTAR.bat"
start "Finance Dashboard"    "%~dp0finance-dashboard\EXECUTAR.bat"
start "World Cup Predictor"  "%~dp0worldcup-predictor\EXECUTAR.bat"
start "Logistics Control"    "%~dp0logistics-control\EXECUTAR.bat"
start "Invest Analyzer"      "%~dp0invest-portfolio-analyzer\EXECUTAR.bat"
start "Gestao de Entregas"   "%~dp0gestao-entregas\EXECUTAR.bat"
start "RPG Character Forge"  "%~dp0rpg-character-forge\EXECUTAR.bat"
start "NF-e Extractor"       "%~dp0nfe-invoice-extractor\EXECUTAR.bat"
start "ML Model API"         "%~dp0ml-model-api-template\EXECUTAR.bat"
start "Churn Predictor"      "%~dp0churn-predictor\EXECUTAR.bat"
echo Pronto. As janelas foram abertas.
timeout /t 4 >nul
