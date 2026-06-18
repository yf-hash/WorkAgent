---
name: md-poster
description: Markdown 转海报/分享卡片（mark-pic 40+ 渐变背景 + Madopic 长图含 KaTeX/Mermaid/ECharts）。
user-invocable: true
argument-hint: "<Markdown 路径或内容> [--tool mark-pic|madopic]"
allowed-tools: [Read, Write, Edit, Bash]
---

# /md-poster — Markdown 转海报

加载技能：`skills/md-poster/SKILL.md`

## 用法

```bash
/md-poster ./article.md --tool madopic
/md-poster ./code-tip.md --tool mark-pic
```

## 与 `/md-table-image` 的边界

- 完整文章 / 代码卡片 → **本命令**
- Markdown 表格 → PNG → `/md-table-image`
