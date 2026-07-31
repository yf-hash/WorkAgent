---
name: product-strategy
description: >
  产品战略画布知识库，覆盖 BMC、Lean Canvas、Value Proposition Canvas、
  Product Vision、North Star Metric 五大战略框架。
  包含画布模板、假设验证方法、北极星设计规则、Pre-Mortem 失败推演、
  战略对齐 OGSM/V2MOM 框架引用。
  触发词：产品战略、商业模式、精益画布、价值主张、产品愿景、北极星指标、
  战略画布、BMC、Lean Canvas、VPC、NSM、立项、融资BP
user-invocable: false
effort: high
---

# Product Strategy — 产品战略画布知识库

战略层面的方法论与模板，统一产品立项、商业模式梳理、价值主张校准、北极星定义的工作流。

---

# 一、战略画布的"三个为什么"原则

```
1. 为什么是这个问题？  → 问题陈述 + 现有替代 + 用户痛点强度
2. 为什么是我们？      → 不公平优势 + 团队禀赋 + 时机窗口
3. 为什么是现在？      → 技术拐点 + 市场窗口 + 用户准备度
```

任何战略画布缺这三个"为什么"中的任何一个，都不能算完成。

---

# 二、Lean Canvas（精益画布）模板

```
┌─────────────────────┬─────────────────┬─────────────────────┐
│ 1. PROBLEM          │ 4. SOLUTION     │ 3. UNIQUE VALUE     │
│  Top 3 problems     │  Top 3 features │     PROPOSITION     │
│                     │                 │  High-concept pitch │
│  EXISTING           │                 │                     │
│  ALTERNATIVES       │                 │                     │
├─────────────────────┼─────────────────┼─────────────────────┤
│ 8. KEY METRICS      │ 9. UNFAIR       │ 2. CUSTOMER         │
│  How you measure    │   ADVANTAGE     │     SEGMENTS        │
│  success            │  Can't be       │  Target customers   │
│                     │  copied/bought  │  Early adopters     │
├─────────────────────┴─────────────────┴─────────────────────┤
│ 5. CHANNELS                                                  │
│   Path to customers                                          │
├──────────────────────────────────────────────────────────────┤
│ 6. COST STRUCTURE        │ 7. REVENUE STREAMS                │
│  Customer Acquisition    │  Revenue Model / Lifetime Value   │
│  Distribution / Hosting  │  Revenue / Gross Margin           │
└──────────────────────────────────────────────────────────────┘
```

填写顺序：2 → 1 → 3 → 4 → 5 → 6+7 → 8 → 9

---

# 三、Business Model Canvas（商业模式画布，9 宫格）

```
KEY PARTNERS │ KEY ACTIVITIES │ VALUE PROP │ CUSTOMER     │ CUSTOMER
             ├────────────────┤            │ RELATIONSHIPS│ SEGMENTS
             │ KEY RESOURCES  │            ├──────────────┤
             │                │            │ CHANNELS     │
─────────────┴────────────────┴────────────┴──────────────┴──────────
COST STRUCTURE              │            REVENUE STREAMS
```

BMC vs Lean 选择：
- 已有产品、商业模式相对成熟 → BMC
- 早期、想法未验证 → Lean Canvas
- 双边平台 → 两侧分别画一份 Lean，再合并 BMC

---

# 四、Value Proposition Canvas（价值主张画布）

```
┌────── 产品/服务 (Value Map) ──────┐  ┌────── 用户 (Customer Profile) ──────┐
│                                   │  │                                     │
│  Products & Services              │  │  Customer Jobs                      │
│  ├─ 我们提供什么                   │  │  ├─ 功能性 Job（要完成的任务）        │
│  └─ ……                            │  │  ├─ 情感性 Job                      │
│                                   │  │  └─ 社会性 Job                      │
│  Pain Relievers                   │  │                                     │
│  ├─ 减少哪些痛苦/障碍/风险          │←→│  Pains                              │
│  └─ ……                            │  │  ├─ 用 Job 时的不爽                 │
│                                   │  │  └─ 担忧/障碍/风险                   │
│  Gain Creators                    │  │                                     │
│  ├─ 创造哪些预期/期望/惊喜收益      │←→│  Gains                              │
│  └─ ……                            │  │  ├─ 必需收益                         │
│                                   │  │  ├─ 期望收益                         │
└───────────────────────────────────┘  │  └─ 惊喜收益                         │
                                       └─────────────────────────────────────┘
```

适配验证：每个 Pain Reliever 对应至少一个真实 Pain，否则是过度设计。

---

# 五、Product Vision Statement（产品愿景声明）

Geoffrey Moore 经典模板：

