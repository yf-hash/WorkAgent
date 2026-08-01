---
name: battle-card
description: >
  竞品作战卡（Battle Card）生成器 — 销售 / 售前在客户面前遭遇对手时的一页纸弹药。
  含一句话定位 / 三大杀手锏 / 三个雷区 / 价格锚点 / 标准应答 / 关键人画像 /
  内部使用提示。区别于深度市场研究（5000+ 字），Battle Card 是 60 秒可读完的
  内部文档。
user-invocable: true
argument-hint: "<对手名称> [--mode build|update|library] [--tier 1|2|3] [--industry fintech|gov|healthcare|saas]"
allowed-tools: [Read, Write, Edit, Grep, Glob, AskUserQuestion]
harness:
  execute:
    preset: writing-scoped
  constrain:
    profile: writing-safe
    gates: [before-write]
  loop:
    mode: one-shot
  memory:
    scope: project
    reads: [project-context]
  security:
    danger-level: medium
---

# /battle-card — 竞品作战卡生成器

加载技能：`skills/presales/battle-card/SKILL.md`
配套 Skill：`market-research`（深度对手分析支撑）、`win-loss-analysis`（赛后情报回流）

## 触发条件
- 销售反馈"客户在比 [对手 X]"，需要一页纸应对话术
- 季度竞争盘点 → 更新现有 Battle Card 库
- 新对手出现 / 老对手发布新功能 → 增量更新

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `<对手名称>` | 竞争对手公司全称 | — |
| `--mode` | 工作模式 | `build` |
| `--tier` | 对手分级（1 必维护 / 2 按需 / 3 一次性）| `2` |
| `--industry` | 目标客户行业（影响杀手锏选择）| — |

### 工作模式

| `--mode` | 输出 |
|----------|------|
| `build` | 生成新 Battle Card（一页纸标准结构）|
| `update` | 更新已有 Battle Card（季度迭代）|
| `library` | 输出全部对手的 Battle Card 库索引 + 维护清单 |

## 使用示例

```
/battle-card Splunk --mode build --tier 1 --industry fintech
/battle-card 某国内 SIEM 厂商 --mode build --tier 2
/battle-card Splunk --mode update    # 季度更新
/battle-card --mode library          # 查看全部对手
```

## 执行流程

```
Step 1: 对手定位
  → 一句话：对手核心定位 + 主要服务客户类型
  → 对手类型分类（国际大厂 / 国内大厂 / 垂直 / 创业 / 开源 / 替代品类）

Step 2: 三大杀手锏
  → 在 [对手] 面前必赢的 3 点（量化对比）
  → 来源：公开 benchmark / 客户案例 / 第三方报告

Step 3: 三个雷区
  → 在 [对手] 面前必败 / 必躲 3 点
  → 每条配应对话术（肯定 + 转移 / 维度重构 / 客户故事）

Step 4: 价格锚点
  → 对手典型报价（来源：销售情报 / 第三方 / 客户透露）
  → 我方对位报价 + 谈判要点

Step 5: 标准应答
  → "为什么不用 [对手]" 30 秒应答
  → "[对手] 有 X 功能你们有吗" 三类应答（有 / 没有 / roadmap）

Step 6: 关键人画像
  → EB / TB / Champion 视角下的对手形象
  → 常见 Champion 反对对手的理由

Step 7: 内部使用提示（仅内部）
  → 对手负面新闻 / 客户流失 / 高管变动
  → 已知合规缺口 / 漏洞 / 失败案例
  → 已挖到的对手客户原话引用（脱敏）

Step 8: 红线检查
  → 不直接贬低 / 不编造缺陷 / 不比较未公开数据 / 不攻击对手客户
```

## 与其他命令的边界

| 选择 | 用前者 | 用后者 |
|------|-------|-------|
| `/battle-card` vs `/market-research` | 一页纸销售弹药 | 几千字深度报告 |
| `/battle-card` vs `/sales-guide` | 对手专项 | 销售一页禅（产品总体）|
| `/battle-card` vs `/win-loss` | 实时应对（赛前）| 复盘学习（赛后）|
| `/battle-card` vs `/gtm-strategy` | 销售前线弹药 | 整体上市战略 |
