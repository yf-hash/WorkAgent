# HARNESS_FRAMEWORK — WorkAgent 五能力分层框架

> 在大模型作为基本算力的前提下，构建"模型负责思考、harness 负责执行/约束/循环/记忆/安全"的自动化执行体系。
>
> 版本：v3.0（首版，2026-08-01）。本文件是 WorkAgent 后续所有结构性重构的锚点。

---

## 1. 为什么需要 harness 分层

当前 WorkAgent 有 24 agents / 115 skills / 86 commands，"模型思考"部分（prompt 工程、职责边界、领域知识）已经很厚重，但"harness 层"极薄：

- `commands/` 里 **71%** 的命令没有声明 `allowed-tools`（模型可任意调用任何工具）
- 无 `.claude/hooks/`、无项目 `CLAUDE.md`、无 `memory/` 目录、无 loop 模板
- Agents 已经引入了 `memory: project` / `MaxTurns` / `skills:[...]` 等 harness 字段——**说明作者已在 agent 层试水，但 command 层没跟上**

如果不把 harness 层显式化，随着场景增加会出现：
1. **执行不可控**：同一命令在不同用户环境下调用不同工具，结果不稳定
2. **约束靠自觉**：模型自己判断"该不该写文件"，一旦决策错误没有拦截
3. **循环靠人手**：迭代类任务（bid 七阶段、article writer-reviewer）每步都要人点一下
4. **记忆丢失**：用户偏好、项目上下文每次都要重新描述
5. **安全无审计**：危险动作只有终端弹窗，无日志、无策略化

## 2. 五能力分层定义

```
┌──────────────────────────────────────────────────────────────┐
│                  模型（Claude Opus / Sonnet）                 │
│               负责：理解 · 生成 · 决策 · 反思                  │
└──────────────────────────────────────────────────────────────┘
                              ▲
                              │  提示 / 结果
                              ▼
┌──────────────────────────────────────────────────────────────┐
│                        HARNESS 层                             │
│                                                              │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐    │
│  │Execute │ │Constrain│ │  Loop  │ │ Memory │ │Security│    │
│  │执行调度│ │  约束  │ │循环控制 │ │  记忆  │ │  安全  │    │
│  └────────┘ └────────┘ └────────┘ └────────┘ └────────┘    │
│                                                              │
│  提供：工具、权限、hook、cron、schedule、记忆读写、审计       │
└──────────────────────────────────────────────────────────────┘
                              ▲
                              │  调用
                              ▼
┌──────────────────────────────────────────────────────────────┐
│           业务层：commands / skills / agents                  │
│         （PRD / 标书 / 售前 / 写作 / 数据 / 媒体 / 研究）      │
└──────────────────────────────────────────────────────────────┘
```

### 2.1 Execute — 执行调度

**做什么**：把模型的意图转成对具体工具的调用；决定用哪个工具、传什么参数、并行还是串行。

**原语**：
- 工具白名单：`allowed-tools: [Read, Write, Edit, Bash, WebFetch, ...]`
- 工具预设：常见组合（read-only / write-scoped / research / media-heavy）
- 子代理编排：Agent tool、并行 / 串行、subagent_type
- Bash / Skill / MCP 路由

**资产位置**：`.claude/harness/execute/`

### 2.2 Constrain — 约束

**做什么**：在模型行动前后加检查点，防止越权、越界、越量。

**原语**：
- Permission 画像：per-scenario 的 allow/ask/deny 组合
- Gate 检查：写前 gate（模型能写什么）、发送前 gate（推送前必须确认）
- ArgumentHint / AskUserQuestion：把不明确输入拉回人工确认
- MaxTurns：agent 最大迭代次数上限

**资产位置**：`.claude/harness/constrain/`

### 2.3 Loop — 循环控制

**做什么**：把"生成→评审→修复→再评审"这类需要多轮的工作自动化。

**原语**：
- `/loop`：自定义 prompt + max-iterations + budget
- Cron / ScheduleWakeup：定时或延时唤醒
- Retry 策略：3-strike 切换、backoff
- Pipeline 阶段：bid 七阶段这种线性流水
- Monitor：常驻监控（日志、CI、外部状态）

**资产位置**：`.claude/harness/loop/`

### 2.4 Memory — 记忆

**做什么**：跨会话保留"用户是谁 / 项目在做什么 / 上次进度到哪"。

**原语**：
- 项目级 `CLAUDE.md`：所有会话必读
- Auto-memory：`memory/` 目录 + MEMORY.md 索引（现有 harness 已内置机制）
- Session Export / Recall：跨 IDE、跨会话检索
- Agent 级 `memory:` 字段：局部作用域记忆

