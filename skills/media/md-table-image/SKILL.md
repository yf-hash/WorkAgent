---
name: md-table-image
description: >
  Markdown 表格转 PNG 图片技能。整合 tablesnap（Go CLI，emoji 支持，深浅主题）+
  markdown-table-imagifier（浏览器端，纯客户端无服务）+ markdown-table-to-image（Flask API，动态尺寸）。
  适合 CI/CD 自动化、隐私敏感场景、API 服务。
  触发词：表格转图片、tablesnap、表格截图、md 表格 PNG、markdown table image
user-invocable: false
effort: low
harness:
  execute:
    preset: media-heavy
  constrain:
    profile: shell-restricted
  loop:
    mode: one-shot
  memory:
    scope: session
    reads: [project-context]
  security:
    danger-level: medium
---

# MD Table Image — Markdown 表格转图

> 单一职责：把 Markdown 表格渲染成 PNG 图片。
> 不做：长文海报（→ `md-poster`）、表格生成本身（→ `table-from-text` / `table-csv-md`）

## 工具选型

| 工具 | 部署 | 适用 |
|---|---|---|
| **tablesnap** | Go CLI | CI/CD 自动化、命令行管道 |
| **markdown-table-imagifier** | 浏览器端 | 临时需求、隐私敏感（数据不离本地） |
| **markdown-table-to-image** | Flask API | 需要 API 服务集成 |

## tablesnap — CLI 命令行

```bash
# 安装
go install github.com/joargp/tablesnap/cmd/tablesnap@latest

# 管道输入
echo "| 姓名 | 部门 | 薪资 |
|------|------|------|
| 张三 | 研发 | 25k |
| 李四 | 产品 | 22k |" | tablesnap > table.png

# 从文件读取
cat data.md | tablesnap > output.png

# 深色主题
cat data.md | tablesnap --theme dark > output.png

# 指定输出路径
cat data.md | tablesnap -o ./imgs/table.png
```

特性：
- emoji 支持（Twemoji）
- 深色/浅色主题
- Go 编写，跨平台，无依赖

适用：CI/CD 自动化、批量处理脚本、报告生成

## markdown-table-imagifier — 浏览器端

```
在线版：https://fahdi.github.io/markdown-table-imagifier/

本地部署：
git clone https://github.com/fahdi/markdown-table-imagifier
# 直接用浏览器打开 index.html
```

特性：
- 纯客户端，无需服务器
- 实时预览
- 可直接下载

适用：临时需求、数据隐私敏感、简单表格快速转换

## markdown-table-to-image — Flask API

```bash
git clone https://github.com/fahdi/markdown-table-to-image
pip install flask pillow
python app.py
# 访问 http://127.0.0.1:5000/

# API 调用
curl -X POST http://127.0.0.1:5000/convert \
  -H "Content-Type: application/json" \
  -d '{"table": "| A | B |\n|---|---|\n| 1 | 2 |"}'
```

特性：
- 动态尺寸（自适应内容）
- 文字自动换行
- 输出 PNG

适用：需要嵌入业务系统的 API 服务

## 选择决策

```
使用场景判断：
  ├── 命令行 / CI 流水线 → tablesnap
  ├── 浏览器即用即走（隐私）→ markdown-table-imagifier
  └── 需要 HTTP API → markdown-table-to-image
```
