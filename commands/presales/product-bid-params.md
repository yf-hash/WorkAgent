---
name: product-bid-params
description: >
  招投标参数生成器（单一职责）— 面向投标 / 销售的内部保密 Excel 文档。
  含完整版与精简版双套参数，按 A/B/C/D 优势分类标记。
  仅做招投标参数一件事，对外可发布的功能清单请用 /product-function-list。
user-invocable: true
argument-hint: "<产品名称> [--version v1.0] [--industry fintech|gov|healthcare|edu|mfg|retail|saas]"
---

# /product-bid-params — 招投标参数生成器

加载技能：`skills/product-writer-router/SKILL.md` + 结构模板 `templates/product/bid-params.md`
配套核验：`skills/doc-auditor/SKILL.md`（生成后自动调用）

## 触发条件
需要为标书编写、技术应答、参数对照表准备一份完整的产品技术参数库时。

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `<产品名称>` | 产品全称（必填） | — |
| `--version` | 当前版本号 | `v1.0` |
| `--industry` | 目标行业（影响行业指标侧重） | — |
| `--out` | 输出路径 | `./outputs/` |

注意：本命令默认输出**内部保密**文档，封面与页眉自动加"内部资料"水印。

## 使用示例

```
/product-bid-params 数据安全网关 --version v2.0 --industry gov
/product-bid-params 智能运维平台 --industry fintech
```

## 执行流程

```
Step 1: 信息采集
  → 必问：A/B 级排他性优势（含证据来源）
  → 总体要求 / 产品功能 / 非功能要求三大模块的指标项
  → 哪些指标在最近版本有变化（需要说明）

Step 2: 结构填充
  → 加载 templates/product/bid-params.md 中的 Excel 双版本结构
  → 生成完整版（全量参数）+ 精简版（核心指标）
  → 每条指标标 A/B/C/D 优势分类

Step 3: 命名与版式
  → 文件名：[产品名]【版本号】招投标参数_完整版_版本号.xlsx
  →       [产品名]【版本号】招投标参数_精简版_版本号.xlsx
  → 密级：内部保密
  → 封面 + 页眉添加"内部资料 / 禁止外传"标注

Step 4: 14 项自查（doc-auditor 自动调用）
  → 重点核查：C2 完整性 / C4 密级标注 / U1 保密归档

Step 5: 输出
  → 完整版 + 精简版 Excel + 自查报告
  → 提醒：上传至投标知识库，禁止公开外发
```

## 与其他命令的边界

| 选择 | 用本命令 | 用其他 |
|------|---------|-------|
| `/product-bid-params` vs `/product-function-list` | 内部投标用 / 含 A/B/C/D 分类 | 对外速查 / 不含分类 |
| `/product-bid-params` vs `/rfp-response` | 标准参数库 | 针对特定 RFP 的应答 |
| `/product-bid-params` vs `/product-competitive` | 投标参数对照 | 销售应对剧本 |
