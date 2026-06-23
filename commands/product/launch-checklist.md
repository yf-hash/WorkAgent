---
name: launch-checklist
description: >
  产品发布检查清单生成器，覆盖产研测设市销 6 轨道、Soft/Hard/Gradual Launch 选型、D-30 / D-7 / D-Day / D+7 时间盒、Go/No-Go 决策模板、回滚预案、关键监控指标、危机响应 SOP。让发布从靠经验变成可复用的 SOP。
  
  与相邻命令的边界（防混淆）：
  - 本命令产出"D-Day 之前的就绪清单"。
  - 上线后的复盘由其他流程承接。
  适用于：新功能上线、版本发布、大改版前对齐、跨团队协同。
user-invocable: true
argument-hint: "<产品/功能名> [--mode full|tracks|timebox|risk|gono] [--launch-type soft|hard|gradual|beta|stealth] [--scale small|medium|large]"
---

# /launch-checklist — 发布检查清单

加载技能：`skills/launch-checklist/SKILL.md`

## 触发条件
新功能/产品/版本即将发布、需要跨团队协同对齐、需要建立可复用的发布 SOP，或需要做 Go/No-Go 决策时。

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `<产品/功能名>` | 待发布的产品/功能（必填） | — |
| `--mode` | 输出模式 | `full` |
| `--launch-type` | 发布类型 | `gradual` |
| `--scale` | 影响规模 | `medium` |

### 输出模式（--mode）
| 值 | 输出 | 适用场景 |
|----|------|---------|
| `full` | 6 轨道全清单 + 时间盒 + Go/No-Go（**默认**） | 重要发布完整准备 |
| `tracks` | 仅 6 轨道清单 | 跨团队任务分配 |
| `timebox` | 仅时间盒 SOP（D-30 ~ D+7） | 倒推日历 |
| `risk` | 风险评估矩阵 + 回滚预案 | 高影响发布的风险审议 |
| `gono` | Go/No-Go 决策会议模板 | 上线前最终对齐 |

### 发布类型（--launch-type）
| 值 | 说明 |
|----|------|
| `soft` | 限定地区/用户群上线 |
| `hard` | 全量 + PR |
| `gradual` | 1% → 10% → 50% → 100% 灰度（**默认**） |
| `beta` | 报名/邀请制 |
| `stealth` | 静默上线 |

### 影响规模（--scale）
| 值 | 时间盒 | 必要轨道数 |
|----|-------|-----------|
| `small` | D-7 ~ D+1 | 3-4（产研测） |
| `medium` | D-30 ~ D+7（**默认**） | 5-6 |
| `large` | D-60 ~ D+30 | 6 + 法务 + PR |

---

## 执行流程（full 模式）

```
Step 1: 发布信息盘点
  → 产品/功能名、版本、发布日期、Owner
  → 影响范围（用户/收入/数据/合规）
  → 关键依赖（API/三方/合作伙伴）

Step 2: 选发布类型
  → 涉及付费/合规 → Gradual 灰度
  → 重大改版需 PR → Hard
  → 早期产品 → Beta
  → 实验性 → Stealth

Step 3: 6 轨道清单生成
  → Product / Engineering / QA / Design / Marketing / Sales-CS
  → 每轨道 Owner + 截止时间
  → 阻断项（必须完成才能发布）vs 建议项

Step 4: 时间盒 SOP
  → D-30 决策日 → D-1 Briefing → D-Day 分阶段 → D+7 复盘
  → 关键里程碑 + 决策点

Step 5: 风险评估
  → 风险 × 概率 × 影响矩阵
  → 阻断/缓解/监测分级
  → 触发条件 + 回滚 SOP

Step 6: Go/No-Go 决策模板
  → 出席角色 / 审计项 / 决策结果模板
```

---

## 输出示例（full 模式片段）

