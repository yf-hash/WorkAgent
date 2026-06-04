---
name: retrospective
description: >
  产品复盘方法论知识库。覆盖 Sprint Retro / Project PIR / Launch PIR /
  Failure PIR / Incident Post-Mortem 五种复盘类型；4L、Start-Stop-Continue、
  5 Whys、Fishbone、Sailboat、Mad-Sad-Glad 六种框架；Blameless Post-Mortem
  原则；Action Items 可跟踪化；失败案例归档结构。
  触发词：复盘、retrospective、PIR、Post-Mortem、根因分析、4L、SSC、
  5 Whys、鱼骨图、Sailboat、Mad-Sad-Glad、Sprint Retro、事故复盘、Blameless
user-invocable: false
effort: high
---

# Retrospective — 产品复盘知识库

把"开个会聊聊感受"变成可沉淀、可追踪、可改进的复盘流程。

---

# 一、复盘的"四层价值"

```
Level 1：发泄         → 团队情绪释放
Level 2：诊断         → 找出问题
Level 3：归因         → 找到根因（不是责任人）
Level 4：改进         → 落实可跟踪的 Action

低价值复盘止步于 1-2 层
高价值复盘必须到 4
```

---

# 二、复盘类型选择

| 类型 | 时机 | 时长 | 重点 |
|------|------|------|------|
| Sprint Retro | Sprint 末（双周） | 60-90 分 | 流程改进、团队协作 |
| Project PIR | 项目结束 | 2-3 小时 | 整体得失、知识沉淀 |
| Launch PIR | 上线 D+7 | 90 分钟 | 发布质量、用户反馈 |
| Failure PIR | 失败/取消项目 | 2 小时 | 战略反思、避免下次 |
| Incident Post-Mortem | 事故 24h 内 | 1 小时 | 时间线、根因、防止复发 |

---

# 三、复盘框架库

## 3.1 4L 框架（最通用）

```
👍 Liked       什么让我们高兴？什么做得好？
💡 Learned     学到了什么？哪些知识沉淀下来？
🚧 Lacked      缺什么？哪些资源/能力不够？
🌟 Longed For  期待什么？下次想要什么变化？
```

适合：通用 Sprint Retro，团队氛围中性。

## 3.2 Start-Stop-Continue（行动导向）

```
🟢 Start    我们应该开始做什么？
🔴 Stop     我们应该停止做什么？
🟡 Continue 我们应该继续做什么？
```

适合：行动落地，团队已熟悉问题。

## 3.3 5 Whys（根因深挖）

```
问题：[现象]
Why 1: 为什么 [现象]？  → [原因 1]
Why 2: 为什么 [原因 1]？ → [原因 2]
Why 3: 为什么 [原因 2]？ → [原因 3]
Why 4: 为什么 [原因 3]？ → [原因 4]
Why 5: 为什么 [原因 4]？ → [根因]

根因 → 改进措施 (针对根因，而非现象)
```

适合：单点深度问题，事故复盘。

## 3.4 Fishbone（鱼骨图，多维根因）

```
                ┌─ 流程 ──────────────┐
                │                    │
   人 ──────────┤                    │
                │                    │── [问题]
   工具 ────────┤                    │
                │                    │
                └─ 文化/环境 ─────────┘
```

每个分支下列出可能原因 → 分析最致命因素。

适合：复杂问题、多团队协作。

## 3.5 Sailboat（船的隐喻）

```
                    🌬️ 风（推动我们的因素）
                         │
                         ▼
   ⚓ 锚（拖累我们的因素）  ────🛥️─────► 🏝️ 海岛（团队目标）
                              ▲
                              │
                    🪨 暗礁（潜在风险）
```

适合：团队建设、视觉化、入门复盘。

## 3.6 Mad-Sad-Glad（情感导向）

```
😡 Mad   什么让我们生气？
😢 Sad   什么让我们失落？
😀 Glad  什么让我们开心？
```

适合：氛围低迷、需要先释放情绪。

---

# 四、Blameless Post-Mortem 五原则

事故复盘的金科玉律：

