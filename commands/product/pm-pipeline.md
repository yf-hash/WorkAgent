---
name: pm-pipeline
description: 端到端 6 模块流水线一键编排器 — 从一句话原始需求到技术规格书 + 归档，全流程自动化。每阶段之间有 Harness 人工卡点，PM 确认或驳回。支持从任意 stage 起跑、断点续跑、跳过某 stage。
user-invocable: true
argument-hint: "<原始需求（一句话）or 已存在的 pipeline 目录> [--from M2|M3|M4|M5|M6|M7] [--to M2|M3|M4|M5|M6|M7] [--skip-gate] [--mode auto|human] [--product-type saas-b|c-end|internal]"
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob, AskUserQuestion]
harness:
  execute:
    preset: agent-orchestrator
  constrain:
    profile: writing-safe
    gates: [before-stage, after-stage, before-freeze]
  loop:
    mode: pipeline
    stages: [M2, M3, M4, M5, M6, M7]
    gate-between: true
  memory:
    scope: project
    reads: [project-context, clarify-history, solution-history, prototype-history, tech-spec-history]
    writes: [pipeline-state]
  security:
    danger-level: low
---

# /pm-pipeline — 端到端流水线编排器

> **一句话原始需求 → 6 模块流水线 → 完整交付包**
>
> 一键调度：M2 需求澄清 → M3 业务方案 → M4 原型底稿 → M5 PRD → M6 技术规格 → M7 归档

## 一句话

**给一句话原始需求（如 "做一个邮箱验证码功能"），本命令按 6 模块顺序调度，每步之间暂停等 PM 确认，最终产出一份完整的可交付需求包**。

## 用法

### 场景 1：从零开始跑全流程

```bash
# 最简：给一句话，全流程走完
/pm-pipeline "做一个邮箱验证码功能"

# 指定模式和产品类型
/pm-pipeline "客户想批量导入发票" --mode human --product-type saas-b

# 跳过人工 gate（不推荐，仅用于快速原型验证）
/pm-pipeline "AI 合同审阅" --skip-gate --mode auto
```

### 场景 2：断点续跑

```bash
# 已经跑到 M4，从 M5 继续
/pm-pipeline ./output/pm-pipeline/invoice-import-20260827/ --from M5

# 只跑 M6（技术规格）
/pm-pipeline ./output/pm-pipeline/invoice-import-20260827/ --from M6 --to M6

# 从 M4 到 M6（跳过 M2/M3，已经存在）
/pm-pipeline ./output/pm-pipeline/xxx/ --from M4 --to M6
```

### 场景 3：局部返工

```bash
# M3 业务方案有修改，重跑 M3 → M4 → M5 → M6
/pm-pipeline ./output/pm-pipeline/xxx/ --from M3
```

## 编排逻辑

### 阶段 0：初始化

若输入是**一句话**：
1. 从需求提取 `{topic}`（≤ 20 字符，英文 slug）
2. 创建目录 `./output/pm-pipeline/{topic}-{yyyymmdd}/`
3. 初始化 `.pipeline-state.json`

若输入是**已存在目录**：
1. 读取 `.pipeline-state.json` 获取当前进度
2. 校验用户 `--from` 参数与状态一致

### `.pipeline-state.json` 内容

```json
{
  "topic": "invoice-import",
  "created_at": "2026-08-27T18:00:00+08:00",
  "raw_input": "客户想批量导入发票",
  "mode": "human",
  "product_type": "saas-b",
  "stages": {
    "M2": { "status": "done", "at": "2026-08-27T18:33:00", "output": "01-clarify-report.md" },
    "M3": { "status": "done", "at": "2026-08-27T19:05:00", "output": "02-business-solution.md" },
    "M4": { "status": "in-progress", "at": null, "output": null },
    "M5": { "status": "pending" },
    "M6": { "status": "pending" },
    "M7": { "status": "pending" }
  },
  "gates": {
    "after-M2": { "reviewed": true, "reviewer": "PM", "at": "2026-08-27T19:00:00" },
    "after-M3": { "reviewed": true, "reviewer": "PM", "at": "2026-08-27T19:30:00" },
    "after-M4": { "reviewed": false }
  }
}
```

### 阶段 1-6：顺序调度

```
M2 → gate → M3 → gate → M4 → gate → M5 → gate → M6 → gate → M7
     ↑                                                        │
     └──────  用户驳回 → 回到上一阶段  ←──────────────────────┘
```

每阶段执行：

```python
def run_stage(stage_id, state):
    # 1. 前置检查：依赖的上游产物是否就绪
    check_prerequisites(stage_id, state)

    # 2. 调用对应命令
    cmd = STAGE_COMMANDS[stage_id]
    result = invoke(cmd, args=build_args(stage_id, state))

    # 3. 更新 state
    state.stages[stage_id] = { "status": "done", "at": now(), "output": result.path }
    save_state(state)

    # 4. Harness gate：AskUserQuestion 询问
    if not skip_gate:
        answer = ask("《{name}》已生成，请审阅：\n{path}\n\n通过 / 驳回 / 编辑后继续？")
        state.gates[f"after-{stage_id}"] = record_gate(answer)

        if answer == "驳回":
            # 回到本阶段重跑
            return run_stage(stage_id, state)
        elif answer == "编辑后继续":
            # 用户手动编辑文件后按回车继续
            wait_for_edit()

    return state
```

