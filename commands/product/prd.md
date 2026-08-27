---
name: prd
description: PRD 统一入口（v3.2）。唯一生成类 skill = prd-writer，四档模式：outline（1 页对齐）/ feature（单功能详版，PDF 10 项）/ full（多功能完整版）/ update（增量合并）。可叠加 --wireframe / --engineering / --validate（PRD 完整性 & 一致性 & 歧义 & 埋点四类校验）/ --input（引用上游澄清报告/业务方案/原型）。行业无关。
user-invocable: true
argument-hint: "<需求描述或 PRD 文件路径> --mode <outline|feature|full|update> [--wireframe] [--engineering] [--validate] [--input <files>] [--lang zh|en]"
allowed-tools: [Read, Write, Edit, AskUserQuestion]
harness:
  execute:
    preset: writing-scoped
  constrain:
    profile: writing-safe
    gates: [before-write]
  loop:
    mode: one-shot
  memory:
    scope: project
    reads: [project-context, clarify-history, solution-history, prototype-history]
  security:
    danger-level: low
---

# /prd — PRD 统一入口（v3.2）

## 一句话

**唯一生成类 skill = `prd-writer`**，四档模式覆盖 PRD 全生命周期，两个可选写作增强 + 一个校验模式 + 一个上游引用参数。

## v3.2 相比 v3.1 的变化

- ✅ **新增 `--validate`**：跑完 PRD 后自动执行四类校验（完整性 / 一致性 / 歧义文本 / 埋点完整性），输出独立校验报告
- ✅ **新增 `--input <files>`**：支持引用上游流水线产物（澄清报告 / 业务方案 / 原型 JSON），保证 PRD 与上游一致，避免上下游冲突
- ✅ **纳入端到端 6 模块流水线**（Module 5）：`/pm-clarify → /pm-solution → /pm-prototype → /prd → /pm-tech-spec`

## 用法

```bash
# ─── 生成类（输入是需求描述） ─────────────────────────
/prd 用户可以查看消费明细 --mode outline           # 1 页对齐
/prd 用户可以批量导出 Excel --mode feature         # 单功能详版（PDF 10 项）
/prd 开发 AI 写作助手浏览器插件 --mode full        # 多功能完整版

# ─── 增强开关（可叠加）─────────────────────────────
/prd 新用户注册引导流程 --mode feature --wireframe        # + ASCII 线框图（4 状态）
/prd 多租户 SaaS 权限中心 --mode full --engineering        # + 工程深度（状态机/字段规格/文案表）
/prd 复杂表单页 --mode full --wireframe --engineering     # 全增强

# ─── 校验模式（生成后自动跑，也可独立跑）───────────────
/prd ./PRD.md --validate                          # 独立跑校验，输出 PRD-validate.md
/prd 批量导入发票 --mode full --validate         # 生成 + 校验一站式

# ─── 引用上游流水线产物（M5 场景）──────────────────────
/prd 批量导入发票 --mode full --input ./output/pm-pipeline/xxx/01-clarify-report.md,./02-business-solution.md,./03-prototype/03-prototype-desc.md

# ─── 变更类（输入是 PRD 文件 + 变更描述）───────────────
/prd ./output/PRD-feature-XX.md --mode update 新增批量导入功能
```

## 分派规则

统一加载 `skills/prd/prd-writer/SKILL.md`，通过 `--mode` 参数控制内部路由：

| `--mode` | 输入 | 输出 |
|---|---|---|
| `outline` | 需求描述 | 1 页对齐稿（背景/用户/目标/功能清单/指标/不做） |
| `feature` | 需求描述 | 单功能详版：PDF 10 项 + 影响范围 + 明确不做 + GWT 验收 + 变更记录 |
| `full` | 需求描述 | 多功能完整版：全局章节 + 每功能用 10 项写 + 非功能 + 指标 + 发布 + 风险 |
| `update` | PRD 文件路径 + 变更描述 | 增量合并（原文保留 + 只改受影响章节 + 【本次更新】标记 + 版本递增） |

## 可选增强

| 标志 | 适用 mode | 作用 | 说明 |
|------|---|------|------|
| `--wireframe` | outline / feature / full | 加 ASCII 线框图 | 覆盖 4 种状态：默认 / 空态 / 加载 / 错误 |
| `--engineering` | outline / feature / full | 加工程实现深度 | 完整状态机 + 字段规格加强（索引/外键/幂等）+ 独立文案清单 + 字段级权限 |
| `--validate` | 全部 | 跑 PRD 校验 | 完整性 / 一致性 / 歧义文本 / 埋点四类，输出 `<PRD>-validate.md` |
| `--input` | 全部 | 引用上游产物 | 逗号分隔的文件路径，通常来自 pm-pipeline 目录 |
| `--lang` | 全部 | 输出语言 | `zh` / `en`，默认 zh |

## --validate 校验四类明细

调用 `skills/pm/pm-prd-validate`（新增）执行：

### 1. 完整性校验
检查 PRD 是否缺失：
- [ ] 异常场景（每个功能）
- [ ] 边界条件（数据范围、字符长度、并发上限）
- [ ] 权限说明（角色 × 功能）
- [ ] 失败处理（网络 / 超时 / 校验 / 依赖）
- [ ] 上线约束、风险点
- [ ] 埋点定义（关键动作）

### 2. 一致性校验（需 `--input`）
对比 PRD 与上游产物（澄清报告 / 业务方案 / 原型 JSON），检测：
- [ ] 目标用户是否一致
- [ ] 功能范围是否一致（P0/P1/P2）
- [ ] 页面清单是否与原型一致
- [ ] 权限矩阵是否一致
- [ ] 依赖清单是否一致

