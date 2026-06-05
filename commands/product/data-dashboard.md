---
name: data-dashboard
description: >
  基于真实埋点数据生成产品看板。集成 PostHog / Mixpanel / Amplitude / Matomo /
  GA4 / Heap 六大主流分析平台，覆盖北极星看板、AARRR 漏斗看板、
  Cohort 留存看板、收入看板、客户 BR 看板、AI 功能监控看板六类标准模板。
  含 SQL / API 查询模板、看板嵌入代码（iframe / React / Markdown）、
  指标对照（不同平台同一指标的不同口径）、告警阈值设计。
  适用于：搭建产品数据看板、为月报/季报生成数据、客户 BR 数据准备、AI 功能上线监控。
user-invocable: true
argument-hint: "<目标/产品> [--mode design|sql|embed|alert|fullset] [--platform posthog|mixpanel|amplitude|matomo|ga4|heap] [--type northstar|aarrr|cohort|revenue|customer-br|ai-monitor]"
allowed-tools: [Read, Write, WebFetch, Bash]
---

# /data-dashboard — 产品数据看板生成

加载技能：`skills/data-dashboard/SKILL.md`

## 触发条件
搭建产品数据看板、为月报/季报生成数据、客户 BR 数据准备、AI 功能上线监控、北极星追踪、漏斗看板。

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `<目标/产品>` | 看板主题（必填） | — |
| `--mode` | 输出模式 | `design` |
| `--platform` | 分析平台 | `posthog` |
| `--type` | 看板类型 | `northstar` |

### 模式（--mode）
| 值 | 输出 | 适用 |
|----|------|------|
| `design` | 看板设计稿（图表选型 + 指标定义）（**默认**） | 设计阶段 |
| `sql` | SQL / API 查询模板（直接可跑） | 工程对接 |
| `embed` | 看板嵌入代码（iframe / React / Markdown） | 文档/PRD 内嵌 |
| `alert` | 告警阈值 + 监控规则 | 上线前配置 |
| `fullset` | 设计 + SQL + 嵌入 + 告警全套 | 完整看板交付 |

### 分析平台（--platform）
| 值 | 类型 | 优势 |
|----|------|------|
| `posthog` | 开源 / SaaS | 一体化，含实验 |
| `mixpanel` | SaaS | 漏斗 / Cohort 强 |
| `amplitude` | SaaS | 行为分析深度 |
| `matomo` | 开源 | 隐私优先、自托管 |
| `ga4` | SaaS | Google 生态 |
| `heap` | SaaS | 自动捕获事件 |

### 看板类型（--type）
| 值 | 内容 |
|----|------|
| `northstar` | 北极星 + 输入指标 + Counter |
| `aarrr` | 五层漏斗 + 各层 Drill-down |
| `cohort` | 队列留存矩阵 + 留存曲线 |
| `revenue` | MRR / ARR / NRR / Churn / LTV |
| `customer-br` | 客户级 KPI 履约（针对单一客户） |
| `ai-monitor` | AI 功能：质量 / 成本 / 安全三维 |

---

## 执行流程

```
Step 1: 业务理解
  → 北极星指标是什么？
  → 当前 baseline 数值
  → 主要决策场景（每日 / 每周 / 每月）

Step 2: 看板结构设计
  → 分区（顶部 KPI / 中部漏斗 / 底部细节）
  → 图表选型（数字 / 折线 / 柱状 / 漏斗 / 留存矩阵）
  → 默认时间范围 + 对比基线

Step 3: 指标定义（Single Source of Truth）
  → 每个指标含：名字 / 计算口径 / 事件 / 属性 / 过滤
  → 同一指标在不同平台的口径差异

Step 4: 查询生成
  → 按 --platform 生成 SQL / Insight URL / API 调用
  → 加性能注释（索引 / 分区 / 采样）

Step 5: 嵌入与分发
  → iframe / React 组件 / Markdown 嵌入
  → 看板权限设置

Step 6: 告警 + 监控
  → 异常阈值（绝对值 / 同比 / 环比）
  → 通知渠道（Slack / 邮件 / 飞书）
```

---

## 输出示例（design 模式 - 北极星看板）

```markdown
# [产品名] 北极星看板

**平台**：PostHog | **刷新**：每日
**默认时间窗**：过去 28 天

## 顶部 KPI 区（4 个数字）
┌────────────────┬────────────────┬────────────────┬────────────────┐
│ 北极星 NSM     │ DAU            │ D7 留存        │ NPS            │
│ 12,500         │ 45,000         │ 38%            │ +42            │
│ ↗️ +15% MoM    │ ↗️ +8%        │ ↗️ +3pp       │ → 0            │
└────────────────┴────────────────┴────────────────┴────────────────┘

## 中部主图（趋势）
- 北极星 12 周折线图（含季度目标线）
- 关键事件标注（实验上线 / 营销 / 故障）

## 底部细节（4 列）
列 1：NSM 拆解（按用户类型）
列 2：地区分布
列 3：渠道贡献
列 4：实验影响（最近 4 个实验对 NSM 的贡献）

## 指标定义

### NSM: 周活跃团队数
- **事件**：core_action_completed
- **过滤**：actor_type = "team_member"
- **聚合**：unique workspace_id
- **时间窗**：滚动 7 天

### D7 留存
- **事件**：page_view
- **Cohort**：注册当周
- **窗口**：注册后第 7 天 ± 1
```

