---
name: poc-plan
description: >
  PoC（Proof of Concept）/ 试点管理 — B 端销售决战环节。覆盖
  PoC 范围谈判（不让客户白嫖、防止无限试用）、成功标准定义（量化 + 时限 +
  退出机制）、PoC SOW 模板、关键节点与验收会、PoC 转正式合同 SOP、
  PoC 失败的体面退出、试点期定价（折扣 vs 转正）、批量 PoC 池管理。
  适用于：销售推进新客户、技术 PoC 启动、试点项目治理、PoC 转化率优化。
user-invocable: true
argument-hint: "<客户名/产品> [--mode scope|sow|review|convert|fullset] [--type technical|business|hybrid] [--duration 2w|4w|8w|12w]"
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

# /poc-plan — PoC / 试点管理

加载技能：`skills/presales/poc-plan/SKILL.md`

## 触发条件
新客户在销售周期中要求 PoC 验证、技术 POC 启动需要范围谈判、PoC 进行中需要里程碑验收、PoC 结束转正式合同、批量 PoC 管理。

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `<客户名/产品>` | 客户名 / PoC 产品（必填） | — |
| `--mode` | 工作模式 | `fullset` |
| `--type` | PoC 类型 | `hybrid` |
| `--duration` | PoC 时长 | `4w` |

### 工作模式（--mode）
| 值 | 输出 | 适用场景 |
|----|------|---------|
| `scope` | 范围谈判 + 成功标准 | PoC 启动前 |
| `sow` | PoC SOW 协议（合同附件） | 协议起草 |
| `review` | 周会 + 阶段验收议程 | PoC 中期 |
| `convert` | PoC → 正式合同 SOP | PoC 末期 |
| `fullset` | 完整 PoC 项目（4 项合一）（**默认**） | 销售关键 |

### PoC 类型（--type）
| 值 | 重点 |
|----|------|
| `technical` | 技术可行性（性能 / 集成 / 兼容） |
| `business` | 业务价值（ROI / 工作流匹配） |
| `hybrid` | 同时验证（**默认**，最常见） |

### 时长（--duration）
| 值 | 适合 |
|----|------|
| `2w` | 极简验证（默认 SaaS） |
| `4w` | 标准（**默认**） |
| `8w` | 深度（含集成 / 多用户） |
| `12w` | 复杂（金融 / 大型企业） |

---

## 执行流程（fullset 模式）

```
Step 1: PoC 资格预审
  → 客户已确认预算（避免白嫖）
  → 决策链清晰（DMU 已知）
  → 成功后有明确转正时间表

Step 2: 范围谈判（最关键）
  → 验证什么（具体场景，3-5 个）
  → 不验证什么（明确排除）
  → 哪些用户（数量 + 角色）
  → 哪些数据（脱敏 vs 真实）
  → 哪些环境（生产 / 沙盒 / 测试）

Step 3: 成功标准定义
  → 必须可量化
  → 必须有时限
  → 必须双方书面确认
  → 必须含失败的"退出条件"

Step 4: SOW 协议起草
  → 范围 + 标准 + 时间盒 + 双方责任
  → 客户授权（数据 / 系统访问）
  → IP 归属（PoC 中的代码 / 配置）
  → 失败的处理（钱退？还是已耗费？）

Step 5: 项目执行
  → Kick-off + 周会 + 中期 Review
  → 阶段性验收
  → 风险升级路径

Step 6: 转正决策
  → 成功 → 立即谈合同（避免拖延）
  → 失败 → 体面退出 + 后续机会留白

Step 7: 复盘
  → 成功转正：标杆案例 + 销售故事
  → 失败：进入失败 PIR
```

---

## 输出示例（fullset 模式）

