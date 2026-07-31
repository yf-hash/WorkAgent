---
name: prd-lite
description: 一页纸 PRD（背景/用户/方案/指标/不在范围），10-15 分钟内完成。适合早期想法对齐、立项前沟通。
user-invocable: true
argument-hint: "<需求描述> [--lang zh|en]"
allowed-tools: [Read, Write, Edit, AskUserQuestion]
---

# /prd-lite — 一页纸 PRD

加载技能：`skills/prd/prd-lite/SKILL.md`

## 用法

```bash
/prd-lite 用户可以查看自己的消费明细和账单
/prd-lite 电商 App 增加"一键复购"功能
```

## 与其他 PRD 命令的边界

| 场景 | 推荐 |
|---|---|
| 1 页对齐方向 | **本命令** |
| 标准 8 章 PRD | `/prd-standard` |
| Spec-First 四件套 | `/prd-spec-first` |
| 含线框图 | `/prd-proto` |
| B 端严格 12 章 | `/pm-prd-enterprise` |
| 对话式渐进引导（想法模糊）| `/prd-diagnose` → `/prd-concept` → `/prd-impl` |
