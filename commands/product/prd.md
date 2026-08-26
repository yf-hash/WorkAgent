---
name: prd
description: PRD 统一入口（13 种模式）。生成类：lite（1 页）/ standard（8 章）/ enterprise（B 端严格 12 章）/ linear（Linear Issue 单功能）/ spec-first（四件套）/ proto（含线框图）/ xqy（银行金融 8 章需规）。渐进类：diagnose → concept → impl（对话式三段）。评估类：quality（5 维评分）/ evaluate（23 节差距）。变更类：update（增量合并）。
user-invocable: true
argument-hint: "<需求描述或 PRD 文件路径> --mode <mode> [--stage <s>] [--fidelity <f>] [--module-type <m>] [--system <name>] [--flow discovery] [--lang zh|en]"
allowed-tools: [Read, Write, Edit, AskUserQuestion]
harness:
  execute:
    preset: writing-scoped
  constrain:
    profile: writing-safe
    gates: [before-write]
  loop:
    mode: one-shot
    # 备注：--flow discovery 时切 pipeline，stages: [diagnose, concept, impl]
  memory:
    scope: project
    reads: [project-context]
  security:
    danger-level: low
---

# /prd — PRD 统一入口

## 一句话

12 个 PRD skill + 1 个模板（enterprise）合入一个命令。`--mode` 分派到对应 skill/模板；无 `--mode` 时按输入类型（描述 / 文件路径）自动推断。

## 用法

```bash
# ─── 生成类（输入是需求描述） ─────────────────────────
/prd 用户可以查看消费明细 --mode lite
/prd 开发 AI 写作助手浏览器插件 --mode standard
/prd 多租户 SaaS 权限中心 --mode enterprise
/prd 用户可以在订单列表页批量导出 Excel --mode linear
/prd 用户可以在 App 内直接购买会员 --mode spec-first
/prd 用户可以在 App 内直接购买会员 --mode spec-first --stage propose
/prd 新用户注册引导流程 --mode proto --fidelity mid
/prd 新增对公账户开户业务接口 --mode xqy
/prd 客户信息变更 --mode xqy --module-type mixed --system 核心账务

# ─── 渐进类（对话式，想法模糊时用）─────────────────────
/prd 想做面向独立设计师的素材管理工具 --mode diagnose
/prd 通过诊断的想法 --mode concept          # 前置：diagnose 完成
/prd ./docs/产品名-概念稿.md --mode impl    # 前置：concept 完成
/prd 想做一个 AI 客服产品 --flow discovery  # 一键跑 diagnose → concept → impl

# ─── 评估类（输入是 PRD 文件）─────────────────────────
/prd ./docs/PRD-v1.md --mode quality        # 5 维度评分
/prd ./docs/PRD-v1.md --mode evaluate       # 23 节深度差距

# ─── 变更类（输入是 PRD 文件 + 变更描述）───────────────
/prd ./docs/PRD-v1.md --mode update 新增批量导入 Excel 模板与前端预校验功能
```

## 分派规则

