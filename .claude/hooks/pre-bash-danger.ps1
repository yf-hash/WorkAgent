# pre-bash-danger.ps1 - PowerShell version

$ErrorActionPreference = 'Stop'
$input_json = [Console]::In.ReadToEnd()

try {
    $data = $input_json | ConvertFrom-Json
    $cmd = $data.tool_input.command
} catch {
    exit 0
}

if ([string]::IsNullOrEmpty($cmd)) {
    exit 0
}

# Dangerous action patterns (.NET regex syntax)
$dangers = @(
    'rm\s+-[a-z]*r[a-z]*f?\s+/',
    'rm\s+-[a-z]*r[a-z]*f?\s+~',
    'rm\s+-[a-z]*r[a-z]*f?\s+\$HOME',
    'rm\s+-[a-z]*r[a-z]*f?\s+\.\*',
    'dd\s+if=/dev/',
    'mkfs\.',
    ':\(\)\{\s*:\|:&\s*\};:',
    'git\s+push\s+.*--force.*\s+main',
    'git\s+push\s+.*--force.*\s+master',
    'chmod\s+-R\s+777\s+/',
    'curl\s+.*\|\s*(bash|sh|zsh)',
    'wget\s+.*\|\s*(bash|sh|zsh)'
)

foreach ($pat in $dangers) {
    if ($cmd -match $pat) {
        [Console]::Error.WriteLine("SECURITY: refused to execute dangerous command:")
        [Console]::Error.WriteLine("  $cmd")
        [Console]::Error.WriteLine("  matched: $pat")
        [Console]::Error.WriteLine("See .claude/harness/security/policies.md")
        exit 2
    }
}

exit 0
