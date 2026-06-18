---
name: prd-spec-first
description: Spec-First 四件套规格（proposal/specs/design/tasks）。AI/研发写代码前先对齐规格，含四阶段质量门控。
user-invocable: true
argument-hint: "<需求描述> [--stage propose|spec|design|tasks|full] [--output inline|dir] [--lang zh|en]"
allowed-tools: [Read, Write, Edit, AskUserQuestion]
---

# /prd-spec-first — Spec-First 四件套

加载技能：`skills/prd-spec-first/SKILL.md`

## 用法

```bash
/prd-spec-first 用户可以在 App 内直接购买会员              # 完整四件套
/prd-spec-first 搜索功能增加 AI 智能推荐 --stage propose   # 仅 proposal
/prd-spec-first 第三方登录集成 --stage tasks               # 仅 tasks
/prd-spec-first New onboarding flow --output dir --lang en
```

## 阶段速查

| stage | 输出 | 适用场景 |
|---|---|---|
| `propose` | proposal.md | 立项对齐、需求评审 |
| `spec` | specs/ 目录 | 研发交付、测试设计 |
| `design` | design.md（与 `/prd-proto` 配合）| 设计对接、原型评审 |
| `tasks` | tasks.md | Sprint 规划、工程执行 |
| `full` | 完整四件套（**默认**）| 新功能完整启动 |
