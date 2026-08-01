---
name: product-solution
description: >
  产品解决方案生成器（单一职责）— 面向行业客户 / 售前对接的可公开 Word 文档（30-60 页）。
  含建设背景、建设思路、系统方案、部署模式、方案优势、建设收益、方案清单七大章节。
  仅做产品级标准解决方案一件事，针对特定客户的一次性方案请用 /proposal。
user-invocable: true
argument-hint: "<产品名称> [--industry fintech|gov|healthcare|edu|mfg|retail|saas] [--version v1.0]"
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

# /product-solution — 产品解决方案生成器

加载技能：`skills/product/product-solution-writer/SKILL.md`
配套核验：`skills/presales/doc-auditor/SKILL.md`（生成后自动调用）

## 触发条件
需要为某一行业生成标准化、可复用的产品解决方案，作为售前对接的基础物料时。

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `<产品名称>` | 产品全称（必填） | — |
| `--industry` | 目标行业（强烈推荐，影响全部内容） | — |
| `--version` | 当前版本号 | `v1.0` |
| `--out` | 输出路径 | `./outputs/` |

## 使用示例

```
/product-solution 数据安全网关 --industry fintech
/product-solution 零信任访问控制 --industry gov --version v2.0
/product-solution 智能运维平台 --industry mfg
```

## 执行流程

```
Step 1: 信息采集
  → 必问：行业监管背景 / 业务痛点排序 / 客户典型规模
  → 主功能模块清单（用于系统方案章节）
  → 典型部署架构 / 硬件配置建议
  → 行业典型案例 2-3 个

Step 2: 结构填充
  → 加载 product-solution-writer 中的七章标准结构
  → 按行业定制建设依据（法规 / 标准 / 政策引用）
  → 每章 ≥80% 完整草稿

Step 3: 命名与版式
  → 文件名：[产品名]【版本号】[行业]解决方案_版本号.docx
  → 按企业字体规范设置（黑体三号 / 宋体小四 等）
  → 密级：可公开

Step 4: 14 项自查（doc-auditor 自动调用）
  → 重点核查：C2 完整性 / C3 时效性 / F6 格式规范

Step 5: 输出
  → 解决方案 + 自查报告 + 待补充清单
  → 建议下一步：行业案例（/product-case）或客户专属提案（/proposal）
```

## 与其他命令的边界

| 选择 | 用本命令 | 用其他 |
|------|---------|-------|
| `/product-solution` vs `/proposal` | 行业标准方案，可复用 | 针对特定客户的一次性方案 |
| `/product-solution` vs `/product-whitepaper` | 含建设思路 / 部署 / 收益 | 围绕单产品的技术介绍 |
| `/product-solution` vs `/solution-architecture` | 业务+技术综合方案 | 偏纯技术架构方案 |
