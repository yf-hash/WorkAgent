# SA Harness — 售前解决方案工程师端到端 7 模块流水线

> **销售转述的一句话 / RFP → 完整售前交付包**：从碎片化客户信息，经过 7 个 Agent 模块，产出可交付客户 / 商务 / 研发的完整售前包（含总体方案 + POC + 实施 + RFP 应答 + 报价底稿 + 归档）。
>
> 版本：v1.0（2026-08-27）

## 一、为什么需要这套 Harness

售前工程师 / 解决方案工程师的日常痛点：

- 销售给回**碎片化模糊客户信息**，需要人工补齐调研缺口
- 每个项目都要重复写调研报告、总体方案、POC 方案、投标应答、偏离表
- 方案容易**遗漏客户硬性约束**（等保、国产化、数据不出境）
- 全套项目物料版本难以追溯，客户需求变了要重头改
- 新人售前上手门槛高，历史案例难以复用

这套 Harness 的核心命题：

> **让大模型作为思考引擎，Harness 作为执行、约束、循环、记忆、安全的骨架**——
> 售前只需要给一句话客户信息或 RFP，然后在每个 gate 做质量把关。

### 相比传统售前工作流的差异化

| 传统售前流程 | 本 Harness |
|---|---|
| 拿到销售转述，人工整理客户信息 | M1：多源输入网关自动清洗 + 抽取 12 类元信息 |
| 客户信息模糊，人工发问题清单 | M2：调研澄清 Agent 自动识别 7 类缺口 + 三类问题清单 |
| 拆功能靠经验 | M3：业务-能力自动映射 + 竞品对标 + 5 类风险 |
| 方案画架构图靠 Visio | M4：架构自动生成 + Mermaid + 三项校验 |
| POC / 实施 / RFP 应答重复劳动 | M5：三个专项方案并行生成 |
| 报价拍脑袋 | M6：基于规则库的估算底稿（不是最终报价） |
| 版本管理靠 Word 另存为 | M7：语义化版本 + 变更触发下游重跑 |

## 二、7 模块流水线全景图

```
┌──────────────────────────────────────────────────────────────┐
│ 【输入】销售一句话 / RFP / 客户访谈转写 / PPT / Excel          │
└──────────────────────────────────────────────────────────────┘
                       │
                       ▼
    ┌──────────────────────────────────────────┐
    │  M1 多源客户输入网关                        │
    │  /sa-intake                               │
    │  ─────────────────────────                │
    │  · 非结构化清洗                             │
    │  · 元信息抽取（12 类）                      │
    │  · 需求模糊等级标记                         │
    │                                           │
    │  → 00-intake.json                         │
    └──────────────────────────────────────────┘
                       │
                    🔒 Harness Gate（关键字段确认）
                       ▼
    ┌──────────────────────────────────────────┐
    │  M2 客户调研澄清 Agent 套件                  │
    │  /sa-clarify                              │
    │  ─────────────────────────                │
    │  Agent 2-1: 信息缺口 & 歧义识别            │
    │  Agent 2-2: 调研问题生成（3 类）            │
    │  Agent 2-3: 痛点收敛（真实 vs 表面）         │
    │                                           │
    │  → 01-clarify-report.md                   │
    │  《客户调研与痛点分析报告》                   │
    └──────────────────────────────────────────┘
                       │
                    🔒 Harness Gate（售前审阅）
                       ▼
    ┌──────────────────────────────────────────┐
    │  M3 方案拆解与定位 Agent 套件               │
    │  /sa-solution-map                          │
    │  ─────────────────────────                │
    │  Agent 3-1: 业务-能力映射                  │
    │  Agent 3-2: 竞争分析                      │
    │  Agent 3-3: 风险 & 依赖识别                │
    │                                           │
    │  → 02-solution-map.md                     │
    └──────────────────────────────────────────┘
                       │
                    🔒 Harness Gate（定制范围锁定）
                       ▼
    ┌──────────────────────────────────────────┐
    │  M4 总体方案 & 架构 Agent 套件              │
    │  /sa-architect                            │
    │  ─────────────────────────                │
    │  Agent 4-1: 总体解决方案                   │
    │    · 8 章结构 + 5 层架构                    │
    │    · Mermaid 业务/技术/部署 3 张图           │
    │  Agent 4-2: 方案自动校验                   │
    │    · 痛点匹配 / 合规约束 / 可行性            │
    │                                           │
    │  → 03-overall-solution.md                 │
    │  → 03-architecture.mmd                    │
    │  → 03-solution-validate.md                │
    └──────────────────────────────────────────┘
                       │
                    🔒 Harness Gate（方案确认）
                       ▼
    ┌──────────────────────────────────────────┐
    │  M5 专项方案 Agent 套件（三合一）            │
    │  /sa-poc /sa-impl /sa-rfp                 │
    │  ─────────────────────────                │
    │  M5.1 POC 测试方案 Agent                  │
    │    · 范围 / 环境 / 用例 / 验收              │
    │  M5.2 实施方案 Agent                      │
    │    · 6 阶段 / RACI / 切换 / 培训            │
    │  M5.3 RFP 应答 Agent                      │
    │    · 逐条应答 + 打分项 + 偏离表              │
    │                                           │
    │  → 04-poc-plan.md                         │
    │  → 04-impl-plan.md                        │
    │  → 04-rfp-response.md + deviation-table   │
    └──────────────────────────────────────────┘
                       │
                    🔒 Harness Gate（专项确认）
                       ▼
    ┌──────────────────────────────────────────┐
    │  M6 报价 & 宣讲物料 Agent 套件             │
    │  /sa-quote                                │
    │  ─────────────────────────                │
    │  Agent 6-1: 配置估算（⚠️ 底稿）             │
    │    · 模块选型 / 服务器 / 许可 / 定制         │
    │  Agent 6-2: 宣讲材料底稿                    │
    │    · PPT 大纲 / 页面文案 / 汇报话术          │
    │                                           │
    │  → 05-config-estimate.md（底稿）           │
    │  → 05-presentation-outline.md              │
    │  → 05-presentation-copy.md                │
    │  → 05-pitch-script.md                     │
    └──────────────────────────────────────────┘
                       │
                    🔒 Harness Gate（估算商务确认）
                       ▼
    ┌──────────────────────────────────────────┐
    │  M7 产物统一管理 & 版本归档                  │
    │  /sa-archive                              │
    │  ─────────────────────────                │
    │  · 完整性检查（必备产物 12 类）              │
    │  · 售前特有交叉引用（痛点闭环 / 定制闭环等）  │
    │  · 语义化版本号（客户变更粒度）              │
    │  · freeze 只读快照（投标版 / POC 版）        │
    │  · 导出 Markdown / Word（对内 / 对客）      │
    │                                           │
    │  → README.md + CHANGELOG.md + VERSION     │
    │  → _frozen/{tag}/ + _export/               │
    └──────────────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────────┐
│ 【输出】完整可交付售前包                                        │
│  ./output/sa-pipeline/{client}-{project}-{yyyymmdd}/         │
└──────────────────────────────────────────────────────────────┘
```

