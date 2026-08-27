---
name: pm-competitive
description: 竞品分析工程化能力编排器 — 一键跑完整两阶段流程（scan → benchmark），也支持 monitor 模式（月度轻量刷新）、focus 模式（只做特定维度）。作为 PM Harness 的横向能力，产出可供 /pm-clarify、/pm-solution、/prd 等主流水线阶段引用。
user-invocable: true
argument-hint: "<产品定位/客户场景> or <已有竞品分析目录> [--mode full|monitor|refresh] [--focus feature|pricing|ecosystem|voc|strategy|all] [--seed <竞品名>] [--depth quick|deep] [--our-name <我方名>] [--out <path>] [--skip-gate]"
allowed-tools: [Read, Write, Edit, Bash, WebFetch, WebSearch, Grep, Glob, AskUserQuestion]
harness:
  execute:
    preset: agent-orchestrator
  constrain:
    profile: research
    gates: [before-stage, after-stage]
  loop:
    mode: pipeline
    stages: [scan, benchmark]
    gate-between: true
  memory:
    scope: project
    reads: [project-context, competitive-history, competitive-benchmark-history]
    writes: [pipeline-state]
  security:
    danger-level: low
---

# /pm-competitive — 竞品分析工程化能力编排器

> **PM Harness 横向能力入口** — 一键跑完整两阶段流程
>
> /pm-competitive-scan → /pm-competitive-benchmark → 完整竞品分析报告

## 一句话

**给一段产品定位或客户场景，本命令自动跑完整两阶段流程**：竞品发现 + 情报采集 → 多维对标 + 差异化定位 + 应对策略，产出可用的竞品分析报告。

## 三种运行模式

### `--mode full`（默认）— 完整两阶段

```bash
# 从零开始跑
/pm-competitive "AI 写作助手，面向中小企业内容营销"

# 加种子竞品
/pm-competitive "AI 写作助手" --seed "Jasper,Copy.ai,ChatGPT,Notion AI"

# 全维度深度
/pm-competitive "AI 写作助手" --depth deep
```

### `--mode monitor`（常态跟踪）— 月度轻量刷新

```bash
# 每月轻量更新（不重跑对标，只更新情报卡的 Changelog 部分）
/pm-competitive ./output/competitive/ai-writer-{date}/ --mode monitor
```

**做什么**：
- 只跑 scan 阶段 + 追加到已有目录
- 检查各竞品 Changelog / 大新闻 / 定价变动
- 生成 `MONITOR-{yyyymm}.md` 差异报告

### `--mode refresh`（季度全量刷新）

```bash
# 完全重跑一遍
/pm-competitive ./output/competitive/ai-writer-{date}/ --mode refresh
```

**做什么**：
- 重跑 scan + benchmark 两阶段
- 与旧版本对比，生成 `DIFF-v1-v2.md`
- 版本号 minor 递增

## `--focus` 参数（只做某维度）

配合 `--mode full` 使用，跳过其他阶段：

```bash
# 只做定价对比（客户临时对比价格用）
/pm-competitive "AI 写作助手" --focus pricing

# 只出销售话术（销售培训用）
/pm-competitive ./01-competitors.json --focus strategy

# 只做功能对标（产品规划用）
/pm-competitive ./01-competitors.json --focus feature
```

## 编排逻辑

### 阶段 0：初始化

若输入是**产品定位描述**：
1. 从定位提取 `{topic-slug}`
2. 创建目录 `./output/competitive/{topic-slug}-{yyyymmdd}/`
3. 初始化 `.competitive-state.json`

若输入是**已存在目录**：
1. 读取 `.competitive-state.json`
2. 依据 --mode 判定行为（monitor / refresh / full）

### 阶段 1-2：顺序调度

```
Stage 1 (scan)              Stage 2 (benchmark)
──────────────              ────────────────────
竞品发现                     多维对标（5 维）
   ↓                            ↓
🔒 竞品清单 gate            🔒 对标结果 gate
   ↓                            ↓
信源采集                    洞察产出（5 类）
   ↓                            ↓
情报卡结构化               差异化定位
   ↓                            ↓
🔒 采集完成 gate            应对策略（4 象限）
   ↓                            ↓
输出 01-competitors.json    话术库 + FAQ
                                ↓
                            🔒 战略产出 gate
                                ↓
                            输出 02-report-full.md
```

## `.competitive-state.json` 结构

```json
{
  "topic": "AI 写作助手",
  "topic_slug": "ai-writer",
  "our_name": "我方 AI 写作助手",
  "created_at": "2026-08-27T15:00:00+08:00",
  "params": {
    "depth": "quick",
    "focus": "all"
  },
  "stages": {
    "scan": { "status": "done", "at": "2026-08-27T15:20:00", "output": "01-competitors.json" },
    "benchmark": { "status": "in-progress" }
  },
  "gates": {
    "after-scan": { "reviewed": true, "at": "2026-08-27T15:22:00" },
    "after-benchmark": { "reviewed": false }
  },
  "version": "1.0.0",
  "next_refresh": "2026-11-27",
  "monitor_history": []
}
```