### STAGE_COMMANDS 映射

| Stage | Command | 输入依赖 |
|---|---|---|
| M2 | `/pm-clarify {raw_input} --mode {mode} --product-type {ptype} --out {dir}/01-clarify-report.md` | raw_input |
| M3 | `/pm-solution {dir}/01-clarify-report.md --product-type {ptype} --out {dir}/02-business-solution.md` | M2 |
| M4 | `/pm-prototype {dir}/02-business-solution.md --out {dir}/03-prototype/` | M3 |
| M5 | `/prd {topic} --mode full --input {dir}/01,02,03 --validate --out {dir}/04-PRD.md` | M2/M3/M4 |
| M6 | `/pm-tech-spec {dir}/04-PRD.md --input {dir}/01,02,03 --product-type {ptype} --out {dir}/05-*.md` | M5 |
| M7 | `/pm-archive {dir}/ --bump patch` | 全部 |

## Harness 卡点行为

### `after-stage` gate 交互

```
【M2 完成】《需求澄清报告》已生成：
  ./output/pm-pipeline/invoice-import-20260827/01-clarify-report.md

关键内容速览：
  - 假设项：8 条
  - 待确认项：3 条
  - 检测到冲突：1 条（"快速上线" vs "支持十万并发"）

请选择：
  (1) 通过 → 继续 M3
  (2) 驳回 → 重跑 M2（提供修改点）
  (3) 编辑后继续 → 我手工改文件，改完按 Enter
  (4) 中止 → 停止流水线，保留当前进度
```

### `--skip-gate` 模式

- 用于快速原型验证（不推荐正式项目）
- 每阶段完成后打印摘要，不问用户
- 最终一键跑到 M7
- 状态记录 `gates.*.reviewed = false` 便于后期审计

## 输出结构（同 pm-archive）

```
./output/pm-pipeline/{topic}-{yyyymmdd}/
  ├── .pipeline-state.json    ← 【本命令维护】流水线状态
  ├── 01-clarify-report.md
  ├── 02-business-solution.md
  ├── 03-prototype/
  ├── 04-PRD.md
  ├── 04-PRD-validate.md
  ├── 05-tech-metrics.md
  ├── 05-tech-spec.md
  ├── 05-tech-spec-validate.md
  ├── README.md               ← 【M7 生成】
  ├── CHANGELOG.md            ← 【M7 生成】
  └── archive-report.md       ← 【M7 生成】
```

## 与其他命令的边界

| 场景 | 用 |
|---|---|
| **一句话 → 完整交付包** | 本命令 |
| 只需要一份 PRD | `/prd --mode full` |
| 只需要澄清报告 | `/pm-clarify` |
| 只需要技术规格 | `/pm-tech-spec`（已有 PRD） |
| 只需要归档 | `/pm-archive`（已有 6 类产物） |
| 想混合手工 + 自动 | 本命令 `--from M4 --to M6` |
| 与研发协作（写系统技术方案） | 归档后交给 `/devagent:dev-spec-dev` |

## 常见剧本

### 剧本 A：紧急客户需求（3-4 小时全流程）

```bash
/pm-pipeline "客户要 XX 功能，2 周上线" --mode human --product-type saas-b

# 每阶段 30-40 分钟，用户 gate 决策 5-10 分钟
# 总时长：3-4 小时（含审阅）
```

### 剧本 B：探索性想法（1 小时快速走）

```bash
/pm-pipeline "有个 AI 助手的想法" --mode auto --skip-gate

# auto 模式 + 跳过 gate
# 总时长：< 1 小时
# 产出物是"半成品"，需人工二次加工
```

### 剧本 C：从 PRD 补技术规格（已有 PRD 场景）

```bash
# 前提：已经有一份 PRD.md 在某目录
/pm-pipeline ./output/existing-project/ --from M6

# 只跑 M6 → M7
# 补齐技术规格 + 归档
```

### 剧本 D：客户反馈后返工 M3-M6

```bash
# 客户看了业务方案后要求改优先级
/pm-pipeline ./output/pm-pipeline/xxx/ --from M3

# 重跑 M3（覆盖旧文件）→ M4 → M5 → M6 → M7
# CHANGELOG 会记录 v1.1.0
```

## 反模式

- ❌ 用 `--skip-gate` 交付客户版——违规，gate 是质量保障
- ❌ 手动改 `.pipeline-state.json`——违规，会导致状态不一致
- ❌ 跨目录混用文件——违规，每个流水线必须独立目录
- ❌ 没跑 M6 直接跳 M7 归档——违规，M7 会拒绝

## 与 /pm 命令的关系

- `/pm` 是**总入口路由器**（智能识别命中哪个能力/剧本/命令）
- `/pm-pipeline` 是**流水线编排器**（专责 6 模块顺序调度）
- 用户说 "端到端"、"全流程需求" 时，`/pm` 会**推荐** `/pm-pipeline`
- 也可直接 `/pm-pipeline "需求"` 显式调用
