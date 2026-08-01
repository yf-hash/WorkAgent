---
name: product-function-list
description: >
  产品型号及功能清单生成器（单一职责）— Excel 表格，列出各产品型号支持的功能模块。
  面向商务 / 销售作为快速查询工具。仅做功能清单一件事，深度功能说明请用
  /product-whitepaper。
user-invocable: true
argument-hint: "<产品名称> [--version v1.0]"
allowed-tools: [Read, Write, Edit, Grep, Glob, AskUserQuestion]
harness:
  execute:
    preset: writing-scoped
  constrain:
    profile: writing-safe
    gates: [before-write]
  loop:
    mode: one-shot
  memory:
    scope: project
    reads: [project-context]
  security:
    danger-level: medium
---

# /product-function-list — 产品型号及功能清单生成器

加载技能：`skills/product/product-writer-router/SKILL.md` + 结构模板 `templates/product/function-list.md`
配套核验：`skills/presales/doc-auditor/SKILL.md`（生成后自动调用）

## 触发条件
需要快速查询某产品有哪些型号 / 各型号支持哪些功能 / 适用什么规模时。

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `<产品名称>` | 产品全称（必填） | — |
| `--version` | 当前版本号 | `v1.0` |
| `--out` | 输出路径 | `./outputs/` |

## 使用示例

```
/product-function-list 数据安全网关 --version v2.0
/product-function-list 智能运维平台
```

## 执行流程

```
Step 1: 信息采集
  → 产品型号清单（基础版 / 专业版 / 旗舰版 / 行业版 等）
  → 每个型号的适用规模（用户数 / 数据量 / 并发等）
  → 功能模块清单（按一级 / 二级模块）
  → 各功能在各型号中的支持情况

Step 2: 表格生成
  → 加载 templates/product/function-list.md 中的标准 Excel 结构
  → 形成型号-功能矩阵

Step 3: 命名
  → 文件名：[产品名]【版本号】产品型号及功能清单_版本号.xlsx
  → 密级：可公开

Step 4: 14 项自查（doc-auditor 自动调用）
  → 重点核查：C2 完整性（避免漏型号 / 漏功能）

Step 5: 输出
  → Excel 清单 + 自查报告
```

## 与其他命令的边界

| 选择 | 用本命令 | 用其他 |
|------|---------|-------|
| `/product-function-list` vs `/product-whitepaper` | 速查表 / 矩阵对比 | 深度功能说明 |
| `/product-function-list` vs `/product-bid-params` | 公开速查 | 内部投标参数对照 |
