# WorkAgent

> 以 Claude Code 为入口，通过自然语言 command 调用适配的 Agent 和 Skill，完成前场需求的工作智能体，满足产品经理、售前工程师、市场营销等不同用户的场景需求。

WorkAgent 是面向产品经理、售前工程师、市场营销等用户的工作智能体，核心理念是：**通过 WorkAgent，让工作效率指数级提升**。

---

## 项目概述

WorkAgent 是一套以 **风格驱动 + 单一职责** 为核心设计理念的 AI 原生工作平台。它不是通用代码工具，而是专为前场业务人员打造的智能工作系统：

- **内容创作**：公众号长文、访谈稿、深度研究报告、文档润色
- **营销推广**：公众号软文 / 小红书 / 知乎 / 朋友圈 / 短视频 / 落地页 / EDM / PR 稿 / 客户故事 9 大文体
- **产品管理**：PRD 全光谱（lite / standard / spec-first / proto / enterprise + 评分 / 评估 / 增量更新）、竞品分析、用户研究、数据分析、路线图规划
- **售前 / 解决方案**：客户拜访 / 需求挖掘 / Gap Analysis / SA Blueprint / Business Case / RFP 应答 / 安全问卷 / 竞品作战卡 / Demo 设计 / PoC 全链路
- **标书编制**：七阶段原子命令（analyze / clarify / outline / write / review / check / export），三色标记 + RAG 增强写作
- **产品资料**：16 类原子产品文档（白皮书 / 技术白皮书 / 宣传册 / 商务介绍 / 技术介绍 / 功能清单 / 销售FAQ / 竞品分析 / 投标参数 / 解决方案 / 案例 / 用户手册 / 部署 / 兼容性 / 发布说明 / 培训）
- **数据看板**：7 类原子看板（北极星 / AARRR / Cohort / Revenue / Customer BR / AI Monitor / 平台选型）
- **演示制作**：6 种 PPT 引擎自动路由，学术/商务/开发者场景全覆盖
- **数据分析**：自然语言转 SQL + Python 沙箱执行，联合数据库与文件分析
- **视频生成**：Remotion 三引擎拆分（native / prompt2video / vidosy），字幕 / TTS / MP4 渲染全流程
- **视频处理**：PDF/PPT 转动态视频、AI 智能剪辑、字幕生成、多平台分发
- **图表架构**：云架构图（AWS/GCP/Azure/K8s）、Visio、Mermaid、PlantUML、Markmap 五引擎独立

**支持编辑器**：Claude Code（完整支持）> Cursor > OpenAI Codex

---

## 核心内容

| 模块 | 数量 | 说明 |
|------|------|------|
| Agents | 25 个 | 自治代理，编排原子命令完成完整业务流程 |
| Skills | 127 个 | 可复用知识库，**严格单一职责**（v2.7 二次裁剪后） |
| Commands | 114 个 | 统一命令入口，**原子命令**为主，不再用 `--mode` 路由 |
| Templates | 13 个 | PRD/BRD/MRD/Roadmap/PM-Discovery/验收/Release/Sales/需求池/PR-FAQ/6-pager/Model Card/Eval Rubric |

**设计原则**：

- **单一职责**：每个 Skill 只完成一个任务，避免上下文膨胀和决策矛盾（v2.6 重构核心）
- **风格驱动**：所有写作输出以用户/角色风格为第一优先级，避免 AI 套话
- **人机协同**：关键节点设置人工确认，标书/内容创作均有阶段性检查点
- **多引擎路由**：PPT、配图、数据分析等场景支持多种后端引擎自动选择
- **质量四层自检**：活人感 → 情感 → 信息 → 结构，逐层验证输出质量

---

## 项目结构

```
WorkAgent/
├── agents/             # 25 个自治代理（编排原子命令完成完整业务流程）
├── skills/             # 127 个原子 Skill（v2.7 二次裁剪后，严格单一职责）
├── commands/           # 114 个原子命令入口
│   ├── writing/        # 11 个（含 style-* / humanize-* 拆分系列）
│   ├── product/        # 47 个（PM 全流程 + 战略决策 + dashboard-* + prd-* 拆分系列）
│   ├── presales/       # 35 个（售前 / 方案 / RFP / Demo / 竞品 / PoC + bid-* 七阶段 + product-* 16 类）
│   ├── research/       # 5 个（含 /web-search）
│   └── media/          # 16 个（PPT / 配图 / 视频 / 字幕 / 图表 + remotion-* / diagram-* / table-* / md-* 拆分）
├── templates/          # 13 个标准模板
├── AUDIT.md            # 后续裁剪与结构优化 checklist
├── HEALTH_REPORT.md    # 仓库整体健康度 + 修复记录
└── README.md
```

---

## 智能体系统

25 个自治 Agent，覆盖产品、内容、标书、数据、研究、媒体、GTM、方案、视觉、**售前 / 解决方案**全域：

