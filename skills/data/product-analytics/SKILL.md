---
name: product-analytics
description: >
  产品数据分析知识库。触发词：指标体系、北极星指标、漏斗分析、留存分析、Cohort、埋点设计、
  PostHog、Matomo、Countly、Jitsu、增长分析、AARRR、DAU/MAU、用户行为分析、事件跟踪、
  数据看板、A/B 测试、增长诊断、用户分群。
user-invocable: false
effort: medium
harness:
  execute:
    preset: research
  constrain:
    profile: writing-safe
  loop:
    mode: one-shot
  memory:
    scope: project
    reads: [project-context]
  security:
    danger-level: low
---

# Product Analytics — 产品数据分析知识库

## 指标体系设计

### 北极星指标选择标准
```markdown
一个好的北极星指标必须：
✅ 代表用户从产品中获得的核心价值
✅ 可量化、唯一、可分解
✅ 与商业目标（收入/增长）强相关
✅ 团队行动能直接影响它
✅ 不是收入本身（收入是结果，不是价值）

典型案例：
- Slack：每日发送的消息数
- Spotify：每月总收听分钟数
- Airbnb：被预订的夜晚数量
- Notion：每周使用产品协作的团队数
- WhatsApp：每日发送的消息数
```

### 指标体系层级
```markdown
Level 0: 北极星指标（1个）
Level 1: 一级驱动指标（3-5个，直接影响北极星）
Level 2: 二级运营指标（可干预的行动指标）
Level 3: 护栏指标（不能变差的底线指标）

示例（SaaS 工具）：
L0: 每周活跃使用核心功能的用户数（WAU-core）
L1: 新用户激活率 | 7日留存率 | 功能渗透率
L2: 注册转化率 | 引导完成率 | 功能发现率
L3: 错误率 < 0.1% | P99延迟 < 2s | Churn < 5%/月
```

## 漏斗分析

### 核心漏斗模板
```markdown
## 用户生命周期漏斗
访问 → 注册 → 激活 → 留存 → 付费 → 推荐

典型基准（SaaS B2C）：
访问 → 注册：2-5%
注册 → 激活：30-60%（取决于激活定义）
激活 → 7日留存：40-60%
7日留存 → 付费：5-15%
付费用户 NPS：>50 被认为良好

## 功能使用漏斗
进入页面 → 发现入口 → 点击尝试 → 完成操作 → 再次使用

流失分析维度：
- 在哪一步流失最多？
- 哪类用户流失更严重（设备/渠道/时间）？
- 流失用户的共同特征是什么？
```

## 留存分析

### Cohort 分析解读
```markdown
## 留存曲线形态
1. 持续下降（不健康）：产品未找到 PMF
   → 重新审视核心价值主张

2. 趋于平缓（健康）：有忠实用户群
   → 提升平缓线的高度（激活优化）

3. 先降后升（付费用户）：正常，尤其 B2B
   → 关注付费后的深度使用

## 关键留存节点
D1（次日留存）：初始体验的直接反馈
D7（7日留存）：是否形成使用习惯
D30（月留存）：长期价值验证
D90（季度留存）：产品黏性的真实考验
```

## 埋点设计规范

### 事件命名规范
```markdown
格式：[对象]_[动词]（全小写，下划线分隔）

对象（Object）：
page, button, feature, modal, form, menu, card, tab

动词（Verb）：
viewed, clicked, submitted, completed, failed, skipped, 
started, finished, upgraded, cancelled

示例：
✅ page_viewed
✅ button_clicked
✅ feature_used
✅ form_submitted
✅ onboarding_completed
✅ subscription_upgraded
✅ error_occurred

❌ viewPage（驼峰）
❌ click（无对象）
❌ userClickedButtonOnDashboard（过于冗长）
```

### 通用属性（每个事件都带）
```javascript
// 通用属性
{
  // 用户维度
  user_id: "uuid",
  user_tier: "free|pro|enterprise",
  user_signup_date: "2024-01-15",
  
  // 会话维度
  session_id: "uuid",
  session_start_time: "ISO8601",
  
  // 环境维度
  platform: "web|ios|android",
  device_type: "desktop|mobile|tablet",
  
  // 页面维度
  page_name: "dashboard",
  page_url: "/dashboard",
  referrer: "email|organic|paid"
}
```

### PostHog 集成示例
```javascript
import posthog from 'posthog-js'

// 初始化
posthog.init('YOUR_API_KEY', {
  api_host: 'https://app.posthog.com',
  capture_pageview: true,
  autocapture: false  // 手动控制，避免噪音
})

// 用户识别
posthog.identify('user_123', {
  email: 'user@example.com',
  plan: 'pro',
  company: 'Acme Corp'
})

// 功能使用埋点
posthog.capture('feature_used', {
  feature_name: 'prd_generator',
  mode: 'full',
  output_length: 1500,
  time_to_complete_ms: 3200
})

// 功能标记（Feature Flags）
if (posthog.isFeatureEnabled('new-editor')) {
  // 展示新编辑器
}
```

### Matomo 集成示例
```javascript
// Matomo 事件跟踪
_paq.push(['trackEvent', 
  'Feature',          // 类别 (Category)
  'PRD Generator',    // 动作 (Action)  
  'Full Mode',        // 标签 (Label, 可选)
  1500                // 值 (Value, 可选)
])

// 目标转化追踪
_paq.push(['trackGoal', 1]) // 注册完成
_paq.push(['trackGoal', 2]) // 付费转化
```

## A/B 测试设计

```markdown
## 实验设计清单
- [ ] 假设清晰（改变X会导致Y提升Z%）
- [ ] 主指标已定义（可测量、可提升的核心指标）
- [ ] 护栏指标已定义（不能恶化的指标）
- [ ] 样本量已计算（统计显著性要求：80% power，5% alpha）
- [ ] 实验时长已确定（建议至少 2 周，覆盖周期效应）
- [ ] 互斥实验已检查（与其他实验不冲突）
- [ ] 回滚方案已准备

## 样本量估算公式（简化）
最小样本量 ≈ 16 × (σ/δ)²
其中 σ 为标准差，δ 为最小可检测效果（MDE）

实践建议：
- MDE 通常设为 5-10%（不要追求检测 1% 的效果）
- 运营时间 = 达到样本量所需天数 + 缓冲期
```

## 数据看板设计

```markdown
## 日运营看板（每日检查）
必看指标：DAU、新增用户、核心功能使用率、错误率、P99延迟

## 增长看板（每周回顾）
注册量、激活率、D7留存、付费转化率、MRR/收入

## 产品健康看板（每月复盘）
D30留存、NPS趋势、功能渗透率、Cohort对比、AB实验汇总

图表选型原则：
- 趋势：折线图
- 对比：柱状图
- 构成：堆叠柱/饼图（少用）
- 分布：直方图
- 漏斗：漏斗图
- 矩阵：热力图
```
