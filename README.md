# WorkAgent

> 以 Claude Code 为入口，通过自然语言 command 调用适配的 Agent 和 Skill，完成前场需求的工作智能体，满足产品、市场、HR、设计等不同用户的场景需求。

WorkAgent 是面向产品、市场、HR、售前等用户的工作智能体，核心理念是：**通过 WorkAgent，让工作效率指数级提升**。

---

## 项目概述

WorkAgent 是一套以 **风格驱动** 为核心设计理念的 AI 原生工作平台。它不是通用代码工具，而是专为前场业务人员打造的智能工作系统：

- **内容创作**：公众号长文、访谈稿、深度研究报告、文档润色
- **产品管理**：PRD 生成、竞品分析、用户研究、数据分析、路线图规划
- **标书编制**：七阶段全流程标书智能编制，三色标记 + RAG 增强写作
- **演示制作**：6 种 PPT 引擎自动路由，学术/商务/开发者场景全覆盖
- **数据分析**：自然语言转 SQL + Python 沙箱执行，联合数据库与文件分析
- **HR 招聘**：简历智能筛选，JD 匹配 + 六维评分 + 候选人排名
- **视频生成**：Remotion 动态视频，模板/字幕/TTS/MP4 渲染全流程

**支持编辑器**：Claude Code（完整支持）> Cursor > OpenAI Codex

---

## 核心内容

| 模块 | 数量 | 说明 |
|------|------|------|
| Agents | 17 个 | 自治代理，编排完整业务流程 |
| Skills | 40 个 | 可复用知识库，自动激活或命令调用 |
| Commands | 31 个（50+ 调用模式） | 统一命令入口，智能路由到对应 Skill/Agent |

**设计原则**：
- **风格驱动**：所有写作输出以用户/角色风格为第一优先级，避免 AI 套话
- **人机协同**：关键节点设置人工确认，标书/内容创作均有阶段性检查点
- **多引擎路由**：PPT、配图、数据分析等场景支持多种后端引擎自动选择
- **质量四层自检**：活人感 → 情感 → 信息 → 结构，逐层验证输出质量

---

## 项目结构

```
WorkAgent/
├── agents/          # 17 个自治代理（编排完整业务流程）
├── skills/          # 40 个可复用知识库
├── commands/        # 31 个统一命令入口（50+ 调用模式）
│   ├── writing/     # 写作类命令（article-writer/bid/humanize/interview-writer/polish/self-evolve）
│   ├── product/     # 产品管理类命令（prd/market-research/analytics/roadmap/gtm-strategy 等）
│   ├── research/    # 研究分析类命令（hv-analysis/paper-collect/paper-interpret/taskweaver）
│   ├── media/       # 媒体生成类命令（ppt/illustrate/diagram/md-visual/table/remotion-generate）
│   └── hr/          # HR 招聘类命令（screen）
├── hooks/           # Claude Code 生命周期钩子（安全拦截 + 质量检查）
├── .claude/
│   └── settings.json    # Claude Code 权限配置
├── .cursor/
│   └── rules/           # Cursor 写作规范规则
├── CLAUDE.md            # Claude Code 完整使用指南
├── AGENTS.md            # Codex/OpenCode 兼容指南
└── README.md
```

---

## 智能体系统

17 个自治 Agent，覆盖产品、内容、标书、数据、研究、HR、媒体、GTM、方案、视觉全域：

