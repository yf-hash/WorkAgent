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

# 产品经理全流程
/pm-skills RICE 优先级框架 --mode framework
/pm-skills 产品发布检查清单 --mode checklist

# === PM 全流程（pm_claude_code_kit 集成）===
/pm-intake "客户工单：审批流跑不通，老板要求 4 周上线"   # 任务类型判断 + 缺口标注
/pm-discovery "AI 安全 SOC 智能体的市场切入"             # 发现阶段一次性产出
/pm-prd-enterprise "多租户 RBAC 后台"                   # 企业级 PRD 严格 12 章模板
/pm-review "PRD-2026-Q2-审批流.md"                      # PM 视角 10 维度评审
/pm-sales-pack "AI 渗透测试智能体 / 央企客户"            # 销售赋能一次性出包

/product-spec 开发一个 AI 写作助手浏览器插件 --mode prd
/product-spec 新功能 GTM 计划 --mode prd --prd-mode gtm
/product-spec 用户注册流程 --mode prd --prd-mode workflow

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

# 战略层 / 用户故事 / MVP / PMF
/product-strategy AI 写作助手 --mode lean
/product-strategy 企业知识库 --mode bmc --biz b2b
/product-strategy 智能客服 --mode vision --output deck
/product-strategy 工具型 SaaS --mode northstar
/user-story-mapping 电商商品搜索改版
/user-story-mapping AI 写作助手新用户引导 --mode skeleton
/mvp-canvas AI 写作助手浏览器插件
/mvp-canvas B2B 数据分析 --mode fullset --budget mid --timebox 4w
/pmf-survey AI 写作助手
/pmf-survey AI 写作助手 --mode signals

# 实验 / 增长 / 定价
/ab-test 注册按钮文案改版 --mode design
/ab-test 引导流程改版 --mode fullset --mde 0.03
/pricing-strategy AI 写作助手 SaaS --mode tier
/pricing-strategy AI 写作助手 --mode psm
/pricing-strategy 企业版重设计 --mode fullset

# 发布
/launch-checklist AI 写作助手 v2 --mode full
/launch-checklist 重大改版 --launch-type hard --scale large

# AI 安全产品 / 报告
# AI 安全产品方法论触发：在对话中描述场景即可激活 pm-ai-security-product Skill
/product-report W42 2026 --mode weekly
/product-report 2026-05 月报 --mode monthly --audience exec
/product-report Q1 2026 --mode quarterly

# 战略决策 / 沟通 / AI 红队
/working-backwards "新功能想法" --mode pr-faq
/build-vs-buy "自研 vs 用 Auth0"
/sunset "Legacy Feature X"
/win-loss --quarter Q2
/churn-analysis --quarter Q2
/tech-debt --quarter Q2
/ai-red-team "v2.0 模型"

