@echo off
py -3 --version >nul 2>nul
if %errorlevel% equ 0 (
    py -3 "%~dp0mini.py" %*
) else (
    python "%~dp0mini.py" %*
)
