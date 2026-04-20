---
name: prd
description: AI 驱动的产品需求文档（PRD）生成，支持从一句话需求到完整 PRD 的多种模式
user-invocable: true
argument-hint: "<需求描述> [--mode lite|full|gtm|workflow] [--format md|notion|linear] [--lang zh|en]"
---

# /prd — AI 产品需求文档生成器

加载技能：`skills/prd-generator/SKILL.md`

## 触发条件
需要撰写产品需求文档（PRD）、功能规格说明、用户故事、GTM 计划，或将模糊想法转换为结构化需求时。

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `<需求描述>` | 产品/功能描述（必填） | — |
| `--mode` | 文档模式 | `full` |
| `--format` | 输出格式 | `md` |
| `--lang` | 输出语言 | `zh` |

### 模式说明
| `--mode` | 输出内容 | 适用场景 |
|----------|---------|---------|
| `lite` | 一页纸 PRD（目标/用户/功能/指标） | 内部评审、快速对齐 |
| `full` | 完整 PRD（背景/目标/用户故事/功能规格/验收标准/风险） | 正式研发交付 |
| `gtm` | GTM 计划（定位/渠道/目标/启动节奏） | 产品上线准备 |
| `workflow` | 用户旅程 + 流程图（Mermaid） | 交互评审、设计对齐 |

## 参考工具生态

| 工具 | 用途 | GitHub |
|------|------|--------|
| PRDforge | AI PRD 生成框架 | TomMaSS/PRDforge |
| ai-prd-generator | Claude 驱动 PRD 生成 | cdeust/ai-prd-generator |
| gtplanner | 需求 → GTM 计划 | opensqz/gtplanner |
| claude-plugin-prd-workflow | Claude PRD 工作流插件 | Yassinello/claude-plugin-prd-workflow |
| SkillPRD | 技能需求文档规范 | Liwei-Ji/SkillPRD |
| prd-generator | 需求文档生成器 | dredozubov/prd-generator |
| carrot-prd | 创业产品 PRD 模板 | talvinder/carrot-product-requirements-document-prd |

## 执行流程

```
Step 1: 需求解析
  → 识别产品类型（To B / To C / 内部工具 / API）
  → 提取核心目标、用户群体、关键约束
  → 询问缺失的关键信息（一次性）

Step 2: 结构生成
  → 按选定模式生成 PRD 框架
  → 填充用户故事（As a... I want... So that...）
  → 定义功能规格（功能点 + 验收标准）

Step 3: 指标设计
  → 定义成功指标（主指标 + 护栏指标）
  → 设计埋点方案
  → 制定 A/B 测试策略（如适用）

Step 4: 风险评估
  → 技术风险、依赖风险、时间风险
  → 未解决的关键假设

Step 5: 输出格式化
  → Markdown / Notion / Linear 格式
  → 附 Mermaid 流程图（--mode workflow 时）
```

## 输出结构（full 模式）

```markdown
# [产品名称] PRD v1.0

## 概述
- 问题陈述
- 解决方案摘要
- 成功标准

## 用户与场景
- 目标用户画像
- 核心使用场景
- 用户旅程地图

## 功能规格
### Feature 1: [名称]
- 用户故事
- 验收标准
- 边界条件

## 非功能需求
- 性能、安全、兼容性

## 指标体系
- 北极星指标
- 核心指标
- 护栏指标

## 发布计划
- MVP 范围
- 迭代计划
- GTM 策略

## 风险与依赖
```

## 使用示例

```
/prd 开发一个 AI 写作助手浏览器插件，支持改写和润色
/prd 电商 App 增加"一键复购"功能 --mode lite
/prd SaaS 产品新用户引导流程优化 --mode workflow
/prd B2B CRM 客户跟进提醒模块 --mode full --lang en
/prd 新品上线准备 --mode gtm
```
