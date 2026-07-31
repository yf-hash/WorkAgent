---
name: style-refine
description: >
  以风格卡片为基准，对已有文章做风格优化（不重写）。先做基线评分，再用 proven_solutions 策略定向修改，
  最多 3 轮。支持 quality/humanize/balance 三种模式。区别于 style-writer-reviewer（从零创作）。
  触发词：风格优化、已有内容优化、style refine、文章风格迁移、风格校准、风格修改
user-invocable: false
effort: medium
argument-hint: "<文档路径> [--style-card <路径>] [--mode quality|humanize|balance] [--target-score 85] [--max-rounds 3]"
---

# Style Refine — 已有内容风格优化

> 单一职责：对已有文章按风格卡片做风格校准，不改变核心内容和事实。
> 不做：从零创作（→ `style-writer-reviewer`）、提炼风格卡片（→ `style-card-extractor`）、AI 去痕扫描（→ `humanizer-scan`）

## 前置输入

- 已有文档路径
- 风格卡片（来自 `style-card-extractor` 或 `--style-card` 加载）

## 流程

### Step 1：基线评分

对原文按风格卡片做双维度评分（与 `style-writer-reviewer` 同维度），输出基线分数和最弱子维度。

### Step 2：诊断驱动改写

只针对得分较低的子维度做改写，**不改变事实、数据、核心观点**：

```
P1（必须修复）：得分 < 60% 的子维度
P2（建议修复）：得分 60-75% 的子维度
P3（可选优化）：得分 75-85% 的子维度
```

每轮改写：
- 标注修改位置（章节/段落）
- 说明使用的 proven_solutions 策略 ID
- 预期分数提升

### Step 3：迭代收敛

| 终止条件 | 说明 |
|---|---|
| 达到目标分数 | 默认 85 |
| 已达最大轮次 | 默认 3 轮 |
| 边际收益递减 | 连续 2 次提升 < 3 分 |

### Step 4：输出对比报告

```markdown
## 风格优化报告

| 维度 | 子维度 | 基线 | 最终 | 提升 |
|------|--------|------|------|------|
| 内容质量 | 深度与完整性 | X/15 | X/15 | +X |
| ... | ... | | | |
| **总分** | | **XX/100** | **XX/100** | **+XX** |

## 关键改写示例（节选 3-5 处）

### 改写 1：[章节名]
- **原文**：[原句]
- **改后**：[改写后]
- **策略**：[SC-XX 删除 AI 高频词]
- **提升**：自然度 +3
```

## 三种模式

| 模式 | 适用 |
|------|------|
| `quality` | 内容好但表达干瘪，需要补案例/数据/对比 |
| `humanize` | 内容好但 AI 味重，需要去痕注入活人感 |
| `balance` | 两边都中等，找最弱的子维度逐个修 |

## 边界

- ❗ 不改事实、数据、核心观点
- ❗ 不重写整段（避免漂移）
- ❗ 风格分数提升 < 5 分时，建议直接调用 `style-writer-reviewer` 重写

## 衔接

- 优化完成后做 AI 去痕全扫描：`humanizer-scan` + `humanizer-soul`
- 学术深度场景：`humanizer-academic`