```
1. 假定善意（Good Intent）
   → 没人故意搞砸，所有行为在当时上下文都是合理的

2. 关注系统而非个人
   → 不问"谁犯了错"，问"系统为什么允许这个错"

3. 时间线优先于结论
   → 先把客观时间线整理清楚，再讨论判断

4. 区分直接原因和根本原因
   → 直接原因：触发问题的最近事件
   → 根本原因：系统层面的脆弱性

5. 改进项针对系统
   → 不是"以后小心点"，而是"加 CI 检查"
```

反模式：
- ❌ "都怪 [人名] 没测试"
- ✅ "我们没有强制 CI 测试覆盖配置变更"

---

# 五、SMART Action Items

每个改进项必须满足：

```
S - Specific：具体动作（不是"提升流程"）
M - Measurable：可衡量（不是"加强"）
A - Assignable：有负责人
R - Realistic：在能力范围内
T - Time-bound：有截止时间
```

| ❌ | ✅ |
|----|----|
| 提升 PR 质量 | 每个 PR 必须 2 人 Review，30 天内合并率 ≥ 90% |
| 减少 Bug | 引入静态分析，4 周内主仓集成 |
| 改进沟通 | 跨团队对齐周二 14:00 站会，从下周起 |

---

# 六、复盘会议时间盒

## 60 分钟（Sprint Retro）

```
00:00 ─ 05:00  设定基调（Prime Directive）
05:00 ─ 15:00  数据回顾（Sprint Goal、Velocity、Bug）
15:00 ─ 35:00  收集卡片（4L / SSC，静默写）
35:00 ─ 50:00  讨论 + Dot Voting
50:00 ─ 58:00  Action Items 提炼
58:00 ─ 60:00  评分 + 关闭
```

## 90 分钟（Launch PIR）

```
00:00 ─ 05:00  Goal 与基调
05:00 ─ 25:00  数据回顾（D-Day 指标 + 用户反馈）
25:00 ─ 40:00  时间线复述（按 D-Day 顺序）
40:00 ─ 65:00  4L 或 5 Whys 深挖
65:00 ─ 80:00  Action Items
80:00 ─ 90:00  下一阶段计划
```

## 120 分钟（Project PIR / Failure PIR）

```
00:00 ─ 10:00  Goal、范围、参与者
10:00 ─ 40:00  全周期复盘（按阶段）
40:00 ─ 80:00  根因分析（Fishbone / 5 Whys）
80:00 ─ 105:00  Action Items + Owner
105:00 ─ 120:00 知识沉淀（写入团队 Wiki）
```

---

# 七、Prime Directive（开场宣誓）

经典版：

> "我们坚信，每个人在他当时所掌握的信息、能力、资源以及当时的情境下，
> 都做了他能做的最好的事。无论我们将要发现什么。"

—— Norm Kerth

每次开场念一遍，确保 Blameless 氛围。

---

# 八、复盘记录归档

```
docs/retros/
├── sprint-12.md           # Sprint Retro
├── launch-ai-v2.md        # Launch PIR
├── failure-overseas.md    # Failure PIR
└── incident-2026-005.md   # Post-Mortem
```

每份必含：
- 时间 / 参与者 / 主持人
- 数据 / 时间线
- 收集的输入
- 根因分析
- Action Items（含 Owner 和截止）
- 上次 Action 跟踪表

---

# 九、Action Items 跟踪机制

```
建议建立 docs/retros/action-tracker.md：

| # | 来源 | 行动 | Owner | 截止 | 状态 | 验证 |
|---|------|------|-------|------|------|------|
| A23 | Sprint 11 | PR 模板上线 | EM | 2026-01-31 | ✅ 完成 | 仓库已有 |
| A24 | Sprint 12 | Refinement 周二锁定 | PO | 下周 | 🟡 进行 | 日历检查 |
```

每次新复盘前，先回顾上次 Action 完成情况。

---

# 十、与其他知识库的关系

| 知识库 | 协作方式 |
|--------|---------|
| `sprint-planning` | Sprint 末必跑 Retro |
| `launch-checklist` | D+7 跑 Launch PIR |
| `ab-test` | 实验日志的复盘归档 |
| `growth-experiment` | 失败实验的学习沉淀 |
| `feedback` | 用户反馈作为复盘输入 |
| `pmf-survey` | PMF 不达标的失败 PIR |
