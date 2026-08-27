# Role — 角色元代理层（Role Meta-Agent）

> 五能力（execute / constrain / loop / memory / security）之上的第六层原语，专门服务"角色总入口"这一新型交互模式。
>
> **角色不是 command，不是 skill，也不是普通 agent**——它是"用户第一层接触点"，负责把自然语言需求拆成一个由现有 command/skill 组成的执行计划。

## 什么时候需要 role？

- 用户不想记 68 个 command 名字，只想说"我要做 XXX"
- 需求跨多个能力域（比如 PRD → 上线清单 → 销售包），单个 command 覆盖不了
- 有典型工作流（比如"新功能全流程"），希望一句话触发整条链路

## Role vs 现有概念

| 概念 | 定位 | 用户如何触发 | 内部做什么 |
|---|---|---|---|
| Command | 单一动作的原子入口 | `/prd`、`/pm-clarify` | 一次调用完成一件事 |
| Skill | 可复用知识模块 | 不直接触发（被引用） | 提供领域方法论 |
| Agent | 领域专家（编排 skill） | `@pm` | 深度专业化处理 |
| **Role** | **角色总入口（编排 command）** | `/pm` 或 `@pm` | 拆解需求 → 生成计划 → 依次执行 |

## Role 的执行三阶段

```
用户输入自然语言需求
        ↓
┌──────────────────────┐
│ 1. 意图识别 + 澄清   │  读 manifest.yaml → 匹配能力域
│    （router.md）      │  必要时反问 1-3 个关键问题
└──────────────────────┘
        ↓
┌──────────────────────┐
│ 2. 任务分解 + 计划   │  匹配 workflow 或动态编排
│    （task-planner.md）│  展示 3-8 步计划让用户确认（唯一 gate）
└──────────────────────┘
        ↓
┌──────────────────────┐
│ 3. 依次自动执行       │  按计划调用具体 command / skill
│    （loop 复用 pipeline）│ 出错时才回到用户
└──────────────────────┘
        ↓
     汇总输出
```

## 目录约定

```
.claude/harness/role/          # 通用原语（本目录）
├── README.md                  # 本文件
├── router.md                  # 角色路由 SOP（意图识别 + 澄清 + 计划确认）
└── task-planner.md            # 任务分解规范（步骤粒度 / 依赖 / 幂等性）

roles/                         # 各角色的数据（业务层）
├── pm/
│   ├── manifest.yaml          # 声明式能力清单
│   └── workflows.md           # 典型剧本
├── sa/
│   ├── manifest.yaml
│   └── workflows.md
└── content/
    ├── manifest.yaml
    └── workflows.md

agents/pm.md                   # PM 角色 meta-agent（供 @pm 触发）
agents/sa.md                   # SA 角色 meta-agent（供 @sa 触发）
agents/content.md              # Content 角色 meta-agent（供 @content 触发）
```

**斜杠入口**：三个角色的 `/pm` / `/sa` / `/content` 由 `agents/*.md` 直接暴露（不再单独设 `commands/pm.md`），Claude Code 会同时接受 `@pm` 与 `/pm` 两种触发方式。

## Frontmatter 声明

角色 meta-agent 用如下 harness 配置：

```yaml
harness:
  execute:
    preset: agent-orchestrator
  constrain:
    profile: agent-orchestrator
    gates: [after-decompose]     # 唯一强制 gate：计划确认
  loop:
    mode: pipeline               # 复用 pipeline（阶段动态生成）
    stages: dynamic              # 由 manifest + LLM 分解得出
    gate-between: false          # 阶段间自动执行
  memory:
    scope: session + project
    reads: [project-context, role-manifest, workflows]
  security:
    danger-level: low            # role 本身不做危险操作，由子命令的 security 决定
```

## 与其他层的边界

- **role 不直接做工具调用**：只做计划，调用交给下游 command
- **role 不硬编码路由**：所有能力映射写在 `manifest.yaml`，改能力不改 agent 正文
- **role 不覆盖 command 的 harness**：每个 command 自己的五能力约束仍然生效
- **role 不管跨会话状态**：那是 memory 层的 project scope

## 反模式

- ❌ 在 role agent 正文里写"包含关键词 X → 加载 skill Y"——那是硬编码路由，改用 manifest.yaml
- ❌ 把 skill 直接暴露给 role 调用——role 只调 command（保留 command 的 gate/security）
- ❌ 无根据地增设新角色——当前 v3.2 已收敛为 `pm` / `sa` / `content` 三角色矩阵（内部 PRD × 对外售前 × 内容传播），新增前必须证明单个 command 或跨调现有角色无法覆盖
- ❌ 计划展示只写命令名不写目的——用户看不懂"依次调用 /prd /pm-tech-spec"，要写"① 撰写 PRD，② 生成技术规格书"
