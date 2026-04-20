---
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, AskUserQuestion, Skill
description: 标书智能编制命令。七阶段人工+AI协同：深度拆解→澄清确认→偏离表+大纲→撰写→评审→核查→定稿输出，另附偏离表同义改写。支持三色标记、RAG知识库、查重检测。
argument-hint: "<子命令> [选项] [文件]"
---

# /bid

标书智能编制命令。七阶段人工+AI协同流水线，覆盖从读标到移交的完整投标作业流程。

**核心理念：偏离表决定方案，而非方案决定偏离表。** 技术偏离表是技术标书的"宪法"，所有方案内容必须与偏离表完全一致。

---

## 全局流程总览

```
招标文件
  │
  ▼
① analyze ──→ 🔴废标项 / 🟡高分项 / 🔵基础项（三色标记）
              技术要求原始清单.xlsx + 澄清问题清单初稿
  │
  ▼
② clarify ──→ 内部评审 → 正式澄清提交 → 解读回复
              最终技术要求清单.xlsx          ← 后续所有阶段以此为准
  │
  ▼
③ outline ──→ 技术偏离表（初稿）+ 评分对标大纲 + 分工排期表
              ★ 偏离表与大纲阶段先行确定，写作内容不得与之矛盾
  │
  ▼
④ write ────→ 逐章节 RAG 生成（痛点→方案逻辑）+ 配图
              bid-draft-[章节].md × N
  │
  ▼
⑤ review ───→ 第一轮：交叉审核 → 第二轮：专家评审 → 修改完善
              评审意见表.xlsx
  │
  ▼
⑥ check ────→ 合规核查 ✅/❌ + 一致性验证 + 查重检测
              bid-check-report.md
  │
  ▼
⑦ export ───→ 最终通读 + 格式化输出 + 商务移交包
              [项目名]-技术标-正本.docx/pdf + 移交清单.md
  │
  └─[可选]─→ rewrite — 偏离表"无偏离"应答同义改写
```

| 阶段 | 命令 | 人工估时 | 核心交付物 |
|------|------|----------|-----------|
| 1. 深度拆解 | `analyze` | 0.5–1天 | 技术要求原始清单 + 澄清问题初稿 |
| 2. 澄清确认 | `clarify` | 1–2天（可并行） | 最终技术要求清单 |
| 3. 偏离表+大纲 | `outline` | 0.5–1天（可并行） | 偏离表初稿 + 大纲 + 排期表 |
| 4. 分模块撰写 | `write` | 3–5天 | 各章节草稿 + 配图 |
| 5. 双轮评审 | `review` | 2–3天 | 评审意见表 + 修改后标书 |
| 6. 验证核查 | `check` | 0.5–1天 | 合规+一致性+查重报告 |
| 7. 定稿输出 | `export` | 0.5天 | 正式标书 + 移交包 |
| 附加（可选） | `rewrite` | 按需 | 偏离表改写对照表 |

**总工期：约 8–14 个工作日**

---

## 子命令速查

```
/bid <子命令> [选项] [文件]

流水线阶段：
  analyze   第1阶段：深度拆解招标文件，三色标记 + 提取需求清单
  clarify   第2阶段：管理技术澄清，生成/更新最终技术要求清单
  outline   第3阶段：偏离表先行 + 评分对标大纲 + 分工排期
  write     第4阶段：逐章节 RAG 增强内容生成（含配图）
  review    第5阶段：多角色评审（交叉审核 + 专家评审）
  check     第6阶段：合规核查 + 一致性验证 + 查重检测
  export    第7阶段：最终定稿检查 + 导出 Word/PDF + 移交清单
  rewrite   附加：技术偏离表"无偏离"应答项同义改写

快捷工具：
  full      全流程：自动执行以上七阶段（含检查点保存）
  kb        知识库管理：添加/列出/清空公司资料
```

| 场景 | 命令 |
|------|------|
| 一键全流程 | `/bid full 招标文件.pdf --kb company-docs/` |
| 深度解析（含三色标记） | `/bid analyze 招标.pdf --color --clarify-list` |
| 更新澄清回复 | `/bid clarify --reply 澄清回复.pdf --update 技术要求原始清单.xlsx` |
| 生成大纲+偏离表 | `/bid outline --from 最终技术要求清单.xlsx --with-deviation` |
| 写技术方案（含配图） | `/bid write --section solution --figures` |
| 写案例章节 | `/bid write --section performance --kb company-docs/案例库/` |
| 两轮评审 | `/bid review --perspective all --round cross` |
| 合规核查+查重 | `/bid check --file 标书.md --against 招标文件.pdf --plagiarism` |
| 最终定稿+移交包 | `/bid export --format both --final-check --handover` |
| 偏离表同义改写 | `/bid rewrite --file 技术偏离表.docx` |

