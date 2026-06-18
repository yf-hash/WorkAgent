---
name: bid-analyze
description: 标书 Phase 1 招标文件深度拆解。三色标记（🔴 废标 / 🟡 高分 / 🔵 基础）+ 技术要求清单。
user-invocable: true
argument-hint: "<招标文件路径>"
allowed-tools: [Read, Write, Edit, AskUserQuestion]
---

# /bid-analyze — 标书 Phase 1 拆解

加载技能：`skills/bid-analyze/SKILL.md`

## 用法

```bash
/bid-analyze ./RFP.docx
```

## 流程

```
Phase 1 → 2（澄清）→ 3（大纲）→ 4（写作）→ 5（评审）→ 6（核查）→ 7（移交）
```
