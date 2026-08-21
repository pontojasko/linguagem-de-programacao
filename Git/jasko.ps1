# jasko.ps1
# Define os caminhos base
$baseDir = "D:\linguagem-de-programacao\Git"
$gitBin = "$baseDir\bin"
$gitCmd = "$baseDir\cmd"

# Localiza o gh.exe
$ghFile = Get-ChildItem -Path "$baseDir" -Recurse -Filter "gh.exe" | Select-Object -First 1
$ghBin = if ($ghFile) { $ghFile.DirectoryName } else { "$baseDir\git\bin" }

# FORÇA o PATH para a sessão atual
$env:Path = "$gitBin;$gitCmd;$ghBin;" + $env:Path

# Configura Git
& "$gitBin\git.exe" config --global user.name "Heitor Jasko"
& "$gitBin\git.exe" config --global user.email "heitorjaskojogos@gmail.com"
& "$gitBin\git.exe" config --global credential.helper manager

Clear-Host
Write-Host "--- JASKO ENVIRONMENT ACTIVATED ---" -ForegroundColor Cyan

# Verifica chamando os executáveis pelo caminho completo
$gitExe = "$gitBin\git.exe"
$ghExe = if ($ghFile) { $ghFile.FullName } else { "gh" }

Write-Host "Git Version: " -NoNewline; & $gitExe --version
Write-Host "GitHub CLI: " -NoNewline; & $ghExe --version
Write-Host "Status do login: " -NoNewline; & $ghExe auth status

Write-Host ""
Write-Host "Ambiente injetado! Tente digitar 'git' abaixo." -ForegroundColor Green