---
name: pm-full-cycle
description: >
  产品经理全流程编排知识库 — 把模糊产品想法一次性转化为完整产品方案：
  市场机会 → 目标客户 → 用户场景 → 痛点 → 竞品 → 定位 → 功能架构 → MVP → Roadmap →
  PRD → 测试验收 → 发布上线 → 销售赋能。
  适合 0→1 立项、客户工单到产品化、内部新方向论证。
  与 product-manager Agent 配合：本 Skill 是知识库与模板，Agent 负责编排子任务。
  触发词：产品全流程、从想法到方案、立项、产品规划、端到端 PM、product full cycle。
user-invocable: true
effort: high
argument-hint: "[产品想法/客户需求/业务方向]"
---

# 产品经理全流程 Skill

## 目标

把一个模糊的产品想法（一句话需求 / 客户工单 / 老板想法）一次性转化为闭环的产品方案，从战略到研发到销售。

## 执行顺序（13 步）

1. **市场机会判断**：谁在花钱、市场多大、为什么现在
2. **目标客户与画像**：行业 × 角色 × 决策链 × 预算来源
3. **核心场景与痛点**：3-5 个高价值场景，痛点强度评分
4. **竞品与替代方案**：客户现在用什么、为什么不够、我们如何赢
5. **产品定位与价值主张**：一句话定位、客户为什么选我
6. **功能架构**：能力分层、可标准化部分、定制化部分
7. **MVP 范围**：必须做 / 暂缓 / 不做
8. **Roadmap**：版本节奏 + 里程碑
9. **PRD 摘要**：核心功能、流程、字段、权限、验收
10. **测试验收**：上线阻断项、客户验收口径
11. **发布上线**：灰度 + 回滚 + 客户通知
12. **销售赋能**：Demo 脚本、FAQ、竞品话术
13. **风险与决策建议**：商业 / 交付 / 技术 / 安全 / 合规

## 输出格式

```markdown
# 产品全流程方案：{{产品/方向}}

## 1. 总体判断
## 2. 市场与客户分析
## 3. 用户角色与场景
## 4. 竞品与替代方案
## 5. 产品定位
## 6. 核心价值
## 7. 功能架构
## 8. MVP 设计
## 9. Roadmap
## 10. PRD 摘要
## 11. 测试验收
## 12. 发布上线
## 13. 销售与售前材料
## 14. 风险与决策建议
```

## 质量要求

- **不是单一文档，是闭环**：从战略到研发到销售要能落到下一步动作
- **每个结论都有可执行项**：不写"应该"，写"由谁、多久、做什么"
- **B 端必含审计/权限/部署**：多租户、私有化、客户验收标准默认必填
- **前后一致**：PRD 中的功能 → Roadmap 的版本 → 验收标准 → 销售材料，链路自洽

## 推荐工具链

| 阶段 | 推荐命令 / Skill / Agent |
|------|--------------------------|
| 1-4 市场用户竞品 | `/market-research` / `/user-research` / `@research-analyst` |
| 5-6 战略定位 | `/product-strategy` / `@product-director` |
| 7-9 PRD/MVP/Roadmap | `/product-spec` / `/mvp-canvas` / `/roadmap` |
| 10 验收 | `/launch-checklist` / `pm-qa-acceptance` |
| 11 发布 | `/launch-checklist` / `@release-manager` |
| 12 销售 | `/sales-guide` / `@product-enablement` |
| 13 决策记录 | `/decision-log` |

## 配套模板

- `templates/brd-template.md`（商业判断）
- `templates/mrd-template.md`（市场判断）
- `templates/prd-template.md`（产品需求）
- `templates/roadmap-template.md`（版本规划）
- `templates/acceptance-checklist-template.md`（验收）
- `templates/release-note-template.md`（发布）
- `templates/sales-enablement-template.md`（销售赋能）
- `templates/requirement-pool-template.md`（需求池）
