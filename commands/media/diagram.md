---
name: diagram
description: >
  图表生成命令，整合 Markmap（思维导图）、PlantUML（UML全系）、Mermaid（流程/时序/甘特）、
  MerdiAi（AI自然语言生成）、diagrams（云架构图）、visio（企业Visio格式）六大引擎，
  按图表类型智能路由；云架构图和 Visio 格式请直接使用 /arch-diagram 和 /visio 命令
user-invocable: true
argument-hint: "<描述或内容> [--engine markmap|plantuml|mermaid|ai|arch|visio|auto] [--type mindmap|flow|sequence|class|er|gantt|component|state|json|cloud|org] [--output code|render|file]"
---

# /diagram — 多引擎图表生成

加载技能：`skills/diagram-suite/SKILL.md`

## 触发条件
需要生成思维导图、UML图、流程图、时序图、甘特图、ER图、架构图，或用自然语言描述图表时。

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `<描述或内容>` | 图表内容描述或原始文本（必填） | — |
| `--engine` | 渲染引擎 | `auto` |
| `--type` | 图表类型 | 自动判断 |
| `--output` | 输出方式 | `code` |

### 引擎选择（--engine）
| 值 | 引擎 | 最适合 |
|----|------|--------|
| `markmap` | Markmap | 思维导图、知识树、大纲可视化 |
| `plantuml` | PlantUML | UML全系、架构图、JSON可视化 |
| `mermaid` | Mermaid | 流程图、时序图、甘特图、ER图 |
| `ai` | MerdiAi/Claude | 自然语言 → 图表（自动选型） |
| `arch` | mingrammer/diagrams | 云架构图（AWS/GCP/Azure/K8s）→ 转发至 `/arch-diagram` |
| `visio` | python-visio / Visio.NET | Visio .vsdx 格式 → 转发至 `/visio` |
| `auto` | 自动路由 | 根据 --type 和描述智能选择 |

### 图表类型（--type）
| 值 | 类型 | 推荐引擎 |
|----|------|---------|
| `mindmap` | 思维导图 | markmap |
| `flow` | 流程图 | mermaid |
| `sequence` | 时序图 | mermaid / plantuml |
| `class` | 类图 | plantuml |
| `er` | ER图 | mermaid |
| `gantt` | 甘特图 | mermaid |
| `component` | 组件/架构图 | plantuml |
| `state` | 状态图 | mermaid / plantuml |
| `json` | JSON/YAML可视化 | plantuml |
| `cloud` | 云架构图 | arch（diagrams）|
| `org` | 组织架构图 | visio / plantuml |

### 输出方式（--output）
| 值 | 说明 |
|----|------|
| `code` | 输出图表代码（可复制到对应工具渲染） |
| `render` | 代码 + 渲染说明 + 在线预览链接 |
| `file` | 尝试调用 CLI 工具生成 PNG/SVG 文件 |

---

## 执行流程

```
Step 1: 引擎路由
  → 分析 --engine 和 --type 参数
  → auto 模式：根据描述关键词自动选择最优引擎
  → arch 引擎：转发至 /arch-diagram 命令（mingrammer/diagrams）
  → visio 引擎：转发至 /visio 命令（python-visio / Visio.NET）
  → 加载对应引擎的语法规范

Step 2: 内容解析
  → 提取图表的节点、关系、层级
  → 规划图表结构（节点数 ≤ 20，层级 ≤ 4）

Step 3: 代码生成
  → 按引擎语法生成图表代码
  → 标签使用中文（除非指定英文）
  → 确保语法正确可渲染

Step 4: 输出
  → code：直接输出代码块
  → render：代码 + 渲染方式说明 + 在线链接
  → file：调用 mmdc/plantuml CLI 生成文件
```

---

## 与其他命令的协同

```
/diagram → 图表代码生成
  ├── /illustrate    → 将图表嵌入文章配图流程
  ├── /md-visual     → 将 Mermaid 图表渲染为图片
  ├── /arch-diagram  → 云架构图（AWS/GCP/Azure/K8s）专用命令
  ├── /visio         → Visio .vsdx 格式专用命令
  └── @diagram-architect → 统一图表编排 Agent，自动选择最优引擎
```

---

## 使用示例

```bash
# 自然语言生成流程图（AI模式）
/diagram 用户注册流程：填写信息→验证邮箱→完善资料→激活账号 --engine ai

# 生成思维导图（Markmap）
/diagram 产品经理核心技能体系 --engine markmap --output render

# 生成系统架构图（PlantUML）
/diagram 微服务架构：API网关→认证服务→业务服务→数据库 --engine plantuml --type component

# 生成时序图（Mermaid）
/diagram OAuth2.0授权码流程 --engine mermaid --type sequence

# 生成甘特图
/diagram 项目计划：需求1周→设计1周→开发3周→测试1周→上线 --type gantt

# 生成ER图
/diagram 电商系统：用户/订单/商品/支付的关系 --type er

# 从文章大纲生成思维导图
/diagram [粘贴文章大纲] --engine markmap

# 云架构图（转发至 /arch-diagram）
/diagram AWS三层架构：CloudFront→ALB→EC2→RDS --engine arch

# Visio 格式（转发至 /visio）
/diagram 组织架构图 --engine visio --type org
```
