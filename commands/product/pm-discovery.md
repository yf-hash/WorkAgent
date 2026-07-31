---
description: PM 全流程发现阶段编排 — 一次性输出市场 + 用户 + 竞品 + 场景 + 机会 + MVP + 风险
argument-hint: "[产品方向/客户线索/业务想法]"
---

# /pm-discovery — 产品发现阶段一次性产出

请基于以下输入，完成产品发现阶段的综合分析：

$ARGUMENTS

> 综合使用 `market-research` / `user-research` / `product-strategy` 知识库
> （竞品深度专项走 `/market-research --mode competitive`），
> 一次性输出立项前需要的关键判断。深度专项请用 `@research-analyst`（含 Market Intelligence Focus Mode）。

## 输出内容

1. **市场背景**（行业、规模、政策、趋势）
2. **目标客户**（行业 × 角色 × 决策链 × 预算来源）
3. **用户角色**（核心 / 影响 / 决策角色）
4. **核心场景**（3-5 个高价值场景）
5. **关键痛点**（频率 × 强度 × 付费意愿评分）
6. **竞品/替代方案**（客户现在用什么、为什么不够）
7. **产品机会点**（差异化 + 时机判断）
8. **MVP 建议**（先做什么、为什么）
9. **风险与待验证假设**（前置 30/60 天要验证什么）

## 输出格式

```markdown
# 产品发现报告：{{方向}}

## 1. 结论先行
（值不值得做、做什么样的、什么节奏）

## 2. 市场与机会
## 3. 目标客户与角色
## 4. 核心场景与痛点
## 5. 竞品与替代方案
## 6. 产品机会判断
## 7. MVP 建议
## 8. 风险与待验证假设
## 9. 推荐下一步

| 动作 | 负责人 | 输出 | Deadline |
|------|--------|------|----------|
```

## 推荐后续

- 立项通过 → `/product-strategy` → `/prd --mode standard`（C 端）或 `/pm-prd-enterprise`（B 端 SaaS）
- 需要更深市场情报 → `@research-analyst §Market Intelligence Focus Mode`
- 需要客户访谈设计 → `/user-research`
- 综合多领域研究 → `@research-analyst`
