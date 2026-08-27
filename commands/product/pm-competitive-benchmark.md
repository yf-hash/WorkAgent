---
name: pm-competitive-benchmark
description: 【竞品分析 - 阶段 2】多维对标 + 差异化定位 + 应对策略。输入 pm-competitive-scan 产出的情报卡 JSON，输出功能矩阵 + 定价矩阵 + 生态对比 + 口碑雷达 + Blue Ocean 差异化布局 + Positioning 定位矩阵 + 应对四象限 + 销售话术库 + 竞品 FAQ。
user-invocable: true
argument-hint: "<01-competitors.json 路径 or 竞品清单描述> [--our-name <我方名>] [--focus feature|pricing|ecosystem|voc|all] [--out <path>]"
allowed-tools: [Read, Write, Edit, AskUserQuestion, Grep, Glob]
harness:
  execute:
    preset: writing-scoped
  constrain:
    profile: writing-safe
    gates: [before-write, after-benchmark, after-strategy]
  loop:
    mode: pipeline
    stages: [多维对标, 洞察产出, 差异化定位, 应对策略, 话术库]
  memory:
    scope: project
    reads: [project-context, competitive-history]
    writes: [competitive-benchmark-history]
  security:
    danger-level: low
---

# /pm-competitive-benchmark — 多维对标 + 差异化定位 + 应对策略（阶段 2）

> **PM Harness 横向能力 - 竞品分析工程化能力（阶段 2/2）**
>
> /pm-competitive-scan（阶段 1）→【本命令】→ 完整竞品分析报告

## 一句话

**输入情报卡集，输出可用的竞品分析报告** —— 功能矩阵 / 定价矩阵 / 生态对比 / 口碑雷达 + Blue Ocean 差异化 + Positioning 定位 + 应对四象限 + 销售话术。

## 输入

```bash
# 最常见：接阶段 1 输出
/pm-competitive-benchmark ./output/competitive/ai-writer-{date}/01-competitors.json

# 指定我方产品名（避免混淆）
/pm-competitive-benchmark ./01-competitors.json --our-name "我方 AI 写作助手"

# 只做某个维度（快速刷新）
/pm-competitive-benchmark ./01-competitors.json --focus pricing
/pm-competitive-benchmark ./01-competitors.json --focus feature

# 全维度（默认）
/pm-competitive-benchmark ./01-competitors.json --focus all
```

## 内部五阶段

### 阶段 1：多维对标（Benchmark）

调用 `skills/pm/pm-competitive-benchmark`：
- 功能矩阵（含覆盖度评级 ✅✅ / ✅ / 🟡 / ❌）
- 定价矩阵（含单位经济对比）
- 生态矩阵（集成 / API / 社区 / 合作伙伴）
- 口碑雷达（六维打分）
- 技术架构对标

### 阶段 2：洞察产出（Insight）

对标结果 → 5 类洞察：
1. 我方绝对优势
2. 我方绝对劣势
3. 客户价值链上的差距
4. 定价错位
5. 未满足的市场需求

### 阶段 3：差异化定位（Positioning）

调用 `skills/pm/pm-competitive-strategy`：
- Blue Ocean 四象限（消除 / 减少 / 提升 / 创造）
- Positioning 二维定位矩阵

### 阶段 4：应对策略（Strategy）

对每家竞品，按应对四象限分类：
- 🟢 领先（Leader）
- 🔴 侧翼（Flank）
- 🟡 跟随（Follow）
- 🟣 合作（Ally）
- ⚫ 避战（Avoid）

### 阶段 5：话术库（Sales Enablement）

竞品 FAQ + 通用应对话术，供售前 / 销售直接用。

## Harness 卡点

### Gate 1：对标完成
```
【多维对标完成】
  功能矩阵：{f} 个功能 × {n} 家厂商
  定价矩阵：套餐结构 + 单位经济
  生态矩阵：{g} 维
  口碑雷达：六维打分

关键发现：
  - 我方绝对优势：{列表}
  - 我方绝对劣势：{列表}
  - 定价错位机会：{描述}

是否继续差异化定位？(y / n / edit)
```

### Gate 2：战略产出
```
【战略产出完成】
  Blue Ocean 布局：消除 {a} 项，减少 {b} 项，提升 {c} 项，创造 {d} 项
  Positioning：{位置描述}
  竞品应对：领先 {p}，侧翼 {q}，跟随 {r}，避战 {s}，合作 {t}

是否生成话术库？(y / n / edit)
```

## 输出目录

```
./output/competitive/{topic-slug}-{yyyymmdd}/
├── 02-benchmark-matrix.md        ← 【本命令产出】多维对标矩阵
├── 02-insights.md                 ← 【本命令产出】5 类洞察
├── 02-positioning.md              ← 【本命令产出】差异化定位 + 布局
├── 02-strategy.md                 ← 【本命令产出】应对四象限
├── 02-sales-playbook.md          ← 【本命令产出】话术库 + FAQ
└── 02-report-full.md              ← 【本命令产出】总报告（合并版）
```

## 输出格式（总报告主结构）

