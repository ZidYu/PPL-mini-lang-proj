param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]] $MiniArgs
)

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Launcher = Join-Path $Root "mini.cmd"
$Arguments = @("/k", "`"$Launcher`"") + $MiniArgs

Start-Process -FilePath "cmd.exe" -ArgumentList $Arguments
