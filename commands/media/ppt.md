---
name: ppt
description: >
  演示文稿全流程生成 — 10阶段完整流水线：主题定义→内容搜集（官方/媒体/学术/产业/RAG索引）→归纳总结→图表构建→幻灯片初稿（0→1核心制作）→版式排版→视觉美化→初版渲染→多维质量评分→3-5轮自迭代优化→最终生成输出；同时支持6种引擎快速模式：学术演讲、商务通用、技术/代码演示、Markdown快速出片、论文自动生成、编程式生成
user-invocable: true
argument-hint: "<任务描述> [--mode full|rag|research|outline|diagram|make] [--backend academic|ppt-master|slidev|marp|slidetailor|sdk] [--rag <文件或URL>...] [--rag-dir <目录>] [--rag-index <名称>] [--rag-mode replace|supplement] [--style <风格>] [--format ppt169|4:3] [--source <路径>] [--output <文件名>] [--lang zh|en] [--pages <数量>] [--duration <分钟>] [--iter 0|1|auto] [--score-pass <分数>]"
allowed-tools: [Read, Write, Edit, Bash, WebSearch, WebFetch, AskUserQuestion]
harness:
  execute:
    preset: media-heavy
  constrain:
    profile: shell-restricted
    gates: [before-write, before-destructive]
  loop:
    mode: one-shot
  memory:
    scope: session
    reads: [project-context]
  security:
    danger-level: medium
---

# /ppt — 演示文稿全流程生成

加载技能（按需）：
- 素材获取：`skills/ppt/ppt-rag-indexer/SKILL.md`（已有材料） · `skills/ppt/ppt-web-researcher/SKILL.md`（联网研究）
- 结构与制作：`skills/ppt/ppt-architect/SKILL.md` · `skills/ppt/ppt-master/SKILL.md` · `skills/ppt/academic-pptx/SKILL.md` · `skills/ppt/marp/SKILL.md`
- 图表配套：`skills/diagram/mermaid-chart/SKILL.md` · `skills/diagram/diagram-plantuml/SKILL.md` · `skills/diagram/diagram-markmap/SKILL.md` · `skills/diagram/arch-diagram/SKILL.md`

---

## 入口决策树

```
用户输入
  │
  ├─ 有本地文件 / 在线URL？
  │   └─→ RAG模式（--mode rag 或 --rag <路径/URL>）
  │        Phase 1→2B→3→4→5→6→7→8→9→10
  │
  ├─ 从零开始，无任何素材？
  │   └─→ 全流程模式（--mode full）
  │        Phase 1→2→3→4→5→6→7→8→9→10
  │
  ├─ 有现成内容/大纲，只需制作？
  │   └─→ 制作模式（--mode make 或 --backend <引擎>）
  │        Phase 5→6→7→8→9→10
  │
  ├─ 只需研究报告，不制作PPT？
  │   └─→ 研究模式（--mode research）
  │        Phase 1→2（或2B）→3，输出素材包
  │
  └─ 只需图表/架构图？
      └─→ 图表模式（--mode diagram）
           Phase 4，输出 diagrams/
```

---

## 快速示例

```bash
# === RAG 模式（已有材料 → PPT）===
/ppt Q4业绩汇报 --rag quarterly_report.pdf --style mckinsey
/ppt AI医疗分析 --rag report.pdf data.xlsx case.docx --pages 20
/ppt 竞品分析   --rag-dir ./research/ --pages 20
/ppt 政策解读   --rag https://gov.cn/policy.pdf https://news.cn/article
/ppt 行业白皮书 --rag internal.pdf https://industry.org/report2024

# 持久化索引（大文档库，避免重复摄入）
/ppt 产品发布PPT --rag spec.pdf user_research.pdf --rag-index proj2025
/ppt 销售培训PPT --rag-index proj2025                 # 复用已有索引
/ppt --rag-list                                         # 查看所有索引

# RAG + 联网补充（内部材料打底，联网补充最新进展）
/ppt 新能源战略报告 --rag analysis.docx --rag-mode supplement --mode full

# === 全流程模式（从零开始）===
/ppt 人工智能医疗应用前景 --mode full --pages 20
/ppt 新能源汽车市场分析   --mode research

# === 引擎快速模式 ===
/ppt 年度总结汇报          --style mckinsey --pages 12
/ppt 深度学习医学图像应用  --backend academic --duration 15
/ppt                       --backend slidetailor --source paper.pdf --duration 15
/ppt React Hooks技术分享   --backend slidev
/ppt                       --backend marp --source README.md
/ppt                       --backend sdk --data data.csv 月度销售报告

# 控制评分与迭代
/ppt 年终总结 --mode full --iter auto          # 自动迭代直到≥85分（默认）
/ppt 年终总结 --mode full --iter 3             # 固定迭代3轮
/ppt 年终总结 --mode full --iter 0             # 不迭代，直接输出
/ppt 年终总结 --mode full --score-pass 90      # 目标分数调为90分
```

---

## 模式说明

| `--mode` | 执行阶段 | 适用场景 |
|----------|---------|---------|
| `full` | Phase 1→2→3→4→5→6→7→8→9→10 | 从零开始，无任何素材 |
| `rag` | Phase 1→2B→3→4→5→6→7→8→9→10 | 有本地文件或在线URL |
| `research` | Phase 1→2（或2B）→3 | 只需研究报告，不制作PPT |
| `outline` | Phase 3→4→5→6→7→8→9→10 | 已有大纲，跳过搜索 |
| `diagram` | Phase 4 | 已有内容，只需配图 |
| `make` | Phase 5→6→7→8→9→10 | 已有完整素材，直接制作 |
| *(省略)* | 自动路由 | 有 `--backend` 则快速模式，否则询问 |

