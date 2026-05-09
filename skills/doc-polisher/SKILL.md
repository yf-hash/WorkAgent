---
name: doc-polisher
description: >
  文档智能润色技能。一键闭环：文档读取 → AI去痕 → 中文排版校正 → 智能配图 → 输出完整文档（支持 .docx 导出）。
  支持 Markdown/PDF/DOCX 输入，支持 auto/staged/iterative 三种模式和 15 种配图风格。
  触发关键词：文档润色、polish、去AI味+配图、自动配图、文档优化、导出Word、docx输出
user-invocable: false
effort: high
argument-hint: "<filepath> [--tone ...] [--intensity ...] [--style ...] [--mode auto|staged|iterative] [--export docx|md]"
---

# 文档智能润色技能

## 闭环流程

1. **文档读取**：识别 `.md/.pdf/.docx`（DOCX 读取使用 python-docx）
2. **AI 去痕**：调用 `humanizer` 技能（五源方法论，六轮改写）
3. **中文排版校正**：执行 sparanoid/chinese-copywriting-guidelines 规则（空格/标点/大小写）
4. **技术文档规范**：`--tone technical/formal` 时执行 ruanyf/document-style-guide 规范
5. **智能配图**：调用 `html-chart` / `mermaid-chart`
6. **整合输出**：生成 `*-polished.md` + `imgs/`，可选导出 `.docx`

## 模式

- `auto`：全自动，无人工介入（默认）
- `staged`：每阶段确认
- `iterative`：多稿迭代，择优输出

## 配图风格

支持 `business-blue/tender/solution/corporate/tech/cyber/data/minimal/warm/education/medical/finance/government/product-promotion/corporate-promotion`。

## DOCX 输入/输出（python-docx）

> 参考：[python-openxml/python-docx](https://github.com/python-openxml/python-docx)

**DOCX 读取**：
```python
# 自动安装依赖
pip install python-docx

# 读取流程
doc = Document(filepath)
→ 提取段落/标题/表格/图片
→ 转换为 Markdown 中间格式
→ 进入润色流程
```

**DOCX 导出**（`--export docx`）：
```python
# 润色后 Markdown → DOCX
→ 保留标题层级（Heading 1/2/3）
→ 保留表格结构
→ 嵌入生成的配图
→ 应用标准样式（Normal/Heading/Code）
→ 输出 <name>-polished.docx
```

## 中文排版自动校正

润色完成后自动执行排版校正（基于 sparanoid/chinese-copywriting-guidelines）：

- 中英文/数字之间自动加空格
- 全角标点规范化
- 专有名词大小写修正（GitHub/iOS/API 等）
- 省略号/破折号规范化

## 质量标准

- 去痕评分：50 分制（直接性/节奏/信任度/真实性/精炼度）
- 排版评分：自动校正项数量统计
- 配图评分：100 分制（信息完整性/视觉清晰度/逻辑连贯性/美观度）

## 输出结构

```
<name>-polished.md       # Markdown 格式（默认）
<name>-polished.docx     # Word 格式（--export docx 时）
imgs/
  - <name>-1.png
  - <name>-2.png
  - metadata.json
```

## 依赖

```bash
pip install python-docx pdfplumber
```
