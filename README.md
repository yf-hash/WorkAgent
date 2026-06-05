# WorkAgent

> 以 Claude Code 为入口，通过自然语言 command 调用适配的 Agent 和 Skill，完成前场需求的工作智能体，满足产品经理、售前工程师、市场营销等不同用户的场景需求。

WorkAgent 是面向产品经理、售前工程师、市场营销等用户的工作智能体，核心理念是：**通过 WorkAgent，让工作效率指数级提升**。

---

## 项目概述

WorkAgent 是一套以 **风格驱动** 为核心设计理念的 AI 原生工作平台。它不是通用代码工具，而是专为前场业务人员打造的智能工作系统：
- **内容创作**：公众号长文、访谈稿、深度研究报告、文档润色
- **营销推广**：公众号软文 / 小红书 / 知乎 / 朋友圈 / 短视频 / 落地页 / EDM / PR 稿 / 客户故事 9 大文体
- **产品管理**：PRD 生成、竞品分析、用户研究、数据分析、路线图规划
- **售前 / 解决方案**：客户拜访 / 需求挖掘 / Gap Analysis / SA Blueprint / Business Case / RFP 应答 / 安全问卷 / 竞品作战卡 / Demo 设计 / PoC 全链路
- **标书编制**：七阶段全流程标书智能编制，三色标记 + RAG 增强写作
- **演示制作**：6 种 PPT 引擎自动路由，学术/商务/开发者场景全覆盖
- **数据分析**：自然语言转 SQL + Python 沙箱执行，联合数据库与文件分析
- **视频生成**：Remotion 动态视频，模板/字幕/TTS/MP4 渲染全流程
- **视频处理**：PDF/PPT 转动态视频、AI 智能剪辑、字幕生成、多平台分发
- **图表架构**：云架构图（AWS/GCP/Azure/K8s）、Visio 图表、多引擎统一路由

**支持编辑器**：Claude Code（完整支持）> Cursor > OpenAI Codex

---

## 核心内容

| 模块 | 数量 | 说明 |
|------|------|------|
| Agents | 25 个 | 自治代理，编排完整业务流程 |
| Skills | 82 个 | 可复用知识库，自动激活或命令调用 |
| Commands | 67 个 | 统一命令入口，智能路由到对应 Skill/Agent |

**设计原则**：
- **风格驱动**：所有写作输出以用户/角色风格为第一优先级，避免 AI 套话
- **人机协同**：关键节点设置人工确认，标书/内容创作均有阶段性检查点
- **多引擎路由**：PPT、配图、数据分析等场景支持多种后端引擎自动选择
- **质量四层自检**：活人感 → 情感 → 信息 → 结构，逐层验证输出质量

---

## 项目结构

