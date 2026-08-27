---
name: sa-pipeline
description: 端到端 7 模块售前流水线一键编排器 — 从一句话原始客户信息到完整售前包（方案 + POC + RFP 应答 + 报价 + 归档），全流程自动化。每阶段之间有 Harness 人工卡点，售前确认或驳回。支持从任意 stage 起跑、断点续跑、变更触发下游重跑。
user-invocable: true
argument-hint: "<原始客户输入 or 已存在的 pipeline 目录> [--from M1|M2|M3|M4|M5|M6|M7] [--to M1|M2|M3|M4|M5|M6|M7] [--stage-5 poc|impl|rfp|all] [--client <名称>] [--industry <行业>] [--compliance <逗号分隔>] [--deployment private|public|hybrid] [--skip-gate]"
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob, AskUserQuestion]
harness:
  execute:
    preset: agent-orchestrator
  constrain:
    profile: writing-safe
    gates: [before-stage, after-stage, before-freeze]
  loop:
    mode: pipeline
    stages: [M1, M2, M3, M4, M5, M6, M7]
    gate-between: true
  memory:
    scope: project
    reads: [project-context, intake-history, clarify-history, solution-map-history, architect-history, poc-history, impl-history, rfp-history, quote-history]
    writes: [pipeline-state]
  security:
    danger-level: low
---

# /sa-pipeline — 售前端到端流水线编排器

> **一句话客户信息 / RFP → 7 模块流水线 → 完整售前交付包**

## 一句话

**给一句话原始客户信息（如 "某制造业客户，要替换老 MES，私有化 + 国产化，3 月上线"），或一个完整 RFP，本命令按 7 模块顺序调度，每步之间暂停等售前确认，最终产出一份完整的可交付售前包**。

## 用法

### 场景 1：从零开始跑全流程（一句话）

```bash
# 最简
/sa-pipeline "某制造业客户，要替换老 MES，私有化 + 国产化，3 月上线"

# 显式指定关键参数
/sa-pipeline "客户想批量替换 CRM" \
  --client "华夏银行" \
  --industry finance \
  --compliance 等保三级,国产化 \
  --deployment private
```

### 场景 2：从零开始跑全流程（RFP 输入）

```bash
/sa-pipeline ./rfp/2026-政务云-RFP.pdf \
  --stage-5 rfp \
  --industry govtech
```

### 场景 3：断点续跑

```bash
# 已经跑到 M4，从 M5 继续
/sa-pipeline ./output/sa-pipeline/xxx/ --from M5

# 只跑 M5 三专项和 M6
/sa-pipeline ./output/sa-pipeline/xxx/ --from M5 --to M6

# 只跑 RFP 应答（其他都有了）
/sa-pipeline ./output/sa-pipeline/xxx/ --from M5 --stage-5 rfp
```

### 场景 4：变更触发下游重跑

```bash
# 客户合规要求变了，从 M3 重跑到 M6
/sa-pipeline ./output/sa-pipeline/xxx/ --from M3

# 部署模式变了（不改方案主体，只调估算）
/sa-pipeline ./output/sa-pipeline/xxx/ --from M6

# RFP 新版本
/sa-pipeline ./output/sa-pipeline/xxx/ --from M5 --stage-5 rfp
```

### 场景 5：选择性生成 M5

```bash
# 只出 POC 方案（不出实施、不出 RFP）
/sa-pipeline "客户信息" --stage-5 poc

# 只出 RFP 应答
/sa-pipeline ./rfp.pdf --stage-5 rfp

# 全部三个（默认）
/sa-pipeline "客户信息" --stage-5 all
```

## 编排逻辑

### 阶段 0：初始化

若输入是**一句话或 RFP**：
1. 从输入提取 `{client}-{project}` 组合
2. 创建目录 `./output/sa-pipeline/{client}-{project}-{yyyymmdd}/`
3. 初始化 `.pipeline-state.json`

若输入是**已存在目录**：
1. 读取 `.pipeline-state.json` 获取当前进度
2. 校验用户 `--from` 参数与状态一致

### `.pipeline-state.json` 内容

```json
{
  "client": "远大制造",
  "project": "mes-替换",
  "topic_slug": "mfg-mes",
  "created_at": "2026-08-27T15:00:00+08:00",
  "raw_input": "某制造业客户，现有老 MES 要替换，私有化+国产化，3 个月上线",
  "params": {
    "industry": "manufacturing",
    "compliance": ["等保三级", "国产化"],
    "deployment": "private",
    "stage_5_targets": ["poc", "impl", "rfp"]
  },
  "stages": {
    "M1": { "status": "done", "at": "2026-08-27T15:03:00", "output": "00-intake.json" },
    "M2": { "status": "done", "at": "2026-08-27T15:30:00", "output": "01-clarify-report.md" },
    "M3": { "status": "done", "at": "2026-08-27T16:00:00", "output": "02-solution-map.md" },
    "M4": { "status": "in-progress" },
    "M5": { "status": "pending" },
    "M6": { "status": "pending" },
    "M7": { "status": "pending" }
  },
  "gates": {
    "after-M1": { "reviewed": true },
    "after-M2": { "reviewed": true },
    "after-M3": { "reviewed": true }
  }
}
```

### 7 阶段调度

```
M1 → gate → M2 → gate → M3 → gate → M4 → gate → M5(POC+IMPL+RFP) → gate → M6 → gate → M7
     ↑                                                                             │
     └────── 用户驳回 → 回到上一阶段 ←────────────────────────────────────────────┘
```

### STAGE_COMMANDS 映射

