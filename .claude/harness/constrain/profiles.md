# Constrain — 权限画像

> 每个画像是一组 allow / ask / deny 规则，覆盖工具在**特定场景**下的可用范围。命令 frontmatter 用 `harness.constrain.profile: <name>` 引用。

## 画像清单

### `read-only`
- allow：Read / Grep / Glob / WebFetch / WebSearch
- ask：任何写操作 / Bash
- deny：rm / dd / chmod 777 / curl 敏感端点
- **场景**：评审 / 分析 / 路由决策类命令

### `writing-safe`
- allow：Read / Grep / Glob / Write / Edit / AskUserQuestion
- ask：Bash / WebFetch（外网）
- deny：rm / dd / mkfs / 覆盖 .git 目录
- **场景**：PRD / 文章 / 方案 / marketing / 各类 doc 生成

### `research`
- allow：Read / Grep / Glob / WebSearch / WebFetch / Write（仅到 `./research/` 或指定输出目录）
- ask：Bash / Edit 已有文件
- deny：Write 到 src/ 目录、rm、chmod
- **场景**：调研、市场分析、竞品跟踪

### `media-heavy`
- allow：Read / Write / Edit / Bash(node/python/ffmpeg/mmdc/plantuml)
- ask：Bash 其他命令 / curl / wget
- deny：rm -rf / mv 到系统目录
- **场景**：PPT / 视频 / 图表 / 图像生成

### `shell-restricted`
- allow：Read / Write / Edit / Bash(git *) / Grep / Glob
- ask：Bash 非 git 命令
- deny：sudo / dd / mkfs / rm -rf /
- **场景**：需要 git 操作的类开发流程

### `agent-orchestrator`
- allow：Agent tool、所有 read、Write / Edit 到 output 目录
- ask：Bash 全部 / 危险 rm
- deny：rm -rf / dd / mkfs
- **场景**：agent 编排类命令，需要广泛能力但仍收敛

### `default`（未声明时的兜底）
- 等同于 `read-only` + `AskUserQuestion`
- 保守优先

## 全局规则（所有画像叠加）

无论哪个画像，永久 deny：
- `rm -rf /` / `rm -rf ~` / `rm -rf .*`
- `dd if=/dev/*` / `mkfs*`
- Fork bomb `:(){ :|:& };:`
- 直接推送到 `main/master` 的 force push
- 覆盖 `.claude/settings.json` 而未经 AskUserQuestion

这一层由 `../security/policies.md` 定义，profile 只能**更严**，不能放宽这些。

## Gates（可选）

除了 allow/ask/deny，profile 还可以要求**关键节点必须 AskUserQuestion**：

```yaml
harness:
  constrain:
    profile: writing-safe
    gates: [before-write, before-external-send]
```

Gate 语义（**核心 gate**，跨命令通用；命令内部可再声明 `after-<stage>` 形式的自定义阶段 gate）：
- `before-write`：在第一次 Write/Edit 前问一次（防止误覆盖）
- `before-external-send`：在推送到 GitHub/Slack/Email 前必须二次确认
- `before-destructive`：任何 rm/mv 前必须确认
- `before-loop-restart`：iterative loop 每 N 轮汇报一次是否继续
- `before-freeze`：归档流水线在生成 `_frozen/` 只读快照前必须确认（不可逆）
- `before-writeback`：Content 流水线在把产物写回关联 PM/SA 项目 `_content/` 前必须确认（会修改另一个项目目录）

**自定义 gate 命名规则**：`^(before|after)-<kebab-case>$`。例如 `after-decompose`（角色 agent 展示计划后确认）、`after-metrics-list`（技术规格书列出 6 大类指标后确认）。`validate-harness.py` 只校验格式，不校验语义——每个命令负责在正文里解释自己的自定义 gate。

## 与 execute 的边界

- execute 决定"**能调用**哪些工具"
- constrain 决定"**如何**调用（哪些直接执行、哪些先问、哪些禁止）"
- 一个命令同时声明两者，harness 取**交集**（约束更严）
