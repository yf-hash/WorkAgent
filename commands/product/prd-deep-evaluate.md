---
name: prd-deep-evaluate
description: PRD 23 节深度评估，三层（方向/结构/细节）差距分析。基于 templates/prd-template.md 企业模板。
user-invocable: true
argument-hint: "<PRD 文件路径>"
allowed-tools: [Read, Write, Edit]
---

# /prd-deep-evaluate — PRD 23 节深度评估

加载技能：`skills/prd/prd-deep-evaluate/SKILL.md`

## 用法

```bash
/prd-deep-evaluate ./docs/PRD-v1.md
```

## 与 `/prd-quality` 的边界

- 通用 5 维度评分：`/prd-quality`
- 基于 23 节企业模板差距分析：**本命令**
