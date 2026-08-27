---
name: sa-archive
description: 【模块 7】售前产物统一管理 & 版本变更管理 — 扫描 sa-pipeline 目录，生成 README 索引 / CHANGELOG / 版本号 / 交叉引用检查报告，支持局部重跑管理、变更触发下游重跑、Markdown/Word 导出。
user-invocable: true
argument-hint: "<sa-pipeline 目录路径> [--bump major|minor|patch] [--freeze] [--tag <name>] [--export markdown|word]"
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob, AskUserQuestion]
model: sonnet  # 轻量：归档 + 版本递增，无需 opus
harness:
  execute:
    preset: writing-scoped
    tools: [Bash]  # extend: freeze 打包 / Word 导出
  constrain:
    profile: writing-safe
    gates: [before-write, before-freeze]
  loop:
    mode: one-shot
  memory:
    scope: project
    reads: [project-context]
    writes: [archive-history]
  security:
    danger-level: low
---

# /sa-archive — 售前产物归档（Module 7）

> **端到端 7 模块流水线的第 7 站（收尾）**

## 一句话

**扫描 sa-pipeline 目录里的 6 类产物，生成 README 索引 + CHANGELOG + 版本号 + 交叉引用完整性检查报告，可 freeze 只读版本快照或导出为 Markdown/Word**。

## 输入

```bash
# 归档一个已完成的流水线目录
/sa-archive ./output/sa-pipeline/mfg-mes-20260827/

# 递增 minor 版本（新增场景 / 应答项）
/sa-archive ./output/sa-pipeline/xxx/ --bump minor

# freeze 冻结（生成不可修改的只读快照）
/sa-archive ./output/sa-pipeline/xxx/ --freeze --tag "v1.0-投标版"

# 导出为 Markdown 打包（供内部）
/sa-archive ./output/sa-pipeline/xxx/ --export markdown

# 导出为 Word（供客户提交）
/sa-archive ./output/sa-pipeline/xxx/ --export word
```

## 必备产物 checklist

| 文件 | 归属 | 必需 | 缺失后果 |
|---|---|---|---|
| `00-intake.json` | M1 | 必需 | 无项目元数据 |
| `01-clarify-report.md` | M2 | 必需 | 无调研依据 |
| `02-solution-map.md` | M3 | 必需 | 无能力映射 |
| `03-overall-solution.md` | M4 | 必需 | 无总体方案 |
| `03-architecture.mmd` | M4 | 必需 | 无架构图 |
| `03-solution-validate.md` | M4 | 强烈建议 | 无校验 |
| `04-poc-plan.md` | M5.1 | 视场景 | 无 POC 交付时缺 |
| `04-impl-plan.md` | M5.2 | 视场景 | 无实施交付时缺 |
| `04-rfp-response.md` | M5.3 | 视场景 | 无投标场景时缺 |
| `04-deviation-table.md` | M5.3 | 与 04-rfp 同 | |
| `05-config-estimate.md` | M6 | 必需 | 无估算依据 |
| `05-presentation-outline.md` | M6 | 视场景 | 无对客汇报时缺 |

## 输出

```
./output/sa-pipeline/{client}-{project}-{yyyymmdd}/
├── README.md                    ← 【本命令产出】索引 + 版本 + 状态
├── CHANGELOG.md                 ← 【本命令产出】变更历史
├── VERSION                       ← 【本命令产出】语义化版本号
├── archive-report.md           ← 【本命令产出】完整性 + 交叉引用报告
├── review-notes.md              ← 【本命令产出，可选】人工审阅记录
├── _frozen/                    ← --freeze 生成
│   └── v1.0-投标版/            ← 只读快照
└── _export/                    ← --export 生成
    ├── {project}-方案包.zip     ← Markdown 打包
    └── {project}-方案包.docx    ← Word 版本（如指定 --export word）
```

## 三步流程

### 步骤 1：完整性 + 交叉引用检查

调用 `skills/sa/sa-artifact-archive`：

**完整性 checklist**（见上表）

**交叉引用检查**：
- 总体方案（M4）引用的痛点是否都在痛点报告（M2）中
- 定制清单（M3）与 POC 必测项（M5.1）是否一致
- RFP 应答（M5.3）的技术偏离是否在方案（M4）中反映
- 配置估算（M6）的模块是否都在方案（M4）中
- M2 假设项是否被下游全部响应

**校验状态确认**：
- M4 solution-validate 不能是"需重写"
- M5.3 应答表满足率必须显式

### 步骤 2：生成 README.md

