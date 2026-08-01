#!/usr/bin/env bash
# post-write-backup.sh — Write/Edit 前自动备份已有文件
#
# 作为 PreToolUse hook 匹配 Write/Edit，如果目标文件已存在，先复制到 .claude/backups/
# 便于误覆盖时回滚

set -euo pipefail

input="$(cat)"
file_path="$(echo "$input" | python -c 'import json,sys; d=json.load(sys.stdin); print(d.get("tool_input",{}).get("file_path",""))' 2>/dev/null || echo "")"

if [ -z "$file_path" ] || [ ! -f "$file_path" ]; then
  exit 0
fi

# 排除的路径（无需备份）
case "$file_path" in
  */node_modules/*|*/.git/*|*/dist/*|*/build/*|*/.claude/backups/*|*/.claude/audit/*)
    exit 0
    ;;
esac

# 生成备份路径：.claude/backups/YYYY-MM-DD/relative-path.HHMMSS
backup_dir=".claude/backups/$(date +%Y-%m-%d)"
timestamp="$(date +%H%M%S)"
rel_path="${file_path#./}"
backup_path="$backup_dir/${rel_path}.${timestamp}"

mkdir -p "$(dirname "$backup_path")"
cp "$file_path" "$backup_path" 2>/dev/null || true

exit 0
