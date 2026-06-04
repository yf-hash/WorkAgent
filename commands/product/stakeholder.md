---
name: stakeholder
description: >
  干系人管理（Stakeholder Management）助手。覆盖干系人识别（Power-Interest 矩阵）、
  RACI 责任矩阵、沟通节奏设计（CEO / 工程 / 销售 / 客户）、
  向上管理（Managing Up）、跨部门同盟搭建、坏消息传递 SOP、
  风险升级（Escalation）流程、Pre-mortem / Post-mortem 沟通。
  适用于：项目立项、跨团队协作、向上汇报、产品决策需多方对齐。
user-invocable: true
argument-hint: "<项目/产品/决策> [--mode identify|raci|comms|up|escalation|fullset] [--audience exec|eng|sales|cs|customer|mixed]"
---

# /stakeholder — 干系人管理

加载技能：`skills/stakeholder/SKILL.md`

## 触发条件
项目立项需多方对齐、跨团队协作有冲突、向上汇报需准备、做坏消息传递、需要做 RACI 责任明确，或风险需要升级时。

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `<项目/产品/决策>` | 干系人管理的对象（必填） | — |
| `--mode` | 工作模式 | `identify` |
| `--audience` | 主要受众 | — |

### 工作模式（--mode）
| 值 | 输出 | 适用场景 |
|----|------|---------|
| `identify` | 干系人识别 + Power-Interest 矩阵（**默认**） | 项目立项 |
| `raci` | RACI 责任矩阵 | 复杂项目分工 |
| `comms` | 沟通计划（频次 / 内容 / 渠道） | 跨团队协作 |
| `up` | 向上管理脚本（CEO / VP 汇报模板） | 高管汇报 |
| `escalation` | 升级流程 + 坏消息传递 SOP | 风险/冲突升级 |
| `fullset` | 五件套全套 | 重大项目启动 |

### 受众（--audience）
| 值 | 说明 |
|----|------|
| `exec` | 高管 / CEO / VP（关心：战略 / 数字 / 风险） |
| `eng` | 工程团队（关心：技术细节 / 工时 / 优先级） |
| `sales` | 销售团队（关心：可卖点 / 客户案例 / 竞品） |
| `cs` | 客服 / 客户成功（关心：工单影响 / 培训） |
| `customer` | 外部客户（关心：价值 / 时间 / 风险） |
| `mixed` | 混合（多类干系人在场） |

---

## 执行流程（identify 模式）

```
Step 1: 干系人盘点
  → 列出所有可能受影响 / 有影响力的人 / 团队
  → 内部：高管 / 同部门 / 跨部门 / 工程 / 设计 / 销售 / 客服
  → 外部：客户 / 合作伙伴 / 监管 / 供应商

Step 2: Power-Interest 分类
  → Power 高 / Interest 高：Manage Closely（深度沟通）
  → Power 高 / Interest 低：Keep Satisfied（保持满意）
  → Power 低 / Interest 高：Keep Informed（持续告知）
  → Power 低 / Interest 低：Monitor（监测）

Step 3: 角色识别
  → Sponsor（项目发起人 / 资源方）
  → Champion（内部支持者）
  → Decider（最终决策者）
  → Influencer（影响决策的人）
  → Blocker（潜在反对者，必须识别）
  → User（最终用户）

Step 4: 沟通策略（每类干系人）
  → 频次（周 / 月 / 关键节点）
  → 内容（数字 / 故事 / 风险 / 决策点）
  → 渠道（邮件 / 会议 / 看板 / 文档）

Step 5: 风险与对策
  → 谁可能 Block？为什么？怎么转化？
  → 哪些干系人需要前置沟通？
```

---

## 输出示例（identify 模式）

```markdown
# [项目名] 干系人管理计划

## 一、干系人盘点

| # | 姓名 / 角色 | 团队 | 角色类型 | Power | Interest |
|---|------------|------|---------|-------|----------|
| 1 | CEO | 高管 | Sponsor | 🔴高 | 🟡中 |
| 2 | CTO | 工程 | Decider | 🔴高 | 🔴高 |
| 3 | VP Sales | 销售 | Influencer | 🟡中 | 🔴高 |
| 4 | 设计 Lead | 设计 | Champion | 🟡中 | 🔴高 |
| 5 | 数据 Lead | 数据 | Influencer | 🟡中 | 🟢低 |
| 6 | CS 主管 | 客服 | Influencer | 🟢低 | 🔴高 |
| 7 | 大客户 A | 外部 | User + Influencer | 🟡中 | 🔴高 |

## 二、Power-Interest 矩阵

```
            Interest 低              Interest 高
            ────────────────────    ────────────────────
Power 高    │ Keep Satisfied      │ Manage Closely     │
            │                     │                     │
            │ • CEO               │ • CTO               │
            ────────────────────  ────────────────────
Power 低    │ Monitor             │ Keep Informed       │
            │                     │                     │
            │ • 数据 Lead          │ • 设计 Lead         │
            │                     │ • VP Sales          │
            │                     │ • CS 主管            │
            │                     │ • 大客户 A           │
