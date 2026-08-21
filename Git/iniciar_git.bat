@echo off
:: O %~dp0 pega a pasta onde este arquivo .bat esta localizado
set "SCRIPT_PATH=%~dp0jasko.ps1"

:: Executa o powershell chamando o script que esta na mesma pasta do .bat
powershell -NoExit -ExecutionPolicy Bypass -File "%SCRIPT_PATH%"