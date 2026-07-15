@echo off
setlocal
set INPUT=%~1
if "%INPUT%"=="" set INPUT=\\dlowenas\paper-proof-grader\DROP_PAPERS_HERE
set OUTPUT=\\dlowenas\paper-proof-grader\OUTPUT\fruits_of_spirit

python "%~dp0fruits_of_spirit_bridge.py" --input "%INPUT%" --output "%OUTPUT%" --pattern "*.md" --no-excel
pause