**资产位置**：`.claude/harness/memory/`

### 2.5 Security — 安全

**做什么**：拒绝真正危险的动作、留下审计痕迹、避免误伤。

**原语**：
- 顶层 deny list：`rm -rf /`、`dd`、`mkfs`、fork bomb
- Hook 级 pre-check：pre-write 检查敏感路径、pre-bash 检查危险命令
- 审计日志：谁在什么时间调了什么工具
- 沙箱：不可逆动作二次确认

**资产位置**：`.claude/harness/security/`

## 3. 统一 frontmatter schema

所有 command / skill / agent 后续按此 schema 补齐 `harness:` 块（可选，缺省走默认档）：

```yaml
---
name: <name>
description: <one-line>
argument-hint: <hint>
user-invocable: true|false

harness:
  execute:
    tools: [Read, Write, Edit]     # allowed-tools 短名
    preset: writing-scoped         # 或引用 .claude/harness/execute/presets/
    parallel: false                # 是否鼓励并行

  constrain:
    profile: writing-safe          # 引用 .claude/harness/constrain/profiles/
    gates: [before-write]          # 关键节点必须问

  loop:
    mode: one-shot                 # one-shot | pipeline | iterative | parallel | monitor
    max-iterations: 5              # iterative 模式下
    budget-tokens: 100k            # 可选预算上限

  memory:
    reads: [user-profile, project-context]
    writes: [output-history]
    scope: project                 # session | project | user

  security:
    danger-level: low              # low | medium | high
    audit: false                   # 是否强制审计日志
---
```

**回退规则**：如果某 command 没有 `harness:` 块，harness 用五个默认档中的 `default` 档（read-only + one-shot + session-memory + medium-security）。

## 4. 五种执行模式（Loop.mode 枚举）

| mode | 语义 | 典型场景 | harness 表现 |
|---|---|---|---|
| `one-shot` | 一次问答一次输出 | /prd --mode lite、/marketing-copy、大部分 commands | 无循环，输出即结束 |
| `pipeline` | 固定阶段串行 | /bid 七阶段、/prd --flow discovery（diagnose→concept→impl） | 阶段间可插 gate |
| `iterative` | 写→评→改直到达标 | @style-evolver、@bid-writer 评审、humanizer 迭代 | 用 /loop + max-iterations |
| `parallel` | 独立子任务并行 | @research-analyst 多角度调研、review-all 多维度审查 | Agent 并行调度 |
| `monitor` | 常驻观察外部状态 | 竞品跟踪、日志监控、CI 状态跟踪 | Monitor 工具 + persistent |

## 5. 权限画像（Constrain.profile 预置档）

| profile | 允许 | 询问 | 拒绝 | 适用 |
|---|---|---|---|---|
| `read-only` | Read/Grep/Glob | Write/Edit | Bash | 分析、评估、评审类 |
| `writing-safe` | Read/Grep/Glob/Write/Edit | Bash | rm/网络请求 | 写作、PRD 生成 |
| `research` | Read/Grep/Glob/WebSearch/WebFetch | Bash/Write | rm | 调研、市场分析 |
| `media-heavy` | Read/Write/Bash(node/python/ffmpeg) | curl/wget | rm -rf | 视频、图表、PPT |
| `shell-restricted` | Read/Write/Edit/Bash(git only) | 其他 Bash | rm/dd | 一般开发操作 |
| `full-trust` | 全部 | 少 | deny list | agent 编排类（谨慎） |

## 6. 目标目录结构

```
WorkAgent/
├── HARNESS_FRAMEWORK.md          # 本文件（顶层锚点）
├── README.md                     # 项目主 README（更新指向 harness）
│
├── .claude/
│   ├── settings.json             # 全局权限 + hooks 位（画像详细规则在 harness/constrain）
│   ├── CLAUDE.md                 # ★ 项目级说明（所有会话必读）
│   ├── README.md                 # 完整命令 / 组件索引
│   │
│   ├── harness/                  # ★ 五能力分层原语
│   │   ├── README.md
│   │   ├── execute/presets.md    # 工具预设 6 类
│   │   ├── constrain/profiles.md # 权限画像 6 类 + gate
│   │   ├── loop/modes.md         # 5 种执行模式
│   │   ├── memory/schema.md      # 4 种作用域
│   │   └── security/policies.md  # 3 级危险度 + deny list
│   │
│   ├── hooks/                    # ★ hook 脚本（4 个骨架，默认未启用）
│   ├── memory/                   # ★ 项目级记忆（MEMORY.md 索引 + 分文件）
│   └── scripts/                  # ★ migrate.py + validate-harness.py
│
├── agents/                       # 24 个业务角色（100% harness 化）
├── commands/                     # 86 个入口（100% harness 化）
├── skills/                       # 115 个知识模块（100% harness 化）
├── templates/                    # 25 个模板
│
└── docs/                         # 元文档归档
    ├── AGENT_ROUTING.md
    ├── AUDIT.md
    ├── HEALTH_REPORT.md
    └── CONSOLIDATION_PLAN.md
```

