---
name: pm-ai-era-evolution
description: >
  AI 时代产品经理技能演变知识库。覆盖新增核心能力（Prompt Engineering / LLM 产品设计 / AI 指标体系 /
  数据飞轮 / AI 伦理）以及不变的核心（用户同理心 / 数据驱动 / 跨部门影响力 / 清晰书面表达）。
  触发词：AI 时代 PM、AI 产品经理、PM 技能演变、Prompt Engineering、LLM 产品设计、AI 指标
user-invocable: false
effort: low
---

# PM AI Era Evolution — AI 时代 PM 技能演变

> 单一职责：AI 时代 PM 需要新增的能力和不变的核心。
> 不做：AI 安全产品方法论（→ `pm-ai-security-product`）、AI 产品架构（→ `@ai-product-architect`）

## 新增核心能力

```
1. Prompt Engineering — 设计 AI 功能的用户交互
   - System Prompt 设计：定义 AI 角色和约束
   - Few-shot 示例选择：影响输出风格
   - 用户输入引导：避免 Garbage In Garbage Out

2. LLM 产品设计 — 处理 AI 特有问题
   - 幻觉处理：拒答、置信度、引用溯源
   - 延迟预期管理：流式输出、加载文案
   - Fallback 设计：失败时的备选路径
   - 上下文窗口管理：长对话压缩与摘要

3. AI 指标体系 — 区别于传统功能
   - 准确率（Accuracy）：客观可验证的对错
   - 有用率（Usefulness）：用户主观觉得有用
   - 接受率（Acceptance）：用户采纳 AI 输出的比例
   - 完成率（Completion）：用户跑完整个流程的比例
   - 编辑率（Edit Distance）：用户改了多少 AI 输出

4. 数据飞轮设计 — 用户使用数据如何改善模型
   - 隐式反馈：点赞、收藏、编辑、复制
   - 显式反馈：评分、修正、举报
   - 数据收集合规：知情同意、脱敏、删除权

5. AI 伦理边界 — 防止产品翻车
   - 偏见检测：性别/种族/年龄/地域
   - 隐私保护：训练数据、推理日志
   - 可解释性：让用户理解 AI 为何这么说
   - 越权风险：AI 不该做的事
```

## 不变的核心能力

```
- 用户同理心：AI 再强，PM 还得知道用户痛点
- 数据驱动决策：AI 实验也要 A/B，也要看显著性
- 跨部门影响力：与算法、工程、设计、销售对齐
- 清晰的书面表达：PRD / Spec / 决策备忘录
```

## AI 功能 PRD 增量要素

```
传统 PRD 之外，AI 功能必须补充：

§AI-1：AI 角色与定位
- 这是 Copilot 还是 Autopilot？
- 用户主导还是 AI 主导？决策权归谁？

§AI-2：输入输出契约
- 输入：用户文本 / 图片 / 音频 / 文档
- 输出：纯文本 / 结构化 JSON / 工具调用
- 失败兜底：拒答文案 / 重试策略 / 转人工

§AI-3：质量评估方案
- Eval 集：N 条 golden cases，覆盖正/负/边界
- 通过标准：准确率 ≥ X%，有用率 ≥ Y%
- 上线门控：未达标不能发布

§AI-4：成本与延迟约束
- 单次调用预估成本
- P95 延迟要求
- 流式 / 同步选择

§AI-5：安全与合规
- 敏感话题处理（政治/医疗/金融建议）
- 越权风险防护
- 数据留存策略
```

## 与其他 AI 相关 Skill 边界

| 场景 | 推荐 |
|------|------|
| AI 时代 PM 通识 | 本 Skill |
| AI 安全产品（SAST/SCA/检测/对抗） | `pm-ai-security-product` |
| AI 产品架构设计 | `@ai-product-architect` |
| AI 红队测试 | `ai-red-team` |
| AI 模型卡 / 评估表 | `templates/model-card-template.md` / `templates/ai-eval-rubric-template.md` |
