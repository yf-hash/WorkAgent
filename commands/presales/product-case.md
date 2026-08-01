---
name: product-case
description: >
  产品成功案例生成器（单一职责）— 对外可发布的客户案例，3-8 页 Word 文档。
  采用 STAR 结构（背景 / 挑战 / 方案 / 成果），含客户证言。仅做成功案例一件事，
  内部赢单失单分析请用 /win-loss，其他文档类型见同目录其他 product-* 命令。
user-invocable: true
argument-hint: "<产品名称> --customer <客户名称> [--industry fintech|gov|healthcare|edu|mfg|retail|saas] [--anonymous]"
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

# /product-case — 产品成功案例生成器

加载技能：`skills/product/product-case-writer/SKILL.md`
配套核验：`skills/presales/doc-auditor/SKILL.md`（生成后自动调用）

## 触发条件
需要编写对外可发布、用于销售场景或合规验证的客户成功案例时。

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `<产品名称>` | 产品全称（必填） | — |
| `--customer` | 客户名称（必填，可后续脱敏） | — |
| `--industry` | 客户所在行业 | — |
| `--anonymous` | 隐去客户真实名称，仅保留行业描述 | `false` |
| `--out` | 输出路径 | `./outputs/` |

## 使用示例

```
/product-case 数据安全网关 --customer 某城商行 --industry fintech --anonymous
/product-case API 安全防护 --customer 招商银行 --industry fintech
/product-case 零信任访问控制 --customer 某三甲医院 --industry healthcare --anonymous
```

## 执行流程

```
Step 1: 信息采集（STAR 四要素）
  → 背景（Situation）：客户规模 / 行业 / 业务背景
  → 挑战（Task）：具体痛点 / 风险事件 / 合规压力
  → 方案（Action）：部署的产品 / 实施过程 / 关键决策
  → 成果（Result）：可量化的收益（拦截 X 次 / 节省 X 人力 / 通过 XX 认证 / 降低 X% 成本）
  → 客户证言：1-2 句话引述，含署名职务（脱敏后用"客户技术负责人"等）

Step 2: 结构填充
  → 加载 product-case-writer 中的 STAR 模板
  → 800-1500 字主体 + 关键数据可视化建议
  → 标注哪些数据需要客户授权后才能公开

Step 3: 命名与脱敏
  → 文件名：[产品名]_[客户名或行业]_成功案例_v1.0.docx
  → 脱敏模式：替换客户名为"某 [行业] 客户"，移除地址/品牌特征
  → 密级：可公开（脱敏后）

Step 4: 14 项自查（doc-auditor 自动调用）
  → 重点核查：是否包含未授权的客户名称、是否含未脱敏的内部数据

Step 5: 输出
  → 案例正文 + 自查报告 + 待客户授权清单（哪些数据需要书面授权）
  → 建议下一步：发起客户授权流程
```

## 与其他命令的边界

| 选择 | 用本命令 | 用其他 |
|------|---------|-------|
| `/product-case` vs `/win-loss` | 对外可发布的成功故事 | 内部赢单 / 失单复盘分析 |
| `/product-case` vs `/product-solution` | 单个客户的真实故事（3-8 页） | 行业级标准解决方案（30-60 页） |
| `/product-case` vs `/product-brochure` | 完整故事 + 数据 | A4 双面亮点摘要 |
| `--anonymous` 时机 | 客户未授权署名 / 行业类案例 | 客户已签授权书可用真实名称 |