```markdown
# 竞品分析总报告：{{topic}}

> 上游：01-competitors.json
> 生成时间：{{yyyy-mm-dd hh:mm}}
> 覆盖竞品：{n} 家（直接 {a} / 间接 {b} / 替代 {c} / 自建 {d}）
> 版本：v1.0

## 摘要（1 页）

### 我方定位
{{one-liner}}

### 竞争格局
- 直接竞品头部：Jasper（品牌 + 企业）+ Copy.ai（中端 + 简单）
- 最强间接威胁：ChatGPT（通用 + 价格）
- 我方切入空档：私有化 + 中文 + 性价比

### Top 3 差异化
1. **私有部署**（Jasper / Copy.ai 均无）
2. **中文原生**（Jasper 中文弱）
3. **性价比**（约为 Jasper 一半价格）

### Top 3 需补齐
1. Chrome 插件（Q1 补齐）
2. Brand Voice 训练（Q2 路线图）
3. 客户案例数量（长期）

### 建议应对
| 竞品 | 应对 | 关键动作 |
|---|---|---|
| Jasper | 侧翼 | 私有化 + 中文 + 企业市场 |
| Copy.ai | 跟随 | 快速补 Chrome 插件 |
| ChatGPT | 避战 | 强调"专业垂直"定位 |
| Notion AI | 合作 | 探索集成 |

## 1. 多维对标矩阵

### 1.1 功能矩阵
（引用 02-benchmark-matrix.md）

### 1.2 定价矩阵
（同上）

### 1.3 生态矩阵
（同上）

### 1.4 口碑雷达
（同上）

### 1.5 技术架构对标
（同上）

## 2. 5 类洞察
（引用 02-insights.md）

## 3. 差异化定位
（引用 02-positioning.md）
### 3.1 Blue Ocean 四象限布局
### 3.2 Positioning 定位矩阵

## 4. 竞品应对策略
（引用 02-strategy.md）

## 5. 销售话术 & FAQ
（引用 02-sales-playbook.md）

## 6. 后续行动
- [ ] 补齐 Chrome 插件（负责人 / 期限）
- [ ] 更新销售 FAQ（负责人 / 期限）
- [ ] 探索 Notion 集成（负责人 / 期限）
- [ ] 月度轻量刷新竞品动态（负责人）
- [ ] 季度全量刷新报告（负责人）

## 7. 版本 & 刷新
- v1.0（{yyyy-mm-dd}）：首次生成
- 下次全量刷新：{yyyy-mm-dd + 3m}
- Monitor 频率：每月轻量（`/pm-competitive --mode monitor`）
```

## 输出格式（单独章节示例：02-strategy.md）

```markdown
# 竞品应对策略

## 应对四象限总览

|                 | 值得投入 | 不值得投入 |
|---|---|---|
| **能超越** | 🟢 领先：{列表} | ⚪ 观望：{列表} |
| **不能超越** | 🔴 侧翼：{列表} | ⚫ 避战：{列表} |

**特殊**：
- 🟡 跟随（快速追上）：{列表}
- 🟣 合作（生态共赢）：{列表}

## 分家应对

### Jasper — 侧翼（Flank）
**判定**：品牌 + 客户数难超越，但市场有切入空档

**核心策略**：
1. **私有化 + 中文 + 企业市场** —— 避开 Jasper 的英语通用市场
2. **性价比策略** —— 定价约为 Jasper 的一半
3. **客户案例聚焦金融 / 政企**（Jasper 弱势领域）

**关键动作 & 里程碑**：
- Q1：完成 3 个金融 / 政企标杆案例
- Q2：私有部署产品能力打磨
- Q3：GTM 聚焦亚太 + 中文市场

**不做的事**：
- 不在英语通用市场硬碰
- 不追品牌曝光度

### Copy.ai — 跟随（Follow）
**判定**：能力接近，需要功能上快速追平

**核心策略**：
1. 补齐 Chrome 插件（Q1）
2. 提升生成质量稳定性
3. 定价保持略低（性价比锚点）

**关键动作**：
- Q1：Chrome 插件上线
- 持续：生成质量 A/B 迭代

### ChatGPT — 避战（Avoid on generic, differentiate deep）
**判定**：无法在通用性 / 价格 / 品牌 上超越

**核心策略**：
1. 明确定位差异 —— "垂直深度" vs "通用"
2. 兼容 ChatGPT API（客户可两个都用）
3. 强调稳定性 / 团队协作 / 私有化

**关键动作**：
- 销售培训：ChatGPT 对比 FAQ
- 产品：兼容 OpenAI API 输入

### Notion AI — 合作（Ally）
**判定**：用户群不同，可集成

**核心策略**：
1. 探索 Notion 官方集成
2. 定位互补 —— "生成 + 组织"

**关键动作**：
- Q2：调研 Notion 集成 API
- Q3：POC 集成

## 策略更新触发
- 竞品发布重要新功能 → 3 个工作日内评审策略
- 竞品大幅调价 → 立即评审
- 客户投诉某个对比场景 > 3 次 → 更新话术
```

## 与其他命令的边界

| 场景 | 用 |
|---|---|
| **情报卡 → 完整竞品分析报告** | 本命令 |
| 竞品发现 + 情报采集 | 前一步 `/pm-competitive-scan` |
| 一键跑完整竞品分析 | `/pm-competitive`（编排器） |
| 常态跟踪（月度） | `/pm-competitive --mode monitor` |
| 立项时引用 | 输出交给 `/pm-clarify` 参考 |
| PRD 补 § 竞品对比 | 输出交给 `/prd --mode full` 引用 |
| SA 场景（客户方案竞争） | 用 `/sa-solution-map`（含竞品章节）而非本命令 |

## 反模式

- ❌ 功能矩阵没有覆盖度评级 —— 违规
- ❌ 洞察不给"对客户价值" —— 违规
- ❌ 应对策略未按 4 象限分类 —— 违规
- ❌ 话术攻击竞品 —— 专业性差
- ❌ 战略与洞察脱节 —— 违规，战略必须基于对标
- ❌ Positioning 不出定位矩阵图 —— 违规
