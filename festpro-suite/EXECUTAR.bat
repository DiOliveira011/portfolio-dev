@echo off
chcp 65001 >nul
title FestPro Suite
setlocal
set "APPDIR=%~dp0"
set "VENV=%LOCALAPPDATA%\portfolio-venvs\festpro-suite"
set "PYEXE=%VENV%\Scripts\python.exe"

if not exist "%PYEXE%" (
  echo.
  echo ============================================================
  echo  Primeira execucao: preparando o ambiente Python.
  echo  Isso baixa as dependencias e pode demorar alguns minutos.
  echo ============================================================
  echo.
  set "PYLAUNCHER=python"
  where py >nul 2>nul && set "PYLAUNCHER=py -3"
  %PYLAUNCHER% -m venv "%VENV%"
  if not exist "%PYEXE%" (
    echo.
    echo ERRO: nao consegui criar o ambiente Python.
    echo Instale o Python 3.12+ de https://www.python.org/downloads/ e tente de novo.
    echo.
    pause
    exit /b 1
  )
  "%PYEXE%" -m pip install --upgrade pip
  "%PYEXE%" -m pip install -r "%APPDIR%requirements.txt"
)

echo.
echo Abrindo a FestPro Suite no navegador...
echo (Para encerrar, feche esta janela.)
echo.
"%PYEXE%" -m streamlit run "%APPDIR%app.py"
pause
