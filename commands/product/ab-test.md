---
name: ab-test
description: >
  A/B 实验设计与分析助手。覆盖假设设计、样本量估算（含 Power Analysis）、分流策略（流量切分/分层正交/独占）、显著性检验（双尾 t / 卡方 / Bayes）、护栏指标体系、SRM 检测、辛普森悖论防范、实验结果解读模板。适用于：注册转化率优化、定价 A/B、UX 改版、推荐算法、AI 模型上线灰度。
user-invocable: true
argument-hint: "<实验目标> [--mode design|sizing|analyze|guardrails|fullset] [--metric <指标>] [--mde <最小可检测效应>] [--alpha 0.05] [--power 0.8] [--platform posthog|growthbook|optimizely|custom]"
---

# /ab-test — A/B 实验设计与分析

加载技能：`skills/data/ab-test/SKILL.md`

## 触发条件
需要设计 A/B 实验、估算样本量、定义实验护栏指标、解读实验结果，或避免 A/B 实验常见陷阱（SRM/辛普森悖论/抢跑停车）时。

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `<实验目标>` | 实验假设或要优化的指标（必填） | — |
| `--mode` | 工作模式 | `design` |
| `--metric` | 主指标 | — |
| `--mde` | 最小可检测效应（如 0.02 = 2%） | — |
| `--alpha` | 一类错误率 | `0.05` |
| `--power` | 统计功效 | `0.8` |
| `--platform` | 实验平台 | `posthog` |

### 工作模式（--mode）
| 值 | 输出 | 适用场景 |
|----|------|---------|
| `design` | 实验设计文档（**默认**） | 实验启动前 |
| `sizing` | 样本量计算 + 实验时长估算 | 设计完了再算量级 |
| `analyze` | 结果分析 + 显著性判定 + 解读 | 实验跑完 |
| `guardrails` | 护栏指标体系 + SRM 检测方案 | 大规模实验上线前 |
| `fullset` | 完整四件套（设计+样本+护栏+分析模板） | 重要实验完整计划 |

### 实验平台（--platform）
| 值 | 特点 |
|----|------|
| `posthog` | 开源、含 Feature Flag 和 Experiment 模块 |
| `growthbook` | 开源、Bayes 优先、SQL 集成强 |
| `optimizely` | 商业平台、前端实验深 |
| `custom` | 自建（基于哈希分桶 + 数仓） |

---

## 执行流程（design 模式）

```
Step 1: 实验假设结构化
  → 用 "If we [变更] for [对象]，then [指标] will [方向]，because [理由]"

Step 2: 主指标选择
  → 必须可在实验时长内观测到（OEC: Overall Evaluation Criterion）
  → 与北极星指标方向一致
  → 不易被 Bot/异常用户污染

Step 3: 护栏指标
  → 不可变差的指标（性能/错误率/反向漏斗）
  → 至少 2 个：1 个用户体验 + 1 个业务底线

Step 4: 分流策略
  → 单一实验：50/50 简单切分
  → 多实验同时跑：分层正交（Layer-Orthogonal）
  → 独占实验：互斥层
  → 避免污染：用户级 sticky bucketing

Step 5: 样本量与时长估算
  → 基于 baseline + MDE + α + power
  → 校正多重比较（Bonferroni / FDR）
  → 估算最短运行时长（覆盖业务周期，至少 1-2 周）

Step 6: 失败模式自检
  → SRM (Sample Ratio Mismatch) 检测方案
  → 抢跑停车 / 偷看 / Peeking 防范
  → 辛普森悖论 / 选择偏差识别
```

---

## 输出示例（design 模式）