## 与 PM 主流水线的关系

竞品分析是**横向能力**，可以：

1. **独立跑**：季度规划前 / 立项前 / 上线前
   ```bash
   /pm-competitive "产品定位"
   ```

2. **为 M2 提供输入**：客户提到竞品时，让澄清报告有依据
   ```bash
   /pm-competitive "客户提到 X" && /pm-clarify "..." --input ./02-report-full.md
   ```

3. **为 M3 提供输入**：业务方案的"差异化"章节有依据
   ```bash
   /pm-solution ./01-clarify-report.md --input ./competitive/xxx/02-report-full.md
   ```

4. **为 M5（PRD）提供输入**：PRD 中的"竞品对比"章节
   ```bash
   /prd --mode full --input ./01-clarify.md,./competitive/xxx/02-report-full.md
   ```

5. **常态跟踪**：Monitor 模式每月刷新一次

## Harness 卡点

### `after-scan` gate

见 `/pm-competitive-scan` 的 Gate 2。

### `after-benchmark` gate

见 `/pm-competitive-benchmark` 的 Gate 2。

### `--skip-gate` 模式

- 用于快速原型验证（不推荐正式产出）
- 每阶段完成后打印摘要，不问用户

## 输出目录结构（完整版）

```
./output/competitive/{topic-slug}-{yyyymmdd}/
├── .competitive-state.json      ← 状态
├── 01-competitor-list.md         ← 阶段 1：竞品清单
├── 01-competitors.json           ← 阶段 1：结构化情报卡集
├── 01-competitor-*.json          ← 阶段 1：每家一份详细卡
├── 01-intel-sources.md           ← 阶段 1：信源清单
├── 01-intel-log.md               ← 阶段 1：采集日志
├── 02-benchmark-matrix.md        ← 阶段 2：多维对标矩阵
├── 02-insights.md                 ← 阶段 2：5 类洞察
├── 02-positioning.md              ← 阶段 2：定位 + 布局
├── 02-strategy.md                 ← 阶段 2：应对四象限
├── 02-sales-playbook.md          ← 阶段 2：话术库 + FAQ
├── 02-report-full.md              ← 【主产出】完整报告
├── VERSION                       ← 版本号
├── CHANGELOG.md                  ← 变更历史
├── MONITOR-{yyyymm}.md           ← Monitor 模式产出
└── DIFF-v{n}-v{n+1}.md            ← Refresh 模式产出
```

## 常见剧本

### 剧本 A：立项前竞品扫描（30-60 分钟）

```bash
/pm-competitive "AI 客服助手" --depth quick

# 快速覆盖 5-8 家竞品
# 输出：报告 + 战略建议
# 时长：30-60 分钟
```

### 剧本 B：季度全量刷新（2-3 小时）

```bash
# 首次
/pm-competitive "AI 写作助手" --depth deep

# 3 个月后
/pm-competitive ./output/competitive/ai-writer-{date}/ --mode refresh
```

### 剧本 C：临时对比某个维度（10-20 分钟）

```bash
# 客户对比价格
/pm-competitive "AI 写作助手" --focus pricing

# 销售培训要话术
/pm-competitive ./01-competitors.json --focus strategy
```

### 剧本 D：常态月度跟踪

```bash
# 每月第一周跑一次
/pm-competitive ./output/competitive/ai-writer-{date}/ --mode monitor

# 输出 MONITOR-{yyyymm}.md：本月竞品动态
```

### 剧本 E：为 PM 主流水线提供输入

```bash
# 1. 先跑竞品分析
/pm-competitive "AI 写作助手"

# 2. PRD 引用竞品报告
/prd "AI 写作助手 v2" --mode full \
  --input ./output/competitive/ai-writer-{date}/02-report-full.md

# 3. PRD 中会有"竞品对比"章节，引用具体差异化
```

## 反模式

- ❌ 用 `--skip-gate` 交付客户版 —— gate 是质量红线
- ❌ 情报卡不做 JSON —— 违规，下游阶段依赖
- ❌ 常年不 refresh —— 竞品动态失效
- ❌ 忘记通知销售 / 售前更新话术 —— 战略不落地
- ❌ 用行业分析报告代替一手采集 —— 违规

## 与 SA 场景的边界

| 场景 | 用 PM 竞品命令 or SA 命令 |
|---|---|
| **内部产品线整体竞争分析** | `/pm-competitive` |
| **客户具体项目的竞争定位** | `/sa-solution-map`（含竞品章节，聚焦本项目） |
| 立项前市场判断 | `/pm-competitive` |
| 招投标应答的竞品对标 | `/sa-solution-map` + `/sa-rfp` |

**规则**：产品级竞争走 PM，项目级竞争走 SA。两者可以互相引用。
