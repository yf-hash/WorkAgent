---
name: product-intro-business
description: >
  产品介绍-商务版 PPT 生成器（单一职责）— 面向商务决策层 / 采购委员会的可公开 PPT。
  侧重商业价值与 ROI，不讲技术细节。仅做商务版 PPT 一件事，技术版请用
  /product-intro-tech。
user-invocable: true
argument-hint: "<产品名称> [--version v1.0] [--industry fintech|gov|healthcare|edu|mfg|retail|saas]"
---

# /product-intro-business — 产品介绍-商务版 PPT 生成器

加载技能：`skills/product-intro-business-writer/SKILL.md`
配套核验：`skills/doc-auditor/SKILL.md`（生成后自动调用）

## 触发条件
需要面向客户高管 / 采购委员会做 30-45 分钟商务路演时。

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `<产品名称>` | 产品全称（必填） | — |
| `--version` | 当前版本号 | `v1.0` |
| `--industry` | 目标行业（影响价值主张） | — |
| `--out` | 输出路径 | `./outputs/` |

## 使用示例

```
/product-intro-business 数据安全网关 --industry fintech
/product-intro-business 智能运维平台 --version v2.0
```

## 执行流程

```
Step 1: 信息采集
  → 一句话定位 + 三大核心价值
  → 不超过 6 个主功能（每个配效果截图）
  → 典型客户 Logo 墙 + 3 个核心案例

Step 2: 结构填充
  → 加载 product-intro-business-writer 中的商务版模板
  → 15-25 页 PPT 草稿

Step 3: 命名与版式
  → 文件名：[产品名]【版本号】产品介绍_商务版_版本号.pptx
  → 密级：可公开

Step 4: 14 项自查（doc-auditor 自动调用）

Step 5: 输出
  → PPT 正文 + 自查报告
  → 建议下一步：技术版 PPT（深度演讲场景）
```

## 与其他命令的边界

| 选择 | 用本命令 | 用其他 |
|------|---------|-------|
| `/product-intro-business` vs `/product-intro-tech` | 商务决策层 / ROI | 技术决策层 / 架构原理 |
| `/product-intro-business` vs `/product-brochure` | PPT 演讲 | 一页纸印刷品 |