# 数据看板
/data-dashboard 北极星看板 --mode design --platform posthog
/data-dashboard AI 客服监控 --type ai-monitor --mode fullset
```

---

## 配置概览

| 类型 | 位置 | 说明 |
|------|------|------|
| Agents | `agents/` | 自治代理，编排写作全流程 |
| Skills | `skills/` | 自动激活的写作知识库 |
| Commands | `commands/` | 统一命令入口（智能路由） |
| Templates | `templates/` | 标准模板库（PRD / BRD / MRD / Roadmap / 验收 / Release Note / Sales Pack / 需求池 / PM Discovery）|
| Hooks | `hooks/` | Claude Code 生命周期钩子（安全 + 质量检查）|
| Settings | `.claude/settings.json` | 权限配置 |
| Cursor Rules | `.cursor/rules/` | Cursor 写作规范规则 |
| Health Report | `HEALTH_REPORT.md` | 仓库整体健康度 + 修复记录 |

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
| `solution-architect` | **售前解决方案总指挥** — 统筹客户拜访 / Gap / 方案 / Business Case / RFP / Demo / 竞品 / PoC / 售前物料全链路 | 售前 SE / SA 工作场景，赢单导向 |
| `product-director` | 产品总监 — 复杂跨部门产品任务的策略层（拆任务/分工/取舍/把关），与 product-manager 互补 | 复杂立项、跨团队大功能、CEO 项目、客户战略级方案、需要总监级评审时 |
| `prd-coach` | PRD 对话教练 — 三镜诊断（用户/商业/技术）+ 两阶段交付（概念稿→实现稿），对话式引导写出可开发 PRD | 想法模糊、非 PM 用户、需要引导式写 PRD 时 |
| `qa-acceptance-designer` | 测试验收设计 — PRD → 验收方案（功能/权限/异常/数据/审计/客户口径），输出上线阻断项 | PRD/版本验收材料编制、UAT 设计、上线 Go/No-Go 前验收阻断项确认时 |
| `ai-product-architect` | AI 产品架构师 — 专注 LLM/Agent/RAG 类功能的规格、Prompt、Eval、失败模式管理，套用 pm-ai-security-product 方法论 | 设计 AI 功能、Prompt 工程交付、AI 功能上线评审时 |
| `growth-strategist` | 增长战略 — 统筹 PMF / 漏斗诊断 / A/B 实验 / 定价的全栈增长经理 | PMF 验证、增长瓶颈诊断、实验设计、定价优化时 |
| `research-analyst` | 综合研究分析师 — 用户研究 + 市场情报 + 反馈分析 + PMF 验证 | 早期 0→1 探索、立项验证、PMF 测量、综合研究方法选型时 |
| `gtm-strategist` | GTM 全链路战略（增长模型/ICP/定位/渠道/定价/90天计划） | 制定上市战略、渠道规划、ICP 设计时 |
| `proposal-writer` | 售前方案 / 可研报告 / 投标技术方案撰写 | 项目型客户响应方案、投标技术文档时 |
| `product-enablement` | 产品赋能（销售指南 / 文档审计 / 产品文档体系） | 销售物料、产品手册、销售支持时 |
| `market-intelligence` | 市场情报分析（竞品监测/TAM/趋势/选品/OSS生态） | 深度竞品分析、市场研究、选品研究时 |
| `bid-writer` | 标书全流程编制（七阶段：拆解→澄清→大纲→撰写→评审→核查→移交） | 标书/投标/招标文件编制时 |
| `content-director` | 全流程内容创作编排 | 需要完整写作流程时 |
| `writer-reviewer` | Writer-Reviewer 互搏 + 知识库进化 | 访谈写作迭代优化时 |
| `style-evolver` | 风格学习 → 风格卡片确认 → Writer-Reviewer 迭代创作 | 风格迁移、参考文章仿写、内容自进化时 |
| `doc-polisher` | 文档智能润色（AI去痕 + 智能配图全自动闭环） | 文档润色、去AI味+配图一体化时 |
| `paper-researcher` | 论文研究（arXiv搜集 + 单篇深度解读） | 论文情报跟踪、学术科普写作时 |
| `video-maker` | 视频生成 — 三引擎路由（native/prompt2video/vidosy）+ PDF转视频 + 字幕 + TTS + MP4渲染 | 视频生成、文档转视频、口播剪辑时 |
| `ppt-generator` | PPT 全流程编排：10阶段流水线 + 6种引擎路由 + 100分5维度质量闭环 | PPT 生成任务时 |
| `data-analyst` | 综合 TaskWeaver + Chat2DB 的数据分析 Agent | 数据查询、分析、报表生成时 |
| `article-illustrator` | 文章内联配图 — HTML图表 + Mermaid + Stable Diffusion 三合一，专为 .md 文章批量配图 | 为文章批量自动配图时 |
| `visual-suite` | 视觉内容全链路（配图/思维导图/UML/Markdown 海报/表格可视化） | 文章配图、图表、MD 转图片时 |
| `visual-creator` | 视觉创作（已弃用 → 用 article-illustrator） | 历史兼容 |
| `diagram-architect` | 统一图表编排，自动路由至 Mermaid/PlantUML/diagrams/Visio 最优引擎，支持批量生成和格式互转 | 图表类型不确定、需要多图表套件、格式互转时 |

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
| `pptx-sdk` | 编程式PPTX生成（python-pptx + PptxGenJS），已降级为参考模块（见 ppt-master/references/pptx-sdk.md） | `/ppt --backend sdk` |
| `ppt-source` | PPT素材获取（合并自 ppt-rag + ppt-researcher）：`--mode rag`（本地/URL索引）/ `research`（联网多源）/ `combined`（RAG+联网补充） | `/ppt --rag` 或 `/ppt --mode full` 自动调用 |
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
| `marketing-copy` | 产品营销推广内容 9 大文体（公众号软文 / 小红书 / 知乎 / 朋友圈 / 短视频 / 落地页 / EDM / PR 稿 / 客户故事 / Demo 脚本），含 ToB / ToC 双语风、AI 安全产品专属话术、避雷词清单 | `/marketing-copy` 命令调用 |
| `doc-formatter` | 文档格式化模块（DOCX读写 + 中文排版校正 + 导出），被 doc-polisher agent 调用 | `/polish` 命令调用 |
| `paper-collector` | arXiv 安全论文搜集与中文摘要生成 | `/paper-collect` 命令调用 |
| `paper-interpreter` | 论文 PDF 深度解读（4000-6000字公众号长文） | `/paper-interpret` 命令调用 |
| `remotion-generator` | Remotion 视频生成（三引擎：native模板/prompt2video全链路/vidosy场景配置） | `/remotion-generate` 命令调用 |
| `pdf2video` | PDF/PPT 转动态视频（stack/focus/zoom/fan 四种场景动画） | `/pdf2video` 命令调用 |
| `omni-captions` | 视频字幕生成（转录/翻译/双语/30+格式，Claude翻译无需额外API） | `/caption` 命令调用 |
| `videocut` | AI 视频智能剪辑（去停顿/重复/口误，ASR+Claude语义分析+FFmpeg剪切） | `/videocut` 命令调用 |
| `content-sync` | 内容多平台分发（30+平台一键同步，Wechatsync MCP + PostBot） | `/sync` 命令调用 |
| `pm-skills` | 产品经理技能库（JTBD/RICE/OKR/PMF/发布清单/用户故事地图等） | 对话触发 或 `/pm-skills` |
| `product-spec` | 产品规格统一知识库（合并 prd-generator + prd-spec + proto-prd），支持 prd/spec/proto/lite 四种模式 | `/product-spec` 命令调用 |
| `prd-writer` | 对话式 PRD 引导写作（集成自 chituai/prd-writer），三镜诊断 + 两阶段交付 + Mode A/B/C 三模式 | `/prd-writer` 命令调用 或 `@prd-coach` |
| `market-research` | 市场研究与竞争情报（竞品/趋势/TAM/亚马逊/OSS生态/品牌战略/营销分析框架）| `/market-research` 命令调用 |
| `user-research` | 用户研究方法论（访谈 / 问卷 / 卡片分类 / 旅程 / 画像 / Founder + JTBD + 痛点强度评分） | `/user-research` 命令调用 |
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
| `compliance-checklist` | 合规检查（等保/SOC2/ISO27001/GDPR/HIPAA/PCI/个保法 + 客户问卷 + DPIA/TPRM） | `/compliance-checklist` 命令调用 |
| `poc-plan` | PoC/试点管理（范围谈判 + SOW + 验收标准 + 转正 SOP + 失败退出） | `/poc-plan` 命令调用 |
| `gtm-strategy` | Go-to-Market 上市战略（增长模型/ICP/定位/渠道/定价/90天计划） | `/gtm-strategy` 命令调用 |
| `sales-guide-writer` | 销售一页禅五章结构 + 场景化销售剧本 + 竞争话术（A/B/C/D 分级）| `/sales-guide` 命令调用 |
| `product-doc-writer` | 24 类标准产品文档结构模板 + 写作规范 + 质量标准 | `/product-doc` 命令调用 |
| `doc-auditor` | 14 项文档质量检查 + 命名规范 + 密级管理 | `/doc-audit` 命令调用 |
| `proposal-generator` | 售前方案 / 可研报告 / 初步设计三大方案知识库 | `/proposal` 命令调用 |
| `ai-illustrator` | AI 智能插图（文章/学术/文档/创意四场景，多引擎路由） | 对话触发，被 `@article-illustrator` 调用 |
| `diagram-suite` | 完整图表生成套件（Markmap / PlantUML / Mermaid / MerdiAi 智能路由） | `/diagram` 命令调用 |
| `md-visual` | Markdown 转视觉图像（mark-pic / Madopic / tablesnap / 表格转图）| `/md-visual` 命令调用 |
| `table-toolkit` | 表格生成与转换（text2table / markdown-table / CSV-to-MD）| `/table` 命令调用 |
| `pm-core-framework` | 产品经理通用工作框架（前置思考层）— 三步判断：阶段/受众/输出结构 | 对话触发 |
| `working-backwards` | Amazon 逆向工作法（PR-FAQ + 6-pager）— 倒推客户价值，先写新闻稿再立项 | 对话触发 或 `/working-backwards` |
| `build-vs-buy` | Build vs Buy 决策框架（TCO 3 年 + Vendor 12 维评估 + Hybrid 模式）| `/build-vs-buy` 调用 |
| `sunset-plan` | 产品 / 功能下线 playbook（90/60/30/0 天客户通知 + 迁移路径 + 数据归属）| `/sunset` 调用 |
| `win-loss-analysis` | Win/Loss 赢单失单分析（访谈结构 + 根因聚类 + ICP 修正 + 季度复盘）| `/win-loss` 调用 |
| `churn-analysis` | Churn 流失分析 + Save Playbook（CHI 健康度 + 三级 Save Play + Win-Back）| `/churn-analysis` 调用 |
| `tech-debt` | 技术债优先级（WSJF + 20% 规则 + SLO 守门 + 业务话术）| `/tech-debt` 调用 |
| `ai-red-team` | AI 红队测试（OWASP LLM Top 10 + 10 个必测场景 + 4 周演练 + 报告输出）| `/ai-red-team` 调用 |
| `pm-full-cycle` | PM 全流程编排（13 步：市场→用户→竞品→定位→功能→MVP→Roadmap→PRD→验收→发布→销售） | 对话触发 |
| `pm-qa-acceptance` | 测试验收设计（10 维：功能/权限/异常/数据/状态/性能/审计/兼容/客户口径/上线阻断项） | 对话触发，被 `@qa-acceptance-designer` 调用 |
| `pm-ai-security-product` | AI / 网络安全产品双维度方法论（AI 维度 + 安全维度 + 红线 12 章产品方案，含 Eval / Prompt / 失败模式 / 成本） | 对话触发 或 `@ai-product-architect` 调用 |
| `discovery-call` | 售前需求挖掘（客户背调 / SPIN / MEDDIC / MoM / 回声邮件 / Win Score 评分）| `/discovery-call` 命令调用 |
| `gap-analysis` | 客户需求 vs 产品能力对照（4 级标签 / 评分 / Closure Plan / 投 vs 弃决策树）| `/gap-analysis` 命令调用 |
| `solution-architecture` | 解决方案架构（SA Blueprint 12 章 / NFR / 三档报价 / 行业定制）| `/solution-architecture` 命令调用 |
| `business-case` | 客户价值证明（ROI / TCO / Payback / NPV / 三档敏感性 / 行业锚点）| `/business-case` 命令调用 |
| `rfp-response` | RFP / RFI 应答（4 级模式 / Winning Themes / KB 复用 / 风险措辞红线）| `/rfp-response` 命令调用 |
| `security-questionnaire` | 安全问卷应答（CAIQ / SIG / VSA / 13 大类 / 合规证据映射）| `/security-questionnaire` 命令调用 |
| `battle-card` | 竞品作战卡（一页纸 / 三大杀手锏 / 三个雷区 / 标准应答 / 季度迭代）| `/battle-card` 命令调用 |
| `demo-design` | Demo 设计与演练（故事线 / 数据集 / 异常应对 / 反对意见 / 评分自检）| `/demo-design` 命令调用 |

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
| `/marketing-copy` | 产品营销推广内容 9 大文体生成器（软文 / 小红书 / 落地页 / EDM / PR / 案例 / Demo 脚本） | `commands/writing/marketing-copy.md` |
| `/polish` | 文档智能润色（AI去痕 + 中文排版校正 + 智能配图，支持 DOCX 导出） | `commands/polish.md` |
| `/paper-collect` | arXiv 安全论文搜集（按时间范围和主题批量检索，中文摘要输出） | `commands/paper-collect.md` |
| `/paper-interpret` | 论文深度解读（PDF → 4000-6000字公众号长文） | `commands/paper-interpret.md` |
| `/remotion-generate` | Remotion 视频生成（三引擎：native模板/prompt2video全链路/vidosy场景配置） | `commands/media/remotion-generate.md` |
| `/pdf2video` | PDF/PPT 文档转动态视频（四种场景动画，直接渲染 MP4） | `commands/media/pdf2video.md` |
| `/caption` | 视频字幕生成（转录+翻译+双语，30+格式，YouTube支持） | `commands/media/caption.md` |
| `/videocut` | AI 视频智能剪辑（去停顿/口误/重复，人工审核模式） | `commands/media/videocut.md` |
| `/sync` | 内容多平台一键分发（30+平台，草稿/直接发布） | `commands/writing/sync.md` |
| `/pm-skills` | 产品经理技能库查询（框架/模板/案例/辅导/清单） | `commands/product/pm-skills.md` |
| `/product-spec` | 产品规格统一入口（lite/prd/spec/proto 四种模式，合并自 /prd + /prd-spec + /proto-prd） | `commands/product/product-spec.md` |
| `/prd-writer` | 对话式 PRD 引导写作（Mode A 从零生成/Mode B 文档评估/Mode C 增量更新），适合非 PM 用户 | `commands/product/prd-writer.md` |
| `/prd` | ⚠️ 已合并至 /product-spec --mode prd（保留兼容） | `commands/product/prd.md` |
| `/market-research` | 竞争情报 & 市场研究（竞品/趋势/TAM/亚马逊/OSS） | `commands/product/market-research.md` |
| `/user-research` | 用户研究（访谈/问卷/卡片分类/旅程/画像） | `commands/product/user-research.md` |
| `/analytics` | 产品数据分析（指标/漏斗/留存/埋点/看板） | `commands/product/analytics.md` |
| `/feedback` | 用户反馈管理（NPS/分析/功能投票/VoC 报告） | `commands/product/feedback.md` |
| `/roadmap` | 产品路线图规划（优先级/里程碑/Gantt/OKR） | `commands/product/roadmap.md` |
| `/design-proto` | 设计与原型工具台（线框图/引导/动效/Penpot） | `commands/product/design-proto.md` |
| `/product-strategy` | 产品战略画布（BMC / Lean / VPC / Vision / 北极星） | `commands/product/product-strategy.md` |
| `/user-story-mapping` | 用户故事地图（Backbone + Walking Skeleton + Release Slices） | `commands/product/user-story-mapping.md` |
| `/mvp-canvas` | MVP 设计画布（RAT + 9 种 MVP 类型 + 验证退出） | `commands/product/mvp-canvas.md` |
| `/ab-test` | A/B 实验设计（假设 / 样本量 / 显著性 / 护栏 / SRM） | `commands/product/ab-test.md` |
| `/launch-checklist` | 发布检查清单（6 轨道 + 时间盒 + Go/No-Go + 灰度） | `commands/product/launch-checklist.md` |
| `/pricing-strategy` | 定价策略（Freemium / 套餐 / PSM / Conjoint / 涨价） | `commands/product/pricing-strategy.md` |
| `/pmf-survey` | PMF 评估（Sean Ellis + HXC + 信号雷达 + Pivot 决策） | `commands/product/pmf-survey.md` |
| `/product-report` | 产品报告（周报/月报/季度/Board/客户 BR） | `commands/product/product-report.md` |
| `/data-dashboard` | 产品数据看板（北极星/AARRR/Cohort/Revenue/客户 BR/AI 监控） | `commands/product/data-dashboard.md` |
| `/compliance-checklist` | 合规检查（等保/SOC2/ISO27001/GDPR/HIPAA/个保法 + 问卷应答） | `commands/product/compliance-checklist.md` |
| `/poc-plan` | PoC/试点管理（范围 + SOW + 验收 + 转正 SOP） | `commands/presales/poc-plan.md` |
| `/pm-discovery` | PM 全流程发现阶段编排（市场+用户+竞品+场景+机会+MVP+风险一次性输出） | `commands/product/pm-discovery.md` |
| `/pm-intake` | 产品需求 Intake — 任务类型判断 + 已知信息提取 + 缺口标注 + 下一步建议 | `commands/product/pm-intake.md` |
| `/pm-prd-enterprise` | 企业级 PRD 严格模板（B 端 SaaS / 私有化 / 多租户 / 审计 / 合规默认必填） | `commands/product/pm-prd-enterprise.md` |
| `/pm-review` | PM 视角产品方案评审 — 10 维度问题清单 + 修改建议 + 优化版本 | `commands/product/pm-review.md` |
| `/pm-sales-pack` | 销售与售前赋能材料一次性出包（定位/痛点/Demo/异议/竞品话术/成交） | `commands/product/pm-sales-pack.md` |
| `/working-backwards` | Amazon 逆向工作法 — PR-FAQ（默认）/ 6-pager 备忘录（--mode six-pager），倒推客户价值 | `commands/product/working-backwards.md` |
| `/build-vs-buy` | Build vs Buy 决策评估（TCO 3 年 + Vendor 评估 + Hybrid 模式建议）| `commands/product/build-vs-buy.md` |
| `/sunset` | Sunset / Deprecation Playbook（90/60/30/0 天客户通知 + 迁移路径 + 数据归属）| `commands/product/sunset.md` |
| `/win-loss` | Win/Loss 赢单失单分析（访谈结构 + 根因聚类 + ICP 修正）| `commands/product/win-loss.md` |
| `/churn-analysis` | Churn 流失分析 + Save Playbook（CHI 健康度 + 三级 Save Play）| `commands/product/churn-analysis.md` |
| `/tech-debt` | 技术债优先级评审（WSJF + 20% 规则 + SLO 守门 + 业务话术）| `commands/product/tech-debt.md` |
| `/ai-red-team` | AI 红队测试（OWASP LLM Top 10 + 10 个必测场景 + 红队报告）| `commands/product/ai-red-team.md` |
| `/discovery-call` | 售前需求挖掘工作流（拜访前准备 / 会议纪要 / 回声邮件 / MEDDIC 评分四模式）| `commands/presales/discovery-call.md` |
| `/gap-analysis` | 客户需求 vs 产品能力对照（4 级匹配 / Gap 评分 / 投 vs 弃决策树 / Closure Plan）| `commands/presales/gap-analysis.md` |
| `/solution-architecture` | 解决方案架构（SA Blueprint 12 章 / 现状 / 目标 / NFR / 路线图 / 三档报价）| `commands/presales/solution-architecture.md` |
| `/business-case` | 客户价值证明（一页纸 / 完整版 / TCO / ROI / 行业锚点 / 三档敏感性）| `commands/presales/business-case.md` |
| `/rfp-response` | RFP / RFI 应答生成器（4 级模式 / Winning Themes / KB 复用 / 评审清单）| `commands/presales/rfp-response.md` |
| `/security-questionnaire` | 安全问卷应答（CAIQ / SIG / VSA / 客户自定义 / 年度续答）| `commands/presales/security-questionnaire.md` |
| `/battle-card` | 竞品作战卡（一页纸 / 三大杀手锏 / 标准应答 / 季度迭代 / 库索引）| `commands/presales/battle-card.md` |
| `/demo-design` | Demo 设计与演练（故事线 / 数据集 / 演练 / 评分 / 后续物料 5 模式）| `commands/presales/demo-design.md` |
| `/gtm-strategy` | GTM 上市战略（增长模型 / ICP / 定位 / 渠道 / 定价 / 90 天计划）| `commands/product/gtm-strategy.md` |
| `/proposal` | 售前方案文档（解决方案 / 可研报告 / 设计方案）| `commands/presales/proposal.md` |
| `/sales-guide` | 销售一页禅（场景剧本 + FAQ + 竞争话术）| `commands/presales/sales-guide.md` |
| `/product-doc` | B2B 产品资料体系（24 类标准文档：白皮书 / 彩页 / 解决方案 / 操作手册 / 招投标参数等） | `commands/presales/product-doc.md` |
| `/doc-audit` | B2B 文档治理审计（24 类完整性 / 14 项自查）| `commands/presales/doc-audit.md` |

### Hooks

| Hook | 事件 | 用途 |
|------|------|------|
| `dangerous-command-blocker.js` | PreToolUse(Bash) | 拦截危险 Shell 命令 |
| TaskCompleted Prompt | TaskCompleted | 内容质量轻量检查 |

---

## Agent 选择指南

### 产品域 12 Agent 路由（按场景）

> **单点能力 → 直接用命令；复杂多技能场景 → 委派 Agent。**

| 需求场景 | 推荐 Agent | 说明 |
|---------|------------|------|
| 全栈 PM 工作（PRD / 路线图 / 多技能编排）| `product-manager` | 全栈 PM，按关键词智能分派子任务 |
| **售前 / 解决方案全链路（客户拜访 → PoC → 合同）** | `solution-architect` | 售前 SE / SA 总指挥，赢单导向 |
| 复杂跨部门 / CEO 项目 / 战略级评审 | `product-director` | 策略层：拆任务、分工、取舍、把关（不直接做产出） |
| 想法模糊 / 非 PM / 需要对话引导写 PRD | `prd-coach` | 渐进式多轮对话，三镜诊断+两阶段交付 |
| **综合研究（用户 + 市场 + 反馈 + PMF）** | `research-analyst` | 早期 0→1 / 立项 / PMF 测量 |
| 制定上市战略 / 渠道规划 / ICP / 90 天计划 | `gtm-strategist` | 专注 GTM 全链路 |
| 深度市场情报（竞品监测 / TAM / 选品） | `market-intelligence` | 仅做市场情报（vs research-analyst 综合多领域） |
| AI 功能 PRD / Prompt 工程 / Eval 设计 | `ai-product-architect` | 套用 pm-ai-security-product 双维度方法论 |
| PMF 验证 / 漏斗诊断 / 增长实验 / 定价 | `growth-strategist` | 用数据做增长决策 |
| **PRD/版本测试验收材料 / UAT / 上线阻断项** | `qa-acceptance-designer` | 验收方案 + 客户验收口径 |
| 生成销售物料 / 产品手册 / 销售指南 | `product-enablement` | 销售赋能 |
| 售前方案 / 可研报告 / 投标技术方案 | `proposal-writer` | 项目型方案 |

### PRD 写作路由

| 场景 | 推荐工具 | 说明 |
|------|---------|------|
| 有产品想法，想法模糊，需要引导 | `/prd-writer` 或 `@prd-coach` | 对话式，三镜诊断→概念稿→实现稿 |
| 想法清晰，需要快速生成结构化 PRD（C 端 / 通用产品） | `/product-spec --mode prd` | 一次输入，一次输出模板 |
| 想法清晰，**B 端 SaaS / 私有化 / 多租户** | `/pm-prd-enterprise` | 12 章严格模板，权限/审计/合规默认必填 |
| 需要规格化文档（四件套）| `/product-spec --mode spec` | Spec-First，proposal/specs/design/tasks |
| 需要线框图 + PRD 一体化 | `/product-spec --mode proto` | ASCII 线框图优先 |
| 评估/改进现有 PRD 文档 | `/prd-writer --mode b` | 三层评分 + 具体改进建议 |
| 在现有 PRD 上增加功能 | `/prd-writer --mode c` | 增量合并，不重写原文 |
| **PRD 已写完，做 PM 视角评审** | `/pm-review` | 10 维度问题清单 + 修改建议 |
| **AI / 安全融合产品 PRD** | `@ai-product-architect` 或 `pm-ai-security-product` Skill | AI 维度 + 安全维度双轴方法论 |

### 视觉内容 Agent 路由

| 需求 | 推荐 Agent | 说明 |
|------|------------|------|
| 为文章/博客 .md 文件自动批量配图 | `article-illustrator` | 扫描段落、混合路由、批量插入图表 |
| 思维导图 / UML / Markdown 海报 / 表格转图 / 学术插图 | `visual-suite` | 综合视觉生产，六大工具链编排 |
| 多引擎图表（Mermaid/PlantUML/diagrams/Visio）+ 格式互转 | `diagram-architect` | 图表类型不确定或需要格式转换时首选 |

### 视频处理命令路由

| 需求 | 推荐命令 | 说明 |
|------|----------|------|
| 从零生成视频（模板/全链路/场景配置） | `/remotion-generate` | Remotion 三引擎：native / prompt2video / vidosy |
| PDF / PPT 文档转动态视频 | `/pdf2video` | 四种场景动画，直接渲染 MP4 |
| 视频字幕生成（转录+翻译+双语） | `/caption` | 支持 YouTube，30+ 字幕格式 |
| 视频智能剪辑（去停顿/口误/重复） | `/videocut` | ASR + Claude 语义分析 + FFmpeg |

---

## 产品经理全工作链路总览

WorkAgent 现已覆盖 C 端 + B 端产品经理 + 售前 / 解决方案全工作场景：**35 个产品命令 + 13 个售前命令 + 45 个产品 Skills + 12 个产品 Agents + 15 个标准模板（含完整填充版）**。

> 📚 **首次上手** → 套用 `templates/pm-discovery-template.md` 跑通 `/pm-intake → /pm-discovery → /pm-prd-enterprise → @qa-acceptance-designer → /pm-sales-pack` 端到端流程（含 PM Discovery / Sales Enablement / Acceptance Checklist 三大填充版模板）。
> 📊 **仓库健康度** → 看 `HEALTH_REPORT.md`，确认所有组件可直接使用。

### 按 PM 工作场景的命令导航

#### 🎯 战略与规划
| 命令 | 一句话定位 |
|------|---------|
| `/product-strategy` | 产品战略画布（BMC / Lean / VPC / Vision / 北极星） |
| `/working-backwards` | Amazon 逆向工作法（PR-FAQ + 6-pager），新功能 / 立项前先写 |
| `/gtm-strategy` | Go-to-Market 上市战略（增长模型 / ICP / 渠道 / 90 天计划） |
| `/roadmap` | 产品路线图（优先级 / 里程碑 / Gantt 视图） |
| `/build-vs-buy` | Build vs Buy 决策（TCO 3 年 + Vendor 评估）|
| `/sunset` | 产品 / 功能下线 Playbook（90/60/30/0 天通知节奏）|
| `/pricing-strategy` | 定价策略（Freemium / 套餐 / PSM / Conjoint） |

#### 💬 高频日常沟通工件
| 命令 / 模板 | 一句话定位 |
|------|---------|
| `templates/pr-faq-template.md` | Amazon PR-FAQ 模板 |
| `templates/six-pager-template.md` | 6-Pager 备忘录模板 |

#### 🔍 用户研究与发现
| 命令 | 一句话定位 |
|------|---------|
| `/pm-discovery` | 发现阶段一次性产出（市场+用户+竞品+场景+机会+MVP+风险） |
| `/user-research` | 用户研究（访谈 / 问卷 / 卡片分类 / 旅程 / 画像） |
| `/market-research` | 市场研究与竞品情报（竞品 / 趋势 / TAM / OSS） |
| `/feedback` | 用户反馈管理（NPS / 主题聚类 / 情感分析 / VoC 报告） |
| `/pmf-survey` | PMF 评估（Sean Ellis / HXC / 信号雷达 / Pivot 决策） |

#### 📋 需求定义
| 命令 | 一句话定位 |
|------|---------|
| `/pm-intake` | 需求 Intake — 任务类型判断 + 缺口标注 + 下一步建议（统一入口） |
| `/prd-writer` | 对话式 PRD 引导（适合非 PM / 想法模糊） |
| `/product-spec` | 产品规格统一入口（lite / prd / spec / proto 四模式） |
| `/pm-prd-enterprise` | 企业级 PRD 严格模板（B 端 SaaS / 私有化 / 多租户） |
| `/pm-review` | PM 视角方案评审（10 维度问题清单 + 修改建议） |
| `/user-story-mapping` | 用户故事地图（Backbone + Walking Skeleton + Slices） |
| `/mvp-canvas` | MVP 设计画布（RAT + 9 种 MVP 类型 + 验证退出） |
| `/design-proto` | 设计原型与线框图（Wireframe / Onboarding / 动效） |

#### 🔒 B 端合规与认证
| 命令 | 一句话定位 |
|------|---------|
| `/compliance-checklist` | 合规检查（等保 / SOC 2 / ISO 27001 / GDPR / 个保法 + 客户问卷应答） |

#### 🚀 交付与上线
| 命令 | 一句话定位 |
|------|---------|
| `/tech-debt` | 技术债优先级（WSJF + 20% 规则 + SLO 守门 + 业务话术）|
| `/launch-checklist` | 发布检查清单（6 轨道 + 时间盒 + Go/No-Go） |
| `/ai-red-team` | AI 红队测试（OWASP LLM Top 10 + 10 个必测场景 + 报告）|

#### 🤝 售前 / 解决方案（SE / SA 全链路）
| 命令 | 一句话定位 |
|------|---------|
| `/discovery-call` | 客户拜访工作流（拜访前 / 会议纪要 / 回声邮件 / MEDDIC 评分）|
| `/gap-analysis` | 客户需求 vs 产品能力对照（4 级匹配 / 评分 / 投 vs 弃决策树）|
| `/solution-architecture` | 解决方案架构（SA Blueprint 12 章 / NFR / 三档报价）|
| `/business-case` | 客户价值证明（ROI / TCO / Payback / 三档敏感性）|
| `/rfp-response` | RFP / RFI 应答（4 级模式 / Winning Themes / KB 复用）|
| `/security-questionnaire` | 安全问卷应答（CAIQ / SIG / VSA / 客户自定义）|
| `/battle-card` | 竞品作战卡（一页纸 / 三大杀手锏 / 季度迭代）|
| `/demo-design` | Demo 设计与演练（故事线 / 数据集 / 异常应对 / 评分）|

#### 💰 销售与上市
| 命令 | 一句话定位 |
|------|---------|
| `/pm-sales-pack` | 销售赋能材料一次性出包（定位/痛点/Demo/异议/竞品话术/成交） |
| `/proposal` | 售前方案文档（解决方案 / 可研报告 / 设计方案） |
| `/sales-guide` | 销售一页禅（场景剧本 + FAQ + 竞争话术） |
| `/product-doc` | B2B 产品资料体系（24 类标准文档：白皮书/彩页/解决方案/手册等） |
| `/marketing-copy` | 产品营销推广内容（软文/小红书/落地页/EDM/PR/客户故事/Demo 脚本）|
| `/poc-plan` | PoC / 试点管理（范围 / SOW / 验收 / 转正 SOP） |
| `/doc-audit` | B2B 文档治理审计（24 类完整性 / 14 项自查） |

#### 📈 客户分析（B 端核心）
| 命令 | 一句话定位 |
|------|---------|
| `/churn-analysis` | 流失分析 + Save Playbook（CHI + 三级 Save Play + Win-Back）|
| `/win-loss` | 赢单失单分析（访谈结构 + 根因聚类 + ICP 修正）|

#### 📊 数据与运营
| 命令 | 一句话定位 |
|------|---------|
| `/analytics` | 产品数据指标设计（北极星 + 漏斗 + 留存 + 埋点） |
| `/data-dashboard` | 产品数据看板（PostHog/Mixpanel + 6 类模板 + 嵌入） |
| `/ab-test` | A/B 实验设计（假设 / 样本量 / 显著性 / 护栏 / 实验日志） |

#### 🔄 报告与沉淀
| 命令 | 一句话定位 |
|------|---------|
| `/product-report` | 产品报告（周报 / 月报 / 季度 / Board / 客户 BR） |

#### 🛠️ 框架与方法论
| 命令 | 一句话定位 |
|------|---------|
| `/pm-skills` | PM 知识库查询（JTBD / RICE / Lenny's 等） |

---

### Agent 全景（产品域 10 个）

| Agent | 主战场 |
|-------|--------|
| `@product-manager` | 全栈 PM（多技能智能路由） |
| `@solution-architect` | 售前 / 解决方案全链路（客户拜访 → PoC → 合同）|
| `@product-director` | 产品总监（策略层：拆任务/分工/取舍/把关） |
| `@prd-coach` | PRD 对话教练（专注 PRD 写作） |
| `@research-analyst` | 综合研究（用户 + 市场 + 反馈 + PMF） |
| `@growth-strategist` | 增长战略（PMF / 漏斗 / A/B / 定价） |
| `@qa-acceptance-designer` | 测试验收设计（验收方案 + 上线阻断项 + 客户验收口径） |
| `@ai-product-architect` | AI 产品架构师（LLM / Agent / RAG，套用 pm-ai-security-product） |
| `@gtm-strategist` | 上市战略 |
| `@product-enablement` | 销售赋能 |
| `@proposal-writer` | 售前方案 |
| `@market-intelligence` | 市场情报（深度专项） |

---

### PM Kit 集成包（pm_claude_code_kit → WorkAgent）

> 来自 `pm_claude_code_kit` 的 PM 全流程工具集已融入本仓库。**不重复实现已有能力，仅补充 B 端 / 企业级视角**。

| 类型 | 新增 / 集成内容 | 用途 |
|------|-----------------|------|
| Agent | `@product-director` | 复杂跨部门 / 战略级评审（与 product-manager 互补） |
| Agent | `@qa-acceptance-designer` | 测试验收方案 + 上线阻断项 |
| Skill | `pm-core-framework` | PM 通用工作框架（前置思考层：阶段/受众/输出结构） |
| Skill | `pm-full-cycle` | PM 端到端 13 步编排（想法 → 上线 + 销售） |
| Skill | `pm-qa-acceptance` | 测试验收 10 维方法论 |
| Skill | `pm-ai-security-product` | AI + 网络安全产品双轴方法论 |
| Command | `/pm-discovery` | 发现阶段一次性产出（市场+用户+竞品+场景+机会） |
| Command | `/pm-intake` | 需求 Intake（任务类型判断 + 缺口标注） |
| Command | `/pm-prd-enterprise` | 企业级 PRD 严格模板（B 端 SaaS / 私有化） |
| Command | `/pm-review` | PM 视角方案评审（10 维度问题清单） |
| Command | `/pm-sales-pack` | 销售赋能材料一次性出包 |
| Templates | `templates/{prd,brd,mrd,roadmap,acceptance-checklist,release-note,sales-enablement,requirement-pool}-template.md` | 8 个标准模板（首次填充本仓库 templates/ 目录） |

**与原有能力的边界规则**：

- `/pm-prd-enterprise` vs `/product-spec --mode prd`：前者用于 B 端严格场景（多租户/审计/合规默认必填），后者用于通用快速生成
- `@product-director` vs `@product-manager`：前者是策略层（评审/分工），后者是执行层（直接产出）
- `@qa-acceptance-designer` vs `/launch-checklist`：前者写验收方案与 Case，后者编排发布全流程
- `pm-ai-security-product` vs `@ai-product-architect`：前者是 Skill（方法论文档），后者是 Agent（套用方法论做产品架构）
- `/pm-sales-pack` vs `/sales-guide`：前者单产品快速出包，后者是销售一页禅设计方法论
- `/pm-intake` 是新的入口命令，承接所有"想法/客户工单/老板需求"的初步澄清

---

### 模板库（`templates/`）

| 模板文件 | 用途 | 配套 Skill / Command |
|---------|------|---------------------|
| `prd-template.md` | 企业级 PRD 12 章模板 | `/pm-prd-enterprise`、`product-spec` |
| `pm-discovery-template.md` | 产品发现报告完整填充版（结论 / 市场 / 客户 / 痛点 / 竞品 / MVP / 风险 10 章）| `/pm-discovery`、`pm-full-cycle` |
| `brd-template.md` | 商业需求文档（值不值得做） | `/product-strategy`、`pm-full-cycle` |
| `mrd-template.md` | 市场需求文档（市场在哪） | `/market-research`、`pm-full-cycle` |
| `roadmap-template.md` | 产品 Roadmap | `/roadmap`、`product-roadmap` |
| `requirement-pool-template.md` | 需求池标准结构 | 配合 PM 工作流使用 |
| `acceptance-checklist-template.md` | 测试验收清单 | `/launch-checklist`、`pm-qa-acceptance` |
| `release-note-template.md` | Release Note（内部 + 客户两版） | `/launch-checklist` |
| `sales-enablement-template.md` | 销售赋能材料 | `/pm-sales-pack`、`@product-enablement` |
| `pr-faq-template.md` | Amazon 新闻稿 + FAQ（PR-FAQ） | `/working-backwards` |
| `six-pager-template.md` | 6 页备忘录（完整段落叙述，禁子弹点） | `/working-backwards --mode six-pager` |
| `model-card-template.md` | AI 透明度行业标准 Model Card | `pm-ai-security-product` |
| `ai-eval-rubric-template.md` | AI Eval 评测尺（7 维 + 通过线 + 红线） | `pm-ai-security-product`、`/ai-red-team` |

---



| 容易混淆的命令对 | 选择规则 |
|----------------|---------|
| `/prd-writer` vs `/product-spec` | 想法模糊用前者（对话引导）；想法清晰用后者（一次模板） |
| `/product-spec` vs `/pm-prd-enterprise` | 通用 / C 端用前者；**B 端 SaaS / 私有化 / 多租户** 用后者（严格 12 章模板） |
| `/product-spec` vs `pm-ai-security-product` | 通用功能用前者；含 LLM/Eval/Prompt 或 AI + 安全融合用后者方法论 |
| `/pm-review` vs `/prd-writer --mode b` | PM 视角 10 维度评审用前者；定性人工评分 + 改进建议用后者 |
| `/pm-review` vs `/doc-audit` | PRD/Spec 内部 10 维度评审用前者；24 类资料完整性用后者 |
| `/pm-intake` vs `/prd-writer` / `@prd-coach` | **任务类型判断 + 缺口标注**用 `/pm-intake`；想法清晰后再用其他工具 |
| `/pm-discovery` vs `@research-analyst` | 一次性快速出报告用前者；深度专项研究用后者 |
| `/pm-sales-pack` vs `/sales-guide` | 单产品快速出包用前者；销售一页禅设计方法论用后者 |
| `@product-director` vs `@product-manager` | 策略层（拆任务/取舍/把关）用前者；执行层（直接产出）用后者 |
| `@qa-acceptance-designer` vs `/launch-checklist` | 验收方案 + 用例 + 阻断项用前者；发布全流程编排用后者 |
| `/working-backwards` vs `/pm-prd-enterprise` | 立项前先 PR-FAQ 倒推客户价值用前者；立项后写正式 PRD 用后者 |
| `/build-vs-buy` vs `/pm-review` | 做"自研还是买"决策评估用前者；任何 PRD/方案的多维度评审用后者 |
| `/sunset` vs `/launch-checklist` | 产品下线 / 退役用前者；新功能上线用后者 |
| `/win-loss` vs `/churn-analysis` | 销售阶段（赢单失单）用前者；签约后（客户流失）用后者 |
| `/ai-red-team` vs `/compliance-checklist` | AI 安全对抗测试用前者；通用合规框架检查用后者 |
| `/user-research` vs `/market-research` | 用户视角（行为/JTBD）用前者；市场视角（竞品/TAM）用后者 |
| `/user-research` vs `/feedback` | 主动设计研究用前者；分析现有反馈用后者 |
| `/user-research` vs `/pmf-survey` | 通用研究用前者；PMF 专项 Sean Ellis 用后者 |
| `/analytics` vs `/data-dashboard` | 指标定义 / 埋点用前者；看板可视化 / 嵌入用后者 |
| `/ab-test` vs `@growth-strategist` | 单实验设计用前者；增长全局诊断 + 实验队列用后者 |
| `/proposal` vs `/product-doc` | 项目型一次性用前者；产品级可复用资料用后者 |
| `/proposal` vs `/sales-guide` | 客户响应方案用前者；销售一页禅用后者 |
| `/marketing-copy` vs `/article-writer` | 带营销目的的推广（CTA 明确）用前者；公众号长文（个人风格 / 观点输出）用后者 |
| `/marketing-copy` vs `/product-doc` | 对外推广物料 / 媒体投放用前者；内部资料体系（白皮书/手册）用后者 |
| `/marketing-copy --type case` vs `/product-doc --type case` | 媒体外推 / 公众号发布版用前者；官网案例库 / 销售口袋资料用后者 |
| `/marketing-copy --type pr` vs `/working-backwards` | 对外发布的真实新闻稿用前者；立项前内部 PR-FAQ 决策工具用后者 |

---

### B 端 PM 完整工作流（端到端）

```
售前阶段：
  /market-research（竞品 / 行业）
  → /sales-guide（销售物料）
  → /product-doc（白皮书 / 解决方案）
  → /proposal（客户响应方案）