```markdown
# A/B 实验设计：[实验名]

## 1. 假设
**If** 我们将 [对照组] 改为 [实验组]
**For** [目标用户群]
**Then** [主指标] 将 [上升/下降] [MDE]
**Because** [背后机制 / 用户洞察]

## 2. 实验信息
| 项目 | 内容 |
|------|------|
| 主指标 (OEC) | [指标名 + 计算口径] |
| 当前 baseline | [当前数值] |
| MDE | [最小可检测效应] |
| α / Power | 0.05 / 0.8 |
| 样本量/组 | [N] |
| 估算时长 | [N 天] |
| 流量分配 | A=50% / B=50% |
| 分桶单位 | user_id（持久化） |

## 3. 护栏指标
| 指标 | 不可变差幅度 |
|------|------------|
| 页面加载 P95 | < +10% |
| JS Error 率 | < +0.1% |
| 转化主漏斗第 N 步 | < -1% |

## 4. 实施计划
- 实验代码 PR：[链接]
- Feature Flag Key：experiment_xyz
- Tracking 事件：experiment_assigned / [关键事件]
- 数据校验 SQL：[查询]

## 5. 决策矩阵
| 主指标 | 护栏 | 决策 |
|--------|------|------|
| 显著上升 | 通过 | ✅ 全量发布 |
| 显著上升 | 部分变差 | ⚠️ 评估权衡 |
| 不显著 | 通过 | ⏸️ 加大样本 / 改方案 |
| 显著下降 | — | ❌ 立即下线 |

## 6. 风险与应对
- [风险]：[应对]
- 预案：实验过程发现 SRM/异常 → 立即停止
```

---

## 输出示例（sizing 模式）

```markdown
# 样本量估算

## 输入参数
- baseline 转化率：12%
- MDE（绝对值）：1.5pp（即从 12% → 13.5%）
- α：0.05（双尾）
- Power：0.8

## 计算结果（双比例 z 检验）
- 每组样本量：≈ 9,400 用户
- 总样本：≈ 18,800
- 日均流量：5,000 → 实验时长 ≈ 4 天
- 建议运行时长：≥ 7 天（覆盖周期效应）

## 备注
- 多实验并行需校正：Bonferroni → α/3 = 0.0167
- 分层不均匀（如 < 5%）需扩样本
- 异常值/僵尸用户预留 5-10% buffer
```

---

## 输出示例（analyze 模式）

```markdown
# A/B 实验结果分析

## 主指标
| 组 | N | 转化率 | 95% CI |
|----|---|--------|--------|
| A | 9420 | 12.0% | [11.3%, 12.7%] |
| B | 9388 | 13.7% | [13.0%, 14.4%] |

**绝对提升**：+1.7pp（+14.2% 相对）
**p 值**：0.001（双尾）→ ✅ 显著
**置信区间不重叠** → 加强信号

## 护栏检查
- ✅ 性能 P95：A 1850ms / B 1820ms（无劣化）
- ✅ Error 率：A 0.05% / B 0.04%
- ⚠️ SRM：A=50.2% B=49.8%，χ² p=0.78（无 SRM）

## 分群分析
| 维度 | A | B | Delta |
|------|---|---|-------|
| 新用户 | 8.0% | 11.5% | +3.5pp ✅ |
| 老用户 | 16.0% | 16.2% | +0.2pp |

→ 实验主要在新用户上奏效，老用户无差异

## 决策
✅ 全量发布
- 优先在新用户漏斗加速推全
- 老用户可不加速（避免无效折腾）

## 后续监测
- 上线后 4 周持续观察留存指标
- 关注首单转化是否带来 D7/D30 留存提升
```

---

## 与其他命令的协同

```
/ab-test（本命令）
  ├── /analytics → 提供 baseline 数据 + 埋点设计
  ├── /mvp-canvas → MVP 上线后做 A/B 验证假设
  └── /pricing-strategy → 定价 A/B 测试

推荐工作流：
  增长实验：
    /ab-test --mode design
    → /ab-test --mode sizing
    → 上线
    → /ab-test --mode analyze
```

---

## 使用示例

```bash
# 设计实验（默认）
/ab-test 注册按钮文案改为"免费试用"是否提升转化

# 样本量估算
/ab-test 首页推荐改版 --mode sizing --metric ctr --mde 0.02

# 结果分析
/ab-test Q4 定价 A/B 结果 --mode analyze

# 大规模实验护栏
/ab-test 推荐算法 v2 上线 --mode guardrails

# 完整四件套（重要实验）
/ab-test 引导流程改版 --mode fullset --platform posthog --mde 0.03

# 自定义平台 + Bayes
/ab-test 搜索排序改版 --platform growthbook --mode design
```
