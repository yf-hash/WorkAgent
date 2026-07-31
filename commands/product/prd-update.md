---
name: prd-update
description: PRD 增量合并更新（不重写原文，只在原文上增量合并新增/变更/删除，所有变更打【本次更新】标记）。
user-invocable: true
argument-hint: "<PRD 文件路径> <要新增/变更/删除的内容描述>"
allowed-tools: [Read, Write, Edit, AskUserQuestion]
---

# /prd-update — PRD 增量更新

加载技能：`skills/prd/prd-incremental-update/SKILL.md`

## 用法

```bash
/prd-update ./docs/PRD-v1.md 新增批量导入 Excel 模板与前端预校验功能
```

## 与其他命令的边界

- 从零写新 PRD：`/prd-standard` 或 `/prd-impl`
- 评估已有 PRD：`/prd-quality` 或 `/prd-deep-evaluate`
- 增量变更：**本命令**
