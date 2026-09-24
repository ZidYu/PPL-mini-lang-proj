param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]] $MiniArgs
)

$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$OneFileExe = Join-Path $Root "dist\mini.exe"
$OneDirExe = Join-Path $Root "dist\mini\mini.exe"

if (Test-Path $OneFileExe) {
    & $OneFileExe @MiniArgs
    exit $LASTEXITCODE
}

if (Test-Path $OneDirExe) {
    & $OneDirExe @MiniArgs
    exit $LASTEXITCODE
}

& python (Join-Path $Root "main.py") @MiniArgs
exit $LASTEXITCODE
