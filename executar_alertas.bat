@echo off
setlocal

cd /d "%~dp0"

if exist ".venv\Scripts\python.exe" (
    set "PYTHON=.venv\Scripts\python.exe"
) else if exist "venv\Scripts\python.exe" (
    set "PYTHON=venv\Scripts\python.exe"
) else (
    set "PYTHON=python"
)

echo Verificando vencimentos...
"%PYTHON%" manage.py check_vencimentos

if errorlevel 1 (
    echo.
    echo O comando terminou com erro.
    exit /b 1
)

echo.
echo Verificacao concluida com sucesso.

endlocal