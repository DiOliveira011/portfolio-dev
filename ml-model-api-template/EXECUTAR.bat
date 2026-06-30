@echo off
chcp 65001 >nul
title ML Model API Template
setlocal
set "APPDIR=%~dp0"
set "VENV=%LOCALAPPDATA%\portfolio-venvs\ml-model-api-template"
set "PYEXE=%VENV%\Scripts\python.exe"
set "PYTHONPATH=%APPDIR%src"

if not exist "%PYEXE%" (
  echo.
  echo Primeira execucao: preparando o ambiente Python ^(pode demorar^)...
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

echo Treinando o modelo...
"%PYEXE%" -m mlapi.train

echo.
echo Abrindo a API... http://localhost:8000/docs
echo.
"%PYEXE%" "%APPDIR%app.py"
pause