---

## 输出示例（sql 模式 - PostHog HogQL）

```sql
-- 北极星：周活跃团队数（PostHog HogQL）
SELECT
    toStartOfWeek(timestamp) AS week,
    uniq(properties.workspace_id) AS active_teams
FROM events
WHERE event = 'core_action_completed'
  AND properties.actor_type = 'team_member'
  AND timestamp >= now() - INTERVAL 12 WEEK
GROUP BY week
ORDER BY week;

-- D7 留存（Cohort 矩阵）
SELECT
    toStartOfWeek(first_seen) AS cohort_week,
    floor(dateDiff('day', first_seen, timestamp) / 1) AS day_offset,
    count(DISTINCT person_id) AS retained_users
FROM (
    SELECT
        person_id,
        timestamp,
        min(timestamp) OVER (PARTITION BY person_id) AS first_seen
    FROM events
    WHERE event = 'page_view'
      AND timestamp >= now() - INTERVAL 8 WEEK
)
WHERE day_offset BETWEEN 0 AND 30
GROUP BY cohort_week, day_offset
ORDER BY cohort_week DESC, day_offset;

-- 漏斗：注册 → 激活
SELECT *
FROM funnel(
    [
        {event: 'sign_up'},
        {event: 'profile_completed'},
        {event: 'first_project_created'},
        {event: 'first_invite_sent'}
    ],
    24h,
    NULL
)
WHERE timestamp >= now() - INTERVAL 30 DAY;
```

---

## 输出示例（embed 模式）

```markdown
# 嵌入到产品月报

## iframe 嵌入

```html
<iframe
  src="https://app.posthog.com/dashboard/12345?token=..."
  width="100%"
  height="600"
  frameborder="0">
</iframe>
```

## React 组件嵌入

```jsx
import { Dashboard } from '@posthog/react'

<Dashboard
  apiKey={process.env.POSTHOG_KEY}
  dashboardId={12345}
  defaultDateRange="-28d"
/>
```

## Markdown 静态截图嵌入（适合月报）

![北极星 28 天趋势](./snapshots/nsm-2026-06.png)
*北极星：12,500（+15% MoM），过去 28 天稳步上升，第 W22 实验上线后加速*

## 嵌入到 PRD / Spec（auto-fetch）

```markdown
[//]: # (data-dashboard:northstar:posthog:12345:auto-render)
```
（CI 会自动拉数据生成最新截图）
```

---

## 输出示例（alert 模式）

```markdown
# 告警与监控规则

## 北极星
- 🟡 WARN：周环比 < +0%（停滞）
- 🔴 CRIT：周环比 < -10%（重大下滑）
- 🟢 OK：周环比 ≥ +2%

## 漏斗
- 🟡 WARN：注册→激活 < 25%
- 🔴 CRIT：注册→激活 < 15%
- 🔴 CRIT：任意层日环比下降 > 30%

## D7 留存
- 🔴 CRIT：D7 留存 < 25%
- 🟡 WARN：留存曲线斜率突变（断崖式）

## AI 功能（如适用）
- 🔴 CRIT：幻觉率（用户标"无用"）> 20%
- 🟡 WARN：平均延迟 P95 > 5s
- 🔴 CRIT：日成本 > 月预算 / 25 天（消耗速度异常）

## 通知配置
```yaml
alerts:
  - rule: northstar_drop
    channels: [slack:#product-alerts, email:pm@company.com]
    suppress_window: 4h
  - rule: ai_hallucination_high
    channels: [slack:#ai-on-call, pagerduty]
    suppress_window: 30m
```
```

---

## 与其他命令的协同

```
/data-dashboard（本命令）
  ├── /analytics → 设计指标体系（先于本命令）
  ├── /product-strategy --mode northstar → 北极星定义 → 看板顶部
  ├── /ab-test → 实验影响标注在看板趋势图
  ├── /pmf-survey → PMF 信号雷达 → 看板组件
  └── /product-report → 月报/季报基于看板数据

推荐工作流：
  搭看板（一次性）：
    /analytics --mode metrics（指标体系）
    → /data-dashboard --mode design
    → /data-dashboard --mode sql（工程对接）
    → /data-dashboard --mode embed（嵌入到文档）
    → /data-dashboard --mode alert（告警配置）

  月度报告：
    /data-dashboard --mode embed > snapshots/2026-06.png
    → /product-report --mode monthly
```

---

## 使用示例

```bash
# 设计北极星看板（默认）
/data-dashboard 周活跃团队数

# 生成 PostHog SQL 查询
/data-dashboard 注册激活漏斗 --mode sql --type aarrr

# Mixpanel 留存看板
/data-dashboard 用户 D7/D30 留存 --platform mixpanel --type cohort

# 收入看板
/data-dashboard SaaS 月度收入 --type revenue --mode fullset

# 客户级 BR 看板（针对单一大客户）
/data-dashboard Acme Corp Q1 BR --type customer-br --mode design

# AI 功能上线监控
/data-dashboard AI 客服监控 --type ai-monitor --mode fullset --platform posthog

# 嵌入代码（嵌入月报 / 看板）
/data-dashboard 北极星看板 --mode embed --platform posthog

# 告警阈值
/data-dashboard 全产品 AARRR --mode alert --type aarrr
```
