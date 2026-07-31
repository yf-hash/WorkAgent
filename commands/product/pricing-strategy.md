---
name: pricing-strategy
description: >
  产品定价策略助手。覆盖五大定价方法（成本加成/竞争对标/价值定价/心理定价/动态定价）、
  SaaS 套餐结构（Freemium/Free Trial/阶梯/用量计费）、Van Westendorp PSM
  价格敏感度测量、Conjoint 联合分析、定价 A/B 测试、涨价/降价 SOP、
  单位经济（LTV/CAC）健康检查、企业级合同定价。
  适用于：新产品定价、套餐重设计、涨价/降价决策、付费转化优化。
user-invocable: true
argument-hint: "<产品/服务描述> [--mode tier|psm|conjoint|increase|decrease|fullset] [--biz saas|hw|service|consumer|api] [--stage launch|growth|mature]"
---

# /pricing-strategy — 产品定价策略

加载技能：`skills/strategy/pricing-strategy/SKILL.md`

## 触发条件
新产品定价、设计套餐结构、做用户价格敏感度调研、涨价/降价决策、付费转化优化，或单位经济（LTV/CAC）健康检查时。

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `<产品/服务描述>` | 产品名 / 业务描述（必填） | — |
| `--mode` | 工作模式 | `tier` |
| `--biz` | 业务形态 | `saas` |
| `--stage` | 产品阶段 | `launch` |

### 工作模式（--mode）
| 值 | 输出 | 适用场景 |
|----|------|---------|
| `tier` | 套餐结构设计（Free / Pro / Business / Enterprise）（**默认**） | 新产品定价 / 套餐重设计 |
| `psm` | Van Westendorp 价格敏感度问卷 + 解读 | 用户价格调研 |
| `conjoint` | Conjoint 联合分析问卷设计 | 多属性定价权重分析 |
| `increase` | 涨价 SOP + 老用户保留策略 | 涨价决策 |
| `decrease` | 降价 / 折扣机制设计 | 促活 / 召回 |
| `fullset` | 套餐 + PSM + 单位经济 + A/B 全套 | 重大定价改版 |

### 业务形态（--biz）
| 值 | 关键差异 |
|----|---------|
| `saas` | MRR / ARR / 用户数 / 套餐分层 |
| `hw` | 一次性 + 服务费 / 渠道分成 |
| `service` | 项目制 / 包月 / Retainer |
| `consumer` | 单价低 / 频次高 / 订阅 |
| `api` | 用量计费为主（按 token/请求） |

### 产品阶段（--stage）
| 值 | 重点 |
|----|------|
| `launch` | 早期定价探索（**默认**） |
| `growth` | 优化转化和 ARPU |
| `mature` | 涨价 / 套餐重设 / 企业级 |

---

## 执行流程（tier 模式）

```
Step 1: 价值与成本盘点
  → 用户感知核心价值是什么？（Value-based 锚点）
  → 单位用户成本（变动 + 固定）
  → 竞品定价区间（Competition-based 参照）

Step 2: 套餐结构选型
  → Freemium vs Free Trial 决策
  → 三档 / 四档 套餐数量
  → 用量阶梯（如有）

Step 3: 价格点设定
  → 中档锚定（最希望卖的）
  → 价格差距 2-3x（避免 1.2x 区分度低）
  → 心理定价技巧（9 字尾 / 整数 / 月年付差额）

Step 4: 套餐功能矩阵
  → 每档解锁的功能 / 用量限制
  → 免费档保留长期可用核心
  → 升级触发点（用量/功能/团队规模）

Step 5: 单位经济健康检查
  → LTV 估算（ARPU × 生命周期 × 毛利）
  → CAC 上限（LTV/3）
  → Payback Period（< 12 / 18 个月）

Step 6: A/B 测试 / 调研建议
  → PSM 对当前定价区间敏感度
  → A/B 测试套餐顺序 / 文案
```

---

## 输出示例（tier 模式）

