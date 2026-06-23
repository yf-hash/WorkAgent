---
name: gtm-strategy
description: >
  Go-to-Market 上市战略规划，覆盖增长模型选择、ICP定义、定位设计、渠道策略、定价方案、90天上市计划及 GTM KPI 体系，支持 SaaS/B2B/B2C/中国市场等多种场景
user-invocable: true
argument-hint: "<产品/业务描述> [--mode diagnose|strategy|launch|optimize|fullplan] [--growth mlg|slg|plg|ecg|auto] [--market cn|global|b2b|b2c] [--output brief|doc|deck]"
---

# /gtm-strategy — Go-to-Market 上市战略规划

加载技能：`skills/gtm-strategy/SKILL.md`

## 触发条件
需要制定产品上市战略、评估增长模型、设计渠道与定价方案、建立 GTM KPI 体系，或进行上市复盘与迭代时。

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `<产品/业务描述>` | 产品名称、类型或一句话描述（必填） | — |
| `--mode` | 执行模式 | `strategy` |
| `--growth` | 增长模型倾向 | `auto` |
| `--market` | 目标市场 | `cn` |
| `--output` | 输出格式 | `doc` |

### 执行模式（--mode）
| 模式 | 输出内容 | 适用场景 |
|------|---------|---------|
| `diagnose` | GTM 现状诊断：找问题、找瓶颈、给建议 | 已上市但增长不达预期 |
| `strategy` | 完整 GTM 策略文档：增长模型 + ICP + 定位 + 渠道 + 定价 | 新产品上市策略制定 |
| `launch` | 90天上市执行计划：里程碑 + 关键任务 + 负责人 + KPI | 即将启动的上市执行 |
| `optimize` | GTM 优化建议：漏斗分析 + 渠道 ROI + 留存改善 | 上市后持续优化 |
| `fullplan` | 完整 GTM 全链路：strategy + launch + 指标体系合并输出 | 高优先级新产品，需完整方案 |

### 增长模型（--growth）
| 模型 | 说明 |
|------|------|
| `mlg` | 营销驱动增长（内容/SEO/广告/PR）|
| `slg` | 销售驱动增长（SDR/AE/大客户攻坚）|
| `plg` | 产品驱动增长（Freemium/自助/口碑扩散）|
| `ecg` | 生态驱动增长（API/合作伙伴/Marketplace）|
| `auto` | 自动根据产品特征推荐最适合的模型 |

### 目标市场（--market）
| 值 | 说明 |
|----|------|
| `cn` | 中国市场（微信生态/企业微信/钉钉/抖音渠道优先）|
| `global` | 全球/海外市场（SEO/LinkedIn/G2/Product Hunt）|
| `b2b` | 企业客户（销售使能/渠道合作/招投标）|
| `b2c` | 消费者市场（社群/KOL/私域/裂变增长）|

### 输出格式（--output）
| 值 | 说明 |
|----|------|
| `brief` | 一页纸摘要（核心决策、关键数字、立即行动项） |
| `doc` | 结构化 Markdown 文档（完整策略，适合团队共享）|
| `deck` | 演示文稿大纲（适合汇报/投资人/管理层）|

---

## 执行流程

```
Step 1: 信息收集与诊断
  → 产品类型（SaaS/硬件/服务/平台）和当前阶段（PMF前/PMF后/扩张期）
  → 目标客户初步判断（ICP 画像）
  → 现有增长模式和主要渠道
  → 上市目标和时间窗口

Step 2: 增长模型选择
  → 评估 MLG / SLG / PLG / ECG 适配性
  → 推荐主模型 + 辅助模型组合
  → 说明选择理由和注意事项

Step 3: ICP + Persona 定义
  → 理想客户画像（ICP）：行业/规模/痛点/预算/决策链
  → 关键用户 Persona（角色/目标/阻力/信息渠道）
  → 客户旅程地图（感知→考虑→决策→使用→推荐）

Step 4: 定位与价值主张
  → 竞争格局分析（直接/间接/潜在替代）
  → 差异化定位声明
  → 价值主张公式（量化收益）
  → 面向不同角色的核心信息

Step 5: 渠道与定价设计
  → 销售模型选择（自助/线上/现场/渠道）
  → 营销渠道组合（付费/自有/赢得媒体）
  → 定价策略（模型 + 定价点 + 套餐设计）

Step 6: 上市计划与 KPI
  → 90天里程碑时间线（预启动→启动→优化）
  → GTM KPI 体系（获客/转化/留存分层指标）
  → 关键风险与应对预案
```

---

## 与其他命令的协同关系

```
/gtm-strategy → 战略层（做什么、怎么做）
  ├── /market-research        → 竞品研究、市场规模验证
  ├── /prd-standard           → 产品需求文档的 GTM 章节
  ├── /roadmap                → 上市里程碑路线图
  └── @gtm-strategist         → 全链路 GTM Agent 编排（含多技能协作）
```

---

## 使用示例

```bash
# 新 SaaS 产品的完整上市策略
/gtm-strategy AI 会议纪要 SaaS --mode strategy --growth auto --market cn

# 已上市产品诊断增长瓶颈
/gtm-strategy 我们的 B2B ERP 产品 --mode diagnose --market b2b

# 生成 90天上市执行计划
/gtm-strategy 跨境电商选品工具 --mode launch --growth plg --market global

# 产品上线后优化渠道 ROI
/gtm-strategy 企业知识库产品 --mode optimize --market cn --output brief

# 生成完整 GTM 方案（适合融资/高管汇报）
/gtm-strategy 智能客服平台 --mode fullplan --growth slg --market b2b --output deck
```
