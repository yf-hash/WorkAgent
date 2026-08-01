#!/usr/bin/env bash
# pre-bash-danger.sh — 拦截明确危险的 Bash 命令
#
# 覆盖 harness/security/policies.md 的全局 deny list，作为 hook 层最后一道墙
# 与 settings.json 的 permissions.deny 双保险

set -euo pipefail

input="$(cat)"
cmd="$(echo "$input" | python -c 'import json,sys; d=json.load(sys.stdin); print(d.get("tool_input",{}).get("command",""))' 2>/dev/null || echo "")"

if [ -z "$cmd" ]; then
  exit 0
fi

# 危险动作正则（严格匹配，避免误伤）
danger_patterns=(
  'rm[[:space:]]+-[a-z]*r[a-z]*f?[[:space:]]+/'
  'rm[[:space:]]+-[a-z]*r[a-z]*f?[[:space:]]+~'
  'rm[[:space:]]+-[a-z]*r[a-z]*f?[[:space:]]+\$HOME'
  'rm[[:space:]]+-[a-z]*r[a-z]*f?[[:space:]]+\.\*'
  'dd[[:space:]]+if=/dev/'
  'mkfs\.'
  ':\(\)\{ :\|:& \};:'
  'git[[:space:]]+push[[:space:]]+.*--force.*[[:space:]]main'
  'git[[:space:]]+push[[:space:]]+.*--force.*[[:space:]]master'
  'chmod[[:space:]]+-R[[:space:]]+777[[:space:]]+/'
  'curl[[:space:]]+.*\|[[:space:]]*(bash|sh|zsh)'
  'wget[[:space:]]+.*\|[[:space:]]*(bash|sh|zsh)'
)

for pat in "${danger_patterns[@]}"; do
  if echo "$cmd" | grep -qE "$pat"; then
    echo "SECURITY: 拒绝执行危险命令：" >&2
    echo "  $cmd" >&2
    echo "  匹配模式：$pat" >&2
    echo "详见 .claude/harness/security/policies.md" >&2
    exit 2
  fi
done

exit 0
