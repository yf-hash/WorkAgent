---
name: content-archive
description: 【模块 5】内容归档 + 多格式导出 + 跨流水线回写。扫描 content-pipeline 目录生成 README + CHANGELOG + VERSION + freeze 只读快照，支持导出 Markdown / Word / PPT JSON，如关联 PM/SA 项目可将产物挂载到原项目附属产物目录。
user-invocable: true
argument-hint: "<content-pipeline 目录路径> [--bump major|minor|patch] [--freeze] [--tag <name>] [--export markdown|word|ppt-json|all] [--writeback]"
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob, AskUserQuestion]
model: sonnet  # 轻量：归档 + 版本递增 + 格式导出，无需 opus
harness:
  execute:
    preset: writing-scoped
    tools: [Bash]  # extend: freeze 打包 / 多格式导出脚本
  constrain:
    profile: writing-safe
    gates: [before-write, before-freeze, before-writeback]
  loop:
    mode: one-shot
  memory:
    scope: project
    reads: [project-context, content-validate-history]
    writes: [content-archive-history]
  security:
    danger-level: low
---

# /content-archive — 内容归档 + 多格式导出（Module 5）

> **端到端内容创作流水线的第 5 站（收尾）**

## 一句话

**扫描 content-pipeline 目录里的产物，生成 README + CHANGELOG + VERSION + freeze 快照，多格式导出，可选择性回写到关联 PM/SA 项目的附属产物目录**。

## 输入

```bash
# 归档一个已完成的流水线目录
/content-archive ./output/content-pipeline/solution-whitepaper-vulnhunter-20260827/

# 递增版本
/content-archive ./output/content-pipeline/xxx/ --bump minor

# freeze 冻结（发布版本）
/content-archive ./output/content-pipeline/xxx/ --freeze --tag "v1.0-发布版"

# 多格式导出
/content-archive ./output/content-pipeline/xxx/ --export all

# 只导出 Word
/content-archive ./output/content-pipeline/xxx/ --export word

# 回写到关联 PM/SA 项目
/content-archive ./output/content-pipeline/xxx/ --writeback
```

## 必备产物 checklist

| 文件 | 归属 | 必需 |
|---|---|---|
| `00-content-request.json` | M1 | ✅ |
| `01-material-pool.md` | M2 | 视场景（有项目关联时必需） |
| `02-draft.md` | M3 | ✅ |
| `02-draft.json` | M3 | 仅 PPT 类必需 |
| `03-validate-report.md` | M4 | ✅ |

## 归档三步

### 步骤 1：完整性 + 校验状态检查

- 必备文件齐全？
- M4 校验状态 ≠ "需重写"？（如是，拒绝归档）

### 步骤 2：生成 README + CHANGELOG + VERSION

```markdown
# 内容包：{{style-name}} - {{topic}}

> 版本：v{{semver}}
> 状态：草稿 / 评审中 / 已冻结（发布版）
> 生成日期：{{yyyy-mm-dd}}
> 归档人：{{git user.name 或询问}}

## 一句话
{{content-request.topic + style}}

## 关联项目
- 类型：{{PM / SA / 无}}
- 路径：{{project.path}}
- 项目版本：{{...}}

## 交付物索引

| # | 阶段 | 产物 | 状态 |
|---|---|---|---|
| M1 | 请求解析 | [00-content-request.json](./00-content-request.json) | ✅ |
| M2 | 素材抽取 | [01-material-pool.md](./01-material-pool.md) | ✅ |
| M3 | 初稿生成 | [02-draft.md](./02-draft.md) | ✅ |
| M4 | 校验报告 | [03-validate-report.md](./03-validate-report.md) | ✅ |
| M5 | 归档导出 | 本文件 + _export/ | ✅ |

## 校验结果摘要
- 事实一致性：✅
- 合规风险：✅（0 处 🔴，2 处 🟠 已修复）
- 文体匹配度：8.5/10
- 完整性：完整
- 引用可追溯率：92%

## 关键信息
- 文体：{{style.name}}
- 篇幅：{{final_length}}（目标 {{target}}）
- 受众：{{audience}}

## 变更历史
见 [CHANGELOG.md](./CHANGELOG.md)

## 多格式产物

在 `./_export/` 中：
- `{topic}.md` — Markdown 版
- `{topic}.docx` — Word 版
- `{topic}.pptx.json` — PPT 结构化 JSON（PPT 类）

## 跨流水线回写

（如启用 --writeback）本内容已挂载到关联项目附属产物：
- `{project.path}/_content/{style-id}-{topic-slug}-{yyyymmdd}/`
```

