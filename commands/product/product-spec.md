---
name: product-spec
description: >
  产品规格统一入口 — 从一句话需求到完整产品规格文档。
  合并自 /prd（PRD文档）+ /prd-spec（Spec-First四件套）+ /proto-prd（线框图+PRD融合）。
  通过 --mode 路由到对应工作流：prd（标准PRD）/ spec（规格四件套）/ proto（线框图优先）/ lite（一页纸）。
  
  与相邻命令的边界（防混淆）：
  - vs /prd-writer：本命令是"模板式一次输出"；/prd-writer 是"对话式渐进引导"。
    想法清晰用本命令，想法模糊用 /prd-writer。
  - vs /ai-feature-spec：通用 PRD 用本命令；
    LLM/Agent/RAG 类 AI 功能用 /ai-feature-spec（含 Eval / 失败模式 / 成本）。
  - vs /user-story-mapping：本命令产出"完整规格文档"；
    /user-story-mapping 产出"故事树 + 切片"。两者可串联（先地图后规格）。
user-invocable: true
argument-hint: "<需求描述> [--mode prd|spec|proto|lite] [--prd-mode lite|full|gtm|workflow] [--spec-mode propose|spec|design|tasks|full] [--proto-mode wireframe-first|prd-first|combined] [--fidelity low|mid] [--output inline|dir] [--format md|notion|linear] [--lang zh|en]"
allowed-tools: [Read, Write, Edit, AskUserQuestion]
---

# /product-spec — 产品规格统一入口

加载技能：`skills/product-spec/SKILL.md`

## 模式速查

```
/product-spec <需求> --mode lite        一页纸快速对齐（默认）
/product-spec <需求> --mode prd         标准 PRD 文档（原 /prd）
/product-spec <需求> --mode spec        Spec-First 四件套（原 /prd-spec）
/product-spec <需求> --mode proto       线框图 + PRD 融合（原 /proto-prd）
```

---

## 模式决策树

```
用户需求是什么？
  │
  ├── 需要快速一页纸对齐（早期探索/内部沟通）
  │   → --mode lite
  │
  ├── 需要标准 PRD 文档（已有设计方向，直接写需求文档）
  │   → --mode prd [--prd-mode lite|full|gtm|workflow]
  │
  ├── 需要新功能完整规格化（立项前对齐 + 研发任务拆解）
  │   → --mode spec [--spec-mode propose|spec|design|tasks|full]
  │
  └── 需要从 UI 界面推导需求（设计驱动，先画线框再写规格）
      → --mode proto [--proto-mode wireframe-first|prd-first|combined]
```

---

## 参数说明

### 主模式 `--mode`

| 值 | 来源 | 输出 | 适用场景 |
|----|------|------|---------|
| `lite` | — | 一页纸 PRD | 早期探索、快速对齐（**默认**） |
| `prd` | 原 `/prd` | 完整 PRD 文档 | 已有设计方向，正式研发交付 |
| `spec` | 原 `/prd-spec` | proposal/specs/design/tasks 四件套 | 新功能启动前的结构化规格对齐 |
| `proto` | 原 `/proto-prd` | ASCII 线框图 + PRD 融合文档 | UI 驱动、从界面推导需求规格 |

### PRD 子模式 `--prd-mode`（`--mode prd` 时生效）

| 值 | 说明 | 适用场景 |
|----|------|---------|
| `lite` | 一页纸 PRD | 内部评审、快速对齐 |
| `full` | 完整 PRD（背景/目标/用户故事/功能规格/验收标准/风险）| **默认**，正式研发交付 |
| `gtm` | GTM 计划（定位/ICP/渠道/定价/目标/90天启动节奏）| 产品上线准备 |
| `workflow` | 用户旅程 + Mermaid 流程图 | 交互评审、设计对齐 |

### Spec 子模式 `--spec-mode`（`--mode spec` 时生效）

| 值 | 输出内容 | 适用场景 |
|----|---------|---------|
| `propose` | proposal.md（背景/目标/范围/不做什么） | 立项对齐、需求评审 |
| `spec` | specs/（用户故事 + 验收标准 + 场景） | 研发交付、测试设计 |
| `design` | design.md（线框图 + 交互流 + UI 规格） | 设计对接、原型评审 |
| `tasks` | tasks.md（可勾选实施清单 + P0/P1/P2）| Sprint 规划、工程执行 |
| `full` | 完整四件套文档 | **默认**，新功能完整启动 |

### Proto 工作流 `--proto-mode`（`--mode proto` 时生效）

| 值 | 流程 | 适用场景 |
|----|------|---------|
| `wireframe-first` | 先生成线框图 → 确认后生成 PRD | **默认**，从 UI 布局反推需求规格 |
| `prd-first` | 先生成 PRD → 再配套生成线框图 | 需求驱动，从需求文字派生视觉原型 |
| `combined` | 线框图和 PRD 同步并行输出 | 赶时间场景，一次性产出两份文档 |

### 其他参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--fidelity low\|mid` | `mid` | 原型保真度（仅 proto 模式生效） |
| `--output inline\|dir` | `inline` | 输出方式（仅 spec 模式生效） |
| `--format md\|notion\|linear` | `md` | 输出格式（仅 prd 模式生效） |
| `--lang zh\|en` | `zh` | 输出语言 |

---

## 执行流程

所有模式共享的前置步骤：

```
Step 0: 需求理解
  → 识别产品类型（To B / To C / 内部工具 / API）
  → 提取核心目标、用户群体、关键约束
  → 缺失关键信息时一次性补问（≤ 3 个问题）
```

### mode=lite 流程

```
Step 1: 快速解析需求（目标/用户/核心功能/指标）
Step 2: 输出一页纸 PRD（背景/用户/方案/指标/不在范围）
```