---

## 完整10阶段流水线

```
Phase 1  主题定义与任务拆解
    ↓
Phase 2  内容搜集（网络5渠道）
Phase 2B RAG索引检索（有--rag时替代或补充Phase 2）
    ↓
Phase 3  归纳总结与叙事架构
    ↓
Phase 4  图表规划与构建
    ↓
Phase 5  幻灯片初稿（0→1核心制作）← 最重要阶段
    ↓
Phase 6  版式排版
    ↓
Phase 7  视觉美化
    ↓
Phase 8  初版渲染
    ↓
Phase 9  多维评分 + 3-5轮迭代优化  ← 质量保障闭环
    ↓
Phase 10 最终生成与输出
```

---

### Phase 1 — 主题定义与任务拆解

**输入**：用户的自然语言描述  
**输出**：`task_brief.md`（结构化任务书，后续所有阶段的基准文档）

```
需求确认清单（7个核心问题）：

Q1. 核心主题是什么？
    → 一句话描述（例：2024年AI医疗行业现状与投资机会）
    → 主题边界（哪些子话题在范围内/范围外）

Q2. 目标受众是谁？
    ├── exec（C-level/领导层）：少文字、大图表、结论前置、决策导向
    ├── professional（行业专家/同行）：数据详实、有深度分析
    ├── general（大众/非专业）：多类比、少术语、故事化
    └── investor（投资人/LP）：重市场规模、竞争壁垒、回报预期

Q3. 演讲目的是什么？
    ├── report（汇报）：金字塔结构，结论优先
    ├── persuade（说服）：STAR案例+数据支撑
    ├── train（培训）：步骤清晰+互动练习
    ├── share（分享）：故事化+洞察提炼
    └── pitch（路演）：痛点→方案→市场→团队→计划

Q4. 核心信息是什么？（受众离场后应记住的3-5条要点）

Q5. 预期页数和时长？
    参考：1页≈1-2分钟；15页≈15-20分钟；25页≈30分钟

Q6. 需要覆盖哪些子主题？（按优先级排序）

Q7. 风格与约束？
    ├── 视觉风格：mckinsey/google/zen/academic/tech-dark/government
    ├── 语言：zh/en/双语
    ├── 品牌颜色：如有（输入十六进制色值）
    └── 特殊约束：禁忌话题/必须包含的素材/行业规范

输出 task_brief.md 格式：
  主题: ...
  受众: ...
  目的: ...
  核心信息: [1] ... [2] ... [3] ...
  目标页数: N页
  子主题清单: [优先级排序]
  风格: ...
  语言: ...
```

---

### Phase 2 — 内容搜集（网络5渠道）

> 当指定 `--rag` 时，跳转到 **Phase 2B**；`--rag-mode supplement` 时两者并行执行。

多源并行搜索，确保内容全面权威：

```
渠道1：官方权威
  ├── 政府/监管机构：政策文件、白皮书、统计年报
  ├── 国际组织：WHO/UN/WEF/OECD/ITU 报告
  ├── 标准机构：ISO/IEEE/GB 标准文件
  └── 企业官方：年报/IR披露/官方博客/产品文档

渠道2：主流媒体
  ├── 财经媒体：Reuters/Bloomberg/FT/36氪/财新/第一财经
  ├── 科技媒体：MIT Technology Review/Wired/TechCrunch/虎嗅/InfoQ
  ├── 行业媒体：垂直领域专业媒体
  └── 新闻稿：PR Newswire/商业电讯

渠道3：学术研究
  ├── 数据库：Google Scholar/arXiv/PubMed/CNKI
  ├── 顶刊：Nature/Science/NEJM/IEEE/ACM
  ├── 顶会：NeurIPS/ICML/CVPR/ICLR
  └── 优先：高被引综述（快速掌握领域全貌）

渠道4：产业报告
  ├── 咨询：McKinsey/Gartner/BCG/IDC/艾瑞
  ├── 案例：HBR/产品案例库
  └── 机构：VC研报/行业协会白皮书

渠道5：社区与用户声音
  ├── 技术社区：GitHub/Stack Overflow/HN/Reddit
  ├── 专业社交：LinkedIn Pulse/知乎/X(Twitter)
  └── 视频内容：TED/YouTube/B站

搜索执行规则：
  → 中英双语关键词并行（同一概念搜两遍）
  → 优先2年内内容，兼顾经典研究
  → 重要数据至少2个独立来源交叉验证
  → 权威度排序：学术>官方>咨询报告>主流媒体>社区
```

---

### Phase 2B — RAG 索引检索（`--rag` 时执行）

当用户提供现成材料时，替代或补充 Phase 2：

