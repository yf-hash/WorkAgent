---
name: pm-discovery-frameworks
description: >
  产品经理发现阶段（Discovery）核心框架知识库。覆盖 JTBD（用户雇佣产品做什么任务）、
  5 Whys（根因追溯）、Opportunity Solution Tree（机会-方案树）、Problem/Solution Fit（问题-方案契合度）。
  适合早期需求探索、根因追溯、机会评估。
  触发词：JTBD、5Whys、Opportunity Solution Tree、Problem Solution Fit、产品发现、用户洞察框架
user-invocable: false
effort: low
---

# PM Discovery Frameworks — 发现阶段框架

> 单一职责：发现阶段（Discovery）的 4 个核心框架。
> 不做：优先级排序（→ `pm-prioritization-frameworks`）、指标框架（→ `pm-metrics-frameworks`）

## 框架速查

| 框架 | 核心问题 | 输出 |
|------|---------|------|
| JTBD | 用户雇佣产品完成什么任务？ | 工作陈述（Job Statement） |
| 5 Whys | 问题的根本原因是什么？ | 根因树 |
| Opportunity Solution Tree | 从目标到解法的探索路径是什么？ | OST 图 |
| Problem / Solution Fit | 问题足够大且可解决吗？ | 假设验证矩阵 |

## JTBD（Jobs-to-be-Done）

```
工作陈述格式：
当 [情境], 我想要 [动机], 这样我就能 [预期结果]。

示例：
当我赶时间出门，我想要快速召唤一辆车，这样我就能准时到达。
（用户雇佣 Uber 完成的"工作"）
```

**使用要点**：
- 关注"工作"而非"功能"
- 区分核心工作 / 相关工作 / 情感工作
- 工作不变，解法在变（汽车之于马车之于互联网叫车）

## 5 Whys 根因追溯

```
现象：新用户 D7 留存只有 15%
Why 1：为什么留存低？→ 用户找不到核心价值
Why 2：为什么找不到？→ 首次使用没有引导
Why 3：为什么没有引导？→ Onboarding 流程缺失
Why 4：为什么缺失？→ MVP 阶段被砍掉
Why 5：为什么被砍？→ 当时认为产品自解释

根因：高估了"自解释"假设，未做 Onboarding
```

## Opportunity Solution Tree（OST）

```
            目标（Outcome）
                  │
        ┌─────────┼─────────┐
        │         │         │
      机会1     机会2     机会3      ← 用户问题/痛点
        │
    ┌───┼───┐
    │   │   │
   解法1 解法2 解法3                ← 待验证的解法
    │
    实验 → 数据验证
```

**使用要点**：
- 目标在顶部（如"新用户激活率提升 30%"）
- 机会通过用户访谈发现，越具体越好
- 每个机会下出 2-3 个解法
- 每个解法对应一个实验

## Problem / Solution Fit

```
假设验证矩阵：
| 假设 | 当前证据 | 验证方法 | 通过标准 |
|------|---------|---------|---------|
| 用户有此痛点 | 5/10 访谈提到 | 扩大访谈到 30 | ≥ 60% 主动提及 |
| 痛点足够痛 | 平均评分 7/10 | 痛点强度问卷 | ≥ 7/10 平均分 |
| 愿意付费 | 3 人口头同意 | LOI / 预付定金 | ≥ 20% 转化 |
| 我们的方案能解 | MVP demo | 5 人试用 | ≥ 4 人复用 |
```

## 串联使用建议

```
JTBD → 找出真实任务
  ↓
5 Whys → 定位根因
  ↓
OST → 梳理机会与解法
  ↓
PSF → 验证 → 进入定义阶段（→ `pm-prioritization-frameworks`）
```