```
WorkAgent/
├── agents/             # 25 个自治代理（编排完整业务流程）
├── skills/             # 82 个可复用知识库
├── commands/           # 67 个统一命令入口（按域分组）
│   ├── writing/        # 8 个：写作类（含 marketing-copy 营销推广）
│   ├── product/        # 31 个：产品管理类（PM 全流程 + 战略决策 + AI 红队）
│   ├── presales/       # 13 个：售前 / 解决方案类（拜访 / 方案 / RFP / Demo / 竞品 / PoC / 销售物料）
│   ├── research/       # 4 个：研究类
│   └── media/          # 11 个：媒体类
├── templates/          # 13 个标准模板（PRD/BRD/MRD/Roadmap/PM-Discovery/验收/Release/Sales/需求池/PR-FAQ/6-pager/Model Card/Eval Rubric）
├── hooks/              # Claude Code 生命周期钩子（可选）
├── .claude/
│   └── settings.json   # Claude Code 权限配置
├── .cursor/
│   └── rules/          # Cursor 写作规范规则
├── CLAUDE.md           # Claude Code 完整使用指南
├── AGENTS.md           # Codex/OpenCode 兼容指南
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
| `ai-product-architect` | AI 产品架构师 — 专注 LLM/Agent/RAG 类功能的规格、Prompt、Eval、失败模式管理（套用 pm-ai-security-product 方法论） | AI 功能 PRD、Prompt 工程交付、AI 功能上线评审 |
| `growth-strategist` | 增长战略 — 统筹 PMF / 漏斗诊断 / A/B 实验 / 定价 | PMF 验证、增长瓶颈诊断、实验设计、定价优化 |
| `research-analyst` | 综合研究分析师 — 用户研究 + 市场情报 + 反馈分析 + PMF 验证 | 早期 0→1 探索、立项验证、PMF 测量 |
| `gtm-strategist` | GTM 全链路战略（增长模型/ICP/定位/渠道/定价/90天计划） | 新产品上市规划、GTM 诊断与优化 |
| `proposal-writer` | 企业方案撰写全链路（售前方案/可研报告/初步设计，多行业定制） | 售前解决方案、项目建议书 |
| `product-enablement` | 产品赋能（销售指南/文档审计/产品文档） | 产品赋能、销售支持 |
| `market-intelligence` | 市场情报分析（竞品监测/TAM/趋势/选品/OSS 生态） | 深度竞品分析、市场研究、选品研究 |
| `bid-writer` | 标书全流程编制（七阶段：拆解→澄清→大纲→撰写→评审→核查→移交） | 标书/投标/招标文件编制 |
| `content-director` | 全流程内容创作编排（风格分析→框架→写作→QA→迭代） | 需要完整写作流程 |
| `writer-reviewer` | Writer-Reviewer 互搏 + 知识库进化 | 访谈写作迭代优化 |
| `style-evolver` | 风格学习 → 风格卡片确认 → Writer-Reviewer 迭代创作 | 风格迁移、参考文章仿写 |
| `doc-polisher` | 文档智能润色（AI 去痕 + 智能配图全自动闭环） | 文档润色、去 AI 味 + 配图一体化 |
| `paper-researcher` | 论文研究（arXiv 搜集 + 单篇深度解读） | 论文情报跟踪、学术科普写作 |
| `video-maker` | Remotion 视频生成（模板/字幕/TTS/渲染） | 企业介绍视频、产品演示视频 |
| `ppt-generator` | PPT 生成协调，6 种引擎路由（academic/slidetailor/ppt-master/slidev/marp/sdk） | PPT 生成任务 |
| `data-analyst` | 综合 TaskWeaver + Chat2DB 的数据分析 Agent | 数据查询、分析、报表生成 |
| `article-illustrator` | 文章内联配图 — HTML 图表 + Mermaid + Stable Diffusion 三合一，专为 .md 文章自动批量配图 | 文章/博客自动配图 |
| `visual-suite` | 视觉内容全链路（配图/思维导图/UML/Markdown 海报/表格可视化） | 文章配图、图表、MD 转图片 |
| `diagram-architect` | 统一图表编排，自动路由至 Mermaid/PlantUML/diagrams/Visio 最优引擎 | 图表类型不确定、需要多图表套件、格式互转时 |

---

## Skill 系统

86 个可复用知识库，支持对话触发或命令调用：

### 写作与内容

| Skill | 描述 | 触发方式 |
|-------|------|---------|
| `article-writer` | 文章风格公众号长文写作（4000-8000 字） | 对话触发 或 `/article-writer` |
| `hv-analysis` | 横纵分析法深度研究，输出 PDF 报告（10000-30000 字） | 对话触发 或 `/hv-analysis` |
| `interview-writer` | 访谈写作 v2.0，Writer-Reviewer 互搏 + 知识库进化 | 对话触发 或 `/interview-writer` |
| `style-evolver` | 风格驱动内容自进化，从参考文章提炼风格卡片，迭代创作 | 对话触发 或 `/self-evolve` |
| `humanizer` | AI 文本人性化改写（40+ 痕迹检测，五维评分） | `/humanize` 命令调用 |
| `marketing-copy` | 产品营销推广内容 9 大文体（公众号软文 / 小红书 / 知乎 / 朋友圈 / 短视频 / 落地页 / EDM / PR 稿 / 客户故事 / Demo 脚本）| `/marketing-copy` 命令调用 |
| `doc-formatter` | 文档格式化模块（DOCX读写 + 中文排版校正 + 导出），被 doc-polisher agent 调用 | `/polish` 命令调用 |
| `bid-writer` | 标书七阶段编制知识库（三色标记/偏离表/RAG 写作/双轮评审/合规核查） | `/bid` 命令调用 |
| `bid-rewriter` | 偏离表"无偏离"应答项五原则同义改写 | `/bid rewrite` 调用 |

### PPT 与可视化

| Skill | 描述 | 触发方式 |
|-------|------|---------|
| `ppt-master` | 通用 PPT 生成，支持多种设计风格和图片生成 | `/ppt` 命令调用 |
| `academic-pptx` | 学术演讲 PPT 生成，论证优先设计 | `/ppt` 命令调用 |
| `slidetailor` | 论文 PDF → 学术幻灯片，NLP 自动提取内容 | `/ppt --backend slidetailor` |
| `slidev` | 开发者/技术演示，Markdown + Vue，代码高亮动画 | `/ppt --backend slidev` |
| `marp` | Markdown 快速出片，输出 HTML/PDF/PPTX | `/ppt --backend marp` |
| `pptx-sdk` | 编程式 PPTX 生成（python-pptx + PptxGenJS） | `/ppt --backend sdk` |
| `html-chart` | HTML 图表生成器，ASCII 草图→HTML→Playwright 截图，4 种风格 | `/illustrate`（主管道） |
| `mermaid-chart` | Mermaid 图表生成（流程图/时序图/甘特图/ER 图等） | `/illustrate --backend mermaid` |
| `stable-diffusion` | AI 图像生成，文生图/图生图（需本地 SD WebUI） | `/illustrate --backend sd` |

### 产品管理

| Skill | 描述 | 触发方式 |
|-------|------|---------|
| `pm-skills` | 产品经理技能库（JTBD/RICE/OKR/PMF/发布清单/用户故事地图等） | 对话触发 或 `/pm-skills` |
| `product-spec` | 产品规格统一知识库（PRD/Spec-First/原型+PRD/一页纸，四种模式） | `/product-spec` 命令调用 |
| `prd-writer` | 对话式 PRD 引导写作（chituai/prd-writer，MIT），三镜诊断+两阶段交付，支持从零生成/文档评估/增量更新 | `/prd-writer` 或 `@prd-coach` |
| `market-research` | 市场研究与竞争情报（竞品/趋势/TAM/亚马逊选品/OSS 生态） | `/market-research` 命令调用 |
| `user-research` | 用户研究方法论（访谈/问卷/卡片分类/旅程/画像/JTBD） | `/user-research` 命令调用 |
| `product-analytics` | 产品数据分析（指标体系/漏斗/留存/埋点/PostHog/Matomo） | `/analytics` 命令调用 |
| `user-feedback` | 用户反馈管理（NPS/CSAT/功能投票/VoC 报告/情感分析） | `/feedback` 命令调用 |
| `product-roadmap` | 路线图规划（RICE/MoSCoW/Gantt/GitHub Projects/OKR） | `/roadmap` 命令调用 |
| `design-proto` | 产品设计与原型（线框图/Penpot/Framer Motion/Onboarding） | `/design-proto` 命令调用 |
| `product-strategy` | 产品战略画布（BMC/Lean/VPC/Vision/北极星）+ 假设清单 + Pre-Mortem | `/product-strategy` 命令调用 |
| `user-story-mapping` | 用户故事地图（Backbone + Walking Skeleton + Release Slices） | `/user-story-mapping` 命令调用 |
| `mvp-canvas` | MVP 设计画布（RAT + 9 种 MVP 类型 + Build-Measure-Learn） | `/mvp-canvas` 命令调用 |
| `ab-test` | A/B 实验完整方法论（假设/样本/显著性/护栏/SRM/Peeking） | `/ab-test` 命令调用 |
| `launch-checklist` | 发布检查清单（6 轨道 + 时间盒 + Go/No-Go + 回滚预案） | `/launch-checklist` 命令调用 |
| `pricing-strategy` | 定价策略（Freemium/套餐/PSM/Conjoint/涨价/单位经济） | `/pricing-strategy` 命令调用 |
| `pmf-survey` | PMF 评估（Sean Ellis + HXC + 信号雷达 + Pivot 决策） | `/pmf-survey` 命令调用 |
| `product-report` | 产品报告（周报/月报/季度/Board/客户 BR + 受众分层） | `/product-report` 命令调用 |
| `data-dashboard` | 数据看板生成（PostHog/Mixpanel/Amplitude/Matomo/GA4/Heap + 6 类模板） | `/data-dashboard` 命令调用 |
| `compliance-checklist` | 合规检查（等保/SOC2/ISO27001/GDPR/HIPAA/PCI/个保法 + 客户问卷） | `/compliance-checklist` 命令调用 |
| `poc-plan` | PoC/试点管理（范围谈判 + SOW + 验收标准 + 转正 SOP） | `/poc-plan` 命令调用 |
| `working-backwards` | Amazon 逆向工作法（PR-FAQ + 6-pager） | `/working-backwards` 命令调用 |
| `build-vs-buy` | Build vs Buy 决策框架（TCO 3 年 + Vendor 12 维评估） | `/build-vs-buy` 命令调用 |
| `sunset-plan` | 产品/功能下线 playbook（90/60/30/0 天客户通知） | `/sunset` 命令调用 |
| `win-loss-analysis` | Win/Loss 赢单失单分析（访谈结构 + 根因聚类 + ICP 修正） | `/win-loss` 命令调用 |
| `churn-analysis` | Churn 流失分析 + Save Playbook（CHI 健康度 + 三级 Save Play） | `/churn-analysis` 命令调用 |
| `tech-debt` | 技术债优先级（WSJF + 20% 规则 + SLO 守门 + 业务话术） | `/tech-debt` 命令调用 |
| `ai-red-team` | AI 红队测试（OWASP LLM Top 10 + 10 个必测场景） | `/ai-red-team` 命令调用 |
| `pm-core-framework` | PM 通用工作框架（前置思考层）— 阶段判断 + 受众判断 + 输出结构 | 对话触发 |
| `pm-full-cycle` | PM 端到端 13 步编排（市场→用户→竞品→定位→功能→MVP→Roadmap→PRD→验收→发布→销售） | 对话触发 |
| `pm-qa-acceptance` | 测试验收 10 维方法论（功能/权限/异常/数据/状态/性能/审计/兼容/客户口径/上线阻断项） | 对话触发，被 `@qa-acceptance-designer` 调用 |
| `pm-ai-security-product` | AI / 网络安全产品双轴方法论（AI 维度 + 安全维度 + 红线 + 12 章产品方案，含 Eval / Prompt / 失败模式 / 成本） | 对话触发，被 `@ai-product-architect` 调用 |

### 数据与研究

| Skill | 描述 | 触发方式 |
|-------|------|---------|
| `taskweaver` | 代码优先 Agent，Python 沙箱执行数据分析和自动化任务 | 对话触发 或 `/taskweaver` |
| `chat2db` | 自然语言转 SQL，支持 MySQL/PostgreSQL 等主流数据库 | 对话触发 或 `/taskweaver --backend sql` |
| `paper-collector` | arXiv 安全论文搜集与中文摘要生成 | `/paper-collect` 命令调用 |
| `paper-interpreter` | 论文 PDF 深度解读（4000-6000 字公众号长文） | `/paper-interpret` 命令调用 |

### 媒体

| Skill | 描述 | 触发方式 |
|-------|------|---------|
| `remotion-generator` | Remotion 动态视频生成（模板/字幕/TTS/渲染） | `/remotion-generate` 命令调用 |
| `pdf2video` | PDF/PPT 转动态视频（stack/focus/zoom/fan 四种场景动画，直接渲染 MP4） | `/pdf2video` 命令调用 |
| `omni-captions` | 视频字幕生成（转录/翻译/双语/30+格式，Claude 翻译无需额外 API） | `/caption` 命令调用 |
| `videocut` | AI 视频智能剪辑（去停顿/重复/口误，ASR+Claude 语义分析+FFmpeg 剪切） | `/videocut` 命令调用 |
| `content-sync` | 内容多平台分发（30+ 平台一键同步，Wechatsync MCP + PostBot） | `/sync` 命令调用 |

### 售前 / 解决方案（SE / SA 全链路）

| Skill | 描述 | 触发方式 |
|-------|------|---------|
| `discovery-call` | 客户拜访与需求挖掘（背调 / SPIN / MEDDIC / MoM / 回声邮件 / Win Score） | `/discovery-call` 命令调用 |
| `gap-analysis` | 客户需求 vs 产品能力对照（4 级标签 / 评分 / Closure Plan / 投 vs 弃决策树）| `/gap-analysis` 命令调用 |
| `solution-architecture` | 解决方案架构（SA Blueprint 12 章 / NFR / 三档报价 / 行业定制）| `/solution-architecture` 命令调用 |
| `business-case` | 客户价值证明（ROI / TCO / Payback / NPV / 三档敏感性 / 行业锚点）| `/business-case` 命令调用 |
| `rfp-response` | RFP / RFI 应答（4 级模式 / Winning Themes / KB 复用 / 风险措辞红线）| `/rfp-response` 命令调用 |
| `security-questionnaire` | 安全问卷应答（CAIQ / SIG / VSA / 13 大类 / 合规证据映射）| `/security-questionnaire` 命令调用 |
| `battle-card` | 竞品作战卡（一页纸 / 三大杀手锏 / 三个雷区 / 标准应答 / 季度迭代）| `/battle-card` 命令调用 |
| `demo-design` | Demo 设计与演练（故事线 / 数据集 / 异常应对 / 反对意见 / 评分自检）| `/demo-design` 命令调用 |

### 产品赋能

| Skill | 描述 | 触发方式 |
|-------|------|---------|
| `gtm-strategy` | GTM 上市战略知识库（增长模型/ICP/定位/渠道/定价/90天计划/GTM KPI） | `/gtm-strategy` 命令调用 |
| `proposal-generator` | 企业方案撰写知识库（售前解决方案/可研报告/初步设计，多行业定制） | `/proposal` 命令调用 |
| `sales-guide-writer` | B2B 销售赋能知识库（销售一页禅/场景剧本/竞争话术/行业 FAQ） | `/sales-guide` 命令调用 |
| `product-doc-writer` | B2B 产品资料体系（24 类标准文档：白皮书/彩页/解决方案/操作手册等） | `/product-doc` 命令调用 |
| `doc-auditor` | 产品文档质量审核（14 项检查/24 类完整性/命名规范/密级管理） | `/doc-audit` 命令调用 |

### 可视化增强

| Skill | 描述 | 触发方式 |
|-------|------|---------|
| `diagram-suite` | 完整图表生成套件（Markmap 思维导图/PlantUML/Mermaid/MerdiAi 四引擎路由） | `/diagram` 命令调用 |
| `arch-diagram` | 云架构图生成（AWS/GCP/Azure/K8s/阿里云），基于 mingrammer/diagrams | `/arch-diagram` 命令调用 |
| `visio-builder` | Visio 图表创建与转换（python-visio / Visio.NET COM），支持 .vsdx 读写和格式互转 | `/visio` 命令调用 |
| `ai-illustrator` | AI 智能插图生成（文章配图/学术图表/文档插图/创意画布，支持多种艺术风格） | 对话触发 |
| `md-visual` | Markdown 转视觉图像（md 转图片/海报/卡片，整合 mark-pic/Madopic/tablesnap） | `/md-visual` 命令调用 |
| `table-toolkit` | 表格生成与转换工具集（文本/CSV/自然语言转 Markdown 表格，多工具链整合） | `/table` 命令调用 |

---

## 命令系统

72 个统一命令入口，按场景分类：

### 写作类

```bash
/article-writer 帮我写一篇关于 Claude Code 的公众号文章
/hv-analysis 帮我用横纵分析法研究 Hermes Agent
/interview-writer 以下是我和张三的访谈记录：[素材]
/self-evolve --learn url1,url2 --title "文章标题"
/humanize article.md --tone casual --intensity high
/polish thesis.pdf --tone academic --intensity max
/marketing-copy AI 安全运营平台 --type wechat --audience tob --industry fintech --cta demo
/marketing-copy 零信任访问控制 --type xhs --industry saas
/marketing-copy 数据安全网关 --type landing --cta demo
/bid full 招标文件.pdf --kb company-docs/
/bid analyze 招标.pdf --color --clarify-list
/bid write --section solution --kb company-docs/ --figures
/bid rewrite --file 技术偏离表.docx
```

### 产品管理类

```bash
/product-spec 开发一个 AI 写作助手浏览器插件 --mode prd
/product-spec 新功能 GTM 计划 --mode prd --prd-mode gtm
/market-research AI 写作工具市场 --mode competitive
/market-research 中国 SaaS 趋势 --mode trend --output report
/user-research 验证用户是否愿意为 AI 写作工具付费
/analytics SaaS 产品指标体系设计 --mode metrics
/analytics 用户注册漏斗分析 --mode funnel
/feedback 分析 feedback.csv 用户反馈 --source feedback.csv
/feedback 设计月度 NPS 调查 --mode nps
/roadmap Q2 产品路线图规划 --horizon 3m
/roadmap 需求优先级排序 --mode prioritize
/design-proto 设计 SaaS 仪表盘线框图 --mode wireframe
/pm-skills RICE 优先级框架 --mode framework
/gtm-strategy 云安全产品上市策略 --mode fullplan --growth plg
/gtm-strategy --mode diagnose --market b2b

