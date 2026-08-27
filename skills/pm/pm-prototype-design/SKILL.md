---
name: pm-prototype-design
description: 原型设计与逻辑校验方法论工具箱 — 供 /pm-prototype 命令调用。含页面模板库、组件类型枚举、结构化 JSON Schema、逻辑校验规则库、ASCII 线框图规范。
user-invocable: false
---

# pm-prototype-design — 原型底稿设计工具箱

> 本 skill 被 `/pm-prototype` 命令调用。

## 一、页面类型模板库

### 常见 6 种页面类型（覆盖 80% 场景）

| 类型 | 用途 | 关键组件 | 4 状态是否必须 |
|---|---|---|---|
| **表单页** | 收集数据 | Form / Input / Button | 是（含校验错误态） |
| **列表页** | 展示 + 筛选 | Table / Filter / Pagination | 是（含空态） |
| **详情页** | 查看单条 | Description / Tab / Action | 部分（数据缺失态） |
| **工作台/首页** | 功能入口 | Card / Statistic / QuickAction | 部分 |
| **流程页** | 多步操作 | Steps / FormBySection | 是（含中断态） |
| **结果页** | 反馈 | Result / Icon / Action | 否 |

## 二、组件类型枚举（结构化 JSON 用）

```
容器类：Container / Card / Panel / Modal / Drawer / Tab
展示类：Text / Title / Icon / Image / Badge / Tag / Divider
输入类：Input / Textarea / Select / DatePicker / TimePicker / Upload / Checkbox / Radio / Switch / Slider
操作类：Button / Link / Dropdown / Menu
数据类：Table / List / Description / Statistic / Progress
反馈类：Alert / Toast / Notification / Result
表单类：Form / FormItem
布局类：Grid / Flex / Space
```

## 三、结构化原型 JSON Schema（v1.0）

```json
{
  "$schema": "pm-prototype-v1",
  "topic": "string",
  "platform": "web | mobile | desktop",
  "fidelity": "low | mid",
  "generated_at": "ISO-8601",
  "pages": [
    {
      "id": "P<number>",
      "name": "string",
      "purpose": "string",
      "roles": ["string"],
      "entry_from": ["page_id or 'first_visit' or 'notification'"],
      "layout": "single-column | two-column | dashboard",
      "components": [
        {
          "type": "组件类型枚举",
          "id": "string",
          "label": "string?",
          "props": { "任意扩展属性": "..." },
          "fields": [ /* 递归组件 */ ],
          "action": {
            "type": "goto | api_call | modal | dispatch",
            "endpoint": "string?",
            "target": "page_id?",
            "on_success": "goto:page_id | close | show_toast",
            "on_error": "show_error | goto:error_page"
          },
          "required": true,
          "validation": "字符串规则或 regex"
        }
      ],
      "states": ["default", "loading", "empty", "error"],
      "transitions": [
        { "trigger": "string", "target": "page_id or 'external'" }
      ],
      "permissions": {
        "read": ["role1", "role2"],
        "write": ["role1"]
      }
    }
  ],
  "flows": {
    "main": "path/to/main.mmd",
    "exception": "path/to/exception.mmd"
  },
  "role_page_matrix": {
    "role_name": ["page_id"]
  },
  "assumptions": [
    { "text": "假设描述", "requires_confirmation": true }
  ]
}
```

## 四、逻辑校验规则库（Agent 4-2 使用）

### R1：跳转闭环
- 遍历所有 `transitions[*].target` 和 `action.target` / `action.on_success:goto:X`
- 若 target 不在 pages[*].id 中且非 `external` → ❌

### R2：异常态覆盖
- 若某组件 `action.type == "api_call"` → 该页面必须包含 `error` state
- 若某页面依赖外部服务（三方支付、AI、OAuth） → 必须画在异常流程 mermaid 中

### R3：必填项标注
- 所有 Input / Select / Upload 必须有 `required: true|false`
- 缺 required 字段 → ❌

### R4：4 状态设计
- 动态数据区域（Table / List / Statistic）必须覆盖 4 状态
- 缺 empty 或 error → ❌
- 静态展示（Text / Icon）可豁免

### R5：角色权限一致性
- `role_page_matrix` 必须与业务方案的权限矩阵一致
- 每个 page.roles 必须是 role_page_matrix 中该角色可见页
- 冲突 → ❌ 严重

### R6：返回路径
- 除首页 / 登录页外，所有页面必须有 `transitions[*].target` 指向"上一级"或"首页"
- 缺失 → ❌

### R7：孤岛页面
- 每个页面必须至少被一个其他页面的 transition 引用（或 entry_from 非空）
- 孤岛页 → ❌

### R8：字段类型合理性
- password 类型必须 `input_type: password`
- 金额、日期字段必须有合理 validation
- 违反 → ⚠️（警告，不阻断）

### R9：埋点点覆盖（可选）
- 关键动作（提交、支付、导出）必须有 `props.tracking_id`
- 缺失 → ⚠️

## 五、ASCII 线框图规范

- 最小宽度 20 字符，最大 60 字符（避免溢出）
- 使用 Unicode Box Drawing：`┌ ─ ┐ │ └ ┘`
- 必填字段用 `*` 标记
- 4 状态用注释区分：`# 默认态` / `# 空态` / `# 加载态` / `# 错误态`

示例（列表页 4 状态）：

```
# 默认态
┌──────────────────────────────┐
│ [搜索框]      [筛选] [新建]  │
├──────────────────────────────┤
│ 名称  |  状态  |  创建时间  │
│ ────  |  ────  |  ────      │
│ 项 1  |  正常  |  2026-08-01│
│ 项 2  |  异常  |  2026-08-02│
└──────────────────────────────┘

# 空态
┌──────────────────────────────┐
│      [空态插图]              │
│    还没有数据                │
│    ┌─────────────┐           │
│    │  新建第一条 │           │
│    └─────────────┘           │
└──────────────────────────────┘

# 加载态
┌──────────────────────────────┐
│    ▁▂▃▄▅▆▇  加载中...        │
└──────────────────────────────┘

# 错误态
┌──────────────────────────────┐
│  ⚠ 加载失败                  │
│  ┌───────┐                   │
│  │ 重试  │                   │
│  └───────┘                   │
└──────────────────────────────┘
```

## 六、Mermaid 流程图规范

### 主流程（sequenceDiagram）
- 参与者：用户 / 前端 / 后端 API / 数据库 / 第三方
- 每一步标注：请求 / 响应 / 存储 / 通知
- 关键判断用 `alt` / `else`

### 异常流程（sequenceDiagram + alt/else）
- 至少覆盖 5 类异常（见 pm-solution-decompose）
- 每类异常都有兜底路径

### 主流程 flowchart（顶层视图，用户看得懂）
- 圆角矩形：用户动作
- 菱形：判断
- 矩形：系统动作
- 虚线：异常跳转

## 七、输出模板

见 `commands/product/pm-prototype.md` 输出章节。
