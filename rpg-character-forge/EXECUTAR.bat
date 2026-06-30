@echo off
chcp 65001 >nul
title RPG Character Forge
setlocal
set "APPDIR=%~dp0"
set "VENV=%LOCALAPPDATA%\portfolio-venvs\rpg-character-forge"
set "PYEXE=%VENV%\Scripts\python.exe"

if not exist "%PYEXE%" (
  echo.
  echo ============================================================
  echo  Primeira execucao: preparando o ambiente Python.
  echo ============================================================
  echo.
  set "PYLAUNCHER=python"
  where py >nul 2>nul && set "PYLAUNCHER=py -3"
  %PYLAUNCHER% -m venv "%VENV%"
  if not exist "%PYEXE%" (
    echo ERRO: instale o Python 3.12+ de https://www.python.org/downloads/ e tente de novo.
    pause
    exit /b 1
  )
  "%PYEXE%" -m pip install --upgrade pip
  "%PYEXE%" -m pip install -r "%APPDIR%requirements.txt"
)

echo.
echo Abrindo o RPG Character Forge... http://localhost:5002
echo (Para encerrar, feche esta janela.)
echo.
"%PYEXE%" "%APPDIR%app.py"
pause
