---
name: product-manual
description: >
  产品操作手册生成器（单一职责）— 面向终端用户 / 运维的可公开 Word 文档。
  含快速入门、功能操作、问题处理、告警日志、附录五大章节。仅做操作手册一件事，
  部署及配置请用 /product-deploy。
user-invocable: true
argument-hint: "<产品名称> [--version v1.0]"
---

# /product-manual — 产品操作手册生成器

加载技能：`skills/product-manual-writer/SKILL.md`
配套核验：`skills/doc-auditor/SKILL.md`（生成后自动调用）

## 触发条件
需要为终端用户 / 运维提供"如何使用产品"的指引文档时。

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `<产品名称>` | 产品全称（必填） | — |
| `--version` | 当前版本号 | `v1.0` |
| `--out` | 输出路径 | `./outputs/` |

## 使用示例

```
/product-manual 数据安全网关 --version v2.0
/product-manual 智能运维平台
```

## 执行流程

```
Step 1: 信息采集
  → 主要用户角色（管理员 / 操作员 / 审计员 等）
  → 核心功能模块清单（按用户操作路径而非技术架构）
  → 高频问题清单
  → 主要告警类型

Step 2: 结构填充
  → 加载 product-manual-writer 中的五章标准结构
  → 每个功能步骤必须配截图占位（标注 [截图：xxx]）
  → 操作步骤用数字编号

Step 3: 命名与版式
  → 文件名：[产品名]【版本号】产品操作手册_版本号.docx
  → 密级：可公开

Step 4: 14 项自查（doc-auditor 自动调用）
  → 重点核查：C3 时效性（截图是否当前版本 UI）

Step 5: 输出
  → 操作手册 + 自查报告 + 待补截图清单
  → 建议下一步：部署及配置手册（/product-deploy）
```

## 与其他命令的边界

| 选择 | 用本命令 | 用其他 |
|------|---------|-------|
| `/product-manual` vs `/product-deploy` | 终端用户日常操作 | 实施工程师安装部署 |
| `/product-manual` vs `/product-training` | 自助参考手册 | 培训课件 + 实操题 |
