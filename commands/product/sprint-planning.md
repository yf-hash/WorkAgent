---
name: sprint-planning
description: >
  Sprint 规划助手。支持 Scrum / Kanban / Shape Up 三种迭代模式、
  Sprint Goal 起草、Backlog 梳理（Definition of Ready）、Story Pointing
  (Planning Poker / T-Shirt / 参照法)、Capacity 规划、Definition of Done、
  Burndown 跟踪、Sprint 反模式自检。
  适用于：双周 Sprint 启动会、Backlog 梳理、估算会、迭代复盘前置。
user-invocable: true
argument-hint: "<Sprint 名/编号> [--mode plan|backlog|estimate|capacity|fullset] [--method scrum|kanban|shapeup|scrumban] [--length 1w|2w|3w|6w] [--team-size <N>]"
---

# /sprint-planning — Sprint 规划

加载技能：`skills/sprint-planning/SKILL.md`

## 触发条件
开 Sprint 启动会、Backlog 梳理、做 Story Pointing、估算 Capacity、检查 DoR/DoD，或需要迭代规划 SOP 时。

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `<Sprint 名/编号>` | Sprint 标识（必填） | — |
| `--mode` | 输出模式 | `plan` |
| `--method` | 迭代方法 | `scrum` |
| `--length` | Sprint 长度 | `2w` |
| `--team-size` | 团队人数 | — |

### 输出模式（--mode）
| 值 | 输出 | 适用场景 |
|----|------|---------|
| `plan` | Sprint 计划文档（Goal+Backlog+Capacity+DoD）| Sprint 启动会（**默认**）|
| `backlog` | Backlog 梳理清单 + DoR 检查 | Refinement 会 |
| `estimate` | Story Pointing 模板 + Planning Poker | 估算会 |
| `capacity` | 容量规划 + Velocity 估算 | 排期前 |
| `fullset` | 完整套件（4 项 + 反模式自检） | 季度初 / 团队启动 |

### 迭代方法（--method）
| 值 | 适合 |
|----|------|
| `scrum` | 双周迭代、固定 Sprint Goal（**默认**） |
| `kanban` | 流式工作、运维 / 客服 |
| `shapeup` | 6 周 + 2 周冷却（Basecamp 模式）|
| `scrumban` | Scrum 加 WIP 限制 |

---

## 执行流程（plan 模式）

```
Step 1: 上下文澄清
  → 团队人数、Sprint 周期、当前 Velocity（如有）
  → 上一个 Sprint 完成情况
  → 季度/月度大目标（用于校准 Sprint Goal）

Step 2: Sprint Goal 起草
  → 单一聚焦、用户/业务价值驱动
  → 可衡量、可背诵
  → 模板："本 Sprint 要 [动作]，以便 [收益]，通过 [信号] 验证"

Step 3: Backlog 候选筛选
  → 从已 Refinement 的故事里选符合 Goal 的
  → 检查 DoR：故事完整 + AC 清晰 + 设计已就位 + 估算已完成
  → 标注 P0（必须完成）/ P1（可选） 

Step 4: Capacity 规划
  → 人数 × 工作日 × 0.6 (有效率)
  → 扣除会议 / On-Call / 跨项目
  → 算出本 Sprint 可承诺 SP 上限

Step 5: 故事 + 任务拆分
  → 每个故事拆 1-3 个子任务
  → 团队 Pull（领取）而非 Push（分配）

Step 6: 风险 + 依赖识别
  → 阻塞项 + Owner + 解决路径
  → 跨团队依赖列表

Step 7: 公开承诺 Sprint Goal
```

---

## 输出示例（plan 模式）

```markdown
# Sprint [N] 计划：[Sprint 名]

**周期**：YYYY-MM-DD ~ YYYY-MM-DD（[N] 工作日）
**团队**：[姓名 1, 姓名 2, ...]（共 [N] 人）
**PM**：[姓名] | **Tech Lead**：[姓名] | **Scrum Master**：[姓名]

## Sprint Goal
> 本 Sprint 我们要 [动作 / 交付]
> 以便 [用户 / 业务价值]
> 通过 [可观测信号] 验证目标达成

## Capacity 估算
- 团队工作日：[N 人 × N 天] = [人天]
- 有效率系数：60%
- 可承诺 SP 上限：[N SP]
- 上 Sprint Velocity：[N SP]

## Sprint Backlog
| ID | 故事 | SP | 优先级 | Owner | DoR |
|----|------|----|--------|-------|-----|
| US-101 | 用户可以导出 PDF | 5 | P0 | [姓名] | ✅ |
| US-102 | 用户可以导出 Excel | 5 | P0 | [姓名] | ✅ |
| US-103 | 导出进度反馈 | 3 | P0 | [姓名] | ✅ |
| US-104 | 导出文件命名规则 | 2 | P1 | [姓名] | ⚠️ 待 UI |

**总计**：15 SP（P0：13 SP / P1：2 SP）

## Definition of Done
- [ ] 代码 Review 合并主干
- [ ] 单测 + 集成测试通过
- [ ] QA 签字
- [ ] PM 验收
- [ ] 文档已更新
- [ ] 监控告警已配置

## 风险与依赖
| 风险/依赖 | 影响 | 应对 | Owner |
|----------|------|------|-------|
| 依赖文件存储 API 升级 | 阻塞 US-101 | 第 1 周完成 API 联调 | [姓名] |
| 团队成员 D5-D7 休假 | -3 SP 容量 | 范围调整为 12 SP | PM |

## 关键日历
- D1：Planning（今日）
- D5：Mid-Sprint Review
- D9：Code Freeze
- D10：Sprint Review + Retro

## 公开承诺
团队对 Sprint Goal 的承诺：✅
若中段需调整范围，触发条件 + 决策流程：[...]
```

---

## 与其他命令的协同

```
/sprint-planning（本命令）
  ├── /roadmap → 季度目标拆分到 Sprint
  ├── /user-story-mapping → R1 故事进入 Backlog
  ├── /product-spec → PRD 拆分为可估算故事
  ├── /retrospective → Sprint 末复盘
  ├── /launch-checklist → Sprint 末发布
  └── /okr → Sprint Goal 对齐季度 OKR

推荐工作流：
  季度初：
    /okr --mode quarterly
    → /roadmap --horizon 3m
    → /user-story-mapping
    → /sprint-planning --mode fullset
  
  每个 Sprint：
    /sprint-planning --mode plan
    → 执行
    → /retrospective
```

---

## 使用示例

```bash
# 标准双周 Scrum 计划（默认）
/sprint-planning Sprint 12

# Backlog 梳理（DoR 检查）
/sprint-planning Sprint 12 --mode backlog

# 估算会（Planning Poker）
/sprint-planning Sprint 12 --mode estimate

# 容量规划（团队 5 人，2 周）
/sprint-planning Sprint 12 --mode capacity --team-size 5

# Shape Up 6 周 Pitch
/sprint-planning Cycle 5 --method shapeup --length 6w

# Kanban 看板初始化
/sprint-planning 客服支持工作流 --method kanban

# 完整四件套（季度初团队启动）
/sprint-planning Sprint 1 --mode fullset --team-size 6
```
