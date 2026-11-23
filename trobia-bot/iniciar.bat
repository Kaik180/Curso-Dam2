@echo off
chcp 65001 >nul
title Bot de trobia
cd /d "%~dp0"
echo Comprobando dependencias...
python -m pip install -r requirements.txt --quiet --disable-pip-version-check
:loop
echo Iniciando el bot de trobia...
python bot.py
echo.
echo El bot se ha detenido. Reiniciando en 5 segundos (cierra esta ventana para apagarlo)...
timeout /t 5 >nul
goto loop
