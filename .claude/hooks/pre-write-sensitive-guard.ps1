# pre-write-sensitive-guard.ps1 - PowerShell version
# Equivalent to pre-write-sensitive-guard.sh, for Windows without Git Bash
# Contract: stdin JSON -> exit 0 pass / exit 2 reject + stderr message

$ErrorActionPreference = 'Stop'
$input_json = [Console]::In.ReadToEnd()

try {
    $data = $input_json | ConvertFrom-Json
    $filePath = $data.tool_input.file_path
} catch {
    exit 0
}

if ([string]::IsNullOrEmpty($filePath)) {
    exit 0
}

# Sensitive path patterns
$patterns = @(
    '\.claude[/\\]settings\.json$',
    '\.claude[/\\]settings\.local\.json$',
    '\.git[/\\](hooks|config|refs)[/\\]',
    '\.env(\.[a-z]+)?$',
    '~[/\\]\.ssh[/\\]',
    '^/etc/',
    '^C:\\Windows\\System32',
    '[/\\]id_rsa$',
    '[/\\]id_ed25519$',
    '\.pem$',
    '\.key$'
)

foreach ($pat in $patterns) {
    if ($filePath -match $pat) {
        [Console]::Error.WriteLine("SECURITY: blocked write to sensitive path: $filePath (matched $pat)")
        [Console]::Error.WriteLine("If needed, use AskUserQuestion to confirm, or temporarily disable this hook.")
        exit 2
    }
}

exit 0
