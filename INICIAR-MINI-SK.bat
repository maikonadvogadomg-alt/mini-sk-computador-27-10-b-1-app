@echo off
chcp 65001 >nul
cd /d "%~dp0"
title Mini SK - ligando
if not exist "ferramentas" mkdir "ferramentas"
set "PY=%~dp0ferramentas\python\python.exe"

if exist "%PY%" goto temnode
echo.
echo   Primeira vez: baixando o Python portatil (uns 11 MB). Espere...
powershell -NoProfile -ExecutionPolicy Bypass -Command "$ProgressPreference='SilentlyContinue'; [Net.ServicePointManager]::SecurityProtocol=[Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -UseBasicParsing 'https://www.python.org/ftp/python/3.12.7/python-3.12.7-embed-amd64.zip' -OutFile 'ferramentas\py.zip'; Expand-Archive -Force 'ferramentas\py.zip' 'ferramentas\python'; Remove-Item 'ferramentas\py.zip'"
if not exist "%PY%" goto semnet

:temnode
where node >nul 2>nul && goto atalho
if exist "%~dp0ferramentas\node\node.exe" goto atalho
echo   Baixando o Node portatil (npm e node para o terminal), uns 30 MB. Espere...
powershell -NoProfile -ExecutionPolicy Bypass -Command "$ProgressPreference='SilentlyContinue'; [Net.ServicePointManager]::SecurityProtocol=[Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -UseBasicParsing 'https://nodejs.org/dist/v22.11.0/node-v22.11.0-win-x64.zip' -OutFile 'ferramentas\node.zip'; Expand-Archive -Force 'ferramentas\node.zip' 'ferramentas'; if (Test-Path 'ferramentas\node') { Remove-Item -Recurse -Force 'ferramentas\node' }; Rename-Item 'ferramentas\node-v22.11.0-win-x64' 'node'; Remove-Item 'ferramentas\node.zip'"
if not exist "%~dp0ferramentas\node\node.exe" echo   (Nao consegui baixar o Node. O Mini SK abre igual; so o npm do terminal nao vai funcionar.)

:atalho
powershell -NoProfile -ExecutionPolicy Bypass -Command "$a=[Environment]::GetFolderPath('Desktop')+'\Mini SK.lnk'; if (!(Test-Path $a)) { $s=(New-Object -ComObject WScript.Shell).CreateShortcut($a); $s.TargetPath='%~dp0INICIAR-MINI-SK.bat'; $s.WorkingDirectory='%~dp0'; $s.IconLocation='%SystemRoot%\System32\shell32.dll,13'; $s.Save() }" >nul 2>nul

"%PY%" "%~dp0abrir.py"
if errorlevel 1 pause
exit /b

:semnet
echo.
echo   Nao consegui baixar o Python. Confira a internet e abra de novo.
pause