## 三、7 模块产物清单

| 模块 | 命令 | 产物 | Skill 支撑 |
|---|---|---|---|
| M1 | `/sa-intake` | 00-intake.json + 解析日志 | sa-input-gateway |
| M2 | `/sa-clarify` | 01-clarify-report.md | sa-clarify |
| M3 | `/sa-solution-map` | 02-solution-map.md | sa-capability-mapping |
| M4 | `/sa-architect` | 03-overall-solution.md + arch.mmd + validate.md | sa-architect + sa-solution-validate |
| M5.1 | `/sa-poc` | 04-poc-plan.md | sa-poc-plan |
| M5.2 | `/sa-impl` | 04-impl-plan.md | sa-impl-plan |
| M5.3 | `/sa-rfp` | 04-rfp-response.md + deviation-table | sa-rfp-response |
| M6 | `/sa-quote` | 05-config-estimate.md + presentation-* | sa-quote-estimate + sa-presentation-draft |
| M7 | `/sa-archive` | README + CHANGELOG + VERSION | sa-artifact-archive |
| 一键编排 | `/sa-pipeline` | 全部 | 上述全部 |

## 四、目录结构约定

```
./output/sa-pipeline/{client}-{project}-{yyyymmdd}/
├── .pipeline-state.json         ← 流水线状态
├── 00-intake.json                ← M1
├── 00-intake-log.md
├── 00-raw-materials/             ← 原始文件
├── 01-clarify-report.md         ← M2
├── 02-solution-map.md           ← M3
├── 03-overall-solution.md       ← M4
├── 03-architecture.mmd          ← M4
├── 03-business-arch.mmd
├── 03-deployment-arch.mmd
├── 03-solution-validate.md      ← M4 校验
├── 04-poc-plan.md                ← M5.1
├── 04-impl-plan.md               ← M5.2
├── 04-rfp-parsed.json           ← M5.3 RFP 解析
├── 04-rfp-scoring.md             ← M5.3 打分分析
├── 04-rfp-response.md           ← M5.3 应答表
├── 04-deviation-table.md         ← M5.3 偏离表
├── 04-rfp-strategy.md           ← M5.3 内部策略
├── 05-config-estimate.md         ← M6 估算底稿
├── 05-presentation-outline.md    ← M6 PPT 大纲
├── 05-presentation-copy.md       ← M6 页面文案
├── 05-pitch-script.md            ← M6 汇报话术
├── review-notes.md               ← 人工审阅（可选）
├── README.md                     ← M7 索引
├── CHANGELOG.md                  ← M7 变更历史
├── VERSION                       ← M7 版本号
├── archive-report.md            ← M7 归档检查
├── _frozen/                      ← M7 冻结快照
│   └── v1.0-投标版/
└── _export/                     ← M7 导出
    ├── {project}-方案包.zip
    └── {project}-方案包.docx
```

