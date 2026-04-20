---
allowed-tools: WebSearch, WebFetch, Read, Write, AskUserQuestion
description: 从 arxiv.org 搜集安全领域最新论文，按时间范围和主题过滤，输出结构化中文摘要
argument-hint: "--since <YYYY-MM-DD> [--until <YYYY-MM-DD>] [--topic <topic>] [--limit <n>] [--output <路径>]"
---

# /paper-collect

从 arxiv.org 搜集安全领域最新论文，按时间范围过滤，输出结构化中文摘要。

## 用法

```
/paper-collect --since 2026-02-01
/paper-collect --since 2026-01-01 --until 2026-02-01 --topic fuzzing
/paper-collect --since 2026-02-01 --topic llm-security,pentest --limit 5
/paper-collect --since 2026-02-01 --limit 5 --output docs/papers/2026-02.md
```

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--since <YYYY-MM-DD>` | 论文发布起始日期（必填） | — |
| `--until <YYYY-MM-DD>` | 论文发布截止日期 | 今天 |
| `--topic <主题>` | 限定搜索主题，逗号分隔多选 | `all` |
| `--limit <数量>` | 每个主题最多返回论文数 | 10 |
| `--output <路径>` | 保存结果到 Markdown 文件 | — |

## 支持的主题

| 主题 ID | 说明 |
|---------|------|
| `llm-security` | LLM/GPT 安全、越狱攻击、提示注入 |
| `fuzzing` | 模糊测试、AFL、覆盖率引导 |
| `code-security` | 代码安全（静态/动态分析、SCA） |
| `pentest` | 渗透测试、自动化漏洞利用、红队 |
| `social-eng` | 社工钓鱼、邮件安全 |
| `ai-agent-sec` | 安全智能体、自主攻击 |
| `ai-safety` | AI 安全（对齐、鲁棒性、后门攻击） |
| `all` | 全部主题（默认） |

## 执行逻辑

1. 解析时间范围和主题参数
2. 按主题并行搜索（优先 WebSearch，备用 arxiv API）
3. 提取标题、摘要、arxiv ID、发布日期
4. 过滤：仅保留在 `--since` 至 `--until` 范围内的论文
5. 标题翻译为中文，摘要压缩翻译为中文（100-150字）
6. 去重（同一 arxiv ID 只保留一条）
7. 按发布时间倒序，按主题分组输出

## 输出格式

```
搜集时间范围：YYYY-MM-DD 至 YYYY-MM-DD
搜集论文总数：N 篇
主题分布：LLM安全 X篇 | 模糊测试 X篇 | ...

---

论文标题：[中文标题]
摘要：[中文摘要，100-150字]
原文URL：https://arxiv.org/abs/[ID]

---
```

## 翻译规范

- 标题：直接翻译为简体中文，专有名词（GPT-4、AFL、BERT）保留英文
- 摘要：提炼核心贡献，中文重新表述，100-150字，避免逐字翻译

## 相关命令

- `/paper-interpret` — 深度解读单篇论文 PDF
