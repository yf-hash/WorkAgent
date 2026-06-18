---
allowed-tools: Bash, Read, Write, Edit, AskUserQuestion, Skill
description: 论文深度解读，将学术论文PDF转化为通俗易懂的公众号长文（4000-6000字）
argument-hint: "<pdf-path> [--output md|docx] [--style popular|professional|casual] [--length short|medium|long]"
---

# /paper-interpret

论文解读命令，将专业学术论文转化为通俗易懂的公众号长文。

## 用法

```
/paper-interpret <PDF文件路径> [选项]
```

## 示例

```
/paper-interpret paper.pdf
/paper-interpret paper.pdf --output docx
/paper-interpret paper.pdf --style professional --length long
```

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `<pdf-path>` | 论文 PDF 文件路径（必填） | — |
| `--output <格式>` | 输出格式：`md` / `docx` / `pdf` | `md` |
| `--style <风格>` | 写作风格：`popular`(科普) / `professional`(专业) / `casual`(轻松) | `popular` |
| `--length <字数>` | `short`(3000-4000字) / `medium`(4000-6000字) / `long`(6000-8000字) | `medium` |

## 执行流程

1. 加载 `skills/paper-interpreter/SKILL.md` 解读规范
2. 读取论文 PDF，提取文本和关键图表
3. 按九大模块提取结构化信息（简介/目的/贡献/引言/相关工作/核心方法/实验/讨论/结论）
4. 按指定风格和字数生成公众号长文（段落式，非列表）
5. 将提取的图表插入对应章节
6. 调用 `humanizer-scan` + `humanizer-soul` skill 去 AI 味（学术深度场景额外 `humanizer-academic`）
7. 询问用户满意度，按反馈持续优化

## 输出格式

```markdown
# 论文解读：[中文标题]

## 基本信息
- 原文标题 / 作者 / 单位 / 关键词 / 原文链接 / 开源代码

## 论文要点
- 论文简介（≥200字段落）
- 研究目的 / 研究贡献（≥200字）

## [各章节，使用论文实际标题的中文译名]

[段落式文字，禁用列表，含关键图表引用]
```

## 写作原则

- **段落式表达**：所有内容用连贯段落，禁止 bullet points
- **通俗易懂**：专业术语加注释，吸引非专业读者
- **配图整合**：关键图表从 PDF 提取后插入对应章节
- **活人感**：去除 AI 套话，保留真实学术洞察

## 关联 Skills

- `paper-interpreter` - 论文解读核心规范
- `humanizer-scan` / `humanizer-soul` / `humanizer-academic` - 去 AI 味处理
- `article-writer` - 写作风格参考

## 相关命令

- `/paper-collect` - 批量收集 arxiv 论文
- `/humanize-scan` - 单独去 AI 味处理（扫描阶段）
- `/polish` - 文档润色（去痕+配图）
