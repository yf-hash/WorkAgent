---
name: paper-collector
description: >
  arXiv 安全论文搜集技能。按时间范围和主题批量检索论文，过滤去重，
  输出中文标题与摘要（100-150字），适用于安全研究情报跟踪。
  触发关键词：paper collect、arxiv、安全论文、论文搜集、security papers
user-invocable: false
effort: medium
argument-hint: "--since <YYYY-MM-DD> [--until <YYYY-MM-DD>] [--topic <topic>] [--limit <n>]"
---

# arXiv 论文搜集技能

## 支持主题

- llm-security
- fuzzing
- code-security
- pentest
- social-eng
- ai-agent-sec
- ai-safety
- all

## 工作流

1. 解析参数（时间范围、主题、数量）
2. 并行检索（WebSearch + arxiv API 兜底）
3. 提取元数据（title/abstract/id/date/url）
4. 时间过滤 + 去重
5. 标题翻译 + 摘要压缩翻译（100-150字）
6. 按发布时间倒序输出

## 输出模板

```markdown
搜集时间范围：YYYY-MM-DD 至 YYYY-MM-DD
搜集论文总数：N 篇
主题分布：...

---
论文标题：[中文标题]
摘要：[中文摘要]
原文URL：https://arxiv.org/abs/xxxx.xxxxx
```
