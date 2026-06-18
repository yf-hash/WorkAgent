---
name: diagram-uml
description: PlantUML 全系 UML 图（时序图/类图/用例图/组件图/部署图/活动图/状态图）+ JSON/YAML 可视化。
user-invocable: true
argument-hint: "<描述> [--type sequence|class|component|usecase|deployment|activity|state|json]"
allowed-tools: [Read, Write, Edit, Bash]
---

# /diagram-uml — UML 全系

加载技能：`skills/diagram-plantuml/SKILL.md`

## 用法

```bash
/diagram-uml 用户登录时序图 --type sequence
/diagram-uml 订单管理类图 --type class
```

## 与其他图表命令的边界

| 场景 | 推荐 |
|---|---|
| UML 全系 | **本命令** |
| 思维导图 | `/diagram-mindmap` |
| Mermaid 轻量流程图/甘特图 | `/mermaid-chart`（如已有命令）|
| 云架构图 | `/arch-diagram` |
