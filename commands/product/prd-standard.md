---
name: prd-standard
description: 标准 PRD（8 章模板：概述/用户场景/功能规格/非功能需求/指标体系/发布计划/风险依赖/变更记录）。Given/When/Then 验收。
user-invocable: true
argument-hint: "<需求描述> [--lang zh|en]"
allowed-tools: [Read, Write, Edit, AskUserQuestion]
---

# /prd-standard — 标准 PRD

加载技能：`skills/prd-standard/SKILL.md`

## 用法

```bash
/prd-standard 开发一个 AI 写作助手浏览器插件
```

## 与其他 PRD 命令的边界

| 场景 | 推荐 |
|---|---|
| 1 页对齐方向 | `/prd-lite` |
| 标准 8 章 PRD | **本命令** |
| Spec-First 四件套 | `/prd-spec-first` |
| 含线框图 | `/prd-proto` |
| B 端严格 12 章 | `/pm-prd-enterprise` |
| LLM/Agent/RAG 类 AI 功能 | `@ai-product-architect` |
