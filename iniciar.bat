@echo off
cd /d "%~dp0"
python -m pip install -r requirements.txt
if errorlevel 1 goto error
python christmas_tree.py
if errorlevel 1 goto error
exit /b 0
:error
echo Confira se o Python esta instalado e disponivel no PATH.
pause