```
FOR        [target customer]
WHO        [statement of need or opportunity]
THE        [product name]
IS A       [product category]
THAT       [key benefit, compelling reason to buy]
UNLIKE     [primary competitive alternative]
OUR PRODUCT [statement of primary differentiation]
```

例：
```
FOR        中国独立开发者
WHO        想要把英文技术博客快速翻译并适配本地语境发表到知乎/掘金
THE        TransPost
IS A       多平台技术内容本地化助手
THAT       提供专业术语保留 + 平台风格自适配 + 一键多平台发布
UNLIKE     通用机器翻译工具（DeepL/Google Translate）
OUR PRODUCT 内置技术博客领域语料 + 平台风格规则库 + 一站式发布工作流
```

---

# 六、North Star Metric（北极星指标）

## 6.1 NSM 三性原则

```
✅ 用户价值性  → 用户从产品获得真正价值时才计数
✅ 收入相关性  → 与商业模式强相关，能预测长期收入
✅ 行动可控性  → 团队可以通过努力影响这个指标
```

反例：
- ❌ DAU（量大不等于有价值）
- ❌ 注册用户数（沉默用户多）
- ❌ 营收（滞后指标，无法用于决策）

正例：
- ✅ Airbnb：每晚预订夜数（Nights Booked）
- ✅ Slack：发送 2000+ 消息的工作区数
- ✅ Spotify：每月听歌时长
- ✅ Notion：每周创建 5+ 页的工作区

## 6.2 NSM 输入指标设计（L1 → L2）

```
NSM = [广度] × [频率] × [质量]

例：每月听歌时长 = 月活用户数 × 月均听歌天数 × 单日听歌分钟
                    ↓        ↓             ↓
                  Input1   Input2        Input3
```

每个 Input 至少有一个团队/小组负责，每周追踪。

## 6.3 反向指标（Counter Metric）

防止 NSM 被过度优化损害用户体验：
- NSM = 视频观看时长 → Counter = 用户主动取消订阅率
- NSM = 推送打开率 → Counter = 取消通知开关率
- NSM = 订单数 → Counter = 退款率/客诉率

---

# 七、战略假设验证清单（Lean 配套）

将画布每个格子转为可证伪假设：

```
| #  | 假设                          | 致命度 | 验证方法           | 验证成本 | 状态  |
|----|------------------------------|-------|-------------------|---------|------|
| H1 | 用户痛点真实存在               | 致命   | 5-10 次用户访谈     | 1 周     | ⬜   |
| H2 | 用户愿意为此付费              | 致命   | 落地页 + 预付费     | 2 周     | ⬜   |
| H3 | 我们能做出可用产品            | 高     | 4 周 MVP 原型      | 1 月     | ⬜   |
| H4 | 渠道能以合理 CAC 获客         | 高     | 2 周小规模投放      | 2 周     | ⬜   |
| H5 | LTV/CAC ≥ 3                  | 高     | 队列分析 + 续约     | 3 月     | ⬜   |
```

验证顺序：致命假设优先，便宜假设优先。

---

# 八、Pre-Mortem 失败推演

立项时强制做：
> "假设两年后这个产品失败了，请写出最可能的失败原因"

每位团队成员独立写 → 汇总归类 → Top 3 风险有应对预案才能立项。

常见失败类型：
1. **市场未到位**（Too early）→ 早期 Adopter 验证
2. **真实痛点弱**（Nice to have）→ 用户访谈痛苦强度评分
3. **执行力不足**（Wrong team）→ 关键岗位补齐计划
4. **竞争误判**（Underestimated）→ 竞品深度分析
5. **商业模型不闭环**（CAC > LTV）→ 单位经济模型

---

# 九、战略对齐框架（OGSM / V2MOM）

## OGSM
- **O**bjective：定性的方向性目标
- **G**oal：定量的可衡量结果
- **S**trategy：达成目标的策略选择
- **M**easure：策略的执行度量

## V2MOM（Salesforce 经典）
- **V**ision：愿景
- **V**alues：价值观（决策时的取舍依据）
- **M**ethods：方法
- **O**bstacles：障碍
- **M**easures：度量

战略画布产出后建议用 V2MOM 做季度对齐。

---

# 十、与其他知识库的关系

| 知识库 | 协作方式 |
|--------|---------|
| `market-research` | 提供 Customer Segments、Existing Alternatives 数据 |
| `user-feedback` | 提供 Pains 和 Gains 的真实素材 |
| `product-analytics` | 提供 NSM 和 Input 指标的埋点设计 |
| `gtm-strategy` | 接收战略输出，落地为 90 天上市计划 |
| `prd-standard` | 接收 Solution，落地为 PRD/Spec |
| `pricing-strategy` | 深化 Revenue Streams 格子 |