---

## 执行逻辑

加载 `skills/bid-writer/SKILL.md` 完整规范，路由到 `bid-writer` Agent 执行，并按需调用专项 Skill：

```
命令解析 → 识别子命令 → bid-writer Agent
  ↓
调用 bid-writer Skill（七阶段知识库与规范）
  ↓
按需调用专项 Skill：
  bid-rewriter    — 偏离表五原则同义改写
  mermaid-chart   — 架构图/流程图/拓扑图生成
  html-chart      — 可视化图表生成
  ↓
输出：草稿 + 配图 + 格式化文档 + 审查报告 + 改写对照表 + 移交清单
```

---

## 第1阶段：analyze

```
/bid analyze <招标文件路径> [--output <报告路径>] [--color] [--clarify-list]
```

三色标记：🔴废标项（100%响应）/ 🟡高分项（重点投入）/ 🔵基础项（标准响应）

逐条提取技术要求为结构化清单（章节号/条款号/原文/初稿响应/偏离类型），标记模糊条款生成澄清问题初稿。

**输出：** `bid-analysis-[项目名].md` + `技术要求原始清单.xlsx` + `技术澄清问题清单（初稿）.docx`

---

## 第2阶段：clarify

```
/bid clarify [--from <澄清问题清单>] [--reply <澄清回复文件>] [--update <需求清单>]
```

生成逐条技术能力评估表，整理正式澄清问题（客观/中立/按优先级排序），解读招标方回复并更新最终清单。

**输出：** `技术澄清问题（正式版）.docx` + `最终技术要求清单.xlsx`

---

## 第3阶段：outline

```
/bid outline [--from <需求清单>] [--type tech|commercial|full] [--pages <页数>] [--with-deviation]
```

偏离表先行（无偏离/正偏离/❌禁止负偏离），严格按评分细则顺序设计章节，生成分工排期表。

**输出：** `bid-outline-[项目名].md` + `技术偏离表（初稿）.docx` + `技术方案编写分工与排期表.xlsx`

---

## 第4阶段：write

```
/bid write [--section <章节>] [--kb <知识库路径>] [--from <大纲文件>] [--mode interactive|batch] [--figures]
```

章节选项：`understanding` / `solution` / `implementation` / `management` / `quality` / `service` / `performance` / `team` / `commercial` / `all`

RAG 增强生成（基于知识库真实资料），`--figures` 自动生成架构图/流程图/拓扑图。

**输出：** `bid-draft-[章节名].md` / `bid-draft-full.md`

---

## 第5阶段：review

```
/bid review [--file <草稿文件>] [--perspective <角色>] [--level strict|normal] [--round cross|expert]
```

第一轮交叉审核（business/technical/delivery/risk/competitive 五视角），第二轮专家评审（技术合理性、差异化优势、评分点覆盖）。

**输出：** `bid-review-[项目名].md` + `技术标书评审意见表.xlsx`

---

## 第6阶段：check

```
/bid check [--file <标书文件>] [--against <招标文件>] [--plagiarism] [--integrity]
```

合规性核查（逐条✅/❌）+ 一致性验证（术语/数据/逻辑/承诺）+ 查重检测（>70%红/40–70%黄/<40%绿）。

**输出：** `bid-check-report-[项目名].md`

---

## 第7阶段：export

```
/bid export [--file <源文件>] [--format docx|pdf|both] [--template <模板路径>] [--final-check] [--handover]
```

最终通读（废标项/偏离表一致性/签章完整性/格式规范），生成正本/副本，商务移交包。

**输出：** `[项目名]-技术标-正本.docx/pdf` + `移交清单.md`

---

## 附加阶段：rewrite

```
/bid rewrite [--file <偏离表文件>] [--items <条款编号,...>] [--output <输出路径>]
```

对偏离表"无偏离"应答项进行同义改写，加载 `skills/bid-rewriter/SKILL.md` 五原则执行。

**输出：** `bid-rewrite-[项目名].md`（原文/改写对照表格式）

---

## 快捷工具

```
/bid full <招标文件> [--kb <知识库路径>] [--mode interactive|auto]
/bid kb add <文件或目录>
/bid kb list
/bid kb clear
```
