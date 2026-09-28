@echo off
setlocal

set "MINI_DIR=%~dp0..\"

where python >nul 2>nul
if not errorlevel 1 (
    python "%MINI_DIR%main.py" %*
    exit /b %ERRORLEVEL%
)

if exist "%MINI_DIR%dist\mini.exe" (
    "%MINI_DIR%dist\mini.exe" %*
    exit /b %ERRORLEVEL%
)

if exist "%MINI_DIR%dist\mini\mini.exe" (
    "%MINI_DIR%dist\mini\mini.exe" %*
    exit /b %ERRORLEVEL%
)

echo Python was not found and no packaged Mini executable is available.
exit /b 9009
