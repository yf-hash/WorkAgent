---
name: product-report
description: >
  产品周报 / 月报 / 季度报告生成器。覆盖产品周报（Weekly Update / 5+5+5 模板）、
  产品月报（北极星 + 漏斗 + 实验 + 风险）、季度评分报告（OKR + Roadmap + 学习沉淀）、
  董事会汇报（Board Update）模板。区分受众（团队 / 高管 / 董事会 / 客户）输出适配。
  适用于：双周邮件、月度高管汇报、季度董事会、客户 Business Review。
user-invocable: true
argument-hint: "<时间窗口/产品> [--mode weekly|monthly|quarterly|board|customer-br] [--audience team|exec|board|customer] [--length brief|standard|detailed]"
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
    danger-level: low
---

# /product-report — 产品周报/月报/季度报告

加载技能：`skills/strategy/product-report/SKILL.md`

## 触发条件
需要写产品周报、月度高管汇报、季度董事会报告、客户 Business Review，或想建立可复用的产品报告模板时。

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `<时间窗口/产品>` | 报告范围（必填） | — |
| `--mode` | 报告类型 | `weekly` |
| `--audience` | 受众 | `team` |
| `--length` | 篇幅 | `standard` |

### 报告类型（--mode）
| 值 | 输出 | 频次 |
|----|------|------|
| `weekly` | 产品周报（5+5+5 模板）（**默认**） | 每周一 |
| `monthly` | 月度产品报告（北极星 + 漏斗 + 实验） | 每月初 |
| `quarterly` | 季度评分报告（OKR + Roadmap + 学习） | 每季初 |
| `board` | 董事会更新（数字 + 战略 + 风险） | 每季 / 半年 |
| `customer-br` | 客户 Business Review（KPI 履约 + 路线图） | 季度 / 年度 |

### 受众（--audience）
| 值 | 关注点 | 风格 |
|----|--------|------|
| `team` | 战术 / 协作 / 阻塞 | 详细、互动 |
| `exec` | 战略 / 数字 / 风险 | 高度浓缩、决策点 |
| `board` | 商业 / 财务 / 战略 | 数字驱动、长周期 |
| `customer` | 价值履约 / 路线图 | 商业语言、具体案例 |

### 篇幅（--length）
| 值 | 字数 |
|----|------|
| `brief` | < 300 字（一屏） |
| `standard` | 500-1500 字（**默认**） |
| `detailed` | 2000+ 字 |

---

## 周报模板（weekly + team）

```markdown
# 产品周报 W[N]：[周日期]

**作者**：[PM] | **日期**：YYYY-MM-DD

## 5 个亮点（What went well）
1. [里程碑 / 成就]：[一句话 + 数字]
2. ...
3. ...
4. ...
5. ...

## 5 个挑战（Lowlights / Blockers）
1. [问题]：[原因 + 我们的应对]
2. ...

## 5 个下周聚焦（Next week's focus）
1. [行动]：[Owner + 截止]
2. ...

## 关键数字（Key Metrics）
| 指标 | 上周 | 本周 | 变化 |
|------|------|------|------|
| 北极星 | X | Y | +Z% |
| 主漏斗转化 | X% | Y% | ±Zpp |

## 实验进展
- [实验名]：[状态] | [结果] | [决策]

## 需要你帮忙
- [资源 / 决策诉求 + Owner]
```

---

## 月报模板（monthly + exec）

```markdown
# 产品月报 [YYYY-MM]：[产品名]

**作者**：[PM] | **日期**：YYYY-MM-DD

## 一句话结论（30 秒读完）
> "本月 [核心成就 / 数字]，下月将 [关键行动]，需要您 [决策点]"

## 北极星指标
| 指标 | 上月 | 本月 | 季度目标 | 趋势 |
|------|------|------|---------|------|
| NSM | X | Y | Z | ↗️ / →/ ↘️ |

## 漏斗健康
```
访问 100K → 注册 12K (12%) → 激活 7K (58%) → 付费 1.5K (21%)
                  ↑ +2pp                        ↑ -3pp
                  实验 A 生效                    定价 A/B 待优化
