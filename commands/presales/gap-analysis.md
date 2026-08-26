---
name: gap-analysis
description: >
  功能差异分析 / Gap Analysis 工具 — 客户需求清单 vs 我方产品能力的逐项映射。
  含 4 级匹配标签（满足 / 部分 / 替代 / 不满足）、需求拆解（功能 / 非功能 / 集成 / 服务）、
  优先级（Must / Should / Could）、Gap 评分（影响 × 紧迫 / 工作量）、应对策略矩阵、
  继续投 vs 弃单决策树、Gap Closure Plan、客户验收口径同步。
user-invocable: true
argument-hint: "<客户需求清单文件或描述> [--mode analyze|score|plan|review] [--industry fintech|gov|healthcare|saas] [--out path]"
allowed-tools: [Read, Write, Edit, Grep, Glob, AskUserQuestion]
harness:
  execute:
    preset: writing-scoped
  constrain:
    profile: writing-safe
    gates: [before-write]
  loop:
    mode: one-shot
  memory:
    scope: project
    reads: [project-context]
  security:
    danger-level: medium
---

# /gap-analysis — 功能差异分析

加载技能：`skills/presales/gap-analysis/SKILL.md`
配套 Skill：`solution-architecture`、`rfp-response`

## 触发条件
- 收到客户需求清单（50-500 条）
- 多个候选客户中需要快速判断"这个单值不值得投"
- Gap 较多时需要做 Closure Plan

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `<需求清单文件或描述>` | 客户需求清单（Excel / Word / 描述）| — |
| `--mode` | 工作模式 | `analyze` |
| `--industry` | 客户行业 | — |
| `--out` | 输出路径 | `./outputs/gap/` |

### 工作模式

| `--mode` | 输出 |
|----------|------|
| `analyze` | 完整 Gap Analysis（拆解 → 标签 → 评分 → 决策建议）|
| `score` | 仅评分（影响 × 紧迫 / 工作量 → 优先级排序）|
| `plan` | Gap Closure Plan（针对高优先级 Gap 的应对方案）|
| `review` | 评审已有 Gap Analysis 文档 |

## 使用示例

```
/gap-analysis ./CustomerRequirements.xlsx --mode analyze --industry fintech
/gap-analysis ./Bank_Reqs.docx --mode score
/gap-analysis 项目 X 的高优 Gap --mode plan
/gap-analysis ./Existing_Gap_Doc.xlsx --mode review
```

## 执行流程

```
Step 1: 需求拆解
  → 一条客户需求 → 多条 SE 视角原子需求
  → 三维度分类（类型 / 优先级 / 复杂度）

Step 2: 4 级匹配标签
  → ✅ 满足 / ⚠️ 部分 / 🔄 替代 / ❌ 不满足
  → 每条配应答描述 + 证据来源

Step 3: Gap 评分
  → 影响度（1-5）× 紧迫度（1-5）/ 工作量（1-5）
  → 高优先级（>=5.0）/ 中（2.0-5.0）/ 低（<2.0）

Step 4: 应对策略
  → 工作量小 + 紧迫高 → 立即定制
  → 工作量小 + 紧迫低 → 纳入 roadmap
  → 工作量中 + 紧迫高 → 资源评估后承诺
  → 工作量中 + 紧迫低 → 替代方案
  → 工作量大 + 紧迫高 → 生态合作 / 战略级取舍
  → 工作量大 + 紧迫低 → 诚实说明 + 时间表

Step 5: 决策树（投 vs 弃）
  → 必备需求中 ❌ ≥3 个 → 大概率丢单
  → 重要需求中 ❌+⚠️ >50% → 产品定位不匹配
  → 高优先级 Gap ≥5 + 决策时间表 <60 天 → 弃单 / 转推

Step 6: Gap Closure Plan
  → 每个高优 Gap：策略（定制 / roadmap / 生态 / 绕过）+ 责任人 + 时间表 + 商务条件

Step 7: 客户验收口径
  → ⚠️ 项：客户认可边界（书面）
  → 🔄 项：客户认可替代方案（合同附件）
  → 定制项：工期 + 报价 + 验收（不允许口头承诺）
  → ❌ 项：客户认可不做不影响整体验收

Step 8: 输出物
  → Excel 标准模板（Req ID / 客户原文 / 类别 / 优先级 / 匹配 / 描述 / 评分 / 策略 / 状态）
  → 《客户名 × 我方 需求 Gap Analysis 与确认书》
```

## 与其他命令的边界

| 选择 | 用前者 | 用后者 |
|------|-------|-------|
| `/gap-analysis` vs `/rfp-response` | 主动梳理需求 vs 能力 | 被动逐条作答 |
| `/gap-analysis` vs `/solution-architecture` | 需求适配度评估 | 完整方案蓝图 |
| `/gap-analysis` vs `/compliance-checklist` | 客户全维度需求 | 仅合规维度 |
