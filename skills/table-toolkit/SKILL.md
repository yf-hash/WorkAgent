---
name: table-toolkit
description: >
  表格生成与转换工具集。触发词：文本转表格、表格生成、CSV转Markdown、Markdown表格、
  text2table、markdown-table、表格格式化、层级文本转表格、数据表格、
  TSV转Markdown、表格对齐、表格工具。
  整合 text2table / markdown-table / Markdown-Table-Generator / csv-markdown-tables / mdtable。
user-invocable: false
effort: low
---

# Table Toolkit — 表格生成与转换工具集

> 整合来源：
> - text2table（层级文本 → 多格式，含Markdown）
> - markdown-table（JS库，程序化生成GFM表格）
> - Markdown-Table-Generator（浏览器TSV/CSV → Markdown）
> - csv-markdown-tables（客户端CSV → Markdown）
> - mdtable（Python CLI，CSV ↔ Markdown 双向转换）

---

## 一、工具选型速查

| 工具 | 输入 | 输出 | 适用场景 |
|------|------|------|---------|
| **text2table** | 层级文本/缩进文本 | YAML/JSON/CSV/HTML/Excel/Markdown | 将大纲/层级内容转为结构化表格 |
| **markdown-table** | JS数组/矩阵 | GFM Markdown表格 | 程序化生成表格（Node.js/前端） |
| **MD-Table-Generator** | TSV/CSV（浏览器粘贴） | Markdown表格 | 快速将Excel数据转为Markdown |
| **csv-markdown-tables** | CSV文本 | Markdown表格 | 纯客户端，无需服务器 |
| **mdtable** | CSV文件 / Markdown表格 | Markdown表格 / CSV（双向） | Python脚本/命令行处理 |

---

## 二、text2table — 层级文本转多格式

### 核心能力
- 自动检测文本层级（缩进/符号）
- 输出 YAML / JSON / CSV / HTML / Excel / Markdown
- TypeScript/Node.js，CLI 友好
- Excel 优化输出

### 安装与使用
```bash
# 安装
npm install -g text2table
# 或 npx 直接使用

# 基础用法
npx text2table -i input.txt -f markdown

# 指定输出格式
npx text2table -i data.txt -f csv -o output.csv
npx text2table -i data.txt -f excel -o output.xlsx
npx text2table -i data.txt -f json -o output.json

# 支持的格式：yaml / json / csv / html / excel / markdown
```

### 输入格式示例
```
产品功能
  核心功能
    用户管理
    权限控制
  扩展功能
    数据导出
    API集成
```

### 输出（Markdown格式）
```markdown
| 层级1 | 层级2 | 层级3 |
|-------|-------|-------|
| 产品功能 | 核心功能 | 用户管理 |
| 产品功能 | 核心功能 | 权限控制 |
| 产品功能 | 扩展功能 | 数据导出 |
| 产品功能 | 扩展功能 | API集成 |
```

---

## 三、markdown-table — 程序化表格生成（JS库）

### 核心能力
- 轻量 ESM 包
- 从数组/矩阵生成 GFM 标准 Markdown 表格
- 支持列对齐（左/右/居中）
- TypeScript 类型支持

### 安装与使用
```bash
npm install markdown-table
```

```javascript
import { markdownTable } from 'markdown-table'

// 基础用法
const table = markdownTable([
  ['产品', '价格', '库存'],
  ['iPhone 15', '¥5999', '充足'],
  ['MacBook Pro', '¥14999', '有限'],
  ['AirPods', '¥1299', '充足']
])
console.log(table)
// 输出：
// | 产品        | 价格    | 库存 |
// | ----------- | ------- | ---- |
// | iPhone 15   | ¥5999   | 充足 |
// | MacBook Pro | ¥14999  | 有限 |
// | AirPods     | ¥1299   | 充足 |

// 指定对齐方式
const aligned = markdownTable(data, {
  align: ['l', 'r', 'c']  // 左/右/居中
})

// 自定义填充字符
const custom = markdownTable(data, {
  padding: false,  // 不填充空格（紧凑模式）
  delimiterStart: false,  // 不加首尾 |
  delimiterEnd: false
})
```

