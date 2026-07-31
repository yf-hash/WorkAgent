---
name: style-extract
description: 从 1-5 篇优质文章提炼共性写作风格，输出标准化「风格卡片」。7 维度分析（开篇/结构/节奏/过渡/结尾/语言/案例）。
user-invocable: true
argument-hint: "<urls 列表> [--save-card <路径>]"
allowed-tools: [Read, Write, WebFetch]
---

# /style-extract — 风格卡片提炼

加载技能：`skills/writing/style-card-extractor/SKILL.md`

## 用法

```bash
/style-extract https://mp.weixin.qq.com/s/xxx1 https://example.com/article2
/style-extract <urls> --save-card ./styles/my-style.md
```

## 衔接

```
风格卡片确认后：
  → /style-create（从零创作）
  → /style-refine（已有内容风格优化）
```
