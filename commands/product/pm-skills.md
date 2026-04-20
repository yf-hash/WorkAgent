---
name: pm-skills
description: 产品经理技能库查询与应用，涵盖框架/方法论/模板/案例，支持 Lenny's Newsletter 精华内容
user-invocable: true
argument-hint: "<技能主题或问题> [--mode framework|template|case|coach|checklist]"
---

# /pm-skills — 产品经理技能库

加载技能：`skills/pm-skills/SKILL.md`

## 触发条件
需要查询产品管理框架、获取 PM 实战模板、学习行业案例，或对产品决策/策略进行专业指导时。

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `<技能主题或问题>` | 想了解的 PM 知识点或具体问题（必填） | — |
| `--mode` | 输出模式 | `framework` |

### 输出模式
| `--mode` | 输出内容 | 适用场景 |
|----------|---------|---------|
| `framework` | 框架说明 + 使用步骤 + 适用场景 | 学习新方法论 |
| `template` | 即用模板（Markdown 格式） | 快速产出文档 |
| `case` | 行业案例分析（公司 + 策略 + 结果） | 借鉴最佳实践 |
| `coach` | 问题诊断 + 具体建议（对话形式） | 遇到具体决策困境 |
| `checklist` | 检查清单（发布/评审/规划用） | 质量把关 |

## 知识体系来源

| 来源 | 内容 | GitHub |
|------|------|--------|
| pm-skills | PM 核心技能知识库 | phuryn/pm-skills |
| product-manager-skills | 产品经理完整技能图谱 | deanpeters/product-manager-skills |
| lenny-skills | Lenny's Newsletter 精华方法论 | refound-ai/lenny-skills |
| Dossier | 产品人个人知识库系统 | rwliebs/Dossier |
| pm-ai | AI 时代产品经理实践指南 | arkham2424/pm-ai |
| awesome-product-management | 产品管理最佳资源合集 | dend/awesome-product-management |
| open-product-management | 开放产品管理知识库 | ProductHired/open-product-management |
| unopim | 开源产品信息管理平台 | unopim/unopim |

## 核心框架体系

```
【发现阶段】
  ├── Jobs-to-be-Done (JTBD)
  ├── Problem Space → Solution Space
  ├── 5 Whys 根因分析
  └── Opportunity Solution Tree

【定义阶段】
  ├── MoSCoW 优先级法
  ├── RICE 评分框架
  ├── ICE 框架
  ├── Kano 模型
  └── 用户故事地图 (Story Mapping)

【执行阶段】
  ├── Sprint 规划
  ├── 技术评审清单
  ├── PRD 评审流程
  └── 发布检查清单

【增长阶段】
  ├── AARRR 漏斗
  ├── 增长飞轮 (Growth Loop)
  ├── PMF 评估方法
  └── 北极星指标设计

【沟通与影响力】
  ├── 向上管理技巧
  ├── 跨部门对齐方法
  ├── 产品评审会最佳实践
  └── OKR 写法规范
```

## 使用示例

```
/pm-skills 如何评估产品是否达到 PMF
/pm-skills RICE 优先级框架 --mode framework
/pm-skills 给我一个产品发布前的检查清单 --mode checklist
/pm-skills 如何向 CEO 汇报产品进展 --mode coach
/pm-skills 分析 Notion 的增长策略 --mode case
/pm-skills 用户故事映射模板 --mode template
/pm-skills AI 时代 PM 的核心技能变化
```
