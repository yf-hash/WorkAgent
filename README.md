# WorkAgent — PM Harness + SA Harness + Content Harness

> 以 **Claude Code 为算力入口**、以 **harness 五能力分层 + 一层角色元代理** 为执行框架、以 **三条端到端流水线** 为核心业务能力的 AI 工作智能体。
>
> **版本**：v3.2（2026-08-27） · **资产**：26 commands · 27 skills · 3 agents · 3 roles · 5+1 harness 原语 · 5 hook 对（sh/ps1）
>
> 服务对象：
> - **产品经理（PM）**：从一句话原始需求到完整可交付需求包（含技术规格书 + 竞品分析）— [PM Harness](docs/PM_HARNESS.md)
> - **售前工程师（SA）**：从销售转述一句话 / RFP 到完整售前包（含方案 + POC + RFP 应答 + 报价）— [SA Harness](docs/SA_HARNESS.md)
> - **内容 / 市场 / 品牌**：从一句自然语言到八大文体内容物料（推广文 / 白皮书 / PR 稿 / PPT / 推文 / 科普文...）— [Content Harness](docs/CONTENT_HARNESS.md)

## 快速上手

打开一个 Claude Code 会话（在本仓库目录），敲斜杠命令：

### PM 场景（内部产品需求 / PRD / 竞品分析）

```bash
# 一键端到端 PM 流水线（内部需求 → PRD → 技术规格）
/pm-pipeline "客户想批量导入发票" --mode human --product-type saas-b

# 竞品分析工程化（横向能力）
/pm-competitive "AI 写作助手，面向中小企业内容营销" --depth deep

# 或用角色总入口（自然语言智能识别）
/pm 客户要一个批量导入发票功能，做完整交付包
/pm 帮我分析 AI 写作助手赛道的竞品
```

### SA 场景（对外客户售前 / 投标）

```bash
# 一键端到端 SA 流水线
/sa-pipeline "某制造业客户，要替换老 MES，私有化 + 国产化，3 月上线" \
  --client "远大制造" \
  --industry manufacturing \
  --compliance 等保三级,国产化 \
  --deployment private

# 投标应答场景
/sa-pipeline ./rfp/2026-政务云-RFP.pdf --stage-5 rfp

# 或用角色总入口
/sa 某制造业客户，要替换老 MES，做完整售前包
```

### Content 场景（内容 / 市场 / 品牌）

```bash
# 一键端到端内容流水线（八大文体皆可）
/content "基于 VulnHunter 项目，写一份产品解决方案白皮书，8000 字左右" \
  --project ./output/pm-pipeline/vulnhunter-20260827/ \
  --writeback

# 或直接一句话
/content "写一篇 PR 稿，我们新版本上线了分布式沙箱调度"

# 或用角色总入口
/content 帮我给项目 X 出一份汇报 PPT
```

完整流水线说明：
- PM：[`docs/PM_HARNESS.md`](docs/PM_HARNESS.md)
- SA：[`docs/SA_HARNESS.md`](docs/SA_HARNESS.md)
- Content：[`docs/CONTENT_HARNESS.md`](docs/CONTENT_HARNESS.md)

## 核心理念

**模型负责思考，harness 负责执行 / 约束 / 循环 / 记忆 / 安全。**

- 模型（Claude Opus / Sonnet）：理解、生成、决策、反思
- Harness（Claude Code + 本仓库 `.claude/harness/`）：工具白名单、权限画像、Stage Gate、记忆读写、危险动作拦截、角色路由

架构与设计原理见 **[HARNESS_FRAMEWORK.md](HARNESS_FRAMEWORK.md)**。

## 三条端到端流水线

### PM Harness（6 模块 - 内部需求 → PRD → 技术规格）

```
一句话原始需求
    ↓
[M2] /pm-clarify        → 01-clarify-report.md
    ↓  🔒 Gate
[M3] /pm-solution       → 02-business-solution.md
    ↓  🔒 Gate
[M4] /pm-prototype      → 03-prototype/*.{md,json,mmd}
    ↓  🔒 Gate
[M5] /prd --validate    → 04-PRD.md + 04-PRD-validate.md
    ↓  🔒 Gate
[M6] /pm-tech-spec      → 05-tech-{metrics,spec,validate}.md
    ↓  🔒 Gate
[M7] /pm-archive        → README.md + CHANGELOG.md + VERSION
```

**+ 横向能力：竞品分析工程化** — `/pm-competitive`（两阶段：scan → benchmark）

### SA Harness（7 模块 - 客户输入 → 方案 → POC/RFP → 报价）

