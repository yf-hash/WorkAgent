# PM Harness — 产品经理端到端 6 模块流水线

> **一句话原始需求 → 结构化需求包**：从老板/销售的一句话想法，经过 6 个 Agent 模块，产出可交付研发/合规/客户的完整需求包（含 PRD + 技术规格书 + 归档）。
>
> 版本：v1.0（2026-08-27）

## 一、为什么需要这套 Harness

大多数 PM 工具只解决了单点问题：**只会写业务 PRD，不会梳理技术指标、不会做原型底稿、不会做归档**。

这套 Harness 的核心命题：

> **让大模型作为思考引擎，Harness 作为执行、约束、循环、记忆、安全的骨架**——
> PM 只需要给一句话，然后在每个 gate 做质量把关。

### 相比传统 PM 工作流的差异化

| 传统流程 | 本 Harness |
|---|---|
| PM 手工梳理需求 → 反复对齐 | 需求澄清 Agent 自动识别 7 要素缺失 |
| PM 拆功能 → 直接写 PRD | 业务方案 Agent 先出流程/优先级/权限矩阵 |
| PM 画原型 → 交给设计师 | 原型 Agent 出结构化 JSON + Mermaid，可导入工具 |
| PRD 写完就完 | 自动跑完整性 / 一致性 / 歧义 / 埋点 四类校验 |
| **技术指标全靠研发梳理** | **技术规格 Agent 自动输出 6 大类指标 + 规格书**（差异化） |
| 版本管理靠 Git | 归档 Agent 生成 README + CHANGELOG + freeze 快照 |

## 二、6 模块流水线全景图

```
┌──────────────────────────────────────────────────────────────┐
│ 【输入】一句话原始需求                                          │
│  "客户想批量导入发票"                                          │
└──────────────────────────────────────────────────────────────┘
                       │
                       ▼
    ┌──────────────────────────────────────────┐
    │  M2 需求澄清 Agent 套件                    │
    │  /pm-clarify                              │
    │  ─────────────────────────                │
    │  Agent 2-1: 歧义识别（7 要素缺失）         │
    │  Agent 2-2: 澄清问题生成（3 类问题）        │
    │  Agent 2-3: 冲突检测 + 伪需求识别          │
    │                                           │
    │  → 01-clarify-report.md                   │
    └──────────────────────────────────────────┘
                       │
                    🔒 Harness Gate (PM 审阅)
                       ▼
    ┌──────────────────────────────────────────┐
    │  M3 业务方案与边界分析 Agent                │
    │  /pm-solution                             │
    │  ─────────────────────────                │
    │  Agent 3-1: 业务方案拆解                   │
    │    · 主/分支/异常流程                       │
    │    · P0/P1/P2 功能清单                     │
    │    · 用户角色 × 权限矩阵                    │
    │    · 本次包含 vs 明确不做                   │
    │  Agent 3-2: 风险 & 依赖识别                │
    │                                           │
    │  → 02-business-solution.md                │
    └──────────────────────────────────────────┘
                       │
                    🔒 Harness Gate (调整优先级)
                       ▼
    ┌──────────────────────────────────────────┐
    │  M4 原型辅助生成工具套件                    │
    │  /pm-prototype                            │
    │  ─────────────────────────                │
    │  Agent 4-1: 页面 & 交互生成                │
    │    · 页面清单 + 组件树                     │
    │    · Mermaid 主流程 + 异常流程              │
    │    · 结构化原型 JSON (可导 Figma/Axure)    │
    │    · ASCII 线框图（4 状态）                 │
    │  Agent 4-2: 原型逻辑校验                   │
    │    · 跳转闭环 / 异常态 / 权限一致           │
    │                                           │
    │  → 03-prototype/*.{md,json,mmd}           │
    └──────────────────────────────────────────┘
                       │
                    🔒 Harness Gate (原型确认)
                       ▼
    ┌──────────────────────────────────────────┐
    │  M5 PRD 编写 Agent 套件                    │
    │  /prd --mode full --validate --input M2,M3,M4 │
    │  ─────────────────────────                │
    │  Agent 5-1: PRD 主文档生成                 │
    │    · 全局章节 + 每功能 10 项                │
    │    · 页面说明（引用原型编号）               │
    │    · 埋点、非功能、上线约束                 │
    │  Agent 5-2: PRD 校验（4 类）               │
    │    · 完整性 / 一致性 / 歧义 / 埋点          │
    │                                           │
    │  → 04-PRD.md + 04-PRD-validate.md         │
    └──────────────────────────────────────────┘
                       │
                    🔒 Harness Gate (PRD 定稿)
                       ▼
    ┌──────────────────────────────────────────┐
    │  M6 产品技术指标 & 规格书 Agent 套件         │
    │  /pm-tech-spec  【核心差异化】               │
    │  ─────────────────────────                │
    │  Agent 6-1: 产品技术指标梳理               │
    │    · 性能 / 安全 / 兼容 / 可靠 / 合规 / 依赖 │
    │  Agent 6-2: 规格书生成                     │
    │    · 10 章正式规格书                        │
    │  Agent 6-3: 规格书校验                     │
    │    · 可量化 / 一致性 / 验收标准             │
    │                                           │
    │  → 05-tech-metrics.md                     │
    │  → 05-tech-spec.md                        │
    │  → 05-tech-spec-validate.md               │
    └──────────────────────────────────────────┘
                       │
                    🔒 Harness Gate (指标定稿)
                       ▼
    ┌──────────────────────────────────────────┐
    │  M7 产物审阅与版本归档                      │
    │  /pm-archive                              │
    │  ─────────────────────────                │
    │  · 完整性检查（必备产物 12 项）             │
    │  · 交叉引用检查（PRD↔业务方案↔原型↔规格）  │
    │  · 语义化版本号（major/minor/patch）       │
    │  · freeze 只读快照（客户交付版）           │
    │                                           │
    │  → README.md + CHANGELOG.md + VERSION     │
    │  → _frozen/{tag}/ (可选)                  │
    └──────────────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────────┐
│ 【输出】完整可交付需求包                                        │
│  ./output/pm-pipeline/{topic}-{yyyymmdd}/                    │
└──────────────────────────────────────────────────────────────┘
```

