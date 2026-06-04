---
name: retrospective
description: >
  产品复盘助手。覆盖 Sprint Retro / Project PIR / Launch PIR / Failure PIR 四种类型，
  支持 4L (Liked/Learned/Lacked/Longed for) / Start-Stop-Continue / 5 Whys /
  Fishbone / Sailboat / Mad-Sad-Glad 多种框架，含失败案例归档、
  Action Items 可追踪化、Blameless Post-Mortem 流程。
  
  与相邻命令的边界（防混淆）：
  - vs /decision-log：本命令是"事后学习沉淀（4L / 5Whys）"；
    /decision-log 是"事中决策记录（Y-Statement + 时间盒）"。
  - vs /experiment-log：本命令是团队/项目复盘；
    /experiment-log 是单个 A/B 实验的归档。
  - vs /launch-checklist：本命令是 D+7 复盘；/launch-checklist 是 D-Day 上线清单。
  适用于：Sprint 末复盘、项目结束、上线后 D+7、失败/事故根因分析。
user-invocable: true
argument-hint: "<复盘对象/事件名> [--type sprint|project|launch|failure|incident] [--framework 4l|ssc|5whys|fishbone|sailboat|msg] [--mode plan|template|analyze|action]"
---

# /retrospective — 产品复盘

加载技能：`skills/retrospective/SKILL.md`

## 触发条件
Sprint 结束、项目交付、产品上线 D+7、出现失败/事故，或需要做 Blameless Post-Mortem 时。

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `<复盘对象/事件名>` | 复盘标题（必填） | — |
| `--type` | 复盘类型 | `sprint` |
| `--framework` | 复盘框架 | `4l` |
| `--mode` | 输出模式 | `template` |

### 复盘类型（--type）
| 值 | 适合 | 时长 |
|----|------|------|
| `sprint` | Sprint 末复盘（**默认**） | 60-90 分钟 |
| `project` | 项目交付后整体复盘 | 2-3 小时 |
| `launch` | 上线 D+7 后 Launch Retro | 90 分钟 |
| `failure` | 失败案例 / 取消项目复盘 | 2 小时 |
| `incident` | 线上事故 Post-Mortem | 1 小时 |

### 复盘框架（--framework）
| 值 | 全称 | 适合 |
|----|------|------|
| `4l` | Liked / Learned / Lacked / Longed For | 通用（**默认**）|
| `ssc` | Start / Stop / Continue | 行动导向 |
| `5whys` | 5 个为什么 | 根因分析 |
| `fishbone` | 鱼骨图 | 多维度根因 |
| `sailboat` | 风/锚/暗礁/海岛 | 视觉化 + 团队建设 |
| `msg` | Mad / Sad / Glad | 情感导向 |

### 输出模式（--mode）
| 值 | 输出 |
|----|------|
| `plan` | 复盘会议议程 + 时间盒 + 角色分工 |
| `template` | 复盘记录模板（**默认**） |
| `analyze` | 已收集材料的整理与提炼 |
| `action` | 仅 Action Items 跟踪表 |

---

## 执行流程（template 模式）

```
Step 1: 复盘范围明确
  → 时间窗（Sprint X / Project Y / 上线 Y）
  → 参与者
  → 数据基础（指标、Bug、反馈）

Step 2: 框架选择
  → 通用 / Sprint → 4L 或 SSC
  → 失败 / 事故 → 5 Whys 或 Fishbone
  → 建团 / 团队氛围低 → Sailboat 或 MSG

Step 3: 数据收集
  → Sprint 数据：完成/计划比、Bug 数、Velocity 偏差
  → Launch 数据：D-Day 指标、用户反馈、舆情
  → Incident 数据：时间线、影响、根因初判

Step 4: 团队输入收集
  → 静默写卡（每人 5 分钟）
  → 亲和图分类
  → Dot Voting 投票排序

Step 5: 根因分析
  → 高频问题 5 Whys
  → 行为/流程/工具/文化分类

Step 6: Action Items 提取
  → 必须 SMART（Specific/Measurable/Assignable/Realistic/Time-bound）
  → Owner + 截止时间
  → 跟踪机制（下次复盘检查）
```

---

## 输出示例（4L Sprint Retro）