| Stage | Command | 输入依赖 |
|---|---|---|
| M1 | `/sa-intake {raw_input} --client {c} --industry {i} --out {dir}/00-intake.json` | raw_input |
| M2 | `/sa-clarify {dir}/00-intake.json --industry {i} --out {dir}/01-clarify-report.md` | M1 |
| M3 | `/sa-solution-map {dir}/01-clarify-report.md --out {dir}/02-solution-map.md` | M2 |
| M4 | `/sa-architect {dir}/02-solution-map.md --deployment {d} --out {dir}/03-*` | M3 |
| M5.1 | `/sa-poc {dir}/03-overall-solution.md --out {dir}/04-poc-plan.md` | M4 |
| M5.2 | `/sa-impl {dir}/03-overall-solution.md --out {dir}/04-impl-plan.md` | M4 |
| M5.3 | `/sa-rfp {rfp_path} {dir}/03-overall-solution.md --out {dir}/04-rfp/` | M4 + RFP |
| M6 | `/sa-quote {dir}/03-overall-solution.md {dir}/04-poc-plan.md --out {dir}/05-*` | M4 + M5.1 |
| M7 | `/sa-archive {dir}/ --bump patch` | 全部 |

## Harness 卡点

### 每阶段之后的 gate 交互

```
【M{n} 完成】《{产物名}》已生成：
  {文件路径}

关键内容速览：
  {关键统计}

请选择：
  (1) 通过 → 继续 M{n+1}
  (2) 驳回 → 重跑 M{n}（提供修改点）
  (3) 编辑后继续 → 我手工改文件，改完按 Enter
  (4) 中止 → 停止流水线，保留当前进度
```

### M5 特殊 gate

M5 可以并行生成三个专项方案：

```
【M4 完成，进入 M5】请选择要生成哪些专项方案：

  [x] M5.1 POC 测试方案（推荐 - 有 POC 意向时）
  [x] M5.2 实施方案（推荐 - 已中标 / 有合同时）
  [x] M5.3 RFP 应答（必须 - 投标场景）

--stage-5 参数可指定：poc / impl / rfp / all（默认 all）
```

### `--skip-gate` 模式

- 用于内部快速原型（**不推荐正式项目**）
- 每阶段完成后打印摘要，不问用户
- 最终一键跑到 M7
- 状态记录 `gates.*.reviewed = false` 便于后期审计

## 输出结构

```
./output/sa-pipeline/{client}-{project}-{yyyymmdd}/
├── .pipeline-state.json         ← 【本命令维护】流水线状态
├── 00-intake.json                ← M1
├── 00-intake-log.md              ← M1
├── 00-raw-materials/             ← M1 原始文件
├── 01-clarify-report.md         ← M2
├── 02-solution-map.md           ← M3
├── 03-overall-solution.md       ← M4
├── 03-architecture.mmd          ← M4
├── 03-business-arch.mmd          ← M4
├── 03-deployment-arch.mmd        ← M4
├── 03-solution-validate.md      ← M4
├── 04-poc-plan.md                ← M5.1（可选）
├── 04-impl-plan.md               ← M5.2（可选）
├── 04-rfp-parsed.json           ← M5.3（可选）
├── 04-rfp-scoring.md             ← M5.3（可选）
├── 04-rfp-response.md           ← M5.3（可选）
├── 04-deviation-table.md         ← M5.3（可选）
├── 05-config-estimate.md         ← M6
├── 05-presentation-outline.md    ← M6
├── 05-presentation-copy.md       ← M6
├── 05-pitch-script.md            ← M6
├── README.md                     ← M7
├── CHANGELOG.md                  ← M7
├── VERSION                       ← M7
└── archive-report.md             ← M7
```

## 常见剧本

### 剧本 A：紧急投标（4-6 小时全流程）

```bash
/sa-pipeline ./rfp/2026-政务云-RFP.pdf \
  --client "某厅" \
  --industry govtech \
  --compliance 等保三级,国产化 \
  --deployment private \
  --stage-5 rfp

# 每阶段 30-60 分钟，售前 gate 决策 10-15 分钟
# 总时长：4-6 小时（含审阅）
# 目标产出：可提交的 04-rfp-response.md + 04-deviation-table.md
```

### 剧本 B：客户 POC 立项

```bash
/sa-pipeline "客户 XX 项目希望做 POC 验证" \
  --client "XX" \
  --stage-5 poc

# 主要输出：04-poc-plan.md + 05-presentation-outline.md
```

### 剧本 C：完整售前包（客户汇报 + 商务报价）

```bash
/sa-pipeline "客户信息" --stage-5 all

# 全部 7 模块 + 3 个专项方案
# 时长：4-6 小时
```

### 剧本 D：客户反馈后返工

```bash
# 客户看了方案后要求换部署为混合云
/sa-pipeline ./output/sa-pipeline/xxx/ --from M4 --deployment hybrid

# 重跑 M4 → M5 → M6 → M7
# CHANGELOG 记录 v1.1.0
```

## 反模式

- ❌ 用 `--skip-gate` 交付客户版 —— gate 是质量保障
- ❌ 手动改 `.pipeline-state.json` —— 状态会不一致
- ❌ 跳过 M2 直接写方案 —— 放弃流水线核心价值
- ❌ RFP 场景没跑 M5.3 就交付 —— 违规
- ❌ 客户合规约束未在 gate 二次确认 —— 生产事故温床

## 与 /sa 命令的关系

- `/sa` 是**总入口路由器**（智能识别命中哪个能力 / 剧本 / 命令）
- `/sa-pipeline` 是**流水线编排器**（专责 7 模块顺序调度）
- 用户说"端到端"、"完整售前包"、"投标"时，`/sa` 会推荐 `/sa-pipeline`
- 也可直接 `/sa-pipeline "需求"` 显式调用
