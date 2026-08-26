---
name: dashboard-revenue
description: >
  收入看板（Revenue Dashboard）生成知识库。模板结构：顶部 6 KPI（MRR/ARR/NRR/Churn/LTV·CAC/Payback/单位经济健康分）
  → 中部 MRR 瀑布图（New/Expansion/Contraction/Churn）+月度趋势 → 底部按套餐细分+大客户 Top 10+Cohort Revenue Retention。
  适合 B 端订阅业务、SaaS 商业健康监控。
  触发词：收入看板、MRR 看板、ARR 看板、NRR 看板、SaaS 看板、订阅业务看板
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

# Dashboard Revenue — 收入看板

> 单一职责：B 端订阅业务的收入看板模板与查询要点。

## 看板模板

```
顶部：6 KPI
  - MRR（月度经常性收入）
  - ARR（年度经常性收入）
  - 净留存（NRR）— > 100% 表示扩张
  - Churn 率（Logo Churn / Revenue Churn 双指标）
  - LTV / CAC — > 3 健康，> 5 优秀
  - Payback Period — < 12 个月健康
  - 单位经济健康分（综合评分）

中部：
  - MRR 瀑布图（New / Expansion / Contraction / Churn）
    显示本月 MRR 变化拆解
  - 月度趋势（12-24 个月）
  - ARR Forecast（基于历史趋势外推）

底部：
  - 按套餐细分（Free / Pro / Business / Enterprise 的占比和 ARPU）
  - 大客户 Top 10（合同金额 + 续约风险标签）
  - Cohort Revenue Retention（按签约月 Cohort 的收入留存矩阵）
```

## 关键公式

```
MRR = ∑ (月度套餐价格 × 活跃订阅数)
ARR = MRR × 12

NRR = (期初 MRR + Expansion - Contraction - Churn) / 期初 MRR × 100%
  > 100% → 净扩张（理想状态）
  90-100% → 健康
  < 90% → 业务衰退

Churn 率：
  Logo Churn = 流失客户数 / 期初客户数
  Revenue Churn = 流失 MRR / 期初 MRR
  注：高价值客户流失对 Revenue Churn 影响大

LTV：
  LTV = ARPU × Gross Margin / Monthly Churn Rate
  例：ARPU $100 × 80% 毛利 / 5% 月流失 = $1600

LTV / CAC > 3 → 健康
Payback Period = CAC / (ARPU × Gross Margin)
  < 12 个月 → 健康
```

## MRR 瀑布图要点

```
                    本月 MRR
       期初 MRR  +New +Expansion -Contraction -Churn  = 本月 MRR
       (基线)    (新签) (扩容)    (降级)        (流失)
```

- 用颜色区分：绿色（增量）/ 红色（流失）
- 必须四类全显示，单看 Net 看不出问题

## 看板设计要点

- ARR 是给董事会看的，MRR 是给运营看的，二者都要有
- Churn 必须分 Logo 和 Revenue 双指标
- 大客户 Top 10 必须标注续约日期 + 健康度
- Cohort Revenue Retention 比 Logo Retention 更反映商业价值

## 告警建议

```
P0：NRR 月环比下降 > 5pp
P0：Top 10 大客户健康度 < 60 分
P1：Revenue Churn 月环比上升 > 1pp
P1：CAC 月度上升 > 20% 且 LTV 不变
```

## 配套 Skill

- 定价优化：`pricing-strategy`
- 续约谈判：`@solution-architect`
