---
name: paper-collector
description: >
  arXiv 学术论文搜集技能。按时间范围和学科领域批量检索论文，过滤去重，
  输出中文标题与摘要（100-150字），适用于学术前沿情报跟踪。
  触发关键词：paper collect、arxiv、学术论文、论文搜集、academic papers、论文追踪、研究动态
user-invocable: false
effort: medium
argument-hint: "--since <YYYY-MM-DD> [--until <YYYY-MM-DD>] [--domain <学科领域>] [--topic <关键词>] [--limit <n>]"
harness:
  execute:
    preset: research
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

# arXiv 论文搜集技能

## 支持学科领域（--domain）

### 安全与 AI 安全
- `llm-security` — LLM/GPT 安全、越狱攻击、提示注入
- `fuzzing` — 模糊测试、AFL、覆盖率引导
- `code-security` — 代码安全（静态/动态分析、SCA）
- `pentest` — 渗透测试、自动化漏洞利用、红队
- `social-eng` — 社工钓鱼、邮件安全
- `ai-agent-sec` — 安全智能体、自主攻击
- `ai-safety` — AI 安全（对齐、鲁棒性、后门攻击）

### 机器学习与 AI
- `llm` — 大语言模型（预训练、推理、微调）
- `multimodal` — 多模态（图文、视频理解）
- `rl` — 强化学习
- `cv` — 计算机视觉
- `nlp` — 自然语言处理
- `generative-ai` — 生成式 AI（Diffusion、GAN、VAE）

### 软件工程
- `code-gen` — AI 代码生成、Copilot
- `formal-methods` — 形式化验证
- `testing` — 软件测试、程序分析

### 其他领域（使用 --topic 自由输入关键词）
- `bio` — 生物信息学
- `physics` — 物理学
- `economics` — 经济学/金融
- `all` — 不限领域，按 --topic 关键词搜索

## 工作流

1. 解析参数（时间范围、领域/主题、数量）
2. 并行检索（WebSearch + arxiv API 兜底）
3. 提取元数据（title/abstract/id/date/url）
4. 时间过滤 + 去重
5. 标题翻译 + 摘要压缩翻译（100-150字）
6. 按发布时间倒序输出

## 输出模板

```markdown
搜集时间范围：YYYY-MM-DD 至 YYYY-MM-DD
搜集论文总数：N 篇
领域/主题：...

---
论文标题：[中文标题]
摘要：[中文摘要]
原文URL：https://arxiv.org/abs/xxxx.xxxxx
```
