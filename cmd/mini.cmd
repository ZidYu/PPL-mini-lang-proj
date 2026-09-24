@echo off
setlocal

set "MINI_DIR=%~dp0..\"

if exist "%MINI_DIR%dist\mini.exe" (
    "%MINI_DIR%dist\mini.exe" %*
    exit /b %ERRORLEVEL%
)

if exist "%MINI_DIR%dist\mini\mini.exe" (
    "%MINI_DIR%dist\mini\mini.exe" %*
    exit /b %ERRORLEVEL%
)

python "%MINI_DIR%main.py" %*
exit /b %ERRORLEVEL%