## 三、6 模块产物清单

| 模块 | 命令 | 产物 | Skill 支撑 |
|---|---|---|---|
| M2 | `/pm-clarify` | 01-clarify-report.md | pm-requirement-clarify |
| M3 | `/pm-solution` | 02-business-solution.md | pm-solution-decompose |
| M4 | `/pm-prototype` | 03-prototype/{md,json,mmd} | pm-prototype-design |
| M5 | `/prd --validate` | 04-PRD.md + 04-PRD-validate.md | prd-writer + pm-prd-validate |
| M6 | `/pm-tech-spec` | 05-tech-{metrics,spec,validate}.md | pm-tech-spec + pm-tech-spec-validate |
| M7 | `/pm-archive` | README + CHANGELOG + freeze | pm-artifact-archive |
| 一键编排 | `/pm-pipeline` | 全部 | 上述全部 |

## 四、目录结构约定

```
./output/pm-pipeline/{topic}-{yyyymmdd}/
├── .pipeline-state.json       ← 流水线状态（由 /pm-pipeline 维护）
├── 01-clarify-report.md       ← M2
├── 02-business-solution.md    ← M3
├── 03-prototype/               ← M4
│   ├── 03-prototype-desc.md
│   ├── 03-prototype.json
│   ├── 03-flow.mmd
│   ├── 03-flow-exception.mmd
│   └── 03-validate.md
├── 04-PRD.md                   ← M5 主文档
├── 04-PRD-validate.md         ← M5 校验
├── 05-tech-metrics.md         ← M6 指标清单
├── 05-tech-spec.md            ← M6 规格书
├── 05-tech-spec-validate.md   ← M6 校验
├── review-notes.md             ← 人工审阅记录（可选）
├── README.md                   ← M7 索引
├── CHANGELOG.md                ← M7 变更历史
├── VERSION                     ← M7 版本号
├── archive-report.md           ← M7 归档检查报告
└── _frozen/                    ← M7 freeze 快照
    └── v1.0-上线版/            ← 只读
```

## 五、如何使用

### 方式 A：一键全流程（推荐）

```bash
/pm-pipeline "客户想批量导入发票" --mode human --product-type saas-b
```

每阶段之间会 gate 询问 PM，全程 3-4 小时。

### 方式 B：通过总入口 /pm 智能识别

```bash
/pm 客户要一个批量导入发票功能，做完整交付包
```

`/pm` agent 识别到"完整交付包"信号 → 推荐 `/pm-pipeline` → 用户确认 → 自动调用。

### 方式 C：手工分步执行

```bash
# 一步一步来，中间可以做其他事
/pm-clarify "客户想批量导入发票" --mode human
/pm-solution ./output/pm-pipeline/invoice-import-20260827/01-clarify-report.md
/pm-prototype ./output/pm-pipeline/xxx/02-business-solution.md
/prd 批量导入发票 --mode full --input ...
/pm-tech-spec ./04-PRD.md --input ./01,./02,./03
/pm-archive ./output/pm-pipeline/xxx/
```

### 方式 D：断点续跑 / 局部返工

```bash
# 客户看了 M3 要求改优先级
/pm-pipeline ./output/pm-pipeline/xxx/ --from M3

# 已有 PRD，只补技术规格
/pm-pipeline ./output/existing-project/ --from M6
```

