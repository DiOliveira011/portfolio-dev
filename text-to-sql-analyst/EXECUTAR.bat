@echo off
chcp 65001 >nul
title Text-to-SQL Analyst
setlocal
set "APPDIR=%~dp0"
set "VENV=%LOCALAPPDATA%\portfolio-venvs\text-to-sql-analyst"
set "PYEXE=%VENV%\Scripts\python.exe"

if not exist "%PYEXE%" (
  echo.
  echo Primeira execucao: preparando o ambiente Python...
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
echo Abrindo o Text-to-SQL Analyst... http://localhost:5005
echo (Modo IA opcional: defina ANTHROPIC_API_KEY antes de abrir.)
echo.
"%PYEXE%" "%APPDIR%app.py"
pause