### 步骤 3：多格式导出（--export）

在归档目录下创建 `_export/`：

| 参数 | 导出 |
|---|---|
| `--export markdown` | 复制 02-draft.md 到 `_export/{topic}.md` |
| `--export word` | 用 pandoc 转换为 `.docx`（需本机有 pandoc） |
| `--export ppt-json` | 复制 02-draft.json 到 `_export/{topic}.pptx.json` |
| `--export all` | 全部导出 |

## Harness 卡点

### `before-write` gate

如果任一项：
- M4 校验状态 = "需重写"
- 必备产物缺失

→ AskUserQuestion：
```
以下问题未解决：
  - M4 校验：{status}
  - 缺失：{列表}

是否仍要归档？
- n（推荐）：先回上游修复
- y-force：强制归档，问题写入 known-issues.md
```

### `before-freeze` gate

`--freeze` 二次确认（不可撤销的只读操作）。

### `before-writeback` gate

`--writeback` 二次确认：
```
将把以下产物回写到 PM/SA 项目：
  源：./output/content-pipeline/xxx/
  目标：{project.path}/_content/{style}-{topic}-{yyyymmdd}/

这会在原项目目录创建新子目录（不覆盖原有文件）。

确认？(y / n)
```

## 输出目录

```
./output/content-pipeline/{style}-{topic}-{yyyymmdd}/
├── 00-content-request.json
├── 01-material-pool.md
├── 02-draft.md
├── 02-draft.json               ← 仅 PPT 类
├── 03-validate-report.md
├── review-notes.md              ← 【本命令产出，可选】
├── README.md                    ← 【本命令产出】索引 + 版本 + 摘要
├── CHANGELOG.md                 ← 【本命令产出】变更历史
├── VERSION                       ← 【本命令产出】语义化版本号
├── archive-report.md            ← 【本命令产出】完整性 + 校验状态
├── _frozen/                     ← --freeze 生成
│   └── v1.0-发布版/             ← 只读快照
└── _export/                     ← --export 生成
    ├── {topic}.md
    ├── {topic}.docx
    └── {topic}.pptx.json
```

## 跨流水线回写机制

当内容基于 PM/SA 项目生成时（M1 有 project 关联），`--writeback` 会将本次内容作为**附属产物**挂载到原项目：

```
./output/pm-pipeline/vulnhunter-20260827/
├── 00 - 06 主流水线产物
├── README.md
├── CHANGELOG.md
├── VERSION
└── _content/                         ← 【回写产生】
    ├── solution-whitepaper-vulnhunter-solution-20260827/
    │   ├── 02-draft.md
    │   └── _export/{topic}.docx
    ├── pr-vulnhunter-v2-launch-20260830/
    │   └── ...
    └── promo-vulnhunter-20260901/
        └── ...
```

此后**同一个 PM 项目同时拥有 PRD、规格书、方案、对外宣传物料**。

## 版本号规则（语义化）

| 变更类型 | Bump |
|---|---|
| 全文重写 / 换文体 / 换素材源 | major |
| 新增章节 / 大幅修改论点 | minor |
| 文案微调 / 修错别字 / 修合规词 | patch |

## 与其他命令的边界

| 场景 | 用 |
|---|---|
| **完成流水线，归档** | 本命令 |
| 内容包挂载到 PM/SA 项目 | 本命令 `--writeback` |
| 冻结发布版 | 本命令 `--freeze` |
| 多格式导出 | 本命令 `--export all` |
| 一键端到端 | `/content`（编排器） |

## 反模式

- ❌ M4 校验"需重写"就归档 —— 违规
- ❌ 修改 `_frozen/` 内容 —— 违规
- ❌ 版本号乱跳 —— 违规
- ❌ 回写时覆盖原项目文件 —— 违规（只能创建新子目录）
- ❌ PPT 类未导出 JSON —— 违规
