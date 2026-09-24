@echo off
setlocal

powershell -ExecutionPolicy Bypass -File "%~dp0..\powershell\build_windows.ps1" %*
exit /b %ERRORLEVEL%
