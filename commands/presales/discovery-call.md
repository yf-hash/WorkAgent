---
name: discovery-call
description: >
  售前需求挖掘工作流 — 客户拜访前准备 + 现场提问框架（SPIN）+ 资格评估（MEDDIC）+
  会议纪要（MoM）+ 24 小时内回声邮件 + Win Score 评分。覆盖首次拜访 / 需求调研 /
  二访 / kickoff 全场景。
user-invocable: true
argument-hint: "<客户公司名> [--mode prep|mom|email|score] [--type first-call|deep-dive|second|kickoff] [--industry fintech|gov|healthcare|saas]"
allowed-tools: [Read, Write, Edit, Grep, Glob, AskUserQuestion]
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
    reads: [project-context]
  security:
    danger-level: medium
---

# /discovery-call — 售前需求挖掘工作流

加载技能：`skills/presales/discovery-call/SKILL.md`

## 触发条件
- 拜访客户前要做议程设计 + 客户背调
- 拜访结束后要写会议纪要 + 回声邮件
- 多次会议后要评估机会健康度（MEDDIC / Win Score）

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `<客户公司名>` | 客户公司全称 | — |
| `--mode` | 工作阶段 | `prep` |
| `--type` | 会议类型 | `first-call` |
| `--industry` | 客户行业 | — |

### 工作模式

| `--mode` | 输出 | 适用阶段 |
|----------|------|---------|
| `prep` | 客户背调 + 议程设计 + SPIN 提问清单 + 必问 10 题 | 会议前 1-3 天 |
| `mom` | 会议纪要（MoM）模板 + Action 清单 + DMU 角色判断 | 会议结束当天 |
| `email` | 24 小时内回声邮件（核心要点 + 下一步承诺）| 会议后 24 小时 |
| `score` | MEDDIC 6 维评分 + Win Score + 投入建议 | 多次会议后机会健康度评估 |

## 使用示例

```
/discovery-call 某城商行 --mode prep --type first-call --industry fintech
/discovery-call 某省 SOC 团队 --mode mom --type deep-dive --industry gov
/discovery-call 某医疗集团 --mode email --type second --industry healthcare
/discovery-call 某 SaaS 创业公司 --mode score --industry saas
```

## 执行流程（按 mode 分支）

### `--mode prep`（会议前准备）
```
Step 1: 客户背调（公开信息）
  → 公司 / 个人 / 竞争三层背调清单
Step 2: 议程设计（60-90 分钟标准）
  → 0-5 寒暄 / 5-15 客户讲 / 15-50 我方提问 / 50-65 我方简介 / 65-80 场景深挖 / 80-90 Next Step
Step 3: SPIN 提问清单
  → S 类（情境）≤30% / I+N 类 ≥50%
Step 4: 必问 10 题（针对当前会议类型）
```

### `--mode mom`（会议纪要）
```
Step 1: 结构化记录
  → 参会人 + 业务现状 + 痛点（量化）+ 已知 / 隐藏需求
Step 2: DMU 角色判断
  → EB / UB / TB / Coach / Blocker
Step 3: Action 清单
  → 每条都要有"谁 / 做什么 / 截止"
Step 4: 风险与机会标记
  → 🟢 / 🟡 / 🔴 三色
```

### `--mode email`（回声邮件）
```
Step 1: 三个核心要点提炼
Step 2: 我方承诺 1-3 条具体行动
Step 3: 下一步会议时间确认
```

### `--mode score`（机会健康度评分）
```
Step 1: MEDDIC 6 维各打分（1-5）
  → Metrics / Economic Buyer / Decision Criteria / Decision Process / Identify Pain / Champion
Step 2: 总分 → Win Score
  → 80%+ → 售前主力投入
  → 50-80% → 标准投入
  → < 50% → 重新评估或弃单
Step 3: 风险信号识别
  → 单点接触 / Champion 失踪 / 过度技术化 / 决策时间表模糊
```

## 与其他命令的边界

| 选择 | 用前者 | 用后者 |
|------|-------|-------|
| `/discovery-call` vs `/user-research` | 售前商业语境 | 产品研发语境 |
| `/discovery-call` vs `/pm-discovery` | 单一客户深度访谈 | PM 全流程发现阶段 |
| `/discovery-call` vs `/solution-architecture` | 第 1-2 次会议（需求挖掘）| 第 3+ 次（方案落地）|
| `/discovery-call --mode mom` vs `/discovery-call --mode email` | 客户会议纪要 | 客户跟进邮件 |
