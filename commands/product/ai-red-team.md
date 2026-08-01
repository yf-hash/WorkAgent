---
description: AI 产品 Red Team 红队测试 — 把"我们 AI 安全吗"变成可执行测试计划（OWASP LLM Top 10 + 10 个必测场景 + 红队报告）
argument-hint: "[AI 功能/模型/上线版本]"
allowed-tools: [Read, Write, Edit, Grep, Glob, AskUserQuestion]
harness:
  execute:
    preset: research
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

# /ai-red-team — AI 产品红队测试

加载技能：`skills/strategy/ai-red-team/SKILL.md`

请基于以下 AI 功能 / 模型版本，制定红队测试计划：

$ARGUMENTS

## 工作流程

### 第 1 步：威胁建模（OWASP LLM Top 10）

| # | 威胁 | 优先级 |
|---|------|--------|
| LLM01 | Prompt Injection | P0 |
| LLM02 | Insecure Output Handling | P0 |
| LLM06 | Sensitive Information Disclosure | P0 |
| LLM07 | Insecure Plugin Design | P0 |
| LLM08 | Excessive Agency | P0 |
| LLM03/04/05/09 | 训练数据 / DoS / 供应链 / 过度依赖 | P1 |
| LLM10 | Model Theft | P2 |

### 第 2 步：10 个必测攻击场景

1. **直接 Prompt Injection**（100% 拒绝 + 符合产品语气）
2. **间接 Prompt Injection**（文档/网页/截图带毒）（≥ 95% 检测）
3. **Jailbreak**（DAN/Grandma/Roleplay/Token Smuggling）（100% 拒绝）
4. **训练数据泄露**（100% 拒绝输出训练 / 历史会话）
5. **越权工具调用**（Agent / Tool Use 边界）（100% 阻断 + 审计）
6. **RAG 数据泄露**（跨租户 / 越权查询）（100% 拒绝）
7. **输出代码 / SQL 注入**（100% 自动检测 + 拒绝执行）
8. **偏见 / 公平性**（子群体差距 < 10%）
9. **幻觉 / 事实错误**（≥ 90% 应说"不知道"）
10. **模型 DoS**（成本上限熔断）

### 第 3 步：测试样本设计

| 维度 | 数量 |
|------|------|
| 攻击场景 | 10 类 |
| 每类样本 | 20-100 条（共 200-500 条）|
| 中文 / 英文比 | 至少 1:1 |
| 公开 Jailbreak prompts | 复用最新模板 |
| 自定义攻击 | 基于产品场景设计 |

### 第 4 步：红队团队

| 角色 | 职责 |
|------|------|
| Red Team Lead | 计划 / 报告 / 协调 |
| Prompt 攻击者 | 设计攻击 prompt |
| 工具调用攻击者 | Agent / Tool / RAG 边界 |
| 数据攻击者 | 训练数据 / 跨租户 |
| 偏见测试者 | 公平性 / 幻觉 |

### 第 5 步：4 周演练节奏

```
W1: 威胁建模 + 攻击样本设计 + Prompt 评审
W2: 执行测试 + 实时观察告警 + 记录失败
W3: 分析根因 + 协商修复优先级 + 起草报告
W4: 跟踪修复 + 回归测试 + 对接下季度
```

## 输出格式

```markdown
# AI Red Team 报告 — {AI 功能} {季度}

## 一、TL;DR
- 测试场景数：10 类 / N 条
- 通过率：%
- P0 失败：M 条
- 上线 / 回滚建议

## 二、威胁覆盖矩阵

| 威胁 | 样本数 | 通过率 | 严重失败 | 已修复 |
|------|--------|--------|----------|--------|

## 三、失败案例（按严重性）

### P0（阻塞上线）

| # | 攻击描述 | 触发条件 | 模型输出（节选）| 影响 | 修复方案 |
|---|----------|----------|------------------|------|----------|

### P1（本季内修）

### P2（待评估）

## 四、缓解措施清单

| 措施 | 状态 | 责任人 |
|------|------|--------|
| 输入过滤强化 | | |
| 输出过滤强化 | | |
| 审计日志增强 | | |
| 模型微调 | | |
| 工具调用边界 | | |

## 五、与上季度对比

| 维度 | 上季度 | 本季度 | 趋势 |

## 六、下季度建议
- 重点测试方向
- 是否需要外部红队

## 七、关联资源
- Model Card：`templates/model-card-template.md`
- Eval Rubric：`templates/ai-eval-rubric-template.md`
- AI 安全产品方法论：`pm-ai-security-product`
- 合规：`/compliance-checklist`
- 上线决策：`/launch-checklist` + `@qa-acceptance-designer`
```

## 输出原则

- 每条失败必须**可复现**：完整 Prompt + 模型版本 + 步骤
- 每条失败配**修复方案**
- 优先级：P0 阻塞上线 / P1 本季内 / P2 待评估
- 修复后**回归测试**

## 红线

- ❌ 红队 = 安全部门玩具（与产品 / 算法脱节）
- ❌ 不复现就声称已修复
- ❌ 只测最近上线功能（长尾要覆盖）
- ❌ 不测中文 / 多语言（很多注入对中文有特殊触发）
- ❌ 测完不进迭代（红队报告变 PPT）
