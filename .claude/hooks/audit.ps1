# audit.ps1 - PowerShell version

$ErrorActionPreference = 'Continue'
$input_json = [Console]::In.ReadToEnd()

try {
    $data = $input_json | ConvertFrom-Json
} catch {
    exit 0
}

$auditDir = '.claude/audit'
if (-not (Test-Path $auditDir)) {
    New-Item -ItemType Directory -Force -Path $auditDir | Out-Null
}

$today = Get-Date -Format 'yyyy-MM-dd'
$logFile = Join-Path $auditDir "$today.log"
$timestamp = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ')

$tool = if ($data.tool_name) { $data.tool_name } else { '?' }
$result = if ($data.tool_response.error) { 'err' } else { 'ok' }

$ti = $data.tool_input
$parts = @()
foreach ($k in @('file_path', 'command', 'pattern', 'url', 'prompt')) {
    $v = $ti.$k
    if ($v) {
        $s = ($v.ToString() -replace "`n", ' ')
        if ($s.Length -gt 120) { $s = $s.Substring(0, 120) }
        $parts += "$k=$s"
    }
}
$summary = $parts -join ' '

"$timestamp tool=$tool result=$result $summary" | Out-File -FilePath $logFile -Append -Encoding UTF8
exit 0
