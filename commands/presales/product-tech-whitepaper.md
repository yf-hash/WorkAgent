---
name: product-tech-whitepaper
description: >
  技术白皮书生成器（单一职责）— 面向技术专家 / 架构师的内部保密 Word 文档。覆盖算法原理、核心模块实现逻辑、安全机制说明，深度高于产品白皮书。仅做技术白皮书一件事，可公开的版本请用 /product-whitepaper。
user-invocable: true
argument-hint: "<产品名称> [--version v1.0] [--industry fintech|gov|healthcare|edu|mfg|retail|saas]"
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

# /product-tech-whitepaper — 技术白皮书生成器

加载技能：`skills/product/product-tech-whitepaper-writer/SKILL.md`
配套核验：`skills/presales/doc-auditor/SKILL.md`（生成后自动调用）

## 触发条件
需要编写面向客户技术团队 / 核心研发的深度技术文档，包含算法、实现机制、安全设计的内部保密资料时。

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `<产品名称>` | 产品全称（必填） | — |
| `--version` | 当前版本号 | `v1.0` |
| `--industry` | 目标行业（影响技术合规章节侧重） | — |
| `--out` | 输出路径 | `./outputs/` |

注意：本命令默认输出**内部保密**文档，封面与页眉自动加"内部资料"水印。

## 使用示例

```
/product-tech-whitepaper 数据安全网关 --version v2.0
/product-tech-whitepaper 零信任访问控制 --industry fintech
/product-tech-whitepaper 终端检测响应 --version v3.1
```

## 执行流程

```
Step 1: 信息采集
  → 必问：技术架构层级 / 关键算法 / 性能数据 / 安全机制
  → 行业相关：合规依据 / 等保 / 国密 / GDPR 等

Step 2: 结构填充
  → 加载 product-tech-whitepaper-writer 中的技术白皮书结构模板
  → 每章 ≥80% 完整草稿（剩余 20% 标注 [需补充：xxx]）
  → 算法描述需含伪代码或流程图占位

Step 3: 命名与版式
  → 文件名：[产品名]【版本号】技术白皮书_版本号.docx
  → 密级：内部保密
  → 封面 + 页眉添加"内部资料 / 禁止外传"标注

Step 4: 14 项自查（doc-auditor 自动调用）
  → 重点核查：C4 密级标注 / U1 保密归档

Step 5: 输出
  → 技术白皮书正文 + 自查报告 + 待补充清单
  → 提醒：上传至内部知识库，禁止通过公开邮件外发
```

## 与其他命令的边界

| 选择 | 用本命令 | 用其他 |
|------|---------|-------|
| `/product-tech-whitepaper` vs `/product-whitepaper` | 内部保密，深度技术 | 可公开，面向技术决策层 |
| `/product-tech-whitepaper` vs `/product-intro-tech` | Word 长文档，算法原理 | PPT 演讲材料 |
| 单份生产 vs 批量套件 | 本命令 | `@product-enablement` 编排器 |
