param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]] $MiniArgs
)

$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$OneFileExe = Join-Path $Root "dist\mini.exe"
$OneDirExe = Join-Path $Root "dist\mini\mini.exe"
$Python = Get-Command python -ErrorAction SilentlyContinue

if ($Python) {
    & $Python.Source (Join-Path $Root "main.py") @MiniArgs
    exit $LASTEXITCODE
}

if (Test-Path $OneFileExe) {
    & $OneFileExe @MiniArgs
    exit $LASTEXITCODE
}

if (Test-Path $OneDirExe) {
    & $OneDirExe @MiniArgs
    exit $LASTEXITCODE
}

Write-Error "Python was not found and no packaged Mini executable is available."
exit 9009