# === 战略决策 ===
/working-backwards "新功能想法" --mode pr-faq
/build-vs-buy "自研 vs 用 Auth0"
/sunset "Legacy Feature X"
/win-loss --quarter Q2
/churn-analysis --quarter Q2

# === 工程协作 ===
/tech-debt --quarter Q2
/ai-red-team "v2.0 模型"

# === PM 全流程（pm_claude_code_kit 集成）===
/pm-intake "客户工单：审批流跑不通，老板要求 4 周上线"   # 任务类型判断 + 缺口标注
/pm-discovery "AI 安全 SOC 智能体的市场切入"             # 发现阶段一次性产出
/pm-prd-enterprise "多租户 RBAC 后台"                   # 企业级 PRD 严格 12 章模板
/pm-review "PRD-2026-Q2-审批流.md"                      # PM 视角 10 维度评审
/pm-sales-pack "AI 渗透测试智能体 / 央企客户"            # 销售赋能一次性出包
```

### 售前 / 解决方案类

```bash
# 客户接触 + 需求挖掘
/discovery-call 某城商行 --mode prep --type first-call --industry fintech
/discovery-call 某医疗集团 --mode mom --type deep-dive --industry healthcare
/discovery-call 项目机会评估 --mode score    # MEDDIC + Win Score