PoC 阶段：
  /poc-plan --mode fullset（范围 + SOW + 验收）
  → 执行 PoC（4-12 周）
  → /poc-plan --mode convert（PoC → 合同）

合同签订：
  → /compliance-checklist --mode questionnaire（合规问卷）
  → 签约

合规与审计（贯穿）：
  /compliance-checklist --mode assess（年度自查）
  → /compliance-checklist --mode roadmap（认证规划）
  → 客户审计 → /doc-audit
```

### C 端 PM 完整工作流（端到端）

```
0→1 早期验证：
  /product-strategy --mode lean（立项画布）
  → /user-research --mode interview（用户访谈）
  → /mvp-canvas --mode fullset（MVP 设计）
  → 上线 MVP
  → 8 周后 /pmf-survey
  → ✅ → 进入 1→10
  → ❌ → 启动 Pivot 决策

1→10 规模化：
  /pmf-survey --mode signals
  → @growth-strategist（漏斗诊断 + 实验队列）
  → /pricing-strategy --mode tier
  → /roadmap --horizon 3m

新功能完整启动：
  /product-strategy → /user-story-mapping
  → /product-spec --mode spec
  → /launch-checklist

季度规划闭环：
  /product-strategy --mode northstar
  → /roadmap --horizon 3m

AI 功能开发：
  /product-strategy --mode lean
  → @ai-product-architect（套用 pm-ai-security-product 方法论）→ POC
  → /ab-test vs baseline → /launch-checklist
  → /ai-red-team

产品报告节奏：
  每周 /product-report --mode weekly
  每月 /product-report --mode monthly --audience exec
  每季 /product-report --mode quarterly
  每季客户 /product-report --mode customer-br

数据与上线后（贯穿全周期）：
  上线后 → /data-dashboard --mode embed
  实验设计 → /ab-test --mode design
```

