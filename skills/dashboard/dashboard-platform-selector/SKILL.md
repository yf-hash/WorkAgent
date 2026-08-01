---
name: dashboard-platform-selector
description: >
  数据分析平台选型决策知识库。覆盖 PostHog / Mixpanel / Amplitude / Matomo / GA4 / Heap 六大平台的强项、弱项、价格对比，
  以及选型决策树（隐私要求 / 预算 vs 功能 / 是否需要 A/B 实验 / 是否偏好开源）。含查询语言速查（HogQL / JQL）。
  触发词：分析平台选型、PostHog vs Mixpanel、数据看板平台、BI 工具选型
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

# Dashboard Platform Selector — 平台选型决策

> 单一职责：选哪个数据分析平台。
> 不做：具体看板模板（→ `dashboard-northstar` / `dashboard-aarrr` 等）

## 六大平台对比

| 平台 | 强项 | 弱项 | 价格 |
|------|------|------|------|
| PostHog | 开源 + 实验一体化 | UI 较复杂 | 免费 / 自托管 |
| Mixpanel | 漏斗 / Cohort 强 | 价格高 | 免费 < 100K MAU |
| Amplitude | 行为分析深度 | 学习成本 | 免费 < 10M 事件/月 |
| Matomo | 隐私优先 / 自托管 | 行为分析弱 | 免费 |
| GA4 | Google 生态 | 复杂 + 采样 | 免费 |
| Heap | 自动捕获事件 | 数据量大 | 中高 |

## 选型决策树

```
有自建 / 隐私要求？
  ├── 是 → PostHog 自托管 / Matomo
  └── 否 → 继续

预算优先 vs 功能优先？
  ├── 预算 → PostHog Cloud / GA4
  └── 功能 → Mixpanel / Amplitude

需要 A/B 实验？
  ├── 是 → PostHog（一体化）
  └── 否 → Mixpanel / Amplitude

工程团队偏好开源？
  └── PostHog

GDPR / 数据本地化必须满足？
  └── Matomo / PostHog 自托管

自动捕获所有事件（不想埋点）？
  └── Heap

Google Ads / Search Console 深度集成？
  └── GA4
```

## 典型场景推荐

```
SaaS 早期（< 50 人）：
  → PostHog Cloud 免费版（够用）

SaaS 增长期（50-500 人，要做 A/B）：
  → PostHog（实验一体化）

SaaS 成熟期（注重行为分析深度）：
  → Mixpanel 或 Amplitude

To C 海外（隐私敏感、欧盟用户）：
  → Matomo 或 PostHog 自托管

中国市场（监管 + 本地化）：
  → 神策 / GrowingIO / 自建

电商（高频转化优化）：
  → GA4 + 自建 BI
```

## 查询语言速查

### PostHog HogQL（类 SQL）

```sql
SELECT toStartOfWeek(timestamp) AS week, uniq(person_id) AS wau
FROM events
WHERE event = 'pageview'
GROUP BY week
ORDER BY week;
```

### Mixpanel JQL（JavaScript）

```javascript
function main() {
  return Events({from_date: '2026-01-01', to_date: '2026-06-01'})
    .filter(e => e.name === 'sign_up')
    .groupBy(['properties.channel'], mixpanel.reducer.count());
}
```

### Amplitude（图形化 + Behavioral Cohorts）

```
不暴露查询语言，所有分析在 UI 中点击拼出来。
适合非技术 PM 自助分析。
```

## 嵌入策略（所有平台通用）

### iframe（最简单）

```html
<iframe
  src="https://app.posthog.com/embedded/dashboard/123?token=xxx"
  width="100%" height="600"
  frameborder="0"
  loading="lazy">
</iframe>
```

### 截图嵌入（适合月报 / PDF 输出）

```bash
posthog dashboards export --id 123 --format png > snapshots/2026-06.png
```

### 实时数据嵌入到 Markdown

```markdown
[//]: # (data-dashboard-widget:nsm)

→ 在文档生成时被 widget 拉取最新数据替换为图表
```

## 配套 Skill（看板模板）

- `dashboard-northstar`
- `dashboard-aarrr`
- `dashboard-cohort`
- `dashboard-revenue`
- `dashboard-customer-br`
- `dashboard-ai-monitor`