# 需求评估 + 方案设计
/gap-analysis ./CustomerRequirements.xlsx --mode analyze --industry fintech
/solution-architecture 某城商行 SOC --mode blueprint --industry fintech --deployment private
/business-case 某政务云项目 --mode onepage --industry gov --baseline statusquo

# 招标 / 应答
/rfp-response ./Bank_Tender.xlsx --industry fintech --themes "国产化,等保三级,本地化"
/security-questionnaire ./Bank_VSQ.xlsx --mode draft --standard custom

# Demo + 竞品
/demo-design 某关键客户 --mode storyline --type business --industry fintech --duration 30
/demo-design 客户 X 现场演练 --mode rehearse
/battle-card Splunk --mode build --tier 1 --industry fintech

# PoC + 售前物料
/poc-plan 某客户试点 --mode fullset --industry fintech
/proposal 智慧城市交通系统 --type feasibility --industry gov
/proposal 企业私有化部署方案 --type presale --industry finance
/sales-guide 数据安全产品 --mode full --industry fintech
/product-doc AI 客服平台 --type whitepaper --industry saas
/doc-audit ./product-docs/ --mode fullset --strict

# 售前总指挥
@solution-architect 某城商行 SOC 项目从首访到合同的完整推进
```

### 研究与数据类

```bash
/paper-collect --since 2026-02-01 --topic llm-security,fuzzing --limit 5
/paper-interpret paper.pdf --style professional --length medium
/taskweaver 查询最近 30 天销售额超过 1000 的订单
/taskweaver 分析 sales.csv 按月统计销售额并生成图表
/taskweaver 合并 data/ 目录下所有 Excel 文件 --output combined.csv
```

### 媒体生成类

```bash
/ppt 帮我做一个论文答辩 PPT，主题是"深度学习"
/ppt 做一个产品介绍 PPT --style google --pages 10
/ppt --backend slidetailor --source paper.pdf --duration 15
/ppt React Hooks 技术分享 --backend slidev
/ppt Q4业绩汇报 --rag quarterly_report.pdf kpi_data.xlsx --style mckinsey
/illustrate article.md
/illustrate --mode single --backend mermaid --type sequence --desc "微服务调用链"
/illustrate --mode single --backend sd --desc "AI 协作封面图" --sd-style digital-art
/remotion-generate --template ai-native-company-intro --render
/pdf2video report.pdf --render
/pdf2video presentation.pptx --style tech --scene-type stack --render
/caption video.mp4 --translate zh --bilingual --format ass
/caption https://youtube.com/watch?v=xxx --translate zh
/videocut lecture.mp4 --mode review
/videocut podcast.mp4 --mode auto
/sync article.md --platforms wechat,zhihu,juejin
/diagram "用户注册流程" --engine markmap --type mindmap
/diagram --engine plantuml --type sequence --desc "微服务调用链"
/arch-diagram 用户→CloudFront→ALB→EC2集群→RDS+ElastiCache --provider aws
/arch-diagram Ingress→Service→Pod(前端/后端/Worker)→PVC --provider k8s
/visio 用户注册流程：填写信息→邮箱验证→完善资料→激活 --type flowchart
/visio diagram.mmd --mode convert --from mermaid --output vsdx
/md-visual article.md --type poster --theme gradient
/table "姓名、年龄、城市\n张三、28、北京" --from text --to md
```

---

## 核心场景

### 场景一：公众号长文创作

适用于需要输出高质量、有个人风格的公众号文章。

```bash
# 直接写作
/article-writer 帮我写一篇关于 AI Native 产品设计的文章