### mode=prd 流程

```
Step 1: 需求解析 → 识别类型、目标、用户、约束
Step 2: 结构生成 → 按 --prd-mode 生成 PRD 框架
Step 3: 指标设计 → 北极星指标 + 埋点 + A/B 策略
Step 4: 风险评估 → 技术/依赖/时间风险
Step 5: 输出格式化 → md/notion/linear 格式
```

### mode=spec 流程

```
Step 1: 需求理解（识别用户/场景/价值/约束）
Step 2: Proposal（背景/目标/成功标准/排除项/开放问题）—— propose|full
Step 3: Specs（用户故事 + Given/When/Then + 数据模型）—— spec|full
Step 4: Design（页面清单 + ASCII 线框图 + Mermaid 交互流）—— design|full
Step 5: Tasks（P0/P1/P2 分级 + 后端/前端/测试 + 埋点 + 发布清单）—— tasks|full
Step 6: 质量门控（每阶段入场条件验证）
```

### mode=proto 流程（wireframe-first 默认）

```
Step 1: 解析需求，识别页面类型/核心操作/用户角色/关键状态

Step 2: 线框图规划
  → 列出需要绘制的页面/视图清单
  → 确定每个页面需覆盖的状态（默认/空/加载/错误/操作反馈）

Step 3: 线框图生成
  → 绘制每个页面的 ASCII 线框图（mid 保真度）
  → 标注关键交互
  → Mermaid 描述核心操作流程

─── 暂停点：输出线框图，等待确认 ───
  ✅ 确认 → 继续生成 PRD
  ✏️  修改 → 说明修改点，重新生成
  ⏭️  跳过 → 直接生成 PRD

Step 4: PRD 生成（基于确认的线框图）
  → 从线框图推导功能规格和用户故事
  → 为每个交互元素补充验收标准（Given/When/Then）
  → 添加非功能需求
  → 设计指标体系和埋点方案
  → 评估风险和发布计划

Step 5: 整合输出
  → 线框图嵌入 PRD 的"设计规格"章节
  → 输出完整融合文档
```

---

## 输出结构

### mode=lite

```markdown
# [功能名] — 一页纸 PRD
背景与问题 / 目标用户 / 解决方案 / 成功指标 / 不在范围
```

### mode=prd（full）

```markdown
# [产品名] PRD v1.0
1. 概述（问题陈述/解决方案/成功标准）
2. 用户与场景（画像/使用场景/用户旅程）
3. 功能规格（用户故事/验收标准/边界条件）
4. 非功能需求（性能/安全/兼容性）
5. 指标体系（北极星/核心/护栏/埋点）
6. 发布计划（Alpha/Beta/GA）
7. 风险与依赖
8. 变更记录
```

### mode=spec（full）

```
<功能名>/
├── proposal.md       为什么做：背景 + 目标 + 范围 + 不做什么
├── specs/
│   ├── user-stories.md    用户故事 + Given/When/Then 验收标准
│   └── edge-cases.md      边界条件 + 异常场景
├── design.md         ASCII 线框图 + Mermaid 交互流 + UI 规格
└── tasks.md          ☐ 可勾选实施清单（P0/P1/P2 分级）
```

### mode=proto

```markdown
# [功能名] — 原型 + PRD 文档

## Part 1：视觉原型
### 1.1 页面/视图清单
### 1.2 [页面名] 线框图（含所有状态）
### 1.3 核心交互流程（Mermaid）
### 1.4 UI 规格（组件/文案/交互说明）

## Part 2：产品需求文档（PRD）
背景与目标 / 目标用户 / 功能规格 / 验收标准 / 指标体系 / 发布计划 / 风险评估
```

---

## 使用示例

```bash
# 最常用：一页纸快速对齐
/product-spec 用户可以查看自己的消费明细和账单

# 标准完整 PRD（正式研发交付）
/product-spec 开发一个 AI 写作助手浏览器插件 --mode prd

# 轻量 PRD（内部评审）
/product-spec 电商 App 增加"一键复购"功能 --mode prd --prd-mode lite

# GTM 计划
/product-spec 新品上线准备 --mode prd --prd-mode gtm

# 用户旅程流程图
/product-spec SaaS 新用户引导流程优化 --mode prd --prd-mode workflow

# Spec-First 完整四件套（新功能启动）
/product-spec 用户可以在 App 内直接购买会员 --mode spec

# Spec-First 仅立项提案
/product-spec 搜索功能增加 AI 智能推荐 --mode spec --spec-mode propose

# Spec-First 仅研发任务清单
/product-spec 第三方登录集成 --mode spec --spec-mode tasks

# 线框图优先 + 完整 PRD（默认推荐）
/product-spec 新用户注册引导流程 --mode proto

# 并行输出线框图 + PRD（赶时间）
/product-spec SaaS 产品仪表盘改版 --mode proto --proto-mode combined

# 英文输出 + 目录结构模式
/product-spec New user onboarding flow --mode spec --output dir --lang en
```

---

## 与其他命令的协同

```
/product-spec（本命令）
  ├── /design-proto  → 高保真原型/Penpot/组件库/动效
  │                    （本命令只产 ASCII 线框图，高保真使用 design-proto）
  ├── /gtm-strategy  → 完整 GTM 全链路战略（本命令 gtm 模式为轻量版）
  └── /metagpt       → 将 PRD 进一步生成完整项目代码

推荐工作流：
  早期探索：/product-spec --mode lite
  新功能完整启动：/product-spec --mode spec --spec-mode full
               → /product-spec --mode proto（线框图确认）
               → 研发启动
  代码生成：/product-spec --mode prd → /metagpt --mode code
```
