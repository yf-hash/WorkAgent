---
allowed-tools: Read, Write, Edit, Bash, AskUserQuestion, Skill
description: 文档智能润色 — AI 去痕 + 自动配图一键闭环，输入 Markdown/PDF/DOCX，自动完成人性化改写和专业配图生成
argument-hint: "<filepath> [--tone casual|formal|technical|academic] [--intensity low|medium|high|max] [--style <风格>] [--mode auto|staged|iterative] [--output <路径>]"
---

# /polish

文档智能润色。一条命令，四步自动完成：读取 → AI 去痕 → 配图生成 → 输出完整文档。

## 用法

```
# 一键全自动（推荐）
/polish article.md

# 学术论文（最高强度去痕 + 商务配图）
/polish thesis.pdf --tone academic --intensity max --style business-blue

# 技术文档（中等强度 + 科技风格）
/polish tech-doc.md --tone technical --intensity medium --style tech

# 商业报告（需精细控制时用阶段确认）
/polish report.docx --tone formal --mode staged --style tender
```

## 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--tone` | `formal` | 语调：casual/formal/technical/academic |
| `--intensity` | `medium` | 去痕强度：low/medium/high/max |
| `--style` | `business-blue` | 配图风格（15种，见下表） |
| `--mode` | `auto` | 运行模式：auto/staged/iterative |
| `--output` | 自动生成 | 输出路径（默认：原文件名-polished） |

## 配图风格（15种）

| 风格 ID | 适用场景 | 配色特点 |
|---------|----------|----------|
| `business-blue` | PPT、商业报告 | 深蓝+纯白，专业清爽 |
| `tender` | 投标文件、政府项目 | 深蓝+金色，权威高端 |
| `solution` | 技术方案、架构设计 | 深灰+科技蓝，专业清晰 |
| `corporate` | 年度报告、战略规划 | 深蓝+银灰，稳重高级 |
| `tech` | AI、编程、技术博客 | 蓝紫渐变，现代创新 |
| `cyber` | 网络安全、黑客主题 | 霓虹绿+深色，科技酷炫 |
| `data` | 数据报告、BI 分析 | 多彩渐变，数据可视化 |
| `minimal` | 教程、说明文档 | 黑白灰，简洁易读 |
| `warm` | 个人成长、情感故事 | 橙黄暖色，友好亲切 |
| `education` | 课程材料、培训文档 | 蓝绿色，清新活力 |
| `medical` | 医疗报告、健康文档 | 医疗蓝+白，专业可信 |
| `finance` | 财务报告、投资分析 | 深绿+金色，稳重高端 |
| `government` | 政府文件、公文材料 | 国旗红+蓝，正式庄重 |
| `product-promotion` | 产品介绍、营销材料 | 活力橙+蓝，吸引眼球 |
| `corporate-promotion` | 企业介绍、品牌宣传 | 品牌蓝+黄，专业活力 |

## 运行模式

| 模式 | 说明 | 适用场景 |
|------|------|----------|
| `auto` | 全自动闭环（推荐），无需人工干预 | 日常文档、快速处理 |
| `staged` | 每个阶段暂停确认 | 重要文档、精细控制 |
| `iterative` | 每张图生成多方案，自动选最佳 | 高质量文档 |

## 执行流程

```
Phase 1: 文档读取与格式检测 [自动]
Phase 2: AI 去痕处理 [自动] — 调用 humanizer-scan + humanizer-soul skills（学术场景额外调用 humanizer-academic）
Phase 3: 智能配图生成 [自动] — 调用 html-chart + mermaid-chart skill
Phase 4: 输出完整文档 [自动]
```

## 输出文件结构

```
原文件目录/
├── article.md                    # 原始文件（保持不变）
├── article-polished.md           # 润色后的文档
└── imgs/
    ├── article-polished-1.png
    └── article-polished-2.png
```

## 质量评分

- AI 去痕：5 维度 50 分制（直接性/节奏/信任度/真实性/精炼度）
- 配图质量：4 维度 100 分制（信息完整性/视觉清晰度/逻辑连贯性/美观度）

## 相关命令

- `/humanize-scan` `/humanize-soul` `/humanize-academic` — 单独执行 AI 去痕的三个阶段
- `/illustrate` — 单独执行文章配图
