---
name: table-from-text
description: 层级文本 / 缩进文本 → 多格式表格（YAML/JSON/CSV/HTML/Excel/Markdown）。基于 text2table。
user-invocable: true
argument-hint: "<input.txt> [--format yaml|json|csv|html|excel|markdown] [--output output.xxx]"
allowed-tools: [Read, Write, Edit, Bash]
---

# /table-from-text — 层级文本转表格

加载技能：`skills/table-from-text/SKILL.md`

## 用法

```bash
/table-from-text ./outline.txt --format markdown
/table-from-text ./outline.txt --format excel --output data.xlsx
```
