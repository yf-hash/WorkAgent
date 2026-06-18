---
name: prd-diagnose
description: 产品想法三镜诊断（用户/商业/技术）。从一句话想法开始，每次只问 1-2 个问题，对话式推进。
user-invocable: true
argument-hint: "<一句话产品想法>"
allowed-tools: [Read, Write, AskUserQuestion]
---

# /prd-diagnose — 三镜诊断

加载技能：`skills/prd-diagnose/SKILL.md`

## 用法

```bash
/prd-diagnose 想做一个面向独立设计师的素材管理工具
```

## 流程

```
诊断完成后必须等用户确认，再进入：
  → /prd-concept（概念稿）
```