```
输入：--rag 文件列表 / URL列表 / --rag-dir 目录

支持格式：PDF / DOCX / PPTX / MD / TXT / HTML / Excel / CSV
支持URL：单页文章 / 在线PDF / 文档站（递归深度≤2）/ GitHub raw

─── 执行流程 ───────────────────────────────────────────

Step 1: 文档摄入
  本地文件：PDF→PyMuPDF逐页 / DOCX→保留标题层级 / PPTX→每页+备注
  在线URL：WebFetch抓正文 / 在线PDF下载后处理

Step 2: 规模判断 → 策略选择
  ≤8文件 且 ≤4万字  → direct（全文直接LLM分析，最准确）
  ≤20万字           → BM25关键词检索（快速）
  >20万字 或需持久化 → 向量检索（ChromaDB / FAISS）

Step 3: 分块
  每块 500-800 tokens，重叠10-15%
  中文在"。""；"句子边界切分
  保留元数据：文件名、页码/URL、章节标题

Step 4: 向量化
  优先级：BGE-M3本地 → OpenAI API → BM25兜底
  --rag-index 时：持久化到 .ppt_rag/<名称>/（可跨session复用）

Step 5: 主题驱动检索
  按 task_brief.md 的子主题列表分别生成检索query
  query扩展：原词 + 主题+章节 + 关键词变体 + 英文版
  top-k=5/章节；过滤相似度<0.45的噪声；同来源最多3片段

Step 6: 合成输出素材包（格式与Phase 2输出完全一致）
  → outline.md / data.md / quotes.md / refs.md / rag_report.md

─── --rag-mode 控制 ────────────────────────────────────
  replace（默认）：仅用RAG，跳过网络搜索（适合保密/离线）
  supplement    ：RAG+网络搜索并行，合并结果（覆盖更全）

─── 覆盖度报告（自动生成）───────────────────────────────
  ✅ 章节A → N个片段（来自X个文件）
  ⚠️ 章节B → 仅Y个片段（建议补充资料或开启supplement）
  总体覆盖率：X%  来源：N个PDF / M个URL
```

---

### Phase 3 — 归纳总结与叙事架构

**输入**：Phase 2/2B 的原始素材  
**输出**：`ppt_assets/`（outline.md / data.md / quotes.md / refs.md）

```
Step 3.1: 内容分类整理
  → 按 task_brief.md 的子主题列表归组所有素材
  → 标注每条内容的来源权威度（5星制）和时效性（年份）
  → 识别并标记：数据点（量化）/ 引语（可引用原文）/ 案例（STAR可用）

Step 3.2: 核心发现提炼（3-5条，每条需有数据支撑）
  → 主要趋势（有方向性的判断）
  → 关键数据（优先选择最新、最权威、最具冲击力的数字）
  → 典型案例（有前后对比、有量化结果）
  → 挑战/争议（增加客观性和深度）

Step 3.3: 叙事框架选择（与 task_brief.md 的演讲目的对应）
  ├── 金字塔（汇报/说服）：结论→依据→数据，麦肯锡标准
  ├── 问题-原因-解决方案（pitch/提案）：痛点→根因→方案
  ├── 现状-趋势-机会-挑战（行业分析）：宏观到微观
  ├── 背景-方法-结果-结论（学术/研究）：IMRAD结构
  └── 故事线（分享/培训）：英雄旅程，从冲突到解决

Step 3.4: 幻灯片大纲（outline.md）
  每页格式：[序号] [行动标题（完整陈述句）] | [核心信息一句话] | [建议内容类型]
  内容类型标注：文字要点 / 数据图表 / 案例故事 / 框架模型 / 图片配图

Step 3.5: 素材库整理
  data.md  → 所有数据点（数值+单位+年份+来源URL）
  quotes.md → 精选引语和案例（人物/机构+原文+出处）
  refs.md  → 参考文献（APA/IEEE格式，按章节分组）
```

---

### Phase 4 — 图表规划与构建

**输入**：outline.md  
**输出**：`diagrams/` 目录（PNG/SVG + 源码）

```
Step 4.1: 图表需求扫描
  扫描 outline.md，识别信号词：
  架构/组件/模块/系统  → 架构图
  流程/步骤/流水线    → 流程图
  年份/里程碑/历史    → 时间线
  对比/VS/优劣        → 对比矩阵
  分类/体系/层级      → 思维导图
  趋势/增长/占比      → 数据图表
  交互/调用/响应      → 时序图

Step 4.2: 引擎路由
  系统/技术架构       → PlantUML组件图 / diagrams云架构图
  业务/工作流程       → Mermaid flowchart / PlantUML活动图
  时间演进            → Mermaid timeline / 自定义SVG时间轴
  对比格局            → 自定义SVG象限/矩阵
  层级/知识体系       → Markmap思维导图
  概念框架（SWOT等）  → 自定义SVG框架图
  数据可视化          → html-chart（ECharts渲染）

Step 4.3: 生成规范
  □ 节点标签中文 ≤ 8字，边标签 ≤ 6字
  □ 单图节点数 ≤ 15（超出拆分子图）
  □ 颜色与task_brief.md的风格一致（从风格预设提取主色）
  □ 导出PNG分辨率 ≥ 150 DPI（1905×1071px @16:9）
  □ 同时输出SVG矢量版（可缩放，用于高清打印）

Step 4.4: 输出清单
  diagrams/
    ├── 01_[类型]_[主题].png/.svg
    ├── 01_[类型]_[主题].mmd（Mermaid源码）
    └── diagram_index.md（图表清单+对应幻灯片页+修改说明）
```

---

### Phase 5 — 幻灯片初稿（0→1 核心制作）

**这是最关键的阶段。从大纲到可读幻灯片的完整构建过程。**

**输入**：outline.md + data.md + quotes.md + diagrams/  
**输出**：`slides/`（各页内容定义文件）

#### 5.1 幻灯片类型系统

每张幻灯片属于以下类型之一，每种类型有固定的内容模板：

