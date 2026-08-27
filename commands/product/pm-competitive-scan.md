---
name: pm-competitive-scan
description: 【竞品分析 - 阶段 1】竞品发现 + 情报采集。输入我方产品定位或客户场景，自动/引导识别四类竞品（直接/间接/替代/自建），对每个竞品采集官网/定价/文档/社区口碑等多信源情报，输出结构化情报卡 JSON。
user-invocable: true
argument-hint: "<产品定位/客户场景/关键词> [--seed <竞品名逗号分隔>] [--depth quick|deep] [--out <path>]"
allowed-tools: [Read, Write, Edit, AskUserQuestion, WebFetch, WebSearch, Grep, Glob, Bash]
harness:
  execute:
    preset: research
    tools: [Bash]  # extend: 站点抓取辅助脚本（curl / html2text）
  constrain:
    profile: research
    gates: [before-write, after-competitor-list, after-intel-collect]
  loop:
    mode: pipeline
    stages: [竞品发现, 信源采集, 情报卡结构化, 可信度分级]
  memory:
    scope: project
    reads: [project-context]
    writes: [competitive-history]
  security:
    danger-level: low
---

# /pm-competitive-scan — 竞品发现 + 情报采集（阶段 1）

> **PM Harness 横向能力 - 竞品分析工程化能力（阶段 1/2）**
>
> 【本命令】/pm-competitive-scan → /pm-competitive-benchmark（阶段 2）→ 完整竞品分析报告

## 一句话

**给一段产品定位或客户场景，自动识别竞品（四类：直接/间接/替代/自建）并采集多信源情报，输出结构化情报卡 JSON**，供下游对标使用。

## 输入

```bash
# 最简：一段产品定位
/pm-competitive-scan "AI 写作助手，面向中小企业内容营销团队"

# 指定种子竞品（避免遗漏关键玩家）
/pm-competitive-scan "AI 写作助手" --seed "Jasper,Copy.ai,ChatGPT,Notion AI"

# 深度采集（对每家竞品跑更多信源）
/pm-competitive-scan "AI 写作助手" --depth deep

# 输出到指定路径
/pm-competitive-scan "AI 写作助手" --out ./output/competitive/ai-writer-20260827/
```

## 内部四阶段

### 阶段 1：竞品发现

调用 `skills/pm/pm-competitive-intel` 的方法论：

1. **强制四类都覆盖**：直接 / 间接 / 替代 / 自建
2. **来源多样化**：搜索 + 用户提及 + 应用商店 + 行业评测 + 社区
3. **数量控制**：直接 3-6 家、间接 2-4 家、替代 1-2 家、自建 1 家

**输出**：竞品候选清单（每家含 name / type / url / 发现来源）

### 阶段 2：信源采集

对每家竞品，按可信度顺序采集：

- 🟢 **高可信**（必采）：官网、定价页、产品文档、Changelog
- 🟡 **中可信**（推荐）：G2/Capterra 评分、独立评测
- 🟠 **中低可信**（快速扫）：Reddit / HN 讨论、Twitter 最近动态
- 🔴 **低可信**（不采）：传闻、竞品对我方的宣传

`--depth deep` 时全部采集，`--depth quick` 只采 🟢 🟡。

### 阶段 3：情报卡结构化

每家竞品生成一份 JSON 情报卡（Schema 见 skill 文档）：
- competitor 元信息
- positioning（定位）
- pricing（定价套餐 + 单位经济）
- capabilities（core / unique / integrations）
- tech（模型 / 部署 / API）
- traction（客户 / 融资）
- community_signals（评分 / Top 抱怨 / Top 好评）
- recent_changes（近 6 月变化）
- gaps_observed（观察到的缺口）

### 阶段 4：可信度分级

每条采集到的信息打标 🟢 / 🟡 / 🟠 / 🔴：
- 🟢 🟡 直接引用
- 🟠 加"据报道"限定
- 🔴 剔除不用

## Harness 卡点

### Gate 1：竞品清单确认

```
【竞品发现完成】共识别 {n} 家：
  直接竞品：{a} 家（{列表}）
  间接竞品：{b} 家（{列表}）
  替代方案：{c} 家（{列表}）
  自建方案：{d} 家（{列表}）

请审阅：
(1) 通过 → 进入情报采集
(2) 补充遗漏 → 我加几家
(3) 剔除不合适 → 我去掉几家
```

