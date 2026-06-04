---
name: data-dashboard
description: >
  数据看板生成知识库。集成 PostHog / Mixpanel / Amplitude / Matomo / GA4 / Heap
  六大主流分析平台。覆盖北极星看板、AARRR 漏斗看板、Cohort 留存矩阵、
  收入看板（MRR/ARR/NRR/Churn）、客户 BR 看板、AI 功能监控看板（质量/成本/安全）
  六类标准模板，含查询模板、嵌入代码、告警规则。
  触发词：data-dashboard、产品看板、北极星看板、漏斗看板、留存看板、
  收入看板、客户 BR、AI 监控、PostHog、Mixpanel、Amplitude、Matomo
user-invocable: false
effort: high
---

# Data Dashboard — 产品看板生成知识库

把"PM 想看的指标"从口头需求 → 真实数据看板，标准化、可嵌入、可监控。

---

# 一、看板设计原则

```
1. 顶部决策，底部细节
   - 顶部：4-6 个核心 KPI（一目了然）
   - 中部：主趋势 + 漏斗
   - 底部：分群 / Drill-down

2. 一个看板回答一个问题
   - 不要把所有数据塞进一个看板
   - 北极星 / AARRR / Cohort / Revenue 分开

3. 含对比，含异常标注
   - 同比 / 环比必须有
   - 实验、故障、营销活动在趋势图标注

4. Single Source of Truth
   - 同一指标只有一个口径定义
   - 文档化指标 + 计算公式
```

---

# 二、六大平台特性对比

| 平台 | 强项 | 弱项 | 价格 |
|------|------|------|------|
| PostHog | 开源 + 实验一体化 | UI 较复杂 | 免费 / 自托管 |
| Mixpanel | 漏斗 / Cohort 强 | 价格高 | 免费 < 100K MAU |
| Amplitude | 行为分析深度 | 学习成本 | 免费 < 10M 事件/月 |
| Matomo | 隐私优先 / 自托管 | 行为分析弱 | 免费 |
| GA4 | Google 生态 | 复杂 + 采样 | 免费 |
| Heap | 自动捕获事件 | 数据量大 | 中高 |

选型决策树：
```
有自建 / 隐私 要求？
  ├── 是 → PostHog 自托管 / Matomo
  └── 否 → 继续

预算优先 vs 功能优先？
  ├── 预算 → PostHog Cloud / GA4
  └── 功能 → Mixpanel / Amplitude

需要 A/B 实验？
  ├── 是 → PostHog（一体化）
  └── 否 → Mixpanel

工程团队偏好开源？
  └── PostHog
```

---

# 三、六类标准看板模板

## 3.1 北极星看板（NorthStar）

```
顶部：4 KPI
  - NSM 当前值 + 趋势
  - 季度目标 + 完成率
  - 关键 Input 指标 1-2 个
  - Counter Metric

中部：12-26 周折线（含目标线）

底部：
  - NSM 拆解（按用户类型 / 地区 / 渠道）
  - 实验影响标注
```

## 3.2 AARRR 漏斗看板

```
顶部：5 KPI（每层一个数字 + 转化率）

中部：
  - 漏斗图（Acquisition → Activation → Retention → Revenue → Referral）
  - 每层 vs Benchmark / 上月对比

底部：
  - 每层 Drill-down（按渠道 / 设备 / 地区）
  - 流失节点 Top 3
```

## 3.3 Cohort 留存看板

```
顶部：3 KPI
  - D1 留存
  - D7 留存
  - D30 留存

中部：留存矩阵
  - 行：注册 Cohort（按周）
  - 列：注册后天数
  - 颜色：留存率（热力图）

底部：
  - 留存曲线（多 Cohort 对比）
  - Power User 占比
```

## 3.4 收入看板（Revenue）

```
顶部：6 KPI
  - MRR / ARR
  - 净留存（NRR）
  - Churn 率
  - LTV / CAC
  - Payback Period
  - 单位经济健康分

中部：
  - MRR 瀑布图（New / Expansion / Contraction / Churn）
  - 月度趋势

底部：
  - 按套餐细分
  - 大客户 Top 10
  - Cohort Revenue Retention
```

## 3.5 客户 BR 看板（Customer Business Review）

```
顶部：客户基础信息
  - 合同金额 / 用户数 / 续约日

中部：价值履约
  - 合同承诺 vs 实际
  - 关键模块使用频次
  - ROI 估算

底部：
  - 月度活跃曲线
  - 反馈与响应表
  - 健康度评分
```

## 3.6 AI 功能监控看板（AI Monitor）

```
顶部：3 维度 KPI
  - 质量：用户标"有用"率 / 引用准确率
  - 成本：日成本 / 单次成本 / vs 预算
  - 安全：拒答率 / 越权拦截 / Refusal 占比

中部：
  - 用户标记趋势
  - 模型延迟 P50/P95/P99
  - 失败模式分布

底部：
  - 失败案例 Top 10（自动归类）
  - HITL 人工兜底量
  - Eval 集回归得分
```

---

# 四、指标定义模板（Single Source of Truth）

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

---

# 五、PostHog 查询模板（HogQL）

## 5.1 北极星

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

## 5.2 漏斗

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

## 5.3 Cohort 留存

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

---

# 六、Mixpanel JQL 模板

```javascript
// 北极星
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

---

# 七、嵌入策略

## 7.1 iframe（最简单）

```html
<iframe
  src="https://app.posthog.com/embedded/dashboard/123?token=xxx"
  width="100%" height="600"
  frameborder="0"
  loading="lazy">
</iframe>
```

## 7.2 截图嵌入（适合月报 / PDF 输出）

```bash
# CI 自动拉数据 + 截图
posthog dashboards export --id 123 --format png > snapshots/2026-06.png
```

## 7.3 实时数据嵌入到 Markdown

```markdown
[//]: # (data-dashboard-widget:nsm)

→ 在文档生成时，被 widget 拉取最新数据替换为图表
```

---

# 八、告警设计

## 8.1 阈值类型

```
绝对值阈值：NSM < 10000
相对阈值：环比下降 > 10%
统计阈值：超过 3σ
预测阈值：实际 vs 预测线偏离 > 20%
```

## 8.2 告警分级

```
🔴 P0：立即响应（On-Call 拉响）
  - 主漏斗某层日环比 -30%
  - 服务可用性 < 99%
  - AI 功能幻觉率 > 30%

🟡 P1：4 小时内响应
  - 北极星周环比停滞
  - D7 留存下降 > 5pp
  - 单位成本超预算 50%

⚪ P2：每日 / 每周关注
  - 长尾指标变化
  - Counter Metric 警告
```

## 8.3 告警风险

```
❌ 告警风暴：阈值过敏 → 团队麻木
✅ 抑制窗口：同一告警 4-24h 内不重复
✅ 升级路径：未响应 30 分钟自动升级
✅ 降噪规则：节假日 / 维护窗口豁免
```

---

# 九、与其他知识库的关系

| 知识库 | 协作 |
|--------|------|
| `product-analytics` | 指标体系设计在前 |
| `product-strategy` | 北极星定义 → 看板顶部 |
| `ab-test` | 实验影响标注 |
| `growth-experiment` | 漏斗看板支撑实验 |
| `pmf-survey` | PMF 信号雷达组件 |
| `product-report` | 月报数据来源 |
| `ai-feature-spec` | AI 监控看板 |
| `chat2db` | 自定义 SQL 探索（与本命令互补） |