```
销售转述一句话 / RFP / 客户访谈
    ↓
[M1] /sa-intake         → 00-intake.json（结构化项目对象）
    ↓  🔒 Gate
[M2] /sa-clarify        → 01-clarify-report.md（客户调研痛点报告）
    ↓  🔒 Gate
[M3] /sa-solution-map   → 02-solution-map.md（业务能力映射 + 竞品 + 风险）
    ↓  🔒 Gate
[M4] /sa-architect      → 03-overall-solution.md + arch.mmd + validate
    ↓  🔒 Gate
[M5] /sa-poc /impl /rfp → 04-poc / 04-impl / 04-rfp + deviation
    ↓  🔒 Gate
[M6] /sa-quote          → 05-config-estimate.md + presentation-*
    ↓  🔒 Gate
[M7] /sa-archive        → README + CHANGELOG + VERSION + freeze
```

### Content Harness（5 模块 - 一句话 → 八大文体内容）

```
自然语言输入
    ↓
[M1] /content-intake      → 00-content-request.json（文体识别 + 需求解析 + 项目关联）
    ↓  🔒 Gate
[M2] /content-materials   → 01-material-pool.md（可选：拉取 PM/SA 项目产物）
    ↓  🔒 Gate
[M3] /content-generate    → 02-draft.md（八大文体专项生成）
    ↓
[M4] /content-validate    → 03-validate-report.md（5 类校验）
    ↓  🔒 Gate（人工审核卡点）
[M5] /content-archive     → README + _export/*.{md,docx,json}
                          + 可回写到关联 PM/SA 项目 _content/
```

## PM / SA / Content：如何选择

| | `/pm`（产品经理） | `/sa`（售前工程师） | `/content`（内容 / 市场） |
|---|---|---|---|
| 服务对象 | 内部产品 PM | 对外客户售前 SA | 内容 / 市场 / 品牌 |
| 输入 | 需求想法 | 销售转述 / RFP | 一句自然语言（含文体） |
| 输出 | PRD + 技术规格书 | 方案 + POC + 报价 | 八大文体内容物料 |
| 关注点 | 用户价值 / 功能规划 | 客户痛点 / 竞争 / 中标 | 传播 / 品牌 / 事实一致 |
| 目录 | `./output/pm-pipeline/` | `./output/sa-pipeline/` | `./output/content-pipeline/` |
| 跨流水线 | 单向被引用 | 单向被引用 | ★ **双向读取 + 回写** |

**共用**：三者共享 `.claude/harness/` 五能力分层框架、stage gate 机制、记忆管理。

**跨流水线协作**：
- PM 项目上线 → Content 出 PR 稿 + 推广文 → 回写到 PM 项目
- SA 中标 → Content 出解决方案白皮书 → 回写到 SA 项目
- PM 竞品分析 → 输出作为 Content 差异化推广文的输入
- 一个项目同时拥有 PRD、规格书、方案、对外宣传物料（`_content/` 子目录挂载）

## 顶层目录

