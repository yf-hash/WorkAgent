# CLAUDE.md

> WorkAgent AI 内容创作平台 | 以风格驱动的 AI 写作基础设施

## 仓库定位

这是 **WorkAgent 风格驱动的 AI 内容创作平台**，支持 Claude Code（完整）、Cursor 和 OpenAI Codex 三种主流 AI 编程/写作工具。

**是什么**：
- 内容创作知识库（Skills + Agents）
- 写作风格学习与迁移系统
- 公众号长文 AI 辅助写作工具

**不是什么**：
- 通用代码开发工具（请使用 DevAgent）
- 特定项目的业务配置
- 个人偏好配置（应放在 `~/.claude/settings.local.json`）

---

## Skill 调用规范

通过独立命令直接调用对应的 skill：

```bash
# 文章风格写作
/article-writer 帮我写一篇关于 Claude Code 的公众号文章

# 横纵分析法深度研究
/hv-analysis 帮我用横纵分析法研究 Hermes Agent

# 访谈写作（Writer-Reviewer 互搏）
/interview-writer 以下是我和张三的访谈记录：[素材]
/interview-writer --target-score 88 --max-rounds 3

# 标书智能编制（七阶段流水线）
/bid full 招标文件.pdf --kb company-docs/          # 一键全流程
/bid analyze 招标.pdf --color --clarify-list        # 深度拆解+三色标记
/bid outline --from 最终技术要求清单.xlsx --with-deviation  # 偏离表+大纲
/bid write --section solution --kb company-docs/ --figures  # 写技术方案
/bid rewrite --file 技术偏离表.docx                 # 偏离表同义改写

# 风格自进化（风格学习 + 迭代创作）
/self-evolve --learn url1,url2 --title "文章标题"            # 完整流程
/self-evolve --learn url1,url2                              # 仅风格学习
/self-evolve --style-card ./style.md --title "文章标题"     # 使用已有风格卡片

# 文本去AI味与文档润色
/humanize article.md --tone casual --intensity high
/polish thesis.pdf --tone academic --intensity max --style business-blue

# 论文研究（搜集 + 解读）
/paper-collect --since 2026-02-01 --topic llm-security,fuzzing --limit 5
/paper-interpret paper.pdf --style professional --length medium

# 简历智能筛选
/screen --jd jd_backend.md ./resumes/ --weights tech --top 5

# Remotion 动态视频生成（三引擎：native/prompt2video/vidosy）
/remotion-generate --template ai-native-company-intro --render
/remotion-generate --engine prompt2video --duration 30 "产品发布宣传片"
/remotion-generate --engine vidosy scenes.json --render

# PDF/PPT 转动态视频
/pdf2video report.pdf --render
/pdf2video presentation.pptx --style tech --scene-type stack --render

# 视频字幕生成
/caption video.mp4 --translate zh --bilingual --format ass
/caption https://youtube.com/watch?v=xxx --translate zh

# AI 视频智能剪辑（去停顿/口误/重复）
/videocut lecture.mp4 --mode review
/videocut podcast.mp4 --mode auto

# 内容多平台分发
/sync article.md --platforms wechat,zhihu,juejin
/sync article.md --platforms wechat,xiaohongshu --mode draft

# PPT 生成（10阶段全流程 / RAG模式 / 6种引擎快速模式）
# === 全流程（从零开始，自动搜索+评分迭代）===
/ppt 人工智能医疗应用前景 --mode full --pages 20 --style mckinsey
/ppt 帮我做一个论文答辩 PPT，主题是"深度学习" --backend academic
# === RAG 模式（有现成材料）===
/ppt Q4业绩汇报 --rag quarterly_report.pdf kpi_data.xlsx --style mckinsey
/ppt AI医疗分析 --rag-dir ./research/ --pages 20
/ppt 政策解读   --rag https://gov.cn/policy.pdf --rag-mode supplement
/ppt 产品发布   --rag spec.pdf user_research.pdf --rag-index proj2025
/ppt --rag-list                                       # 查看已保存索引
# === 引擎快速模式 ===
/ppt 做一个产品介绍 PPT --style google --pages 10
/ppt --backend slidetailor --source paper.pdf --duration 15
/ppt React Hooks 技术分享 --backend slidev
/ppt 把 README.md 转成幻灯片 --backend marp --source README.md
# === 评分与迭代控制 ===
/ppt 年终总结 --mode full --iter auto --score-pass 90
/ppt 年终总结 --mode full --iter 0                    # 跳过迭代直接输出
/ppt 年终总结 --mode full --score-only                # 仅评分，不修改

# 云架构图生成（mingrammer/diagrams）
/arch-diagram 用户→CloudFront→ALB→EC2集群→RDS+ElastiCache --provider aws
/arch-diagram Ingress→Service→Pod(前端/后端/Worker)→PVC --provider k8s
/arch-diagram Pub/Sub→Dataflow→BigQuery→Looker --provider gcp --direction LR
/arch-diagram AWS VPC + Azure AD + 本地数据中心通过 VPN 互联 --provider multi
/arch-diagram 微服务架构：API网关→认证/订单/支付服务→MySQL --mode code

# Visio 图表创建与转换（python-visio / Visio.NET）
/visio 用户注册流程：填写信息→邮箱验证→完善资料→激活 --type flowchart
/visio diagram.mmd --mode convert --from mermaid --output vsdx
/visio arch.puml --mode convert --from plantuml --output svg
/visio network.vsdx --mode export --output png
/visio CEO→CTO,CFO,CMO; CTO→研发总监,架构师 --type org
/illustrate article.md                          # 全自动为文章配图
/illustrate article.md --mode staged            # 阶段模式（每步确认）
/illustrate --mode single --desc "用户登录流程：输入→验证→跳转"
/illustrate --mode single --backend mermaid --type sequence --desc "微服务调用链"
/illustrate --mode single --backend sd --desc "AI协作封面图" --sd-style digital-art

# 数据查询 / SQL / Python 数据分析
/taskweaver 查询最近 30 天销售额超过 1000 的订单
/taskweaver 优化这个慢查询 --mode optimize --db mysql
/taskweaver 分析 sales.csv 按月统计销售额并生成图表
/taskweaver 合并 data/ 目录下所有 Excel 文件 --output combined.csv

# MetaGPT 项目生成
/metagpt 开发一个待办事项 API，FastAPI + SQLite
/metagpt 仅生成 PRD：在线书店系统 --mode prd

# 产品管理全流程
/pm-skills RICE 优先级框架 --mode framework
/pm-skills 产品发布检查清单 --mode checklist

/prd 开发一个 AI 写作助手浏览器插件 --mode full
/prd 新功能 GTM 计划 --mode gtm
/prd 用户注册流程 --mode workflow

/market-research AI 写作工具市场 --mode competitive
/market-research 中国 SaaS 趋势 --mode trend --output report
/market-research 降噪耳机亚马逊选品 --mode amazon

/user-research 验证用户是否愿意为 AI 写作工具付费
/user-research 新用户引导流程体验 --mode journey
/user-research 信息架构卡片分类 --mode card-sort

/analytics SaaS 产品指标体系设计 --mode metrics
/analytics 用户注册漏斗分析 --mode funnel
/analytics 设计埋点方案 --mode event --platform posthog

/feedback 分析 feedback.csv 用户反馈 --source feedback.csv
/feedback 设计月度 NPS 调查 --mode nps
/feedback 生成 Q1 用户之声报告 --mode voc

/roadmap Q2 产品路线图规划 --horizon 3m
/roadmap 需求优先级排序 --mode prioritize
/roadmap 生成 Gantt 图 --mode gantt

/design-proto 设计 SaaS 仪表盘线框图 --mode wireframe
/design-proto 新用户引导方案 --mode onboarding
/design-proto 按钮点击动效 --mode motion
```

