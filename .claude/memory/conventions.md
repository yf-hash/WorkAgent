---
name: conventions
description: WorkAgent 仓库的目录 / 命名 / frontmatter 规范
metadata:
  type: project
---

## 目录

- `commands/<domain>/<name>.md` — 用户直接调用的斜杠命令，domain 是 product/writing/media/research/presales/tools
- `skills/<subdomain>/<name>/SKILL.md` — 单一职责的知识模块（`user-invocable: false`）
- `agents/<name>.md` — 业务角色代理（编排多个 skill）
- `templates/*.md` — 可填充的输出模板
- `.claude/harness/*` — 五能力层原语（v3.0 新增）
- `.claude/memory/*` — 项目级记忆
- `.claude/hooks/*` — hook 脚本
- `docs/*` — 元文档归档（AGENT_ROUTING / AUDIT / HEALTH / CONSOLIDATION）

## 命名

- Commands：动词短语（`prd` / `bid` / `humanize` / `market-research`）
- Skills：名词短语（`prd-standard` / `bid-analyze` / `humanizer-scan`）
- Agents：角色名 + `-writer/-designer/-strategist/-analyst`（`bid-writer` / `impeccable-designer`）
- 全部 kebab-case，不允许下划线

## Frontmatter 必填

Commands：
```yaml
---
name: <kebab>
description: <one-line>
argument-hint: "<hint>"
user-invocable: true
allowed-tools: [Read, Write, Edit]        # 兼容字段，未来由 harness.execute.preset 取代
harness:                                  # v3.0 新增，可选
  execute:
    preset: writing-scoped
  constrain:
    profile: writing-safe
  loop:
    mode: one-shot
  memory:
    scope: project
  security:
    danger-level: low
---
```

Skills：
```yaml
---
name: <kebab>
description: |
  <多行描述，含触发词>
user-invocable: false
effort: low|medium|high
harness: {...}                            # v3.0 新增，可选
---
```

Agents：
```yaml
---
name: <kebab>
description: <one-line>
model: opus|sonnet|haiku
tools: <逗号列表>
skills: [<skill 名>, ...]
memory: session|project|user|agent
effort: low|medium|high
color: <color>
MaxTurns: <int>
harness: {...}                            # v3.0 新增，可选
---
```

## 写作规则

- Commands 正文 ≤ 200 行，膨胀就把知识挪进 skill
- Skills 正文 ≤ 600 行，膨胀就拆子 skill
- Agents 正文 ≤ 400 行，膨胀就精简 checklist 或挪到 templates/
- 中文技术类：**不打空格**（"harness 层"不写"harness 层"是错的—— harness 是外文词，需空格）
  - 正确："harness 层"、"agent 编排"、"skill 复用"
  - 错误："harness层"、"agent编排"

## v3.0 harness 迁移原则

- 所有新命令必须声明 `harness:` 块
- 存量命令按 P1 批次补齐，先补 `harness.execute.preset` 和 `harness.loop.mode`
- 不改业务命令正文
