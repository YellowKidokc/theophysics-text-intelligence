@echo off
setlocal
set INPUT=C:\Users\lowes\OneDrive\Desktop\genesis-to-quantum
set OUTPUT=%~dp0OUTPUT\manual_docker_run
mkdir "%OUTPUT%" 2>nul

docker run --rm -v "%INPUT%:/data/input:ro" -v "%OUTPUT%:/data/output" theophysics/paper-intelligence:gtq-all25-20260507-191530 grade --pattern "gtq-*.html"
if errorlevel 1 pause & exit /b 1

docker run --rm -v "%OUTPUT%:/data/output" theophysics/paper-intelligence:gtq-all25-20260507-191530 report
pause