---

## 配置概览

| 类型 | 位置 | 说明 |
|------|------|------|
| Agents | `agents/` | 自治代理，编排写作全流程 |
| Skills | `skills/` | 自动激活的写作知识库 |
| Commands | `commands/` | 统一命令入口（智能路由） |
| Hooks | `hooks/` | Claude Code 生命周期钩子（安全 + 质量检查）|
| Settings | `.claude/settings.json` | 权限配置 |
| Cursor Rules | `.cursor/rules/` | Cursor 写作规范规则 |

> Skills 完整列表见 README.md。

---

## 编辑器优先级

**Claude Code > Cursor > Codex**

- 必须优先保证 Claude Code 的体验
- 其次保证 Cursor 的体验
- 再次保证 Codex 的体验

---

## 在此仓库工作的规则

### 配置原则

1. **风格驱动**：所有写作输出以用户/角色风格为第一优先级
2. **Frontmatter 规范**：Skills 和 Agents 文件必须包含正确的 YAML frontmatter
3. **活人感优先**：任何写作任务输出必须避免 AI 套话，保持真实语感
4. **文档同步**：Skills 内容变更必须同步更新 README.md

### Frontmatter 规范

**Skills** (`skills/*/SKILL.md`) 必须包含：

```yaml
---
name: skill-name           # 英文标识（小写横杠）
description: >             # 详细描述，包含触发关键词（≤1024字符）
  ...
user-invocable: true|false # 是否在 / 菜单显示
effort: low|medium|high    # 任务复杂度
argument-hint: "[args]"    # 参数提示（可选）
---
```