```markdown
# [产品名] 套餐定价方案

## 套餐总览
| 档 | 名称 | 价格 | 目标用户 | 成交策略 |
|----|------|------|---------|---------|
| L1 | Free | $0 | 个人尝鲜 | 长期可用，限制用量 |
| L2 | Pro | $19/月 | 个人专业 | 解锁高级功能 |
| L3 | Team ⭐ | $49/月起 | 5-50 人团队 | **主推**，最盈利 |
| L4 | Enterprise | 联系销售 | 50+ 企业 | 定制 + SLA |

## 套餐功能矩阵
| 功能 | Free | Pro | Team | Enterprise |
|------|------|-----|------|------------|
| 项目数 | 3 | 无限 | 无限 | 无限 |
| 用户数 | 1 | 1 | 5（每加 $9） | 无限 |
| AI 调用 | 100/月 | 1000/月 | 5000/月 | 自定义 |
| 集成 | 基础 5 个 | 全部 | 全部 + API | 全部 + 自定义 |
| 支持 | 社区 | Email | Email + 培训 | 专属 + SLA |
| 数据保留 | 30 天 | 1 年 | 永久 | 永久 + 备份 |

## 价格设计逻辑
- Free → Pro：$19 是"咖啡价"，门槛低
- Pro → Team：2.6x 跳跃，解锁协作
- Team → Enterprise：商谈空间，案例授权可享 -20%

## 单位经济估算
- 平均 ARPU：$32（混合）
- 估算 LTV：$32 × 18 月 × 70% 毛利 = $403
- CAC 上限：< $134（LTV/3）
- 当前 CAC：$60 → 健康

## 调研 / A/B 计划
1. PSM 调研 N=200，验证 $19 / $49 是否在可接受区间
2. A/B 测试 Team 价格 $49 vs $59
3. A/B 测试套餐顺序（Team 默认选中 vs Pro 默认）

## 风险
- $19 太低：可能被认为不专业
- Team 升级路径不清：需 5+ 用户触发点提示
- Enterprise 商谈空间：需销售脚本支撑

## 后续
→ /ab-test --mode design 设计定价 A/B
→ /pricing-strategy --mode psm 调研敏感度
→ /gtm-strategy 落地价格沟通策略
```

---

## 输出示例（psm 模式）

```markdown
# Van Westendorp PSM 调研问卷

**目标用户**：[Persona]
**样本量目标**：N ≥ 200
**触达渠道**：[渠道]

## 问卷题目（4 题）

1. At what price would [产品/服务] be **so expensive** that you would never consider buying it?
   _____ 元 / 月

2. At what price would [产品/服务] be **expensive** but you'd still consider buying it?
   _____ 元 / 月

3. At what price would [产品/服务] be a **bargain** — a great buy for the money?
   _____ 元 / 月

4. At what price would [产品/服务] be **so cheap** that you would question its quality?
   _____ 元 / 月

## 数据分析

| 交点 | 含义 | 建议 |
|------|------|------|
| OPP | 最优定价点 | 推荐定价 |
| IDP | 最佳价值点 | 锚定价格 |
| PMC | 最低可接受 | 套餐起步价 |
| PME | 最高可接受 | 套餐顶价 |

可接受区间：[PMC, PME]

## 解读注意
- 样本必须代表目标用户（不能拉群里随便问）
- 区分新用户 / 老用户（可能价格预期不同）
- 区分付费用户 / 免费用户
- 国家 / 地区差异（购买力平价）
```

---

## 与其他命令的协同

```
/pricing-strategy（本命令）
  ├── /product-strategy → Revenue Streams 深化
  ├── /gtm-strategy → 定价是 GTM 核心
  ├── /market-research → 竞品价格情报
  ├── /user-research → PSM / Conjoint 调研
  ├── /ab-test → 定价 A/B 设计
  ├── /analytics → LTV / CAC 数据
  └── /pmf-survey → PMF 后定价更稳

推荐工作流：
  新产品上市：
    /product-strategy --mode lean
    → /market-research --mode competitive
    → /pricing-strategy --mode tier
    → /pricing-strategy --mode psm（调研）
    → 上市
    → /ab-test（持续优化）
```

---

## 使用示例

```bash
# SaaS 套餐设计（默认）
/pricing-strategy AI 写作助手 SaaS

# Van Westendorp 价格敏感度
/pricing-strategy AI 写作助手 --mode psm

# Conjoint 联合分析
/pricing-strategy 数据分析平台 --mode conjoint

# 涨价决策（成熟产品）
/pricing-strategy 团队协作工具 --mode increase --stage mature

# 降价 / 召回机制
/pricing-strategy 流失用户召回 --mode decrease

# API 用量计费
/pricing-strategy 大模型 API 服务 --biz api --mode tier

# 重大定价改版完整方案
/pricing-strategy 企业版重设计 --mode fullset --biz saas --stage growth
```
