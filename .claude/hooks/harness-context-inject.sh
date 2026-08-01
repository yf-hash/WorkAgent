#!/usr/bin/env bash
# harness-context-inject.sh — 用户提交斜杠命令时，注入该命令的 harness 元数据作为上下文
#
# Claude Code UserPromptSubmit hook 契约：
#   stdin: { "prompt": "..." }
#   stdout: 若为 JSON { "additionalContext": "..." } → 注入到会话上下文
#   exit 0 放行；任何失败静默跳过
#
# 目的：不强制切 profile，只让模型看到"当前场景该用什么执行/约束/循环模式"，
# 从而在思考时自我遵循，避免误用工具。

set -eu

input="$(cat)"

# Python 处理：识别 /command，找文件，抠 harness 块，emit additionalContext
python - "$input" <<'PY' 2>/dev/null || true
import json, re, sys
from pathlib import Path

def emit(ctx=None):
    if ctx:
        print(json.dumps({"additionalContext": ctx}, ensure_ascii=False))
    sys.exit(0)

try:
    data = json.loads(sys.argv[1])
except Exception:
    emit()

prompt = (data.get("prompt") or "").strip()
if not prompt.startswith("/"):
    emit()

# 提取命令名（首个词，去除斜杠和后续空格 / 参数）
m = re.match(r"^/([a-z][a-z0-9-]+)", prompt)
if not m:
    emit()
cmd_name = m.group(1)

# 找 commands/**/cmd_name.md
root = Path(".").resolve()
candidates = list((root / "commands").rglob(f"{cmd_name}.md"))
if not candidates:
    emit()
cmd_path = candidates[0]

# 读 frontmatter
text = cmd_path.read_text(encoding="utf-8", errors="ignore")
fm_match = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", text, re.DOTALL)
if not fm_match:
    emit()
fm = fm_match.group(1)

# 抠 harness 块
lines = fm.split("\n")
start = None
for i, line in enumerate(lines):
    if line.rstrip() == "harness:":
        start = i
        break
if start is None:
    emit()

end = len(lines)
for i in range(start + 1, len(lines)):
    if lines[i] and not lines[i].startswith(" ") and not lines[i].startswith("\t"):
        end = i
        break
harness = "\n".join(lines[start:end])

# 简单解析字段
def grab(pattern):
    m = re.search(pattern, harness, re.MULTILINE)
    return m.group(1).strip() if m else "?"

preset = grab(r"^    preset:\s*(\S+)")
profile = grab(r"^    profile:\s*(\S+)")
loop_mode = grab(r"^    mode:\s*([\w-]+)")
scope = grab(r"^    scope:\s*(\S+)")
danger = grab(r"^    danger-level:\s*(\S+)")

ctx = f"""[HARNESS] 用户调用了 /{cmd_name}，harness 元数据：
- execute.preset: {preset}
- constrain.profile: {profile}
- loop.mode: {loop_mode}
- memory.scope: {scope}
- security.danger-level: {danger}

请按此约束行动：只用 preset 允许的工具、遵守 profile 的 gate、按 loop.mode 决定是否循环、按 danger-level 决定是否二次确认。完整规则见 .claude/harness/。"""

emit(ctx)
PY
