---
name: product-training
description: >
  产品培训材料生成器（单一职责）— 面向渠道商 / 客户 / 内部员工的可公开培训套件。
  含培训课件 PPT + 实操指南 + 培训试题。仅做培训材料一件事，单纯的产品介绍 PPT 请用
  /product-intro-business 或 /product-intro-tech。
user-invocable: true
argument-hint: "<产品名称> [--audience channel|customer|internal] [--version v1.0]"
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

# /product-training — 产品培训材料生成器

加载技能：`skills/product/product-writer-router/SKILL.md` + 结构模板 `templates/product/training.md`
配套核验：`skills/presales/doc-auditor/SKILL.md`（生成后自动调用）

## 触发条件
需要为渠道商认证培训、客户上线培训、内部员工新人培训准备一整套培训材料时。

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `<产品名称>` | 产品全称（必填） | — |
| `--audience` | 培训对象 | `internal` |
| `--version` | 当前版本号 | `v1.0` |
| `--out` | 输出路径 | `./outputs/` |

### 培训对象差异

| `--audience` | 内容侧重 |
|-------------|---------|
| `channel` | 销售场景 / 商务话术 / 案例库 / 售前流程 |
| `customer` | 操作步骤 / 业务场景 / 故障处理 / 自服务 |
| `internal` | 产品全局 / 技术原理 / 实施流程 / 升级注意事项 |

## 使用示例

```
/product-training 数据安全网关 --audience channel
/product-training 智能运维平台 --audience customer --version v2.0
```

## 执行流程

```
Step 1: 信息采集
  → 培训目标（学完能做什么）
  → 学员先决条件（需要掌握的基础知识）
  → 培训时长（半天 / 1 天 / 2 天）
  → 是否含实操环境

Step 2: 套件填充
  → 加载 templates/product/training.md 中的培训套件模板
  → 生成三件套：课件 PPT + 实操指南 Word + 试题 Word

Step 3: 命名
  → [产品名]【版本号】培训课件_[受众]_版本号.pptx
  → [产品名]【版本号】实操指南_[受众]_版本号.docx
  → [产品名]【版本号】培训试题_[受众]_版本号.docx
  → 密级：可公开

Step 4: 14 项自查（doc-auditor 自动调用）

Step 5: 输出
  → 培训三件套 + 自查报告
  → 建议下一步：版本说明（/product-release-note）
```

## 与其他命令的边界

| 选择 | 用本命令 | 用其他 |
|------|---------|-------|
| `/product-training` vs `/product-intro-business` | 培训套件（含试题 / 实操） | 单纯销售演讲 PPT |
| `/product-training` vs `/product-manual` | 课程编排 | 自助参考手册 |