```markdown
# Acme Corp PoC 计划

**销售 Owner**：王 AE | **PreSales**：李 PreSales | **Tech Lead**：张 SE
**PoC 类型**：Hybrid（技术 + 业务）
**时长**：4 周（D-Day：2026-07-01 到 2026-07-29）
**预算**：客户已经口头确认 ¥100 万年合同

---

## 一、范围（Scope）

### ✅ 验证范围
1. **技术验证**：
   - 与客户 SAP 系统集成（数据双向同步）
   - 单租户 1000+ QPS 性能
   - SSO（Azure AD）联调

2. **业务验证**：
   - 信审团队 20 人 7 天工作流
   - 5 个真实信审用例端到端跑通
   - 效率提升 ≥ 30%（vs 现有方案）

### ❌ 不在范围
- 风控团队接入（后续合同范围）
- 移动端（暂只支持 Web）
- 自定义模板开发（用标准模板）
- 数据迁移（客户提供 100 条样本数据即可）

### 用户与数据
- **用户**：20 名信审 + 2 名 Admin
- **数据**：客户提供 100 条已脱敏测试数据
- **环境**：我方 PoC 沙盒（独立租户）

---

## 二、成功标准（量化 + 双方签字）

| 维度 | 指标 | 必达 | 优秀 |
|------|------|------|------|
| 技术：SAP 集成 | 数据同步成功率 | ≥ 99% | 99.9% |
| 技术：性能 | P95 响应 < N ms | ≤ 500ms | ≤ 300ms |
| 技术：SSO | Azure AD 通过率 | 100% | 100% |
| 业务：用例通过 | 5 个用例全过 | 5 / 5 | 5 / 5 |
| 业务：效率提升 | vs baseline | ≥ 30% | ≥ 40% |
| 业务：用户满意度 | NPS（PoC 内）| ≥ +30 | ≥ +50 |

**成功定义**：6 项至少 5 项达到"必达"
**失败定义**：< 4 项达到必达

---

## 三、PoC SOW（协议关键条款）

### 3.1 双方责任
**我方**：
- 提供 PoC 沙盒环境 + 配置
- 1 名 PreSales 全程支持（4 周内累计 ≤ 80 小时）
- 提供培训 1 场（4 小时）
- 每周 1 次 Sync 会议

**客户**：
- 提供测试数据（脱敏，1 周内）
- 提供 SAP 测试账号（W1）
- 提供 Azure AD 配置权限（W1）
- 指定 Champion 全程对接

### 3.2 IP 归属
- PoC 中我方代码：归我方
- 客户业务流配置：归客户（提供导出）
- 测试数据：归客户（PoC 结束销毁）

### 3.3 费用
- 选项 A：免费（条件：成功后 30 天内签合同）
- 选项 B：象征性 ¥X（成功后从合同抵扣）
- 选项 C：完全付费 PoC（条件：客户要求大量定制）

→ 本 PoC 选 A（销售推动）

### 3.4 退出机制
**成功** → 双方在 PoC 末次会议签字 → 进入正式合同谈判（30 天内）
**失败** → 我方提供详细分析报告 + 改进建议 → 双方友好结束
**中止** → 任一方书面通知，1 周内移交资料 + 销毁数据

---

## 四、关键时间节点

| 周 | 里程碑 | 输出 | 责任人 |
|----|--------|------|--------|
| W0 | Kick-off | 项目章程签署 | AE + Champion |
| W1 | 环境就绪 | SAP 联调通过 + Azure AD 通过 | SE + IT |
| W2 | 用户培训 | 20 人参训完成 | PreSales |
| W2 | First Value | 1 个用例端到端跑通 | PreSales + Champion |
| W3 | 中期 Review | 5 用例进度 + 数据中期 | 全员 |
| W4 | 末次验收 | 6 维度数据 + 客户决策 | AE + 客户 DM |
| W5 | 转正谈判 | 合同条款 + Multi-Year 评估 | AE + 客户 |

---

## 五、风险与应对

| 风险 | 应对 | Owner |
|------|------|-------|
| 客户 IT 提供 SAP 账号延迟 | W1 末必须就绪，否则延期 | AE 升级到 Champion |
| 信审用户参与度低 | Champion 内部宣讲 + 激励 | Champion |
| 性能不达标 | 中期 Review 前 SE 备 Plan B | SE |
| 客户决策链变化 | 周会保持透明 | AE |

---

## 六、Review 会议节奏

### W0 Kick-off（90 分钟）
- 范围 + 成功标准签字
- 时间表 + 责任分工
- 沟通节奏（Slack 群 / 周会时间）

### 每周 Sync（30 分钟）
- 上周进度
- 阻塞与升级
- 下周计划

### W3 中期 Review（60 分钟）
- 6 维度数据中期评分
- 风险审议
- 是否调整范围

### W4 末次验收（90 分钟）
- 6 维度最终数据
- 双方签字
- 转正讨论

---

## 七、转正预案

### 成功 → 30 天内签约
```
Day 0：末次验收会议 → 签字成功
Day 1：发送 Proposal（含 Multi-Year 折扣）
Day 7：商务谈判 1
Day 14：法务对齐
Day 21：合同终稿
Day 28：财务付款 + 签约
Day 30：正式 Kick-off
```

### 失败 → 体面退出
```
Day 0：末次会议 → 失败确认
Day 1：详细分析报告 + 改进路线图
Day 7：体面收尾会议（不撕破脸）
Future：6 个月后重启评估（如改进达成）
```

---

## 八、销售启发：避免常见 PoC 陷阱

```
❌ 无限延长 PoC（客户不签 + 你不甘心）
   → 范围 + 时间盒 + 失败定义都签字

❌ 范围越做越大（客户得寸进尺）
   → 任何"额外验证"= 新 SOW + 转正承诺

❌ PoC 期间为客户做定制开发
   → 只用标准产品，定制写入正式合同

❌ 不让客户付任何费用
   → 至少象征性付费（¥0 客户无承诺感）

❌ 验收标准模糊
   → "效率提升" → "效率从 X 提升到 Y"

❌ 客户决策人不参加任何会议
   → Kick-off + 末次验收必须高管出席
```
```

---

## 与其他命令的协同

```
/poc-plan（本命令）
  └── /pricing-strategy → PoC 转正定价

推荐工作流：
  新客户：
    /poc-plan --mode fullset
    → 执行 PoC
    → 成功 → 转正合同
    → 失败 → 体面退出 + 后续跟进
```

---

## 使用示例

```bash
# 完整 PoC 项目（默认）
/poc-plan Acme Corp

# 范围谈判
/poc-plan Acme Corp --mode scope

# SOW 协议起草
/poc-plan Acme Corp --mode sow

# 中期 Review 议程
/poc-plan Acme Corp --mode review

# 转正合同 SOP
/poc-plan Acme Corp --mode convert

# 技术 PoC（仅技术验证）
/poc-plan Beta Inc --type technical --duration 2w

# 复杂 PoC（金融 12 周）
/poc-plan 招商银行 --duration 12w --mode fullset
```
