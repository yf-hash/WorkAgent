---
name: analytics
description: >
  产品数据指标设计 — 指标体系 + 漏斗 + 留存 + 埋点四件套。
  产品分析的"上游设计"层。
  
  与相邻命令的边界（防混淆）：
  - vs /dashboard 看板系列：本命令做"指标定义 / 计算口径 / 埋点 Schema"，
    /dashboard --metric northstar|aarrr|cohort 等做"看板可视化 + SQL 查询 + 嵌入"。
    指标定下来后再去做看板。
user-invocable: true
argument-hint: "<分析目标> [--mode metrics|funnel|cohort|event] [--platform posthog|matomo|countly|jitsu]"
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

# /analytics — 产品数据指标设计

加载技能：`skills/data/product-analytics/SKILL.md`

## 触发条件
设计指标体系、定义漏斗、规划埋点 Schema，或为后续看板 / 实验提供数据基础时。

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `<分析目标>` | 分析问题或产品模块（必填） | — |
| `--mode` | 分析类型 | `metrics` |
| `--platform` | 目标平台 | `posthog` |

### 分析模式（已聚焦）
| `--mode` | 输出内容 | 适用场景 |
|----------|---------|---------|
| `metrics` | 指标体系设计（北极星 + 输入 + 护栏） | 产品定义、季度规划 |
| `funnel` | 漏斗定义（事件序列 + 转化口径） | 注册/付费/激活路径 |
| `cohort` | 留存定义（Cohort 切片 + 留存口径） | 用户质量评估 |
| `event` | 埋点 Schema（事件命名 + 属性 + 代码示例） | 前端工程师对接 |

### ⚠️ 已迁移的能力
- 看板设计 → 使用 `/dashboard --metric northstar|aarrr|cohort` 等（v2.8 起统一入口）

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
/analytics 用户注册到激活的漏斗 --mode funnel
/analytics 新用户 7/30/90 天留存 --mode cohort
/analytics 设计 AI 功能使用埋点方案 --mode event --platform posthog
```

## 推荐工作流

```
1. /analytics --mode metrics（定义指标体系）
2. /analytics --mode event（产出埋点 Schema）
3. 工程实施
4. `/dashboard --metric northstar|aarrr|cohort`（基于指标做对应看板）
```