---

## 四、Markdown-Table-Generator — 浏览器TSV转Markdown

### 核心能力
- 浏览器端，无需安装
- 支持 TSV（Tab分隔）和 CSV 输入
- 实时预览
- 一键复制输出

### 使用方式
```
在线版：https://jakebathman.github.io/Markdown-Table-Generator/

工作流：
1. 在 Excel/Google Sheets 中选中数据
2. Ctrl+C 复制（自动为 TSV 格式）
3. 粘贴到工具输入框
4. 自动生成 Markdown 表格
5. 复制输出，粘贴到 Markdown 文档
```

### 适用场景
```
Excel数据 → Markdown文档：最常用场景
Google Sheets → GitHub README：快速生成数据表格
会议记录表格 → 技术文档：格式转换
```

---

## 五、csv-markdown-tables — 纯客户端CSV转Markdown

### 核心能力
- 纯 JavaScript，无服务器
- CSV 文本 → Markdown 表格
- 支持首行作为表头

### API 使用
```javascript
// 引入库
import MarkdownTablesJS from 'csv-markdown-tables'

// 基础转换
const csv = `姓名,部门,薪资
张三,研发,25000
李四,产品,22000
王五,设计,20000`

const markdown = MarkdownTablesJS.convert(csv, true)  // true = 首行为表头
console.log(markdown)
// 输出：
// | 姓名 | 部门 | 薪资  |
// |------|------|-------|
// | 张三 | 研发 | 25000 |
// | 李四 | 产品 | 22000 |
// | 王五 | 设计 | 20000 |
```

---

## 六、mdtable — Python CLI 双向转换

### 核心能力
- CSV → Markdown 表格
- Markdown 表格 → CSV（双向）
- 支持自定义分隔符
- 支持紧凑输出（minified）

### 安装与使用
```bash
# 安装
pip install mdtable
# 或直接使用源码
git clone https://github.com/michelcaradec/mdtable

# CSV → Markdown
cat data.csv | python mdtable.py
cat data.csv | python mdtable.py > table.md

# Markdown → CSV（反向转换）
cat table.md | python mdtable.py --reverse

# 自定义分隔符
cat data.csv | python mdtable.py --separator ";"

# 紧凑模式（不填充空格）
cat data.csv | python mdtable.py --minify
```

### 批量处理脚本
```bash
# 将目录下所有 CSV 转为 Markdown
for f in data/*.csv; do
  cat "$f" | python mdtable.py > "docs/${f%.csv}.md"
done
```

---

## 七、Claude 辅助生成表格内容

### 从自然语言生成 Markdown 表格
```
请将以下信息整理为 Markdown 表格：

[自然语言描述的数据]

要求：
- 列名简洁（≤6字）
- 数据对齐（数字右对齐，文字左对齐）
- 不超过 [N] 列
```

### 从非结构化文本提取表格
```
请从以下文本中提取结构化数据，生成 Markdown 表格：

[非结构化文本]

提取维度：[维度1] / [维度2] / [维度3]
```

### 表格数据增强
```
请为以下 Markdown 表格：
1. 添加排序（按 [列名] 降序）
2. 添加汇总行
3. 标注异常值（用 **加粗** 标记）

[原始表格]
```

---

## 八、场景决策树

```
需要生成/转换表格
  │
  ├── 输入是层级文本/大纲？
  │   → text2table（支持多种输出格式）
  │
  ├── 输入是 Excel/Google Sheets 数据？
  │   → Markdown-Table-Generator（浏览器粘贴即用）
  │
  ├── 输入是 CSV 文件？
  │   ├── Python 环境 → mdtable（CLI，支持双向）
  │   └── 浏览器环境 → csv-markdown-tables（纯客户端）
  │
  ├── 需要程序化生成（Node.js/前端项目）？
  │   → markdown-table（npm包，API调用）
  │
  └── 需要将表格转为图片？
      → 参考 md-visual skill（tablesnap / table-imagifier）
```
