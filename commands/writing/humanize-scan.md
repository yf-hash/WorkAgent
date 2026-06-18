---
name: humanize-scan
description: AI 痕迹扫描去除（29 种 AI 模式 + 中文高频词 + 7 项句式微策略 + 中文排版校正）。
user-invocable: true
argument-hint: "[filepath|text] [--intensity low|medium|high]"
allowed-tools: [Read, Write, Edit]
---

# /humanize-scan — AI 痕迹扫描

加载技能：`skills/humanizer-scan/SKILL.md`

## 用法

```bash
/humanize-scan ./articles/draft.md --intensity high
```

## 衔接

```
扫描后必跑：/humanize-soul（灵魂注入）
学术场景额外：/humanize-academic
```
