---
name: table-from-text
description: >
  从层级文本/缩进文本生成多格式表格技能。基于 text2table，自动检测文本层级（缩进/符号），
  输出 YAML / JSON / CSV / HTML / Excel / Markdown。适合大纲/层级内容转结构化表格。
  触发词：文本转表格、text2table、层级转表格、缩进转表格、大纲转表格
user-invocable: false
effort: low
harness:
  execute:
    preset: writing-scoped
  constrain:
    profile: writing-safe
  loop:
    mode: one-shot
  memory:
    scope: project
    reads: [project-context]
  security:
    danger-level: low
---

# Table From Text — 层级文本转表格

> 单一职责：把层级/缩进文本 → 多格式表格。
> 不做：CSV/Markdown 表格互转（→ `table-csv-md`）、表格转图（→ `md-table-image`）

## 核心能力

- 自动检测文本层级（缩进/符号）
- 输出 YAML / JSON / CSV / HTML / Excel / Markdown
- TypeScript/Node.js，CLI 友好
- Excel 优化输出

## 安装与使用

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

## 输入格式示例

```
产品功能
  核心功能
    用户管理
    权限控制
  扩展功能
    数据导出
    API 集成
```

## 输出（Markdown 格式）

```markdown
| 层级 1 | 层级 2 | 层级 3 |
|--------|--------|--------|
| 产品功能 | 核心功能 | 用户管理 |
| 产品功能 | 核心功能 | 权限控制 |
| 产品功能 | 扩展功能 | 数据导出 |
| 产品功能 | 扩展功能 | API 集成 |
```

## 适用场景

- 把会议笔记/思维导图大纲 → 结构化表格
- 把代码注释中的层级文档 → 文档表
- 把组织架构文本 → 部门表
