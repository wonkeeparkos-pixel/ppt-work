@echo off
title FBT cafe collector
set "PY=C:\Users\wonkee01\AppData\Local\Programs\Python\Python312\python.exe"
if not exist "%PY%" set "PY=py -3.12"
%PY% "%~dp0fbt_collector.py" %*
if /i not "%~1"=="--auto" pause