| Agent | 职责 | 调用时机 |
|-------|------|---------|
| `product-manager` | 全栈产品经理（PRD/竞品/用研/分析/路线图/反馈全流程） | 产品决策、需求文档、产品策略 |
| `market-intelligence` | 市场情报分析（竞品监测/TAM/趋势/选品/OSS 生态） | 竞品分析、市场研究、选品研究 |
| `bid-writer` | 标书全流程编制（七阶段：拆解→澄清→大纲→撰写→评审→核查→移交） | 标书/投标/招标文件编制 |
| `content-director` | 全流程内容创作编排（风格分析→框架→写作→QA→迭代） | 需要完整写作流程 |
| `writer-reviewer` | Writer-Reviewer 互搏 + 知识库进化 | 访谈写作迭代优化 |
| `style-evolver` | 风格学习 → 风格卡片确认 → Writer-Reviewer 迭代创作 | 风格迁移、参考文章仿写 |
| `doc-polisher` | 文档智能润色（AI 去痕 + 智能配图全自动闭环） | 文档润色、去 AI 味 + 配图一体化 |
| `talent-screener` | 简历智能筛选（JD 匹配、六维评分、候选人排名） | 招聘初筛、简历批量筛选 |
| `paper-researcher` | 论文研究（arXiv 搜集 + 单篇深度解读） | 论文情报跟踪、学术科普写作 |
| `video-maker` | Remotion 视频生成（模板/字幕/TTS/渲染） | 企业介绍视频、产品演示视频 |
| `ppt-generator` | PPT 生成协调，6 种引擎路由（academic/slidetailor/ppt-master/slidev/marp/sdk） | PPT 生成任务 |
| `data-analyst` | 综合 TaskWeaver + Chat2DB 的数据分析 Agent | 数据查询、分析、报表生成 |
| `visual-creator` | 文章配图 Agent — HTML 图表 + Mermaid + Stable Diffusion 三合一 | 配图/图表/视觉内容生成 |
| `product-enablement` | 产品赋能工作流（销售指南/文档审计/产品文档） | 产品赋能、销售支持 |
| `gtm-strategist` | GTM 全链路战略 Agent（增长模型/ICP/定位/渠道/定价/90天计划） | 新产品上市规划、GTM 诊断与优化 |
| `proposal-writer` | 企业方案撰写全链路 Agent（售前方案/可研报告/初步设计，多行业定制） | 售前解决方案、项目建议书 |
| `visual-suite` | 视觉内容全链路 Agent（配图/思维导图/UML/Markdown 海报/表格可视化） | 文章配图、图表、MD 转图片 |

---

## Skill 系统

40 个可复用知识库，支持对话触发或命令调用：

### 写作与内容

| Skill | 描述 | 触发方式 |
|-------|------|---------|
| `article-writer` | 文章风格公众号长文写作（4000-8000 字） | 对话触发 或 `/article-writer` |
| `hv-analysis` | 横纵分析法深度研究，输出 PDF 报告（10000-30000 字） | 对话触发 或 `/hv-analysis` |
| `interview-writer` | 访谈写作 v2.0，Writer-Reviewer 互搏 + 知识库进化 | 对话触发 或 `/interview-writer` |
| `style-evolver` | 风格驱动内容自进化，从参考文章提炼风格卡片，迭代创作 | 对话触发 或 `/self-evolve` |
| `humanizer` | AI 文本人性化改写（40+ 痕迹检测，五维评分） | `/humanize` 命令调用 |
| `doc-polisher` | 文档智能润色闭环（读取→去痕→配图→输出） | `/polish` 命令调用 |
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
| `prd-generator` | AI PRD 生成（lite/full/gtm/workflow 四种模式） | `/prd` 命令调用 |
| `market-research` | 市场研究与竞争情报（竞品/趋势/TAM/亚马逊选品/OSS 生态） | `/market-research` 命令调用 |
| `product-analytics` | 产品数据分析（指标体系/漏斗/留存/埋点/PostHog/Matomo） | `/analytics` 命令调用 |
| `user-feedback` | 用户反馈管理（NPS/CSAT/功能投票/VoC 报告/情感分析） | `/feedback` 命令调用 |
| `product-roadmap` | 路线图规划（RICE/MoSCoW/Gantt/GitHub Projects/OKR） | `/roadmap` 命令调用 |
| `design-proto` | 产品设计与原型（线框图/Penpot/Framer Motion/Onboarding） | `/design-proto` 命令调用 |

### 数据与研究

| Skill | 描述 | 触发方式 |
|-------|------|---------|
| `taskweaver` | 代码优先 Agent，Python 沙箱执行数据分析和自动化任务 | 对话触发 或 `/taskweaver` |
| `chat2db` | 自然语言转 SQL，支持 MySQL/PostgreSQL 等主流数据库 | 对话触发 或 `/taskweaver --backend sql` |
| `paper-collector` | arXiv 安全论文搜集与中文摘要生成 | `/paper-collect` 命令调用 |
| `paper-interpreter` | 论文 PDF 深度解读（4000-6000 字公众号长文） | `/paper-interpret` 命令调用 |
| `metagpt` | 多 Agent 软件公司模拟，PRD→架构→代码→测试全流程 | 对话触发 或 `/metagpt` |

### HR 与媒体

| Skill | 描述 | 触发方式 |
|-------|------|---------|
| `resume-screener` | 简历智能筛选（JD 匹配、硬过滤、六维评分） | `/screen` 命令调用 |
| `remotion-generator` | Remotion 动态视频生成（模板/字幕/TTS/渲染） | `/remotion-generate` 命令调用 |

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
| `ai-illustrator` | AI 智能插图生成（文章配图/学术图表/文档插图/创意画布，支持多种艺术风格） | 对话触发 |
| `md-visual` | Markdown 转视觉图像（md 转图片/海报/卡片，整合 mark-pic/Madopic/tablesnap） | `/md-visual` 命令调用 |
| `table-toolkit` | 表格生成与转换工具集（文本/CSV/自然语言转 Markdown 表格，多工具链整合） | `/table` 命令调用 |

