@echo off
title FBT desktop icon
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0make_desktop_icon.ps1"
echo.
pause