# 风格迁移：先学习参考文章风格，再创作
/self-evolve --learn https://mp.weixin.qq.com/xxx --title "我的新文章标题"

# 访谈稿：Writer-Reviewer 互搏迭代
/interview-writer --target-score 88 --max-rounds 3
```

### 场景二：标书全流程编制

七阶段流水线，支持一键全流程或分阶段执行：

```bash
# 一键全流程
/bid full 招标文件.pdf --kb company-docs/

# 分阶段执行
/bid analyze 招标.pdf --color --clarify-list   # 拆解 + 三色标记
/bid outline --from 要求清单.xlsx --with-deviation  # 偏离表 + 大纲
/bid write --section solution --kb company-docs/    # 写技术方案
/bid rewrite --file 技术偏离表.docx                 # 偏离表改写
```

三色标记规则：🔴 一票否决项 / 🟡 高分项 / 🔵 基础合规项

### 场景三：PPT 智能生成

6 种引擎自动路由，覆盖学术/商务/开发者场景：

```bash
/ppt 论文答辩 PPT，主题"深度学习在医疗影像中的应用"   # 自动路由到 academic-pptx
/ppt 产品季度汇报 --style business --pages 15          # 自动路由到 ppt-master
/ppt --backend slidetailor --source paper.pdf          # 论文 PDF 直接转幻灯片
/ppt React 技术分享 --backend slidev                   # 开发者演示
```

### 场景四：产品经理全流程

从需求到上线的完整 PM 工作流：

```bash
/pm-discovery "AI 写作助手浏览器插件"               # 一次性发现报告
/product-spec 开发 AI 写作助手浏览器插件 --mode prd # PRD（C 端 / 通用）
/pm-prd-enterprise "多租户企业版"                  # PRD（B 端严格 12 章）
/market-research AI 写作工具市场 --mode competitive  # 竞品分析
/analytics 用户注册漏斗分析 --mode funnel            # 数据分析
/roadmap Q2 路线图规划 --horizon 3m                  # 路线图
/feedback 生成 Q1 用户之声报告 --mode voc            # 用户反馈
@qa-acceptance-designer "MVP 范围 v0.1"             # 验收方案
/launch-checklist MVP 上线 --mode full              # 上线检查
```

### 场景五：深度研究报告

横纵分析法，输出 10000-30000 字深度报告：

```bash
/hv-analysis 研究 Cursor 的产品策略与市场定位
```

### 场景六：GTM 上市战略

从增长模型选择到 90 天执行计划的完整 GTM 路径：

```bash
/gtm-strategy 云安全 SaaS 产品上市 --mode fullplan --growth plg
/gtm-strategy --mode diagnose    # 诊断当前 GTM 问题
/gtm-strategy 进入政府市场 --growth slg --market b2b --output deck
```

### 场景七：企业方案撰写

多行业定制，支持售前解决方案、可研报告、初步设计方案：

```bash
/proposal 智慧交通系统 --type feasibility --industry gov
/proposal 企业私有化部署 --type presale --industry finance
/proposal 工厂数字化改造 --type design --industry mfg
```

### 场景八：售前 / 解决方案全链路

从客户首次接触到合同签约的完整售前工作流：

```bash
# Stage 1 接触：拜访前准备 → 现场 → 会议纪要 → 回声邮件
/discovery-call 某城商行 --mode prep --type first-call --industry fintech
/discovery-call 某城商行 --mode mom
/discovery-call 某城商行 --mode email

# Stage 2 评估：需求 vs 能力 + 对手分析
/gap-analysis ./Bank_Reqs.xlsx --mode analyze --industry fintech
/battle-card Splunk --mode build --tier 1 --industry fintech

# Stage 3 方案：SA Blueprint + Business Case + Demo 准备
/solution-architecture 某城商行 SOC --mode blueprint --deployment private
/business-case 某城商行 SOC --mode onepage --baseline statusquo
/demo-design 某城商行 --mode storyline --duration 30

# Stage 4 应答：RFP / 安全问卷 / 标书
/rfp-response ./Bank_Tender.xlsx --industry fintech
/security-questionnaire ./Bank_VSQ.xlsx --standard custom
/bid full 招标文件.pdf --kb company-docs/

# Stage 5 演示 + PoC + 合同
/demo-design 某城商行 --mode rehearse        # 演练
/poc-plan 某城商行 PoC --mode fullset
/business-case 某城商行 --mode full           # 给法务 / 财务的完整版

# 一键编排：售前总指挥
@solution-architect 某城商行 SOC 项目从首访到合同的完整推进
```

### 场景九：产品营销推广

9 大文体覆盖产品对外推广（区别于个人风格公众号，强调 CTA + 转化）：

```bash
# 公众号软文 / 知乎专业种草（B 端教育）
/marketing-copy AI 安全运营平台 --type wechat --audience tob --industry fintech --cta demo
/marketing-copy 零信任访问控制方案 --type zhihu --audience tob --cta whitepaper

# 小红书种草（IT 决策人）
/marketing-copy 数据安全网关 --type xhs --audience tob --industry saas

# 官网落地页 / EDM 营销
/marketing-copy 数据安全网关 --type landing --cta demo
/marketing-copy v2.0 新功能发布 --type edm --audience tob --cta demo

