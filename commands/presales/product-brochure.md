---
name: product-brochure
description: >
  产品彩页生成器（单一职责）— A4 双面或三折页的展会 / 客户拜访宣传物料。
  仅生成产品彩页一件事，不超过 2 页图文并茂。其他文档类型见同目录其他 product-* 命令。
user-invocable: true
argument-hint: "<产品名称> [--format a4-double|trifold] [--industry fintech|gov|healthcare|edu|mfg|retail|saas]"
---

# /product-brochure — 产品彩页生成器

加载技能：`skills/product/product-writer-router/SKILL.md` + 结构模板 `templates/product/brochure.md`
配套核验：`skills/presales/doc-auditor/SKILL.md`（生成后自动调用）

## 触发条件
展会、客户拜访、商务路演等需要一份能快速传递产品价值的宣传物料时。

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `<产品名称>` | 产品全称（必填） | — |
| `--format` | 版式：A4 双面 / 三折页 | `a4-double` |
| `--industry` | 目标行业（影响亮点选择） | — |
| `--out` | 输出路径 | `./outputs/` |

## 使用示例

```
/product-brochure 数据安全网关 --format a4-double
/product-brochure 零信任访问控制 --format trifold --industry fintech
```

## 执行流程

```
Step 1: 信息采集
  → 一句话定位
  → 三大亮点（每个不超过 15 字）
  → 核心数据指标（性能 / 案例数 / 认证等）
  → 二维码 / 联系方式

Step 2: 版式填充
  → 加载 templates/product/brochure.md 中对应版式模板
  → 内容压缩到 ≤2 页

Step 3: 命名与版式
  → 文件名：[产品名]_产品彩页_v1.0.pdf
  → 密级：可公开

Step 4: 14 项自查（doc-auditor 自动调用）
  → 重点核查：F7 封面配色 / F3 标题完整性

Step 5: 输出
  → 彩页 PDF + 自查报告
  → 建议下一步：产品白皮书（深度信息承接）
```

## 与其他命令的边界

| 选择 | 用本命令 | 用其他 |
|------|---------|-------|
| `/product-brochure` vs `/product-whitepaper` | ≤2 页快速浏览 | ≥20 页深度阅读 |
| `/product-brochure` vs `/product-intro-business` | 印刷物料 | PPT 演讲材料 |
