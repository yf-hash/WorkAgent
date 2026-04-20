---
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, WebFetch, AskUserQuestion, Skill
description: 风格学习 → 风格卡片确认 → Writer-Reviewer 迭代创作，两阶段自进化写作
argument-hint: "[--learn <urls>] [--title <标题>] [--framework <框架>] [--style-card <路径>] [--mode quality|humanize|balance] [--target-score <分数>]"
---

# /self-evolve

内容自进化命令。两阶段流程：**风格学习**提炼参考文章共性规律生成「风格卡片」，**创作执行**以风格卡片为基准 Writer-Reviewer 迭代创作。

## 用法

```
# 完整流程（风格学习 + 创作）
/self-evolve --learn <url1,url2,...> --title <文章标题> [--framework <框架>]

# 仅风格学习（生成风格卡片，稍后复用）
/self-evolve --learn <url1,url2,...>

# 使用已有风格卡片创作
/self-evolve --style-card <风格卡片路径> --title <文章标题> [--framework <框架>]

# 优化已有文章
/self-evolve --title <文章标题> <文档路径>
```

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--learn <urls>` | 1-5 篇优质文章链接，触发阶段一风格学习 | — |
| `--title <标题>` | 要创作的文章标题 | — |
| `--framework <框架>` | 文章框架（可选），如 `"问题引入→分析→方案→行动"` | AI 自动推导 |
| `--style-card <路径>` | 已保存的风格卡片路径（跳过阶段一） | — |
| `--save-card <路径>` | 将生成的风格卡片保存到指定路径 | — |
| `--target-score <分>` | 目标评分，默认 85，范围 60-100 | 85 |
| `--max-rounds <轮>` | 最大迭代轮次，范围 1-5 | 3 |
| `--mode <模式>` | `quality`=内容优先，`humanize`=去AI味优先，`balance`=双向均衡 | `quality` |
| `--show-process` | 显示完整迭代过程 | false |

## 执行流程

加载 `skills/style-evolver/SKILL.md` 完整规范执行，流程摘要：

### 阶段一：风格学习（`--learn` 触发）

1. WebFetch 逐篇抓取文章全文
2. 逐篇分析：开篇模式、论证结构、段落节奏、过渡方式、结尾策略、语言风格、案例密度
3. 提炼共性规律，生成「风格卡片」
4. **⏸ 暂停**，展示风格卡片等待用户确认/修改

### 阶段二：创作执行（风格卡片确认后）

1. 加载风格卡片
2. Writer 按风格卡片 + 标题/框架生成初稿
3. Reviewer 双维度评分（内容质量 50 分 + 风格合规 50 分）+ 精准诊断
4. Writer 针对诊断定向修改（最多 `--max-rounds` 轮）
5. 达到目标分或边际收益递减时停止

**终止条件（满足任一即停）：**
- 评分达到目标分数
- 已迭代最大轮次
- 连续 2 次提升 < 3 分

## 质量标准

| 维度 | 满分 | 子维度 |
|------|------|--------|
| 内容质量 | 50 | 深度/15 + 案例/15 + 逻辑/10 + 结构/10 |
| 风格合规 | 50 | 自然度/15 + 真实感/15 + 节奏/10 + 一致性/10 |

## 输出格式

```
# 自进化完成

## 进化概览
- 风格来源：[N 篇参考文章 / 已有风格卡片]
- 原始分数：XX/100（优化已有内容时）
- 最终分数：XX/100
- 总提升：+XX 分
- 迭代轮次：X 轮
- 终止原因：[目标达成 / 最大轮次 / 边际收益递减]

## 最终文章

[完整文章内容]
```

## 相关命令

- `/interview-writer` — 访谈写作，内置 Writer-Reviewer 互搏
- `/khazix-writer` — 卡兹克风格公众号长文
- `/hv-analysis` — 横纵分析法深度研究