# 短视频脚本（抖音 / 视频号 / 小红书）
/marketing-copy 半夜告警没人响应 --type video --duration 60

# 客户案例稿（外推版本）
/marketing-copy 城商行案例 --type case --industry fintech --length long --cta demo

# 新闻稿 / PR 稿
/marketing-copy "[公司名] 完成 A 轮融资" --type pr --length medium
```

### 场景十：视频全链路处理

从文档转视频到智能剪辑、字幕生成、多平台分发：

```bash
# PDF/PPT 转动态视频
/pdf2video report.pdf --render
/pdf2video presentation.pptx --style tech --scene-type zoom --render

# AI 视频智能剪辑（去停顿/口误）
/videocut lecture.mp4 --mode review
/videocut podcast.mp4 --mode auto

# 视频字幕生成（支持 YouTube）
/caption video.mp4 --translate zh --bilingual --format ass
/caption https://youtube.com/watch?v=xxx --translate zh

# 内容多平台一键分发
/sync article.md --platforms wechat,zhihu,juejin,xiaohongshu
```

### 场景十一：云架构图与 Visio 图表

从自然语言描述生成标准云架构图和 Visio 图表：

```bash
# 云架构图（AWS/GCP/Azure/K8s）
/arch-diagram 用户→CloudFront→ALB→EC2集群→RDS+ElastiCache --provider aws
/arch-diagram Ingress→Service→Pod(前端/后端/Worker)→PVC --provider k8s
/arch-diagram Pub/Sub→Dataflow→BigQuery→Looker --provider gcp

# Visio 图表创建与格式互转
/visio 用户注册流程：填写信息→邮箱验证→完善资料→激活 --type flowchart
/visio diagram.mmd --mode convert --from mermaid --output vsdx
/visio arch.puml --mode convert --from plantuml --output svg
```

---

## 使用指南

### 编辑器配置

**Claude Code（推荐）**

直接在 Claude Code 中使用 `/` 命令调用，所有功能完整支持。配置文件位于 `.claude/settings.json`，已预设必要权限。

**Cursor**

在 Agent 模式下使用，写作规范规则已配置于 `.cursor/rules/writing-guidelines.mdc`。

**OpenAI Codex / OpenCode**

参考 `AGENTS.md` 中的兼容指南，通过读取 Skill 文件内容调用。

### Skill 调用方式

Skills 支持两种触发方式：

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
# === PM 全流程入门（首次可参考 templates/pm-discovery-template.md 完整填充版）===
/pm-intake "你脑子里那个模糊的想法"          # 任务类型判断 + 缺口标注
/pm-discovery "你的产品方向"                  # 一次性发现报告
/working-backwards "你的功能想法"             # 立项前 PR-FAQ 倒推客户价值
/pm-prd-enterprise "你的产品名"               # B 端严格 12 章 PRD
@qa-acceptance-designer "MVP 范围 v0.1"      # 验收方案
/pm-sales-pack "你的产品名 / 目标客户"        # 销售赋能

# === 售前 / 解决方案入门 ===
@solution-architect "客户名 / 项目名"        # 端到端售前编排
/discovery-call 某客户 --mode prep            # 拜访前准备
/gap-analysis ./Requirements.xlsx             # 客户需求 vs 我方能力
/solution-architecture 项目名 --mode blueprint  # SA Blueprint 12 章
/business-case 项目名 --mode onepage          # 一页纸 ROI 给客户 CFO
/rfp-response ./RFP.xlsx                      # RFP 批量应答
/security-questionnaire ./VSQ.xlsx            # 安全问卷应答
/battle-card 对手名 --tier 1                  # 竞品作战卡
/demo-design 客户名 --mode storyline          # Demo 故事线

# === 营销推广入门 ===
/marketing-copy 产品名 --type wechat --cta demo      # 公众号软文
/marketing-copy 产品名 --type landing                # 落地页文案
/marketing-copy 客户名 --type case                   # 案例稿（外推版）

# === 战略决策 ===
/build-vs-buy "自研 vs 用 Auth0"             # Build vs Buy 决策（TCO + Vendor 评估）
/sunset "Legacy Feature X"                   # 产品/功能下线 Playbook（90/60/30/0 天）
/win-loss --quarter Q2                        # 赢单失单分析（季度做）
/churn-analysis --quarter Q2                  # 流失分析 + Save Playbook

# === 工程协作 ===
/tech-debt --quarter Q2                       # 技术债优先级评审

# === AI 产品 ===
/ai-red-team "v2.0 模型"                      # AI 红队测试（OWASP LLM Top 10）

# === 通用任务 ===
# 写一篇公众号文章
/article-writer 帮我写一篇关于 AI 工具提效的文章

# 生成一份 PRD（C 端通用）
/product-spec 开发一个团队协作工具 --mode prd --prd-mode lite

# 做一个 PPT（支持 RAG 模式）
/ppt 产品季度汇报 --style business --pages 10
/ppt Q4业绩汇报 --rag quarterly_report.pdf kpi_data.xlsx

# GTM 上市策略
/gtm-strategy 新产品上市规划 --mode fullplan

# 企业方案文档
/proposal 云计算解决方案 --type presale --industry fintech

# 云架构图
/arch-diagram 用户→CloudFront→ALB→EC2集群→RDS --provider aws

# 视频处理
/pdf2video report.pdf --render
/videocut lecture.mp4 --mode review

# 生成思维导图
/diagram "产品设计流程" --engine markmap --type mindmap
```

**4. 查看完整命令列表**

参考 `CLAUDE.md` 获取所有命令的完整参数说明和使用示例。

---

## 更新日志

### v2.4（聚焦工作技能，移除团队/人际管理类组件）

**裁剪后规模：25 Agents / 82 Skills / 67 Commands（31 product + 13 presales + 8 writing + 11 media + 4 research）/ 13 Templates。**

- **🗑️ 移除团队协作与人际关系管理类组件**：
  - 删除 2 个 Agent：`talent-screener`（HR 招聘）、`customer-success-manager`（客户关系维护）
  - 删除 6 个 Skill：`resume-screener`、`sprint-planning`、`retrospective`、`customer-success`、`stakeholder`（沟通工件）、`okr`（季度 OKR）
  - 删除 9 个 Command：`/screen`、`/sprint-planning`、`/retrospective`、`/customer-success`、`/status-update`、`/rbac-design`、`/sla-design`、`/stakeholder`、`/okr`（rbac/sla 在 v2.3 已删 Skill 但命令未清理；stakeholder/okr 早期残留）
  - 删除 2 个 Template：`one-on-one-templates.md`、`stakeholder-update-templates.md`
  - 删除空目录 `commands/hr/`