## 六、Harness 卡点（Gate）机制

流水线在每个阶段之间设置人工审阅卡点：

| Gate | 触发时机 | 用户选项 |
|---|---|---|
| after-M2 | 澄清报告生成后 | 通过 / 驳回重跑 / 编辑后继续 / 中止 |
| after-M3 | 业务方案生成后 | 通过 / 调整优先级 / 驳回 / 中止 |
| after-M4 | 原型底稿生成后 | 通过 / 修改页面 / 驳回 / 中止 |
| after-M5 | PRD 生成后 | 通过 / 增量修改 / 驳回 / 中止 |
| after-M6 | 技术规格生成后 | 通过 / 调整指标 / 驳回 / 中止 |
| before-freeze | freeze 前 | 确认 / 取消 |

**旁路**：`--skip-gate` 用于快速原型验证，正式项目严禁使用。

## 七、六大 Skill 的能力矩阵

| Skill | 位置 | 服务命令 | 核心能力 |
|---|---|---|---|
| pm-requirement-clarify | skills/pm/ | /pm-clarify | 7 要素识别、冲突规则库、伪需求 checklist、业务目标可量化 |
| pm-solution-decompose | skills/pm/ | /pm-solution | 流程模板、P0/P1/P2 规则、权限矩阵、依赖识别 |
| pm-prototype-design | skills/pm/ | /pm-prototype | 页面模板、组件枚举、JSON Schema、逻辑校验规则 |
| pm-prd-validate | skills/pm/ | /prd --validate | 完整性/一致性/歧义/埋点四类校验 |
| pm-tech-spec | skills/pm/ | /pm-tech-spec | 6 大类指标模板、常见场景参考值、章节模板 |
| pm-tech-spec-validate | skills/pm/ | /pm-tech-spec | 可量化/一致性/验收 三项校验 |
| pm-artifact-archive | skills/pm/ | /pm-archive | 目录扫描、交叉引用、语义化版本、freeze |

## 八、精简后的资产清单（v2.1）

v2.0 精简重构后 + v2.1 新增竞品分析工程化能力：

| 资产 | 数量 | 说明 |
|---|---|---|
| Commands（`commands/product/`） | 10 | 6 主流水线命令 + 1 编排器 + 3 竞品分析命令 |
| Skills（`skills/pm/` + `skills/prd/`） | 11 | 7 主流水线 skill + 1 prd-writer + 3 竞品分析 skill |
| Agents（`agents/`） | 1 | `pm.md` 总入口路由器 |
| Roles（`roles/pm/`） | 1 | manifest.yaml + workflows.md |
| Docs（`docs/`） | 2 | 本文件 + docs README |

历史资产（如 `/pm-intake`、`/pm-discovery`、`/pm-review`、`/design-proto`、`@product-manager`、`@prd-coach`、`@ai-product-architect`、`@qa-acceptance-designer`、`/dashboard`、`/gtm-strategy` 等）在 v2.0 重构中已移除，可通过 `git log` 追溯或 `git checkout` 恢复。

## 九、横向能力：竞品分析工程化（v2.1 新增）

除了 M2-M7 主流水线，PM Harness 提供**横向的竞品分析工程化能力**，可独立跑或为主流水线提供输入。

### 两阶段流程

```
产品定位描述
    ↓
[阶段 1] /pm-competitive-scan
    · 竞品发现（4 类）：直接 / 间接 / 替代 / 自建
    · 多信源采集：🟢 官方一手 + 🟡 三方评测 + 🟠 社区口碑
    · 情报卡结构化 JSON
    · 可信度分级
    ↓  🔒 Gate（竞品清单确认）
    ↓
[阶段 2] /pm-competitive-benchmark
    · 5 维对标：功能 / 定价 / 生态 / 口碑 / 技术架构
    · 5 类洞察：优势 / 劣势 / 价值链差距 / 定价错位 / 未满足需求
    · Blue Ocean 差异化布局：消除 / 减少 / 提升 / 创造
    · Positioning 二维定位矩阵
    · 应对四象限：领先 / 侧翼 / 跟随 / 避战 / 合作
    · 销售话术 + 竞品 FAQ
    ↓  🔒 Gate（战略产出确认）
    ↓
完整竞品分析报告
```

### 一键编排

```bash
/pm-competitive "产品定位" [--depth quick|deep] [--seed <竞品名>]
```

### 三种模式

| 模式 | 场景 | 时长 |
|---|---|---|
| `--mode full`（默认） | 首次分析 / 立项前 | 30 分钟 - 3 小时（看 depth） |
| `--mode monitor` | 月度轻量刷新 | 10-20 分钟 |
| `--mode refresh` | 季度全量刷新（对比历史版本） | 与 full 相当 |

