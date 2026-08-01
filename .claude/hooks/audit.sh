#!/usr/bin/env bash
# audit.sh — 通用 PostToolUse 审计日志
#
# 记录每次工具调用到 .claude/audit/YYYY-MM-DD.log
# 建议只对 danger-level=high 的场景启用（避免噪声）

set -euo pipefail

input="$(cat)"
audit_dir=".claude/audit"
mkdir -p "$audit_dir"

log_file="$audit_dir/$(date +%Y-%m-%d).log"
timestamp="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

tool="$(echo "$input" | python -c 'import json,sys; d=json.load(sys.stdin); print(d.get("tool_name",""))' 2>/dev/null || echo "?")"
result="$(echo "$input" | python -c 'import json,sys; d=json.load(sys.stdin); r=d.get("tool_response",{}); print("ok" if not r.get("error") else "err")' 2>/dev/null || echo "?")"

# 只记录关键字段，避免日志爆炸
summary="$(echo "$input" | python -c '
import json, sys
d = json.load(sys.stdin)
ti = d.get("tool_input", {})
# 提取有意义的关键字段
keys = ["file_path", "command", "pattern", "url", "prompt"]
parts = []
for k in keys:
    v = ti.get(k)
    if v:
        s = str(v)[:120].replace("\n", " ")
        parts.append(f"{k}={s}")
print(" ".join(parts))
' 2>/dev/null || echo "")"

echo "$timestamp tool=$tool result=$result $summary" >> "$log_file"

exit 0
