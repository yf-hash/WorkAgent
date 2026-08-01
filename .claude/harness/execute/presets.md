# Execute — 工具预设

> 常见的工具组合。命令 frontmatter 用 `harness.execute.preset: <name>` 引用，代替手写 `allowed-tools`。

## 预设清单

| preset | 展开为 allowed-tools | 适用 |
|---|---|---|
| `read-only` | `[Read, Grep, Glob]` | 分析、评估、审查、路由决策 |
| `writing-scoped` | `[Read, Write, Edit, Grep, Glob, AskUserQuestion]` | 写作类（文章、PRD、方案、marketing） |
| `research` | `[Read, Write, Grep, Glob, WebSearch, WebFetch]` | 调研、市场分析、竞品 |
| `media-heavy` | `[Read, Write, Edit, Bash, Glob]` | PPT、视频、图表、图像生成 |
| `shell-restricted` | `[Read, Write, Edit, Bash, Grep, Glob]` | 需要执行脚本但不联网 |
| `agent-orchestrator` | `[Read, Write, Edit, Grep, Glob, AskUserQuestion, Bash, WebSearch]` | agent 编排（配合 constrain.profile 收敛） |
| `default` | `[Read, Grep, Glob, AskUserQuestion]` | 未声明时的兜底（保守） |

## 组合规则

- 同一命令**只声明一个** preset；不要叠加
- 需要额外工具时，用 `tools: [...]` 显式追加：
  ```yaml
  harness:
    execute:
      preset: writing-scoped
      tools: [WebSearch]          # 追加
  ```
- 需要屏蔽 preset 里的某个工具时，写 `exclude: [...]`：
  ```yaml
  harness:
    execute:
      preset: writing-scoped
      exclude: [Bash]
  ```

## 与 constrain 的关系

- Execute 说"**能用**哪些工具"
- Constrain 说"用这些工具时**受什么约束**"（比如 Bash 只能 git *）
- 一个 command 通常一个 execute preset + 一个 constrain profile

## 边界

- 不管**并行**（并行策略在 loop.mode = parallel 里）
- 不管**是否需要人工确认**（那是 constrain.gates）
- 不管**记忆读写**（那是 memory.reads/writes）
