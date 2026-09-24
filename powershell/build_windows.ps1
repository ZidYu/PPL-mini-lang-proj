param(
    [switch] $OneFile
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)

Set-Location $Root

$PyInstallerAvailable = $false

try {
    python -c "import PyInstaller" 2>$null
    if ($LASTEXITCODE -eq 0) {
        $PyInstallerAvailable = $true
    }
} catch {
    $Error.Clear()
}

if (-not $PyInstallerAvailable) {
    python -m pip install --upgrade pyinstaller
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to install PyInstaller."
    }
}

$PyInstallerArgs = @("--name", "mini", "--console", "main.py")

if ($OneFile) {
    $PyInstallerArgs = @("--onefile") + $PyInstallerArgs
}

python -m PyInstaller @PyInstallerArgs
if ($LASTEXITCODE -ne 0) {
    throw "PyInstaller build failed."
}

if ($OneFile) {
    Write-Host "Built dist\mini.exe"
} else {
    Write-Host "Built dist\mini\mini.exe"
}
