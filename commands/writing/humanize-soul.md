---
name: humanize-soul
description: AI 文本灵魂注入（六大人性原则 H1-H6 + 声音校准 + 33 领域情绪预设）。
user-invocable: true
argument-hint: "[filepath|text] [--voice-sample filepath] [--domain 领域名]"
allowed-tools: [Read, Write, Edit]
---

# /humanize-soul — 灵魂注入

加载技能：`skills/humanizer-soul/SKILL.md`

## 前置

必须已 `/humanize-scan`（消除 29 模式）。

## 用法

```bash
/humanize-soul ./articles/cleaned.md
/humanize-soul ./articles/cleaned.md --domain 情感
/humanize-soul ./articles/cleaned.md --voice-sample ./my-voice/sample.txt
```
