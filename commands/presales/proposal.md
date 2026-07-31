---
name: proposal
description: >
  售前方案文档 — 企业项目型方案撰写。覆盖售前解决方案、可行性研究报告、
  初步设计方案三大类型，行业适配（政府 / 金融 / 制造 / SaaS），
  与 /sales-guide / /product-* 系列 / /bid 七阶段标书互补。
  
  与相邻命令的边界（防混淆）：
  - vs /sales-guide：本命令产出"客户响应方案"（项目型，一次性）；
    /sales-guide 产出"销售一页禅"（场景剧本，给销售用）。
  - vs /product-* 系列：本命令是"项目型一次性方案"；
    /product-whitepaper / /product-solution 等是"产品级可复用资料"。
  - vs /bid 七阶段：本命令更通用；
    /bid --phase all 流水线专门做招投标全流程。
  适用于：客户响应型方案、项目立项报告、技术方案确认。
user-invocable: true
argument-hint: "<项目描述> [--type presale|feasibility|design] [--industry gov|finance|mfg|saas|general] [--section all|outline|chapter] [--output md|outline|brief]"
---

# /proposal — 企业方案文档生成

加载技能：`skills/proposal-generator/SKILL.md`

## 触发条件
需要撰写售前解决方案、可行性研究报告、初步设计方案，或生成方案目录、章节内容、报价单时。

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `<项目描述>` | 项目名称或一句话描述（必填） | — |
| `--type` | 方案类型 | `presale` |
| `--industry` | 目标行业 | `general` |
| `--section` | 生成范围 | `all` |
| `--output` | 输出格式 | `md` |

### 方案类型（--type）
| 值 | 类型 | 适用场景 |
|----|------|---------|
| `presale` | 售前解决方案 | 商机响应、投标、客户演示 |
| `feasibility` | 可行性研究报告 | 项目立项、决策支撑 |
| `design` | 初步设计方案 | 项目启动前技术方案确认 |

### 行业（--industry）
| 值 | 行业 | 特殊要求 |
|----|------|---------|
| `gov` | 政府/公共事业 | 政策引用、国产化、等保合规 |
| `finance` | 金融 | 监管合规、灾备、数据安全 |
| `mfg` | 制造业 | ERP/MES集成、生产连续性 |
| `saas` | SaaS/互联网 | 云原生、敏捷交付、DevOps |
| `general` | 通用 | 标准模板，不含行业特化内容 |

### 生成范围（--section）
| 值 | 说明 |
|----|------|
| `all` | 完整方案（目录 + 全部章节内容） |
| `outline` | 仅生成目录结构 |
| `chapter` | 指定章节（配合章节名使用） |

### 输出格式（--output）
| 值 | 说明 |
|----|------|
| `md` | Markdown 完整文档 |
| `outline` | 纯目录大纲（适合快速对齐） |
| `brief` | 执行摘要（1-2页，适合高管汇报） |

---

## 执行流程

```
Step 1: 项目信息收集
  → 项目名称与背景（必填）
  → 甲方/客户类型（政府/企业/事业单位）
  → 项目规模与预算范围（可选）
  → 核心痛点与建设目标（可选，有则更精准）

Step 2: 方案类型判断
  → 根据 --type 参数选择对应模板
  → 根据 --industry 加载行业定制化内容
  → 确认生成范围（全文/目录/指定章节）

Step 3: 结构生成
  → 输出标准目录结构
  → 按章节顺序填充内容
  → 关键章节插入图表说明（架构图/甘特图/报价表）

Step 4: 质量核验
  → 检查：需求有来源、技术有对比、数据有出处
  → 检查：风险有应对、效益有量化、进度有甘特
  → 检查：图表编号规范、术语统一

Step 5: 输出格式化
  → 按 --output 参数格式化输出
  → 标注需要人工补充的占位内容（[待填写]标记）
```

---

## 与其他命令的协同关系

```
/proposal → 方案文档生成
  ├── /market-research  → 竞品分析、行业背景数据支撑
  ├── /gtm-strategy     → 售前方案的 GTM 章节
  ├── /roadmap          → 实施计划甘特图生成
  └── @proposal-writer  → 全链路方案 Agent（含多轮问答+完整生成）

@product-enablement → B2B 产品资料体系（与本命令互补）
  本命令：项目型方案（一次性交付）
  product-enablement：产品型资料（可复用的标准化文档）
```

---

## 使用示例

```bash
# 快速生成售前解决方案目录
/proposal 智慧园区管理平台 --type presale --section outline

# 政府项目可行性研究报告
/proposal 县域政务数据共享平台 --type feasibility --industry gov

# 金融行业初步设计方案
/proposal 银行风控系统升级 --type design --industry finance --output md

# 制造业售前方案（完整版）
/proposal 汽车零部件MES系统 --type presale --industry mfg --output md

# 快速生成执行摘要（高管汇报用）
/proposal 企业知识管理平台 --type presale --output brief

# 只生成报价单章节
/proposal 政务云平台建设 --type presale --section chapter --chapter 报价单
```
