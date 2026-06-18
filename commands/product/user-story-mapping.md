---
name: user-story-mapping
description: >
  用户故事地图生成器，基于 Jeff Patton 经典方法论：Backbone（用户旅程骨架）+
  Tasks（活动任务）+ Stories（用户故事）三层结构 + Walking Skeleton（行走骨架）+
  Release Slices（发布切片）。把一句话需求拆解为可独立发布的故事切片。
  适用于：新功能拆分、MVP 范围对齐、Sprint 规划前置、需求评审。
user-invocable: true
argument-hint: "<功能/产品描述> [--mode full|backbone|skeleton|slices|stories] [--persona <角色>] [--release-count <N>]"
---

# /user-story-mapping — 用户故事地图

加载技能：`skills/user-story-mapping/SKILL.md`

## 触发条件
需要把模糊需求拆解为可发布的故事切片、定义 MVP 范围、为 Sprint 规划做准备、或开 Three Amigos 评审会时。

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `<功能/产品描述>` | 功能名或一句话产品描述（必填） | — |
| `--mode` | 输出粒度 | `full` |
| `--persona` | 主用户角色 | 自动识别 |
| `--release-count` | 切片数量（R1/R2/...） | `3` |

### 输出粒度（--mode）
| 值 | 输出 | 适用场景 |
|----|------|---------|
| `full` | 完整三层 + 切片 + 故事卡（**默认**） | 新功能完整规划 |
| `backbone` | 仅 Backbone 用户旅程骨架 | 早期方向对齐 |
| `skeleton` | Walking Skeleton 端到端最小切片 | MVP 范围定义 |
| `slices` | R1/R2/R3 发布切片清单 | 路线图准备 |
| `stories` | 详细用户故事 + 验收标准 | 进入 Sprint 前精修 |

---

## 执行流程

```
Step 1: 上下文澄清（≤2 个澄清问题）
  → 主用户角色（如未指定）
  → 当前功能阶段（0→1 / 优化扩展）
  → 关键约束（时间/资源/技术）

Step 2: Backbone 骨架（用户旅程）
  → 沿时间轴列出 ≤ 7-9 个核心活动
  → 用动词短语（不是名词）
  → 跨系统/角色边界标注

Step 3: Tasks 任务展开
  → 每个 Backbone 活动下展开 3-5 个用户任务
  → 用户视角的动作，颗粒度大致相当

Step 4: Stories 故事拆分
  → 每个 Task 下拆分独立可交付故事
  → 标注 P0/P1/P2 优先级
  → 关键故事写完整 Given/When/Then

Step 5: Walking Skeleton + Release Slices
  → R1：Walking Skeleton，端到端跑通
  → R2：扩大覆盖、关键路径补强
  → R3：体验优化、边缘场景、个性化

Step 6: 风险与异常路径
  → 每个 Task 至少标注 1 个异常路径
  → Three Amigos 待对齐项标记
```

---

## 输出示例（full 模式）

```markdown
# [功能名] 用户故事地图

## 主角色
- [Persona 1] - [一句话描述]

## 一、Backbone（用户旅程骨架）

[活动1] → [活动2] → [活动3] → [活动4] → [活动5]

## 二、Story Map（地图视图）

|        | 活动1     | 活动2     | 活动3     | 活动4     | 活动5     |
|--------|----------|----------|----------|----------|----------|
| Tasks  | T1.1     | T2.1     | T3.1     | T4.1     | T5.1     |
|        | T1.2     | T2.2     | T3.2     | T4.2     | T5.2     |
|========|==========|==========|==========|==========|==========|
| R1 MVP | s1.1 🔴  | s2.1 🔴  | s3.1 🔴  | s4.1 🔴  | s5.1 🔴  |
|--------|----------|----------|----------|----------|----------|
| R2     | s1.2 🟡  | s2.2 🟡  | s3.2 🟡  | -        | s5.2 🟡  |
|--------|----------|----------|----------|----------|----------|
| R3     | -        | s2.3 ⚪  | -        | s4.2 ⚪  | -        |

## 三、Walking Skeleton（R1 MVP）

R1 包含的故事：[故事列表 + 简述]

## 四、关键故事卡

### Story s2.1：[故事名]
**作为** [角色]
**我想** [动作]
**以便** [价值]

**验收标准**：
- Given [前置条件]
  When [操作]
  Then [结果]
  And [附加验证]

**优先级**：P0 | **估算**：[Story Points] | **依赖**：[依赖故事]

## 五、待对齐问题（Three Amigos 议程）
1. [...]
2. [...]
```

---

## 与其他命令的协同

```
/user-story-mapping（本命令）
  ├── /user-research → 提供 Persona 和 JTBD
  ├── /product-strategy → 提供 Vision 决定地图聚焦
  ├── /mvp-canvas → R1 切片即 MVP 范围
  ├── /prd-standard / /prd-spec-first → 故事卡 → 详细 PRD
  └── /roadmap → 切片 → 路线图里程碑

推荐工作流：
  新功能立项：
    /user-research --mode persona
    → /user-story-mapping --mode full
    → /prd-spec-first --stage spec
```

---

## 使用示例

```bash
# 完整故事地图（默认）
/user-story-mapping 电商商品搜索改版

# 仅生成骨架（快速对齐）
/user-story-mapping AI 写作助手新用户引导 --mode backbone

# Walking Skeleton（MVP 范围）
/user-story-mapping SaaS 数据导出功能 --mode skeleton

# 指定主角色 + 多版本切片
/user-story-mapping 团队协作看板 --persona "项目经理" --release-count 4

# 详细故事卡（Sprint 前精修）
/user-story-mapping 用户认证流程 --mode stories
```
