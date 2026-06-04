---
name: customer-success
description: >
  B 端客户成功管理 — 客户全生命周期运营。覆盖客户实施 Onboarding（30/60/90 天计划）、
  客户健康度评分（使用深度 + 关键事件 + NPS + 续约信号）、续约预测（红黄绿分级）、
  Land & Expand 扩展销售、流失预警与挽留、客户分层运营（Tier 1/2/3）。
  
  与相邻命令的边界（防混淆）：
  - vs /account-plan：本命令是"标准客户全生命周期 SOP"，按分层批量管理；
    /account-plan 是"战略大客户深度 Plan"，按客户单独经营（Power Map / 白空间）。
  - vs /poc-plan：本命令负责签约后的实施；/poc-plan 负责签约前的试点。
  - vs /sla-design：本命令是"客户成果承诺"，/sla-design 是"合同条款承诺"。
  适用于：CSM 团队搭建、新客户实施、健康度看板、续约阶段管理、客户扩展销售。
user-invocable: true
argument-hint: "<客户名/产品> [--mode onboarding|health|renewal|expand|churn|fullset] [--tier 1|2|3] [--stage day0-30|day30-90|day90-365|renewal]"
---

# /customer-success — B 端客户成功管理

加载技能：`skills/customer-success/SKILL.md`

## 触发条件
新客户实施启动、需要量化客户健康度、续约前评估、规划 Land & Expand 扩展销售、识别流失风险并设计挽留方案、CSM 团队工作流搭建时。

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `<客户名/产品>` | 客户全称 / 产品（必填） | — |
| `--mode` | 工作模式 | `onboarding` |
| `--tier` | 客户分层 | — |
| `--stage` | 客户旅程阶段 | — |

### 工作模式（--mode）
| 值 | 输出 | 适用场景 |
|----|------|---------|
| `onboarding` | 30/60/90 天实施计划 + 关键里程碑（**默认**） | 新客户启动 |
| `health` | 健康度评分模型 + 看板 + 告警 | 客户运营常态 |
| `renewal` | 续约预测 + Playbook（红/黄/绿）+ 谈判材料 | T-90/T-30 续约 |
| `expand` | Land & Expand 机会识别 + 扩展销售脚本 | 已 PMF 客户增长 |
| `churn` | 流失预警 + 挽留 SOP + Win-back | 流失迹象出现 |
| `fullset` | 完整 CSM 体系（含分层运营 SOP） | CSM 团队搭建 |

### 客户分层（--tier）
| 值 | 标准 | 服务力度 |
|----|------|---------|
| `1` | 战略客户（ARR Top 5% / 标杆） | 专属 CSM + 月度 QBR |
| `2` | 重点客户（ARR Top 25%） | 共享 CSM + 季度 QBR |
| `3` | 长尾客户 | Pooled CSM + 自助 |

### 客户旅程阶段（--stage）
| 值 | 重点 |
|----|------|
| `day0-30` | 实施 + 关键人培训 + 首次成功 |
| `day30-90` | 价值证明 + 第二批用户接入 |
| `day90-365` | 业务嵌入 + 扩展机会识别 |
| `renewal` | 续约前 90/60/30 天阶段 |

---

## 执行流程（onboarding 模式）

```
Step 1: 客户信息盘点
  → 合同金额 / 用户数 / 行业 / 部署模式（SaaS / 私有）
  → 关键人地图（Sponsor / Champion / Decision Maker / End User）
  → 客户的"成功"定义（业务指标 + 时间预期）

Step 2: 30 天计划（首次成功 First Value）
  → W1：Kick-off + 项目章程 + 时间表
  → W2：账号开通 + SSO/SCIM 配置 + 数据迁移
  → W3：核心用户培训 + 首批 5-10 个真实用例
  → W4：First Value 验证 + 客户内部宣讲

Step 3: 60 天计划（业务嵌入）
  → 第二批用户接入（10-50 人）
  → 关键 SOP 文档化
  → 数据看板上线
  → 月度健康度复盘启动

Step 4: 90 天计划（价值证明）
  → 业务影响量化报告（ROI 对比）
  → 客户成功故事采访
  → 季度 QBR 准备
  → 扩展机会识别

Step 5: 健康度初次评分
  → 启动健康度监测
  → 设定预警阈值
```

---

## 输出示例（onboarding 模式 - 30/60/90 天）

