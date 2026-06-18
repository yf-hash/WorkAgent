---
name: doc-formatter
description: >
  文档格式化技能 — DOCX 读写 + 中文排版校正模块。负责 .docx 文件的读取解析、
  中文排版规范化（中英文空格/标点/大小写）、技术文档规范校正、以及最终的 DOCX 格式导出。
  作为 doc-polisher agent 的格式化子模块调用，也可独立用于排版校正场景。
  触发关键词：DOCX格式导出、word导出、中文排版、排版校正、docx输出、导出Word、
  chinese typography、copywriting guidelines
user-invocable: false
effort: medium
argument-hint: "<filepath> [--tone technical|formal] [--export docx|md]"
---

# 文档格式化技能

文档 DOCX 读写与中文排版规范化模块。被 `doc-polisher` agent 在润色流程后调用，
也可独立运行进行纯排版校正。

---

## 职责范围

本技能专注于**格式化**部分，不执行 AI 去痕或配图生成（由 `humanizer-scan` / `humanizer-soul` 和 `html-chart` 负责）：

1. **DOCX 文件解析**：读取 `.docx` 文件，转换为 Markdown 中间格式
2. **中文排版校正**：执行 sparanoid/chinese-copywriting-guidelines 规则
3. **技术文档规范**：`--tone technical/formal` 时执行 ruanyf/document-style-guide
4. **DOCX 格式导出**：将 Markdown 内容转换回 `.docx` 并保留结构

---

## DOCX 读取（python-docx）

> 参考：[python-openxml/python-docx](https://github.com/python-openxml/python-docx)

```python
pip install python-docx pdfplumber

# 读取流程
doc = Document(filepath)
→ 提取段落/标题/表格/图片
→ 转换为 Markdown 中间格式
→ 进入后续处理流程
```

---

## 中文排版自动校正

基于 [sparanoid/chinese-copywriting-guidelines](https://github.com/sparanoid/chinese-copywriting-guidelines)：

| 规则 | 示例（错误 → 正确） |
|------|-------------------|
| 中英文之间加空格 | `AI技术` → `AI 技术` |
| 中文与数字之间加空格 | `3个月` → `3 个月` |
| 全角标点规范化 | `，。！` 优于 `,.!` |
| 专有名词大小写 | `github` → `GitHub`，`ios` → `iOS` |
| 省略号规范化 | `...` → `……` |
| 破折号规范化 | `--` → `——` |

技术文档附加规范（`--tone technical/formal` 时，基于 [ruanyf/document-style-guide](https://github.com/ruanyf/document-style-guide)）：
- 中文句子内不使用全角括号，改用半角 `( )`
- 避免在代码块中使用全角字符
- API/命令名称不加引号，直接使用 code 格式

---

## DOCX 导出（`--export docx`）

```python
# 润色/处理后 Markdown → DOCX
→ 保留标题层级（Heading 1/2/3）
→ 保留表格结构
→ 嵌入生成的配图
→ 应用标准样式（Normal/Heading/Code）
→ 输出 <name>-polished.docx
```

---

## 输出结构

```
<name>-polished.md       # Markdown 格式（默认）
<name>-polished.docx     # Word 格式（--export docx 时）
imgs/
  - <name>-1.png
  - <name>-2.png
  - metadata.json
```

---

## 排版质量报告

排版校正完成后输出统计：

```
排版自动校正报告
├── 中英文空格修正：X 处
├── 全角标点规范化：X 处
├── 专有名词大小写修正：X 处（GitHub/iOS/API 等）
├── 省略号/破折号规范化：X 处
└── 技术文档规范修正（如适用）：X 处
```

---

## 依赖

```bash
pip install python-docx pdfplumber
```
