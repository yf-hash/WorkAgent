# Agents 索引（24 个）

> 按职责分层组织，用户按场景选择入口。详细能力见每个 agent 文件的 frontmatter 和正文；agent 之间的边界与协作规则见 [`../AGENT_ROUTING.md`](../AGENT_ROUTING.md)。

---

## 战略层（策略 / 决策 / 编排）

高抽象度、跨团队、含决策与取舍。

| Agent | 一句话 | 何时调 |
|---|---|---|
| `product-director` | 产品总监 — 复杂跨部门任务的策略层（拆任务/分工/取舍/把关） | 立项、大功能、CEO 项目 |
| `solution-architect` | 售前解决方案总指挥 — 客户拜访 → PoC → 合同全链路 | 售前 SE/SA 场景 |
| `gtm-strategist` | GTM 全链路战略（增长模型/ICP/定位/渠道/定价/90 天） | 新品上市 / GTM 诊断 |
| `growth-strategist` | 增长战略（PMF / 漏斗 / 实验 / 定价） | PMF 验证、增长瓶颈 |

---

## 领域专家（独立方法论）

单一方法论、深度专业、可独立完成任务。

### 产品与需求
| Agent | 一句话 |
|---|---|
| `prd-coach` | PRD 对话教练 — 三镜诊断 + 概念稿→实现稿 |
| `xqy-spec-writer` | 银行/金融 XQY 需规说明书（8 章模板 + 5 强制表格） |
| `qa-acceptance-designer` | PRD → 验收方案（功能/权限/异常/数据/审计/客户口径） |
| `ai-product-architect` | AI 功能 PRD（Prompt / Eval / 失败模式） |

### 研究与情报
| Agent | 一句话 |
|---|---|
| `research-analyst` | 综合研究（用户/市场/反馈/PMF + Market Intelligence Focus Mode） |
| `web-search-analyst` | 多引擎联网研究（Bing / 百度 / CSDN / 掘金等 9 引擎并行） |
| `paper-researcher` | 论文研究（arXiv 搜集 + 单篇解读） |

### 内容与写作
| Agent | 一句话 |
|---|---|
| `content-director` | 全流程内容创作编排（风格 → 框架 → 写作 → QA → 迭代） |
| `style-evolver` | 风格学习 → 风格卡片 → Writer-Reviewer 迭代 |
| `doc-polisher` | 文档润色（AI 去痕 + 智能配图闭环） |

### 视觉与设计
| Agent | 一句话 |
|---|---|
| `impeccable-designer` | 反 AI Slop 的前端设计语言总指挥（13 子命令） |
| `diagram-architect` | 统一图表编排（Mermaid/PlantUML/Markmap/diagrams/Visio 路由） |
| `article-illustrator` | 文章内联配图（HTML 图表 + Mermaid + SD 三合一） |

---

## 全栈执行（编排大量命令 / 生产流水线）

编排 5+ 命令、长流程、生产级交付。

| Agent | 一句话 | 生产流水线 |
|---|---|---|
| `product-manager` | 全栈 PM（PRD / 竞品 / 用研 / 分析 / 路线图 / 反馈） | 20+ 命令编排 |
| `product-enablement` | 产品赋能（销售指南 / 文档审计 / 16 类产品资料） | 16 个 product-* |
| `proposal-writer` | 企业方案撰写（售前方案 / 可研 / 初步设计） | 多轮问答 |
| `bid-writer` | 标书七阶段编制（analyze → export） | 7 阶段 |
| `ppt-generator` | PPT 10 阶段（RAG → 架构 → 制作 → 评分 → 迭代） | 6 引擎路由 |
| `video-maker` | 视频生成（Remotion 三引擎 + PDF2video + TTS + 字幕） | 三引擎路由 |
| `data-analyst` | 数据分析（TaskWeaver + Chat2DB 双引擎） | SQL + Python |

---

## 选择速查

**想不清用哪个？**

- 「客户 / 售前 / 投标」 → `solution-architect`（总指挥） / `bid-writer`（标书专职）
- 「产品新想法」 → 想法模糊：`prd-coach`；已清晰：`product-manager` / `product-director`
- 「AI 功能特殊性」 → `ai-product-architect`（PRD） + `growth-strategist`（AB 验证）
- 「写东西」 → 通用文章：`content-director`；有参考风格：`style-evolver`；润色现有：`doc-polisher`
- 「做图」 → 文章内配图：`article-illustrator`；独立图表：`diagram-architect`；UI 设计：`impeccable-designer`
- 「PPT / 视频」 → `ppt-generator` / `video-maker`（都会自动路由到合适引擎）
- 「数据」 → `data-analyst`（SQL + Python）
- 「上市」 → `gtm-strategist`（战略） + `growth-strategist`（执行）

模糊边界（PM vs GTM、Research vs Web-search 等）见 [`../AGENT_ROUTING.md`](../AGENT_ROUTING.md)。

---

## 变更历史

- **v2.8（2026-07）**：删除 `impeccable-manual-edit-applier`（draft，无调用路径）；新增本索引 + `AGENT_ROUTING.md`。25 → 24。
- **v2.7**：合并 `market-intelligence` → `research-analyst`；补录 `web-search-analyst` / `xqy-spec-writer`。
- **v2.6**：删除 `writer-reviewer`（被 `style-writer-reviewer` skill 覆盖）。
