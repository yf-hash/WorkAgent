---
name: diagram-plantuml
description: >
  PlantUML 引擎技能。覆盖 UML 全系（时序图/类图/用例图/组件图/部署图/活动图/对象图/状态图）
  以及 JSON/YAML 可视化。Java 驱动，最全面的 UML 支持。
  触发词：PlantUML、UML、时序图、类图、用例图、组件图、部署图、活动图、JSON 可视化
user-invocable: false
effort: medium
---

# Diagram PlantUML — UML 全系

> 单一职责：用 PlantUML 生成 UML 各类图表。
> 不做：思维导图（→ `diagram-markmap`）、轻量流程图（→ `mermaid-chart`）、云架构图（→ `arch-diagram`）

## 适用场景

- 软件架构设计文档
- 系统交互说明
- 数据库设计
- 业务流程规范化

## 图表类型与语法

### 时序图（Sequence）

```plantuml
@startuml
actor 用户
participant "前端" as FE
participant "后端 API" as BE
database "数据库" as DB

用户 -> FE: 登录请求
FE -> BE: POST /auth/login
BE -> DB: 查询用户
DB --> BE: 返回用户信息
BE --> FE: JWT Token
FE --> 用户: 登录成功
@enduml
```

### 类图（Class）

```plantuml
@startuml
class User {
  +id: Long
  +name: String
  +email: String
  +login(): Boolean
}
class Order {
  +id: Long
  +amount: Decimal
  +status: String
}
User "1" --> "many" Order : 创建
@enduml
```

### 组件/架构图（Component）

```plantuml
@startuml
package "前端层" {
  [Web App]
  [Mobile App]
}
package "服务层" {
  [API Gateway]
  [Auth Service]
  [Business Service]
}
database "数据层" {
  [MySQL]
  [Redis]
}
[Web App] --> [API Gateway]
[Mobile App] --> [API Gateway]
[API Gateway] --> [Auth Service]
[API Gateway] --> [Business Service]
[Business Service] --> [MySQL]
[Business Service] --> [Redis]
@enduml
```

### JSON/YAML 可视化

```plantuml
@startjson
{
  "name": "产品配置",
  "version": "1.0",
  "features": ["功能 A", "功能 B"],
  "config": {
    "timeout": 30,
    "retry": 3
  }
}
@endjson
```

## 渲染方式

```bash
# 方式 1：在线渲染
# https://www.plantuml.com/plantuml/uml/

# 方式 2：本地 JAR
java -jar plantuml.jar diagram.puml        # 生成 PNG
java -jar plantuml.jar -tsvg diagram.puml  # 生成 SVG
java -jar plantuml.jar -tpdf diagram.puml  # 生成 PDF

# 方式 3：VSCode 插件
# 安装 "PlantUML" 插件，Alt+D 预览
```

## 质量基线

```
✓ 时序图：参与者 ≤ 6 个，消息 ≤ 15 条
✓ 类图：单类方法 ≤ 10 个，关系明确（继承/聚合/组合）
✓ 组件图：分层清晰（前端/服务/数据），依赖方向一致
✓ 中文标签，技术词保留英文
```
