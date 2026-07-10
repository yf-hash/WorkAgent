---
name: product-sales-faq
description: >
  销售常见问题（FAQ）生成器（单一职责）— 面向销售 / 售前的可公开 Word 文档。
  覆盖技术原理、竞品对比、部署运维、价格授权、服务支持五大类常见问答。
  仅做销售 FAQ 一件事，完整销售一页禅请用 /sales-guide。
user-invocable: true
argument-hint: "<产品名称> [--version v1.0] [--industry fintech|gov|healthcare|edu|mfg|retail|saas]"
---

# /product-sales-faq — 销售常见问题生成器

加载技能：`skills/product-writer-router/SKILL.md` + 结构模板 `templates/product/sales-faq.md`
配套核验：`skills/doc-auditor/SKILL.md`（生成后自动调用）

## 触发条件
需要为销售在客户现场提供高频问题的标准应答库时。

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `<产品名称>` | 产品全称（必填） | — |
| `--version` | 当前版本号 | `v1.0` |
| `--industry` | 目标行业（影响问题类型） | — |
| `--out` | 输出路径 | `./outputs/` |

## 使用示例

```
/product-sales-faq 数据安全网关 --version v2.0
/product-sales-faq 零信任访问控制 --industry fintech
```

## 执行流程

```
Step 1: 信息采集
  → 五大类问题各列举至少 3 个高频问题：技术原理 / 竞品对比 / 部署运维 / 价格授权 / 服务支持
  → 已知销售在客户现场被问倒的问题
  → 行业特殊关注的合规问题

Step 2: 结构填充
  → 加载 templates/product/sales-faq.md 中的标准问答结构
  → 每个 FAQ = 问题标题 + 标准应答（含话术）
  → 应答控制在 100-200 字，可口语表达

Step 3: 命名
  → 文件名：[产品名]【版本号】销售常见问题_版本号.docx
  → 密级：可公开

Step 4: 14 项自查（doc-auditor 自动调用）
  → 重点核查：C2 完整性（五大类是否齐全）/ C3 时效性

Step 5: 输出
  → FAQ 文档 + 自查报告
  → 建议下一步：完整销售一页禅（/sales-guide）
```

## 与其他命令的边界

| 选择 | 用本命令 | 用其他 |
|------|---------|-------|
| `/product-sales-faq` vs `/sales-guide` | 单独 FAQ 文档 | 完整销售一页禅（含场景 / 对比） |
| `/product-sales-faq` vs `/product-competitive` | 客户高频问答 | 系统化竞品对比 |