- **🔧 调用链路修复**：
  - `product-manager.md` 与 `ai-product-architect.md` 的 `skills:` 字段移除已删除引用
  - `writer-reviewer.md` 修正 frontmatter `skills` 写法（`skills: foo` → `skills: [foo]`）
  - 清理 10+ commands 与 10+ skills 中"与其他命令的协同"等关联块对已删命令的引用
- **🧹 重复命令清理**：删除冗余 `commands/product/sales-guide.md`（与 `commands/presales/sales-guide.md` 重复）

### v2.3（售前 / 解决方案补齐 + 营销推广 + 产品域裁剪）

**新增 1 个 Agent + 9 个 Skill + 9 个 Command + 1 个 Template，产品域命令拆分为 product/ + presales/。**

- **🆕 售前 / 解决方案能力（1 Agent + 8 Skill + 8 Command）**
  - 新增 `@solution-architect` 售前总指挥 Agent — 端到端编排客户拜访 → 需求 → 方案 → ROI → RFP → Demo → PoC → 合同
  - 新增 Skill：`discovery-call`（SPIN + MEDDIC + MoM + Win Score）、`gap-analysis`（4 级映射 + 投/弃决策树）、`solution-architecture`（SA Blueprint 12 章 + NFR + 三档报价）、`business-case`（ROI/TCO/Payback/NPV + 三档敏感性）、`rfp-response`（4 级模式 + Winning Themes + KB 复用）、`security-questionnaire`（CAIQ/SIG/VSA + 13 大类）、`battle-card`（一页纸竞品作战卡）、`demo-design`（故事线 + 演练 + 异常应对）
  - 对应命令：`/discovery-call`、`/gap-analysis`、`/solution-architecture`、`/business-case`、`/rfp-response`、`/security-questionnaire`、`/battle-card`、`/demo-design`
- **🆕 营销推广能力（1 Skill + 1 Command）**
  - 新增 `marketing-copy` Skill 与 `/marketing-copy` 命令 — 9 大文体（公众号 / 小红书 / 知乎 / 朋友圈 / 短视频 / 落地页 / EDM / PR 稿 / 客户故事 / Demo 脚本）+ ToB / ToC 双语风 + AI 安全产品专属话术 + 避雷词清单
