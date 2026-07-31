---
name: interview-writer
description: 基于访谈素材创作公众号长文，通过 Writer-Reviewer 互搏机制迭代优化
user-invocable: true
argument-hint: "[访谈素材] [--target-score 85] [--max-rounds 3] [--mode full]"
---

# /interview-writer

访谈写作 v2.0，通过 Writer-Reviewer 互搏机制生成高质量访谈文章。

## 用法

```
/interview-writer [访谈素材或主题]
/interview-writer --target-score 88 --max-rounds 3
```

## 示例

```
/interview-writer 以下是我和 [人物] 的访谈记录：[粘贴素材]
/interview-writer 帮我写一篇关于 [人物] 的专访文章
/interview-writer --style-card ./my-style.md --target-score 88
```

## 执行流程

1. 加载 `skills/writing/interview-writer/SKILL.md` 完整规范
2. Phase 1：素材解析（提取核心观点 3-5 个，识别金句和故事，设计框架）
3. Phase 2：Writer 初稿（按访谈写作规范创作，输出自评）
4. Phase 3：Reviewer 评审（四层评分，找出最弱层，给出 3 条具体建议）
5. Phase 4：Writer-Reviewer 互搏（最多 max-rounds 轮，每轮针对最弱层定向修改）
6. Phase 5：知识库沉淀（保存有效模式到 `knowledge-base/interview-patterns.md`）

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--style-card <路径>` | 风格卡片路径 | 内置访谈风格 |
| `--target-score <分数>` | 目标质量分（四层加权） | 85 |
| `--max-rounds <轮次>` | 最大互搏轮次 | 3 |
| `--mode <模式>` | `full`=完整互搏，`draft`=仅初稿 | `full` |
| `--save-kb <true/false>` | 是否沉淀到知识库 | `true` |

## 访谈写作四大原则

1. **受访者声音优先**：保留真实表达，≥5 处直接引用
2. **细节证明真实**：用具体细节而非抽象描述
3. **叙事重构**：不是流水账，而是有主题的故事
4. **立场鲜明**：作者有观点，不做中立记录员

## 质量标准

- 字数：4000-8000 字
- 综合得分：≥85（四层加权）
- 直接引用：≥5 处受访者原话
- AI 套话：0
- 迭代轮次：≤3 轮达标

## 输出格式

```
[文章正文 4000-8000 字]

---
质量报告

| 层次 | 最终得分 | 提升幅度 |
|------|---------|---------|
| 活人感 | X/30 | +X |
| 情感   | X/25 | +X |
| 信息   | X/25 | +X |
| 结构   | X/20 | +X |
| 综合   | X/100 | +X |

迭代路径：[初始分] → [第1轮后] → ... → [最终分]
知识库更新：[是/否]
```
