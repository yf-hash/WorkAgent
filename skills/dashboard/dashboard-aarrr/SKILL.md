---
name: dashboard-aarrr
description: >
  AARRR 漏斗看板生成知识库。模板结构：顶部 5 KPI（每层一个数字+转化率）→ 中部漏斗图+每层 vs Benchmark/上月对比→ 底部每层 Drill-down（按渠道/设备/地区）+流失节点 Top 3。含 PostHog HogQL 漏斗查询模板。
触发词：AARRR 看板、漏斗看板、转化漏斗、海盗指标看板
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

# Dashboard AARRR — 海盗指标漏斗看板

> 单一职责：AARRR 漏斗看板模板与查询。
> 不做：AARRR 指标设计本身（→ `pm-metrics-frameworks` §二）、北极星看板（→ `dashboard-northstar`）

## 看板模板

```
顶部：5 KPI（每层一个数字 + 转化率）
  Acquisition: N 注册 / 渠道占比
  Activation:  N 激活 / Aha 到达率
  Retention:   D1/D7/D30
  Revenue:     付费转化 / ARPU
  Referral:    NPS / K-factor

中部：
  - 漏斗图（Acquisition → Activation → Retention → Revenue → Referral）
  - 每层 vs Benchmark / 上月对比
  - 每层 vs 行业基准（如有）

底部：
  - 每层 Drill-down（按渠道 / 设备 / 地区）
  - 流失节点 Top 3（哪里掉得最严重）
  - 关键改进实验进展
```

## PostHog HogQL 漏斗查询

```sql
SELECT *
FROM funnel(
    [
      {event: 'page_view', properties: {pathname: '/'}},
      {event: 'sign_up'},
      {event: 'first_project_created'},
      {event: 'first_invite_sent'}
    ],
    7d
)
WHERE timestamp >= now() - INTERVAL 30 DAY;
```

## 看板设计要点

- 漏斗每层标注绝对数 + 转化率（不要只标一种）
- 加 Benchmark 对比线（行业 / 历史 / 目标）
- Drill-down 维度选有行动空间的（渠道可调、地区可调，设备类型一般无解）
- 流失节点 Top 3 必须可点击跳转到该节点详情

## 自顶向下诊断顺序

```
看板使用流程：
1. 看顶部 5 KPI，哪层最弱？
2. 看中部漏斗，弱在哪两层之间？
3. 看底部 Drill-down，是某个细分群更弱吗？
4. 看流失节点 Top 3，是技术问题还是体验问题？

❌ 不要跳到下游优化 — 上游漏了，下游再优化也是漏斗变小。
```

## 告警建议

```
P0：某层日环比 -30%（突变）
P1：关键层环比连续 3 周下降 > 5%
P2：长尾层缓慢恶化（月度关注）
```
