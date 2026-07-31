---
description: Churn 流失分析与 Save Playbook — 把客户流失转化为产品/体验/商业改进（含 CHI 客户健康度 + Save Play 三级 + Win-Back）
argument-hint: "[时间区间 / 客户群]"
---

# /churn-analysis — 流失分析 + 挽留剧本

加载技能：`skills/churn-analysis/SKILL.md`

请基于以下输入做 Churn 分析：

$ARGUMENTS

## 工作流程

### 第 1 步：流失分类

按 5 类划分：
1. 产品不达标（< 30%）
2. 价格 / 商业模型（< 20%）
3. 客户成功失败（< 20%）
4. 客户内部变化（不可控）
5. 竞品迁移（< 10%）

### 第 2 步：5 Whys 根因

对每个流失客户追问 5 层：
- 为什么流失？
- 为什么 X？
- ……（至少 5 次）

### 第 3 步：流失漏斗

```
全部续约期客户 → 风险客户（CHI ≤ 40）→ 触发 Save Play → 挽留成功 / 失败
```

### 第 4 步：CHI（客户健康度）设计

```
CHI = 
  使用频率 × 30% + 功能广度 × 20% + 关键事件 × 15% +
  反馈情绪 × 15% + 财务行为 × 10% + Champion 状态 × 10%
```

分层：
- 80-100 Healthy（升级机会）
- 60-79 Stable（QBR 维持）
- 40-59 At Risk（Save Play 1）
- 20-39 Critical（Save Play 2）
- 0-19 Lost（Save Play 3 / Win-Back 名单）

### 第 5 步：Save Play 三级

| 等级 | 触发 | 行动 |
|------|------|------|
| Save 1 | CHI 40-59 | CSM 主动 → Day 0 关心邮件 → Day 7 电话 → Day 30 跟进 |
| Save 2 | CHI 20-39 | Save Squad（3-5 人）+ 客户高层会议 |
| Save 3 | < 20 / 已通知 | 漂亮离场 + 离场访谈 + Win-Back 名单 |

### 第 6 步：Win-Back 名单

流失 6-12 个月后回访，触发条件：
- 你方有重大产品改进
- 竞品出问题
- 客户 Champion 跳槽
- 客户业务扩张

B 端 Win-Back 转化率 5-15%。

## 输出格式

```markdown
# Churn 分析报告 — {时间区间}

## 一、TL;DR
- Logo Churn: N%（vs 上期 ±%）
- NRR / GRR: %
- 关键根因 Top 3
- 3 个最重要 Action

## 二、流失客户列表

| 客户 | ARR | 类别 | 真实原因 | CSM 早期识别 |
|------|-----|------|----------|--------------|

## 三、根因聚类

| # | 根因 | 占比 | 是否可控 |

## 四、流失漏斗

| 阶段 | 客户数 | 漏斗率 |
| 全部续约期客户
| CHI 进入 At Risk
| 触发 Save Play
| 挽留成功
| 流失

## 五、Save Play 效果

| 等级 | 触发数 | 挽留成功 | 成功率 |

## 六、Action Items
### 产品改进
### 商业模型
### 客户成功流程

## 七、ICP 修正
- 流失最多客户特征 → 不该再卖
- 续约最好客户特征 → 重点投入

## 八、Win-Back 名单

| 客户 | 流失原因 | Win-Back 触发条件 | 跟进人 |

## 九、关联资源
- 数据看板：`/dashboard --metric customer-br`（客户健康度看板）
- 用户研究（离场访谈）：`/user-research --mode interview`
- 销售对账：`/win-loss`
```

## 红线（不要做）

- ❌ 流失发生才发现（CHI 不到位）
- ❌ CSM 一人扛（没 Save Squad）
- ❌ 客户说价格贵就调价（80% 真因不是价格）
- ❌ 不做离场访谈（丢失最值钱数据）
- ❌ Win-Back 名单只有名字没有触发条件
