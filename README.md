# WorkAgent

> 以风格驱动的 AI 内容创作平台

WorkAgent 是面向内容创作者的 AI 辅助写作系统，核心理念是：**先学习你的风格，再用你的风格写作**。

## 快速开始

### 用卡兹克风格写文章

直接触发，无需命令：

```
帮我写一篇公众号文章，主题是 Claude Code 的实际使用体验
```

或显式调用：

```
/khazix-writer 帮我写一篇关于 Claude Code 的公众号文章
```

### 横纵分析法深度研究

对产品/公司/概念/人物进行系统性研究，输出排版精美的 PDF 报告：

```
/hv-analysis 帮我用横纵分析法研究 Hermes Agent
/hv-analysis 深度研究一下 Claude Code 这个产品
/hv-analysis 竞品分析：Cursor vs Claude Code vs Windsurf
```

### 访谈写作（Writer-Reviewer 互搏）

输入访谈素材，自动提炼核心观点，通过 Writer-Reviewer 对抗迭代生成高质量文章：

```
/interview-writer 以下是我和 [人物] 的访谈记录：[粘贴素材]
/interview-writer --target-score 88 --max-rounds 3
```

### PPT 生成（6种引擎）

智能路由到最合适的引擎，或手动指定 `--backend`：

```
# 学术演讲（无论文PDF） → academic-pptx
/ppt 帮我做论文答辩 PPT，主题"深度学习在医学图像分割中的应用"

# 学术演讲（有论文PDF，自动提取内容） → SlideTailor
/ppt --backend slidetailor --source paper.pdf --duration 15

# 商务通用 PPT → ppt-master
/ppt 做一个年度总结 PPT --style mckinsey --pages 12

# 技术/代码演示 → Slidev
/ppt React Hooks 深度解析技术分享 --backend slidev

# Markdown 快速出片 → Marp
/ppt 把这份 README.md 转成幻灯片 --backend marp --source README.md

# ���据驱动/批量生成 → PPTX SDK
/ppt 根据 data.csv 批量生成月度销售报告 --backend sdk
```

### 文章配图生成（三合一）

智能路由到三种渲染后端，零成本生成专业级配图：

```
# 全自动为整篇文章配图（扫描→识别→批量生成→插入）
/illustrate article.md

# 阶段模式（每步暂停确认 ASCII 草图和 HTML 效果）
/illustrate article.md --mode staged

# 单图生成：结构化图表（ASCII→HTML→截图，零成本）
/illustrate --mode single --desc "用户注册流程：填写信息→验证→发送邮件→激活"
/illustrate --mode single --type arch --desc "微服务三层架构：前端/网关/服务/数据库"
/illustrate --mode single --type compare --desc "方案A快速部署 vs 方案B高度定制"

# 单图生成：精确语义图表（Mermaid）
/illustrate --mode single --backend mermaid --type sequence --desc "API调用时序"
/illustrate --mode single --backend mermaid --type er --desc "用户-订单-商品关系"

# 单图生成：AI创意图像（Stable Diffusion，需本地 WebUI）
/illustrate --mode single --backend sd --desc "AI多智能体协作科技感封面"

# 风格选择
/illustrate article.md --style tech           # 科技感深色
/illustrate article.md --style business-blue  # 商务蓝白（默认）
/illustrate article.md --style minimal        # 极简线条
```

**三个后端对比**：

| 后端 | 适合图表类型 | 成本 | 质量 |
|------|------------|------|------|
| `html`（默认）| 流程图/架构图/对比表/步骤图 | 零成本 | 专业商务风 |
| `mermaid` | 时序图/ER图/甘特图/类图 | 零成本 | 精确语义 |
| `sd` | 封面图/插图/创意图像 | 需本地GPU | AI生成 |

### 数据查询与分析（SQL + Python 双后端）

自然语言转 SQL、SQL 优化、Python 数据分析，支持 MySQL/PostgreSQL/SQLite/MongoDB 等：

