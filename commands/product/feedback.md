---
name: feedback
description: >
  用户反馈管理 — 多渠道反馈数据的收集、分析、行动闭环。覆盖反馈收集（弹窗 /邮件 / 应用内 / 工单）、主题聚类与情感分析、NPS / CSAT 设计、功能投票看板、Voice of Customer（VoC）月报 / 季报。
  
  与相邻命令的边界（防混淆）：
  - vs /user-research：本命令是"被动分析现有反馈数据"；
    /user-research 是"主动设计研究并采集"。
  - vs /pmf-survey：PMF 是 NPS 的"专项进阶版"（Sean Ellis 测试）。
  适用于：产品反馈数据治理、月度 VoC 报告、新功能优先级、流失原因分析。
user-invocable: true
argument-hint: "<产品/功能描述> [--mode collect|analyze|nps|vote|voc] [--source <文件或URL>]"
---

# /feedback — 用户反馈管理

加载技能：`skills/strategy/user-feedback/SKILL.md`

## 触发条件
需要设计反馈收集机制、分析用户反馈数据、生成用户之声报告，或整合多渠道反馈时。

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `<产品/功能描述>` | 产品名称或分析上下文（必填） | — |
| `--mode` | 工作模式 | `analyze` |
| `--source` | 反馈数据来源文件 | — |

### 工作模式
| `--mode` | 输出内容 | 适用场景 |
|----------|---------|---------|
| `collect` | 反馈收集方案（渠道 + 时机 + 问题设计） | 产品上线后规划 |
| `analyze` | 反馈数据分析（主题聚类 + 情感 + 优先级） | 处理积压反馈 |
| `nps` | NPS/CSAT 调查设计 + 结果解读 | 满意度度量 |
| `vote` | 功能投票看板设计（需求优先级） | Roadmap 规划 |
| `voc` | Voice of Customer 报告（月/季度） | 管理汇报 |

## 参考工具生态

| 工具 | 特点 | GitHub |
|------|------|--------|
| LogChimp | 开源功能投票 & 反馈看板 | logchimp/logchimp |
| ABC User Feedback | LINE 开源用户反馈平台 | line/abc-user-feedback |
| Quackback | 轻量反馈收集组件 | QuackbackIO/quackback |
| Touchpoints | 政府数字服务反馈工具（GSA） | GSA/touchpoints |
| Backfeed | 结构化反馈管理 | omnidotdev/backfeed-app |

## 执行流程（analyze 模式）

```
Step 1: 数据摄入
  → 支持格式：CSV/JSON/纯文本/截图文字
  → 字段识别：时间、渠道、内容、评分、用户标签

Step 2: 主题聚类
  → 功能请求 (Feature Request)
  → Bug 报告 (Bug Report)
  → 体验问题 (UX Issue)
  → 好评 (Positive)
  → 其他/噪音

Step 3: 情感分析
  → 情感标签（正面/中性/负面）
  → 强度评分（1-5）
  → 情感触发词提取

Step 4: 优先级矩阵
  → 频次 × 情感强度 × 用户价值
  → 生成 Top 10 优先处理项

Step 5: VoC 报告
  → 执行摘要（3条关键发现）
  → 各主题详情 + 用户原话
  → 建议的产品动作
```

## 输出示例（voc 模式）

```markdown
# [产品名] 用户之声报告 — [月份]

## 关键发现
1. 导出功能是本月最高频投诉（占 23% 反馈）
2. AI 建议质量满意度显著提升（NPS +12）
3. 移动端卡顿问题需优先修复

## 反馈分布
| 类型 | 数量 | 占比 | 情感倾向 |
|------|------|------|---------|
| 功能请求 | 45 | 38% | 中性 |
| Bug 报告 | 28 | 24% | 负面 |
| 体验反馈 | 30 | 25% | 混合 |
| 好评 | 15 | 13% | 正面 |

## 用户原声精选
> "导出 PDF 的时候格式全乱了..." — 用户 A

## 建议行动
- P0: 修复 PDF 导出格式问题（影响 28 个用户）
- P1: 优化移动端滚动性能
- P2: 规划批量导出功能
```

## 使用示例

```
/feedback 为新上线的 AI 助手设计反馈收集方案 --mode collect
/feedback 分析 feedback.csv 用户反馈数据 --source feedback.csv
/feedback 设计月度 NPS 调查 --mode nps
/feedback 整理功能需求优先级投票 --mode vote
/feedback 生成 Q1 用户之声报告 --source q1_feedback.json --mode voc
```
