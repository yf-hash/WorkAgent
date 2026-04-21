---
name: table
description: >
  表格生成与转换命令，支持文本/CSV/自然语言转 Markdown 表格，
  整合 text2table / markdown-table / mdtable / csv-markdown-tables 工具链
user-invocable: true
argument-hint: "<内容或文件> [--from text|csv|tsv|nl|md] [--to md|csv|json|excel|html] [--align l|r|c|auto] [--header true|false]"
---

# /table — 表格生成与转换

加载技能：`skills/table-toolkit/SKILL.md`

## 触发条件
需要生成 Markdown 表格、转换 CSV/TSV 数据、将层级文本转为表格，或对表格数据进行格式化时。

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `<内容或文件>` | 原始数据、文件路径或自然语言描述（必填） | — |
| `--from` | 输入格式 | `nl`（自然语言）|
| `--to` | 输出格式 | `md` |
| `--align` | 列对齐方式 | `auto` |
| `--header` | 首行是否为表头 | `true` |

### 输入格式（--from）
| 值 | 说明 | 推荐工具 |
|----|------|---------|
| `nl` | 自然语言描述 | Claude 直接生成 |
| `text` | 层级/缩进文本 | text2table |
| `csv` | CSV 格式数据 | mdtable / csv-markdown-tables |
| `tsv` | TSV（Tab分隔，Excel复制） | Markdown-Table-Generator |
| `md` | 已有 Markdown 表格（格式化/转换）| mdtable |

### 输出格式（--to）
| 值 | 说明 |
|----|------|
| `md` | GFM Markdown 表格 |
| `csv` | CSV 格式 |
| `json` | JSON 数组 |
| `excel` | Excel 文件（.xlsx）|
| `html` | HTML `<table>` |

### 对齐方式（--align）
| 值 | 说明 |
|----|------|
| `l` | 全部左对齐 |
| `r` | 全部右对齐 |
| `c` | 全部居中 |
| `auto` | 自动（数字右对齐，文字左对齐）|

---

## 执行流程

```
Step 1: 输入解析
  → 识别输入格式（--from 参数或自动检测）
  → 提取数据结构（行/列/层级）

Step 2: 工具路由
  → nl → Claude 直接生成 Markdown 表格
  → text → text2table 处理层级结构
  → csv/tsv → mdtable 或 csv-markdown-tables
  → md → 格式化/转换现有表格

Step 3: 格式化输出
  → 应用对齐方式
  → 确保 GFM 兼容性
  → 输出目标格式

Step 4: 增强选项（可选）
  → 排序（按指定列）
  → 添加汇总行
  → 标注异常值
```

---

## 与其他命令的协同

```
/table → 表格生成/转换
  ├── /md-visual --type table → 将表格转为图片
  ├── /diagram --type er      → 从表格关系生成ER图
  └── @visual-suite           → 完整视觉内容编排
```

---

## 使用示例

```bash
# 自然语言生成表格
/table 列出主流前端框架的对比：React/Vue/Angular，维度包括学习曲线/生态/性能/适用场景

# CSV 转 Markdown 表格
/table data.csv --from csv --to md

# TSV（Excel复制）转 Markdown
/table [粘贴Excel数据] --from tsv --to md

# 层级文本转表格
/table "产品功能\n  核心功能\n    用户管理\n    权限控制" --from text --to md

# Markdown 表格转 CSV
/table table.md --from md --to csv

# 生成表格并转为图片（组合命令）
/table 季度销售数据对比 --to md
# 然后：
/md-visual [上面生成的表格] --tool tablesnap

# 带对齐的表格（数字右对齐）
/table 财务数据 --from csv --align auto
```