## 五、如何使用

### 方式 A：一键全流程（推荐）

```bash
/sa-pipeline "某制造业客户，要替换老 MES，私有化 + 国产化，3 月上线" \
  --client "远大制造" \
  --industry manufacturing \
  --compliance 等保三级,国产化 \
  --deployment private
```

每阶段之间 gate 询问售前，全程 4-6 小时。

### 方式 B：通过总入口 /sa 智能识别

```bash
/sa 某制造业客户，要替换老 MES，需要私有化 + 国产化，3 月上线
```

`/sa` agent 识别"完整售前包"信号 → 推荐 `/sa-pipeline` → 用户确认 → 自动调用。

### 方式 C：手工分步执行

```bash
/sa-intake "客户信息" --client "XX"
/sa-clarify ./output/sa-pipeline/xxx/00-intake.json
/sa-solution-map ./01-clarify-report.md
/sa-architect ./02-solution-map.md
/sa-poc ./03-overall-solution.md  # 或 /sa-impl / /sa-rfp
/sa-quote ./03-overall-solution.md ./04-poc-plan.md
/sa-archive ./output/sa-pipeline/xxx/
```

### 方式 D：变更触发下游重跑

```bash
# 客户合规变了
/sa-pipeline ./output/sa-pipeline/xxx/ --from M3

# 只跑 RFP 应答
/sa-pipeline ./output/sa-pipeline/xxx/ --from M5 --stage-5 rfp

# 部署模式变了
/sa-pipeline ./output/sa-pipeline/xxx/ --from M6
```

## 六、Harness 卡点机制

流水线在每个阶段之间设置人工审阅卡点：

| Gate | 触发时机 | 用户选项 |
|---|---|---|
| after-M1 | 元数据抽取后 | 通过 / 补充字段 / 重新解析 |
| after-M2 | 调研报告生成后 | 通过 / 部分修改 / 驳回重跑 / 中止 |
| after-M3 | 方案定位 + 定制范围锁定 | 通过 / 调整能力匹配 / 驳回 |
| after-M4 | 方案 + 校验 | 通过 / 修改架构 / 校验 🔴 修复 |
| after-M5 | 专项方案完成 | 通过 / 补齐缺失 |
| after-M6 | 估算 + 宣讲底稿 | 通过（提醒商务确认） |
| before-freeze | freeze 前 | 确认 / 取消 |

**旁路**：`--skip-gate` 用于内部快速原型，正式项目严禁使用。

## 七、10 个 Skill 的能力矩阵

| Skill | 位置 | 服务命令 | 核心能力 |
|---|---|---|---|
| sa-input-gateway | skills/sa/ | /sa-intake | 多源输入清洗 + 12 类元信息抽取 + 模糊等级 |
| sa-clarify | skills/sa/ | /sa-clarify | 7 类调研 + 行业模板 + 伪需求 + 冲突规则 + 合规扫描 |
| sa-capability-mapping | skills/sa/ | /sa-solution-map | 覆盖度评级 + 定制分级 + 竞品维度 + 5 类风险 |
| sa-architect | skills/sa/ | /sa-architect | 5 层架构 + Mermaid + 部署选型 + 集成模式库 |
| sa-solution-validate | skills/sa/ | /sa-architect | 痛点匹配 + 合规映射 + 可行性冲突 |
| sa-poc-plan | skills/sa/ | /sa-poc | POC 范围界定 + 环境模板 + 用例格式 + 风险库 |
| sa-impl-plan | skills/sa/ | /sa-impl | 6 阶段模板 + RACI + 切换策略 + 培训计划 |
| sa-rfp-response | skills/sa/ | /sa-rfp | RFP 解析 + 打分项 + 应答话术 + 偏离表 |
| sa-quote-estimate | skills/sa/ | /sa-quote | 服务器规格计算 + 许可类型 + 定制分级 |
| sa-presentation-draft | skills/sa/ | /sa-quote | 8 章 PPT + 页面文案 + 话术 + Q&A 库 |
| sa-artifact-archive | skills/sa/ | /sa-archive | 目录扫描 + 售前交叉引用 + 变更触发规则 |

