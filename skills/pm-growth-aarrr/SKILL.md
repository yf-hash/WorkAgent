---
name: pm-growth-aarrr
description: >
  AARRR 增长漏斗框架知识库。覆盖五层指标（Acquisition/Activation/Retention/Revenue/Referral）的
  关键 KPI 与设计要点。用于增长诊断、漏斗分析、北极星拆解的子指标层。
  触发词：AARRR、海盗指标、增长漏斗、CAC、激活率、Aha Moment、留存、ARPU、LTV、NPS、K-factor
user-invocable: false
effort: low
---

# PM Growth AARRR — 海盗指标增长漏斗

> 单一职责：AARRR 五层漏斗的指标定义与设计要点。
> 不做：北极星指标设计（→ `pm-north-star`）、看板生成（→ `dashboard-aarrr`）

## 五层漏斗

```
Acquisition（获客）   →   Activation（激活）   →   Retention（留存）
                                                        ↓
                              Referral（推荐）   ←   Revenue（变现）
```

## A1: Acquisition（获客）

```
关键 KPI：
- CAC（Customer Acquisition Cost）：单个客户获取成本
- 流量渠道占比：自然 / 付费 / 推荐 / SEO 各占比
- 渠道 ROI：(LTV - CAC) / CAC，> 3 为健康
- 注册转化率：访客 → 注册的转化

诊断要点：
- CAC 持续上涨而留存不变 → 渠道质量下降
- 单一渠道 > 60% → 渠道集中风险
- 注册转化 < 5% → 注册流程过重
```

## A2: Activation（激活）

```
关键 KPI：
- Aha Moment 到达率：新用户达到核心价值瞬间的比例
- 新用户 D1 完成度：首次使用核心功能的比例
- TTV（Time To Value）：注册到 Aha Moment 的时间

Aha Moment 示例：
- Twitter：关注 30 人 + 7 天内登录 ≥ 4 次
- Facebook：10 天内加 7 个好友
- Slack：团队发送 2000 条消息
- Dropbox：1 台设备上传 1 个文件并访问

诊断要点：
- 激活率 < 20% → Onboarding 体验差或 PMF 弱
- TTV > 24 小时 → 引导流程冗长
```

## A3: Retention（留存）

```
关键 KPI：
- D1/D7/D30/D90 留存率
- DAU/WAU/MAU
- 留存曲线（Cohort）
- Churn Rate：N 期未活跃的流失率

留存曲线类型：
- 死亡曲线：持续下降到 0 → 无 PMF
- L 型曲线：稳定在 N% → 有 PMF
- 微笑曲线：先降后升 → 强 PMF + 唤回成功

诊断要点：
- D7 < D1/2 → 早期流失严重，Onboarding 问题
- 老用户曲线和新用户曲线差距大 → 留存随时间改善
```

## A4: Revenue（变现）

```
关键 KPI：
- ARPU（每用户平均收入）
- LTV（用户生命周期价值）
- LTV / CAC：> 3 健康，> 5 优秀
- 付费转化率：免费 → 付费
- ARR / MRR：B 端订阅业务核心
- NRR（Net Revenue Retention）：> 100% 表示扩张

诊断要点：
- 付费转化 < 2% → 价值未传递 / 定价错位
- NRR < 100% → 流失超过扩张，业务衰退
- LTV/CAC < 1 → 业务亏损，不可持续
```

## A5: Referral（推荐）

```
关键 KPI：
- NPS（Net Promoter Score）：推荐者 - 贬损者
- K-factor：每个用户带来的新用户数（> 1 病毒传播）
- 分享率：实际分享 / 看到分享按钮
- 邀请转化：邀请发出 / 邀请人接受

K-factor 公式：
K = i × c
i = 每个用户发出邀请数
c = 每个邀请的转化率

诊断要点：
- NPS < 30 → 用户口碑弱
- K < 0.1 → 几乎无病毒传播
- 分享率 > 10% 但转化 < 5% → 落地页问题
```

## 全漏斗诊断顺序

```
出现问题，自顶向下排查：
1. Acquisition 数量 OK 吗？质量呢？
2. Activation 率正常吗？Aha 路径有断点吗？
3. D1/D7 留存崩了吗？
4. 付费转化正常吗？
5. Referral 出来了吗？

不要跳到下游优化 — 上游漏了，下游再优化也是漏斗变小。
```