```

## 关键里程碑
- ✅ [已完成]：[影响]
- 🟡 [进行中]：[进度 + 预计]
- 🔴 [延期]：[原因 + 应对]

## 实验复盘（本月）
| 实验 | 假设 | 结果 | 决策 |
|------|------|------|------|
| A | ... | +1.7pp ✅ | 全量 |
| B | ... | 不显著 | 改设计 |
| C | ... | 进行中 | W2 出 |

## 风险与我们的应对
| 风险 | 影响 | 应对 | 升级到您 |
|------|------|------|---------|
| [...] | [...] | [...] | 是 / 否 |

## 下月计划
1. [Top 1]
2. [Top 2]
3. [Top 3]

## 需要您的决策 / 支持
- [一句话决策点]：[选项 A / B / C]，截止 [日期]
```

---

## 季度报告模板（quarterly）

```markdown
# Q[N] 产品季度报告：[产品]

**Owner**：[PM] | **周期**：YYYY-Q[N]

## 执行摘要（50 字）
> [本季度核心成果 + 下季度方向]

## OKR 评分
| Objective | KR 综合评分 | 评价 |
|-----------|------------|------|
| O1: ... | 0.85 | ✅ |
| O2: ... | 0.45 | ⚠️ |
| O3: ... | 0.70 | ✅ |

## 北极星变化
[12 周变化曲线 + 同比]

## 关键交付
- ✅ [交付物 1]：[影响]
- ✅ [交付物 2]：[影响]

## 学习与失败
- 学习：[一句话]
- 失败：[一句话 + 我们的处理]

## 下季度规划
1. [O1 + KR 摘要]
2. [O2 + KR 摘要]
3. [O3 + KR 摘要]

## 资源诉求
- [资源 1]：[理由]
- [资源 2]：[理由]
```

---

## 董事会汇报模板（board）

```markdown
# Q[N] 董事会更新：[产品]

## 北极星
- 当前：X
- 季度目标：Y
- YoY：+Z%

## 商业指标
| 指标 | Q-1 | 本 Q | YoY |
|------|------|------|-----|
| MRR / ARR | $X | $Y | +Z% |
| 付费用户 | X | Y | +Z% |
| 净留存 NRR | X% | Y% | +Zpp |
| CAC | $X | $Y | -Z% |
| 毛利率 | X% | Y% | ↑ |

## 战略进展（3 条）
1. [战略主题]：[进展]
2. ...
3. ...

## 主要风险
| 风险 | 影响 | 应对 |
|------|------|------|

## 提请董事会决策
- [决策点 1]
- [决策点 2]

## 附录
- 详细 OKR / 财务 / 用户数据
```

---

## 客户 BR 模板（customer-br）

```markdown
# [客户名] Q[N] Business Review

## 价值履约总结
本季度我们为您实现了：
- [指标 1]：[数值] → [价值 $]
- [指标 2]：[数值] → [价值 $]
- 估算总价值：$ X (vs 您的成本 $ Y → ROI Z%)

## 使用情况
| 指标 | 上季 | 本季 | 趋势 |
|------|------|------|------|
| 活跃用户数 | X | Y | ↗️ |
| 关键功能使用 | X | Y | ↗️ |

## 您的反馈与我们的响应
| 您提出的 | 我们的进展 | 上线 |
|---------|----------|------|
| [问题 1] | ✅ 已解决 | YYYY-MM |
| [问题 2] | 🟡 进行中 | YYYY-MM |

## 即将到来（路线图）
- [功能 1]：[Q+1]
- [功能 2]：[Q+2]

## 续约 / 扩展讨论
- 当前合同：到期 YYYY-MM-DD
- 推荐方案：[续约 / 升级 / 扩展用户数]
```

---

## 与其他命令的协同

```
/product-report（本命令）
  ├── /roadmap → 月报里程碑
  ├── /analytics → 北极星 / 漏斗数据
  └── /ab-test → 本月实验复盘

推荐节奏：
  每周一上午：/product-report --mode weekly
  每月 1 日：/product-report --mode monthly --audience exec
  每季初：/product-report --mode quarterly + 董事会另发 board
  每季客户：/product-report --mode customer-br
```

---

## 使用示例

```bash
# 产品周报（默认）
/product-report W42 2026

# 月度高管汇报
/product-report 2026-05 月报 --mode monthly --audience exec

# 季度评分报告
/product-report Q1 2026 --mode quarterly

# 董事会更新
/product-report Q1 2026 --mode board --audience board

# 客户 BR
/product-report 客户 Acme Corp Q1 --mode customer-br --audience customer

# 简短一屏团队周报
/product-report W42 --mode weekly --length brief

# 详细月报
/product-report 2026-05 --mode monthly --length detailed
```