### 与主流水线的组合

竞品分析作为**横向能力**，可以在主流水线的多个阶段作为输入：

```
1. 立项前     → /pm-competitive → /pm-clarify（作为背景）
2. 方案定位   → 竞品报告 → /pm-solution（作为差异化依据）
3. PRD 补章节 → 竞品报告 → /prd --input（引用"竞品对比"章节）
4. 常态跟踪   → 每月 /pm-competitive --mode monitor
```

### 目录结构

```
./output/competitive/{topic-slug}-{yyyymmdd}/
├── .competitive-state.json      ← 状态
├── 01-competitor-list.md         ← 阶段 1
├── 01-competitors.json           ← 阶段 1（下游依赖）
├── 01-competitor-*.json          ← 单竞品情报卡
├── 01-intel-sources.md
├── 01-intel-log.md
├── 02-benchmark-matrix.md        ← 阶段 2
├── 02-insights.md
├── 02-positioning.md
├── 02-strategy.md
├── 02-sales-playbook.md
├── 02-report-full.md              ← 主产出
├── VERSION
├── CHANGELOG.md
├── MONITOR-{yyyymm}.md          ← Monitor 产出
└── DIFF-v{n}-v{n+1}.md            ← Refresh 产出
```

### 与 SA 场景边界

| 场景 | 用 PM 竞品命令 or SA 命令 |
|---|---|
| **内部产品线整体竞争分析** | `/pm-competitive` |
| **客户具体项目的竞争定位** | `/sa-solution-map`（含竞品章节） |
| 立项前市场判断 | `/pm-competitive` |
| 招投标应答的竞品对标 | `/sa-solution-map` + `/sa-rfp` |

**规则**：产品级竞争走 PM，项目级竞争走 SA。两者可以互相引用。

## 九、反模式（禁止）

- ❌ **跳过 M2 直接写 PRD**——放弃了流水线的核心价值
- ❌ **用 --skip-gate 交付客户**——gate 是质量红线
- ❌ **PRD 不跑 --validate**——完整性无保障
- ❌ **没跑 M6 就交付**——客户会质疑技术能力
- ❌ **手工改 .pipeline-state.json**——状态不一致
- ❌ **修改 _frozen/ 内文件**——审计留档不可篡改
- ❌ **一句话需求跳过澄清直接编码**——生产事故温床

## 十、演进路线

- ✅ v1.0（2026-08-27）：首版 6 模块流水线上线
- ⏳ v1.1：接入 Linear MCP，M7 归档后自动创建 Linear Issue
- ⏳ v1.2：M4 原型 JSON 增加 Penpot / Figma 官方插件的直接推送
- ⏳ v1.3：M6 技术指标接入行业基线库（等保 / SOC2 / HIPAA 模板自动填充）
- ⏳ v2.0：接入研发侧 `/devagent:dev-spec-dev`，实现 PM → 研发一键交接

## 十一、故障排查

| 症状 | 原因 | 解决 |
|---|---|---|
| M4 原型 JSON 无效 | Agent 4-1 输出格式错 | 重跑 M4 |
| M5 校验一直"需重写" | PRD 缺关键章节 | 手动补 → 重跑 --validate |
| M6 指标全是"合理" | 上游澄清报告太模糊 | 回 M2 补数字 |
| M7 归档拒绝 | 校验状态不通过 | 修复后再归档，或 --allow-force |
| /pm-pipeline 状态错乱 | .pipeline-state.json 被手改 | 删除文件重来 |

## 十二、快速上手

**第一次用**：

```bash
# 1. 用一个简单需求熟悉流水线
/pm-pipeline "做一个用户反馈收集页面" --mode auto --skip-gate

# 2. 看看产出目录长啥样
ls ./output/pm-pipeline/user-feedback-*/

# 3. 用正式模式跑一个真实需求
/pm-pipeline "真实的需求描述" --mode human --product-type saas-b
```

**升级你的日常习惯**：

- 老板给一句话 → 立刻 `/pm-pipeline`，30 分钟内交澄清报告
- 客户来紧急需求 → 走完整流水线，3-4 小时交完整交付包
- PoC 准备 → M6 输出直接对应验收标准
- 招投标响应 → freeze 一版当技术方案附件

---

**相关文档**：

- 顶层 Harness 框架：[`HARNESS_FRAMEWORK.md`](../HARNESS_FRAMEWORK.md)
- 项目级说明：[`.claude/CLAUDE.md`](../.claude/CLAUDE.md)
- PM 角色清单：[`roles/pm/manifest.yaml`](../roles/pm/manifest.yaml)
- 6 大命令文档：[`commands/product/pm-*.md`](../commands/product/)
- 7 大 skill 文档：[`skills/pm/pm-*/SKILL.md`](../skills/pm/)
