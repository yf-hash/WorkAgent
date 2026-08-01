---
name: style-refine
description: 以风格卡片为基准，对已有文章做风格优化（不重写）。先基线评分，再用 proven_solutions 策略定向修改。
user-invocable: true
argument-hint: "<文档路径> [--style-card <路径>] [--mode quality|humanize|balance] [--target-score 85] [--max-rounds 3]"
allowed-tools: [Read, Write, Edit, AskUserQuestion]
harness:
  execute:
    preset: writing-scoped
  constrain:
    profile: writing-safe
    gates: [before-write]
  loop:
    mode: iterative
    max-iterations: 4
  memory:
    scope: project
    reads: [project-context]
  security:
    danger-level: low
---

# /style-refine — 已有内容风格优化

加载技能：`skills/writing/style-refine/SKILL.md`

## 用法

```bash
/style-refine ./articles/draft.md --style-card ./styles/my-style.md
/style-refine ./articles/draft.md --mode humanize
```

## 与 `/style-create` 的边界

- 从零创作：`/style-create`
- 已有文章风格校准（不改事实）：**本命令**