**Agents** (`agents/*.md`) 必须包含：

```yaml
---
name: agent-name           # 英文标识
description: 简述          # ≤200字符
model: sonnet|opus|haiku   # 推荐模型
tools: Read, Write, ...    # 工具清单
skills: [skill-name]       # 调用的 Skills
memory: project            # 记忆范围
effort: high               # 复杂度标记
color: blue|yellow|green   # 语义颜色
---
```

### 内容质量标准

所有写作输出必须通过「四层自检」：

| 层次 | 检查项 | 标准 |
|------|--------|------|
| **活人感** | 是否有真实的人在说话 | 无 AI 套话，有个人立场 |
| **情感** | 是否打动读者 | 有温度，不说教 |
| **信息** | 是否有干货 | 有见识，不废话 |
| **结构** | 是否好读 | 段落节奏流畅 |

---

## 组件说明

### Agents

| Agent | 职责 | 调用时机 |
|-------|------|---------|
| `product-manager` | 全栈产品经理（PRD/竞品/用研/分析/路线图/反馈全流程） | 产品决策、需求文档、产品策略时 |
| `market-intelligence` | 市场情报分析（竞品监测/TAM/趋势/选品/OSS生态） | 竞品分析、市场研究、选品研究时 |
| `bid-writer` | 标书全流程编制（七阶段：拆解→澄清→大纲→撰写→评审→核查→移交） | 标书/投标/招标文件编制时 |
| `content-director` | 全流程内容创作编排 | 需要完整写作流程时 |
| `writer-reviewer` | Writer-Reviewer 互搏 + 知识库进化 | 访谈写作迭代优化时 |
| `style-evolver` | 风格学习 → 风格卡片确认 → Writer-Reviewer 迭代创作 | 风格迁移、参考文章仿写、内容自进化时 |
| `doc-polisher` | 文档智能润色（AI去痕 + 智能配图全自动闭环） | 文档润色、去AI味+配图一体化时 |
| `talent-screener` | 简历智能筛选（JD匹配、六维评分、候选人排名） | 招聘初筛、简历批量筛选时 |
| `paper-researcher` | 论文研究（arXiv搜集 + 单篇深度解读） | 论文情报跟踪、学术科普写作时 |
| `video-maker` | 视频生成代理 — 三引擎路由（native/prompt2video/vidosy）+ PDF转视频 + 字幕 + TTS + MP4渲染 | 视频生成、文档转视频、口播剪辑时 |
| `ppt-generator` | PPT 全流程编排：10阶段流水线（研究/RAG/图表/制作/评分迭代）+ 6种引擎路由 + 100分5维度质量闭环 | PPT 生成任务时 |
| `data-analyst` | 综合 TaskWeaver + Chat2DB 的数据分析 Agent | 数据查询、分析、报表生成时 |
| `visual-creator` | 文章配图 Agent — HTML图表（ASCII→HTML→截图）+ Mermaid + Stable Diffusion 三合一 | 配图/图表/视觉内容时 |
| `diagram-architect` | 统一图表编排 Agent，自动路由至 Mermaid/PlantUML/diagrams/Visio 最优引擎，支持批量生成和格式互转 | 图表类型不确定、需要多图表套件、格式互转时 |

