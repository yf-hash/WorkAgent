---
name: content-validate
description: 【模块 4】五类内容校验 — 输入初稿 + 素材池，跑事实一致性 / 合规风险 / 文体风格 / 完整性 / 引用可追溯 五类校验，输出《内容校验报告》，标记风险点。人工审核前的最后质量红线。
user-invocable: true
argument-hint: "<02-draft.md 路径> [<01-material-pool.md 路径>] [--focus fact|compliance|style|complete|reference|all] [--out <path>]"
allowed-tools: [Read, Write, Edit, AskUserQuestion, Grep, Glob]
model: sonnet  # 轻量：规则化 5 类校验对齐，opus 溢出
harness:
  execute:
    preset: writing-scoped
  constrain:
    profile: writing-safe
    gates: [before-write, after-validate]
  loop:
    mode: pipeline
    stages: [事实一致性, 合规风险, 文体风格, 完整性, 引用可追溯]
  memory:
    scope: project
    reads: [project-context, content-materials-history, content-generate-history]
    writes: [content-validate-history]
  security:
    danger-level: low
---

# /content-validate — 五类内容校验（Module 4）

> **端到端内容创作流水线的第 4 站 — 人工审核前的质量红线**
>
> /content-generate →【本命令】→ /content-archive

## 一句话

**跑五类校验（事实一致性 / 合规风险 / 文体风格 / 完整性 / 引用可追溯），输出《内容校验报告》标记风险点**，供人工审阅参考。

## 输入

```bash
# 最常见：接 M2 + M3 输出
/content-validate ./output/content-pipeline/xxx/02-draft.md ./01-material-pool.md

# 无素材池（跳过事实 + 引用校验）
/content-validate ./02-draft.md

# 只跑特定校验
/content-validate ./02-draft.md ./01-material-pool.md --focus compliance
/content-validate ./02-draft.md ./01-material-pool.md --focus fact
```

## 五类校验

### 校验 1：事实一致性（需素材池）

调用 `skills/content/content-validate` 的规则库：
- 遍历初稿中所有具体事实（数字 / 能力 / 客户 / 案例）
- 对比素材池：
  - ✅ 一致：直接来自素材
  - 🟡 部分一致：夸大 or 简化
  - 🔴 不一致：与素材冲突
  - ⚠️ 未在素材池：可能 AI 合成，需人工确认

### 校验 2：合规风险

扫描绝对化用词 + 敏感词 + 行业禁语：
- 广告法关键词：最 / 第一 / 唯一 / 100% / 永远 / 绝对
- 行业禁语（依受众）
- 未授权披露内容（客户名 / 内部估算）

### 校验 3：文体风格

对比 `content-templates` 里对应文体的规范：
- 章节结构是否完整
- 语气是否匹配（PR 稿 vs 推文的语气应显著不同）
- 长度是否在容忍范围
- 是否有该文体的必备要素（如 PR 稿必须有引用）

### 校验 4：完整性

按文体的必备要素 checklist 检查：

| 文体 | 必查 |
|---|---|
| tech-whitepaper | 架构图、技术指标数字、局限承认、术语表 |
| solution-whitepaper | Summary、行业数据、Mermaid、案例、ROI、落地路径 |
| ppt | 每页 title/bullets/visual/note、Q&A 页 |
| pr | 5W1H 导语、引用（含姓名+职位）、Boilerplate |
| promo | 一句话价值主张、具体收益数字、CTA |
| solution-doc | 痛点-能力映射表、部署形态、场景 |
| activity-tweet | 亮点、福利、CTA |
| tech-popular | 类比、局限承认、拓展 |

### 校验 5：引用可追溯（需素材池）

遍历初稿中所有引用（数字 / 客户 / 案例 / 指标）：
- 每个引用是否能在素材池找到？
- 未找到 → 标"自定义假设"
- 找到 → 记录来源

## Harness 卡点（关键红线）

**校验后 gate**：AskUserQuestion 展示：

```
【M4 五类校验完成】

事实一致性：{n1}/{total1} 通过
  🔴 冲突：{c1} 处
  🟡 部分：{p1} 处
  ⚠️ 未在素材：{u1} 处

合规风险：{c} 处高风险 / {m} 处中风险
  🔴 绝对化词：{列表}
  🔴 未授权披露：{列表}

文体风格：{s}/10 分（{style} 规范匹配度）

完整性：{完整/不完整}
  缺失：{列表}

引用可追溯：{n}/{total} 有来源

--------------------------------
总体判定：{通过 / 有修改建议 / 需重写}

请选择：
(1) 编辑初稿后重跑校验 → 我改后按回车
(2) 局部重写某章节 → /content-generate --section {n}
(3) 全部重跑生成 → /content-generate 从头
(4) 强制通过（记入 known-issues.md）→ 谨慎
(5) 中止
```

