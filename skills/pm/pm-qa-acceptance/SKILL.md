---
name: pm-qa-acceptance
description: >
  测试验收设计知识库 — 把 PRD/功能/版本转化为可执行的验收方案。
  覆盖 10 大验收维度：功能、流程、字段、权限、状态流转、异常、性能、安全审计、兼容性、客户验收口径。
  特别强调 B 端企业级产品（多租户、私有化、合规）的验收要点。
  触发词：测试验收、验收用例、UAT、上线阻断项、客户验收、验收方案、测试用例、
  acceptance test、QA design、acceptance criteria、test cases。
user-invocable: true
effort: medium
argument-hint: "[PRD/功能/版本]"
harness:
  execute:
    preset: writing-scoped
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

# 测试验收设计 Skill

## 验收维度（10 维）

1. **功能正确性**：每条业务规则都能复现
2. **流程完整性**：主流程、异常流程、回退流程
3. **字段和数据准确性**：必填、唯一、格式、跨表一致性
4. **权限正确性**：角色矩阵 × 操作矩阵 + 越权检测
5. **状态流转正确性**：状态机图谱无死锁、无非法跃迁
6. **异常提示合理性**：用户能看懂、能恢复、不暴露内部错误
7. **性能和稳定性**：响应时间、吞吐、并发、长时运行
8. **安全和审计**：注入、越权、日志完整、追溯链路
9. **兼容性**：浏览器/系统/数据库/旧版本数据
10. **客户验收口径**：客户语言写、客户视角验、客户场景跑

## 输出格式

```markdown
# 验收方案：{{功能/版本}}

## 1. 验收范围

## 2. 功能测试用例

| 用例ID | 场景 | 前置条件 | 操作步骤 | 预期结果 | 优先级 |
|---|---|---|---|---|---|

## 3. 权限测试

## 4. 异常测试

## 5. 数据校验

## 6. 非功能测试

## 7. 上线前检查清单

## 8. 客户验收标准
```

## 上线阻断项原则（P0 不达标必须延期）

- 主流程 1 条不通 → 阻断
- 任一角色越权可触达不该看的数据 → 阻断
- 任一审计日志缺失 → 阻断
- 任一非功能指标低于合同/SLA 承诺 → 阻断
- 客户验收必备场景无法演示 → 阻断

## 配套模板

参考 `templates/acceptance-checklist-template.md`。

## 关联资源

- 上游：`prd-standard` / `prd-implementation-draft`（PRD 来源）
- 下游：`launch-checklist`（Launch Readiness）、`/pm-review`（PRD 评审）
- Agent：`@qa-acceptance-designer`（编排，Go/No-Go 阻断项）
