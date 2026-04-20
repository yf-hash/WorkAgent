---
name: analytics
description: 产品数据分析，支持指标体系设计、漏斗分析、埋点方案、增长分析、PostHog/Matomo/Countly 集成
user-invocable: true
argument-hint: "<分析目标> [--mode metrics|funnel|cohort|growth|event|dashboard] [--platform posthog|matomo|countly|jitsu]"
---

# /analytics — 产品分析工作台

加载技能：`skills/product-analytics/SKILL.md`

## 触发条件
需要设计产品指标体系、分析用户漏斗、设计埋点方案、搭建增长看板，或将数据转化为产品决策时。

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `<分析目标>` | 分析问题或产品模块（必填） | — |
| `--mode` | 分析类型 | `metrics` |
| `--platform` | 目标平台 | `posthog` |

### 分析模式
| `--mode` | 输出内容 | 适用场景 |
|----------|---------|---------|
| `metrics` | 指标体系设计（北极星+OKR+护栏指标） | 产品定义、季度规划 |
| `funnel` | 漏斗分析（转化路径 + 流失节点 + 优化建议） | 注册/付费/激活优化 |
| `cohort` | 留存分析（Cohort 矩阵 + 留存曲线解读） | 用户质量评估 |
| `growth` | 增长诊断（AARRR框架 + 增长杠杆识别） | 增长策略制定 |
| `event` | 埋点方案（事件命名规范 + 属性设计 + 代码示例） | 前端工程师对接 |
| `dashboard` | 看板设计（图表选型 + 布局 + 刷新频率） | 日报/周报自动化 |

## 参考平台生态

| 平台 | 特点 | GitHub |
|------|------|--------|
| PostHog | 开源产品分析，漏斗/留存/特征标记 | PostHog/posthog |
| Matomo | 开源 GA 替代，隐私优先 | matomo-org/matomo |
| Countly | 移动端产品分析 | Countly/countly-server |
| Jitsu | 实时事件数据管道 | jitsucom/jitsu |
| Notion Growth | Product Analytics × Notion 集成 | iamAyushSaxena/Product-Analytics-Notion-Growth |

## 执行流程

```
Step 1: 业务理解
  → 产品类型（SaaS/消费/工具/内容）
  → 商业模式（订阅/广告/交易/服务）
  → 当前最关键的业务问题

Step 2: 指标设计
  → 北极星指标（单一 + 可量化 + 与价值强相关）
  → 一级指标（直接驱动北极星）
  → 二级指标（可干预的行动指标）
  → 护栏指标（不能变差的底线）

Step 3: 埋点规划（event 模式）
  → 事件分类（用户行为/产品状态/业务事件）
  → 命名规范（对象_动词，如 button_clicked）
  → 属性设计（通用属性 + 事件专属属性）

Step 4: 分析输出
  → SQL 查询示例（如适用）
  → PostHog/Matomo 配置代码
  → 看板截图模板描述

Step 5: 行动建议
  → 数据驱动的优化假设
  → A/B 实验设计
  → 下一个关注周期
```

## 输出示例（event 模式）

```javascript
// PostHog 埋点示例
posthog.capture('feature_used', {
  feature_name: 'prd_generator',
  mode: 'full',
  user_tier: 'pro',
  time_to_complete_ms: 3200,
  output_word_count: 1500
})

// 事件清单
// page_viewed        { page_name, referrer }
// button_clicked     { button_id, page_context }
// feature_used       { feature_name, mode }
// upgrade_triggered  { trigger_point, current_plan }
// error_occurred     { error_type, component }
```

## 使用示例

```
/analytics SaaS 订阅产品指标体系设计
/analytics 用户注册到激活的漏斗分析 --mode funnel
/analytics 新用户 7/30/90 天留存分析 --mode cohort
/analytics 产品增长诊断 AARRR --mode growth
/analytics 设计 AI 功能使用埋点方案 --mode event --platform posthog
/analytics 搭建日常运营数据看板 --mode dashboard
```