```
# 数据库查询
/taskweaver 查询最近 30 天销售额超过 1000 的订单
/taskweaver 按月统计 2024 年各地区销售额，取前 10 名
/taskweaver 优化这个慢查询 --mode optimize
/taskweaver 解释这段 SQL 的含义 --mode explain
```

### TaskWeaver 数据分析

代码优先 Agent，SQL 查询与 Python 代码执行一体化：

```
/taskweaver 读取 sales.csv 按月统计销售额并生成趋势图
/taskweaver 将 data/ 目录下所有 Excel 文件合并去重 --output combined.csv
/taskweaver 分析 log.txt 中各类错误的出现频率
```

### MetaGPT 项目生成

多 Agent 软件公司模拟，从需求到代码一键生成完整项目：

```
/metagpt 开发一个待办事项 API，支持增删改查，使用 FastAPI + SQLite
/metagpt 仅生成 PRD：在线书店系统 --mode prd
/metagpt 开发博客系统 --roles pm,architect --mode design
```

---

## Skills

| Skill | 触发场景 | 使用方式 |
|-------|---------|---------|
| `khazix-writer` | 写公众号文章、写稿子、续写、按我风格写 | 对话触发 或 `/khazix-writer` |
| `hv-analysis` | 横纵分析、深度研究、竞品分析、研究产品/公司/概念/人物 | 对话触发 或 `/hv-analysis` |
| `interview-writer` | 访谈写作、人物专访、对话整理、访谈稿 | 对话触发 或 `/interview-writer` |
| `ppt-master` | 通用 PPT 生成，支持多种设计风格和图片生成 | `/ppt` 命令调用 |
| `academic-pptx` | 学术演讲 PPT 生成，论证优先设计 | `/ppt` 命令调用 |
| `slidetailor` | 论文PDF → 学术幻灯片，NLP自动内容提取 | `/ppt --backend slidetailor` |
| `slidev` | 开发者/技术演示（Markdown+Vue，代码高亮动画） | `/ppt --backend slidev` |
| `marp` | Markdown 快速出片，输出 HTML/PDF/PPTX | `/ppt --backend marp` |
| `pptx-sdk` | 编程式 PPTX 生成（python-pptx / PptxGenJS） | `/ppt --backend sdk` |
| `mermaid-chart` | 精确语义图表（时序图/ER图/甘特图/类图） | `/illustrate --backend mermaid` |
| `stable-diffusion` | AI 图像生成，文生图/图生图（需本地 SD WebUI） | `/illustrate --backend sd` |
| `html-chart` | HTML图表生成器，ASCII→HTML→截图，4种商务风格（主管道） | `/illustrate`（默认） |
| `chat2db` | 自然语言转 SQL，SQL 优化，支持 MySQL/PostgreSQL 等 | 对话触发 或 `/taskweaver --backend sql` |
| `taskweaver` | 代码优先 Agent，Python 沙箱执行数据分析和自动化任务 | 对话触发 或 `/taskweaver` |
| `metagpt` | 多 Agent 软件公司，PRD→架构→代码→测试全流程 | 对话触发 或 `/metagpt` |

## Commands

独立命令，直接调用对应的 skill：

| Command | 描述 | 文件 |
|---------|------|------|
| `/khazix-writer` | 卡兹克风格公众号长文写作（4000-8000字） | `commands/khazix-writer.md` |
| `/hv-analysis` | 横纵分析法深度研究，输出 PDF 报告（10000-30000字） | `commands/hv-analysis.md` |
| `/interview-writer` | 访谈写作 Writer-Reviewer 互搏流程 | `commands/interview-writer.md` |
| `/ppt` | PPT 生成，自动识别学术演讲或通用 PPT 场景 | `commands/ppt.md` |
| `/illustrate` | 文章配图生成，HTML图表/Mermaid/SD三合一，支持全文自动配图 | `commands/illustrate.md` |
| `/taskweaver` | 数据分析 Agent — SQL 查询（Chat2DB）+ Python 代码执行，双后端智能路由 | `commands/taskweaver.md` |
| `/metagpt` | 多 Agent 软件项目生成（PRD→架构→代码→测试） | `commands/metagpt.md` |

