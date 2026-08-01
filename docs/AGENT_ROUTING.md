# Agent 路由与边界规则

> 24 个 agent 中有若干组职责相近、容易误选。本文件列出**必须显式区分**的边界。
> 索引见 [`agents/README.md`](agents/README.md)。

---

## 1. `@product-manager` vs `@gtm-strategist`

| 判据 | product-manager | gtm-strategist |
|---|---|---|
| **主体** | 产品内部逻辑（做什么 / 怎么做） | 产品外部路径（卖给谁 / 怎么卖） |
| **交付物** | PRD / 路线图 / 用研 / 竞品 / 反馈 | ICP / 定位 / 渠道 / 定价 / 90 天计划 |
| **时机** | 立项 → 迭代 | 上市 → 增长 |
| **典型输入** | 用户 pain point、场景、需求 | 目标市场、竞品格局、增长模型（PLG/SLG/CLG） |

**冲突规则**：定价决策同时属两个 agent。默认走 `growth-strategist`；若定价依赖商业模式重塑，才升到 `gtm-strategist`。

---

## 2. `@research-analyst` vs `@web-search-analyst`

| 判据 | research-analyst | web-search-analyst |
|---|---|---|
| **抽象层** | 方法论层（用研 / VoC / PMF / 竞品矩阵） | 执行层（多引擎并行搜索 + 三角验证） |
| **输入** | 研究问题、假设 | 关键词、话题、URL 列表 |
| **输出** | 研究报告（有洞察、有决策） | 事实清单（含来源） |
| **依赖** | 会调用 `@web-search-analyst` 拿数据 | 独立执行，或被上游 agent 调用 |

**冲突规则**：用户问「市场怎么样」→ research-analyst；用户问「XX 出了什么新版本」→ web-search-analyst。

---

## 3. `@product-manager` vs `@growth-strategist`

| 判据 | product-manager | growth-strategist |
|---|---|---|
| **阶段** | 产品全生命周期 | 上线后的增长阶段 |
| **实验类型** | 功能实验（这个功能要不要做） | 增长实验（激活/留存/转化/定价） |
| **指标框架** | 用户 pain → 需求 → 验收 | AARRR / 北极星 / cohort |

**冲突规则**：AB 测试同时属两个。默认走 `product-manager`（他会调 `ab-test` skill）；若实验目标是漏斗指标，升到 `growth-strategist`。

---

## 4. `@content-director` vs `@style-evolver`

| 判据 | content-director | style-evolver |
|---|---|---|
| **场景** | 常规文章（有主题、走标准流程） | 有明确参考风格的文章 |
| **风格来源** | 内置四层自检 | 用户提供的参考文（学、卡、创） |
| **迭代方式** | 一次成稿 + QA | Writer-Reviewer 互搏迭代直到达标 |

**冲突规则**：用户说「帮我写一篇关于 X 的文章」→ content-director；用户说「模仿这篇/这个人的风格写 X」→ style-evolver。

---

## 5. `@article-illustrator` vs `@diagram-architect` vs `@ppt-generator`

| 判据 | article-illustrator | diagram-architect | ppt-generator |
|---|---|---|---|
| **载体** | .md 文章内嵌配图 | 独立图表文件（PNG / SVG / VSDX） | PPT 里的图表 |
| **触发** | 文章配图批量补齐 | 用户明确要一张架构图/流程图 | 做 PPT 时自动内嵌 |
| **引擎** | HTML+Playwright + Mermaid + SD | Mermaid / PlantUML / Markmap / diagrams / Visio | 6 种 PPT 引擎 + ppt-architect（内部调度） |

**冲突规则**：这三个不重叠，用错代价高（导出格式和上下文都不同）。

---

## 6. `@solution-architect` vs `@proposal-writer` vs `@bid-writer`

| 判据 | solution-architect | proposal-writer | bid-writer |
|---|---|---|---|
| **触发** | 客户 / 项目名 | 具体方案 / 可研 / 初步设计 | 招标文件 PDF |
| **流程** | discovery → gap → SA → BC → RFP → demo → PoC | 多轮问答 → 章节写作 | 七阶段（analyze → clarify → outline → write → review → check → export） |
| **输出** | 全链路交付物 | 单份方案文档 | 一整套投标文件 |

**冲突规则**：
- 客户还在早期接触 → solution-architect（总指挥）
- 客户要一份方案文档 → proposal-writer
- 拿到正式招标文件 → bid-writer（标书专职）

`solution-architect` 会内部调用 `proposal-writer` / `bid-writer`；用户可直接调后两者跳过总指挥。

---

## 7. `@prd-coach` vs `@product-manager` vs `@ai-product-architect` vs `@xqy-spec-writer`

| Agent | 场景 |
|---|---|
| `prd-coach` | 想法模糊、非 PM 用户、需要对话引导 |
| `product-manager` | 已有清晰想法、按标准 PRD 流程 |
| `ai-product-architect` | AI 功能（LLM / Agent / RAG） — Prompt / Eval / 失败模式必须独立管理 |
| `xqy-spec-writer` | 银行 / 金融 / 政府类甲乙方交付 — 强制 8 章模板 + 5 张表格 |

**冲突规则**：AI 功能 + 甲乙方场景 → 先 `ai-product-architect` 出 PRD → 再 `xqy-spec-writer` 转成需规格式（两阶段）。

---

## 8. 决策速查表

问自己：**「用户此刻站在哪个岗位？」**

| 用户身份 | 首选 agent |
|---|---|
| 产品经理 / 产品新想法 | product-manager / prd-coach（想法模糊） |
| 售前 SE / SA | solution-architect |
| 标书专员 | bid-writer |
| 客户成功 / 培训 | product-enablement |
| 产品总监 / 跨部门项目 | product-director |
| 增长 / 数据 / 实验 | growth-strategist / product-manager |
| 上市 / GTM | gtm-strategist |
| 内容 / 公众号 / 长文 | content-director / style-evolver |
| 研究 / 情报 | research-analyst / web-search-analyst / paper-researcher |
| 设计 / 前端 UI | impeccable-designer |
| PPT / 视频 / 图表 | ppt-generator / video-maker / diagram-architect |
| 文档润色 | doc-polisher |
| 数据查询 | data-analyst |

---

## 9. 变更历史

- **v2.8（2026-07）**：新增本文件（配套 `agents/README.md` 索引）。
