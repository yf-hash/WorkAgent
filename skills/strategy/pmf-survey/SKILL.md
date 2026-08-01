---
name: pmf-survey
description: >
  Product-Market Fit（PMF）评估方法论知识库。覆盖 Sean Ellis 经典 PMF 测试
  ("if you could no longer use, how would you feel?") + 40% 阈值起源、
  Rahul Vohra（Superhuman）四步法、Brian Balfour 增长金字塔、
  High-Expectation Customer（HXC）识别、PMF 综合信号（留存 / NPS / 病毒
  / 自然流量）、PMF 前后行为差异、不达 PMF 的 Pivot 决策。
  触发词：PMF、Product-Market Fit、产品市场契合、Sean Ellis、Superhuman、
  40% 法则、High-Expectation Customer、HXC、PMF 信号、Pivot
user-invocable: false
effort: high
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

# PMF Survey — Product-Market Fit 评估知识库

把"我们到 PMF 了吗"从主观判断变成可量化、可重复的测量。

---

# 一、PMF 不是什么

```
❌ "我有用户" → 用户量不等于 PMF
❌ "用户说喜欢" → 嘴上说和不能没你不一样
❌ "上了热搜"  → 短期声量不等于长期需求
❌ "VC 投资"   → 资本判断也会错
❌ "竞品被收购" → 市场被验证不等于你被验证

✅ PMF = "如果你的产品消失，目标用户会真的痛"
```

---

# 二、Sean Ellis PMF 测试

## 2.1 起源

```
Sean Ellis 在 Dropbox / LogMeIn 等公司工作时发现：
  问"如果不能再用这个产品，你会感到？"
  非常失望 ≥ 40% 的产品，几乎都达成了快速增长

低于 40% 的产品，往往陷入增长困境
```

## 2.2 标准问题

```
"How would you feel if you could no longer use [产品]?"
A. Very disappointed     ← 关键
B. Somewhat disappointed
C. Not disappointed
D. N/A — I no longer use it
```

## 2.3 阈值解读

| A 占比 | 解读 | 行动 |
|--------|------|------|
| ≥ 50% | Strong PMF | 全力放大 |
| 40-49% | PMF | 推广 + 优化弱项 |
| 25-39% | 接近 PMF | 深度优化 |
| 10-24% | Pre-PMF | 重定位 / 重设计 |
| < 10% | 远未到 PMF | Pivot 决策 |

## 2.4 调研对象的关键

```
✅ 必须是 Activated User
   - 注册 ≥ 1 周
   - 使用 ≥ 2 次
   - 完成核心动作

❌ 错误对象：
   - 全部注册用户（包含未激活）
   - 内部员工 / 朋友
   - 未付费用户调研付费产品
```

---

# 三、Rahul Vohra（Superhuman）四步法

```
Step 1：缩小焦点
  → 不问全部用户，只问"非常失望"用户
  → 找出他们的共性 = HXC（High-Expectation Customer）

Step 2：分析高频价值
  → 问"产品对你最大的帮助是什么"
  → 在 HXC 中找到 Top 3 价值

Step 3：双轴优化
  → 一边强化 HXC 喜爱的功能（Why You Love）
  → 一边解决"有点失望"用户的痛（On the Fence）

Step 4：循环迭代
  → 每季度做一次 PMF 测试
  → 跟踪 40% 数字变化
```

---

# 四、High-Expectation Customer（HXC）

## 4.1 定义

```
HXC = 选 "非常失望" 的用户中具有共同特征的人群

特征维度：
  - 行业 / 公司规模 / 角色
  - 使用频次 / 场景
  - 付费意愿 / 推荐意愿
```

## 4.2 价值

```
✅ 真正爱产品的人 → 反映产品真实价值
✅ 营销应该针对 HXC，而非泛泛推广
✅ 产品方向应满足 HXC 的延伸需求
✅ 招聘 / 融资材料中的"理想用户"
```

## 4.3 操作

```
1. 把 A 答案的用户单独导出
2. 看他们的画像数据（行业 / 规模 / 角色）
3. 看共同特征（如 80% 是设计师 + 5-20 人团队）
4. 这个画像就是你的 HXC
```

---

# 五、PMF 综合信号（多维度交叉验证）

单看 Sean Ellis 不够，组合 4-5 个信号才稳：