```markdown
# Acme Corp 客户实施计划

**合同**：ARR ¥80 万 | **用户数**：120 | **行业**：金融
**关键人**：
- Sponsor：CIO 张总（决策最终拍板）
- Champion：技术总监 李总（推动者）
- 主用户群：信审团队 + 风控团队

**客户成功定义**：3 个月内信审效率提升 40%

## 30 天：First Value（关键里程碑）

### W1（Kick-off）
- [ ] D+1：项目启动会（双方核心团队 + 周会节奏）
- [ ] D+3：项目章程签署（成功标准 + 责任矩阵 + 升级路径）
- [ ] D+5：客户技术对接（SSO / SCIM / 网络）

### W2（基础就绪）
- [ ] 账号开通 + SSO 联调通过
- [ ] 数据迁移演练（历史数据 6 个月）
- [ ] 客户安全合规审查通过

### W3（用户培训）
- [ ] 核心用户培训 1 场（10 人，含视频回放）
- [ ] 首批 5 个真实用例上线
- [ ] 1on1 答疑 3 场

### W4（First Value 验证）
- [ ] First Value 量化（如：5 个用例的效率提升）
- [ ] 客户内部宣讲会（Champion 主讲）
- [ ] 30 天复盘 + 60 天计划确认

## 60 天：业务嵌入

### W5-W8
- [ ] 第二批用户接入（120 人全员）
- [ ] 关键 SOP 文档化（5 篇）
- [ ] 数据看板上线 + 客户专属指标
- [ ] 月度健康度复盘开启

## 90 天：价值证明 + QBR

### W9-W13
- [ ] 业务影响量化报告（vs baseline）
- [ ] 客户成功故事采访（视频 + 案例文档）
- [ ] 季度 QBR（高管层 + Sponsor 出席）
- [ ] 扩展机会评估（其他部门 / 子产品）

## 关键风险与应对
| 风险 | 应对 | Owner |
|------|------|-------|
| 数据迁移延期 | 提前 W2 启动备份 | CSM + 客户 IT |
| 用户抵触 | Champion 内部宣讲 + 激励 | Champion |
| 安全合规延期 | W1 启动法务审 | CSM + 法务 |

## 健康度监测启动
- D+30：首次健康度评分
- 预警阈值：< 60 分立即介入
- 告警通道：Slack #cs-acme + 客户群
```

---

## 输出示例（health 模式 - 健康度评分）

```markdown
# Acme Corp 客户健康度模型

## 评分公式（0-100 分）

| 维度 | 权重 | 数据源 | 计算 |
|------|------|--------|------|
| 使用深度 | 35% | 产品埋点 | 周活用户/总用户 × 关键功能使用率 |
| 关键事件 | 20% | CRM | 培训完成 / SOP 发布 / Champion 在职 |
| NPS / 满意度 | 15% | 调研 | NPS ≥ +30 = 100，每 -10 减 20 |
| 业务影响 | 15% | 客户提供 | 是否有量化 ROI |
| 续约信号 | 15% | 销售信息 | 高管见面 / 扩展讨论 |

## 红黄绿分级
- 🟢 绿（80-100）：扩展销售机会
- 🟡 黄（60-79）：常规运营
- 🔴 红（< 60）：立即介入 + 升级到 VP CS

## Acme Corp 当前评分：72（🟡 黄）
| 维度 | 分 | 说明 |
|------|----|----|
| 使用深度 | 28 / 35 | 周活 90%，但高级功能仅 30% |
| 关键事件 | 18 / 20 | Champion 稳定，培训已完成 |
| NPS | 12 / 15 | NPS +25 |
| 业务影响 | 8 / 15 | 量化 ROI 未做（重点） |
| 续约信号 | 6 / 15 | 高管半年未见 |

## 行动建议
1. **重点**：本月安排业务影响量化项目（+7 分潜力）
2. 下季度高管 1on1（+5 分）
3. 推动高级功能采用（+5 分）

## 自动告警
- 健康度连续 30 天 < 60 → 升级到 VP CS
- 关键事件中 Champion 离职 → 立即响应
- 使用深度月环比 -20% → 红色告警
```

---

## 输出示例（renewal 模式 - 续约 Playbook）