## 输出格式

### 03-validate-report.md

```markdown
# 内容校验报告

> 初稿：02-draft.md
> 素材池：01-material-pool.md
> 生成时间：{{yyyy-mm-dd hh:mm}}

## 总体判定
- ✅ 通过 / 🟡 有修改建议 / 🔴 需重写

## 1. 事实一致性 [n]/[total]
| # | 初稿位置 | 描述 | 素材池对应 | 判定 | 建议 |
|---|---|---|---|---|---|
| F1 | § 3.2 沙箱能力 | "同时运行 100 个沙箱" | M-001（PRD § 3.2） | ✅ | — |
| F2 | § 3.3 性能 | "P95 200ms" | M-002（tech-spec P3 P95 500ms） | 🔴 冲突 | 改为 P95 500ms |
| F3 | § 4 客户案例 | "服务 500 家客户" | 未在素材池 | ⚠️ | AI 合成，需删除或人工核实 |

## 2. 合规风险 [n]
| # | 位置 | 原文 | 类型 | 建议改写 |
|---|---|---|---|---|
| C1 | § 1 引言 | "业内最先进" | 🔴 广告法（绝对化） | 改为"行业领先水平" |
| C2 | § 5 优势 | "100% 安全" | 🔴 广告法 | 改为"全链路安全保障" |
| C3 | § 6 案例 | "某银行"（未匿名） | 🔴 未授权披露 | 改为"某大型商业银行" |

## 3. 文体风格
- 匹配度：{s}/10
- 章节结构：{✅/❌}
- 语气匹配：{✅/❌}
- 长度：{value}（目标 {target}，偏差 {δ}%）

### 详细
{对每个不合规项说明}

## 4. 完整性
- 必备要素：
  - [x] 一句话价值主张
  - [x] Mermaid 架构图
  - [ ] ROI 定量测算（缺失）
  - [x] 至少 2 个案例

### 缺失建议
- ROI 章节缺失 → 建议从 solution-map 的收益数据补
- 术语表缺失（技术白皮书必备）

## 5. 引用可追溯 [n]/[total]
| # | 引用 | 来源 | 判定 |
|---|---|---|---|
| R1 | "100 个沙箱" | M-001 | ✅ |
| R2 | "P95 500ms" | M-002 | ✅ |
| R3 | "500 家客户" | — | ❌ 自定义假设 |

## 6. 关键行动清单
| # | 优先级 | 动作 | 位置 |
|---|---|---|---|
| A1 | 🔴 | 删除"业内最先进" | § 1 |
| A2 | 🔴 | 修正 P95 数字 | § 3.3 |
| A3 | 🔴 | 删除或核实"500 家客户" | § 4 |
| A4 | 🟠 | 补 ROI 章节 | § 7 |

## 7. 推荐下一步
- 修复 🔴 项后重跑本命令
- 通过后 → `/content-archive`
```

## 通过标准

| 类别 | 通过标准 |
|---|---|
| 事实一致性 | 无 🔴 冲突 |
| 合规风险 | 无 🔴 绝对化 / 未授权 |
| 文体风格 | 匹配度 ≥ 7/10 |
| 完整性 | 必备要素齐全 |
| 引用可追溯 | 关键事实 100% 有来源 |

**总体判定**：
- 五项全过 → ✅ 通过
- 任一有 🔴 → 🔴 需重写
- 其他 → 🟡 有修改建议

## 与其他命令的边界

| 场景 | 用 |
|---|---|
| **初稿 + 素材 → 五类校验报告** | 本命令 |
| 归档 | 下一步 `/content-archive` |
| 一键端到端 | `/content`（编排器） |
| 只查合规（无素材） | 本命令 `--focus compliance` |
| PRD 校验（不同场景） | `/prd --validate`（PM 场景） |

## 反模式

- ❌ 无素材池却宣称"事实一致" —— 违规，此类必须标"未校验"
- ❌ 校验后无关键行动清单 —— 违规
- ❌ 🔴 项默认通过 —— 严重违规
- ❌ 校验只列问题不给改写建议 —— 违规
- ❌ 报告没有可信度维度 —— 违规