| `--mode` | 加载技能 | 输入 | 输出 | 前置 |
|---|---|---|---|---|
| `lite` | `skills/prd/prd-lite/SKILL.md` | 需求描述 | 1 页纸 PRD（背景/用户/方案/指标/不在范围）10-15 分钟 | 无 |
| `standard` | `skills/prd/prd-standard/SKILL.md` | 需求描述 | 标准 8 章 PRD + Given/When/Then 验收 | 无 |
| `enterprise` | `templates/prd-template.md`（模板直填，无独立 skill） | 需求描述 | B 端严格 12 章 PRD（含多租户/审计/隔离/合规/私有化默认必填），适合 B 端 SaaS / 私有化 | 无 |
| `linear` | `skills/prd/prd-linear/SKILL.md` | 需求描述 | Linear Issue 级单功能 PRD（背景/名词/入口/主流程/异常边界/数据规则/权限/文案/GWT 验收/影响范围/明确不做/变更记录），含红线自检 | 无 |
| `spec-first` | `skills/prd/prd-spec-first/SKILL.md` | 需求描述 | Spec-First 四件套（proposal/specs/design/tasks），受 `--stage` 约束 | 无 |
| `proto` | `skills/prd/prd-proto/SKILL.md` | 需求描述 | PRD + ASCII 线框图（4 状态：默认/空/加载/错误），受 `--fidelity` 约束 | 无 |
| `xqy` | `skills/prd/prd-xqy/SKILL.md` | 需求描述 | 银行/金融 8 章需规说明书（含 5 张强制表格），受 `--module-type` / `--system` 约束 | 无 |
| `diagnose` | `skills/prd/prd-diagnose/SKILL.md` | 一句话想法 | 三镜（用户/商业/技术）诊断问答 | 无 |
| `concept` | `skills/prd/prd-concept-draft/SKILL.md` | 已通过诊断的想法 | 概念稿 v1（1 页方向对齐） | diagnose 完成 |
| `impl` | `skills/prd/prd-implementation-draft/SKILL.md` | 概念稿路径 | 实现稿 v2（23 节企业级） | concept 完成 |
| `quality` | `skills/prd/prd-quality-check/SKILL.md` | PRD 文件路径 | 5 维评分（完整 30% / 可测 25% / 量化 20% / 边界 15% / 数据 10%） | 有 PRD 文件 |
| `evaluate` | `skills/prd/prd-deep-evaluate/SKILL.md` | PRD 文件路径 | 23 节企业模板差距分析（方向/结构/细节三层） | 有 PRD 文件 |
| `update` | `skills/prd/prd-incremental-update/SKILL.md` | PRD 文件 + 变更描述 | 增量合并（不重写原文，只标【本次更新】） | 有 PRD 文件 |

## 自动推断（无 `--mode` 时）

不填 `--mode` 也能工作，但会用 `AskUserQuestion` 让你选：

```
输入是 <需求描述>（文本，非路径）
  → 问：想要哪种 PRD？
    - lite（1 页对齐）
    - standard（C 端 8 章）
    - enterprise（B 端严格 12 章，含审计/隔离/合规）
    - linear（Linear Issue 单功能，含红线自检）
    - spec-first（四件套）
    - proto（含线框图）
    - xqy（银行/金融需规）
    - 我还不确定 → 走 --flow discovery（三镜诊断 → 概念 → 实现）

输入是 <.md 文件路径>
  → 问：想做什么？
    - quality（5 维评分）
    - evaluate（23 节深度）
    - update（有变更描述） → 提示补充变更内容

输入以 "-" 开头（可能是选项）
  → 报错并列出可用 --mode
```

## 参数适用范围

| 参数 | 适用 mode | 值 | 说明 |
|---|---|---|---|
| `--stage` | `spec-first` | `propose\|spec\|design\|tasks\|full` | 四件套的哪一件；默认 full |
| `--fidelity` | `proto` | `low\|mid` | 线框保真度；默认 low |
| `--module-type` | `xqy` | `interface\|menu\|batch\|mixed` | 银行需规的功能分类 |
| `--system` | `xqy` | 系统名 | 挂在需规封面的系统标识 |
| `--flow` | 无 mode | `discovery` | 一键顺序执行 diagnose → concept → impl（含 gate 提示） |
| `--lang` | 全部 | `zh\|en` | 输出语言，默认 zh |

## 强顺序与 gate 逻辑

`--mode concept` / `--mode impl` **必须**检查前置条件：

```
--mode concept
  ├─ 无 diagnose 输出 → 用 AskUserQuestion 问三镜（用户/商业/技术），否则报错
  └─ 有 diagnose 输出 → 直接进入

--mode impl
  ├─ 无 concept 输出 → 报错，提示"先跑 --mode concept"
  └─ 有 concept 输出 + 用户已确认方向 → 直接进入

--flow discovery
  → 依次跑 diagnose → concept → impl
  → 每段结束用 AskUserQuestion 显式 gate："方向确认无误吗？"
```