```
WorkAgent/
├── HARNESS_FRAMEWORK.md          # 顶层 harness 五能力分层框架
├── README.md                     # 本文件
│
├── .claude/                      # harness 层
│   ├── CLAUDE.md                 # 项目级说明（每次会话必读）
│   ├── README.md                 # .claude 索引 + 版本日志
│   ├── settings.json             # 全局权限 + hooks 位
│   ├── harness/                  # 五能力原语 + role 元代理层
│   │   ├── execute/presets.md    # 工具预设（6 类）
│   │   ├── constrain/profiles.md # 权限画像（6 类 + gate）
│   │   ├── loop/modes.md         # 循环模式（5 种）
│   │   ├── memory/schema.md      # 记忆作用域（4 种）
│   │   ├── security/policies.md  # 危险度策略（3 级 + deny list）
│   │   └── role/                 # 角色元代理原语（router + task-planner）
│   ├── hooks/                    # 5 对 hook 脚本（.sh + .ps1）
│   ├── memory/                   # 项目级记忆（MEMORY.md 索引 + 3 分文件）
│   └── scripts/                  # migrate.py / validate-harness.py
│
├── agents/                       # 3 个总入口 agent
│   ├── pm.md                     # PM 角色路由器
│   ├── sa.md                     # SA 角色路由器
│   └── content.md                # Content 角色路由器
│
├── commands/
│   ├── product/                  # PM 10 个命令
│   │   ├── pm-clarify.md          # M2 需求澄清
│   │   ├── pm-solution.md         # M3 业务方案
│   │   ├── pm-prototype.md        # M4 原型底稿
│   │   ├── prd.md                 # M5 PRD + 校验
│   │   ├── pm-tech-spec.md        # M6 技术规格书
│   │   ├── pm-archive.md          # M7 归档
│   │   ├── pm-pipeline.md         # 端到端主流水线编排器
│   │   ├── pm-competitive-scan.md      # 竞品分析 阶段 1（发现+情报）
│   │   ├── pm-competitive-benchmark.md # 竞品分析 阶段 2（对标+战略）
│   │   └── pm-competitive.md      # 竞品分析编排器
│   ├── presales/                 # SA 10 个命令
│   │   ├── sa-intake.md           # M1 输入网关
│   │   ├── sa-clarify.md          # M2 客户调研
│   │   ├── sa-solution-map.md     # M3 方案拆解
│   │   ├── sa-architect.md        # M4 总体方案 + 架构
│   │   ├── sa-poc.md              # M5.1 POC 方案
│   │   ├── sa-impl.md             # M5.2 实施方案
│   │   ├── sa-rfp.md              # M5.3 RFP 应答
│   │   ├── sa-quote.md            # M6 报价 + 宣讲
│   │   ├── sa-archive.md          # M7 归档
│   │   └── sa-pipeline.md         # 端到端编排器
│   └── content/                  # Content 6 个命令
│       ├── content-intake.md      # M1 内容请求网关
│       ├── content-materials.md   # M2 项目素材抽取
│       ├── content-generate.md    # M3 八大文体专项生成
│       ├── content-validate.md    # M4 五类校验
│       ├── content-archive.md     # M5 归档 + 多格式导出
│       └── content.md             # 统一入口编排器（对外唯一入口）
│
├── skills/
│   ├── pm/                       # PM 10 个 skill
│   │   ├── pm-requirement-clarify/       # M2 支撑
│   │   ├── pm-solution-decompose/        # M3 支撑
│   │   ├── pm-prototype-design/          # M4 支撑
│   │   ├── pm-prd-validate/              # M5 校验
│   │   ├── pm-tech-spec/                 # M6 指标方法论
│   │   ├── pm-tech-spec-validate/        # M6 校验
│   │   ├── pm-artifact-archive/          # M7 支撑
│   │   ├── pm-competitive-intel/         # 竞品情报采集
│   │   ├── pm-competitive-benchmark/     # 竞品对标方法论
│   │   └── pm-competitive-strategy/      # 差异化战略方法论
│   ├── prd/
│   │   └── prd-writer/            # PM M5 核心 skill
│   ├── sa/                       # SA 11 个 skill
│   │   ├── sa-input-gateway/
│   │   ├── sa-clarify/
│   │   ├── sa-capability-mapping/
│   │   ├── sa-architect/
│   │   ├── sa-solution-validate/
│   │   ├── sa-poc-plan/
│   │   ├── sa-impl-plan/
│   │   ├── sa-rfp-response/
│   │   ├── sa-quote-estimate/
│   │   ├── sa-presentation-draft/
│   │   └── sa-artifact-archive/
│   └── content/                  # Content 5 个 skill
│       ├── content-intake/         # 文体识别 + 需求解析
│       ├── content-materials/      # 项目素材抽取方法论
│       ├── content-templates/      # 八大文体模板库
│       ├── content-validate/       # 5 类校验规则
│       └── content-archive/        # 归档 + 多格式导出
│
├── roles/                        # 角色声明式配置
│   ├── pm/
│   │   ├── manifest.yaml         # PM 能力清单
│   │   └── workflows.md
│   ├── sa/
│   │   ├── manifest.yaml         # SA 能力清单
│   │   └── workflows.md
│   └── content/
│       ├── manifest.yaml         # Content 能力清单（八大文体）
│       └── workflows.md
│
└── docs/                         # 元文档
    ├── PM_HARNESS.md             # PM 6 模块流水线总览
    ├── SA_HARNESS.md             # SA 7 模块流水线总览
    ├── CONTENT_HARNESS.md        # Content 5 模块流水线总览
    └── README.md
```

## 差异化能力

### PM Harness 相对于传统 PM 工具

| 传统 PM 流程 | 本 Harness |
|---|---|
| PM 手工梳理需求 → 反复对齐 | M2：需求澄清 Agent 自动识别 7 要素缺失 + 冲突 + 伪需求 |
| PM 拆功能 → 直接写 PRD | M3：业务方案 Agent 先出流程 / P0/P1/P2 / 权限矩阵 |
| PM 画原型 → 交给设计师 | M4：原型 Agent 出结构化 JSON + Mermaid |
| PRD 写完就完 | M5：自动跑 4 类校验（完整 / 一致 / 歧义 / 埋点） |
| **技术指标全靠研发梳理** | **M6：技术规格 Agent 自动输出 6 大类指标 + 规格书**（核心差异化） |
| 版本管理靠 Git | M7：归档 Agent 生成 README + CHANGELOG + freeze 快照 |

