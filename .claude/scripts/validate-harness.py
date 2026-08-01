#!/usr/bin/env python3
"""
validate-harness.py — 校验所有 harness 块的结构合法性

不依赖 pyyaml；用简单缩进式解析（4/2 格）+ 枚举白名单。

用法：
  python .claude/scripts/validate-harness.py               # 输出所有问题
  python .claude/scripts/validate-harness.py --strict      # 遇错 exit 1
"""
from __future__ import annotations
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STRICT = "--strict" in sys.argv

# ─── 枚举白名单（应与 .claude/harness/*/*.md 保持一致）───────────
EXECUTE_PRESETS = {
    "read-only", "writing-scoped", "research", "media-heavy",
    "shell-restricted", "agent-orchestrator", "default",
}
CONSTRAIN_PROFILES = {
    "read-only", "writing-safe", "research", "media-heavy",
    "shell-restricted", "agent-orchestrator", "full-trust", "default",
}
LOOP_MODES = {"one-shot", "pipeline", "iterative", "parallel", "monitor"}
MEMORY_SCOPES = {"session", "project", "user", "agent"}
DANGER_LEVELS = {"low", "medium", "high"}
GATE_KEYS = {
    "before-write", "before-external-send", "before-destructive",
    "before-loop-restart",
}

# ─── preset ↔ allowed-tools 一致性 ────────────────────────────
# 每个 preset 下"绝对不该出现"的工具（出现即违反语义）
PRESET_FORBIDDEN_TOOLS = {
    "read-only":   {"Write", "Edit", "Bash"},
    "writing-scoped": {"Bash"},        # 除非 harness.execute.tools 显式扩展
    "research":    {"Bash"},            # 除非扩展
    "default":     {"Write", "Edit", "Bash"},
    # media-heavy / shell-restricted / agent-orchestrator 定义较宽松，不做 forbidden 检查
}

# 提取 frontmatter 里 allowed-tools 数组
ALLOWED_TOOLS_RE = re.compile(r"^allowed-tools:\s*\[([^\]]*)\]", re.MULTILINE)

# ─── frontmatter 提取 ─────────────────────────────────────────────
FRONTMATTER_RE = re.compile(r"^---\r?\n(.*?)\r?\n---\r?\n", re.DOTALL)


def extract_harness_block(fm: str) -> str | None:
    """从 frontmatter 里抠出 harness: 段"""
    lines = fm.split("\n")
    start = None
    for i, line in enumerate(lines):
        if line.rstrip() == "harness:":
            start = i
            break
    if start is None:
        return None
    # 抽到下一个 0 缩进键或结尾
    end = len(lines)
    for i in range(start + 1, len(lines)):
        line = lines[i]
        # 0 缩进且不是空行 = 到达下一个顶层键
        if line and not line.startswith(" ") and not line.startswith("\t"):
            end = i
            break
    return "\n".join(lines[start:end])


def parse_harness(block: str) -> dict:
    """极简 YAML 解析，只支持我们用的固定结构"""
    def strip_inline_comment(v: str) -> str:
        # 去掉 " # xxx" 形式的行内注释（仅当 # 前有空格）
        m = re.match(r'^([^"#]*?)\s+#.*$', v)
        return m.group(1).rstrip() if m else v

    result = {}
    lines = block.split("\n")
    # skip "harness:" line
    i = 1
    current_section = None
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        # 2 格缩进 = section key
        m = re.match(r"^  ([a-z-]+):\s*(.*)$", line)
        if m:
            current_section = m.group(1)
            value = strip_inline_comment(m.group(2).strip())
            if value:  # inline value（罕见）
                result[current_section] = value
            else:
                result[current_section] = {}
            i += 1
            continue
        # 4 格缩进 = section field
        m = re.match(r"^    ([a-z-]+):\s*(.*)$", line)
        if m and current_section:
            key = m.group(1)
            value = strip_inline_comment(m.group(2).strip())
            if isinstance(result.get(current_section), dict):
                result[current_section][key] = value
            i += 1
            continue
        # 其他缩进 = 错误
        if line.startswith(" "):
            # 记录但不报错，交给校验函数
            pass
        i += 1
    return result


