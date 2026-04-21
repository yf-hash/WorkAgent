# AGENTS.md

> WorkAgent AI 内容创作平台 | OpenAI Codex / OpenCode 项目指导

## 项目概述

WorkAgent 是以**风格驱动**的 AI 内容创作平台，核心理念是：**先学习写作风格，再用该风格创作内容**。

本文件为 OpenAI Codex、OpenCode 和其他兼容工具的项目指导文件。Claude Code 用户请参阅 `CLAUDE.md`。

---

## 仓库结构

```
WorkAgent/
├── CLAUDE.md              # Claude Code 项目指导
├── AGENTS.md              # 本文件（Codex/OpenCode 指导）
├── README.md              # 快速开始指南
├── .claude/
│   └── settings.json      # Claude Code 权限配置
├── .cursor/
│   └── rules/             # Cursor 写作规范规则
├── agents/                # 自治代理（编排写作全流程）
│   └── content-director.md
├── skills/                # 写作技能知识库
│   ├── article-writer/    # 文章写作风格
│   │   ├── SKILL.md
│   │   ├── references/    # 风格体系文档
│   │   └── templates/     # 写作模板
│   └── content-evolve/    # 风格学习+迭代创作
│       ├── SKILL.md
│       ├── references/    # 分析方法论
│       └── templates/     # 风格卡片模板
└── hooks/                 # Claude Code 钩子（安全+质量）
    ├── hooks.json
    ├── security/
    └── quality/
```

---

## 工具映射表

| 功能 | Claude Code | Cursor | Codex/OpenCode |
|------|-------------|--------|----------------|
| 文章写作 | `/article-writer` | 对话触发 | 读取 `skills/article-writer/SKILL.md` 后执行 |
| 风格学习+创作 | `/content-evolve` | 对话触发 | 读取 `skills/content-evolve/SKILL.md` 后执行 |
| 全流程编排 | `@content-director` | Agent 模式 | 读取 `agents/content-director.md` |

---

## Skills 使用说明（Codex 环境）

在 Codex / OpenCode 中，没有原生的 Slash Command 支持。推荐做法：

**方式 1：加载 Skill 文件**

```
请读取 skills/article-writer/SKILL.md，然后按照其中的写作流程，
帮我写一篇关于 [主题] 的公众号文章。
```

**方式 2：指定风格学习**

```
请读取 skills/content-evolve/SKILL.md，然后：
1. 分析以下文章的写作风格：[URL1, URL2]
2. 生成风格卡片
3. 用该风格写一篇关于 [标题] 的文章
```

**方式 3：完整流程编排**

```
请读取 agents/content-director.md，作为内容总监，
帮我完成以下写作任务：[任务描述]
```

---

## 写作任务规范

在此仓库中进行写作任务时，请遵循：

### 1. 风格优先

- 任何写作输出必须遵循指定风格（文章风格或用户学习的自定义风格）
- 禁止使用 AI 套话（"首先"、"总之"、"不得不说"、"深刻感受到"等）
- 保持"有见识的普通人在认真聊一件事"的语感

### 2. 质量标准

写作完成后执行四层自检：

```
Layer 1 - 活人感：文章是否像一个真实的人在说话？
Layer 2 - 情感：是否有温度，能打动读者？
Layer 3 - 信息：是否有真正的见解和干货？
Layer 4 - 结构：段落节奏是否流畅好读？
```

每层评分 0-100，综合≥85 为达标。

### 3. 文件输出规范

- 文章输出为 `.md` 文件，存放在 `output/` 目录（自动创建）
- 风格卡片存放在 `style-cards/` 目录（自动创建）
- 文件名格式：`YYYY-MM-DD-文章标题.md`

---

## 项目约定

| 约定 | 说明 |
|------|------|
| 写作语言 | 默认中文，除非明确指定英文 |
| 文章长度 | 公众号长文 4000-8000 字 |
| 迭代轮次 | 默认最多 3 轮，可通过参数调整 |
| 目标评分 | 默认 85 分，可通过 `--target-score` 调整 |
| 风格卡片格式 | YAML，见 `skills/content-evolve/templates/style-card.md` |

---

## 快速验证

读取本仓库后，可以通过以下方式验证配置正确：

```bash
# 列出所有 Skills（确认两个 Skill 存在）
ls skills/

# 查看 article-writer 的触发条件
head -20 skills/article-writer/SKILL.md

# 查看 content-evolve 的参数说明
grep -A 20 "intake" skills/content-evolve/SKILL.md
```
