---
name: pm-prioritization-frameworks
description: >
  产品经理优先级排序框架知识库。覆盖 RICE、MoSCoW、ICE、Kano 四种主流排序框架，含公式、适用场景、使用示例。
  用于需求池排序、MVP 范围界定、版本规划取舍。
  触发词：RICE、MoSCoW、ICE、Kano、需求优先级、需求排序、MVP 范围、功能取舍
user-invocable: false
effort: low
---

# PM Prioritization Frameworks — 优先级排序框架

> 单一职责：4 种优先级排序框架的公式与适用场景。
> 不做：需求发现（→ `pm-discovery-frameworks`）、路线图（→ `product-roadmap`）

## 框架速查

| 框架 | 公式/说明 | 适用场景 |
|------|---------|---------|
| RICE | (Reach × Impact × Confidence) ÷ Effort | 多需求横向比较 |
| MoSCoW | Must / Should / Could / Won't | MVP 范围界定 |
| ICE | Impact × Confidence × Ease | 快速优先级 |
| Kano | 必备 / 期望 / 惊喜 / 反向 / 无差异 | 功能价值分类 |

## RICE 详解

```
RICE Score = (Reach × Impact × Confidence) ÷ Effort

- Reach（覆盖）：N 名用户/月
- Impact（影响）：3=巨大 / 2=高 / 1=中 / 0.5=低 / 0.25=极小
- Confidence（置信度）：100% / 80% / 50%（< 50% 应先做 PoC）
- Effort（工作量）：人月

示例：
| 需求 | Reach | Impact | Confidence | Effort | RICE |
|------|-------|--------|-----------|--------|------|
| 评论功能 | 5000 | 2 | 80% | 4 | 2000 |
| Onboarding 改版 | 8000 | 1 | 100% | 2 | 4000 ← 优先做 |
```

## MoSCoW 详解

```
Must Have（必备）：缺了产品就垮，零容忍
Should Have（重要）：缺了体验受损但能用
Could Have（锦上添花）：有时间就做
Won't Have（不做）：明确排除，写入 PRD §5.2

使用要点：
- Must 占比 < 60%，否则就是没做取舍
- 每个 Won't 都要说清"为什么本期不做"
- MoSCoW 是阶段共识，不是永久禁令
```

## ICE 详解

```
ICE Score = Impact × Confidence × Ease（每项 1-10 分）

适合：快速会议、灵感排序、增长实验
缺点：精度不如 RICE，不适合大投入决策
```

## Kano 详解

```
五类功能：
- 必备型（Must-be）：缺了不满意，有了也不会特别满意
  例：登录、支付安全
- 期望型（One-dimensional）：越多越好，与满意度线性相关
  例：响应速度、价格优惠
- 兴奋型（Attractive）：超预期，惊喜
  例：意外彩蛋、AI 智能补全
- 反向型（Reverse）：有了反而不满意
  例：过度推荐、强制升级
- 无差异型（Indifferent）：用户不关心
  例：无人用的高级设置

使用要点：
- 通过 Kano 问卷量化（功能存在/不存在 两个问题）
- 必备型不做就完，期望型决定竞争力，兴奋型创造惊喜
- 兴奋型会随时间退化为必备型（智能手机摄像头）
```

## 框架组合使用

```
场景 → 框架选择：
- 需求池有 50+ 个候选 → RICE（量化排序）
- MVP 范围讨论会 → MoSCoW（快速达成共识）
- 增长实验排序 → ICE（轻量快速）
- 大版本功能价值评估 → Kano（区分类型）
```