- **🔧 修复**：补齐 `/product-doc` 命令文件（之前 README/CLAUDE 引用但文件缺失）
- **🗂️ 命令拆分**：新建 `commands/presales/` 目录，从 `commands/product/` 迁出 13 个售前命令（`discovery-call` / `gap-analysis` / `solution-architecture` / `business-case` / `rfp-response` / `security-questionnaire` / `battle-card` / `demo-design` / `poc-plan` / `proposal` / `sales-guide` / `product-doc` / `doc-audit`），保留 36 个 PM 核心命令在 `product/`
- **🧹 产品域裁剪**：删除 3 个不必须 Agent（`data-platform-pm` / `release-manager` / `compliance-officer`）、15 个冗余/过技术/业务不符 Skill（`metagpt` / `rbac-design` / `sla-design` / `integration-design` / `spec-validate` / `ai-feature-spec` / `prd-generator` / `prd-spec` / `proto-prd` / `experiment-log` / `growth-experiment` / `decision-log` / `account-plan` / `cpq-config` / `sync-tasks`）+ 12 个对应命令；修复 5 个 Agent 的断链引用
- **📋 examples/ 目录合并入 templates/**：新增 `pm-discovery-template.md`，升级 `sales-enablement-template.md` 与 `acceptance-checklist-template.md` 为完整填充版，删除 examples/ 目录
- **最终规模**：27 Agents / 88 Skills / 73 Commands（36 product + 13 presales + 8 writing + 11 media + 4 research + 1 hr）/ 15 Templates

### v2.2
- 新增 `diagram-architect` 统一图表编排 Agent（Mermaid/PlantUML/diagrams/Visio 四引擎路由）
- 新增 `arch-diagram` 云架构图技能（AWS/GCP/Azure/K8s/阿里云，基于 mingrammer/diagrams）
- 新增 `visio-builder` Visio 图表技能（python-visio + Visio.NET COM，.vsdx 读写与格式互转）
- 新增 `pdf2video` PDF/PPT 转动态视频技能（stack/focus/zoom/fan 四种场景动画）
- 新增 `omni-captions` 视频字幕生成技能（30+ 格式，Claude 翻译，YouTube 支持）
- 新增 `videocut` AI 视频智能剪辑技能（ASR + Claude 语义分析 + FFmpeg 精准剪切）
- 新增 `content-sync` 内容多平台分发技能（30+ 平台，Wechatsync MCP + PostBot）
- 新增 `ppt-rag` PPT 专用 RAG 索引检索技能（本地文件/URL 向量化，语义检索）
- 新增 `ppt-researcher` PPT 多源内容搜集技能（官方/媒体/学术/产业/社区 5 渠道并行）
- 新增 `ppt-architect` PPT 场景图表构建技能（自动识别图表需求，路由至最优引擎）
- 新增命令：`/arch-diagram`、`/visio`、`/pdf2video`、`/caption`、`/videocut`、`/sync`
- PPT 系统升级为 10 阶段全流程（研究/RAG/归纳/图表/制作/评分迭代），100 分 5 维度质量闭环
- Agent 数量升至 18 个，Skills 升至 49 个，Commands 升至 37 个

### v2.1
- 新增 `gtm-strategist` GTM 全链路战略 Agent
- 新增 `proposal-writer` 企业方案撰写全链路 Agent
- 新增 `visual-suite` 视觉内容全链路 Agent（整合六大视觉技能）
- 新增 `diagram-suite` 完整图表套件（Markmap/PlantUML/Mermaid/MerdiAi 四引擎）
- 新增 `ai-illustrator` AI 智能插图技能（多种艺术风格支持）
- 新增 `md-visual` Markdown 转视觉图像技能（md 转图片/海报/卡片）
- 新增 `table-toolkit` 表格生成与转换工具集
- 新增 `gtm-strategy` GTM 知识库（增长模型/ICP/定位/渠道/定价）
- 新增 `proposal-generator` 企业方案撰写知识库（多行业/三类方案）
- 新增 `sales-guide-writer` B2B 销售赋能知识库（销售一页禅/竞争话术）
- 新增 `product-doc-writer` B2B 产品资料体系（24 类标准文档）
- 新增 `doc-auditor` 产品文档质量审核知识库
- 新增命令：`/diagram`、`/md-visual`、`/table`、`/gtm-strategy`、`/proposal`、`/sales-guide`、`/product-doc`、`/doc-audit`
- Agent 数量升至 17 个，Skills 升至 40 个

### v2.0
- 新增 `product-manager` 全栈 PM Agent，整合 PRD/竞品/用研/分析/路线图/反馈全流程
- 新增 `market-intelligence` 市场情报 Agent
- 新增 `product-enablement` 产品赋能 Agent
- 新增 `style-evolver` 风格自进化 Agent 和 Skill
- 新增 `doc-polisher` 文档润色 + 配图一体化 Agent
- PPT 引擎扩展至 6 种（新增 SlideTailor、PPTX SDK）
- 命令系统扩展至 40+ 个，新增产品管理全套命令

### v1.0
- 初始版本，包含写作、标书、PPT、数据分析、HR 筛选核心能力
- 14 个 Agent，36+ 个 Skill，40+ 个 Command

### v2.x（PM Kit 集成）
- 集成 [pm_claude_code_kit](C:/Users/13141/Desktop/pm_claude_code_kit) 的 PM 全流程能力
- 新增 2 个 Agent：`@product-director`（策略层）、`@qa-acceptance-designer`（验收设计）
- 新增 4 个 Skill：`pm-core-framework`、`pm-full-cycle`、`pm-qa-acceptance`、`pm-ai-security-product`
- 新增 5 个 Command：`/pm-intake`、`/pm-discovery`、`/pm-prd-enterprise`、`/pm-review`、`/pm-sales-pack`
- 首次填充 `templates/` 模板库：8 个标准模板（PRD/BRD/MRD/Roadmap/验收/Release Note/Sales Pack/需求池）
- 重叠能力（PRD 写作、市场研究、用户研究、Roadmap、Release、销售赋能）以「**追加 B 端 / 企业级视角**」方式合并到现有 Skill，避免重复实现

### v2.1（PM 高频缺失补齐）
覆盖 PM 岗位 P0 缺失场景。新增 7 个 Skill + 8 个 Command + 6 个 Template：
- **战略决策**：`/working-backwards`（PR-FAQ + 6-pager）、`/build-vs-buy`、`/sunset`、`/win-loss`、`/churn-analysis`
- **运营协作**：`/tech-debt`（技术债优先级）
- **AI 产品**：`/ai-red-team`（OWASP LLM Top 10 红队测试）
- **模板**：`pr-faq-template.md`、`six-pager-template.md`、`model-card-template.md`、`ai-eval-rubric-template.md`

---

## 来源

本项目集成了以下开源仓库的内容：

### 写作能力
- [article-writer-skills] — 文章写作技能
  - `article-writer` — 公众号长文写作 skill
  - `hv-analysis` — 横纵分析法深度研究 skill

### 产品管理全流程能力
- [pm_claude_code_kit](https://github.com/) — 产品经理智能体工作台（B 端 / 企业级视角）
  - `pm-core-framework`、`pm-full-cycle`、`pm-qa-acceptance`、`pm-ai-security-product` Skills
  - `@product-director`、`@qa-acceptance-designer` Agents
  - `/pm-intake`、`/pm-discovery`、`/pm-prd-enterprise`、`/pm-review`、`/pm-sales-pack` Commands
  - 8 个标准模板（PRD/BRD/MRD/Roadmap/验收清单/Release Note/Sales Pack/需求池）

### PPT 生成能力
- [ppt-master](https://github.com/hugohe3/ppt-master) — AI 驱动的演示文稿生成系统（商务通用）
- [academic-pptx-skill](https://github.com/Gabberflast/academic-pptx-skill) — 学术演讲 PPT，论证优先设计
- [SlideTailor](https://github.com/nusnlp/SlideTailor) — NLP 从论文 PDF 自动生成幻灯片内容
- [Slidev](https://github.com/slidevjs/slidev) — 开发者演示框架（Markdown + Vue，代码高亮动画）
- [Marp](https://github.com/marp-team/marp) — Markdown 快速转换幻灯片（HTML/PDF/PPTX）
- [python-pptx](https://github.com/scanny/python-pptx) — Python PPTX 编程库（编程式批量生成）
- [PptxGenJS](https://github.com/gitbrent/PptxGenJS) — JavaScript PPTX 编程库（API/Web 端生成）
- [frontend-slides](https://github.com/zarazhangrui/frontend-slides) — 前端演示参考风格（集成于 Slidev 主题）

### 数据与可视化工具
- [TaskWeaver](https://github.com/microsoft/TaskWeaver) — 微软代码优先 AI Agent 框架
  - Python 沙箱执行、插件系统、自动错误修复
- [Chat2DB](https://github.com/chat2db/Chat2DB) — AI 数据库助手
  - 自然语言转 SQL、SQL 优化、Schema 理解
- [Stable Diffusion WebUI](https://github.com/AUTOMATIC1111/stable-diffusion-webui) — AI 图像生成
  - 文生图、图生图、风格迁移、批量生成
- [Mermaid](https://github.com/mermaid-js/mermaid) — 文本图表生成
  - 流程图、时序图、甘特图、ER 图、思维导图

感谢以上作者的开源贡献：

- [@hugohe3](https://github.com/hugohe3)
- [@Gabberflast](https://github.com/Gabberflast)
- [@nusnlp](https://github.com/nusnlp)（SlideTailor）
- [@slidevjs](https://github.com/slidevjs)
- [@marp-team](https://github.com/marp-team)
- [@scanny](https://github.com/scanny)（python-pptx）
- [@gitbrent](https://github.com/gitbrent)（PptxGenJS）
- [@zarazhangrui](https://github.com/zarazhangrui)（frontend-slides）
- [@microsoft](https://github.com/microsoft)
- [@chat2db](https://github.com/chat2db)
- [@AUTOMATIC1111](https://github.com/AUTOMATIC1111)
- [@mermaid-js](https://github.com/mermaid-js)
