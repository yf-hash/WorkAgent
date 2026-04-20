---
name: doc-polisher
description: >
  文档智能润色技能。一键闭环：文档读取 → AI去痕 → 智能配图 → 输出完整文档。
  支持 Markdown/PDF/DOCX，支持 auto/staged/iterative 三种模式和 15 种配图风格。
  触发关键词：文档润色、polish、去AI味+配图、自动配图、文档优化
user-invocable: false
effort: high
argument-hint: "<filepath> [--tone ...] [--intensity ...] [--style ...] [--mode auto|staged|iterative]"
---

# 文档智能润色技能

## 闭环流程

1. 文档读取：识别 `.md/.pdf/.docx`
2. AI 去痕：调用 `humanizer` 技能
3. 智能配图：调用 `html-chart` / `mermaid-chart`
4. 整合输出：生成 `*-polished.md` + `imgs/`

## 模式

- `auto`：全自动，无人工介入（默认）
- `staged`：每阶段确认
- `iterative`：多稿迭代，择优输出

## 配图风格

支持 `business-blue/tender/solution/corporate/tech/cyber/data/minimal/warm/education/medical/finance/government/product-promotion/corporate-promotion`。

## 质量标准

- 去痕评分：50 分制（直接性/节奏/信任度/真实性/精炼度）
- 配图评分：100 分制（信息完整性/视觉清晰度/逻辑连贯性/美观度）

## 输出结构

```
<name>-polished.md
imgs/
  - <name>-1.png
  - <name>-2.png
  - metadata.json
```