```markdown
# Acme Corp 续约管理（合同到期：2026-12-31）

## T-90 天（2026-10-02）
- [ ] 健康度复盘 + 评分
- [ ] 续约预测（红/黄/绿）
- [ ] 续约材料启动准备

## T-60 天（2026-11-01）
- [ ] 业务影响报告（年度 ROI 量化）
- [ ] 续约方案（同价 / 涨价 / 降价 / 扩展）
- [ ] Sponsor 沟通会

## T-30 天（2026-12-01）
- [ ] 报价正式提交
- [ ] 法务条款对齐
- [ ] 谈判时间锁定

## T-7 天
- [ ] 合同签署
- [ ] 续约 Kick-off

## 续约预测：🟢 绿（高确定性）
**理由**：
- 健康度 80+
- 业务嵌入深（信审团队 100% 使用）
- 高管支持（Q3 收到 CIO 推荐信）

**风险**：
- 竞品 Y 低价试探（已知）
- 应对：突出生态绑定 + 已有数据迁移成本

## 续约方案
| 方案 | 价格 | 说明 |
|------|------|------|
| Renew Same | ¥80 万 | Baseline |
| Renew + Upsell ⭐ | ¥120 万 | 推荐：扩展到 200 用户 + 新模块 |
| Multi-Year | ¥220 万 / 3 年 | 锁定 + 8% 折扣 |

## 关键人沟通
- Sponsor (CIO)：1 次面谈（业务价值 + 战略对齐）
- Champion (技术总监)：周会同步
- 财务总监：报价细节 + 付款条款
- 采购总监：合同流程
```

---

## 输出示例（expand 模式 - Land & Expand）

```markdown
# Acme Corp 扩展机会评估

## 现状
- 当前：信审团队 120 用户 / ARR ¥80 万
- 业务影响已验证：信审效率 +45%

## 扩展机会矩阵

| 机会 | 预估 ARR | 概率 | 周期 | Owner |
|------|---------|------|------|-------|
| 风控团队接入（80 人） | ¥40 万 | 80% | Q3 | 张 CSM |
| 信审模块升级（高级 AI） | ¥30 万 | 60% | Q4 | 销售 |
| 海外子公司试点（30 人） | ¥20 万 | 30% | Q4 | 销售 + CSM |
| API 集成（CRM 联动） | ¥10 万 | 90% | Q3 | CSM |

## 优先级行动
1. ⭐ 风控团队 + API 集成（高确定性）
2. 信审升级（基于 ROI 报告说服）
3. 海外（探索性 + 长周期）

## 扩展销售脚本
**对 CIO**：
> "信审团队的 ROI 已验证 45% 效率提升。风控团队和信审有 60% 流程重叠，
> 我们做了快速估算，预计 6 个月可达成类似效果。是否本月安排技术调研会？"

**对财务总监**：
> "如果同时扩展风控 + API 集成，年度合同 ¥120 万对应业务价值约 ¥600 万
> （信审 + 风控合并人效），ROI 5:1。"
```

---

## 与其他命令的协同

```
/customer-success（本命令）
  ├── /account-plan       → 大客户专属 Plan + QBR
  ├── /sla-design         → 客户合同的 SLA 条款
  ├── /poc-plan           → 实施前的 PoC 转正式
  ├── /feedback           → NPS / VoC 健康度数据源
  ├── /data-dashboard --type customer-br → 客户级看板
  ├── /pricing-strategy   → 续约 Upsell 报价
  ├── /retrospective      → 客户失败 / 续约成功复盘
  └── /stakeholder        → 客户内部多关键人沟通

推荐工作流：
  新客户上线：
    /poc-plan → 验证通过
    → /customer-success --mode onboarding
    → D+30 后 /customer-success --mode health
    → 持续 /data-dashboard --type customer-br

  续约管理：
    T-90 /customer-success --mode renewal
    → /account-plan（大客户）
    → /pricing-strategy（Upsell 报价）
    → 签约 → /customer-success --mode expand
```

---

## 使用示例

```bash
# 新客户实施 30/60/90 天计划（默认）
/customer-success Acme Corp --tier 1

# 健康度评分模型
/customer-success Acme Corp --mode health

# 续约前 90 天准备
/customer-success Acme Corp --mode renewal --stage renewal

# Land & Expand 机会
/customer-success Acme Corp --mode expand

# 流失预警 + 挽留
/customer-success Beta Inc --mode churn

# CSM 团队整体搭建（含分层 SOP）
/customer-success 全产品 CSM 体系 --mode fullset

# 长尾客户分层运营
/customer-success 中小客户池 --tier 3 --mode fullset
```
