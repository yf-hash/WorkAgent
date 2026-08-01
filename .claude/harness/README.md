# .claude/harness — 五能力分层原语库

> 顶层框架说明见 [`../../HARNESS_FRAMEWORK.md`](../../HARNESS_FRAMEWORK.md)。

本目录存放 harness 层的**可复用原语**（reusable primitives），供 commands / skills / agents 在 frontmatter 里引用，从而把"执行 / 约束 / 循环 / 记忆 / 安全"从每个业务命令里抽出来，集中管理、集中演化。

## 五子目录

| 目录 | 提供 | 主要文件 |
|---|---|---|
| [`execute/`](execute/) | 工具白名单预设、并行/串行策略 | `presets.md`（工具预设组合） |
| [`constrain/`](constrain/) | 权限画像、gate 检查点 | `profiles.md`（6 个权限档） |
| [`loop/`](loop/) | 循环模板（pipeline/iterative/monitor） | `modes.md`（5 种执行模式） |
| [`memory/`](memory/) | 记忆读写 schema、CLAUDE.md 模板 | `schema.md`（4 种作用域） |
| [`security/`](security/) | deny list、危险动作策略、审计 | `policies.md`（3 级危险度） |

## 如何被引用

在任何 command / skill / agent 的 frontmatter 里：

```yaml
harness:
  execute:
    preset: writing-scoped          # → execute/presets.md 里的 writing-scoped
  constrain:
    profile: writing-safe           # → constrain/profiles.md 里的 writing-safe
  loop:
    mode: iterative
    max-iterations: 5
  memory:
    scope: project
  security:
    danger-level: low
```

harness 解析器（未来可用 hook 实现）读取到这些字段后，在会话开始时应用对应策略。目前先作为**约定 + 文档**存在，方便人和模型判断该命令的运行边界。

## 演化原则

- 原语文件是"简洁的规格"，不是长文——大幅膨胀就应该拆
- 每个原语必须列举：**语义 / 何时用 / 何时不用 / 与其他原语的边界**
- 新增原语前先看能不能复用现有的
