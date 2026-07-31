---
name: humanize
description: 三段式 AI 去痕流水线（scan → soul → academic）。--mode scan 扫描 29 模式；--mode soul 六大人性原则灵魂注入；--mode academic 学术深度强化（30 条 9 大类）。--mode all 走完整三段。
user-invocable: true
argument-hint: "[filepath|text] --mode scan|soul|academic|all [--intensity low|medium|high] [--voice-sample <path>] [--domain <name>]"
allowed-tools: [Read, Write, Edit]
---

# /humanize — AI 去痕三段式

## 一句话

三段式流水线一个入口。`scan → soul → academic` 是推荐顺序；`--mode all` 一键跑完。

## 用法

```bash
# 三段单独跑
/humanize ./articles/draft.md --mode scan --intensity high
/humanize ./articles/cleaned.md --mode soul --domain 情感
/humanize ./papers/final.md --mode academic

# 一键三段（含 gate 提示）
/humanize ./articles/draft.md --mode all
```

## 分派规则

| `--mode` | 加载技能 | 一句话 | 前置 |
|---|---|---|---|
| `scan` | `skills/humanizer-scan/SKILL.md` | 29 种 AI 模式扫描去除 + 中文高频词 + 7 项句式微策略 + 中文排版校正 | 无 |
| `soul` | `skills/humanizer-soul/SKILL.md` | 六大人性原则 H1-H6 + 声音校准 + 33 领域情绪预设 | scan 已完成 |
| `academic` | `skills/humanizer-academic/SKILL.md` | 30 条高级学术去痕指令（9 大类），顶刊/学位论文/严格检测 | soul 已完成 |
| `all` | 依次加载三个 skill | scan → soul → academic 完整流水线，每段 gate 提示 | 无 |

## 推荐流程

```
扫描（消除机器痕迹）→ 灵魂（注入人性）→ 学术（严格检测强化）
```

- 一般文章：`--mode scan` + `--mode soul`
- 学术投稿：`--mode all`（含 academic）
- 只要清扫：`--mode scan`

## 前置校验

- `--mode soul`：若未先跑 scan，输出会含残留 AI 模式，warn 后继续
- `--mode academic`：必须先跑 scan + soul（用 AskUserQuestion 强制确认）

## 迁移说明（v2.8）

旧命令 `/humanize-scan` / `/humanize-soul` / `/humanize-academic` 已合并至本命令，用 `--mode <name>` 替代。3 个 skill 未变。

**⚠️ 与 v2.6 拆原子命令方向的取舍**：v2.6 曾拆过 `--mode` 参数化，v2.8 重新在命令层做入口合并（skills 层仍保持原子）。目的是降低命令数量、集中前置校验（scan→soul→academic 有强顺序），不再要求用户记 3 个前缀。