| 信号 | 健康线 | 测量 |
|------|-------|------|
| Sean Ellis | A ≥ 40% | 调研 |
| 留存曲线 | D30 在 25%+ 且趋于平缓 | Cohort 分析 |
| NPS | ≥ +40 | NPS 调研 |
| 病毒系数（K）| ≥ 0.5 | 邀请追踪 |
| 自然流量增长 | 月 +10%+ | Analytics |
| 付费转化（如适用）| 行业 benchmark + | 漏斗 |

判定矩阵：
- 4-5 个达标 → ✅ Strong PMF
- 3 个达标 → ✅ PMF
- 2 个达标 → ⚠️ 接近
- 1 个或 0 个 → ❌ Pre-PMF

---

# 六、Pre-PMF vs Post-PMF 行为差异

## 6.1 Pre-PMF（应该聚焦）

```
✅ 跟用户聊（每周 ≥ 5 次访谈）
✅ 反复迭代核心价值
✅ 测试不同定位 / 表达
✅ 不投放（投放掩盖产品问题）
✅ 不招太多人（保持灵活）

❌ 加新功能（先把核心做好）
❌ 优化引导（先确定值得引导的功能）
❌ 写销售物料（产品没定型就写白搭）
```

## 6.2 Post-PMF（应该放大）

```
✅ 招销售 / 营销
✅ 启动 Paid Channel
✅ 优化漏斗 / Onboarding
✅ 写销售物料 / 培训材料
✅ 建立客户成功体系

❌ 大改产品（PMF 后稳定核心）
❌ 进入新市场（先在原市场扩展）
```

---

# 七、Pivot 决策（不达 PMF 时）

## 7.1 何时 Pivot

```
连续 2-3 个月：
  - PMF < 25%
  - 留存曲线持续下降
  - 没有自然增长
  - 增加投入也不增长
```

## 7.2 Pivot 类型（Eric Ries）

```
1. Zoom-In Pivot：聚焦原产品的某个功能成为新产品
2. Zoom-Out Pivot：原产品成为新更大产品的一部分
3. Customer Segment Pivot：换目标客户
4. Customer Need Pivot：发现客户更痛的需求
5. Platform Pivot：从应用变成平台
6. Business Architecture Pivot：B2C → B2B 或反过来
7. Value Capture Pivot：换变现方式
8. Engine of Growth Pivot：换增长模型（病毒/付费/粘性）
9. Channel Pivot：换分发渠道
10. Technology Pivot：换技术实现
```

## 7.3 Pivot 之前先问

```
1. 是 PMF 没到，还是只是短期波动？
2. 客户访谈是否给了清晰的 Pivot 方向？
3. 团队是否还有能量再 Pivot 一次？
4. 资源能否支撑 Pivot 后再跑 6 个月？
```

---

# 八、PMF 调研触达模板

## 8.1 邮件模板

```
主题：5 分钟，帮我们做得更好（[产品名]）

正文：
你好 [姓名]，

我是 [产品名] 的 [角色]，我们正在做产品方向的调整，
你的回答会直接影响我们的下一步。

只需 5 分钟，4 个问题。

[问卷链接]

非常感谢，
[姓名]
```

## 8.2 应用内弹窗

```
触发条件：使用 ≥ 1 周 + 已完成核心动作

弹窗文案：
"嗨，我们想听你的真实想法（5 分钟）"
[去回答] [稍后]
```

## 8.3 一对一访谈

```
适合：早期 < 100 用户
触达：私聊 / 邮件邀约
时长：15-30 分钟
形式：先问 4 题 + 深度追问
```

---

# 九、PMF 调研频率

```
早期（0-6 个月）：每月 1 次（小样本，快速迭代）
PMF 后（6+ 个月）：每季度 1 次
重大改版后：1 个月窗口期再测
新市场扩展：进入后 2 个月测
```

---

# 十、与其他知识库的关系

| 知识库 | 协作方式 |
|--------|---------|
| `mvp-canvas` | MVP 验证后才能做 PMF 测试 |
| `user-research` | PMF 调研是用户研究方法之一 |
| `product-strategy` | PMF 数据 → 调整 UVP / Solution |
| `pricing-strategy` | PMF 后才能稳定定价 |
| `user-feedback` | NPS 调研协同 PMF 信号 |
