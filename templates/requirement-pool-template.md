# 需求池模板

> 单需求池标准结构。配套 Skill：`product-roadmap`、`prd-quality-check`、`pm-prioritization-frameworks`。
> 推荐与 Linear / Jira / GitHub Projects / 飞书任务同步使用。

| 需求ID | 需求名称 | 来源 | 客户/角色 | 场景 | 问题描述 | 需求类型 | 优先级 | 状态 | 版本 | 负责人 | 备注 |
|---|---|---|---|---|---|---|---|---|---|---|---|

## 字段说明

- **需求ID**：建议格式 `REQ-{YYYY}-{编号}`
- **来源**：客户访谈 / 销售反馈 / 竞品分析 / 内部规划 / 客户工单 / 用户反馈
- **需求类型**：新功能 / 优化 / 缺陷 / 技术债 / 合规 / 架构
- **优先级**：P0 / P1 / P2 / P3（参考 `roadmap-planning` 评分模型）
- **状态**：待评估 / 已收录 / 待开发 / 开发中 / 已上线 / 已关闭 / 已驳回
- **版本**：目标版本号（与 Roadmap 对齐）

## 配套工作流

```
收集 → /pm-intake（信息澄清）
     → /prd-diagnose（需求拆解）
     → /roadmap（优先级与版本）
     → 同步到 Linear / Jira / GitHub Projects / 飞书
```