### Gate 2：采集完成确认

```
【情报采集完成】
  高可信信息：{p} 条
  中可信信息：{q} 条
  待验证信息：{r} 条

关键覆盖度：
  {竞品 A}：定位✅ 定价✅ 能力✅ 生态🟡 口碑✅
  {竞品 B}：定位✅ 定价✅ 能力✅ 生态❌ 口碑🟡
  ...

请选择：
(1) 通过 → 保存 JSON，可进入下一阶段 /pm-competitive-benchmark
(2) 补采某家 → 我补齐后继续
(3) 中止
```

## 输出目录

```
./output/competitive/{topic-slug}-{yyyymmdd}/
├── 01-competitor-list.md         ← 【本命令产出】竞品清单（含四类分类）
├── 01-competitors.json           ← 【本命令产出】结构化情报卡集
├── 01-competitor-{name}.json     ← 单个竞品情报（每家一份）
├── 01-intel-sources.md           ← 【本命令产出】采集信源清单（可追溯）
└── 01-intel-log.md               ← 【本命令产出】采集日志（哪些成功 / 哪些失败）
```

## 输出格式（竞品清单主文档）

```markdown
# 竞品清单：{{topic}}

> 生成时间：{{yyyy-mm-dd hh:mm}}
> 我方定位：{{positioning}}
> 采集深度：{{depth}}

## 直接竞品（{n} 家）
| # | 名称 | URL | 定位 | 发现来源 |
|---|---|---|---|---|
| D1 | Jasper | https://jasper.ai | AI Content Platform for Enterprise | Google + G2 |
| D2 | Copy.ai | https://copy.ai | AI-powered copywriting | Google + Product Hunt |
| ... | ... | ... | ... | ... |

## 间接竞品（{n} 家）
| # | 名称 | URL | 部分重叠场景 | 发现来源 |
|---|---|---|---|---|
| I1 | ChatGPT | https://chat.openai.com | 通用助手，但用户用于写作 | 用户提及 |
| I2 | Notion AI | https://notion.so | 工作流嵌入写作 | 用户提及 |

## 替代方案（{n} 家）
| # | 方案 | 说明 | 用户为什么选它 |
|---|---|---|---|
| A1 | 雇佣写手 | 传统方案 | 品牌一致性 |
| A2 | 用模板 + 人工 | 半自动 | 成本低 |

## 自建方案（{n} 家）
| # | 方案 | 组件 | 门槛 |
|---|---|---|---|
| S1 | OpenAI API + Prompt 库 | GPT-4 + LangChain | 需技术团队 |

## 关键观察
- 直接竞品价格集中在 $30-100/月
- Jasper 和 Copy.ai 是绝对头部
- ChatGPT 是最强间接威胁（价格 + 通用性）
- 私有部署选项：无一家提供 ← 我方潜在切入点

## 推荐下一步
`/pm-competitive-benchmark ./01-competitors.json` — 进入多维对标 + 差异化定位 + 应对策略
```

## 输出格式（单竞品情报卡）

见 `skills/pm/pm-competitive-intel/SKILL.md` § 三 抓取规则的 JSON Schema。

## 与其他命令的边界

| 场景 | 用 |
|---|---|
| **产品定位 → 竞品情报卡** | 本命令 |
| 多维对标 + 战略 | 下一步 `/pm-competitive-benchmark` |
| 一键跑完整竞品分析 | `/pm-competitive`（编排器） |
| 立项前需要竞品输入 | 本命令产出 → 供 `/pm-clarify` 引用 |
| PRD 需要竞品对比章节 | 本命令产出 → 供 `/prd` 引用 |
| SA 场景（客户方案竞争） | `/sa-solution-map`（已内含竞品分析章节） |

## 反模式

- ❌ 只列 3 家直接竞品 —— 违规，四类都要覆盖
- ❌ 未产出 JSON 只出 Markdown —— 违规，下游依赖 JSON
- ❌ 采集信息未标可信度 —— 违规
- ❌ 用行业分析报告代替第一手 —— 违规
- ❌ 情报卡漏关键字段（定价 / 能力 / 客户）—— 违规
