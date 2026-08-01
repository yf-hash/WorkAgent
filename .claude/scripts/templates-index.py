#!/usr/bin/env python3
"""
templates-index.py — 扫描 templates/ 生成索引 + used-by 溯源

在 commands/skills/agents 里 grep template 文件名，找出谁引用了每个 template。
输出到 templates/README.md（覆盖）。
"""
from __future__ import annotations
import re
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[2]

def find_templates() -> list[Path]:
    """返回所有 templates/**.md 路径（排除 README.md 和 archive/ 目录）"""
    return sorted([
        p for p in (ROOT / "templates").rglob("*.md")
        if p.name != "README.md"
        and "archive" not in p.relative_to(ROOT / "templates").parts
    ])


def find_users(template_rel: str) -> list[str]:
    """在 commands/agents/skills 里 grep template 相对路径，返回引用者列表"""
    users = []
    # 尝试两种形式：完整路径 + 仅文件名
    template_name = Path(template_rel).name
    patterns = [template_rel, template_name]

    for scan_dir in ["commands", "agents", "skills"]:
        for p in (ROOT / scan_dir).rglob("*.md"):
            if p.name == "README.md":
                continue
            try:
                text = p.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            for pat in patterns:
                if pat in text:
                    users.append(p.relative_to(ROOT).as_posix())
                    break
    return sorted(set(users))


def main():
    templates = find_templates()
    print(f"扫描 {len(templates)} 个 template...")

    # 分组：顶层 templates/ vs templates/product/
    top_level = [t for t in templates if len(t.relative_to(ROOT / "templates").parts) == 1]
    product = [t for t in templates if len(t.relative_to(ROOT / "templates").parts) > 1]

    lines = [
        "# templates — 填充模板索引",
        "",
        f"> {len(templates)} 个静态模板，由 commands / skills / agents 通过 Read 工具按需加载。",
        "> **模板本身不带 harness 元数据**：它们是数据，不是执行组件；消费它的 command/agent 的 harness 决定执行边界。",
        "> 归档的模板见 [`archive/README.md`](archive/README.md)。",
        "",
        "## 顶层模板（通用产品 / 研发 / 销售）",
        "",
        "| 模板 | 用途 | 主要引用者 |",
        "|---|---|---|",
    ]

    for t in top_level:
        rel = t.relative_to(ROOT).as_posix()
        name = t.stem
        users = find_users(rel)
        # 只列前 3 个引用者
        users_str = "、".join(f"`{u}`" for u in users[:3]) or "—"
        if len(users) > 3:
            users_str += f"（+{len(users) - 3}）"
        lines.append(f"| [`{name}`]({t.relative_to(ROOT / 'templates').as_posix()}) | {name.replace('-template', '').replace('-', ' ')} | {users_str} |")

    lines.extend([
        "",
        "## 产品资料模板（templates/product/）",
        "",
        "由 `skills/product/product-writer-router` 按需 Read，实现 16 类产品资料的原子化。",
        "",
        "| 模板 | 主要引用者 |",
        "|---|---|",
    ])

    for t in product:
        rel = t.relative_to(ROOT).as_posix()
        name = t.stem
        users = find_users(rel)
        users_str = "、".join(f"`{u}`" for u in users[:3]) or "—"
        if len(users) > 3:
            users_str += f"（+{len(users) - 3}）"
        lines.append(f"| [`product/{name}`](product/{t.name}) | {users_str} |")

    lines.extend([
        "",
        "## 与 harness 层的关系",
        "",
        "- Template = 数据（被读的 markdown）",
        "- Command / Skill / Agent = 执行体（有 `harness:` 块）",
        "- Template 不需要 `harness:` 字段；使用它的组件的 harness 生效",
        "",
        "## 修改 template 的影响面",
        "",
        "改一个 template → 影响所有 \"主要引用者\" 列出的组件的输出。修改前对照本索引评估。",
        "",
        "## 重新生成本索引",
        "",
        "```bash",
        "python .claude/scripts/templates-index.py",
        "```",
        "",
        "扫描全仓 grep 引用关系，覆盖写入本文件。",
    ])

    output = "\n".join(lines) + "\n"
    (ROOT / "templates" / "README.md").write_text(output, encoding="utf-8", newline="\n")

    total_refs = sum(len(find_users(t.relative_to(ROOT).as_posix())) for t in templates)
    print(f"写入 templates/README.md")
    print(f"总引用数: {total_refs}")


if __name__ == "__main__":
    main()
