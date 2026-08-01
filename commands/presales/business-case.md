---
name: business-case
description: >
  客户价值证明（Business Case / ROI / TCO）生成器 — 给客户经济决策人（EB / CFO）
  看的量化论证。含 ROI / Payback / NPV / IRR 四大财务指标、TCO 三年模型、
  量化收益 5 类（节流 / 故障规避 / 合规 / 营收 / 体验）、保守 / 中性 / 激进三档敏感性、
  一页纸 + 完整版双模板、行业 ROI 锚点。
user-invocable: true
argument-hint: "<客户公司或项目名> [--mode onepage|full|tco|roi|review] [--industry fintech|gov|healthcare|mfg|saas] [--baseline statusquo|diy|competitor] [--out path]"
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

# /business-case — 客户价值证明（ROI / TCO）

加载技能：`skills/presales/business-case/SKILL.md`
配套 Skill：`pricing-strategy`、`solution-architecture`

## 触发条件
- 销售要给客户 EB / CFO 准备决策材料
- 招标 / 大客户场景需要量化论证为什么买我方
- 客户问 "ROI 多少 / 多久回本"

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `<客户公司或项目名>` | — | — |
| `--mode` | 输出模式 | `onepage` |
| `--industry` | 客户行业（决定 ROI 锚点）| — |
| `--baseline` | 对比基线 | `statusquo` |
| `--out` | 输出路径 | `./outputs/business-case/` |

### 输出模式

| `--mode` | 输出 |
|----------|------|
| `onepage` | 一页纸执行摘要（决策建议 + 核心数据 + 财务指标）|
| `full` | 完整版（30+ 页：问题 → 方案 → 收益 → 投入 → 财务指标 → 风险）|
| `tco` | 仅 TCO 三年模型（Year 0-3 + 直接成本 + 隐性成本）|
| `roi` | 仅 ROI 计算器（5 类收益 + 三档敏感性）|
| `review` | 评审已有 Business Case（数字可信度 / 假设合理性 / 风险透明）|

### 对比基线

| `--baseline` | 适用 |
|------------|------|
| `statusquo` | 客户继续维持现状（最易论证 / 最常用）|
| `diy` | 客户考虑过自建 |
| `competitor` | 客户在选我方 vs 对手 |

## 使用示例

```
/business-case 某城商行 SOC 项目 --mode onepage --industry fintech --baseline statusquo
/business-case 某政务云项目 --mode full --industry gov --baseline diy
/business-case 已有 BC 文档 --mode review --industry mfg
/business-case 某制造业项目 --mode tco --industry mfg
```

## 执行流程

```
Step 1: 信息采集
  → 客户业务规模 / 当前痛点量化数据 / 业务影响
  → 客户折现率（一般 8-12%）/ 决策周期

Step 2: Cost of Inaction 测算
  → 客户继续不做的代价（量化）
  → 故障损失 / 合规罚款 / 机会成本

Step 3: 收益建模（5 类）
  → 节流（人力 / 工具 / 故障 / 合规）
  → 故障损失规避
  → 合规罚款规避
  → 营收增长（转化 / 客单 / 留存）
  → 客户体验（NPS / 投诉 / 留存）
  → 每类给出公式 + 数据来源 + 同行案例锚点

Step 4: TCO 三年建模
  → 直接成本（License / 实施 / 培训 / 维护 / SLA / 硬件）
  → 隐性成本（内部人力 / 变更 / 集成 / 迁移）

Step 5: 财务指标计算
  → ROI / Payback / NPV / IRR
  → 与行业基准对比（按 industry 提供锚点）

Step 6: 三档敏感性
  → 保守 / 中性 / 激进
  → 每档对应不同 Payback / ROI

Step 7: 关键假设 + 风险
  → 假设清单（如客户配合 X 实施）
  → 风险矩阵（识别 / 概率 / 影响 / 应对）

Step 8: 决策建议
  → 一页纸 Executive Summary
  → 决策时间表建议
```

## 与其他命令的边界

| 选择 | 用前者 | 用后者 |
|------|-------|-------|
| `/business-case` vs `/proposal` | 全数字财务论证 | 综合方案叙述 |
| `/business-case` vs `/pricing-strategy` | 给客户算 ROI | 自家产品定价策略 |
| `/business-case` vs `/solution-architecture` | 商务可行性 | 技术可行性 |
| `/business-case` vs `/build-vs-buy` | 客户买我方 vs 不买 | 客户自研 vs 买（任意供应商）|
