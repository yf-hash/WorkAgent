---
name: pm-core-framework
description: >
  产品经理通用工作框架知识库 — 任何产品任务的"前置思考层"。
  在动手做 PRD/Roadmap/竞品/用研之前，先用本框架判断：任务阶段、目标受众、输出深度。
  触发词：PM 工作框架、产品思考框架、PM 通用方法、产品分析框架、
  PM 阶段判断、产品输出结构、PM common framework。
user-invocable: true
effort: low
argument-hint: "[产品/需求/问题描述]"
---

# 产品经理通用工作框架 Skill

> 本 Skill 是「前置思考层」。具体方法论见同目录其他 PM 框架 Skill：
> - 发现阶段：`pm-discovery-frameworks`
> - 优先级：`pm-prioritization-frameworks`
> - 增长漏斗：`pm-growth-aarrr`
> - 北极星：`pm-north-star`
> - 向上管理：`pm-upward-management`
> - AI 时代演进：`pm-ai-era-evolution`

## 三步前置判断

### 1. 判断产品阶段

| 阶段 | 关键问题 | 推荐工具 |
|------|---------|---------|
| 机会发现 | 行业、市场、客户、竞品、政策、技术趋势 | `/market-research`, `@market-intelligence` |
| 需求澄清 | 用户、场景、问题、约束、价值 | `/user-research`, `/prd-diagnose` → `/prd-concept` |
| 方案设计 | 功能、流程、页面、字段、权限、状态、异常 | `/prd-standard`, `/prd-spec-first`, `/design-proto` |
| 研发落地 | PRD、验收标准、排期、风险、依赖 | `/prd-quality`, `pm-qa-acceptance` |
| 发布运营 | Release Note、用户手册、培训材料、数据分析 | `/launch-checklist`, `/analytics` |
| 商业化支持 | 售前方案、销售话术、Demo、报价、客户案例 | `/sales-guide`, `@product-enablement` |

### 2. 判断目标受众

| 受众 | 关注点 | 输出风格 |
|------|--------|---------|
| 管理层 | 战略价值、投入产出、风险、里程碑 | 结论先行 + 数据支撑 |
| 客户领导 | 业务价值、合规、成本、效果、交付保障 | 场景化 + 价值量化 |
| 客户技术 | 架构、部署、权限、稳定性、安全性 | 架构图 + 接口契约 |
| 研发团队 | 流程、字段、接口、规则、状态、异常、验收 | 表格化 + 可测试 |
| 销售/售前 | 痛点、价值、场景、差异化、异议处理 | 一句话 + Demo 路径 |

### 3. 标准输出结构

默认 10 段式：

1. 背景判断
2. 目标用户
3. 核心问题
4. 产品目标
5. 解决方案
6. 功能模块
7. 业务流程
8. 权限与数据
9. 验收标准
10. 风险与后续迭代

## 质量自检清单

- [ ] 是否说明了「谁」在「什么场景」遇到「什么问题」
- [ ] 是否说明了为什么现在要做（Why now）
- [ ] 是否区分客户价值和公司价值
- [ ] 是否能转化为研发任务（不是"应该"，而是"做什么"）
- [ ] 是否考虑权限、审计、数据隔离、异常流程
- [ ] 是否能形成可复用产品能力，而不是一次性项目定制

## 与同目录其他 Skill 的边界

- **本 Skill**：判断「这是什么任务、要给谁看、按什么结构写」
- **pm-discovery-frameworks**：JTBD / Kano / 用户旅程 / 五个为什么等发现框架
- **pm-prioritization-frameworks**：RICE / MoSCoW / ICE / Kano / WSJF 优先级框架
- **pm-growth-aarrr**：海盗指标 AARRR / RARRA 增长漏斗
- **pm-north-star**：北极星指标体系
- **pm-upward-management**：向上管理 / 跨部门协作 / 资源争取
- **pm-ai-era-evolution**：AI 时代 PM 能力演化

配合使用：先用本 Skill 定位 → 再用具体方法框架。