## khazix-writer 说明

`khazix-writer` 内置了「数字生命卡兹克」的写作风格体系，核心是：

> **"有见识的普通人在认真聊一件打动他的事。"**

- 亲自下场，不隔空评论
- 口语化叙述，不用套话
- 四层自检体系保证"活人感"
- 适用于公众号长文（4000-8000 字）

## hv-analysis 说明

横纵分析法由数字生命卡兹克提出，融合了：
- 索绪尔的历时-共时分析（Saussure）
- 社会科学的纵向-横截面研究设计
- 商学院案例研究法
- 竞争战略分析

核心原则：纵向追时间深度，横向追同期广度，最终交汇出判断。

**输出格式**：
- Markdown 报告：`[研究对象]_横纵分析报告.md`
- PDF 报告：`[研究对象]_横纵分析报告.pdf`（A4 排版，深蓝/绿/浅蓝配色）

**依赖**：`pip install weasyprint markdown --break-system-packages`

## interview-writer 参数说明

```
--style-card <路径>         使用已保存的风格卡片（可选）
--target-score <分数>       目标评分，默认 85
--max-rounds <轮次>         最大互搏轮次，默认 3
--mode full|draft           full=完整互搏流程，draft=仅输出初稿
--save-kb true|false        是否沉淀到知识库，默认 true
```

## PPT 生成说明

WorkAgent 集成了两个 PPT 生成 skill，自动根据场景选择：

### academic-pptx（学术演讲 PPT）

**适用场景**：
- 会议论文演讲（conference talk）
- 研讨会报告（seminar）
- 论文答辩（thesis defense）
- 资助申请简报（grant briefing）

**设计原则**：
- 论证优先设计（Argument-first design）
- 行动标题（Action titles）— 每张幻灯片标题是完整句子
- 一个展品一张幻灯片
- 强制引用和参考文献
- 白色背景，单一无衬线字体

**依赖**：
```bash
pip install "markitdown[pptx]"
npm install -g pptxgenjs
```

### ppt-master（通用 PPT）

**适用场景**：
- 商业报告、产品介绍
- 年度总结、工作汇报
- 营销材料、培训材料

**核心特性**：
- 完全可编辑的原生 PPTX（DrawingML 形状，非图片）
- 支持 PDF/DOCX/URL/Markdown 源文档转换
- 多角色 AI 协作（Strategist → Image_Generator → Executor）
- 支持 10+ 图片生成后端（Gemini、OpenAI、Qwen 等）
- 多种设计风格（Google、McKinsey、Zen、Pixel 等）

**依赖**：
```bash
pip install python-pptx PyMuPDF mammoth svglib reportlab Pillow
npm install -g pptxgenjs
```

**参数说明**：
```
--format <格式>             画布格式（ppt169/ppt43/xiaohongshu/moments），默认 ppt169
--style <风格>              设计风格（google/mckinsey/zen/pixel/academic），默认自动判断
--source <路径>             源文档路径（PDF/DOCX/URL/Markdown）
--pages <数量>              目标页数，默认自动计算
--type <类型>               演讲类型（conference/seminar/defense/grant），默认 conference
--duration <分钟>           演讲时长，默认 15
--image-backend <后端>      图片生成后端（gemini/openai/qwen/zhipu），默认 gemini
```

---

## 来源

本项目集成了以下开源仓库的内容：

### 写作能力
- [khazix-skills](https://github.com/KKKKhazix/khazix-skills) — 数字生命卡兹克的写作技能
  - `khazix-writer` — 公众号长文写作 skill
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
- [@KKKKhazix](https://github.com/KKKKhazix)
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