```
A. 封面页（Cover）
   结构：主标题 + 副标题 + 日期/演讲者/场合
   规则：主标题≤18字；副标题≤25字；无数据无要点
   示例：主标题="中国AI医疗市场2024年度报告"
         副标题="机会、挑战与投资展望"

B. 目录/导航页（TOC）
   结构：章节编号 + 章节标题 + 简短说明（可选）
   规则：章节数3-6个；标题≤10字；允许视觉化（圆形/方块流程）
   变体：大纲式（纵向列表）/ 视觉式（图标+卡片）/ 流程式（箭头）

C. 章节转场页（Section Divider）
   结构：章节编号 + 章节标题 + 1句引言（可选）
   规则：背景用主色实色/大图；文字高对比；≤3个元素

D. 核心论点页（Key Point）← 占比最大（60-70%）
   结构：行动标题 + 核心论据（2-4条要点）+ 支撑数据/图片
   规则：
     · 标题：一个完整陈述句，说明"是什么/为什么"（非泛泛标题）
       ✓ "中国AI医疗市场年增速达47%，领跑全球"
       ✗ "市场增长情况"
     · 要点：每条≤20字，优先用数字开头
     · 每页≤4条要点（3条最佳）
     · 至少1个视觉元素（图片/图表/图标）

E. 数据图表页（Data/Chart）
   结构：行动标题 + 图表主体 + 数据解读标注（1-2句）+ 来源
   规则：
     · 标题说明图表的结论而非内容类型
       ✓ "过去5年AI投融资增速超传统IT 3倍"
       ✗ "AI投融资趋势图"
     · 来源标注右下角，字号≤10pt
     · 图表留白充足（不贴边）
     · 解读标注用带颜色的标注框直接指向关键数据

F. 案例故事页（Case Study）
   结构：案例名称 + STAR框架四格（情境/任务/行动/结果）
   规则：
     · Situation（情境）：1-2句背景
     · Task（任务）：面临什么挑战或目标
     · Action（行动）：具体做了什么（3-5步）
     · Result（结果）：量化成果（必须有数字）
     · 每格≤30字，整体克制，留白比例>40%

G. 对比分析页（Comparison）
   结构：行动标题 + 双栏/三栏对比表格/卡片
   规则：
     · 对比维度≤6行
     · 用颜色/图标突出优势项
     · 结论用标注框在最显眼位置给出

H. 框架模型页（Framework）
   结构：行动标题 + 框架图（SVG）+ 简短说明
   支持：SWOT/4P/2×2矩阵/金字塔/飞轮/漏斗/五力/冰山模型
   规则：框架图占页面60-70%；文字解释放旁边或下方

I. 结论与行动建议页（Conclusion/CTA）
   结构：核心结论（1-3条）+ 行动建议（3-5条可执行项）
   规则：
     · 核心结论复述整篇PPT的最重要发现
     · 行动建议要具体、可执行（动词开头，有时间/责任人最好）
     · 不引入任何新信息

J. 致谢/联系页（End）
   结构：结束语 + 联系方式（可选）+ QA引导（可选）
   规则：简洁克制，与封面风格呼应
```

#### 5.2 页面序列构建规则

```
标准页面序列（20页PPT为例）：

[A] 封面          1页
[B] 目录          1页
────────────────────────
[C] 第1章转场     1页
[D][D][D][E][F]   5页（核心内容+数据+案例）
────────────────────────
[C] 第2章转场     1页
[D][D][E][G]      4页
────────────────────────
[C] 第3章转场     1页
[D][D][H][E]      4页
────────────────────────
[I] 结论与建议    1页
[J] 致谢/联系     1页
────────────────────────
共：20页

页数控制原则：
  10分钟演讲 → 8-12页
  20分钟演讲 → 15-20页
  30分钟演讲 → 20-30页
  纯阅读版本 → 页数不限
```

#### 5.3 每页内容密度规范

```
字数预算（总字数包含标题）：

封面页：    ≤ 40字
目录页：    ≤ 80字
转场页：    ≤ 30字
核心论点页：≤ 150字（标题15字 + 3个要点各≤30字 + 注释≤30字）
数据图表页：≤ 80字（标题+解读+来源）
案例故事页：≤ 200字（STAR四格合计）
对比分析页：≤ 180字
框架模型页：≤ 100字
结论页：    ≤ 200字

信息密度检查：
  □ 任意单页文字不超过7行
  □ 没有一段完整的句子（都应拆成要点）
  □ 每页至少25%为留白
  □ 禁止出现小于16pt的正文字体
```

#### 5.4 开场与结尾策略

```
开场策略（封面后第一页内容）：
  冲击数据型：开门见山放最震撼的数字，制造认知冲突
    例："2024年AI在医疗领域创造了$450亿价值，但85%的医院还没用上它"
  故事钩子型：1-2句引发共鸣的场景描写，建立情感连接
  问题驱动型：直接提出受众最关心的问题，营造悬念
  结论先行型（麦肯锡风）：第一页就是结论，后面全是支撑

结尾策略（最后一页内容前）：
  回顾核心信息：用3点式清单重申最重要的3条结论（非重复展示）
  明确行动建议：每条建议包含：做什么+为什么+何时/谁来做
  留下"下一步"：引导受众的后续行动（扫码/联系/试用/讨论）
```

#### 5.5 Ghost Deck 自检规则

```
幽灵甲板测试（Ghost Deck Test）：
  仅读每页标题，能否还原整个PPT的完整论证链？

合格标准：
  □ 每个标题是完整陈述句（有主语、动词、结论）
  □ 标题按顺序读下来构成一个完整的故事
  □ 没有任何一个标题是"关于XX的介绍"这类空洞标题
  □ 数据页标题包含数据本身（不只是"趋势图"）

失败标志（需要修改标题）：
  ✗ "市场概况"  → ✓ "全球AI医疗市场已达2300亿，中国占比超30%"
  ✗ "竞争分析"  → ✓ "三大头部玩家占据80%市场，新进入者空间有限"
  ✗ "我们的优势" → ✓ "独有数据优势+算法专利构成两道护城河"
```

---

### Phase 6 — 版式排版

**输入**：Phase 5 的内容定义  
**输出**：带版式的幻灯片草图（SVG/代码层面）

