---
name: table-csv-md
description: >
  CSV ↔ Markdown 表格互转技能。整合 mdtable（Python CLI 双向）+ Markdown-Table-Generator（浏览器 TSV/CSV 粘贴）+
  csv-markdown-tables（纯客户端 JS）+ markdown-table（Node.js 程序化生成）。
  适合 Excel 数据转 Markdown、批量 CSV 处理、程序化生成。
  触发词：CSV 转 Markdown、Markdown 转 CSV、TSV、Excel 数据转表格、mdtable、表格转换
user-invocable: false
effort: low
---

# Table CSV-MD — CSV/Markdown 表格互转

> 单一职责：CSV / TSV / Markdown 表格之间互转。
> 不做：层级文本 → 表格（→ `table-from-text`）、表格转图（→ `md-table-image`）

## 工具选型

| 工具 | 部署 | 适用 |
|---|---|---|
| **mdtable** | Python CLI | 双向转换、批量处理 |
| **Markdown-Table-Generator** | 浏览器 | Excel 粘贴即用 |
| **csv-markdown-tables** | 纯客户端 JS | 业务系统集成（无服务） |
| **markdown-table** | Node.js npm | 程序化生成（前端/后端） |

## mdtable — Python CLI 双向转换

```bash
pip install mdtable
# 或源码：git clone https://github.com/michelcaradec/mdtable

# CSV → Markdown
cat data.csv | python mdtable.py > table.md

# Markdown → CSV（反向）
cat table.md | python mdtable.py --reverse

# 自定义分隔符
cat data.csv | python mdtable.py --separator ";"

# 紧凑模式
cat data.csv | python mdtable.py --minify

# 批量
for f in data/*.csv; do
  cat "$f" | python mdtable.py > "docs/${f%.csv}.md"
done
```

适用：Python 环境、批量处理、CI 流水线

## Markdown-Table-Generator — 浏览器 TSV 转 Markdown

```
在线版：https://jakebathman.github.io/Markdown-Table-Generator/

工作流：
1. 在 Excel/Google Sheets 中选中数据
2. Ctrl+C 复制（自动为 TSV 格式）
3. 粘贴到工具输入框
4. 自动生成 Markdown 表格
5. 复制输出，粘贴到 Markdown 文档
```

适用：Excel 数据 → Markdown 文档的最常用场景

## csv-markdown-tables — 纯客户端 JS

```javascript
import MarkdownTablesJS from 'csv-markdown-tables'

const csv = `姓名,部门,薪资
张三,研发,25000
李四,产品,22000`

const markdown = MarkdownTablesJS.convert(csv, true)  // true = 首行表头
```

适用：业务系统集成、纯客户端无服务器

## markdown-table — Node.js npm 包

```bash
npm install markdown-table
```

```javascript
import { markdownTable } from 'markdown-table'

const table = markdownTable([
  ['产品', '价格', '库存'],
  ['iPhone 15', '¥5999', '充足'],
  ['MacBook Pro', '¥14999', '有限']
])

// 指定对齐
const aligned = markdownTable(data, { align: ['l', 'r', 'c'] })

// 紧凑模式
const custom = markdownTable(data, {
  padding: false,
  delimiterStart: false,
  delimiterEnd: false
})
```

适用：Node.js 项目程序化生成、前端动态渲染、TypeScript 项目

## 选择决策

```
输入 / 部署判断：
  ├── Excel/Google Sheets 粘贴 → Markdown-Table-Generator
  ├── Python 环境 / 批量 / 双向 → mdtable
  ├── 浏览器纯客户端 → csv-markdown-tables
  └── Node.js / 前端动态 → markdown-table
```
