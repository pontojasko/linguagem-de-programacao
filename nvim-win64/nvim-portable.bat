@echo off
set "XDG_CONFIG_HOME=%~dp0config"
set "XDG_DATA_HOME=%~dp0data"
set "NVIM_APPNAME=nvim"
"%~dp0bin\nvim.exe" %*
