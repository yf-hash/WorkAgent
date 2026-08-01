---
name: dashboard-northstar
description: >
  北极星看板（NorthStar Dashboard）生成知识库。模板结构：顶部 4 KPI（NSM 当前值+趋势/季度目标+完成率/
  关键 Input 指标/Counter Metric）→ 中部 12-26 周折线（含目标线）→ 底部 NSM 拆解（按用户类型/地区/渠道）+实验影响标注。
  含 PostHog/Mixpanel 查询模板。
  触发词：北极星看板、NorthStar Dashboard、NSM 看板
user-invocable: false
effort: low
harness:
  execute:
    preset: research
  constrain:
    profile: read-only
  loop:
    mode: one-shot
  memory:
    scope: project
    reads: [project-context]
  security:
    danger-level: low
---

# Dashboard NorthStar — 北极星看板

> 单一职责：北极星看板模板与查询。
> 不做：北极星指标设计本身（→ `pm-metrics-frameworks` §一）、AARRR 漏斗看板（→ `dashboard-aarrr`）

## 看板模板

```
顶部：4 KPI
  - NSM 当前值 + 趋势
  - 季度目标 + 完成率
  - 关键 Input 指标 1-2 个
  - Counter Metric（护栏指标）

中部：12-26 周折线
  - 主线：NSM 周值
  - 目标线：季度目标外推
  - 实验标注：A/B 实验、故障、营销活动

底部：
  - NSM 拆解（按用户类型 / 地区 / 渠道）
  - 实验影响标注（点击查看实验详情）
```

## 指标定义（Single Source of Truth）

```yaml
metric:
  id: nsm.weekly_active_teams
  name: 周活跃团队数（NSM）
  description: 过去 7 天内有团队成员完成核心动作的工作区数

  event: core_action_completed
  filters:
    - property: actor_type
      operator: equals
      value: team_member

  aggregation:
    type: unique
    field: workspace_id

  time_window: 7d
  granularity: weekly

  benchmarks:
    target: 15000
    healthy_growth: "+5% WoW"

  related_metrics:
    - mau
    - team_invites
    - core_action_per_team
```

## PostHog 查询（HogQL）

```sql
SELECT
    toStartOfWeek(timestamp) AS week,
    uniq(properties.workspace_id) AS nsm
FROM events
WHERE event = 'core_action_completed'
  AND properties.actor_type = 'team_member'
  AND timestamp >= now() - INTERVAL 12 WEEK
GROUP BY week
ORDER BY week;
```

## Mixpanel 查询（JQL）

```javascript
function main() {
  return Events({
    from_date: '2026-01-01',
    to_date: '2026-06-04',
    event_selectors: [{event: 'core_action_completed'}]
  })
  .filter(e => e.properties.actor_type === 'team_member')
  .groupByUser([mixpanel.numeric_bucket('time', mixpanel.daily_time_buckets)],
               mixpanel.reducer.count())
  .reduce(mixpanel.reducer.sum());
}
```

## 看板设计要点

- 顶部 KPI 必须含 Counter Metric（防止 NSM 被异化）
- 折线图必须叠加目标线，让"达成与否"一目了然
- 实验标注用箭头 + 简短文字，避免覆盖数据
- 拆解维度选 3 个即可，多了反而看不清主要驱动

## 告警建议

```
P1（4 小时内响应）：北极星周环比连续 2 周下降 > 3%
P2（每日关注）：Counter Metric 出现异常波动
```
