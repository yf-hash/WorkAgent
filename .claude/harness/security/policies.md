# Security — 危险度分级 + 全局策略

> 命令 frontmatter 用 `harness.security.{danger-level, audit}` 声明。

## 三级危险度

### `low`（默认）
- **含义**：无副作用或副作用完全可回滚
- **典型**：写文档、生成 PRD、只读分析、路由决策
- **策略**：不额外要求，走 constrain profile

### `medium`
- **含义**：可能覆盖用户已有文件、调用外部 API、消耗额度
- **典型**：文章 humanize（覆盖原稿）、web search（额度）、bash 执行本地脚本
- **策略**：
  - 首次执行前 AskUserQuestion 确认
  - 覆盖已有文件时自动备份到 `.claude/backups/`
  - 输出结果附加 "已执行动作清单"

### `high`
- **含义**：不可逆、影响外部系统、涉及权限变更
- **典型**：Git push --force、Slack/Email 推送、rm、chmod、CI/CD 触发
- **策略**：
  - **强制** AskUserQuestion 二次确认
  - 强制审计日志到 `.claude/audit/YYYY-MM-DD.log`
  - `constrain.gates: [before-destructive]` 自动生效
  - deny list 检查在最外层拦截

## 全局 deny list（永不放宽）

以下动作在**任何** profile 下都禁止：

```
rm -rf /
rm -rf ~
rm -rf .*
rm -rf $HOME
dd if=/dev/*
mkfs*
:(){ :|:& };:                      # fork bomb
git push --force main
git push --force master
覆盖 .git/hooks/ 内容
覆盖 .claude/settings.json（未经 AskUserQuestion）
覆盖 ~/.ssh/ 任何文件
写入 /etc/、C:\Windows\System32
```

顶层 `.claude/settings.json` 的 `permissions.deny` 是此清单的 CI 化实现。

## 审计（可选启用）

```yaml
harness:
  security:
    danger-level: high
    audit: true                   # 强制记录所有工具调用到日志
```

审计日志格式（.claude/audit/YYYY-MM-DD.log）：
```
2026-08-01T14:32:11 command=/bid tool=Bash args="mmdc -i in.mmd -o out.png" result=ok
2026-08-01T14:32:45 command=/bid tool=Write file="./output/bid-v1.md" bytes=42315 result=ok
```

审计日志由 hook 生成（`.claude/hooks/audit.sh`），不由模型手写。

## 敏感信息拦截

以下内容永不写入 memory / 永不外发：
- API keys / tokens（正则匹配 `sk-*` / `ghp_*` / `xoxb-*` 等）
- `.env` 文件内容
- SSH 私钥（`-----BEGIN * PRIVATE KEY-----`）
- 数据库连接串含密码

由 hook 层（`.claude/hooks/pre-write.sh`、`pre-external.sh`）执行。

## 与其他层的边界

- security 是**最后一道墙**，永远比 constrain 更严
- constrain 里的 profile 可以说 "本场景禁止 Bash"，但 security 的 deny list 永不因场景放宽
- 一个 low 级命令也可能触发 deny list（例如误传 `rm -rf ~`）——此时 hook 拦截、命令中断
