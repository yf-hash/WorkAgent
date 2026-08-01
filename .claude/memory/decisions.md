---
name: decisions
description: WorkAgent 关键设计决策历史
metadata:
  type: project
---

## 2026-08-01 · v3.0 引入 harness 五能力分层

**Why**：v2.x 累积到 86 commands + 115 skills + 24 agents，"模型思考"部分很厚，但"harness 层"（执行 / 约束 / 循环 / 记忆 / 安全）极薄。61 个 command 未声明 allowed-tools、无项目级 CLAUDE.md、无 hooks、无 memory 目录。风险：执行不稳、约束靠自觉、循环靠人手、记忆丢失、无审计。

**How to apply**：新命令必须声明 `harness:` 块；存量命令按 P0→P1→P2 三批补齐；不改业务正文。顶层锚点见 `HARNESS_FRAMEWORK.md`。

## 2026-08-01 · P1+P2 全量 harness 元数据补齐

**Why**：完成后 225 个业务组件（86 commands + 24 agents + 115 skills）全部带 `harness:` 块，覆盖率 100%。加上 4 个 hook 骨架脚本（默认未启用），harness 层从"约定"升级为"可运行"。

**How to apply**：
- 新组件用 `.claude/scripts/migrate-harness*.py` 里的域默认档；不匹配的加进 SPECIAL
- 修改 SPECIAL 后重跑脚本（幂等，只处理缺失字段）
- 启用 hook 前先看 `.claude/hooks/README.md` 的三个默认档（保守/审计/备份）

## 2026-08-01 · v3.1 hooks 启用 + 上下文注入 + templates 索引

**Why**：v3.0 只搭了 harness 骨架，运行时约束仍需人工遵循。v3.1 让 harness 真正"跑起来"：3 个 hook 默认启用（安全 guard × 2 + 上下文注入 × 1），实现"模型思考时就看到当前场景的 harness 元数据"，无需强制拦截即可自我约束。

**How to apply**：
- 敏感路径写 / 危险 bash → 自动 exit 2 拦截（安全底线）
- 用户敲 `/command` → UserPromptSubmit hook 自动查 harness 块并注入 additionalContext
- templates 目录用 `python .claude/scripts/templates-index.py` 生成索引，追踪 25 个 template 的引用者（发现 5 个孤儿：brd/mrd/pm-discovery/requirement-pool/roadmap）
- 三个 hook 已实测通过（bash 5.2 msys / Windows）

## 2026-08-01 · v3.2 清理 + 跨引擎 + 一致性校验

**Why**：v3.1 打通了运行时，但 3 项遗留：孤儿模板未处理、PowerShell 环境无 hook 版本、preset↔allowed-tools 一致性没工具保障。v3.2 做完清理，让 harness 达到"可 CI 化"成熟度。

**How to apply**：
- 5 个孤儿模板分诊：3 迁到 `templates/archive/`（brd/mrd/requirement-pool，无消费方）+ 2 补引用（roadmap/pm-discovery，给 skill 加"配套模板"章节）→ 0 孤儿
- 每个 hook 出 `.ps1` 双胞胎（UTF-8 BOM + 英文消息，兼容 PS5 中文 Windows）；settings.json 一键切换 `bash xxx.sh` ↔ `powershell -File xxx.ps1`
- `validate-harness.py` 加 preset↔allowed-tools 一致性检查（e.g. read-only 不该有 Write），允许 `harness.execute.tools` 扩展绕过
- `.gitignore` 覆盖 `.claude/audit/`、`.claude/backups/`、`.claude/settings.local.json` 等运行时目录
- 3 个 CI 门：`migrate.py --strict` + `validate-harness.py --strict` + `templates-index.py`

## 2026-08-01 · 合并 /pm-prd-enterprise 到 /prd --mode enterprise

**Why**：与 v2.8.1 收敛思路一致（`/humanize` `/bid` `/dashboard` 已单命令多模式）。B 端严格 12 章不再单独占用一个前缀。

**How to apply**：所有 `/pm-prd-enterprise ...` 改为 `/prd ... --mode enterprise`。全仓 20 处引用已同步更新。

## 2026-07-XX · v2.8 skills 分入 14 子域

**Why**：skills 从平铺 100+ 到按业务子域组织，便于导航和分批治理。

**How to apply**：新 skill 直接归入对应子域；跨域时优先复用现有 skill。