## 与其他命令 / Agent 的边界

| 场景 | 用 |
|---|---|
| C 端通用 PRD | 本命令 `--mode lite/standard/spec-first/proto` |
| B 端 SaaS / 私有化严格 12 章 | 本命令 `--mode enterprise` |
| **Linear/Jira Issue 单功能规范化描述**（含红线自检） | **本命令 `--mode linear`** ⭐ |
| 银行 / 金融 / 政府核心系统需规 | 本命令 `--mode xqy` 或 `@xqy-spec-writer` |
| LLM / Agent / RAG 类 AI 功能 PRD | `@ai-product-architect` |
| 想法模糊、需要对话教练 | 本命令 `--flow discovery` 或 `@prd-coach` |
| 验收方案（PRD → 测试用例） | `@qa-acceptance-designer` |

## 与 `/prd-proto` + `/design-proto` 的组合

- `--mode proto` 输出 ASCII 线框图 + PRD 融合稿（用于对齐需求）
- 高保真原型（视觉设计层）走 `/design-proto` 或 `@impeccable-designer`

## `--mode enterprise` 输出约束（无 skill 时的最小规则）

模板路径：`templates/prd-template.md`（当前目录不可读时按同结构直接生成）。除模板 12 章结构外，强制遵守：

- 用清晰编号；字段 / 权限 / 状态 / 验收项一律表格化
- **对研发友好**：流程 / 规则 / 字段 / 状态 / 异常必须完整
- **对测试可验收**：每条业务规则都能写成一条用例
- **对交付可解释**：默认包含审计、多租户隔离、私有化部署口径
- 不只写功能说明，同时写清 **业务规则** 与 **实现边界**

## 迁移说明（v2.8.2）

以下 12 个旧命令已合并至本命令，映射如下（skills / template 层完全不变，能力保留）：

| 旧命令 | 新写法 |
|---|---|
| `/prd-lite <需求>` | `/prd <需求> --mode lite` |
| `/prd-standard <需求>` | `/prd <需求> --mode standard` |
| `/pm-prd-enterprise <需求>` | `/prd <需求> --mode enterprise` |
| `/prd-spec-first <需求> [--stage X]` | `/prd <需求> --mode spec-first [--stage X]` |
| `/prd-proto <需求> [--fidelity X]` | `/prd <需求> --mode proto [--fidelity X]` |
| `/prd-xqy <需求> [--module-type X]` | `/prd <需求> --mode xqy [--module-type X]` |
| `/prd-diagnose <想法>` | `/prd <想法> --mode diagnose` |
| `/prd-concept <想法>` | `/prd <想法> --mode concept` |
| `/prd-impl <概念稿路径>` | `/prd <概念稿路径> --mode impl` |
| `/prd-quality <PRD 路径>` | `/prd <PRD 路径> --mode quality` |
| `/prd-deep-evaluate <PRD 路径>` | `/prd <PRD 路径> --mode evaluate` |
| `/prd-update <PRD 路径> <变更>` | `/prd <PRD 路径> --mode update <变更>` |

**⚠️ 覆盖 AUDIT.md "合 prd-* 11 个"撤回项**：AUDIT 曾以"场景清晰、合并会牺牲精度"为由撤回。v2.8.1 推翻此决定，v2.8.2 进一步吸收 `/pm-prd-enterprise`，理由：
1. skills / template 层保持独立，精度不减
2. 与 `/humanize` `/bid` `/dashboard` 同一收敛思路（v2.8 已验证可行）
3. `prd-spec-first --stage` 已是先例，多模式单命令行得通
4. 用户从记 12 个前缀降到 1 个前缀 + `--mode`