def validate_file(path: Path) -> list[str]:
    """返回该文件的错误列表；空 = 无错"""
    errors = []
    text = path.read_text(encoding="utf-8")
    m = FRONTMATTER_RE.match(text)
    if not m:
        return []  # 不是 frontmatter 文件，跳过
    fm = m.group(1)

    if "harness:" not in fm:
        return []  # 没 harness 块

    block = extract_harness_block(fm)
    if block is None:
        errors.append("harness 块提取失败")
        return errors

    parsed = parse_harness(block)

    # 检查五大 section 齐全
    for section in ["execute", "constrain", "loop", "memory", "security"]:
        if section not in parsed:
            errors.append(f"缺 section: harness.{section}")

    # execute.preset
    exe = parsed.get("execute", {})
    if isinstance(exe, dict):
        preset = exe.get("preset", "").strip()
        if preset and preset not in EXECUTE_PRESETS:
            errors.append(f"execute.preset 越界: {preset!r} 不在 {sorted(EXECUTE_PRESETS)}")

    # constrain.profile
    con = parsed.get("constrain", {})
    if isinstance(con, dict):
        profile = con.get("profile", "").strip()
        if profile and profile not in CONSTRAIN_PROFILES:
            errors.append(f"constrain.profile 越界: {profile!r} 不在 {sorted(CONSTRAIN_PROFILES)}")
        # gates: 检查方括号列表内的每个 key
        gates = con.get("gates", "").strip()
        if gates.startswith("["):
            items = [x.strip() for x in gates.strip("[]").split(",") if x.strip()]
            for g in items:
                if g not in GATE_KEYS:
                    errors.append(f"constrain.gates 未知 gate: {g!r}")

    # loop.mode
    loop = parsed.get("loop", {})
    if isinstance(loop, dict):
        mode = loop.get("mode", "").strip()
        if mode and mode not in LOOP_MODES:
            errors.append(f"loop.mode 越界: {mode!r} 不在 {sorted(LOOP_MODES)}")

    # memory.scope
    mem = parsed.get("memory", {})
    if isinstance(mem, dict):
        scope = mem.get("scope", "").strip()
        if scope and scope not in MEMORY_SCOPES:
            errors.append(f"memory.scope 越界: {scope!r} 不在 {sorted(MEMORY_SCOPES)}")

    # security.danger-level
    sec = parsed.get("security", {})
    if isinstance(sec, dict):
        dl = sec.get("danger-level", "").strip()
        if dl and dl not in DANGER_LEVELS:
            errors.append(f"security.danger-level 越界: {dl!r} 不在 {sorted(DANGER_LEVELS)}")

    # 检查是否有 loop 子键错误缩进（即出现在 harness 顶层）
    top_level_keys_from_block = set()
    for line in block.split("\n")[1:]:  # skip "harness:"
        m = re.match(r"^  ([a-z-]+):\s*", line)
        if m:
            top_level_keys_from_block.add(m.group(1))
    forbidden_at_top = {"max-iterations", "gate-between", "stages",
                       "fanout", "convergence-check", "pipeline-when",
                       "pipeline-stages", "budget-tokens"}
    misplaced = top_level_keys_from_block & forbidden_at_top
    for k in misplaced:
        errors.append(f"缩进错误: {k!r} 应在 loop 下 4 格缩进，不该出现在 harness 顶层")

    # ─── preset ↔ allowed-tools 一致性 ─────────────────────
    at_match = ALLOWED_TOOLS_RE.search(fm)
    exe_preset = ""
    if isinstance(exe, dict):
        exe_preset = exe.get("preset", "").strip()

    if at_match and exe_preset in PRESET_FORBIDDEN_TOOLS:
        allowed = {t.strip() for t in at_match.group(1).split(",") if t.strip()}
        # 允许 harness.execute.tools 扩展
        exe_tools = exe.get("tools", "").strip() if isinstance(exe, dict) else ""
        extension = set()
        if exe_tools.startswith("["):
            extension = {t.strip() for t in exe_tools.strip("[]").split(",") if t.strip()}

        forbidden = PRESET_FORBIDDEN_TOOLS[exe_preset]
        violated = (allowed & forbidden) - extension
        for tool in sorted(violated):
            errors.append(
                f"preset↔allowed-tools 冲突: preset={exe_preset!r} 不该允许 {tool!r}"
                f"（如需扩展，写 harness.execute.tools: [{tool}]）"
            )

    return errors


def main():
    print(f"Root: {ROOT}\n")
    total = 0
    bad_files = 0
    total_errors = 0

    scan_dirs = [
        ("commands", "*.md"),
        ("agents", "*.md"),
        ("skills", "SKILL.md"),
    ]

    for subdir, pattern in scan_dirs:
        for p in sorted((ROOT / subdir).rglob(pattern)):
            if p.name == "README.md":
                continue
            total += 1
            errs = validate_file(p)
            if errs:
                bad_files += 1
                total_errors += len(errs)
                rel = p.relative_to(ROOT).as_posix()
                print(f"[FAIL] {rel}")
                for e in errs:
                    print(f"    - {e}")

    print(f"\n=== 汇总 ===")
    print(f"扫描: {total} 文件")
    print(f"通过: {total - bad_files}")
    print(f"问题: {bad_files} 文件 / {total_errors} 项")

    if STRICT and total_errors > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
