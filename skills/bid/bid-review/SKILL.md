---
name: bid-review
description: >
  标书第 5 阶段：双轮多维度评审。第一轮交叉审核（五视角：business/technical/delivery/risk/competitive）+
  第二轮专家评审（技术架构合理性、差异化、评分覆盖、实施可行性）。输出 bid-review 报告 + 评审意见表。
  触发词：标书评审、bid review、标书审查、技术方案评审
user-invocable: false
effort: medium
harness:
  execute:
    preset: writing-scoped
  constrain:
    profile: writing-safe
  loop:
    mode: one-shot
  memory:
    scope: project
    reads: [project-context]
  security:
    danger-level: medium
---

# Bid Review — 标书 Phase 5 双轮评审

> 单一职责：标书七阶段第 5 阶段（双轮评审）。
> 上游：`bid-write` 的标书草稿。
> 下游：`bid-check` 合规与一致性核查。

## 第一轮：交叉审核（五视角）

| 视角 | 检查重点 |
|------|----------|
| `business` | 价值主张清晰、竞争差异化、客户痛点响应 |
| `technical` | 架构合理、技术参数/功能要求全部响应、风险可控 |
| `delivery` | 里程碑合理、资源充足、实施计划可行 |
| `risk` | 废标风险、承诺过度、法律合规、错别字/格式错误 |
| `competitive` | 亮点突出、与竞品区分、得分最大化 |

### 五视角检查清单

```markdown
## Business 视角
- [ ] 客户痛点是否有明确响应（不只是技术堆砌）
- [ ] 差异化卖点是否突出（vs 已知竞品）
- [ ] ROI / 价值主张是否量化

## Technical 视角
- [ ] 所有技术要求是否覆盖（对照最终清单）
- [ ] 架构是否合理（无明显技术债 / 过度设计）
- [ ] 性能 / 安全 / 兼容性指标是否达标

## Delivery 视角
- [ ] 里程碑是否合理（不过于乐观也不保守）
- [ ] 资源投入是否匹配工作量
- [ ] 风险应对方案是否完整

## Risk 视角
- [ ] 是否有过度承诺（做不到的别写）
- [ ] 是否有法律合规风险
- [ ] 错别字、格式错误是否清理

## Competitive 视角
- [ ] 高分项是否拿满
- [ ] 亮点是否容易被评委一眼看到
- [ ] 是否回避了我方明显弱项
```

## 第二轮：专家评审

由具备项目经验的资深技术专家 / 项目经理执行：

- 技术架构合理性、有无技术风险
- 是否突出我方差异化优势
- 评分点是否全部覆盖
- 实施计划可行性、售后服务是否到位

### 专家评审输出格式

```markdown
## 专家评审意见

### 评分预估
基于评分细则逐项评估：[X / 100] 分

### 强项
1. [章节] [亮点]
2. ...

### 弱项（需修改）
1. [章节] [问题] → 建议：[改进方向]
2. ...

### 风险提示
1. [风险点] [影响] → 缓解：[方案]
```

## 输出物

- `bid-review-[项目名].md`
- `技术标书评审意见表.xlsx`

## 双轮评审节奏

```
Day 1：第一轮交叉审核（5 视角，4-8 小时）
Day 2-3：基于第一轮意见修改
Day 4：第二轮专家评审（2-4 小时）
Day 5：最终修改 + 进入 bid-check
```
