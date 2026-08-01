#!/usr/bin/env bash
# pre-write-sensitive-guard.sh — 阻止 Write/Edit 到敏感路径
#
# Claude Code hook 契约：
#   stdin: JSON { "tool_input": { "file_path": "...", ... }, ... }
#   exit 0 = 放行；exit 2 = 拒绝并把 stderr 反馈给模型；其他 = 提示错误

set -euo pipefail

input="$(cat)"
file_path="$(echo "$input" | python -c 'import json,sys; d=json.load(sys.stdin); print(d.get("tool_input",{}).get("file_path",""))' 2>/dev/null || echo "")"

if [ -z "$file_path" ]; then
  exit 0
fi

# 敏感路径清单（正则）
sensitive_patterns=(
  '\.claude/settings\.json$'
  '\.claude/settings\.local\.json$'
  '\.git/(hooks|config|refs)/'
  '\.env(\.[a-z]+)?$'
  '~/\.ssh/'
  '/etc/'
  '^C:\\Windows\\System32'
  '/id_rsa$'
  '/id_ed25519$'
  '\.pem$'
  '\.key$'
)

for pat in "${sensitive_patterns[@]}"; do
  if echo "$file_path" | grep -qE "$pat"; then
    echo "SECURITY: 拦截写入敏感路径：$file_path（匹配 $pat）" >&2
    echo "如确需修改，请使用 AskUserQuestion 显式确认，或临时禁用此 hook。" >&2
    exit 2
  fi
done

exit 0