### SA Harness 相对于传统售前工作流

| 传统售前流程 | 本 Harness |
|---|---|
| 销售转述整理靠人 | M1：多源输入网关自动清洗 + 抽取 12 类元信息 |
| 客户信息模糊人工发问题 | M2：调研澄清 Agent 自动识别 7 类缺口 |
| 拆功能靠经验 | M3：业务-能力自动映射 + 竞品对标 + 5 类风险 |
| 方案画架构图靠 Visio | M4：架构自动生成 + Mermaid + 三项校验 |
| POC / 实施 / RFP 重复劳动 | M5：三个专项方案并行生成 |
| 报价拍脑袋 | M6：基于规则库的估算底稿（⚠️ 底稿，非最终报价） |
| 变更需求重写全部 | M7：语义化版本 + 变更触发下游局部重跑 |

## 反模式（三条流水线共通）

- ❌ 用 `--skip-gate` 交付客户版 —— gate 是流水线质量红线
- ❌ 跳过澄清直接写方案 / PRD —— 放弃了 harness 的核心价值
- ❌ 合规约束用 auto 假设 —— 生产事故温床
- ❌ 手工改 `.pipeline-state.json` —— 状态会不一致
- ❌ 修改 `_frozen/` 内文件 —— 审计留档不可篡改

## 资产统计（v3.2）

| 类型 | 数量 | 明细 |
|---|---|---|
| **Commands** | 26 | 10 PM（`commands/product/`）+ 10 SA（`commands/presales/`）+ 6 Content（`commands/content/`） |
| **Skills** | 27 | 10 PM + 1 PRD + 11 SA + 5 Content |
| **Agents** | 3 | `pm` / `sa` / `content` 角色总入口 |
| **Roles** | 3 | 每个含 `manifest.yaml` + `workflows.md` |
| **Harness 原语** | 5 + 1 | execute · constrain · loop · memory · security · role（角色元代理） |
| **Hooks** | 5 对 | `.sh` + `.ps1` 双平台；3 启用（2 安全 guard + 1 上下文注入），2 骨架（备份 / 审计） |
| **Memory** | 4 文件 | `MEMORY.md` 索引 + `project-context.md` + `conventions.md` + `decisions.md` |
| **Scripts** | 2 | `migrate.py` · `validate-harness.py`（CI 强制运行） |
| **Meta docs** | 4 | `docs/{PM,SA,CONTENT}_HARNESS.md` + `docs/README.md` |

**Harness 覆盖率**：commands 26/26 · agents 3/3 = **29/29 (100%)** 强制层已声明 `harness:` 块。skills 按设计允许省略（inner 模块，继承调用方 command 的策略）。CI 通过 `validate-harness.py --strict` 强制。

## 版本

- **v3.2**（2026-08-27）：新增 Content Harness 5 模块流水线（八大文体内容创作）+ 跨流水线回写
- **v3.1**（2026-08-27）：PM Harness 新增竞品分析工程化能力（`/pm-competitive` scan → benchmark）
- **v3.0**（2026-08-27）：新增 SA Harness 7 模块流水线（对外售前场景 + RFP 应答）
- **v2.0**（2026-08-27）：精简至端到端 6 模块 PM 流水线（M2→M7）
- **v1.x**：见 git history

## 相关文档

- [HARNESS_FRAMEWORK.md](HARNESS_FRAMEWORK.md) — 顶层 harness 五能力分层
- **[docs/PM_HARNESS.md](docs/PM_HARNESS.md) — PM 6 模块流水线总览（入门必读）**
- **[docs/SA_HARNESS.md](docs/SA_HARNESS.md) — SA 7 模块流水线总览（入门必读）**
- **[docs/CONTENT_HARNESS.md](docs/CONTENT_HARNESS.md) — Content 5 模块流水线总览（入门必读）**
- [.claude/README.md](.claude/README.md) — harness 层配置索引 + 命令一览
- [.claude/CLAUDE.md](.claude/CLAUDE.md) — 项目级会话说明
- [.claude/harness/role/README.md](.claude/harness/role/README.md) — 角色元代理层原理
- [roles/pm/manifest.yaml](roles/pm/manifest.yaml) — PM 角色能力清单
- [roles/sa/manifest.yaml](roles/sa/manifest.yaml) — SA 角色能力清单
- [roles/content/manifest.yaml](roles/content/manifest.yaml) — Content 角色能力清单（八大文体）