```
6.1 网格系统
  基准网格：16列 × 9行（16:9画面）
  安全边距：上下各 1.2cm，左右各 1.5cm
  内容区域：去边距后的中心 86% 区域
  模块对齐：所有元素对齐网格线，允许跨格但不允许半格

6.2 字体层级（4级）
  L1 大标题（封面）：44-54pt / 加粗 / 主色或白色
  L2 页面标题（行动标题）：28-36pt / 加粗 / 深色
  L3 正文/要点：18-22pt / 常规或半粗 / 深灰色
  L4 注释/来源：10-12pt / 常规 / 浅灰色
  原则：同一文档字体种类≤2种（标题体+正文体）

6.3 布局模板（6种）
  ① 全图型：背景全出血大图+标题叠加（封面/转场页）
  ② 左文右图：文字区40% | 图片/图表区60%
  ③ 上标题下内容：标题占20%高度 | 内容区80%（数据/图表页）
  ④ 双栏对比：左右各50%，中间分割线（对比分析页）
  ⑤ 三格并列：三个等宽模块（步骤/特点/方案对比）
  ⑥ 大数字型：中心一个大数字（60pt+）+上下小字说明（关键数据页）

6.4 视觉层级规则
  □ 最重要信息（1个）：最大、最深色、视觉中心
  □ 次要信息（2-3个）：中等大小
  □ 支撑信息（其余）：最小、最浅
  □ 强调元素：仅用强调色，全页只有1-2处
  □ 留白是设计的一部分（重要信息周围保留呼吸空间）

6.5 图文平衡检查
  □ 纯文字页占比 < 25%（超出则插入图标或图表）
  □ 单页文字行数 ≤ 7行
  □ 无"文字墙"（连续3行以上无任何视觉分隔）
  □ 所有图片/图表占页面面积 ≥ 30%
```

---

### Phase 7 — 视觉美化

**输入**：Phase 6 的排版草图  
**输出**：完成视觉设计的幻灯片

```
7.1 色彩系统（4色方案）
  主色（Primary）：  品牌色/行业色，用于标题、关键要素（1种）
  辅助色（Secondary）：与主色和谐，用于次要元素、背景变化（1-2种）
  强调色（Accent）：  高对比，仅用于最需突出的1-2处（1种）
  中性色（Neutral）：  白/浅灰/深灰，用于背景、正文、分割线

  风格预设对照：
  mckinsey    → 主色 #003087（深蓝）| 强调 #FF6600（橙）| 背景白
  google      → 主色 #4285F4（蓝）| 辅助 #34A853/FBBC05/EA4335 | 背景白
  zen         → 主色 #2C3E50（深灰蓝）| 辅助 #ECF0F1 | 极简
  academic    → 主色 #1565C0（学术蓝）| 背景白 | IEEE标准
  tech-dark   → 主色 #00D4AA（霓虹绿）| 背景 #1A1A2E | 深色
  government  → 主色 #CC0000（政务红）或 #003087（政务蓝）| 庄重

7.2 图片资源策略
  AI生成图片：主题配图（DALL-E/Gemini/通义万象）
    → 提示词模板："[场景], [风格], professional, clean background, [主色系]"
  免版权图片：Unsplash/Pexels/Pixabay（关键词搜索）
  图标：Flaticon/Iconfont（统一同一套图标风格）
  数据图表：matplotlib/ECharts（配色与主色系匹配）
  
  图片质量标准：
  □ 最小尺寸1920×1080px（全屏背景图）
  □ 非装饰性图片必须与内容直接相关
  □ 不使用低质量/模糊/过度滤镜图片

7.3 美化优先级清单（按顺序执行）
  ① 统一色彩：全文严格使用4色方案，无随意颜色
  ② 字体对齐：检查每页字体层级是否正确，清除遗漏的小字
  ③ 图表配色：将所有图表颜色替换为与PPT主色系匹配
  ④ 封面+转场页：重点美化，使用全图或强视觉元素
  ⑤ 图标统一：替换不一致的图标为同风格同大小
  ⑥ 强调标注：用颜色框/箭头/加粗突出每页最重要的1个信息
  ⑦ 细节收尾：对齐所有元素、清理多余线条、统一边距

7.4 可访问性检查
  □ 正文文字与背景对比度比 ≥ 4.5:1（WCAG AA标准）
  □ 不能仅靠颜色区分信息（需配合形状/标注）
  □ 字体 ≥ 16pt（小字需有充分上下文）
```

---

### Phase 8 — 初版渲染

路由至对应引擎生成可交付的初版文件：

```
引擎路由（与 task_brief.md 的场景对应）：
  学术演讲（无PDF）  → academic-pptx
  学术演讲（有PDF）  → SlideTailor + academic-pptx
  商务/通用          → ppt-master（SVG→PPTX流水线）
  技术/代码演示      → Slidev（slides.md + Vue组件）
  Markdown快速出片   → Marp
  编程/批量/数据驱动 → python-pptx / PptxGenJS

渲染完成后，进入 Phase 9 评分。
```

---

### Phase 9 — 多维评分 + 迭代优化（3-5轮闭环）

**这是质量保障的核心机制。**

#### 9.1 评分维度与评分规则（满分100分）

