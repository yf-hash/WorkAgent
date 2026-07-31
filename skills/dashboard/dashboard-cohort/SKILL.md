---
name: dashboard-cohort
description: >
  Cohort 留存看板生成知识库。模板结构：顶部 3 KPI（D1/D7/D30 留存）→ 中部留存矩阵热力图（行：注册 Cohort 按周；
  列：注册后天数；颜色：留存率）→ 底部留存曲线（多 Cohort 对比）+Power User 占比。含 HogQL Cohort 留存查询模板。
  触发词：留存看板、Cohort 看板、留存矩阵、留存曲线、Cohort retention
user-invocable: false
effort: low
---

# Dashboard Cohort — 留存看板

> 单一职责：Cohort 留存看板模板与查询。
> 不做：留存策略本身（→ `pm-metrics-frameworks` §二·A3 留存）、流失分析（→ `churn-analysis`）

## 看板模板

```
顶部：3 KPI
  - D1 留存
  - D7 留存
  - D30 留存

中部：留存矩阵（热力图）
  - 行：注册 Cohort（按周）
  - 列：注册后天数（D1/D3/D7/D14/D30/D60/D90）
  - 颜色：留存率（深色 = 高留存）

底部：
  - 留存曲线（多 Cohort 对比）
  - Power User 占比（DAU/MAU > 50% 的用户）
  - 留存曲线类型识别（死亡 / L 型 / 微笑）
```

## PostHog HogQL Cohort 查询

```sql
WITH cohorts AS (
    SELECT
        person_id,
        toStartOfWeek(min(timestamp)) AS cohort_week
    FROM events
    WHERE event = 'sign_up'
    GROUP BY person_id
)
SELECT
    cohort_week,
    floor(dateDiff('day', cohort_week, e.timestamp)) AS day_offset,
    count(DISTINCT e.person_id) / count(DISTINCT c.person_id) AS retention_rate
FROM cohorts c
JOIN events e ON c.person_id = e.person_id
WHERE e.event = 'page_view'
GROUP BY cohort_week, day_offset
ORDER BY cohort_week DESC, day_offset;
```

## 留存曲线类型判读

```
死亡曲线（持续下降到 0）
  → 无 PMF，根本没人愿意留下
  → 不要继续投放，回到 Discovery（→ pm-discovery-frameworks）

L 型曲线（先降后趋于稳定）
  → 有 PMF，有一群核心用户
  → 关注 L 的水平段在哪：> 30% 优秀，10-30% 可接受

微笑曲线（先降后升）
  → 强 PMF + 唤回成功 / 网络效应
  → 罕见且珍贵，深入分析为什么会升

新老 Cohort 对比
  → 新 Cohort 留存高于老 → 留存随产品改进
  → 新 Cohort 留存低于老 → 新功能/营销引来错误用户
```

## 看板设计要点

- 热力图最好按周分 Cohort（按天太碎，按月反应慢）
- 列至少包含 D1/D7/D30 三个关键点
- 颜色用单色渐变（避免红绿色盲）
- Power User 占比是早期 PMF 信号，必须含

## 告警建议

```
P0：D7 留存周环比下降 > 5pp
P1：D30 留存月环比下降 > 3pp
P2：留存曲线类型变化（L 型变死亡曲线 = 严重 PMF 衰退）
```
