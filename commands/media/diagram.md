---
name: diagram
description: 图表统一入口（Mermaid/PlantUML/Markmap 等）。--type mindmap 思维导图；--type uml 全系 UML（时序/类/用例/组件/部署/活动/状态）；--type json JSON/YAML 可视化。云架构图与 Visio 走各自专用命令。
user-invocable: true
argument-hint: "<描述或路径> --type mindmap|uml|json [--subtype sequence|class|component|usecase|deployment|activity|state]"
allowed-tools: [Read, Write, Edit, Bash]
---

# /diagram — 图表统一入口

## 一句话

思维导图 / UML / 数据结构可视化一个入口。`--type` 分派。

## 用法

```bash
# 思维导图
/diagram ./outline.md --type mindmap

# UML 全系（--subtype 二级参数）
/diagram 用户登录时序图 --type uml --subtype sequence
/diagram 订单管理类图 --type uml --subtype class
/diagram 微服务组件图 --type uml --subtype component

# JSON/YAML 数据结构可视化
/diagram config.json --type json
```

## 分派规则

| `--type` | 加载技能 | 二级参数 |
|---|---|---|
| `mindmap` | `skills/diagram/diagram-markmap/SKILL.md` | — |
| `uml` | `skills/diagram/diagram-plantuml/SKILL.md` | `--subtype sequence\|class\|component\|usecase\|deployment\|activity\|state` |
| `json` | `skills/diagram/diagram-plantuml/SKILL.md`（PlantUML JSON 语法） | — |

## 与其他图表命令的边界

| 场景 | 用 |
|---|---|
| 思维导图 / UML / JSON | **本命令** |
| Mermaid 轻量流程 / 甘特 / 状态图 | `/illustrate --backend mermaid` |
| 云架构图（AWS/GCP/Azure/K8s） | `/arch-diagram` |
| Visio 创建 / 格式互转 | `/visio` |
| PPT 场景图表 | 由 `@ppt-generator` 自动路由 |

## 迁移说明（v2.8）

旧命令 `/diagram-mindmap` / `/diagram-uml` 已合并至本命令，用 `--type mindmap|uml` 替代。2 个 skill 未变。

**⚠️ 与 v2.6 拆原子命令方向的取舍**：v2.6 曾拆过 diagram-* 系列，v2.8 在命令层合回一个入口（skills 保持拆分）。用户从记 5 个命令（diagram-mindmap / diagram-uml / arch-diagram / visio / illustrate）降到记 3 个（`/diagram` 通用、`/arch-diagram` 云图、`/visio` 微软套件）。