```
┌──────────────────────────────────────────────────────────────────┐
│  维度            权重   评分项（每项0-满分，合计=该维度满分）         │
├──────────────────────────────────────────────────────────────────┤
│ D1 内容质量       25分                                             │
│    论点清晰度      8分  每页有且只有1个核心信息（无模糊/多义）        │
│    数据支撑        8分  核心论点有量化数据，数据有来源               │
│    完整覆盖        5分  子主题全覆盖，无重要遗漏                     │
│    案例质量        4分  有具体案例，结果量化                         │
├──────────────────────────────────────────────────────────────────┤
│ D2 逻辑结构       25分                                             │
│    Ghost Deck     10分  仅读标题可还原完整论证（每个无效标题-2分）   │
│    叙事框架        8分  开场-发展-结论结构清晰，有明确主线           │
│    页面递进        4分  前后页面有逻辑联系，非独立碎片               │
│    结论清晰        3分  最后有明确结论和行动建议                     │
├──────────────────────────────────────────────────────────────────┤
│ D3 视觉设计       20分                                             │
│    色彩一致        6分  全文严格遵守4色方案，无随意用色              │
│    字体层级        5分  4级字体层级清晰，无混乱                      │
│    图文平衡        5分  纯文字页<25%，有足够视觉元素                 │
│    排版对齐        4分  所有元素对齐网格，无错位                     │
├──────────────────────────────────────────────────────────────────┤
│ D4 信息密度       15分                                             │
│    文字克制        5分  无"文字墙"，每页≤7行，要点≤20字/条          │
│    视觉精炼        5分  图表简洁，无多余元素，留白≥25%              │
│    层次清晰        5分  重要信息突出，次要信息退后，有视觉焦点        │
├──────────────────────────────────────────────────────────────────┤
│ D5 受众匹配       15分                                             │
│    语言层次        5分  专业术语与受众认知水平匹配                   │
│    信息深度        5分  内容深度与受众期望匹配（不过浅不过深）        │
│    行动导向        3分  有清晰的call-to-action                      │
│    时长适配        2分  页数/信息量与演讲时长匹配                    │
└──────────────────────────────────────────────────────────────────┘

评分结果等级：
  90-100  优秀（A）→ 直接进入 Phase 10 最终输出
  80-89   良好（B）→ 执行1轮迭代，聚焦最弱维度
  70-79   中等（C）→ 执行2轮迭代
  60-69   及格（D）→ 执行3轮迭代
  50-59   较差（E）→ 执行4轮迭代，含内容重构
  <50     不合格（F）→ 执行5轮迭代，或返回Phase 3重新归纳
```

**评分报告格式**：
```
╔══════════════════════════════════════════════════════╗
║  PPT 质量评分报告  v[轮次]                           ║
╠══════════════════════════════════════════════════════╣
║  D1 内容质量    [XX]/25  ████████░░  [等级]         ║
║  D2 逻辑结构    [XX]/25  ████████░░  [等级]         ║
║  D3 视觉设计    [XX]/20  ████████░░  [等级]         ║
║  D4 信息密度    [XX]/15  ████████░░  [等级]         ║
║  D5 受众匹配    [XX]/15  ████████░░  [等级]         ║
╠══════════════════════════════════════════════════════╣
║  总分          [XXX]/100               [等级]        ║
╚══════════════════════════════════════════════════════╝

主要问题：
  ⚠️ [维度X] [具体页码] [具体问题描述]
  ⚠️ [维度Y] [具体页码] [具体问题描述]

最弱维度：[D?] → 下一轮迭代聚焦此维度
```

#### 9.2 迭代优化循环（3-5轮）

```
参数控制：
  --iter auto（默认）：自动迭代直到总分≥85或达5轮
  --iter N           ：固定迭代N轮（0=不迭代，1-5）
  --score-pass X     ：自定义通过分数（默认85）

迭代循环逻辑：
  ┌──────────────────────────────────────────────────────┐
  │  WHILE 轮次 < max_iter AND 总分 < score_pass:        │
  │    1. 读取上轮评分报告，定位最弱维度                   │
  │    2. 针对该维度执行改进策略（见下表）                  │
  │    3. 仅修改受影响的幻灯片（精准改，不全量重做）        │
  │    4. 重新运行评分                                    │
  │    5. 如本轮提升 < 3分（改进停滞），切换到次弱维度      │
  └──────────────────────────────────────────────────────┘
```

**各维度改进策略**：

```
D1 内容质量改进（当D1最弱时）：
  → 补充缺失数据：回到 Phase 2/2B 补搜或RAG查询
  → 强化论点：为每个"空洞论点"找到量化支撑
  → 丰富案例：增加具体案例（STAR格式，有量化结果）
  → 聚焦核心：删除与核心论点无关的内容
  修改范围：主要内容页（D/F类型）

D2 逻辑结构改进（当D2最弱时）：
  → 修改无效标题：将所有"泛标题"改为"行动标题"（陈述句）
  → 调整页面顺序：重新排列幻灯片使论证链更清晰
  → 增强过渡：在章节间加过渡说明，建立前后联系
  → 强化开场/结尾：优化第一页冲击性和最后一页行动导向
  修改范围：所有标题 + 开场页 + 结尾页

D3 视觉设计改进（当D3最弱时）：
  → 统一色彩：审查所有页面，清除偏离4色方案的颜色
  → 修复层级：按字体层级规范重新设置所有文字大小
  → 增加视觉：将纯文字页替换为图文混排版式
  → 优化图表：重新配色使图表颜色与主色系匹配
  修改范围：视觉密集审查全文

D4 信息密度改进（当D4最弱时）：
  → 精简文字：每条要点控制在20字内，删除冗余表述
  → 替换文字为视觉：超过4条要点的页面用图表/框架图替代
  → 增加留白：减少内容量，扩大元素间距
  → 突出焦点：每页添加1处颜色/大小强调标注
  修改范围：文字密集的内容页

D5 受众匹配改进（当D5最弱时）：
  → 调整语言深度：简化术语（面向大众）或增加专业深度（面向专家）
  → 增删细节：按受众需求增加/删减支撑信息
  → 强化CTA：在结尾页添加明确、具体、可执行的建议
  → 调整页数：删除超时内容或补充重要内容
  修改范围：重点修改受众体验薄弱的页面
```

