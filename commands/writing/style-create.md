---
name: style-create
description: Writer-Reviewer 双 Agent 互搏迭代创作。基于风格卡片 + 标题/框架，按 quality/humanize/balance 三种模式生成。
user-invocable: true
argument-hint: "[--title <标题>] [--framework <框架>] [--style-card <路径>] [--target-score 85] [--max-rounds 3] [--mode quality|humanize|balance]"
allowed-tools: [Read, Write, Edit, WebFetch, AskUserQuestion]
---

# /style-create — 风格驱动从零创作

加载技能：`skills/style-writer-reviewer/SKILL.md`

## 用法

```bash
/style-create --title "理解 RAG 的本质" --style-card ./styles/my-style.md
/style-create --title "Agent 框架对比" --framework "起承转合" --mode humanize
```

## 前置

- 风格卡片（来自 `/style-extract`）
- 标题 + 可选框架

## 衔接

```
创作完成后必跑：
  → /humanize-scan（消除 29 模式）
  → /humanize-soul（六大人性原则注入）
```
