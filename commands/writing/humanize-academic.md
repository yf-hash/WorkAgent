---
name: humanize-academic
description: 学术文本深度强化（30 条高级学术去痕指令，9 大类）。适用顶刊投稿、学位论文、严格 AI 检测。
user-invocable: true
argument-hint: "[filepath|text]"
allowed-tools: [Read, Write, Edit]
---

# /humanize-academic — 学术深度强化

加载技能：`skills/humanizer-academic/SKILL.md`

## 前置

必须先做 `/humanize-scan` + `/humanize-soul`。

## 用法

```bash
/humanize-academic ./papers/draft.md
```

## 适用

顶刊投稿、学位论文、严格 AI 检测（Turnitin/GPTZero/Originality.ai）。
