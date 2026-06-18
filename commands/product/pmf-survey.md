---
name: pmf-survey
description: >
  Product-Market Fit（PMF）评估助手。基于 Sean Ellis 经典 PMF 测试 + Rahul Vohra
  四步法 + Brian Balfour 增长金字塔。覆盖 PMF 四问问卷设计、40% 阈值解读、
  样本筛选（Activated Users）、High-Expectation Customer 识别、
  PMF 信号雷达图（留存 / NPS / 病毒 / 付费）、PMF 后行动剧本、
  Pre-PMF 与 Post-PMF 行为差异。
  适用于：早期产品 PMF 验证、迭代后再测、定位调整后再验证、融资材料准备。
user-invocable: true
argument-hint: "<产品/功能> [--mode survey|analyze|signals|action|fullset] [--users-source user-list|wechat|email]"
---

# /pmf-survey — PMF 评估

加载技能：`skills/pmf-survey/SKILL.md`

## 触发条件
新产品/新版本上线后想验证 PMF、定位调整后想验证有效性、融资前需要 PMF 数据，或团队对"是否到 PMF"有分歧时。

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `<产品/功能>` | 待评估的产品/功能（必填） | — |
| `--mode` | 工作模式 | `survey` |
| `--users-source` | 用户触达渠道 | — |

### 工作模式（--mode）
| 值 | 输出 | 适用场景 |
|----|------|---------|
| `survey` | Sean Ellis PMF 四问问卷设计 + 触达脚本（**默认**） | 启动调研 |
| `analyze` | 已收集回答的分析模板（40% 阈值 + 高期望用户）| 数据回收后 |
| `signals` | PMF 信号雷达图（留存 / NPS / 病毒 / 付费） | 综合验证 |
| `action` | PMF 后行动剧本（推 vs 优化 vs Pivot）| 调研后决策 |
| `fullset` | 完整四件套（问卷 + 分析 + 雷达 + 行动） | 重要决策 |

---

## 执行流程（survey 模式）

```
Step 1: 调研对象筛选
  → 必须是 Activated User（真正使用过产品并获得价值）
  → 推荐：使用 ≥ 2 次 + 完成核心动作的用户
  → 样本量目标：≥ 30 回答（最低）/ ≥ 100（标准）

Step 2: Sean Ellis 四问设计
  → Q1：核心问题"如果不能再用 [产品]，你会感到？"
  → Q2-Q4：辅助问题（高期望用户识别 + 改进方向）

Step 3: 触达方案
  → 渠道：邮件 / 应用内弹窗 / 微信 / 一对一
  → 时机：用户使用 ≥ 1 周后
  → 激励：低 / 高（看群体）

Step 4: 问卷预演
  → 5 个用户走一遍，确认理解一致
  → 调整问题表述
```

---

## Sean Ellis 四问标准模板

```markdown
# [产品名] 用户调研

我们想了解 [产品名] 对你的真实价值，请用 5 分钟回答 4 个问题：

## Q1（核心）：如果你不能再用 [产品名]，你会感到？
- A. 非常失望 ⭐
- B. 有点失望
- C. 不会失望
- D. 我已经不再用了

## Q2：你认为 [产品名] 最适合什么样的人使用？

[开放回答]

## Q3：[产品名] 对你最大的帮助是什么？

[开放回答]

## Q4：你觉得 [产品名] 还可以怎么改进？

[开放回答]
```

---

## 分析模板（analyze 模式）

```markdown
# PMF 调研分析报告

## 调研基础数据
- 触达用户：[N]
- 完成回答：[M]（回收率 [M/N]%）
- 调研周期：YYYY-MM-DD ~ YYYY-MM-DD
- 用户筛选：使用 ≥ 2 次 + 完成核心动作

## 核心 PMF 评分（Sean Ellis）
| 选项 | 数量 | 占比 |
|------|------|------|
| A. 非常失望 ⭐ | 47 | **42%** |
| B. 有点失望 | 38 | 34% |
| C. 不会失望 | 22 | 20% |
| D. 已不用 | 5 | 4% |

**PMF 信号**：选 A 的占 42%
- ≥ 40% → ✅ 可能达到 PMF
- 25%-40% → ⚠️ 接近 PMF，继续优化
- < 25% → ❌ 远未到 PMF

## High-Expectation Customer（HXC）画像
> 选 A 的用户共同特征：

- 行业：[占比 / 例]
- 角色：[占比 / 例]
- 公司规模：[占比 / 例]
- 使用频次：[平均]
- 使用场景：[Top 3]

→ HXC 是真正爱产品的人，未来定位 / 营销应聚焦此类。

## Q3 价值聚类（用户感知的最大价值）

主题 1：节省时间（28% 选 A 用户提到）
- "本来 2 小时，现在 20 分钟搞定"

主题 2：质量提升（21%）
- "比手工写的好 30%"

主题 3：知识沉淀（15%）
- "团队不再重复造轮子"

→ 真正的价值是 [Top 1]，定位应强调这一点。

## Q4 改进方向（流失风险信号）

主题 1：[改进点]（选 B/C 用户高频）
主题 2：[改进点]
主题 3：[改进点]

→ 优先修复 Top 2 改进点，可将 B/C 用户转化为 A。

## 决策建议
✅ 已达 PMF（42%），建议：
1. 聚焦 HXC 推广
2. 优化 Q4 Top 2 改进点
3. 启动增长引擎搭建
```

