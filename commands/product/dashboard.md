---
name: dashboard
description: 统一数据看板入口（7 类：northstar / aarrr / cohort / revenue / customer-br / ai-monitor / platform-selector）。用 --metric 选择看板类型；不填则先跑 platform-selector 决策树。
user-invocable: true
argument-hint: "[--metric northstar|aarrr|cohort|revenue|customer-br|ai-monitor|platform-selector] [--platform posthog|mixpanel|amplitude] [<客户名>]"
allowed-tools: [Read, Write, Edit]
harness:
  execute:
    preset: writing-scoped
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

# /dashboard — 统一数据看板

## 一句话

7 类看板一个入口，`--metric` 分派到对应技能。

## 用法

```bash
# 平台选型（选不出用哪家分析平台时先跑）
/dashboard --metric platform-selector

# 北极星看板
/dashboard --metric northstar --platform posthog

# AARRR 漏斗
/dashboard --metric aarrr

# Cohort 留存（D1/D7/D30 + 热力图 + Power User）
/dashboard --metric cohort

# 收入（MRR/ARR/NRR/Churn/LTV·CAC/Payback + 大客户 Top 10）
/dashboard --metric revenue

# 客户 BR / QBR（合同 + 履约 + 健康度）
/dashboard --metric customer-br 某城商行

# AI 功能监控（质量/成本/安全）
/dashboard --metric ai-monitor
```

## 分派规则

| `--metric` | 加载技能 | 一句话 |
|---|---|---|
| `northstar` | `skills/dashboard/dashboard-northstar/SKILL.md` | NSM 当前值/趋势/季度目标/完成率/Counter Metric/NSM 拆解/实验影响 |
| `aarrr` | `skills/dashboard/dashboard-aarrr/SKILL.md` | 5 层 KPI + 漏斗图 + Benchmark + Drill-down + 流失节点 Top 3 |
| `cohort` | `skills/dashboard/dashboard-cohort/SKILL.md` | D1/D7/D30 KPI + 留存矩阵热力图 + 多 Cohort 曲线 + Power User 占比 |
| `revenue` | `skills/dashboard/dashboard-revenue/SKILL.md` | MRR/ARR/NRR/Churn/LTV·CAC/Payback + MRR 瀑布 + Cohort Rev Retention + 大客户 Top 10 |
| `customer-br` | `skills/dashboard/dashboard-customer-br/SKILL.md` | 合同金额/用户/续约日 + 价值履约 + 关键模块使用 + ROI + 健康度评分 |
| `ai-monitor` | `skills/dashboard/dashboard-ai-monitor/SKILL.md` | 质量（有用率/引用准确率）+ 成本（日成本/单次/vs 预算）+ 安全（拒答率/越权/Refusal） |
| `platform-selector` | `skills/dashboard/dashboard-platform-selector/SKILL.md` | PostHog/Mixpanel/Amplitude/Matomo/GA4/Heap 六大平台对比 + 决策树 |

## 决策树

```
不确定用哪家分析平台？   → platform-selector
已知平台，要看整体健康？ → northstar
新增/激活/留存漏斗？     → aarrr
用户留存怎么样？         → cohort
商业化健康度？           → revenue
关键客户续约风险？       → customer-br
AI 功能是否失控？        → ai-monitor
```

## 迁移说明（v2.8）

旧命令：`/dashboard-northstar` / `/dashboard-aarrr` / `/dashboard-cohort` / `/dashboard-revenue` / `/dashboard-customer-br` / `/dashboard-ai-monitor` / `/dashboard-platform-selector` 已合并至本命令，用 `--metric <name>` 替代。Skills 层未变，能力完全保留。
