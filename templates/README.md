# templates — 填充模板索引

> 22 个静态模板，由 commands / skills / agents 通过 Read 工具按需加载。
> **模板本身不带 harness 元数据**：它们是数据，不是执行组件；消费它的 command/agent 的 harness 决定执行边界。
> 归档的模板见 [`archive/README.md`](archive/README.md)。

## 顶层模板（通用产品 / 研发 / 销售）

| 模板 | 用途 | 主要引用者 |
|---|---|---|
| [`acceptance-checklist-template`](acceptance-checklist-template.md) | acceptance checklist | `agents/qa-acceptance-designer.md`、`skills/pm/pm-qa-acceptance/SKILL.md`、`skills/strategy/launch-checklist/SKILL.md` |
| [`ai-eval-rubric-template`](ai-eval-rubric-template.md) | ai eval rubric | `agents/ai-product-architect.md`、`commands/product/ai-red-team.md`、`skills/pm/pm-ai-era-evolution/SKILL.md`（+1） |
| [`model-card-template`](model-card-template.md) | model card | `commands/product/ai-red-team.md`、`skills/pm/pm-ai-era-evolution/SKILL.md`、`skills/strategy/ai-red-team/SKILL.md` |
| [`pm-discovery-template`](pm-discovery-template.md) | pm discovery | `skills/pm/pm-discovery-frameworks/SKILL.md` |
| [`pr-faq-template`](pr-faq-template.md) | pr faq | `commands/product/working-backwards.md`、`skills/pm/working-backwards/SKILL.md`、`skills/writing/marketing-copy/SKILL.md` |
| [`prd-template`](prd-template.md) | prd | `agents/prd-coach.md`、`commands/product/prd.md`、`skills/prd/prd-deep-evaluate/SKILL.md`（+2） |
| [`release-note-template`](release-note-template.md) | release note | `skills/strategy/launch-checklist/SKILL.md` |
| [`roadmap-template`](roadmap-template.md) | roadmap | `skills/strategy/product-roadmap/SKILL.md` |
| [`sales-enablement-template`](sales-enablement-template.md) | sales enablement | `commands/product/pm-sales-pack.md`、`skills/writing/marketing-copy/SKILL.md` |
| [`six-pager-template`](six-pager-template.md) | six pager | `commands/product/working-backwards.md`、`skills/pm/working-backwards/SKILL.md` |

## 产品资料模板（templates/product/）

由 `skills/product/product-writer-router` 按需 Read，实现 16 类产品资料的原子化。

| 模板 | 主要引用者 |
|---|---|
| [`product/bid-params`](product/bid-params.md) | `commands/presales/product-bid-params.md`、`skills/product/product-writer-router/SKILL.md`、`skills/strategy/compliance-checklist/SKILL.md` |
| [`product/brochure`](product/brochure.md) | `commands/presales/product-brochure.md`、`skills/product/product-writer-router/SKILL.md` |
| [`product/compat`](product/compat.md) | `commands/presales/product-compat.md`、`skills/product/product-writer-router/SKILL.md` |
| [`product/competitive`](product/competitive.md) | `commands/presales/product-competitive.md`、`skills/product/product-writer-router/SKILL.md` |
| [`product/deploy`](product/deploy.md) | `commands/presales/product-deploy.md`、`skills/product/product-writer-router/SKILL.md` |
| [`product/function-list`](product/function-list.md) | `commands/presales/product-function-list.md`、`skills/product/product-writer-router/SKILL.md` |
| [`product/intro-business`](product/intro-business.md) | `commands/presales/product-intro-business.md`、`skills/product/product-writer-router/SKILL.md` |
| [`product/intro-tech`](product/intro-tech.md) | `commands/presales/product-intro-tech.md`、`skills/product/product-tech-whitepaper-writer/SKILL.md`、`skills/product/product-writer-router/SKILL.md` |
| [`product/manual`](product/manual.md) | `commands/presales/product-manual.md`、`skills/product/product-writer-router/SKILL.md` |
| [`product/release-note`](product/release-note.md) | `commands/presales/product-release-note.md`、`skills/product/product-writer-router/SKILL.md` |
| [`product/sales-faq`](product/sales-faq.md) | `commands/presales/product-sales-faq.md`、`skills/product/product-writer-router/SKILL.md` |
| [`product/training`](product/training.md) | `commands/presales/product-training.md`、`skills/product/product-writer-router/SKILL.md` |

## 与 harness 层的关系

- Template = 数据（被读的 markdown）
- Command / Skill / Agent = 执行体（有 `harness:` 块）
- Template 不需要 `harness:` 字段；使用它的组件的 harness 生效

## 修改 template 的影响面

改一个 template → 影响所有 "主要引用者" 列出的组件的输出。修改前对照本索引评估。

## 重新生成本索引

```bash
python .claude/scripts/templates-index.py
```

扫描全仓 grep 引用关系，覆盖写入本文件。
