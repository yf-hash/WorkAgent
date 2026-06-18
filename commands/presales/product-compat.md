---
name: product-compat
description: >
  兼容性支持文档生成器（单一职责）— 面向集成商 / 实施工程师的可公开 Word 文档。
  按平台矩阵呈现对 OS / 数据库 / 中间件 / 云平台的支持情况。仅做兼容性文档一件事，
  部署步骤请用 /product-deploy。
user-invocable: true
argument-hint: "<产品名称> [--version v1.0]"
---

# /product-compat — 兼容性支持文档生成器

加载技能：`skills/product-compat-writer/SKILL.md`
配套核验：`skills/doc-auditor/SKILL.md`（生成后自动调用）

## 触发条件
需要为集成商 / 实施工程师快速查询"本产品在 X 平台上是否经过测试可用"时。

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `<产品名称>` | 产品全称（必填） | — |
| `--version` | 当前版本号 | `v1.0` |
| `--out` | 输出路径 | `./outputs/` |

## 使用示例

```
/product-compat 数据安全网关 --version v2.0
/product-compat 智能运维平台
```

## 执行流程

```
Step 1: 信息采集
  → OS 兼容矩阵（含国产 OS：麒麟、统信、欧拉、龙蜥）
  → 数据库矩阵（含国产 DB：达梦、人大金仓、神通、瀚高、TiDB）
  → 中间件矩阵
  → 云平台矩阵
  → CPU 架构（x86_64 / ARM / MIPS / 龙芯）
  → 浏览器矩阵
  → 测试结果与测试日期

Step 2: 矩阵填充
  → 加载 product-compat-writer 中的矩阵模板
  → 用 ✅ / ⚠️ / ✗ 标记测试结果

Step 3: 命名与版式
  → 文件名：[产品名]【版本号】兼容性支持文档_版本号.docx
  → 密级：可公开

Step 4: 14 项自查（doc-auditor 自动调用）
  → 重点核查：C3 时效性（测试日期是否过期 > 6 个月）

Step 5: 输出
  → 兼容性文档 + 自查报告
  → 建议下一步：部署及配置手册（/product-deploy）
```

## 与其他命令的边界

| 选择 | 用本命令 | 用其他 |
|------|---------|-------|
| `/product-compat` vs `/product-deploy` | 平台支持矩阵 | 部署步骤 |
| `/product-compat` vs `/product-function-list` | 平台兼容性 | 型号功能矩阵 |