### Skills

| Skill | 描述 | 触发方式 |
|-------|------|---------|
| `article-writer` | 文章风格公众号长文写作（4000-8000字） | 对话触发 或 `/article-writer` |
| `hv-analysis` | 横纵分析法深度研究，输出 PDF 报告（10000-30000字） | 对话触发 或 `/hv-analysis` |
| `interview-writer` | 访谈写作 v2.0，Writer-Reviewer 互搏 + 知识库进化 | 对话触发 或 `/interview-writer` |
| `ppt-master` | 通用 PPT 生成，支持多种设计风格和图片生成 | `/ppt` 命令调用 |
| `academic-pptx` | 学术演讲 PPT 生成，论证优先设计 | `/ppt` 命令调用 |
| `slidetailor` | 论文PDF → 学术幻灯片，NLP自动提取内容 | `/ppt --backend slidetailor` |
| `slidev` | 开发者/技术演示，Markdown+Vue，代码高亮动画 | `/ppt --backend slidev` |
| `marp` | Markdown快速出片，输出HTML/PDF/PPTX | `/ppt --backend marp` |
| `pptx-sdk` | 编程式PPTX生成（python-pptx + PptxGenJS） | `/ppt --backend sdk` |
| `ppt-rag` | PPT专用RAG索引检索：本地文件/URL向量化，语义检索合成素材包 | `/ppt --rag` 自动调用 |
| `ppt-researcher` | PPT多源内容搜集：官方/媒体/学术/产业/社区5渠道并行搜索 | `/ppt --mode full` 自动调用 |
| `ppt-architect` | PPT场景图表构建：自动识别图表需求，路由至Mermaid/PlantUML/diagrams | `/ppt` Phase 4 自动调用 |
| `mermaid-chart` | Mermaid 图表生成（流程图/时序图/甘特图/ER图等） | `/illustrate --backend mermaid` |
| `arch-diagram` | 云架构图生成（AWS/GCP/Azure/K8s/阿里云），基于 mingrammer/diagrams | `/arch-diagram` 命令调用 |
| `visio-builder` | Visio 图表创建与转换（python-visio / Visio.NET COM），支持 .vsdx 读写和格式互转 | `/visio` 命令调用 |
| `stable-diffusion` | AI 图像生成，文生图/图生图（需本地 SD WebUI） | `/illustrate --backend sd` |
| `html-chart` | HTML图表生成器，ASCII草图→HTML→Playwright截图，4种风格 | `/illustrate`（主管道） |
| `chat2db` | 自然语言转 SQL，支持 MySQL/PostgreSQL 等主流数据库 | 对话触发 或 `/taskweaver --backend sql` |
| `taskweaver` | 代码优先 Agent，Python 沙箱执行数据分析和自动化任务 | 对话触发 或 `/taskweaver` |
| `style-evolver` | 风格驱动内容自进化，从参考文章提炼风格卡片，Writer-Reviewer 迭代创作 | 对话触发 或 `/self-evolve` |
| `bid-writer` | 标书七阶段编制知识库（三色标记/偏离表规范/RAG写作/双轮评审/合规核查） | `/bid` 命令调用 |
| `bid-rewriter` | 偏离表"无偏离"应答项五原则同义改写 | `/bid rewrite` 调用 |
| `humanizer` | AI 文本人性化改写（40+ 痕迹检测，五维评分，中文排版规范自动校正） | `/humanize` 命令调用 |
| `doc-polisher` | 文档智能润色闭环（读取→去痕→排版校正→配图→输出，支持 DOCX 导出） | `/polish` 命令调用 |
| `paper-collector` | arXiv 安全论文搜集与中文摘要生成 | `/paper-collect` 命令调用 |
| `paper-interpreter` | 论文 PDF 深度解读（4000-6000字公众号长文） | `/paper-interpret` 命令调用 |
| `resume-screener` | 简历智能筛选（JD匹配、硬过滤、六维评分） | `/screen` 命令调用 |
| `remotion-generator` | Remotion 视频生成（三引擎：native模板/prompt2video全链路/vidosy场景配置） | `/remotion-generate` 命令调用 |
| `pdf2video` | PDF/PPT 转动态视频（stack/focus/zoom/fan 四种场景动画） | `/pdf2video` 命令调用 |
| `omni-captions` | 视频字幕生成（转录/翻译/双语/30+格式，Claude翻译无需额外API） | `/caption` 命令调用 |
| `videocut` | AI 视频智能剪辑（去停顿/重复/口误，ASR+Claude语义分析+FFmpeg剪切） | `/videocut` 命令调用 |
| `content-sync` | 内容多平台分发（30+平台一键同步，Wechatsync MCP + PostBot） | `/sync` 命令调用 |
| `metagpt` | 多 Agent 软件公司模拟，PRD→架构→代码→测试全流程 | 对话触发 或 `/metagpt` |
| `pm-skills` | 产品经理技能库（JTBD/RICE/OKR/PMF/发布清单/用户故事地图等） | 对话触发 或 `/pm-skills` |
| `prd-generator` | AI PRD 生成（lite/full/gtm/workflow 四种模式） | `/prd` 命令调用 |
| `market-research` | 市场研究与竞争情报（竞品/趋势/TAM/亚马逊/OSS生态/品牌战略/营销分析框架） | `/market-research` 或 `/user-research` 命令调用 |
| `product-analytics` | 产品数据分析（指标体系/漏斗/留存/埋点/PostHog/Matomo） | `/analytics` 命令调用 |
| `user-feedback` | 用户反馈管理（NPS/CSAT/功能投票/VoC 报告/情感分析） | `/feedback` 命令调用 |
| `product-roadmap` | 路线图规划（RICE/MoSCoW/Gantt/GitHub Projects/OKR） | `/roadmap` 命令调用 |
| `design-proto` | 产品设计与原型（线框图/Penpot/Framer Motion/Onboarding） | `/design-proto` 命令调用 |