```markdown
# [产品名] Launch Readiness Checklist

**发布日期**：YYYY-MM-DD | **类型**：Gradual | **规模**：Medium
**主 Owner**：[姓名] | **On-Call EM**：[姓名]

## 一、6 轨道清单

### 🛠️ Product 产品轨道（Owner：PM）
| # | 任务 | 截止 | 状态 | 阻断 |
|---|------|------|------|------|
| P1 | PRD 已批准 | D-21 | ⬜ | ⛔ |
| P2 | 验收标准全过 | D-14 | ⬜ | ⛔ |
| P3 | 边界场景覆盖 | D-14 | ⬜ | ⛔ |
| P4 | 文案最终版 | D-7 | ⬜ | ⛔ |
| P5 | 北极星 + 护栏指标定义 | D-21 | ⬜ | ⛔ |
| P6 | 决策矩阵已写入 | D-7 | ⬜ | ⚠️ |

### ⚙️ Engineering 工程轨道（Owner：EM）
| # | 任务 | 截止 | 状态 | 阻断 |
|---|------|------|------|------|
| E1 | Code Review 全过 | D-7 | ⬜ | ⛔ |
| E2 | 单测/集成/E2E 通过 | D-7 | ⬜ | ⛔ |
| E3 | 性能压测达标 | D-7 | ⬜ | ⛔ |
| E4 | DB Migration 已演练 | D-3 | ⬜ | ⛔ |
| E5 | Feature Flag 已配 | D-3 | ⬜ | ⛔ |
| E6 | 回滚 SOP 已演练 | D-1 | ⬜ | ⛔ |
| E7 | 告警 + On-Call 就绪 | D-1 | ⬜ | ⛔ |

### 🧪 QA 测试轨道
[...]

### 🎨 Design 设计轨道
[...]

### 📣 Marketing 市场轨道
[...]

### 💼 Sales / CS 销售客服轨道
[...]

## 二、时间盒 SOP

```
D-30  Go/No-Go #1（确认发布日期）
D-21  各轨道接收清单
D-14  Code Freeze（仅 P0 Bug Fix）
D-10  Pre-Launch Review
D-7   内测全过 + 灰度配置 + Marketing 素材冻结
D-3   Go/No-Go #2（看 Pre-Launch 数据）
D-1   D-Day Briefing
D-Day 1% → 10% → 50% → 100% 分阶段
D+1   稳定性日报
D+7   Launch Retrospective
D+30  商业指标复盘
```

## 三、风险评估
| # | 风险 | 概率 | 影响 | 应对 | Owner |
|---|------|------|------|------|-------|
| R1 | 数据库迁移失败 | 低 | 高 | 演练 + 回滚脚本 | EM |
| R2 | 主漏斗下降 > 20% | 中 | 高 | 灰度立即收 + 复盘 | PM |
| R3 | 客服工单激增 | 中 | 中 | 提前培训 + 话术 | CS Lead |

## 四、回滚预案
**触发**（任一）：
- 5xx 错误率 > 1%
- 主漏斗下降 > 20%
- 数据库延迟 3x baseline

**步骤（≤ 5 分钟）**：
1. On-Call 拉群通知
2. Feature Flag → off
3. 数据库回滚（如需）
4. 客服话术 + 公告
5. 1h 内根因初判，48h 内 PIR

## 五、Go/No-Go 决策模板
[...]
```

---

## 与其他命令的协同

```
/launch-checklist（本命令）
  ├── /gtm-strategy → Marketing 轨道内容
  ├── /roadmap → 发布日期来源
  ├── /ab-test → 灰度阶段实验设计
  ├── /product-release-note → 版本说明
  └── /analytics → D-Day 监控指标埋点

推荐工作流：
  重大发布：
    /launch-checklist --launch-type gradual --scale large
    → /ab-test --mode design（灰度阶段）
    → 上线
```

---

## 使用示例

```bash
# 完整发布清单（默认 medium 规模 + gradual 灰度）
/launch-checklist AI 写作助手 v2

# 小型发布（仅产研测）
/launch-checklist 推送通知功能 --scale small

# 大型 Hard Launch（含法务 + PR）
/launch-checklist 重大改版 v3 --launch-type hard --scale large

# Soft Launch（限定地区）
/launch-checklist 海外版 0.1 --launch-type soft --scale medium

# 仅生成时间盒倒推日历
/launch-checklist 春节大促活动 --mode timebox --scale large

# 仅 Go/No-Go 决策模板
/launch-checklist v2.5 上线评审 --mode gono
```
