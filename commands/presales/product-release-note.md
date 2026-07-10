---
name: product-release-note
description: >
  产品版本说明（Release Note）生成器（单一职责）— 面向全员 + 客户的可公开 PPT 或 Word。
  含版本概述、新增功能、优化改进、Bug 修复、已知问题、升级注意事项、下一版本预告
  七大章节。仅做版本说明一件事，技术细节请用 /product-tech-whitepaper。
user-invocable: true
argument-hint: "<产品名称> --version <新版本号> [--from <旧版本号>] [--format ppt|word]"
---

# /product-release-note — 产品版本说明生成器

加载技能：`skills/product-writer-router/SKILL.md` + 结构模板 `templates/product/release-note.md`
配套核验：`skills/doc-auditor/SKILL.md`（生成后自动调用）

## 触发条件
产品发布新版本，需要向全员 / 渠道 / 客户同步本次更新内容时。

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `<产品名称>` | 产品全称（必填） | — |
| `--version` | 新版本号（必填） | — |
| `--from` | 上一个版本号（用于差异说明） | — |
| `--format` | 输出格式 | `ppt` |
| `--out` | 输出路径 | `./outputs/` |

## 使用示例

```
/product-release-note 数据安全网关 --version v2.0 --from v1.5
/product-release-note 智能运维平台 --version v3.1 --from v3.0 --format word
```

## 执行流程

```
Step 1: 信息采集
  → 本版本主题（核心变化的一句话总结）
  → 新增功能清单（用户视角，非技术视角）
  → 优化改进项清单
  → Bug 修复清单（含修复编号）
  → 已知问题与规避方案
  → 升级路径与注意事项
  → 下一版本预告（高层规划，不承诺时间）

Step 2: 结构填充
  → 加载 templates/product/release-note.md 中的七章模板
  → 按变更项归类
  → 每项功能必须有用户价值描述

Step 3: 命名
  → 文件名：[产品名]【新版本号】版本说明_新版本号.[pptx|docx]
  → 密级：可公开

Step 4: 14 项自查（doc-auditor 自动调用）
  → 重点核查：C3 时效性 / F2 修订记录

Step 5: 输出
  → 版本说明 + 自查报告
  → 提醒：升级注意事项需同步到部署手册
```

## 与其他命令的边界

| 选择 | 用本命令 | 用其他 |
|------|---------|-------|
| `/product-release-note` vs `/product-whitepaper` | 版本变化 | 产品全貌 |
| `/product-release-note` vs `/product-deploy` | 升级注意事项 | 完整部署步骤 |
| `/product-release-note` vs `/product-tech-whitepaper` | 功能用户视角 | 内部技术深度 |
