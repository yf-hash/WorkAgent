---
name: prd-impl
description: PRD 实现稿（Version 2），23 节企业级模板。基于已确认的概念稿展开，自动填补常见盲区。对应 templates/prd-template.md。
user-invocable: true
argument-hint: "<已确认的概念稿路径或产品名>"
allowed-tools: [Read, Write, Edit, AskUserQuestion]
---

# /prd-impl — PRD 实现稿

加载技能：`skills/prd-implementation-draft/SKILL.md`

## 用法

```bash
/prd-impl ./docs/产品名-概念稿.md
```

## 前置

必须先 `/prd-concept` 输出且用户已确认方向。

## 输出

完整 23 节 PRD（参见 `templates/prd-template.md`）
