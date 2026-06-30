@echo off
chcp 65001 >nul
title Presence Keeper
REM Abre a janela sem console (pythonw). Se nao houver, cai para py/python.
where pythonw >nul 2>nul
if %errorlevel%==0 (
  start "" pythonw "%~dp0presence_keeper.py"
  exit /b
)
where py >nul 2>nul
if %errorlevel%==0 (
  py -3 "%~dp0presence_keeper.py"
  exit /b
)
python "%~dp0presence_keeper.py"