**迭代历史记录**：
```
迭代记录表（每轮自动追加）：
  轮次  总分  D1   D2   D3   D4   D5   改进聚焦      主要改动
  v1    72   18   19   13   11   11   D3视觉+D4密度  重做封面/统一色彩
  v2    81   20   21   16   13   11   D5受众         修改CTA+简化术语
  v3    87   21   22   16   14   14   D1内容         补充2个数据案例
  → 总分87≥85，达到通过线，结束迭代
```

#### 9.3 迭代终止条件

```
满足任一条件时终止迭代，进入 Phase 10：
  ① 总分 ≥ score-pass（默认85）              → 正常通过
  ② 已执行 max_iter 轮（--iter 指定或默认5）  → 到达上限
  ③ 连续2轮总分提升 < 3分（改进停滞）        → 主动终止
  ④ 用户手动干预（用 --iter 0 跳过迭代）      → 强制跳过

终止时报告：
  "已完成 [N] 轮迭代，最终得分 [X]/100
   各维度：D1=[x] D2=[x] D3=[x] D4=[x] D5=[x]
   主要改进：[改动摘要]
   进入最终输出..."
```

---

### Phase 10 — 最终生成与输出

**触发时机**：Phase 9 评分通过 或 迭代轮次耗尽

```
10.1 最终渲染（对应引擎执行完整输出）
  academic / slidetailor → [名称]_final.pptx
  ppt-master             → exports/[名称]_final.pptx
  slidev                 → dist/index.html（+ pdf/pptx可选）
  marp                   → [名称]_final.pdf（+ html/pptx可选）
  sdk                    → [名称]_final.pptx + generate_ppt.py

10.2 标准输出包
  ├── [名称]_final.pptx   主文件（Office可编辑）
  ├── [名称]_final.pdf    PDF备用版本（方便分发）
  ├── assets/
  │   ├── diagrams/       所有图表源码（.mmd/.puml）+ 渲染PNG/SVG
  │   ├── data.md         数据引用（来源+页码）
  │   └── refs.md         参考文献
  ├── notes.md            演讲备注（每页要点+建议话术）
  └── score_report.md     最终评分报告+迭代历史

10.3 附加输出（可选）
  slides.html            Web版本（Slidev）
  generate_ppt.py/.js    生成脚本（sdk模式）
  ppt_assets/            研究素材包（全流程/RAG模式）
  .ppt_rag/<名称>/        持久化索引（--rag-index时）

10.4 交付说明
  → 演讲时间估算（页数×1.5分钟经验值）
  → 推荐演讲重点页（哪3页必须停留超过2分钟）
  → 常见问答预演（基于内容预判3-5个QA及参考回答）
  → 编辑提示（如何在PPT中修改图表颜色/替换图片）
```

---

## 引擎选择指南（`--backend`）

| `--backend` | 最适合 | 输出格式 |
|-------------|--------|---------|
| `academic` | 学术演讲（无论文PDF） | .pptx |
| `slidetailor` | 学术演讲（有论文PDF，自动提取） | .pptx |
| `ppt-master` | 商务通用、设计优先 | .pptx |
| `slidev` | 技术/代码演示、前端展示 | .html/.pdf/.pptx |
| `marp` | Markdown 快速出片 | .html/.pdf/.pptx |
| `sdk` | 编程式、数据驱动、批量生成 | .pptx |

**自动路由规则**（未指定 `--backend` 时）：
```
有 --source *.pdf AND 学术关键词      → slidetailor
有学术关键词（论文答辩/研究报告）     → academic
有代码/技术/开发者关键词              → slidev
有 --source *.md OR Markdown关键词   → marp
有数据/批量/CSV/报表关键词           → sdk
其他（商务/产品/汇报/通用）           → ppt-master
```

---

## 全部参数

### 通用参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--mode` | 执行模式（full/rag/research/outline/diagram/make） | 自动检测 |
| `--backend` | 指定引擎（覆盖自动路由） | 自动检测 |
| `--source <路径>` | 源文档（PDF/DOCX/MD/URL/CSV） | — |
| `--output <文件名>` | 输出文件名（无扩展名） | 自动生成 |
| `--lang zh\|en` | 幻灯片语言 | `zh` |
| `--pages <数量>` | 目标页数 | 自动 |
| `--style <风格>` | 视觉风格（mckinsey/google/zen/academic/tech-dark/government） | 自动 |
| `--audience` | 目标受众（exec/professional/general/investor） | `professional` |
| `--purpose` | 演讲目的（report/persuade/train/share/pitch） | `report` |

### 评分与迭代参数（新增）

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--iter 0\|1\|2\|3\|4\|5\|auto` | 迭代轮数；auto=自动迭代直到通过 | `auto` |
| `--score-pass <分数>` | 通过分数线（达到后停止迭代） | `85` |
| `--score-only` | 仅评分不迭代（输出评分报告，不修改PPT） | `false` |

### RAG 参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--rag <来源>` | 本地文件或URL（空格分隔多个）；PDF/DOCX/PPTX/MD/HTML/Excel | — |
| `--rag-dir <目录>` | 递归索引整个目录（最多500个文件） | — |
| `--rag-index <名称>` | 持久化索引名称（.ppt_rag/<名称>/，可复用） | 临时 |
| `--rag-mode replace\|supplement` | replace=仅RAG；supplement=RAG+网络搜索补充 | `replace` |
| `--rag-top-k <n>` | 每章节检索片段数 | `5` |
| `--rag-backend chroma\|faiss\|bm25\|auto` | 向量存储后端 | `auto` |
| `--rag-list` | 列出所有已保存索引 | — |

