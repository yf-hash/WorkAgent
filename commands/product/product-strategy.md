---
name: product-strategy
description: >
  产品战略画布生成器，覆盖 BMC 商业模式画布、Lean Canvas 精益画布、
  Value Proposition Canvas 价值主张画布、北极星指标定义、产品愿景声明，
  支持 SaaS / B2B / B2C / 双边平台 / 硬件 / 服务等多种业务形态。
  适用于：产品立项、战略复盘、融资BP、季度方向对齐。
user-invocable: true
argument-hint: "<产品/业务描述> [--mode bmc|lean|vpc|vision|northstar|fullset] [--biz saas|b2b|b2c|platform|hw|service] [--stage 0to1|1to10|10to100] [--output canvas|doc|deck]"
---

# /product-strategy — 产品战略画布

加载技能：`skills/pm/product-strategy/SKILL.md`

## 触发条件
需要做产品战略对齐、定义商业模式、提炼价值主张、设定北极星指标、撰写产品愿景，或为融资/立项准备战略材料时。

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `<产品/业务描述>` | 产品名/业务一句话描述（必填） | — |
| `--mode` | 战略画布类型 | `lean` |
| `--biz` | 业务形态 | `saas` |
| `--stage` | 产品阶段 | `0to1` |
| `--output` | 输出格式 | `canvas` |

### 画布模式（--mode）
| 值 | 输出 | 适用场景 |
|----|------|---------|
| `bmc` | 商业模式画布（9宫格） | 已有产品的整体商业逻辑梳理 |
| `lean` | 精益画布（10宫格 + 假设） | 早期产品、未验证想法（**默认**） |
| `vpc` | 价值主张画布（用户Job + Pain/Gain + 产品适配） | 产品-用户契合度对齐 |
| `vision` | 产品愿景声明（FOR/WHO/THAT/UNLIKE/OUR） | 团队对齐、招聘材料、官网首屏 |
| `northstar` | 北极星指标体系（NSM + Inputs + Counter） | 数据驱动决策、季度规划 |
| `fullset` | 全套战略文档（Vision + Lean + VPC + NSM） | 立项、融资BP、年度规划 |

### 业务形态（--biz）
| 值 | 关键差异点 |
|----|-----------|
| `saas` | ARR/MRR、留存、CAC/LTV、扩展收入 |
| `b2b` | 销售周期、决策链、合同金额、续约率 |
| `b2c` | DAU/MAU、付费转化、ARPU、病毒系数 |
| `platform` | 双边网络效应、Take Rate、流动性 |
| `hw` | 毛利、库存周转、渠道、售后 |
| `service` | 项目利润率、可复用资产、人效 |

### 产品阶段（--stage）
| 值 | 战略重心 |
|----|---------|
| `0to1` | 找 PMF、验证假设、最小有效市场 |
| `1to10` | 增长引擎、漏斗优化、复购/留存 |
| `10to100` | 规模化、平台化、生态、新品类 |

### 输出格式（--output）
| 值 | 说明 |
|----|------|
| `canvas` | ASCII 画布 + 解读（**默认**） |
| `doc` | Markdown 完整文档 |
| `deck` | 演示文稿大纲（投资人/管理层） |

---

## 执行流程

```
Step 1: 战略上下文澄清（≤3 个澄清问题）
  → 产品当前阶段（0→1 / 1→10 / 10→100）
  → 业务形态和商业模式
  → 当前最关键的战略问题

Step 2: 画布生成
  → 按 --mode 加载对应模板
  → 关键格子至少给出 2-3 个候选答案，标记推荐
  → 留白处用 [待补充] 标记，不臆测

Step 3: 假设清单提取（lean 模式核心）
  → 把每个画布格子转化为可验证假设
  → 按风险高低排序（最致命假设排第一）
  → 给每个假设建议验证方法（访谈/原型/MVP/A/B）

Step 4: 北极星指标设计（northstar / fullset 模式）
  → NSM 单一指标（用户价值 + 商业价值 + 可量化）
  → 输入指标（Input Metrics）3-5 个
  → 反向指标（Counter Metrics）防止过度优化

Step 5: 战略风险与对策
  → 用 Pre-Mortem 模型推演失败原因
  → 给出 Top 3 关键风险和应对预案
```

---

## 输出示例（lean 模式）

```
┌──────────────────────── Lean Canvas: [产品名] ────────────────────────┐
│ 1. PROBLEM            │ 4. SOLUTION         │ 3. UNIQUE VALUE PROP  │
│ • 用户最痛的3个问题    │ • 对应 MVP 解法      │ "一句话价值主张"       │
│                       │                     │ HIGH-CONCEPT PITCH    │
│ EXISTING ALTERNATIVES │                     │                       │
│ • 现有替代方案         │                     │                       │
├───────────────────────┼─────────────────────┼───────────────────────┤
│ 8. KEY METRICS        │ 9. UNFAIR ADVANTAGE │ 2. CUSTOMER SEGMENTS  │
│ • 北极星 + 输入指标    │ • 不可复制的优势      │ • 早期adopter         │
│                       │                     │ • 主流客户群           │
├───────────────────────┴─────────────────────┴───────────────────────┤
│ 5. CHANNELS                          │ 6. COST STRUCTURE             │
│ • 触达用户的渠道                       │ • 主要成本项                   │
├──────────────────────────────────────┼───────────────────────────────┤
│ 7. REVENUE STREAMS                                                   │
│ • 收入来源 + 定价模型 + 单位经济                                       │
└──────────────────────────────────────────────────────────────────────┘

🎯 假设风险排序（最致命假设优先验证）：
  1. [假设] → [验证方法] → [验证成本]
  2. ...

📊 北极星指标候选：
  - 候选 A：[指标]（推荐理由）
  - 候选 B：[指标]
```

---

## 与其他命令的协同

```
/product-strategy（本命令）
  ├── /market-research → 验证客户细分、TAM/SAM/SOM
  ├── /user-research   → 验证 Problem 假设
  ├── /pricing-strategy → 收入模型深化
  ├── /pmf-survey      → 验证 UVP 是否对齐
  └── /gtm-strategy    → 战略落地为上市计划

推荐工作流：
  立项阶段：/product-strategy --mode lean --stage 0to1
         → /pmf-survey（PMF 验证）
         → /product-strategy --mode bmc（PMF 后切换商业模式视角）

  季度规划：/product-strategy --mode northstar
         → /roadmap --horizon 3m（路线图落地）
         → /roadmap --horizon 3m
```

---

## 使用示例

```bash
# 早期产品精益画布（默认）
/product-strategy AI 写作助手 SaaS

# 已有产品的商业模式梳理
/product-strategy 企业知识库平台 --mode bmc --biz b2b

# 价值主张校准
/product-strategy 跨境电商选品工具 --mode vpc

# 产品愿景声明（融资 BP / 招聘）
/product-strategy 智能客服平台 --mode vision --output deck

# 北极星指标体系
/product-strategy 工具型 SaaS --mode northstar --biz saas

# 全套战略文档（立项/融资）
/product-strategy 双边设计平台 --mode fullset --biz platform --output doc
```
