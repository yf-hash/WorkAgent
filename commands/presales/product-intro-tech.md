---
name: product-intro-tech
description: >
  产品介绍-技术版 PPT 生成器（单一职责）— 面向技术决策层 / IT 负责人的可公开 PPT。
  深入技术原理、架构图、API 接口、性能指标。仅做技术版 PPT 一件事，商务版请用
  /product-intro-business。
user-invocable: true
argument-hint: "<产品名称> [--version v1.0] [--industry fintech|gov|healthcare|edu|mfg|retail|saas]"
---

# /product-intro-tech — 产品介绍-技术版 PPT 生成器

加载技能：`skills/product-intro-tech-writer/SKILL.md`
配套核验：`skills/doc-auditor/SKILL.md`（生成后自动调用）

## 触发条件
需要面向 CTO / 架构师 / IT 负责人做 45-60 分钟技术演讲时。

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `<产品名称>` | 产品全称（必填） | — |
| `--version` | 当前版本号 | `v1.0` |
| `--industry` | 目标行业 | — |
| `--out` | 输出路径 | `./outputs/` |

## 使用示例

```
/product-intro-tech 数据安全网关 --version v2.0
/product-intro-tech 零信任访问控制 --industry fintech
```

## 执行流程

```
Step 1: 信息采集
  → 系统架构图 / 关键技术选型
  → 核心 API 接口（高层）
  → 性能数据（含测试环境说明）
  → 部署模式与集成方案

Step 2: 结构填充
  → 加载 product-intro-tech-writer 中的技术版模板
  → 20-40 页 PPT 草稿

Step 3: 命名与版式
  → 文件名：[产品名]【版本号】产品介绍_技术版_版本号.pptx
  → 密级：可公开（注意：不能包含技术白皮书级别的内部细节）

Step 4: 14 项自查（doc-auditor 自动调用）

Step 5: 输出
  → PPT 正文 + 自查报告
  → 建议下一步：技术白皮书（内部深度版）
```

## 与其他命令的边界

| 选择 | 用本命令 | 用其他 |
|------|---------|-------|
| `/product-intro-tech` vs `/product-intro-business` | 技术决策层 / 架构 | 商务决策层 / ROI |
| `/product-intro-tech` vs `/product-tech-whitepaper` | PPT 可公开 | Word 内部保密 |