---

## 命令系统

31 个统一命令入口，按场景分类：

### 写作类

```bash
/article-writer 帮我写一篇关于 Claude Code 的公众号文章
/hv-analysis 帮我用横纵分析法研究 Hermes Agent
/interview-writer 以下是我和张三的访谈记录：[素材]
/self-evolve --learn url1,url2 --title "文章标题"
/humanize article.md --tone casual --intensity high
/polish thesis.pdf --tone academic --intensity max
/bid full 招标文件.pdf --kb company-docs/
/bid analyze 招标.pdf --color --clarify-list
/bid write --section solution --kb company-docs/ --figures
/bid rewrite --file 技术偏离表.docx
```

### 产品管理类

```bash
/prd 开发一个 AI 写作助手浏览器插件 --mode full
/prd 新功能 GTM 计划 --mode gtm
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
/proposal 智慧城市交通系统 --type feasibility --industry gov
/proposal 企业私有化部署方案 --type presale --industry finance
/sales-guide 数据安全产品 --mode full --industry fintech
/product-doc AI 客服平台 --type whitepaper --industry saas
/doc-audit ./product-docs/ --mode fullset --strict
```

### 研究与数据类

```bash
/paper-collect --since 2026-02-01 --topic llm-security,fuzzing --limit 5
/paper-interpret paper.pdf --style professional --length medium
/taskweaver 查询最近 30 天销售额超过 1000 的订单
/taskweaver 分析 sales.csv 按月统计销售额并生成图表
/taskweaver 合并 data/ 目录下所有 Excel 文件 --output combined.csv
/metagpt 开发一个待办事项 API，FastAPI + SQLite
```

### 媒体生成类

```bash
/ppt 帮我做一个论文答辩 PPT，主题是"深度学习"
/ppt 做一个产品介绍 PPT --style google --pages 10
/ppt --backend slidetailor --source paper.pdf --duration 15
/ppt React Hooks 技术分享 --backend slidev
/illustrate article.md
/illustrate --mode single --backend mermaid --type sequence --desc "微服务调用链"
/illustrate --mode single --backend sd --desc "AI 协作封面图" --sd-style digital-art
/remotion-generate --template ai-native-company-intro --render
/diagram "用户注册流程" --engine markmap --type mindmap
/diagram --engine plantuml --type sequence --desc "微服务调用链"
/md-visual article.md --type poster --theme gradient
/table "姓名、年龄、城市\n张三、28、北京" --from text --to md
```

### HR 类

```bash
/screen --jd jd_backend.md ./resumes/ --weights tech --top 5
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
/prd 开发 AI 写作助手浏览器插件 --mode full        # 完整 PRD
/market-research AI 写作工具市场 --mode competitive  # 竞品分析
/analytics 用户注册漏斗分析 --mode funnel            # 数据分析
/roadmap Q2 路线图规划 --horizon 3m                  # 路线图
/feedback 生成 Q1 用户之声报告 --mode voc            # 用户反馈
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
# 写一篇公众号文章
/article-writer 帮我写一篇关于 AI 工具提效的文章

# 生成一份 PRD
/prd 开发一个团队协作工具 --mode lite

# 做一个 PPT
/ppt 产品季度汇报 --style business --pages 10

# GTM 上市策略
/gtm-strategy 新产品上市规划 --mode fullplan

# 企业方案文档
/proposal 云计算解决方案 --type presale --industry fintech

# 生成思维导图
/diagram "产品设计流程" --engine markmap --type mindmap
```

**4. 查看完整命令列表**

参考 `CLAUDE.md` 获取所有命令的完整参数说明和使用示例。

---

## 更新日志

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

---

## 来源

本项目集成了以下开源仓库的内容：

### 写作能力
- [article-writer-skills] — 文章写作技能
  - `article-writer` — 公众号长文写作 skill
  - `hv-analysis` — 横纵分析法深度研究 skill

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
- [MetaGPT](https://github.com/geekan/MetaGPT) — 多 Agent 软件公司模拟
  - PM→Architect→Engineer→QA 全流程项目生成
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
- [@geekan](https://github.com/geekan)
- [@chat2db](https://github.com/chat2db)
- [@AUTOMATIC1111](https://github.com/AUTOMATIC1111)
- [@mermaid-js](https://github.com/mermaid-js)
