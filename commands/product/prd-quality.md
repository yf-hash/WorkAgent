---
name: prd-quality
description: PRD 质量自检（5 维度评分：完整性 30%/可测性 25%/可量化 20%/边界明确 15%/数据支撑 10%）。通用 PRD 评分。
user-invocable: true
argument-hint: "<PRD 文件路径>"
allowed-tools: [Read, Write, Edit]
---

# /prd-quality — PRD 通用质量自检

加载技能：`skills/prd-quality-check/SKILL.md`

## 用法

```bash
/prd-quality ./docs/PRD-v1.md
```

## 与其他评估命令的边界

- 5 维度通用评分：**本命令**
- 23 节企业模板差距分析：`/prd-deep-evaluate`