```markdown
# Sprint [N] Retrospective

**日期**：YYYY-MM-DD
**参与者**：[姓名 1, 姓名 2, ...]
**主持人**：[Scrum Master]

## Sprint 概况
- Sprint Goal：[Goal]
- 计划 SP：15 / 完成 SP：13（87%）
- Velocity 偏差：上 Sprint 14 / 本 Sprint 13
- Bug：P0 0 / P1 1 / P2 3
- 主要里程碑：[...]

## 4L 收集

### 👍 Liked（喜欢的）
- 跨职能配合更紧（设计 + 工程同步开会）
- Daily Standup 改成 15 分钟有效率
- 文档化 PRD 质量大幅提升

### 💡 Learned（学到的）
- 故事拆分粒度：13 SP 还是太大，应拆 3-5 SP
- 三方 API 不可控：未来要加超时和降级
- Onboarding 改版用户反馈：5 步比 7 步更受欢迎

### 🚧 Lacked（缺失的）
- QA 资源紧张：1 个 QA 撑 8 个开发
- 设计稿在 Sprint 中段才到（应 D-3 就位）
- 没有跨团队对齐时间

### 🌟 Longed For（期待的）
- 引入 Feature Flag 平台
- 增加 1 个 QA 自动化工程师
- 设计先行 1 个 Sprint

## 根因深挖（5 Whys 应用于 Top 1）

**问题**：故事拆分粒度过大

Why 1：为什么 13 SP 故事还是被纳入？
→ 因为评估时低估了第三方 API 集成

Why 2：为什么低估了 API 集成？
→ 因为没有跑过 PoC

Why 3：为什么没跑 PoC？
→ 因为时间紧，跳过了 Spike

Why 4：为什么时间紧？
→ 因为 Refinement 推迟了

Why 5：为什么 Refinement 推迟？
→ 因为 PO 上 Sprint 也忙赶进度

**根因**：Refinement 时间没保护好

## Action Items
| # | 行动 | Owner | 截止 | 验证 |
|---|------|-------|------|------|
| A1 | 故事 > 8 SP 强制 Spike | EM | 下 Sprint 起 | Backlog 检查 |
| A2 | Refinement 周二 14:00 锁死 | PO | 下周起 | 日历 |
| A3 | 设计稿 D-3 必须 100% | Designer | 下 Sprint | Sprint Plan 检查 |
| A4 | QA 自动化招聘启动 | EM | 本月 | HR 流程 |

## 上次 Action 跟踪
| # | 上次行动 | 状态 | 备注 |
|---|---------|------|------|
| A1 | Daily 15 分钟 | ✅ 完成 | 沿用 |
| A2 | 引入 PR 模板 | ✅ 完成 | 已生效 |

## 评分（团队对本 Sprint）
- 满意度：4 / 5
- 流程顺畅度：3 / 5（拆分问题）
- 团队氛围：5 / 5
```

---

## 输出示例（incident Post-Mortem）

```markdown
# Incident Post-Mortem：[事件名]

**事件 ID**：INC-2026-005
**严重等级**：P1（用户可感知）
**影响时长**：23 分钟
**影响范围**：30% 海外用户无法登录

## 时间线（UTC）
| 时间 | 事件 |
|------|------|
| 14:02 | 部署 v2.3.1 |
| 14:05 | 监控告警：5xx 错误率 1.5% |
| 14:08 | On-Call 工程师介入 |
| 14:12 | 初判：登录服务异常 |
| 14:18 | 决策：回滚 v2.3.1 |
| 14:22 | 回滚完成 |
| 14:25 | 服务恢复 |

## 影响
- 用户：~2 万受影响
- 业务：登录失败 1.2 万次
- 收入：估算 < $500（订阅产品）

## 根因（Blameless）
直接原因：v2.3.1 配置文件 region 字段大小写不一致
根本原因：
  1. 配置变更没有被集成测试覆盖
  2. 灰度策略未生效（直接全量）
  3. 海外区域监控延迟 3 分钟

## 改进项
| # | 行动 | Owner | 截止 | 类型 |
|---|------|-------|------|------|
| 1 | 配置变更纳入 CI 测试 | EM | 2 周 | 防止复发 |
| 2 | 强制灰度（1% → 10% → 50% → 100%） | EM | 1 周 | 流程 |
| 3 | 海外监控延迟 < 30s | SRE | 4 周 | 检测加速 |
| 4 | Runbook 更新 | EM | 1 周 | 响应加速 |

## 学习（Blameless）
- "对错检测"机制比"惩罚"更重要
- 跨区域配置必须有差异化测试
- 灰度策略是底线，不可绕过
```

---

## 与其他命令的协同

```
/retrospective（本命令）
  ├── /sprint-planning → Sprint 末必跑
  ├── /launch-checklist → D+7 必跑（type=launch）
  ├── /ab-test → 实验失败/成功复盘
  ├── /growth-experiment → 实验日志归档
  ├── /pmf-survey → PMF 不达预期复盘
  └── /feedback → 用户反馈作为输入

推荐工作流：
  双周 Sprint：
    Sprint 末 → /retrospective --type sprint --framework 4l
  
  上线后：
    D+7 → /retrospective --type launch
  
  事故响应：
    Incident 后 24h → /retrospective --type incident --framework 5whys
```

---

## 使用示例

```bash
# Sprint 末复盘（默认 4L 框架）
/retrospective Sprint 12

# Start-Stop-Continue 框架
/retrospective Sprint 12 --framework ssc

# 上线后 D+7 复盘
/retrospective AI 助手 v2 上线 --type launch

# 事故 Post-Mortem
/retrospective 海外登录服务 23 分钟故障 --type incident --framework 5whys

# 项目失败复盘
/retrospective 出海试点项目 --type failure --framework fishbone

# 季度项目交付复盘
/retrospective Q1 数据分析平台项目 --type project

# 仅生成 Action Items 跟踪表
/retrospective Q1 团队复盘 --mode action
```