### 3. 歧义文本检测
扫描 PRD 中的模糊表述，标记【建议 PM 重写】：
- 高频模糊词：优化 / 提升 / 尽可能 / 快 / 好 / 更多 / 大部分 / 相关 / 合理 / 智能化
- 时间模糊：尽快 / 短时间内 / 未来 / 稍后
- 数量模糊：大量 / 少量 / 部分 / 若干

### 4. 埋点完整性
关键动作必须有埋点定义：
- [ ] 页面 PV / UV
- [ ] 表单提交（成功 / 失败）
- [ ] 支付 / 转化关键节点
- [ ] 错误页 / 空态触达
- [ ] 核心 CTA 点击

## 校验输出格式（`<PRD>-validate.md`）

```markdown
# PRD 校验报告：{{PRD 文件名}}

> 生成时间：{{yyyy-mm-dd hh:mm}}
> 关联上游：{{--input 文件列表}}

## 总体结论
- 通过 / 有修改建议 / 需重写

## 1. 完整性 [n] 项 - [status]
| # | 缺失 | 位置 | 严重度 | 建议补充 |
|---|---|---|---|---|

## 2. 一致性 [n] 项 - [status]
| # | 冲突 | PRD 位置 | 上游位置 | 建议 |
|---|---|---|---|---|

## 3. 歧义文本 [n] 项 - [status]
| # | 原文 | 位置 | 建议改写为 |
|---|---|---|---|

## 4. 埋点完整性 [n] 项 - [status]
| # | 缺失埋点 | 位置 | 建议 event 定义 |
|---|---|---|---|

## 5. 推荐下一步
- [ ] 认可 PRD → `/pm-tech-spec ./PRD.md --input <澄清报告>`
- [ ] 需修改 → `/prd ./PRD.md --mode update <修改点>`
```

## 自动推断（无 `--mode` 时）

```
输入是 <需求描述>（文本，非路径）
  → 用 AskUserQuestion 问：
    - outline（1 页对齐，10 分钟）
    - feature（单功能详版，PDF 10 项，30–60 分钟）
    - full（多功能完整 PRD，2–4 小时）

输入是 <.md 文件路径> + 有 --validate
  → 独立执行校验，不重写 PRD

输入是 <.md 文件路径> + 有变更描述文本
  → 默认走 --mode update

输入是 <.md 文件路径> + 无参数
  → 询问用户意图（评分 / 校验 / 增量更新）
```

## 与其他命令 / Agent 的边界

| 场景 | 用 |
|---|---|
| 早期想法对齐、立项前沟通 | 本命令 `--mode outline` |
| 单个功能点（Linear/Jira Issue 级） | 本命令 `--mode feature` |
| 多功能完整 PRD、正式评审 | 本命令 `--mode full` |
| 含线框图 | 任意生成 mode + `--wireframe` |
| B 端 / 多租户 / 私有化深度 | 本命令 `--mode full --engineering` |
| 已有 PRD 增量变更 | 本命令 `--mode update <PRD 路径> <变更描述>` |
| PRD 校验（不重写） | 本命令 `--validate` |
| **端到端 6 模块流水线** | `/pm-pipeline` 一键调度 |
| 需求澄清（更结构化） | `/pm-clarify`（M2） |
| 业务方案拆解 | `/pm-solution`（M3） |
| 原型底稿 | `/pm-prototype`（M4） |
| PRD → 技术规格书 | `/pm-tech-spec`（M6） |

## v2.x / v3.0 / v3.1 → v3.2 全量迁移映射

| 旧写法 | 新写法（v3.2） | 备注 |
|---|---|---|
| `--mode lite` | `--mode outline` | 语义等价 |
| `--mode standard` | `--mode full` | 语义等价 |
| `--mode enterprise` | `--mode full --engineering` | 严格 12 章 = full + 工程深度 |
| `--mode linear` | `--mode feature` | 语义等价，红线自检保留 |
| `--mode proto --fidelity low` | `--mode feature --wireframe` | 拆分为独立增强 |
| `--mode proto --fidelity mid` | `--mode full --wireframe --engineering` | 中保真 = full + 全增强 |
| `--mode impl` | `--mode full --engineering` | 语义等价 |
| `--mode xqy` | 已废弃，用 `--mode full --engineering` | 行业锁定移除 |
| `--mode diagnose` | 已废弃，走 `/devagent:pm-debate` 或 `/pm-clarify` | 想法诊断不属于 PRD 范畴 |
| `--mode concept` | 已废弃，直接用 `--mode outline` | outline 已覆盖 |
| `--mode spec-first` | 已废弃 | 工程范式，不再内置 |
| `--mode quality` | 用 `--validate` | 独立校验模式 |
| `--mode evaluate` | 已废弃 | 无对照基准 |
| `--flow discovery` | 已废弃，走 `/pm-clarify → /pm-solution` | 拆分职责 |
| `--stage` / `--fidelity` / `--module-type` / `--system` | 已废弃 | 已归档 |

## 归档说明

`skills/prd/` 目录下只保留 `prd-writer` 一个 skill；`skills/pm/pm-prd-validate/`（新增）负责 `--validate` 逻辑。恢复历史 skill：

```bash
git mv skills/prd/_archived/<skill-name> skills/prd/<skill-name>
```

详见 `skills/prd/_archived/README.md`。