---

## PMF 信号雷达图（signals 模式）

```markdown
# PMF 综合信号雷达图

## 五维信号

```
                    Sean Ellis PMF 测试
                          (42%)
                            ●
                           ╱│╲
                          ╱ │ ╲
                         ╱  │  ╲
              留存曲线   ●───┼───●  净推荐 NPS
              (D30 35%)      │       (+45)
                         ╲   │   ╱
                          ╲  │  ╱
                           ╲ │ ╱
                            ●●
                       自然流量增长
                       (月 +15%)
```

| 维度 | 数值 | 健康线 | 状态 |
|------|------|-------|------|
| Sean Ellis | 42% | ≥ 40% | ✅ |
| 留存 D30 | 35% | ≥ 30% | ✅ |
| NPS | +45 | ≥ +40 | ✅ |
| 自然流量月增 | +15% | ≥ +10% | ✅ |
| 病毒 K | 0.4 | ≥ 0.5 | ⚠️ |

## 综合判定
**Pre-PMF / 接近 PMF / 已 PMF / Strong PMF**

→ 已 PMF（4/5 维度健康）
→ 弱项：病毒系数，建议增强分享/邀请机制
```

---

## PMF 后行动剧本（action 模式）

```markdown
# PMF 后行动建议

## 当前状态
- ✅ 已 PMF（Sean Ellis 42%）
- ✅ 留存 / NPS 均健康
- ⚠️ 病毒系数偏低

## 三选一决策

### 选项 A：放大推广（Scale）
**何时选**：PMF 强（45%+），团队有营销/销售能力

行动：
1. 加大获客投入（CAC 上限计算）
2. 招聘销售/客户成功
3. 启动增长实验队列
4. 完善 Onboarding 漏斗

### 选项 B：深化优化（Optimize）⭐
**何时选**：PMF 接近线（40-50%），有明确改进项

行动：
1. 优先解决 Q4 Top 2 改进点
2. 提升弱信号维度（如病毒）
3. 3 个月后再做 PMF 测试
4. 留存深度优化

### 选项 C：聚焦细分（Niche）
**何时选**：PMF 在某个细分市场强，整体弱

行动：
1. 聚焦 HXC 画像，调整定位
2. 重写官网首屏（针对 HXC）
3. 调整 GTM 策略（针对细分）

## 推荐：选项 B
基于：
- PMF 42% 接近健康线但非高分
- 病毒系数偏弱有改进空间
- 团队规模未到放大期

下一步：
1. /ab-test（针对 referral 漏斗设计实验）
2. /pricing-strategy --mode psm（验证定价合理）
3. 3 个月后再测 PMF
```

---

## 与其他命令的协同

```
/pmf-survey（本命令）
  ├── /user-research → 早期访谈识别 PMF 假设
  ├── /mvp-canvas → MVP 验证完才有 PMF 测试意义
  ├── /product-strategy --mode lean → 调整 UVP / Solution
  └── /pricing-strategy → PMF 后才能稳定定价

推荐工作流：
  早期产品验证：
    /mvp-canvas → 上线 MVP
    → 8 周后 /pmf-survey
    → ✅ PMF → /ab-test + /pricing-strategy
    → ⚠️ 接近 → /pmf-survey --mode action（优化）
    → ❌ 远未 → 启动 Pivot 决策
```

---

## 使用示例

```bash
# Sean Ellis 问卷设计（默认）
/pmf-survey AI 写作助手

# 已收集回答的分析
/pmf-survey AI 写作助手 --mode analyze

# 综合 PMF 信号雷达
/pmf-survey AI 写作助手 --mode signals

# PMF 后行动决策
/pmf-survey AI 写作助手 --mode action

# 完整套件
/pmf-survey AI 写作助手 --mode fullset

# 指定触达渠道
/pmf-survey 团队协作工具 --users-source email
```
