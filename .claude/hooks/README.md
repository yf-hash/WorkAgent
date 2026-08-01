# .claude/hooks — hook 脚本

> 本目录存放 Claude Code hook 脚本，被 `.claude/settings.json` 里的 `hooks` 字段引用。
>
> **v3.1 状态**：3 个已默认启用（安全 + 上下文注入），2 个骨架待按需开启（备份 + 审计）。

## 脚本清单

每个 hook 提供 **两种实现**：`.sh`（Git Bash / WSL）+ `.ps1`（Windows PowerShell），行为等价。settings.json 里换一下路径即可切换引擎。

| 脚本 | 事件 | 状态 | 作用 |
|---|---|---|---|
| `pre-write-sensitive-guard`（[.sh](pre-write-sensitive-guard.sh) / [.ps1](pre-write-sensitive-guard.ps1)） | `PreToolUse` matcher `Write\|Edit` | ✅ **默认启用（.sh）** | 拦截写入 `.claude/settings.json`、`.git/hooks/`、`.env`、`~/.ssh/` 等敏感路径 |
| `pre-bash-danger`（[.sh](pre-bash-danger.sh) / [.ps1](pre-bash-danger.ps1)） | `PreToolUse` matcher `Bash` | ✅ **默认启用（.sh）** | 拦截 `rm -rf /` / `dd` / `mkfs` / fork bomb / `git push --force main` / `curl \| sh` 等 |
| `harness-context-inject`（[.sh](harness-context-inject.sh) / [.ps1](harness-context-inject.ps1)） | `UserPromptSubmit` matcher `.*` | ✅ **默认启用（.sh）** | 检测 `/command` 调用，读取该命令的 harness 元数据（preset / profile / loop.mode / danger-level）注入到会话上下文，让 Claude 自我遵循场景约束 |
| `post-write-backup`（[.sh](post-write-backup.sh) / [.ps1](post-write-backup.ps1)） | `PreToolUse` matcher `Write\|Edit` | ⚪ 骨架 | 覆盖已有文件前先备份到 `.claude/backups/YYYY-MM-DD/` |
| `audit`（[.sh](audit.sh) / [.ps1](audit.ps1)） | `PostToolUse` matcher `.*` | ⚪ 骨架 | 记录工具调用到 `.claude/audit/YYYY-MM-DD.log` |

## 引擎选择

**Git Bash（默认）**：settings.json 里的 hook 调用形如 `bash .claude/hooks/xxx.sh`。要求本机装了 Git（自带 Git Bash）。macOS / Linux 也走这条路径。

**PowerShell**：无 Git Bash 环境下，把 settings.json 里的 `bash xxx.sh` 换成 `powershell -NoProfile -File xxx.ps1`：

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          { "type": "command", "command": "powershell -NoProfile -File .claude/hooks/pre-write-sensitive-guard.ps1" }
        ]
      }
    ]
  }
}
```

**.ps1 版本注意事项**：
- 文件带 UTF-8 BOM，避免 PowerShell 5.x 在中文 Windows 上按 GBK 解析导致乱码
- 消息用英文（PS5 输出编码问题），中文用户读 stderr 需 UTF-8 终端
- PowerShell 7（pwsh）无编码问题，可直接用 `pwsh -File`

## 已启用 hook 的效果

**pre-write-sensitive-guard**：
- 写入敏感路径 → exit 2 + stderr 提示 → 模型看到错误并调整
- 写入 `./output/*` 等正常路径 → exit 0 放行

**pre-bash-danger**：
- 执行 `rm -rf /` / `dd if=/dev/xxx` / fork bomb / `git push --force main/master` / `curl | sh` → 拦截
- 执行 `ls` / `git status` / `python x.py` 等 → 放行

**harness-context-inject**（v3.1 新增，MVP）：
- 用户敲 `/prd 需求描述 --mode standard` → 注入：
  ```
  [HARNESS] 用户调用了 /prd，harness 元数据：
  - execute.preset: writing-scoped
  - constrain.profile: writing-safe
  - loop.mode: one-shot
  - memory.scope: project
  - security.danger-level: low
  请按此约束行动：只用 preset 允许的工具、遵守 profile 的 gate、按 loop.mode 决定是否循环、按 danger-level 决定是否二次确认。
  ```
- 让模型在思考阶段就感知场景约束，实现"软性"的场景切换（不强制拦截，避免误伤）

## 启用剩余 hook（备份 + 审计）

编辑 `.claude/settings.json`，把 `_examples_backup_and_audit` 里的两个块合并到正式 `hooks` 对象：

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          { "type": "command", "command": "bash .claude/hooks/pre-write-sensitive-guard.sh" },
          { "type": "command", "command": "bash .claude/hooks/post-write-backup.sh" }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          { "type": "command", "command": "bash .claude/hooks/audit.sh" }
        ]
      }
    ]
  }
}
```

**权衡**：
- `post-write-backup.sh` 会累积磁盘占用（每次 Write 都拷一份）——适合本地开发调试期启用，团队协作时关掉
- `audit.sh` 会写日志，Bash 频繁调用时噪声大——建议只匹配 `danger-level=high` 场景

## Hook 事件参考（Claude Code 官方）

| 事件 | 时机 | 典型用途 |
|---|---|---|
| `PreToolUse` | 工具调用前 | 敏感路径拦截、参数校验、备份 |
| `PostToolUse` | 工具调用后 | 结果记录、自动 lint、缓存 |
| `UserPromptSubmit` | 用户提交前 | 输入分类、注入项目上下文 |
| `Stop` | 会话/任务结束 | 生成总结、导出 CONTEXT.md |
| `Notification` | 通知发送时 | 二次转发到 Slack/Email |

## 契约

- 脚本从 **stdin** 读 JSON（`PreToolUse`/`PostToolUse`：`{ tool_name, tool_input, tool_response }`；`UserPromptSubmit`：`{ prompt }`）
- 退出码：`0` 放行、`2` 拒绝（stderr 反馈给模型）、其他为错误
- `UserPromptSubmit` 特殊：stdout 若为 JSON `{"additionalContext": "..."}` → 注入到上下文
- 依赖 `python` + `bash`（Git Bash 或原生 bash）——已在 `settings.json` 的 allow 列表
- Windows 上通过 Git Bash 执行 `.sh`（已验证）

## 运行时目录（按需生成）

- `.claude/audit/YYYY-MM-DD.log` — 启用 audit.sh 后
- `.claude/backups/YYYY-MM-DD/<原路径>.HHMMSS` — 启用 post-write-backup.sh 后
- 建议加入 `.gitignore`：
  ```
  .claude/audit/
  .claude/backups/
  ```


