---
name: pm-clarify
description: 【模块 2】需求澄清 Agent 套件 — 三合一：歧义识别 + 澄清问题生成 + 需求收敛&冲突检测。输入一句话原始需求，输出《需求澄清报告》。支持 auto（自问自答，标注假设项）/ human（问题清单交给 PM 回答）两种模式。
user-invocable: true
argument-hint: "<原始需求（一句话或短段落）> [--mode auto|human] [--product-type saas-b|c-end|internal] [--out <path>]"
allowed-tools: [Read, Write, Edit, AskUserQuestion, Grep, Glob]
harness:
  execute:
    preset: writing-scoped
  constrain:
    profile: writing-safe
    gates: [before-write, after-clarify-report]
  loop:
    mode: pipeline
    stages: [识别歧义, 生成问题, 冲突检测, 汇总报告]
  memory:
    scope: project
    reads: [project-context]
    writes: [clarify-history]
  security:
    danger-level: low
---

# /pm-clarify — 需求澄清 Agent 套件（Module 2）

> **端到端 6 模块流水线的第 1 站**
>
> 用户输入 →【本命令】→《需求澄清报告》→ /pm-solution → /pm-prototype → /prd → /pm-tech-spec → /pm-archive

## 一句话

**把老板/销售/客户一句话的模糊想法，变成一份结构化、经过冲突检测、明确标注假设与待确认项的《需求澄清报告》**。

## 输入

```bash
# 最简：一句话需求 + 自动模式
/pm-clarify 做一个邮箱验证码功能 --mode auto

# 显式指定产品类型
/pm-clarify 客户想要批量导出发票 --mode human --product-type saas-b

# 指定输出路径（默认 ./output/pm-pipeline/{topic}-{yyyymmdd}/01-clarify-report.md）
/pm-clarify "让 AI 帮我审批合同" --mode auto --out ./output/legal-ai/01-clarify.md
```

## 两种运行模式

| 模式 | 触发 | 行为 | 适合场景 |
|---|---|---|---|
| `auto`（默认） | `--mode auto` | Agent 基于同类产品知识库自问自答，所有推断结论 **必须** 标记【假设项，需要 PM 确认】 | PM 想快看一份"半成品报告"再决定要不要人工介入 |
| `human` | `--mode human` | Agent 只出问题清单，等 PM 回答后再继续 | 需求方向确实模糊、假设风险高、必须先对齐 |

未指定 `--mode` 时，用 AskUserQuestion 询问一次。

## 内部三个子 Agent（顺序执行）

### Agent 2-1：需求歧义识别

**做什么**：基于上下文识别下列七要素中缺失/歧义的部分：

1. **业务目标**（为什么做？成功指标是什么？）
2. **用户是谁**（角色、规模、付费能力）
3. **使用场景**（何时何地何种情境）
4. **成功标准**（可量化的衡量指标）
5. **边界范围**（做什么 / 不做什么）
6. **约束**（时间、预算、合规、技术）
7. **排除项**（明确不覆盖的场景）

**输出**：`【缺失清单】` + `【歧义清单】`

### Agent 2-2：澄清问题生成

**做什么**：把缺失/歧义转成面向提出人的提问，分三类：

- **业务问题**（目标、价值、优先级）
- **用户场景问题**（角色、频率、异常）
- **约束条件问题**（合规、性能、集成）

**auto 模式**下：Agent 用 `skills/pm/pm-requirement-clarify` 里的 B 端/SaaS 模板给出参考答案，逐条标【假设项】。
**human 模式**下：直接输出问题清单，暂停等 PM 回答。

### Agent 2-3：需求收敛 & 冲突检测

**做什么**：

1. 检测需求内部冲突（例：既要简单快速上线 vs 支持十万级并发）
2. 分类三类需求：**业务目标 / 功能需求 / 非功能需求**
3. 识别**伪需求**（例："想要一个导出按钮" ← 真实业务目标可能是"月末对账"）

**输出**：《需求澄清报告》

## 输出格式（《需求澄清报告》标准结构）

```markdown
# 需求澄清报告：{{topic}}

> 生成时间：{{yyyy-mm-dd hh:mm}}
> 模式：auto / human
> 原始输入：{{raw_input}}

## 1. 业务背景
（谁 / 因为什么 / 想解决什么问题）

## 2. 业务目标
（可量化的成功指标；模糊表述必须重写）

## 3. 目标用户
| 角色 | 规模 | 关键动机 | 决策权 |
|---|---|---|---|

## 4. 使用场景
（3-5 个典型场景，含频率与关键动作）

## 5. 成功衡量指标
（业务指标 + 产品指标 + 用户指标；每项必须可测量）

## 6. 需求范围
### 6.1 本次包含
### 6.2 明确不包含
（"不做什么"和"做什么"同等重要）

## 7. 假设项【重要】
| # | 假设内容 | 依据 | 需要 PM 确认 |
|---|---|---|---|

## 8. 待确认项【重要】
| # | 问题 | 分类 | 影响 | 建议决策人 |
|---|---|---|---|---|

## 9. 检测到的冲突
| # | 冲突项 A | 冲突项 B | 影响 | 建议 |
|---|---|---|---|---|

## 10. 伪需求识别
| 表面需求 | 可能的真实需求 | 依据 |
|---|---|---|

## 11. 风险点
（法务 / 合规 / 商业 / 交付）

## 12. 推荐下一步
- [ ] 若 PM 认可假设项 → `/pm-solution ./01-clarify-report.md`
- [ ] 若需修改 → 回到本命令加 `--refine` 参数迭代

## 附：调用的 Skill
- pm-requirement-clarify（B 端 / SaaS 模板）
- pm-discovery-frameworks（JTBD / 场景卡）
- pm-prioritization-frameworks（分类判断）
```

## Harness 卡点（流水线关键动作）

- **产出前 gate**：三个子 Agent 顺序执行完毕，输出草稿前 **强制** AskUserQuestion：
  - "假设项数量：{n}，是否需要 human 模式重跑覆盖？"
  - "检测到冲突：{列表}，是否要求 PM 先解决再进入 M3？"
- **产出后 gate**：写入报告文件后自动打印下一步命令：
  ```
  ✅ 需求澄清报告已生成：./output/.../01-clarify-report.md
  🔒 Harness 卡点：请人工审核报告
  ▶ 通过 → /pm-solution ./output/.../01-clarify-report.md
  ▶ 驳回 → /pm-clarify --refine "补充：..." （回到本命令）
  ```

## 与其他命令的边界

| 场景 | 用 |
|---|---|
| **一句话原始需求 → 结构化澄清** | 本命令 |
| 需求已澄清、要写业务方案 | `/pm-solution` |
| 需要一键跑完整 6 模块流水线 | `/pm-pipeline` |

## 反模式

- ❌ auto 模式没标【假设项】——违规，必须重跑
- ❌ 输出没有"明确不包含"章节——违规，说明未完成边界收敛
- ❌ 冲突检测栏留空——违规，至少要写"未检测到冲突"
- ❌ 直接调用 `/prd` 跳过本命令——放弃了 6 模块流水线的价值

## 输出目录约定

默认 `./output/pm-pipeline/{topic}-{yyyymmdd}/01-clarify-report.md`，其中：
- `{topic}` = 从 raw_input 提取的关键词（≤ 8 字符，自动 slug）
- `{yyyymmdd}` = 生成日期

如需自定义：`--out <path>`。
