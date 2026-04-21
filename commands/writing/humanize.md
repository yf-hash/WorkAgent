---
allowed-tools: Read, Write, Edit, Bash, AskUserQuestion
description: AI 文本人性化改写 — 识别 40+ 种 AI 写作痕迹，去除 AI 生成痕迹，让文本更自然真实
argument-hint: "[filepath|text] [--tone casual|formal|technical|academic] [--intensity low|medium|high|max]"
---

# /humanize

AI 文本人性化改写。识别并去除 AI 生成痕迹，让文字读起来像真实人类作者的风格。

## 用法

```
/humanize [文件路径或直接粘贴文本]
/humanize article.md --tone casual --intensity high
/humanize thesis.pdf --tone academic --intensity max
/humanize report.docx --tone formal --intensity medium
```

## 参数说明

| 参数 | 选项 | 默认值 | 说明 |
|------|------|--------|------|
| `--tone` | `casual` / `formal` / `technical` / `academic` | `formal` | 语调风格 |
| `--intensity` | `low` / `medium` / `high` / `max` | `medium` | 去痕强度 |

### 语调说明

| 语调 | 去痕强度 | 适用场景 |
|------|----------|----------|
| `casual` | 90% | 博客、营销文案、社交媒体 |
| `formal` | 70% | 商业报告、政府文件 |
| `technical` | 60% | 技术文档、API 文档 |
| `academic` | 80-90% | 学术论文、期刊投稿 |

### 强度说明

| 强度 | 百分比 | 适用场景 |
|------|--------|----------|
| `low` | 40-50% | 内部文档、草稿快速优化 |
| `medium` | 60-70% | 技术文档、正式报告、博客 |
| `high` | 75-85% | 重要文档、学术论文（一般） |
| `max` | 85-95% | 顶刊投稿、学位论文、严格检测 |

## 执行流程

加载 `skills/humanizer/SKILL.md` 完整规范执行：

1. 接收输入（文件路径或直接文本）
2. 识别 40+ 种 AI 写作痕迹（内容/语言/风格/交流/学术五类）
3. 按语调和强度应用改写策略（基础 10 条 + 进阶 13 条 + 学术高级技术）
4. 输出改写结果 + 修改说明 + 五维度质量评分（总分 50）

## 支持格式

`.md` / `.txt` — 直接读取；`.docx` — 需 python-docx；`.pdf` — 需 pdfplumber（首次自动安装）

## 输出格式

```
## 改写结果

### 1. 改写后的文本
[完整改写内容]

### 2. 主要修改说明
删除的 AI 痕迹：[具体列表]
应用的改写策略：[具体列表]

### 3. 质量评分
| 维度 | 得分 | 说明 |
|------|------|------|
| 直接性 | X/10 | |
| 节奏   | X/10 | |
| 信任度 | X/10 | |
| 真实性 | X/10 | |
| 精炼度 | X/10 | |
| 总分   | XX/50 | |
```

## 相关命令

- `/polish` — AI 去痕 + 自动配图一键闭环
- `/article-writer` — 文章风格公众号长文写作
