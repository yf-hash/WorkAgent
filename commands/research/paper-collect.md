---
name: paper-collect
user-invocable: true
allowed-tools: WebSearch, WebFetch, Read, Write, AskUserQuestion
description: 从 arxiv.org 搜集指定学科领域最新论文，按时间范围和主题过滤，输出结构化中文摘要
argument-hint: "--since <YYYY-MM-DD> [--until <YYYY-MM-DD>] [--domain <领域>] [--topic <关键词>] [--limit <n>] [--output <路径>]"
---

# /paper-collect

从 arxiv.org 搜集指定学科领域最新论文，按时间范围过滤，输出结构化中文摘要。

加载技能：`skills/research/paper-collector/SKILL.md`

## 用法

```
/paper-collect --since 2026-02-01
/paper-collect --since 2026-01-01 --until 2026-02-01 --domain llm
/paper-collect --since 2026-02-01 --domain llm-security,pentest --limit 5
/paper-collect --since 2026-02-01 --domain all --topic "retrieval augmented generation" --limit 10
/paper-collect --since 2026-02-01 --limit 5 --output docs/papers/2026-02.md
```

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--since <YYYY-MM-DD>` | 论文发布起始日期（必填） | — |
| `--until <YYYY-MM-DD>` | 论文发布截止日期 | 今天 |
| `--domain <领域>` | 学科领域，逗号分隔多选（见下表） | `all` |
| `--topic <关键词>` | 自由关键词搜索（补充 domain 或单独使用） | — |
| `--limit <数量>` | 每个领域最多返回论文数 | 10 |
| `--output <路径>` | 保存结果到 Markdown 文件 | — |

## 支持的学科领域（--domain）

### 安全与 AI 安全
| 领域 ID | 说明 |
|---------|------|
| `llm-security` | LLM/GPT 安全、越狱攻击、提示注入 |
| `fuzzing` | 模糊测试、AFL、覆盖率引导 |
| `code-security` | 代码安全（静态/动态分析、SCA） |
| `pentest` | 渗透测试、自动化漏洞利用、红队 |
| `social-eng` | 社工钓鱼、邮件安全 |
| `ai-agent-sec` | 安全智能体、自主攻击 |
| `ai-safety` | AI 安全（对齐、鲁棒性、后门攻击） |

### 机器学习与 AI
| 领域 ID | 说明 |
|---------|------|
| `llm` | 大语言模型（预训练、推理、微调） |
| `multimodal` | 多模态（图文、视频理解） |
| `rl` | 强化学习 |
| `cv` | 计算机视觉 |
| `nlp` | 自然语言处理 |
| `generative-ai` | 生成式 AI（Diffusion、GAN、VAE） |

### 软件工程
| 领域 ID | 说明 |
|---------|------|
| `code-gen` | AI 代码生成、程序合成 |
| `testing` | 软件测试、程序分析 |
| `formal-methods` | 形式化验证 |

### 通用
| 领域 ID | 说明 |
|---------|------|
| `all` | 不限领域，配合 --topic 关键词使用 |

## 执行逻辑

1. 解析时间范围和领域/关键词参数
2. 按领域并行搜索（优先 WebSearch，备用 arxiv API）
3. 提取标题、摘要、arxiv ID、发布日期
4. 过滤：仅保留在 `--since` 至 `--until` 范围内的论文
5. 标题翻译为中文，摘要压缩翻译为中文（100-150字）
6. 去重（同一 arxiv ID 只保留一条）
7. 按发布时间倒序，按领域分组输出

## 输出格式

```
搜集时间范围：YYYY-MM-DD 至 YYYY-MM-DD
搜集论文总数：N 篇
领域分布：[领域A] X篇 | [领域B] X篇 | ...

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
