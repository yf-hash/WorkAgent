---
name: product-competitive
description: >
  竞品分析生成器（单一职责）— 面向销售 / 售前的内部保密 PPT。
  含 A/B/C/D 四级优势分类、功能对比矩阵、D 级应对话术、竞争应对剧本。
  仅做竞品分析一件事，单个对手的一页纸作战卡请用 /battle-card。
user-invocable: true
argument-hint: "<产品名称> [--competitors <对手1,对手2,对手3>] [--industry fintech|gov|healthcare|edu|mfg|retail|saas]"
---

# /product-competitive — 竞品分析生成器

加载技能：`skills/product-writer-router/SKILL.md` + 结构模板 `templates/product/competitive.md`
配套核验：`skills/doc-auditor/SKILL.md`（生成后自动调用）

## 触发条件
需要系统性盘点本产品与 3-5 个核心竞品的优劣势，并形成销售应对剧本时。

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `<产品名称>` | 我方产品全称（必填） | — |
| `--competitors` | 对手清单（3-5 家，逗号分隔，必填） | — |
| `--industry` | 目标客户行业 | — |
| `--out` | 输出路径 | `./outputs/` |

注意：本命令默认输出**内部保密**文档，封面与页眉自动加"内部资料"水印。

## 使用示例

```
/product-competitive 数据安全网关 --competitors 厂商A,厂商B,厂商C
/product-competitive 零信任访问控制 --competitors 对手X,对手Y --industry fintech
```

## 执行流程

```
Step 1: 信息采集
  → 必问：对手 3-5 家 / 各自核心卖点 / 各自典型客户 / 与我方主要遭遇场景
  → 我方 A/B 级排他性优势是什么
  → 我方 D 级劣势在哪里

Step 2: 结构填充
  → 加载 templates/product/competitive.md 中的竞品分析结构
  → 形成 A/B/C/D 四级优势分类矩阵
  → 为每个 D 级劣势准备应对话术

Step 3: 命名与版式
  → 文件名：[产品名]_竞品分析_v1.0.pptx
  → 密级：内部保密
  → 封面 + 页眉添加"内部资料 / 禁止外传"标注

Step 4: 14 项自查（doc-auditor 自动调用）
  → 重点核查：C4 密级标注 / U1 保密归档

Step 5: 输出
  → 竞品分析 PPT + 自查报告
  → 建议下一步：单个对手深度作战卡（/battle-card）
```

## 与其他命令的边界

| 选择 | 用本命令 | 用其他 |
|------|---------|-------|
| `/product-competitive` vs `/battle-card` | 3-5 家系统盘点 / PPT | 单个对手一页纸 / 销售随身卡 |
| `/product-competitive` vs `/product-bid-params` | 销售应对剧本 | 投标技术参数对照 |
| `/product-competitive` vs `/win-loss` | 事前竞争盘点 | 事后赢单 / 失单复盘 |
