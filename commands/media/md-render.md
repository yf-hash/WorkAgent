---
name: md-render
description: Markdown 转图片渲染（--format poster：mark-pic 40+ 渐变背景 / Madopic 长图含 KaTeX/Mermaid/ECharts；--format table：tablesnap / imagifier / Flask API 三选一）。
user-invocable: true
argument-hint: "<Markdown 路径或内容> --format poster|table [--tool <backend>] [--theme dark|light]"
allowed-tools: [Read, Write, Edit, Bash]
---

# /md-render — Markdown 转图

## 一句话

两个方向：文章/代码卡片 → 海报（poster），Markdown 表格 → PNG（table）。

## 用法

```bash
# 长文/代码卡片 → 海报
/md-render ./article.md --format poster --tool madopic
/md-render ./code-tip.md --format poster --tool mark-pic

# Markdown 表格 → 图片
/md-render ./data.md --format table --tool tablesnap --theme dark
```

## 分派规则

| `--format` | 加载技能 | 后端可选 |
|---|---|---|
| `poster` | `skills/md-poster/SKILL.md` | `mark-pic`（40+ 渐变） / `madopic`（长图含 KaTeX/Mermaid/ECharts） |
| `table` | `skills/md-table-image/SKILL.md` | `tablesnap`（CLI） / `imagifier`（浏览器） / `flask-api` |

## 判据

- 完整文章 / 代码片段 / 分享卡片 → `--format poster`
- 单个 Markdown 表格 → `--format table`
- 若同时有表格和长文 → 拆开分别跑

## 迁移说明（v2.8）

旧命令 `/md-poster` / `/md-table-image` 已合并至本命令，用 `--format poster|table` 替代。