## 八、与 PM Harness 的关系

| | `/pm`（产品经理） | `/sa`（售前工程师） |
|---|---|---|
| 服务对象 | 内部产品 PM | 对外客户售前 SA |
| 输入 | 需求想法 / 用户反馈 | 销售转述 / RFP / 客户访谈 |
| 输出 | PRD + 技术规格书 | 方案 + POC + RFP 应答 + 报价 |
| 关注点 | 用户价值 / 功能规划 | 客户痛点 / 竞争定位 / 中标 |
| 流水线 | 6 模块（M2 澄清 → M7 归档） | 7 模块（M1 输入 → M7 归档） |
| 差异化 | 产品技术指标规格书 | RFP 应答 + 偏离表 + 报价估算 |
| 目录 | `./output/pm-pipeline/{topic}-{date}/` | `./output/sa-pipeline/{client}-{project}-{date}/` |

**共用**：两者都基于 Claude Code + `.claude/harness/` 五能力分层，共享 stage gate 机制、记忆管理、安全策略。

**互补场景**：
- 售前拿了客户合同，产品要拆解成内部功能开发 → 售前用 `/sa`，产品用 `/pm`
- 通用产品的立项 → 直接用 `/pm`
- 定制化客户项目 → 用 `/sa`

## 九、反模式（禁止）

- ❌ **跳过 M2 直接写方案** —— 放弃了流水线的核心价值
- ❌ **用 --skip-gate 交付客户版** —— gate 是质量红线
- ❌ **合规约束用 auto 假设** —— 生产事故温床
- ❌ **报价底稿当正式报价** —— 商务翻脸
- ❌ **投标场景没跑 M5.3** —— 违规，就没有应答表
- ❌ **修改 _frozen/ 内文件** —— 审计留档不可篡改
- ❌ **一句话客户信息跳过澄清直接投标** —— 中标了也交付不了

## 十、演进路线

- ✅ v1.0（2026-08-27）：首版 7 模块流水线上线
- ⏳ v1.1：M1 支持 PDF OCR / 语音转写自动化
- ⏳ v1.2：M5.3 RFP 应答支持自动引用历史应答库
- ⏳ v1.3：M6 估算接入行业价格库
- ⏳ v2.0：与 CRM 集成，客户信息 / 项目阶段 自动同步

## 十一、故障排查

| 症状 | 原因 | 解决 |
|---|---|---|
| M1 解析 PDF 失败 | 依赖 PDF 解析库 | 用 --with 手动指定或转 markdown |
| M2 合规字段全空 | 原文没提 | 用 --mode human 补齐 |
| M4 校验一直"需重写" | 方案缺关键章节 | 手动补 → 重跑 |
| M5.3 应答满足率 < 80% | 方案与 RFP 不匹配 | 回 M4 加强能力覆盖 |
| M6 服务器数量不合理 | 客户规模数字缺 | 回 M2 补 |
| /sa-pipeline 状态错乱 | .pipeline-state.json 被手改 | 删除文件重来 |

## 十二、快速上手

**第一次用**：

```bash
# 1. 简单需求熟悉流水线
/sa-pipeline "客户想做一个用户反馈收集系统" --mode auto --skip-gate

# 2. 看看产出目录长啥样
ls ./output/sa-pipeline/*/

# 3. 用正式模式跑真实需求
/sa-pipeline "真实客户信息" \
  --client "XXX" \
  --industry manufacturing \
  --compliance 等保三级 \
  --deployment private
```

**升级你的日常习惯**：

- 销售给一句话 → 立刻 `/sa-pipeline`，1 小时内交调研报告
- 拿到 RFP → 走 `/sa-pipeline --stage-5 rfp`，4-6 小时交完整应答
- 客户要 POC → `/sa-pipeline --stage-5 poc`，交 POC 方案 + 环境要求
- 客户合规变了 → `/sa-pipeline ./xxx/ --from M3`，几十分钟出新方案

---

**相关文档**：

- 顶层 Harness 框架：[`../HARNESS_FRAMEWORK.md`](../HARNESS_FRAMEWORK.md)
- PM Harness 总览：[`PM_HARNESS.md`](PM_HARNESS.md)
- 项目级说明：[`../.claude/CLAUDE.md`](../.claude/CLAUDE.md)
- SA 角色清单：[`../roles/sa/manifest.yaml`](../roles/sa/manifest.yaml)
- 10 大命令文档：[`../commands/presales/sa-*.md`](../commands/presales/)
- 11 大 skill 文档：[`../skills/sa/sa-*/SKILL.md`](../skills/sa/)