### 学术场景参数（academic / slidetailor）

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--type conference\|seminar\|defense\|grant` | 演讲类型 | `conference` |
| `--duration <分钟>` | 演讲时长（控制页数） | `15` |
| `--audience specialist\|mixed\|general` | 受众类型 | `specialist` |
| `--citation apa\|ieee\|chicago` | 引用格式 | `ieee` |

### 商务场景参数（ppt-master）

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--format ppt169\|ppt43\|xiaohongshu\|moments` | 画布格式 | `ppt169` |
| `--image-backend gemini\|openai\|qwen\|zhipu` | 图片生成后端 | `gemini` |

### 技术演示参数（slidev）

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--theme default\|seriph\|bricks\|forest\|geist\|apple-basic` | 主题 | `default` |
| `--export html\|pdf\|pptx` | 导出格式 | `html` |

### Markdown 出片参数（marp）

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--theme default\|gaia\|uncover` | 主题 | `default` |
| `--export html\|pdf\|pptx` | 导出格式 | `pdf` |
| `--size 16:9\|4:3` | 幻灯片比例 | `16:9` |

### 编程式参数（sdk）

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--engine python-pptx\|pptxgenjs` | SDK 引擎 | `python-pptx` |
| `--template <路径>` | 基础模板 .pptx | — |
| `--data <路径>` | 数据源（CSV/JSON/Excel） | — |

---

## 输出格式汇总

```
全流程/RAG模式（Phase 10 输出）：
  [名称]_final.pptx        主文件
  [名称]_final.pdf         PDF备用
  assets/diagrams/         图表（PNG+SVG+源码）
  assets/data.md           数据引用
  assets/refs.md           参考文献
  notes.md                 演讲备注
  score_report.md          评分+迭代历史
  ppt_assets/              研究素材包（含outline/data/quotes/refs）
  .ppt_rag/<名称>/          RAG持久化索引（--rag-index时）

仅研究模式（--mode research）：
  ppt_assets/research_report.md
  ppt_assets/outline.md
  ppt_assets/refs.md
  ppt_assets/rag_report.md （RAG模式时）

仅图表模式（--mode diagram）：
  diagrams/[序号]_[类型]_[主题].png/.svg
  diagrams/diagram_index.md
```

---

## 与其他命令的协同

```
/ppt (研究阶段)     → /market-research   更深度的竞品/市场研究
/ppt (图表阶段)     → /arch-diagram      专业云架构图生成
                    → /diagram --type uml       PlantUML 轻量图表
                    → /diagram --type mindmap   Markmap 思维导图
/ppt (美化阶段)     → @article-illustrator    图表+配图一体化美化
/ppt (学术场景)     → /paper-collect     论文搜集与整理
/ppt (汇报场景)     → /prd --mode standard      产品文档一键转PPT
/ppt (报告场景)     → @content-director  长文拆解+叙事优化
/ppt (批量图表)     → @diagram-architect 批量图表套件生成
```

---

## 依赖速查

```bash
# RAG模式（--rag / --rag-dir）
pip install PyMuPDF python-docx python-pptx markitdown beautifulsoup4 pandas openpyxl
pip install chromadb          # 向量存储首选（持久化）
pip install faiss-cpu         # 向量存储次选（速度最快）
pip install rank-bm25         # 最轻量备选（关键词检索）
pip install sentence-transformers  # 本地嵌入（BGE-M3多语言）

# 全流程模式（网络搜索）
pip install requests beautifulsoup4 markdownify

# 图表构建
npm install -g @mermaid-js/mermaid-cli    # Mermaid
pip install diagrams                       # 云架构图
brew install graphviz                      # Graphviz渲染（macOS）
winget install graphviz                    # Graphviz渲染（Windows）

# academic / slidetailor
pip install "markitdown[pptx]" python-pptx
pip install transformers torch PyMuPDF     # slidetailor额外依赖

# ppt-master（商务通用）
pip install python-pptx PyMuPDF mammoth svglib reportlab Pillow
npm install -g pptxgenjs

# slidev（技术演示）
npm install -g @slidev/cli
npx playwright install chromium            # 导出PDF/PPTX需要

# marp
npm install -g @marp-team/marp-cli

# sdk
pip install python-pptx Pillow pandas openpyxl
npm install pptxgenjs
```

---

## 综合对比

| 维度 | full全流程 | RAG模式 | academic | slidetailor | ppt-master | slidev | marp | sdk |
|------|-----------|--------|---------|------------|----------|--------|------|-----|
| 适用起点 | 无素材 | 有文件/URL | 有主题 | 有论文PDF | 有主题/文档 | 有主题 | 有MD | 有数据 |
| 内容质量 | ★★★★★ | ★★★★★ | ★★★ | ★★★★ | ★★★ | ★★ | ★★ | ★★★★ |
| 生成速度 | 慢(20-60m) | 中(5-15m) | 快 | 中 | 中 | 快 | 极快 | 慢(需编程) |
| 设计质量 | ★★★★ | ★★★★ | ★★★ | ★★★ | ★★★★★ | ★★★ | ★★ | 自定义 |
| 自迭代优化 | ✅ 3-5轮 | ✅ 3-5轮 | ✅ 3-5轮 | ✅ 3-5轮 | ✅ 3-5轮 | ⚠️ 有限 | ⚠️ 有限 | ❌ |
| 引用溯源 | ✅ 全自动 | ✅ 到页码 | ✅ 强制 | ✅ 提取 | ❌ | ❌ | ❌ | ⚠️ 手动 |
| 保密/离线 | ❌ 联网 | ✅ 可全离线 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| 跨session | ❌ | ✅ --rag-index | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| 批量生成 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ⚠️ 有限 | ✅ 最佳 |
| 代码展示 | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ 最佳 | ✅ 良好 | ❌ |
