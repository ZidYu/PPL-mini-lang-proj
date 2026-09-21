@echo off
setlocal

set "MINI_DIR=%~dp0"
start "Mini Language" cmd /k ""%MINI_DIR%mini.cmd" %*"