```markdown
# 售前方案包：{{client}} - {{project}}

> 版本：v{{semver}}
> 状态：草稿 / 评审中 / 已冻结（投标版）
> 项目阶段：{{stage}}
> 生成日期：{{yyyy-mm-dd}}

## 客户信息（脱敏时可选省略）
- 客户名：{{client}}
- 行业：{{industry}}
- 项目名：{{project}}
- 项目阶段：{{stage}}
- 关键联系人：{{...}}

## 交付物索引

| # | 阶段 | 产物 | 状态 |
|---|---|---|---|
| M1 | 输入接入 | [00-intake.json](./00-intake.json) | ✅ |
| M2 | 客户调研 | [01-clarify-report.md](./01-clarify-report.md) | ✅ |
| M3 | 方案拆解 | [02-solution-map.md](./02-solution-map.md) | ✅ |
| M4 | 总体方案 | [03-overall-solution.md](./03-overall-solution.md) + [arch](./03-architecture.mmd) + [validate](./03-solution-validate.md) | ✅ |
| M5.1 | POC 方案 | [04-poc-plan.md](./04-poc-plan.md) | ✅ |
| M5.2 | 实施方案 | [04-impl-plan.md](./04-impl-plan.md) | ✅ |
| M5.3 | RFP 应答 | [04-rfp-response.md](./04-rfp-response.md) + [偏离](./04-deviation-table.md) | ✅ |
| M6 | 报价宣讲 | [05-config-estimate.md](./05-config-estimate.md) + [pitch](./05-presentation-outline.md) | ✅ |

## 关键结论

### 项目定位（一句话）
{{从 02-solution-map.md § 6 提取}}

### 我方三大差异化
{{从 03-overall-solution.md 提取}}

### 关键风险
{{从各处 § 风险 提取严重度=高的项}}

### 商务提醒
{{从 05-config-estimate.md § 商务提醒 提取}}

## 变更历史

见 [CHANGELOG.md](./CHANGELOG.md)

## 对内 vs 对客

### 对内版本（本目录全部）
- 含商务提醒 / 内部估算 / 应答策略

### 对客版本（./_export/客户版/）
- 移除 review-notes.md / 05-quote § 商务提醒 / 04-rfp-strategy.md
- 添加客户 LOGO / 保密声明

## 局部重跑指南

- 客户需求变了 → 回 `/sa-clarify --refine`
- 方案架构变了 → 回 `/sa-architect --refine`
- 部署方案变了（影响估算） → 只重跑 `/sa-quote`
- RFP 有新版本 → 只重跑 `/sa-rfp`

## 与内部研发协作

- 系统技术方案交给研发：将 03-overall-solution.md + 05-config-estimate.md 交给研发
- 测试用例设计：将 04-poc-plan.md 交给测试团队
- 合同 / 报价：将 05-config-estimate.md + 04-rfp-response.md 交给商务
```

### 步骤 3：生成 CHANGELOG

初次归档：
```markdown
# CHANGELOG

## v1.0.0 - 2026-08-27

### 初次归档
- [x] M1 输入网关（source: sales）
- [x] M2 客户调研（human 模式）
- [x] M3 方案拆解（3 个定制点，5 个风险）
- [x] M4 总体方案（6 大模块，20 台服务器）
- [x] M5.1 POC 方案（4 周，5 个必测用例）
- [x] M5.2 实施方案（3 月周期）
- [x] M5.3 RFP 应答（94 条，满足率 97.9%）
- [x] M6 配置估算 + 宣讲底稿

### 待客户确认（M2 假设项）
- {列表}

### 未解决问题
- {从校验的 ❌ 项汇总}
```

后续归档：
```markdown
## v1.1.0 - 2026-09-05

### 修改（minor）
- [x] M4 方案调整数据库为 GaussDB（客户要求）
- [x] M6 服务器数量从 20 → 22 台（数据库副本变化）

### 未变
- M1 / M2 / M3 / M5 保持 v1.0.0
```

## Harness 卡点

- **归档前 gate**：如果任一校验报告状态 = "需重写"，AskUserQuestion：
  ```
  以下产物未通过校验，是否仍要归档？
    - 03-solution-validate.md：需重写（"数据不出境"未回应）
    - 04-rfp-response.md：满足率仅 82%

  - n（推荐）：先回上游修复
  - y-force：强制归档，问题写入 known-issues.md
  ```
- **freeze 前 gate**：`--freeze` 二次确认

## 变更触发下游重跑

售前场景常见变更：

| 变更 | 触发重跑 |
|---|---|
| 客户新增 P0 痛点 | M2 → M3 → M4 → M5 → M6 |
| 客户合规约束变化 | M3 → M4 → M5 → M6 |
| 部署模式改变 | M4 → M6 |
| RFP 新版本 | M5.3 → M6 |
| 客户规模数字变化 | M6 |

用 `/sa-pipeline --from Mx` 触发。

## 导出格式

### --export markdown
- 打包全部 md + mmd + json → zip
- 保留目录结构

### --export word
- 使用 pandoc 转换（需要客户机器安装 pandoc）
- 合并成一份大 docx（对客户友好）
- 生成两版：对内完整版 / 对客脱敏版

## 与其他命令的边界

| 场景 | 用 |
|---|---|
| **完成流水线，归档** | 本命令 |
| freeze 为投标版 | 本命令 `--freeze --tag "v1.0-投标版"` |
| 导出交付客户 | 本命令 `--export word` |
| 全流程一键 | `/sa-pipeline` |

## 反模式

- ❌ 校验未过就 freeze —— 违规
- ❌ 对客版本未脱敏 —— 违规
- ❌ 修改 _frozen/ 内容 —— 违规（审计留档不可篡改）
- ❌ 版本号乱跳 —— 违规
- ❌ CHANGELOG 遗漏关键变更 —— 违规
