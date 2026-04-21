---
name: article-writer
description: 用内置文章风格写一篇公众号长文（4000-8000字）
user-invocable: true
argument-hint: "[主题/素材] [--style-card path]"
---

# /article-writer

以内置文章风格创作公众号长文。

## 用法

```
/article-writer [主题或素材]
/article-writer --style-card ./my-style.md
```

## 示例

```
/article-writer 帮我写一篇关于 Claude Code 实际使用体验的文章
/article-writer 写一篇公众号文章，主题是 AI 正在改变内容创作
/article-writer [粘贴产品 brief] 帮我写成文章
```

## 执行流程

1. 加载 `skills/article-writer/SKILL.md` 完整规范
2. HKR 质检选题（Happy / Knowledge / Resonance）
3. 判断文章原型（调查实验型/产品体验型/现象解读型/工具分享型/方法论分享型）
4. 按文章结构模板创作（4000-8000 字）
5. 四层自检（L1 硬性规则 → L2 风格一致性 → L3 内容质量 → L4 活人感终审）
6. 输出文章正文 + 质检报告

## 核心风格

> **"有见识的普通人在认真聊一件打动他的事。"**

- 亲自下场，不隔空评论
- 口语化叙述，不用套话
- 四层自检体系保证"活人感"
- 适用于公众号长文（4000-8000 字）

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--style-card <路径>` | 使用已保存的风格卡片 | 内置文章风格 |

## 输出格式

```
[文章正文 4000-8000 字]

---
质检报告
L1 硬性规则 ✅
L2 风格一致性 ✅
L3 内容质量 ✅
L4 活人感 ✅
```

## 参考资料

- 风格示例：`skills/article-writer/references/style_examples.md`
- 内容方法论：`skills/article-writer/references/content_methodology.md`
