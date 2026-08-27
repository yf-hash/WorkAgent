# WorkAgent — 项目级说明（所有 Claude Code 会话必读）

> 你现在进入的是 **WorkAgent** 仓库：一套面向产品经理 / 售前 / 内容三个角色的 AI 工作智能体（26 commands + 27 skills + 3 agents + 3 roles，v3.2）。
>
> 本文件由 Claude Code harness 在每次会话开始时自动载入，用于在**模型思考**之上强制一层**项目级执行规范**。

## 一、你在这里做什么

WorkAgent 的核心命题是：**大模型作为算力，harness 作为执行器**——你（Claude）负责理解和生成，harness（Claude Code 框架）负责执行、约束、循环、记忆、安全。

顶层框架文档见 [`../HARNESS_FRAMEWORK.md`](../HARNESS_FRAMEWORK.md)。所有 harness 原语见 [`harness/`](harness/)。

## 二、五能力分层速查

| 层 | 你需要做的判断 | harness 提供 |
|---|---|---|
| Execute | 用哪些工具？ | [`harness/execute/presets.md`](harness/execute/presets.md) 6 类预设 |
| Constrain | 该问用户吗？该拒绝吗？ | [`harness/constrain/profiles.md`](harness/constrain/profiles.md) 6 类画像 |
| Loop | 一次搞完还是要循环？ | [`harness/loop/modes.md`](harness/loop/modes.md) 5 种模式 |
| Memory | 从哪读上下文？往哪写？ | [`harness/memory/schema.md`](harness/memory/schema.md) 4 种作用域 |
| Security | 会不会造成不可逆伤害？ | [`harness/security/policies.md`](harness/security/policies.md) 3 级危险度 |

## 三、命令 / 技能 / 代理的语义

- **Commands**（`commands/`，26 个）：斜杠命令，用户直接调用的入口，含 argument-hint 和输入结构；分 3 域（product/presales/content）
- **Skills**（`skills/`，27 个）：可复用知识模块，`user-invocable: false` 表示只被 command/agent 调用
- **Agents**（`agents/`，3 个）：三大角色总入口（PM / SA / Content），编排 commands 完成端到端流水线
- **Roles**（`roles/`，3 个）：声明式能力清单（`manifest.yaml` + `workflows.md`），供 agent 读取路由

## 四、本仓库的硬规则

1. **不要新造 command / skill / agent 除非用户明确要求**——现有资产已经很密，先复用
2. **command 的正文只写"分派逻辑"和"关键约束"，具体知识放对应 skill**——避免 command 膨胀
3. **frontmatter 里没声明 `harness:` 的走默认档**（read-only + one-shot + session-memory + medium-security）
4. **写作类命令产出的文档默认放在 `./output/` 或用户指定路径**，不写入 `commands/skills/agents/templates` 任何一处
5. **修改 command / skill / agent 前先读原文**——Edit 工具会强制这样做，别绕过

## 五、常见误区

- ❌ 用 `/prd` 时不看 `--mode`，直接自行揣测走 standard——**必须问一下**（本文件加载了 [`../commands/product/prd.md`](../commands/product/prd.md) 的模式列表）
- ❌ 遇到 pipeline 类命令（`/pm-pipeline` / `/sa-pipeline` / `/content` / `/pm-competitive`）时试图一口气跑完——**阶段间必须 gate**
- ❌ 在 iterative 类命令中忽略 max-iterations——**必须停下来汇报**
- ❌ 编辑 `.claude/settings.json` 未经用户确认——**属于 security.deny list**
- ❌ 写 memory 记录了 API key / 密码 / 敏感路径——**属于 security 拦截项**

## 六、给用户的入口

用户第一次进来时通常应问：
1. 你现在的角色？（PM / 售前 SA / 内容 Content）
2. 你想产出什么？（PRD + 技术规格 / 售前方案 + 报价 / 八大文体内容）
3. 有目标客户 / 项目背景吗？（Content 场景优先问是否要关联现有 PM / SA 项目）

然后按结果推荐 `/pm` · `/sa` · `/content` 角色总入口或具体流水线命令。

## 七、迭代原则

- 每次显著变更后更新 [`../HARNESS_FRAMEWORK.md`](../HARNESS_FRAMEWORK.md) 的迁移优先级章节
- 新增 harness 原语时同步更新 [`harness/README.md`](harness/README.md)
- 项目级重要决策记入 [`memory/decisions.md`](memory/decisions.md)