### Commands

| Command | 描述 | 位置 |
|---------|------|------|
| `/article-writer` | 文章风格公众号长文写作（4000-8000字） | `commands/writing/article-writer.md` |
| `/hv-analysis` | 横纵分析法深度研究，输出 PDF 报告（10000-30000字） | `commands/hv-analysis.md` |
| `/interview-writer` | 访谈写作 Writer-Reviewer 互搏流程 | `commands/interview-writer.md` |
| `/ppt` | PPT 10阶段全流程（主题→研究/RAG→归纳→图表→制作→评分迭代→输出）+ 6种引擎快速路由 + 100分质量闭环 | `commands/media/ppt.md` |
| `/illustrate` | 文章配图生成 — ASCII→HTML→截图 / Mermaid / Stable Diffusion 三合一 | `commands/illustrate.md` |
| `/diagram` | 多引擎图表生成（Markmap/PlantUML/Mermaid/diagrams/Visio 六引擎路由） | `commands/media/diagram.md` |
| `/arch-diagram` | 云架构图生成（AWS/GCP/Azure/K8s/阿里云），基于 mingrammer/diagrams | `commands/media/arch-diagram.md` |
| `/visio` | Visio 图表创建与转换（python-visio / Visio.NET），支持 .vsdx 读写和格式互转 | `commands/media/visio.md` |
| `/taskweaver` | 数据分析 Agent — 自然语言转 SQL（Chat2DB）+ Python 代码执行，联合数据库查询与文件分析 | `commands/taskweaver.md` |
| `/bid` | 标书智能编制（七阶段流水线：analyze/clarify/outline/write/review/check/export/rewrite） | `commands/bid.md` |
| `/self-evolve` | 内容自进化 — 风格学习 + Writer-Reviewer 迭代创作（支持风格卡片复用） | `commands/self-evolve.md` |
| `/humanize` | AI 文本人性化改写（识别 40+ 种痕迹，五维度评分） | `commands/humanize.md` |
| `/polish` | 文档智能润色（AI去痕 + 中文排版校正 + 智能配图，支持 DOCX 导出） | `commands/polish.md` |
| `/paper-collect` | arXiv 安全论文搜集（按时间范围和主题批量检索，中文摘要输出） | `commands/paper-collect.md` |
| `/paper-interpret` | 论文深度解读（PDF → 4000-6000字公众号长文） | `commands/paper-interpret.md` |
| `/screen` | 简历智能筛选（JD匹配、六维评分、候选人排名） | `commands/screen.md` |
| `/remotion-generate` | Remotion 视频生成（三引擎：native模板/prompt2video全链路/vidosy场景配置） | `commands/media/remotion-generate.md` |
| `/pdf2video` | PDF/PPT 文档转动态视频（四种场景动画，直接渲染 MP4） | `commands/media/pdf2video.md` |
| `/caption` | 视频字幕生成（转录+翻译+双语，30+格式，YouTube支持） | `commands/media/caption.md` |
| `/videocut` | AI 视频智能剪辑（去停顿/口误/重复，人工审核模式） | `commands/media/videocut.md` |
| `/sync` | 内容多平台一键分发（30+平台，草稿/直接发布） | `commands/writing/sync.md` |
| `/metagpt` | 多 Agent 软件项目生成（PRD→架构→代码→测试） | `commands/metagpt.md` |
| `/pm-skills` | 产品经理技能库查询（框架/模板/案例/辅导/清单） | `commands/product/pm-skills.md` |
| `/prd` | PRD 生成（lite/full/gtm/workflow 四种模式） | `commands/product/prd.md` |
| `/market-research` | 竞争情报 & 市场研究（竞品/趋势/TAM/亚马逊/OSS） | `commands/product/market-research.md` |
| `/user-research` | 用户研究（访谈/问卷/卡片分类/旅程/画像） | `commands/product/user-research.md` |
| `/analytics` | 产品数据分析（指标/漏斗/留存/埋点/看板） | `commands/product/analytics.md` |
| `/feedback` | 用户反馈管理（NPS/分析/功能投票/VoC 报告） | `commands/product/feedback.md` |
| `/roadmap` | 产品路线图规划（优先级/里程碑/Gantt/OKR） | `commands/product/roadmap.md` |
| `/design-proto` | 设计与原型工具台（线框图/引导/动效/Penpot） | `commands/product/design-proto.md` |

### Hooks

| Hook | 事件 | 用途 |
|------|------|------|
| `dangerous-command-blocker.js` | PreToolUse(Bash) | 拦截危险 Shell 命令 |
| TaskCompleted Prompt | TaskCompleted | 内容质量轻量检查 |
