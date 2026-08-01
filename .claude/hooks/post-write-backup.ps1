# post-write-backup.ps1 - PowerShell version

$ErrorActionPreference = 'Continue'
$input_json = [Console]::In.ReadToEnd()

try {
    $data = $input_json | ConvertFrom-Json
    $filePath = $data.tool_input.file_path
} catch {
    exit 0
}

if ([string]::IsNullOrEmpty($filePath) -or -not (Test-Path $filePath -PathType Leaf)) {
    exit 0
}

$excludePatterns = @('[/\\]node_modules[/\\]', '[/\\]\.git[/\\]', '[/\\]dist[/\\]',
                     '[/\\]build[/\\]', '[/\\]\.claude[/\\]backups[/\\]',
                     '[/\\]\.claude[/\\]audit[/\\]')
foreach ($p in $excludePatterns) {
    if ($filePath -match $p) { exit 0 }
}

$today = Get-Date -Format 'yyyy-MM-dd'
$ts = Get-Date -Format 'HHmmss'
$backupDir = ".claude/backups/$today"
$relPath = $filePath -replace '^\.[/\\]', ''
$backupPath = Join-Path $backupDir ($relPath + ".$ts")

$parent = Split-Path $backupPath -Parent
if (-not (Test-Path $parent)) {
    New-Item -ItemType Directory -Force -Path $parent | Out-Null
}
try {
    Copy-Item -Path $filePath -Destination $backupPath -Force
} catch {
    # silent fail
}
exit 0