| Agent | 职责 | 调用时机 |
|-------|------|---------|
| `product-manager` | 全栈产品经理（PRD/竞品/用研/分析/路线图/反馈全流程） | 产品决策、需求文档、产品策略 |
| `solution-architect` | **售前解决方案总指挥** — 统筹客户拜访 / Gap / 方案 / Business Case / RFP / Demo / 竞品 / PoC / 售前物料全链路 | 售前 SE / SA 工作场景，赢单导向 |
| `product-director` | 产品总监 — 复杂跨部门产品任务的策略层（拆任务/分工/取舍/把关） | 复杂立项、跨团队大功能、CEO 项目、客户战略级方案 |
| `prd-coach` | PRD 对话教练 — 三镜诊断 + 两阶段交付（概念稿→实现稿），对话式引导非 PM 用户写出可开发的需求文档 | 想法模糊/非 PM/需要引导式写需求文档时 |
| `qa-acceptance-designer` | 测试验收设计 — PRD → 验收方案（功能/权限/异常/数据/审计/客户口径），输出上线阻断项 | PRD/版本验收、UAT 设计、上线 Go/No-Go 阻断项确认 |
| `ai-product-architect` | AI 产品架构师 — 专注 LLM/Agent/RAG 类功能的规格、Prompt、Eval、失败模式管理 | AI 功能 PRD、Prompt 工程交付、AI 功能上线评审 |
| `growth-strategist` | 增长战略 — 统筹 PMF / 漏斗诊断 / A/B 实验 / 定价 | PMF 验证、增长瓶颈诊断、实验设计、定价优化 |
| `research-analyst` | 综合研究分析师 — 用户研究 + 市场情报 + 反馈分析 + PMF 验证 | 早期 0→1 探索、立项验证、PMF 测量 |
| `gtm-strategist` | GTM 全链路战略（增长模型/ICP/定位/渠道/定价/90天计划） | 新产品上市规划、GTM 诊断与优化 |
| `proposal-writer` | 企业方案撰写全链路（售前方案/可研报告/初步设计，多行业定制） | 售前解决方案、项目建议书 |
| `product-enablement` | 产品赋能（销售指南/文档审计/16 类产品资料编排） | 产品赋能、销售支持 |
| `market-intelligence` | 市场情报分析（竞品监测/TAM/趋势/选品/OSS 生态） | 深度竞品分析、市场研究、选品研究 |
| `bid-writer` | 标书七阶段编制（接收 /bid-* 系列子命令） | 标书/投标/招标文件编制 |
| `content-director` | 全流程内容创作编排（风格分析→框架→写作→QA→迭代） | 需要完整写作流程 |
| `style-evolver` | 风格学习 → 风格卡片确认 → Writer-Reviewer 迭代创作 | 风格迁移、参考文章仿写 |
| `doc-polisher` | 文档智能润色（AI 去痕 + 智能配图全自动闭环） | 文档润色、去 AI 味 + 配图一体化 |
| `paper-researcher` | 论文研究（arXiv 搜集 + 单篇深度解读） | 论文情报跟踪、学术科普写作 |
| `video-maker` | Remotion 视频生成路由（native / prompt2video / vidosy / pdf2video） | 企业介绍视频、产品演示视频 |
| `ppt-generator` | PPT 生成协调，5 种引擎路由（academic/slidetailor/ppt-master/slidev/marp；SDK 内嵌 ppt-master） | PPT 生成任务 |
| `data-analyst` | 综合 TaskWeaver + Chat2DB 的数据分析 Agent | 数据查询、分析、报表生成 |
| `article-illustrator` | 文章内联配图 — HTML 图表 + Mermaid + Stable Diffusion 三合一，专为 .md 文章自动批量配图 | 文章/博客自动配图 |
| `diagram-architect` | 统一图表编排，自动路由至 Mermaid/PlantUML/Markmap/diagrams/Visio 最优引擎 | 图表类型不确定、需要多图表套件、格式互转时 |
| `impeccable-designer` | **反 AI Slop 的前端设计语言总指挥** — 集成 [Paul Bakaus 的 impeccable.style](https://impeccable.style/)，7 领域 vocabulary + 32 上游 flow 参考 + 27 条反模式 + 12 条 critique，让 AI 写的 UI 不再像 AI | landing page / dashboard / 组件设计、AI 味 UI 修复、上线前设计审查 |
| `web-search-analyst` | 多引擎联网研究分析师（Bing / 百度 / CSDN / DuckDuckGo / Brave / 掘金等 9 大引擎并行 + 跨源三角验证） | 热点解读、技术调研、竞品快照、错误排查 |
| `xqy-spec-writer` | 银行/金融 XQY 需求规格说明书（8 章模板 + 5 张强制表格） | 银行/保险/证券/国企/运营商/政府类甲乙方交付场景 |

---

## Skill 系统（v2.7 二次裁剪后）

127 个原子 Skill。下方按域列出，每个 Skill **单一职责**、**有边界声明**。

### 写作与内容（10）

| Skill | 描述 | 触发方式 |
|-------|------|---------|
| `article-writer` | 文章风格公众号长文写作（4000-8000 字） | `/article-writer` |
| `hv-analysis` | 横纵分析法深度研究（10000-30000 字 PDF 报告） | `/hv-analysis` |
| `interview-writer` | 访谈写作 v2.0，Writer-Reviewer 互搏 + 知识库进化 | `/interview-writer` |
| `style-card-extractor` | 从参考文章提炼风格卡片 | `/style-extract` |
| `style-writer-reviewer` | 基于风格卡片 + Writer-Reviewer 互搏创作 | `/style-create` |
| `style-refine` | 已有文章按风格卡片优化 | `/style-refine` |
| `humanizer-scan` | AI 痕迹扫描（29 模式 / 五维评分） | `/humanize-scan` |
| `humanizer-soul` | 灵魂注入（6 大人性原则） | `/humanize-soul` |
| `humanizer-academic` | 学术深度强化（30 条指令） | `/humanize-academic` |
| `marketing-copy` | 9 大营销文体（公众号软文 / 小红书 / 知乎 / 朋友圈 / 短视频 / 落地页 / EDM / PR 稿 / 客户故事 / Demo 脚本） | `/marketing-copy` |

### 标书编制（7 阶段拆分，7 Skill）

| Skill | 阶段 | 触发命令 |
|-------|------|---------|
| `bid-analyze` | 1. 拆解 + 三色标记 | `/bid-analyze` |
| `bid-clarify` | 2. 澄清问题清单 | `/bid-clarify` |
| `bid-outline` | 3. 大纲 + 偏离表 | `/bid-outline` |
| `bid-write` | 4. 分模块撰写 | `/bid-write` |
| `bid-review` | 5. 双轮评审 | `/bid-review` |
| `bid-check` | 6. 合规核查 | `/bid-check` |
| `bid-export` | 7. 移交导出 | `/bid-export` |

### PRD 全光谱（10 Skill）

| Skill | 用途 | 触发命令 |
|-------|------|---------|
| `prd-lite` | 1 页对齐方向 | `/prd-lite` |
| `prd-standard` | 标准 8 章 PRD | `/prd-standard` |
| `prd-spec-first` | Spec-First 四件套 | `/prd-spec-first` |
| `prd-proto` | 含 ASCII 线框图 | `/prd-proto` |
| `prd-quality-check` | 5 维度评分 | `/prd-quality` |
| `prd-deep-evaluate` | 23 节模板差距分析 | `/prd-deep-evaluate` |
| `prd-diagnose` | 三镜诊断（想法模糊） | `/prd-diagnose` |
| `prd-concept-draft` | 概念稿 | `/prd-concept` |
| `prd-implementation-draft` | 实现稿 | `/prd-impl` |
| `prd-incremental-update` | 已有 PRD 增量更新 | `/prd-update` |

> B 端严格 12 章另走 `/pm-prd-enterprise`。

### 产品资料（16 类原子 Skill）

`product-whitepaper-writer` / `product-tech-whitepaper-writer` / `product-brochure-writer` / `product-intro-business-writer` / `product-intro-tech-writer` / `product-function-list-writer` / `product-sales-faq-writer` / `product-competitive-writer` / `product-bid-params-writer` / `product-solution-writer` / `product-case-writer` / `product-manual-writer` / `product-deploy-writer` / `product-compat-writer` / `product-release-note-writer` / `product-training-writer`

> 每个 Skill 对应 `/product-*` 命令，覆盖单一文档类型。详细分工见 `commands/presales/` 各文件 frontmatter。

### 数据看板（7 类原子 Skill）

| Skill | 看板类型 | 触发命令 |
|-------|---------|---------|
| `dashboard-northstar` | 北极星 | `/dashboard-northstar` |
| `dashboard-aarrr` | AARRR 漏斗 | `/dashboard-aarrr` |
| `dashboard-cohort` | Cohort 留存 | `/dashboard-cohort` |
| `dashboard-revenue` | 收入（MRR/ARR/NRR） | `/dashboard-revenue` |
| `dashboard-customer-br` | 客户 BR / QBR | `/dashboard-customer-br` |
| `dashboard-ai-monitor` | AI 功能监控 | `/dashboard-ai-monitor` |
| `dashboard-platform-selector` | 平台选型决策 | `/dashboard-platform-selector` |

### 产品管理（核心方法论 + 框架）

- 战略决策：`product-strategy` / `working-backwards` / `build-vs-buy` / `sunset-plan` / `win-loss-analysis` / `churn-analysis`
- 流程方法：`mvp-canvas` / `user-story-mapping` / `ab-test` / `launch-checklist` / `pmf-survey`
- 数据：`product-analytics` / `user-research` / `market-research` / `user-feedback` / `product-roadmap`
- 设计与运营：`design-proto` / `pricing-strategy` / `product-report` / `compliance-checklist` / `tech-debt`
- AI 产品：`ai-red-team` / `pm-ai-security-product`
- PM 框架：`pm-discovery-frameworks` / `pm-prioritization-frameworks` / `pm-growth-aarrr` / `pm-north-star` / `pm-upward-management` / `pm-ai-era-evolution` / `pm-qa-acceptance`

### PPT 与可视化

| Skill | 描述 | 触发方式 |
|-------|------|---------|
| `ppt-master` | 通用 PPT 生成 | `/ppt` |
| `academic-pptx` | 学术演讲 PPT | `/ppt`（自动路由） |
| `slidetailor` | 论文 PDF → 学术幻灯片 | `/ppt --backend slidetailor` |
| `slidev` | 开发者演示（Markdown + Vue） | `/ppt --backend slidev` |
| `marp` | Markdown 快速出片 | `/ppt --backend marp` |
| `ppt-architect` | PPT 场景图表构建（路由至 mermaid/plantuml/diagrams） | 内部调度 |
| `ppt-rag-indexer` | PPT 专用 RAG 索引检索 | `/ppt --rag` |
| `ppt-web-researcher` | PPT 多源内容搜集（官方/媒体/学术/产业/社区） | `/ppt --research` |
| `html-chart` | HTML+Playwright 截图，4 种风格 | `/illustrate` |
| `mermaid-chart` | Mermaid 图表生成 | `/illustrate --backend mermaid` |
| `diagram-markmap` | Markmap 思维导图 | `/diagram-mindmap` |
| `diagram-plantuml` | PlantUML 全系 UML | `/diagram-uml` |
| `arch-diagram` | 云架构图（AWS/GCP/Azure/K8s/阿里云） | `/arch-diagram` |
| `visio-builder` | Visio 图表创建与格式互转 | `/visio` |
| `ai-illustrator` | AI 智能插图（article / thesis-figure / document 子流程） | 对话触发 |
| `stable-diffusion` | SD WebUI 文生图 / 图生图 | `/illustrate --backend sd` |
| `impeccable` | 反 AI Slop 前端设计语言（7 领域 vocabulary + 32 上游 flow 参考 + 27 反模式 + 12 critique） | `/impeccable` |
| `md-poster` | Markdown 转海报/分享卡片 | `/md-poster` |
| `md-table-image` | Markdown 表格转图片 | `/md-table-image` |
| `table-from-text` | 层级文本 → Markdown/CSV/Excel 表格 | `/table-from-text` |
| `table-csv-md` | CSV ↔ Markdown 表格互转 | `/table-csv` |

### 数据与研究

| Skill | 描述 | 触发方式 |
|-------|------|---------|
| `taskweaver` | 代码优先 Agent，Python 沙箱执行 | `/taskweaver` |
| `chat2db` | 自然语言转 SQL | 对话触发 |
| `paper-collector` | arXiv 安全论文搜集 | `/paper-collect` |
| `paper-interpreter` | 论文 PDF 深度解读（4000-6000 字公众号长文） | `/paper-interpret` |

### 媒体

| Skill | 描述 | 触发方式 |
|-------|------|---------|
| `remotion-native` | Remotion 原生模板渲染 | `/remotion-native` |
| `remotion-prompt2video` | 提示词 → 视频 | `/remotion-prompt2video` |
| `remotion-vidosy` | Vidosy JSON → 视频 | `/remotion-vidosy` |
| `pdf2video` | PDF/PPT 转动态视频 | `/pdf2video` |
| `omni-captions` | 视频字幕生成 | `/caption` |
| `videocut` | AI 视频智能剪辑 | `/videocut` |
| `content-sync` | 30+ 平台内容分发 | `/sync` |

### 售前 / 解决方案

| Skill | 描述 | 触发方式 |
|-------|------|---------|
| `discovery-call` | 客户拜访与需求挖掘 | `/discovery-call` |
| `gap-analysis` | 客户需求 vs 产品能力对照 | `/gap-analysis` |
| `solution-architecture` | SA Blueprint 12 章 | `/solution-architecture` |
| `business-case` | 客户价值证明（ROI / TCO / Payback / NPV） | `/business-case` |
| `rfp-response` | RFP / RFI 应答 | `/rfp-response` |
| `security-questionnaire` | 安全问卷应答（CAIQ / SIG / VSA） | `/security-questionnaire` |
| `battle-card` | 竞品作战卡 | `/battle-card` |
| `demo-design` | Demo 设计与演练 | `/demo-design` |
| `poc-plan` | PoC/试点管理 | `/poc-plan` |
| `gtm-strategy` | GTM 上市战略 | `/gtm-strategy` |
| `proposal-generator` | 企业项目型方案文档 | `/proposal` |
| `sales-guide-writer` | B2B 销售赋能 | `/sales-guide` |
| `doc-auditor` | 产品文档质量审核 | `/doc-audit` |

### 工具与集成（tools）

| Skill | 描述 | 触发方式 |
|-------|------|---------|
| `od-contribute` | 一键向 [nexu-io/open-design](https://github.com/nexu-io/open-design) 提交贡献（Skill / Design System / 翻译 / 文档 / bug）——即使不会写代码 | `/od-contribute` |

---

## 命令系统（v2.6 原子命令为主）

### 写作类

```bash
/article-writer 帮我写一篇关于 Claude Code 的公众号文章
/hv-analysis 帮我用横纵分析法研究 Hermes Agent
/interview-writer 以下是我和张三的访谈记录：[素材]

# 风格三段式：提炼 → 创作 → 优化
/style-extract --learn url1,url2 --output style.md
/style-create --title "文章标题" --style-card style.md
/style-refine article.md --style-card style.md

# 去 AI 味三段式：扫描 → 灵魂 → 学术
/humanize-scan article.md
/humanize-soul article.md
/humanize-academic thesis.md

/polish thesis.pdf --tone academic --intensity max
/marketing-copy AI 安全运营平台 --type wechat --audience tob --industry fintech --cta demo

# 标书七阶段（原子命令串行）
/bid-analyze 招标文件.pdf --color --clarify-list
/bid-clarify
/bid-outline --from 要求清单.xlsx --with-deviation
/bid-write --section solution --kb company-docs/ --figures
/bid-review
/bid-check
/bid-export
```

### 产品管理类

```bash
# PRD 全光谱
/prd-lite "AI 写作助手"                     # 1 页对齐方向
/prd-standard "AI 写作助手"                 # 标准 8 章
/prd-spec-first "API 网关重构"              # Spec-First 四件套
/prd-proto "新功能页面" --wireframe         # 含 ASCII 线框图
/pm-prd-enterprise "多租户 RBAC 后台"       # B 端严格 12 章

# 对话渐进 PRD（想法模糊时）
/prd-diagnose "我有个模糊的想法..."
/prd-concept                                # 概念稿
/prd-impl                                   # 实现稿
/prd-update prd-v1.md                       # 增量更新

# PRD 质量
/prd-quality prd.md                         # 5 维度评分
/prd-deep-evaluate prd.md                   # 23 节模板差距

# 调研类
/market-research AI 写作工具市场 --mode competitive
/user-research 验证用户付费意愿
/analytics 用户注册漏斗分析

# 数据看板（7 类原子）
/dashboard-northstar
/dashboard-aarrr
/dashboard-cohort
/dashboard-revenue
/dashboard-customer-br
/dashboard-ai-monitor
/dashboard-platform-selector

# 战略决策
/working-backwards "新功能想法"
/build-vs-buy "自研 vs 用 Auth0"
/sunset "Legacy Feature X"
/win-loss --quarter Q2
/churn-analysis --quarter Q2
/tech-debt --quarter Q2
/ai-red-team "v2.0 模型"

# PM 流程
/pm-intake "客户工单"
/pm-discovery "AI 安全 SOC 智能体的市场切入"
/pm-review "PRD-2026-Q2.md"
/pm-sales-pack "AI 渗透测试智能体 / 央企客户"
/gtm-strategy 云安全产品上市 --growth plg
```

### 售前 / 解决方案类

```bash
# 客户接触 + 需求挖掘
/discovery-call 某城商行 --mode prep --type first-call
/discovery-call 某医疗集团 --mode mom

# 需求评估 + 方案设计
/gap-analysis ./Requirements.xlsx --industry fintech
/solution-architecture 某城商行 SOC --industry fintech --deployment private
/business-case 某政务云项目 --industry gov

# 招标 / 应答
/rfp-response ./Bank_Tender.xlsx --industry fintech --themes "国产化,等保三级"
/security-questionnaire ./Bank_VSQ.xlsx --standard custom

# 标书七阶段：见上方 /bid-* 系列

# Demo + 竞品
/demo-design 某关键客户 --type business --duration 30
/battle-card Splunk --tier 1 --industry fintech

# PoC + 售前物料
/poc-plan 某客户试点 --industry fintech
/proposal 智慧城市交通 --type feasibility --industry gov
/sales-guide 数据安全产品 --industry fintech

# 16 类产品资料（原子命令）
/product-whitepaper AI 客服平台 --industry saas
/product-tech-whitepaper AI 客服平台
/product-brochure AI 客服平台
/product-intro-business AI 客服平台
/product-intro-tech AI 客服平台
/product-function-list AI 客服平台
/product-sales-faq AI 客服平台
/product-competitive AI 客服平台
/product-bid-params AI 客服平台
/product-solution AI 客服平台
/product-case AI 客服平台 --customer 某城商行
/product-manual AI 客服平台
/product-deploy AI 客服平台
/product-compat AI 客服平台
/product-release-note v2.0
/product-training AI 客服平台

/doc-audit ./product-docs/

# 售前总指挥
@solution-architect 某城商行 SOC 项目从首访到合同的完整推进
```

### 研究与数据类

```bash
/paper-collect --since 2026-02-01 --topic llm-security,fuzzing --limit 5
/paper-interpret paper.pdf --style professional --length medium
/taskweaver 查询最近 30 天销售额超过 1000 的订单
/hv-analysis 研究 Cursor 的产品策略与市场定位
```

### 媒体生成类

```bash
/ppt 帮我做一个论文答辩 PPT，主题是"深度学习"
/ppt 做一个产品介绍 PPT --style google --pages 10
/ppt --backend slidetailor --source paper.pdf
/ppt Q4业绩汇报 --rag quarterly_report.pdf kpi_data.xlsx --style mckinsey

/illustrate article.md
/illustrate --mode single --backend mermaid --type sequence --desc "微服务调用链"
/illustrate --mode single --backend sd --desc "AI 协作封面图" --sd-style digital-art

# Remotion 三引擎拆分
/remotion-native --template ai-native-company-intro --render
/remotion-prompt2video "30秒展示产品核心价值"
/remotion-vidosy story.json --render

/pdf2video report.pdf --render
/caption video.mp4 --translate zh --bilingual --format ass
/videocut lecture.mp4 --mode review
/sync article.md --platforms wechat,zhihu,juejin

# 图表五引擎独立
/diagram-mindmap "用户注册流程"
/diagram-uml --type sequence --desc "微服务调用链"
/arch-diagram 用户→CloudFront→ALB→EC2集群→RDS --provider aws
/visio 用户注册流程 --type flowchart
/visio diagram.mmd --mode convert --from mermaid --output vsdx

# Markdown 转图 + 表格
/md-poster article.md --theme gradient
/md-table-image table.md
/table-from-text "层级文本..." --to md
/table-csv data.csv --to md

# 反 AI Slop 设计语言
/impeccable craft "AI 安全产品 marketing landing page"
/impeccable critique src/components/Hero.tsx
/impeccable audit
/impeccable polish "the checkout form"
/impeccable quieter "the dashboard sidebar"
/impeccable bolder "the marketing hero"
/impeccable distill "the pricing page"
/impeccable harden "the signup flow"
/impeccable onboard "first-run experience"
```

---

## 核心场景

### 场景一：公众号长文创作

```bash
# 直接写作
/article-writer 帮我写一篇关于 AI Native 产品设计的文章

# 风格驱动三段式：先学风格，再创作，再优化
/style-extract --learn https://mp.weixin.qq.com/xxx --output style.md
/style-create --title "我的新文章标题" --style-card style.md
/style-refine article.md --style-card style.md

# 去 AI 味三段式
/humanize-scan article.md
/humanize-soul article.md

# 访谈稿：Writer-Reviewer 互搏迭代
/interview-writer --target-score 88 --max-rounds 3
```

### 场景二：标书全流程编制（v2.6 七阶段原子命令）

```bash
/bid-analyze 招标文件.pdf --color --clarify-list   # 1. 拆解 + 三色标记
/bid-clarify                                       # 2. 澄清问题清单
/bid-outline --from 要求清单.xlsx --with-deviation # 3. 大纲 + 偏离表
/bid-write --section solution --kb company-docs/   # 4. 分模块撰写
/bid-review                                        # 5. 双轮评审
/bid-check                                         # 6. 合规核查
/bid-export                                        # 7. 移交导出
```

三色标记规则：🔴 一票否决项 / 🟡 高分项 / 🔵 基础合规项

### 场景三：PPT 智能生成

```bash
/ppt 论文答辩 PPT，主题"深度学习在医疗影像中的应用"   # 自动路由到 academic-pptx
/ppt 产品季度汇报 --style business --pages 15          # 自动路由到 ppt-master
/ppt --backend slidetailor --source paper.pdf          # 论文 PDF 直接转幻灯片
/ppt React 技术分享 --backend slidev                   # 开发者演示
```

### 场景四：产品经理全流程

```bash
/pm-discovery "AI 写作助手浏览器插件"             # 一次性发现报告
/prd-standard "AI 写作助手浏览器插件"            # 标准 8 章 PRD（C 端）
/pm-prd-enterprise "多租户企业版"                # B 端严格 12 章
/market-research AI 写作工具市场 --mode competitive
/analytics 用户注册漏斗分析
/roadmap Q2 路线图规划 --horizon 3m
@qa-acceptance-designer "MVP 范围 v0.1"          # 验收方案
/launch-checklist MVP 上线
```

### 场景五：售前 / 解决方案全链路

```bash
# Stage 1 接触
/discovery-call 某城商行 --mode prep --type first-call
/discovery-call 某城商行 --mode mom

# Stage 2 评估
/gap-analysis ./Bank_Reqs.xlsx --industry fintech
/battle-card Splunk --tier 1 --industry fintech

# Stage 3 方案
/solution-architecture 某城商行 SOC --deployment private
/business-case 某城商行 SOC --baseline statusquo
/demo-design 某城商行 --duration 30

# Stage 4 应答
/rfp-response ./Bank_Tender.xlsx --industry fintech
/security-questionnaire ./Bank_VSQ.xlsx --standard custom
/bid-analyze 招标文件.pdf                         # 标书走 /bid-* 七阶段

# Stage 5 演示 + PoC
/demo-design 某城商行 --mode rehearse
/poc-plan 某城商行 PoC

# 一键编排
@solution-architect 某城商行 SOC 项目从首访到合同的完整推进
```

### 场景六：产品营销推广

```bash
/marketing-copy AI 安全运营平台 --type wechat --audience tob --industry fintech --cta demo
/marketing-copy 零信任访问控制方案 --type zhihu --audience tob --cta whitepaper
/marketing-copy 数据安全网关 --type xhs --audience tob --industry saas
/marketing-copy 数据安全网关 --type landing --cta demo
/marketing-copy v2.0 新功能发布 --type edm --audience tob --cta demo
/marketing-copy 半夜告警没人响应 --type video --duration 60
/marketing-copy 城商行案例 --type case --industry fintech --length long --cta demo
/marketing-copy "[公司名] 完成 A 轮融资" --type pr --length medium
```

### 场景七：视频全链路处理

```bash
# Remotion 三引擎
/remotion-native --template ai-native-company-intro --render
/remotion-prompt2video "30秒展示产品核心价值"
/remotion-vidosy story.json

# 文档转视频 + 智能剪辑 + 字幕
/pdf2video report.pdf --render
/videocut lecture.mp4 --mode review
/caption video.mp4 --translate zh --bilingual --format ass
/sync article.md --platforms wechat,zhihu,juejin,xiaohongshu
```

### 场景八：图表五引擎

```bash
# 思维导图 / UML / 云架构 / Visio / 通用配图
/diagram-mindmap "产品设计流程"
/diagram-uml --type sequence --desc "微服务调用链"
/arch-diagram 用户→CloudFront→ALB→EC2集群→RDS --provider aws
/visio 用户注册流程 --type flowchart
/illustrate article.md
```

### 场景九：反 AI Slop 的前端设计语言（Impeccable）

```bash
# 从零做一个落地页
/impeccable craft "AI 安全产品 marketing landing page"
/impeccable craft "城商行 SOC 产品页" --register brand --genre tech-minimal --stack react

# 已有 UI "AI 味重"，修
/impeccable critique src/components/Hero.tsx
/impeccable audit
/impeccable polish "the checkout form"

# 调强度
/impeccable bolder "the marketing hero"
/impeccable quieter "the dashboard sidebar"
/impeccable distill "the pricing page"

# 工程兜底 + 配置阶段
/impeccable harden "the signup flow"
/impeccable onboard "first-run experience"
/impeccable teach

# 端到端编排
@impeccable-designer 从零做一个 B 端 AI 安全产品的官网，editorial 风格
```

---

## 使用指南

### 编辑器配置

**Claude Code（推荐）**：直接 `/` 命令调用。配置位于 `.claude/settings.json`。
**Cursor**：Agent 模式，规则位于 `.cursor/rules/writing-guidelines.mdc`。
**OpenAI Codex / OpenCode**：通过读取 Skill 文件内容调用。

### Skill 调用方式

1. **对话触发**：在对话中描述需求，Claude Code 自动识别并激活对应 Skill
2. **命令调用**：使用 `/command-name` 直接调用，支持参数控制行为

### 质量标准

所有写作输出通过四层自检：

| 层次 | 检查项 | 标准 |
|------|--------|------|
| 活人感 | 是否有真实的人在说话 | 无 AI 套话，有个人立场 |
| 情感 | 是否打动读者 | 有温度，不说教 |
| 信息 | 是否有干货 | 有见识，不废话 |
| 结构 | 是否好读 | 段落节奏流畅 |

禁止出现的 AI 套话：「首先」「总之」「不得不说」「值得注意的是」「综上所述」等。

---

## 快速开始

**1. 克隆仓库**

```bash
git clone https://github.com/your-org/WorkAgent.git
cd WorkAgent
```

**2. 在 Claude Code 中打开**

```bash
claude .
```

**3. 尝试第一个命令**

```bash
# PM 全流程入门
/pm-intake "你脑子里那个模糊的想法"
/pm-discovery "你的产品方向"
/prd-diagnose "想法模糊"                      # 想法模糊时
/prd-standard "你的产品名"                    # 直接写
/working-backwards "你的功能想法"
@qa-acceptance-designer "MVP 范围 v0.1"

# 售前入门
@solution-architect "客户名 / 项目名"
/discovery-call 某客户 --mode prep
/gap-analysis ./Requirements.xlsx
/solution-architecture 项目名
/business-case 项目名
/rfp-response ./RFP.xlsx
/battle-card 对手名 --tier 1
/demo-design 客户名

# 营销推广入门
/marketing-copy 产品名 --type wechat --cta demo
/marketing-copy 产品名 --type landing
/marketing-copy 客户名 --type case

# 战略决策
/build-vs-buy "自研 vs 用 Auth0"
/sunset "Legacy Feature X"
/win-loss --quarter Q2
/churn-analysis --quarter Q2

# 通用任务
/article-writer 帮我写一篇关于 AI 工具提效的文章
/prd-lite "团队协作工具"
/ppt 产品季度汇报 --style business --pages 10
/arch-diagram 用户→CloudFront→ALB→EC2集群→RDS --provider aws
/pdf2video report.pdf --render
/diagram-mindmap "产品设计流程"
```

**4. 查看详细分工**

每个命令、Skill、Agent 的 frontmatter 都明确写明「不做什么 / 流转到哪个组件」。仓库健康度见 `HEALTH_REPORT.md`。

---

## 更新日志

### v2.7（二次裁剪 + 文档漂移修正，2026-07）

- 删除 4 个低价值 / 被覆盖的 Skill：`pm-core-framework` / `doc-formatter` / `bid-rewriter` / `pptx-sdk`
- 删除 1 个能力被 `@diagram-architect` + `@article-illustrator` 覆盖的 Agent：`visual-suite`
- 补录 v2.6 遗漏的 2 个 Agent：`web-search-analyst` / `xqy-spec-writer`（此前存在但 README/HEALTH_REPORT 未列入）
- 清理根仓库无关文件：删除 5 个漏洞挖掘遗留 Python 脚本
- 修复 `doc-polisher` / `product-director` / `bid-writer` / `ppt-generator` / `article-illustrator` 的 skills 列表和路由描述
- 新增 `AUDIT.md`：后续裁剪与结构优化的 checklist（product-\*-writer 合并、pm-\* 合并、skills 分子目录等）
- 最终规模：**25 Agents / 127 Skills / 114 Commands / 13 Templates**

### v2.6（单一职责拆分，2026-06）

- 拆分 16 个"多任务融合" Skill → 49 个原子 Skill
- 拆分 9 个 `--mode` 命令 → 30 个原子命令
- 删除冗余 `@writer-reviewer` Agent（已被 `style-writer-reviewer` Skill 完全覆盖）
- 修复 v2.5 残留的全部断链引用（pm-skills / product-spec / prd-writer / data-dashboard / bid full / humanize / diagram / remotion-generate 等）
- 修复 SR 违规描述（`proposal-generator` / `ai-illustrator` / `bid-write`）
- 最终规模：**24 Agents / 129 Skills / 112 Commands / 13 Templates**

### v2.5（依赖修复 + 重复清理 + 文档同步）

- 删除遗留兼容文件（`agents/visual-creator.md` 等）
- 修复所有指向已删命令/Agent 的引用（一次性修复 8 类）
- 为多个命令补齐"加载技能"声明
- 规模：25 Agents / 95 Skills / 83 Commands

### v2.4（聚焦工作技能，移除团队/人际管理类组件）

- 删除 2 个 Agent / 6 个 Skill / 9 个 Command / 2 个 Template
- 调用链路修复，重复命令清理

### v2.3（售前 / 解决方案补齐 + 营销推广 + 产品域裁剪）

- 新增售前 8 Skill / 8 Command + 营销推广 1 Skill + 1 Command
- 新建 `commands/presales/` 目录，迁出 13 个售前命令

### v2.2 / v2.1 / v2.0

- v2.2：新增图表架构 / Visio / Remotion / PPT 多源研究等能力
- v2.1：GTM / Proposal / Visual Suite 等编排 Agent
- v2.0：全栈 PM Agent / 风格自进化 / 文档润色 + 配图

### v1.0

- 初始版本：14 个 Agent，36+ 个 Skill，40+ 个 Command

---

## 来源

本项目集成了以下开源仓库的内容：

### 写作能力
- article-writer / hv-analysis — 文章写作技能

### 产品管理全流程能力
- [pm_claude_code_kit](https://github.com/) — B 端 / 企业级视角的 PM 工作台

### PPT 生成能力
- [ppt-master](https://github.com/hugohe3/ppt-master)、[academic-pptx-skill](https://github.com/Gabberflast/academic-pptx-skill)、[SlideTailor](https://github.com/nusnlp/SlideTailor)、[Slidev](https://github.com/slidevjs/slidev)、[Marp](https://github.com/marp-team/marp)、[python-pptx](https://github.com/scanny/python-pptx)、[PptxGenJS](https://github.com/gitbrent/PptxGenJS)、[frontend-slides](https://github.com/zarazhangrui/frontend-slides)

### 数据与可视化工具
- [TaskWeaver](https://github.com/microsoft/TaskWeaver)、[Chat2DB](https://github.com/chat2db/Chat2DB)、[Stable Diffusion WebUI](https://github.com/AUTOMATIC1111/stable-diffusion-webui)、[Mermaid](https://github.com/mermaid-js/mermaid)

### 设计语言（反 AI Slop）
- [pbakaus/impeccable](https://github.com/pbakaus/impeccable) — Paul Bakaus 的"让 AI harness 更会做设计"的设计语言（[impeccable.style](https://impeccable.style/)）

感谢以上作者的开源贡献。
