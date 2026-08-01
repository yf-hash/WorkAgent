# Memory — 记忆读写 schema

> 命令 frontmatter 用 `harness.memory.{scope, reads, writes}` 声明。

## 四种作用域

| scope | 生命周期 | 存储位置 | 典型内容 |
|---|---|---|---|
| `session` | 当前会话 | 上下文窗口内 | 本次对话的临时决策 |
| `project` | 当前项目 | `.claude/memory/` + MEMORY.md 索引 | 项目背景、约定、决策历史 |
| `user` | 跨项目、跨会话 | 用户 auto-memory（`~/.claude/projects/<hash>/memory/`） | 用户偏好、领域知识、协作风格 |
| `agent` | 单个 agent 的持续记忆 | agent 内部（`agents/<name>/memory.md`） | agent 的历史行动、学到的技巧 |

## 引用方式

```yaml
harness:
  memory:
    scope: project              # 主 scope
    reads:                      # 会话开始时载入
      - project-context         # → .claude/memory/project-context.md
      - user-preferences        # → 用户 auto-memory 相应文件
    writes:                     # 命令产出时按需写入
      - output-history          # → .claude/memory/output-history.md
```

## 项目级记忆的推荐分文件

放在 `.claude/memory/`，索引写入 `MEMORY.md`：

| 文件 | 内容 |
|---|---|
| `project-context.md` | 项目定位、目标用户、核心场景 |
| `conventions.md` | 项目约定：命名、目录、frontmatter 规范 |
| `decisions.md` | 关键设计决策 + 时间 + 原因 |
| `output-history.md` | 重要输出的位置 + 日期（供后续查找） |
| `user-profile.md` | 用户特定的偏好、专长、协作方式 |

## 用户级记忆（auto-memory）

- 已由 Claude Code harness 内置：`~/.claude/projects/<repo-hash>/memory/`
- 命令的 `harness.memory.reads: user-*` 会命中此层
- 详见 `MEMORY.md` 的自动机制（不由本框架管理，只引用）

## Session Export / Recall（跨 IDE、跨会话）

- `devagent:session-export` skill：导出当前会话为 CONTEXT.md
- `devagent:tool-recall` skill：跨工具搜索历史对话
- 命令声明 `harness.memory.exportable: true` 后，harness 可在会话结束时提示导出

## 反模式

- ❌ 把易变的临时决策写进 `project` 级（污染跨会话）
- ❌ 把用户敏感偏好写进 `project` 级（应该走 `user`）
- ❌ 每个 command 都声明大量 reads（会话开始时载入成本）
- ❌ 用 memory 代替 template / prompt（memory 是"当时是什么状态"，不是"应该怎么做"）

## 与 harness 其他层的边界

- **不管权限**：Write 到 memory 目录也要过 constrain
- **不管循环**：iterative 循环中的中间状态用 session，不写 project
- **不管安全**：敏感信息永不入 memory（那是 security 的事）
