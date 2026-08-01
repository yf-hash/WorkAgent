---
name: solution-architecture
description: >
  解决方案架构设计 — 售前 SA 从客户需求到完整方案蓝图。SA Blueprint 12 章
  （执行摘要 / 业务背景 / As-Is / To-Be / 部署模式 / 集成 / 容量 / 高可用 /
  安全合规 / 路线图 / 商业模型 / 风险）+ 客户化定制 + NFR 清单 + 三档报价。
user-invocable: true
argument-hint: "<客户公司或项目名> [--mode blueprint|as-is|to-be|nfr|roadmap|review] [--industry fintech|gov|healthcare|mfg|saas] [--deployment saas|private|hybrid] [--out path]"
allowed-tools: [Read, Write, Edit, Grep, Glob, AskUserQuestion]
harness:
  execute:
    preset: writing-scoped
  constrain:
    profile: writing-safe
    gates: [before-write]
  loop:
    mode: pipeline
    stages: [discovery, gap, sa-blueprint, business-case, rfp, demo, poc]
    gate-between: true
  memory:
    scope: project
    reads: [project-context]
  security:
    danger-level: medium
---

# /solution-architecture — 解决方案架构设计

加载技能：`skills/presales/solution-architecture/SKILL.md`
配套 Skill：`arch-diagram`（生成架构图）、`gap-analysis`（差距分析）、`business-case`（财务模型）

## 触发条件
- 客户已完成需求挖掘，进入方案设计阶段
- 需要给客户一份端到端的解决方案蓝图（架构 + 集成 + 路线图 + 报价）

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `<客户公司或项目名>` | — | — |
| `--mode` | 方案模式 | `blueprint` |
| `--industry` | 客户行业 | — |
| `--deployment` | 部署模式 | — |
| `--out` | 输出路径 | `./outputs/solution/` |

### 方案模式

| `--mode` | 输出 |
|----------|------|
| `blueprint` | 完整 SA Blueprint 12 章（30-50 页）|
| `as-is` | 仅现状分析（含问 10 题清单）|
| `to-be` | 仅目标架构（含架构图）|
| `nfr` | 非功能需求清单（性能 / 可用性 / 安全 / 合规 / 可观测）|
| `roadmap` | 仅实施路线图（90 天三阶段 + 里程碑）|
| `review` | 评审已有方案（客户视角 / 完整性 / 可信度 / 商业可行 / 风险透明）|

## 使用示例

```
/solution-architecture 某城商行 SOC 项目 --mode blueprint --industry fintech --deployment private
/solution-architecture 某政务云项目 --mode as-is --industry gov
/solution-architecture 某 SaaS 客户 --mode to-be --industry saas --deployment saas
/solution-architecture 某医院 --mode nfr --industry healthcare
/solution-architecture 已有方案 --mode review
```

## 执行流程

```
Step 1: 信息盘点
  → 加载 discovery-call 输出（如有）
  → 客户业务 + 已有 IT 资产 + 已知约束

Step 2: As-Is 现状评估
  → 必问 10 题（系统 / 集成 / 数据 / 用户 / 安全 / 运维 / 痛点 / 限制 / 决策）
  → 现有架构图（客户提供 或 反推 + 标⚠️ 待验证）

Step 3: To-Be 目标架构
  → 三层透视（业务 / 应用 / 基础设施）
  → 客户化关键决策点（部署 / 数据 / 认证 / 高可用 / 国产化 / 扩展性）
  → 调用 arch-diagram 生成主架构图

Step 4: 集成 + 容量 + NFR
  → SSO / SCIM / API / 数据同步具体方案
  → Year 1 / 3 容量预测
  → NFR 7 大类清单（性能 / 可用性 / 扩展 / 安全 / 合规 / 可观测 / 可维护）

Step 5: 实施路线图
  → 90 天三阶段（试点 → 核心上线 → 全量）
  → 每 Phase 里程碑 + 验收 + 责任分工
  → 风险节点识别

Step 6: 商业模型与报价
  → 三档定价（标准 / 推荐 / 企业）
  → 报价 7 项（License / 实施 / 培训 / 维护 / SLA / 定制 / 第三方）
  → 折扣谈判预案

Step 7: 客户化定制
  → 按 industry 调整重点（金融 / 政府 / 医疗 / 制造 / SaaS）
  → 引用同行业客户案例

Step 8: 评审清单
  → 客户视角 / 完整性 / 可信度 / 商业可行 / 风险透明 五维度
```

## 与其他命令的边界

| 选择 | 用前者 | 用后者 |
|------|-------|-------|
| `/solution-architecture` vs `/proposal` | 技术架构方案（SA 主笔）| 商业方案三大类 |
| `/solution-architecture` vs `/arch-diagram` | 完整方案文档 | 单纯生成架构图 |
| `/solution-architecture` vs `/prd --mode enterprise` | 售前面向客户 | PM 内部产品规格 |
| `/solution-architecture` vs `/discovery-call` | 第 3+ 次会议（架构落地）| 第 1-2 次（需求挖掘）|
| `/solution-architecture` vs `/gap-analysis` | 完整方案蓝图 | 客户需求 vs 产品能力对照表 |
