---
name: product-whitepaper
description: >
  产品白皮书生成器（单一职责）— 面向技术负责人 / 方案架构师的可公开 Word 文档。
  覆盖产品定位、核心功能、技术架构、部署模式、产品优势、应用场景、案例的标准结构。
  生成后自动调用 doc-auditor 做 14 项自查。仅做产品白皮书一件事，其他文档类型见同目录其他 product-* 命令。
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

# /product-whitepaper — 产品白皮书生成器

加载技能：`skills/product/product-whitepaper-writer/SKILL.md`
配套核验：`skills/presales/doc-auditor/SKILL.md`（生成后自动调用）

## 触发条件
需要编写面向客户技术决策层、可公开传播的产品白皮书时。

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `<产品名称>` | 产品全称（必填） | — |
| `--version` | 当前版本号 | `v1.0` |
| `--industry` | 目标行业（影响场景章节侧重） | — |
| `--out` | 输出路径 | `./outputs/` |

### 行业定制

| `--industry` | 应用场景章节侧重 |
|--------------|------------------|
| `fintech` | 合规审计 / 风险控制 / 数据安全 |
| `gov` | 政策符合性 / 国产化 / 可控性 |
| `healthcare` | 数据合规 / 互联互通 / 稳定性 |
| `edu` | 易用性 / 扩展性 / 性价比 |
| `mfg` | 系统集成 / 工厂部署 / ROI |
| `retail` | 转化率 / 用户体验 / 数据洞察 |
| `saas` | 功能完整性 / 集成生态 / API |

## 使用示例

```
/product-whitepaper 数据安全网关 --version v2.0
/product-whitepaper 零信任访问控制 --industry fintech
/product-whitepaper 智能运维平台 --version v3.1 --industry gov
```

## 执行流程

```
Step 1: 信息采集
  → 必问：一句话定位 / 三大差异化优势 / 目标客户 / 产品形态 / 已有案例
  → 行业相关：监管背景 / 业务痛点排序

Step 2: 结构填充
  → 加载 product-whitepaper-writer 中的白皮书结构模板
  → 将采集到的产品信息填入框架
  → 每章生成 ≥80% 完整草稿（剩余 20% 标注 [需补充：xxx]）

Step 3: 命名与版式
  → 文件名：[产品名]【版本号】产品白皮书_版本号.docx
  → 添加修订记录表 + 法律声明 + 版权信息
  → 密级：可公开

Step 4: 14 项自查（doc-auditor 自动调用）
  → 输出自查报告（✅ / ⚠️ / ❌）

Step 5: 输出
  → 白皮书正文 + 自查报告 + 待补充清单
  → 建议下一份配套文档：技术白皮书（深度版）/ 产品解决方案
```

## 与其他命令的边界

| 选择 | 用本命令 | 用其他 |
|------|---------|-------|
| `/product-whitepaper` vs `/product-tech-whitepaper` | 面向技术决策层，可公开 | 面向技术专家，内部保密，深度更高 |
| `/product-whitepaper` vs `/product-solution` | 标准化产品级文档 | 面向特定行业的解决方案 |
| `/product-whitepaper` vs `/product-brochure` | ≥20 页深度内容 | A4 双面短篇宣传 |
| 单份生产 vs 批量套件 | 本命令 | `@product-enablement` 编排器 |