```

## 三、沟通策略

### Manage Closely（CTO）
- 频次：每周 1on1（30 分钟）
- 内容：技术风险 + 资源诉求 + 进度
- 渠道：会议 + 邮件总结
- 关键节点：W4 架构评审 / W8 上线评审

### Keep Satisfied（CEO）
- 频次：双周更新 + 月度战略汇报
- 内容：关键数字 + 风险 + 关键决策点
- 渠道：1 页文档 + 30 分钟会议
- 重点：用商业语言，不深入技术

### Keep Informed（设计 / Sales / CS / 大客户）
- 频次：双周邮件 + 关键节点同步
- 内容：进度 + 影响他们的变化
- 渠道：邮件 + 共享看板

### Monitor（数据 Lead）
- 频次：月度 status 更新
- 渠道：邮件抄送

## 四、Champion 与 Blocker 分析

### Champion（VP Sales）
- 立场：强支持（看到客户痛点）
- 利用：让 VP Sales 在管理层会议为项目背书
- 风险：销售期望过高 → 提前管理预期

### 潜在 Blocker（数据 Lead）
- 顾虑：怕新功能影响数据看板稳定性
- 转化策略：W2 单独沟通，让数据 Lead 早期参与设计评审，列在 RACI 的 Consulted

## 五、关键沟通节点
- W0：Kick-off（所有 Manage Closely + Champion）
- W4：中期评审（增加 Keep Satisfied）
- W8：上线评审（全员）
- W13：D+30 复盘（核心团队）

## 六、风险与对策
- R1：CTO 临时被抽调到其他项目
  → 应对：W2 与 CTO 确认资源承诺，写入项目章程
- R2：销售期望过高
  → 应对：W4 评审时同步实际范围，避免最后惊讶
```

---

## 输出示例（raci 模式）

```markdown
# [项目名] RACI 责任矩阵

| 任务 | PM | Eng | Design | QA | Sales | CS | CEO |
|------|----|----|--------|----|----|----|----|
| 需求确认 | **R/A** | C | C | I | C | I | I |
| 技术方案 | A | **R** | C | I | I | I | I |
| 设计稿 | A | C | **R** | I | I | I | I |
| 代码实现 | A | **R** | I | I | I | I | I |
| 测试 | A | C | I | **R** | I | I | I |
| 上线 | **R/A** | R | I | C | I | I | I |
| GTM | **R/A** | I | C | I | C | C | I |
| 客户培训 | A | I | I | I | C | **R** | I |
| 战略决策 | C | I | I | I | I | I | **R/A** |

**图例**：
- R = Responsible（执行）
- A = Accountable（负责，决策）
- C = Consulted（咨询）
- I = Informed（告知）

**原则**：每行一个 A（避免决策模糊）
```

---

## 输出示例（up 模式 - 向上管理）

```markdown
# [项目名] 高管汇报模板（30 分钟）

## 1. 一句话核心结论（30 秒）
> "我们已完成 70% 范围，预计延期 1 周但仍能 D+0 上线，需要您批准 XX 决策"

## 2. 关键数字（2 分钟）
| 指标 | 计划 | 实际 | 偏差 |
|------|------|------|------|
| 进度 | 75% | 70% | -5pp |
| 团队 Velocity | 30 SP | 32 SP | +2 |
| 关键 Bug | 0 | 1 (P1) | -1 |

## 3. 风险 + 应对（5 分钟）
| 风险 | 影响 | 应对 |
|------|------|------|
| 第三方 API 不稳定 | 高 | 增加降级方案 |

## 4. 决策点（10 分钟）— 您的决策需要在 [日期] 前给出
**决策 1**：是否接受延期 1 周？
- 选项 A：延期 1 周（我推荐）
- 选项 B：砍 P2 范围按时上
- 选项 C：加资源加速（需调 1 名工程师）

## 5. 你需要的资源 / 支持（5 分钟）
- 跟 VP Sales 同步预期管理
- 月底战略会前批准 GTM 计划

## 6. 下次汇报（30 秒）
- 双周后同时间，主题：上线就绪度
```

---

## 与其他命令的协同

```
/stakeholder（本命令）
  ├── /launch-checklist → 上线前的干系人沟通
  ├── /roadmap → 路线图沟通对齐
  ├── /retrospective → 复盘谁参加
  ├── /pmf-survey → 客户类干系人调研
  ├── /product-report → 月报覆盖干系人
  └── /okr --mode align → OKR 跨团队对齐

推荐工作流：
  重大项目立项：
    /stakeholder --mode fullset
    → /raci 矩阵 → 确定责任分工
    → /comms 计划 → 沟通节奏
    → 项目执行
    → 升级/阻塞 → /stakeholder --mode escalation
    → 上线 → /launch-checklist
    → D+7 → /retrospective
```

---

## 使用示例

```bash
# 干系人识别 + Power-Interest 矩阵（默认）
/stakeholder 海外版上线项目

# RACI 责任矩阵
/stakeholder 跨团队 AI 功能 --mode raci

# 沟通计划设计
/stakeholder 重大改版项目 --mode comms

# 向 CEO 汇报模板
/stakeholder Q2 项目进展 --mode up --audience exec

# 风险升级 + 坏消息传递
/stakeholder 项目延期决策 --mode escalation

# 完整五件套（重大项目启动）
/stakeholder 出海项目 --mode fullset

# 与销售团队同步
/stakeholder 新功能 GTM 计划 --audience sales --mode comms
```
