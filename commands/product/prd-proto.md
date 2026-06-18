---
name: prd-proto
description: 线框图 + PRD 融合。ASCII 线框图标注规范、4 种状态（默认/空/加载/错误）必须覆盖、保真度提升路径。
user-invocable: true
argument-hint: "<需求描述> [--fidelity low|mid] [--lang zh|en]"
allowed-tools: [Read, Write, Edit, AskUserQuestion]
---

# /prd-proto — 线框图 + PRD 融合

加载技能：`skills/prd-proto/SKILL.md`

## 用法

```bash
/prd-proto 新用户注册引导流程
/prd-proto SaaS 仪表盘改版 --fidelity mid
```

## 输出

```markdown
# [功能名] — 原型 + PRD 文档

## 1. 视觉原型
### 1.1 页面/视图清单
### 1.2 各页面线框图（默认/空/加载/错误 4 种状态）
### 1.3 核心交互流程（Mermaid）
### 1.4 UI 规格

## 2. PRD（嵌入线框图）
```

## 衔接

- 配 `/prd-standard` 或 `/prd-spec-first --stage design` 使用
- 高保真原型用 `/design-proto`
