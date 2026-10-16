@echo off
title FBT weekly setup
set "PY=C:\Users\wonkee01\AppData\Local\Programs\Python\Python312\python.exe"
if not exist "%PY%" set "PY=py -3.12"
%PY% "%~dp0fbt_weekly.py" --install
echo.
timeout /t 60
