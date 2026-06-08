Write-Host "--- nosleep Installer ---" -ForegroundColor Cyan

# Define installation directory in user profile
$installDir = Join-Path $HOME ".nosleep"
if (-not (Test-Path $installDir)) {
    New-Item -ItemType Directory -Path $installDir | Out-Null
    Write-Host "Created installation directory: $installDir"
}

# Determine if running locally or remotely
$scriptDir = $PSScriptRoot
$isLocal = $null -ne $scriptDir -and $scriptDir -ne "" -and (Test-Path (Join-Path $scriptDir "nosleep.py"))

# Copy or download files
$files = @("nosleep.py", "nosleep.bat")
foreach ($file in $files) {
    $destPath = Join-Path $installDir $file
    if ($isLocal) {
        $sourcePath = Join-Path $scriptDir $file
        Copy-Item $sourcePath -Destination $destPath -Force
        Write-Host "Copied $file from local directory."
    } else {
        # Fallback to downloading from GitHub
        $githubUser = if ($env:NOSLEEP_GH_USER) { $env:NOSLEEP_GH_USER } else { "tiktok-rick" }
        $sourceUrl = "https://raw.githubusercontent.com/$githubUser/noSleep/main/$file"
        Write-Host "$file not found locally. Fetching from $sourceUrl..." -ForegroundColor Yellow
        try {
            Invoke-WebRequest -Uri $sourceUrl -OutFile $destPath -UseBasicParsing -ErrorAction Stop
            Write-Host "Successfully downloaded $file" -ForegroundColor Green
        } catch {
            Write-Error "Failed to download $file. If installing from a fork, run: `$env:NOSLEEP_GH_USER = 'YourUsername' before installing."
            throw "Installation failed. Could not download $file."
        }
    }
}


# Add to user PATH if not already present
$pathValues = [Environment]::GetEnvironmentVariable("PATH", "User") -split ";"
if ($pathValues -notcontains $installDir) {
    Write-Host "Adding $installDir to User PATH..."
    $newPath = ($pathValues + $installDir) -join ";"
    [Environment]::SetEnvironmentVariable("PATH", $newPath, "User")
    Write-Host "PATH updated successfully. Note: You may need to restart your terminal for changes to take effect." -ForegroundColor Green
} else {
    Write-Host "Directory already in PATH." -ForegroundColor Yellow
}

Write-Host "Installation completed successfully! Run 'nosleep' in any new terminal window." -ForegroundColor Green
