---
name: user-research
description: >
  用户研究工作台 — 访谈 / 问卷 / 卡片分类 / 旅程 / 画像 / Founder 六种方法。
  
  与相邻命令的边界（防混淆）：
  - vs /market-research：本命令做"用户视角"（行为 + 动机 + JTBD）；
    /market-research 做"市场视角"（竞品 + 趋势 + TAM）。两者互补。
  - vs /feedback：本命令是"主动研究"（设计研究问题去问）；
    /feedback 是"被动分析"（已有反馈数据做聚类）。
user-invocable: true
argument-hint: "<研究目标> [--mode interview|survey|card-sort|journey|persona|founder] [--participants <N>]"
allowed-tools: [Read, Write, Edit, Grep, Glob, AskUserQuestion]
harness:
  execute:
    preset: research
  constrain:
    profile: writing-safe
    gates: [before-write]
  loop:
    mode: one-shot
  memory:
    scope: project
    reads: [project-context]
  security:
    danger-level: low
---

# /user-research — 用户研究工作台

加载技能：`skills/research/user-research/SKILL.md`

## 触发条件
设计用户访谈脚本、问卷、卡片分类、用户旅程地图、用户画像，或寻找早期 Adopter / 创始人级用户时。

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `<研究目标>` | 研究目的或待验证假设（必填） | — |
| `--mode` | 研究方法 | `interview` |
| `--participants` | 目标参与人数 | `5` |

### 研究模式
| `--mode` | 输出内容 | 适用场景 |
|----------|---------|---------|
| `interview` | 访谈脚本 + 问题卡片 + 分析框架 | 定性探索、需求挖掘 |
| `survey` | 问卷结构 + 问题设计 + 分析逻辑 | 量化验证、规模调研 |
| `card-sort` | 卡片分类任务设计 + 结果分析框架 | 信息架构、导航设计 |
| `journey` | 用户旅程地图（当前态 + 理想态） | 体验优化、痛点挖掘 |
| `persona` | 用户画像（基于数据/访谈）| 对齐团队认知 |
| `founder` | 创始人/早期用户发现脚本 | 0→1 产品验证 |

## 参考工具生态

| 工具 | 用途 | GitHub |
|------|------|--------|
| openinterviewer | AI 驱动用户访谈平台 | linxule/openinterviewer |
| founder-discovery | 创始人目标用户发现 | ORBWEVA/founder-discovery |
| designflow-kit | 设计研究工作流套件 | eaglescrooge/designflow-kit |
| card_sorter | 卡片分类工具 | eddequincey/card_sorter |
| skill_seekers | 技能/能力发现工具 | yusufkaraaslan/skill_seekers |

## 执行流程（interview 模式）

```
Step 1: 研究设计
  → 明确研究问题（What do we NOT know?）
  → 定义参与者筛选标准（Screener）
  → 确定访谈时长和形式

Step 2: 脚本生成
  → 开场白 + 破冰问题（2-3分钟）
  → 背景了解（5分钟）
  → 核心探索问题（20-30分钟）
  → 深挖追问提示
  → 结束语

Step 3: 分析框架
  → 亲和图分类维度
  → Jobs-to-be-Done 提取模板
  → 洞察优先级矩阵

Step 4: 报告模板
  → 关键发现摘要
  → 引用金句
  → 行动建议
```

## 输出示例（interview 模式）

```markdown
# 用户访谈脚本：[研究目标]

## 筛选标准（Screener）
- 条件 1
- 条件 2

## 开场白
"您好，感谢参与今天的访谈..."

## 背景问题
1. 能简单介绍一下您日常的工作流程吗？
2. [追问]...

## 核心问题
1. 当您遇到 [场景] 时，您通常怎么做？
2. 上一次您 [行为] 是什么时候？能描述一下那次经历吗？
3. [追问提示：为什么？然后呢？还有什么？]

## 分析框架
| 用户 | 痛点 | 现有解法 | 期望 | JTBD |
|------|------|---------|------|------|
```

## 使用示例

```
/user-research 验证用户是否愿意为 AI 写作工具付费
/user-research 了解产品经理的日常工具链 --mode interview
/user-research 导航信息架构优化 --mode card-sort
/user-research 新用户注册流程体验 --mode journey
/user-research 基于 50 条访谈记录生成用户画像 --mode persona
/user-research 寻找 SaaS 工具早期用户 --mode founder --participants 20
```