**运行时目录**（按需生成，不预建）：
- `.claude/audit/YYYY-MM-DD.log` — 启用 audit.sh 后生成
- `.claude/backups/YYYY-MM-DD/` — 启用 post-write-backup.sh 后生成

## 7. 迁移优先级

**P0（本轮已完成）**：
1. ✅ 建立 `.claude/harness/` 五子目录 + 每目录 README + 5 类原语文件
2. ✅ 新建 `.claude/CLAUDE.md`（项目级说明）
3. ✅ 新建 `.claude/memory/`（MEMORY.md 索引 + project-context / conventions / decisions）
4. ✅ 新建 `.claude/hooks/README.md`（骨架，settings.json 预留 hooks 位）
5. ✅ 归档元文档到 `docs/`
6. ✅ 3 个代表性场景做 harness 化改造：
   - `commands/product/prd.md` — one-shot（+ discovery pipeline 分支）
   - `commands/presales/bid.md` — pipeline 七阶段
   - `commands/writing/article-writer.md` — iterative（四层自检）

**P1（已完成）**：
7. ✅ 为 61 个缺 `allowed-tools` 的 command 补 `allowed-tools` + `harness:` 块（86/86 覆盖）
8. ✅ 为 24 个 agent 补 `harness:` 块（24/24 覆盖）
9. ✅ 增补 `.claude/hooks/` 实际脚本（pre-write-sensitive-guard / pre-bash-danger / post-write-backup / audit）

**P2（已完成）**：
10. ✅ 为 115 个 skill 补 `harness:` 块（115/115 覆盖）

**P3（v3.1 已完成）**：
11. ✅ 3 个 hook 默认启用（pre-write-sensitive-guard / pre-bash-danger / harness-context-inject）
12. ✅ 场景感知 MVP：UserPromptSubmit hook 自动注入命令的 harness 元数据（软性，不强制拦截）
13. ✅ PowerShell 版本 hook（5 个 .ps1，无 Git Bash 环境替代）
14. ✅ templates 目录索引化：22 个活跃 + 3 个归档，0 孤儿
15. ✅ 迁移脚本合并（`migrate.py` 单入口）+ YAML 结构校验（`validate-harness.py --strict`）+ preset ↔ allowed-tools 一致性检查
16. ✅ `.gitignore` 覆盖运行时目录（audit/backups/settings.local）
17. 强制切换 permission profile 的 hook（继续延后，等生产观察 ≥1 个月）

**当前覆盖率**：commands 86/86 · agents 24/24 · skills 115/115 = **225/225 (100%)**
**Hook 启用率**：3/5（安全 guard × 2 + 上下文注入 × 1；备份 / 审计保持骨架）

## 8. 批处理迁移模板

对某个域批量补齐时，用以下模板（以 `commands/writing/*.md` 为例）：

```yaml
# 追加到 frontmatter 内、--- 之前
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
    danger-level: low
```

需要特殊处理的命令（如 iterative 写作、pipeline 流程）在批处理后单独覆盖。

## 8. 与现有资产的映射

| 现有资产 | 归入 harness 层 |
|---|---|
| `allowed-tools:` frontmatter | Execute |
| `.claude/settings.json` permissions | Constrain + Security |
| `AskUserQuestion` 交互点 | Constrain（gate） |
| `MaxTurns:` (agents) | Loop |
| `/loop` 命令 | Loop |
| Agent 的 `memory:` 字段 | Memory |
| 用户 auto-memory 目录 | Memory |
| `deny` 列表 | Security |
| 顶层 `AGENT_ROUTING.md` | Execute（agent 路由规则） |

## 9. 不做的事

- **不重写业务命令的正文**：只补 frontmatter 的 `harness:` 块和把权限画像挪到画像文件
- **不改 skills 内部逻辑**：skills 是知识库，harness 化只影响调用方式不影响内容
- **不引入新的工具/框架**：所有能力都用 Claude Code 原生的 tools/hooks/settings/memory 机制

---

**下一步**：见 §7 迁移优先级 P0。本次重构完成后，每个 command 的一句话可以从"这是 XX 命令"升级为"这是 XX 命令，在 harness 五能力层的定位是 [execute: 写作画像 / loop: iterative / memory: project / security: low]"。
