# harness-context-inject.ps1 - PowerShell version

$ErrorActionPreference = 'Continue'
$input_json = [Console]::In.ReadToEnd()

try {
    $data = $input_json | ConvertFrom-Json
    $prompt = $data.prompt
} catch {
    exit 0
}

if ([string]::IsNullOrEmpty($prompt) -or -not $prompt.StartsWith('/')) {
    exit 0
}

if ($prompt -match '^/([a-z][a-z0-9-]+)') {
    $cmdName = $Matches[1]
} else {
    exit 0
}

$repoRoot = (Get-Location).Path
$commandsDir = Join-Path $repoRoot 'commands'
$candidates = Get-ChildItem -Path $commandsDir -Recurse -Filter "$cmdName.md" -ErrorAction SilentlyContinue
if ($candidates.Count -eq 0) {
    exit 0
}
$cmdFile = $candidates[0].FullName

try {
    $text = Get-Content $cmdFile -Raw -Encoding UTF8
} catch {
    exit 0
}

if ($text -notmatch '(?s)^---\r?\n(.*?)\r?\n---\r?\n') {
    exit 0
}
$fm = $Matches[1]

if ($fm -notmatch '(?m)^harness:$') {
    exit 0
}

$lines = $fm -split "`n"
$startIdx = -1
for ($i = 0; $i -lt $lines.Count; $i++) {
    if ($lines[$i].TrimEnd() -eq 'harness:') {
        $startIdx = $i
        break
    }
}
if ($startIdx -eq -1) { exit 0 }

$endIdx = $lines.Count
for ($i = $startIdx + 1; $i -lt $lines.Count; $i++) {
    if ($lines[$i].Length -gt 0 -and -not $lines[$i].StartsWith(' ') -and -not $lines[$i].StartsWith("`t")) {
        $endIdx = $i
        break
    }
}
$harness = ($lines[$startIdx..($endIdx - 1)] -join "`n")

function Grab([string]$text, [string]$pattern) {
    if ($text -match $pattern) { return $Matches[1].Trim() }
    return '?'
}

$preset = Grab $harness '(?m)^    preset:\s*(\S+)'
$profile = Grab $harness '(?m)^    profile:\s*(\S+)'
$loopMode = Grab $harness '(?m)^    mode:\s*([\w-]+)'
$scope = Grab $harness '(?m)^    scope:\s*(\S+)'
$danger = Grab $harness '(?m)^    danger-level:\s*(\S+)'

$ctx = "[HARNESS] User invoked /$cmdName, harness metadata:`n" +
       "- execute.preset: $preset`n" +
       "- constrain.profile: $profile`n" +
       "- loop.mode: $loopMode`n" +
       "- memory.scope: $scope`n" +
       "- security.danger-level: $danger`n`n" +
       "Follow this constraint: only use preset-allowed tools, respect profile gates, decide looping per loop.mode, decide re-confirmation per danger-level. Full rules in .claude/harness/."

$output = @{ additionalContext = $ctx } | ConvertTo-Json -Compress
[Console]::Out.WriteLine($output)
exit 0
