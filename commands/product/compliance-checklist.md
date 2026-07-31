---
name: compliance-checklist
description: >
  合规检查与认证规划。覆盖中国（等保 2.0 / 数据安全法 / 个保法 / 网安法 / 关基）、国际（SOC 2 / ISO 27001 / GDPR / HIPAA / PCI-DSS）、行业（金融 / 医疗 / 教育）合规要求。含合规优先级评估、Gap Analysis、整改清单、合规路线图、TPRM 第三方风险、DPIA 数据保护影响评估、违约通知 SOP。适用于：合规自查、合规认证规划、客户合规问卷应答、监管报送、跨境业务合规对齐。
user-invocable: true
argument-hint: "<合规框架/产品> [--mode assess|gap|roadmap|questionnaire|incident|fullset] [--framework dengbao|soc2|iso27001|gdpr|hipaa|pci|pipl|fullstack] [--region cn|us|eu|apac|global]"
---

# /compliance-checklist — 合规检查与认证规划

加载技能：`skills/strategy/compliance-checklist/SKILL.md`

## 触发条件
合规自查、客户合规问卷应答、规划下一个合规认证、监管要求落地、违约事件响应、跨境业务合规审议、新行业（金融 / 医疗 / 政府）拓展前评估。

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `<合规框架/产品>` | 合规框架名 / 产品名（必填） | — |
| `--mode` | 工作模式 | `assess` |
| `--framework` | 目标合规框架 | — |
| `--region` | 目标地区 | `cn` |

### 工作模式（--mode）
| 值 | 输出 | 适用场景 |
|----|------|---------|
| `assess` | 现状自评 + 优先级建议（**默认**） | 起步阶段 |
| `gap` | Gap 分析（现状 vs 目标）+ 整改清单 | 具体合规启动 |
| `roadmap` | 多合规路线图（12-24 月规划） | 战略规划 |
| `questionnaire` | 客户合规问卷应答模板 | 销售支持 |
| `incident` | 违约通知 SOP + 流程 | 事件响应 |
| `fullset` | 评估 + Gap + 路线图 + 问卷 | 完整合规体系 |

### 合规框架（--framework）
| 值 | 含义 |
|----|------|
| `dengbao` | 等保 2.0 |
| `soc2` | SOC 2 Type I/II |
| `iso27001` | ISO 27001（含 27017 / 27018） |
| `gdpr` | 欧盟 GDPR |
| `hipaa` | 美国医疗 HIPAA |
| `pci` | 支付卡 PCI-DSS |
| `pipl` | 中国个保法 |
| `fullstack` | 多框架组合 |

### 地区（--region）
| 值 | 重点合规 |
|----|---------|
| `cn` | 等保 + 数安 + 个保（**默认**） |
| `us` | SOC 2 + HIPAA + CCPA |
| `eu` | GDPR + ISO 27001 |
| `apac` | 多国混合 |
| `global` | 全球客户混合 |

---

## 执行流程（assess 模式）

```
Step 1: 业务理解
  → 客户类型（C / B / 政企 / 海外）
  → 数据类型（普通 / 个人 / 敏感个人）
  → 部署形态（SaaS / 私有 / 跨境）

Step 2: 法律识别
  → 适用的中国法律
  → 客户所在地法律
  → 数据来源国法律

Step 3: 现状评估
  → 已具备能力（加密 / RBAC / 审计 / 备份等）
  → 已具备文档（政策 / 程序 / 控制清单）
  → 已具备团队（CISO / DPO / 合规 / 法务）

Step 4: 优先级排序
  → 客户必须要求 → P0
  → 销售推动 → P1
  → 内部健康 → P2

Step 5: 路线图
  → 6 / 12 / 24 月规划
  → 每个合规的实施成本和价值
```

---

## 输出示例（assess 模式）

```markdown
# [产品名] 合规现状评估

## 业务上下文
- 客户：B 端 SMB + 大企业（含 5 家金融）
- 数据：业务数据 + 个人信息（员工 / 客户姓名邮箱）
- 部署：SaaS 多租户（中国数据中心）
- 海外：暂无，但 6 个月内计划开拓东南亚

## 一、法律识别
✅ 必须遵守：
- 网络安全法
- 数据安全法
- 个人信息保护法

⚠️ 重点关注：
- 关基条例（金融客户可能要求等保 3 级）
- 出海后：GDPR（如东南亚有欧盟客户引申）

## 二、现状评估

### 技术能力
| 能力 | 当前 | 目标 |
|------|------|------|
| 数据加密 | ✅ TLS 1.2 + AES-256 | OK |
| 访问控制 | ⚠️ 仅基础 RBAC，无 MFA | 加 MFA |
| 审计日志 | ❌ 仅业务关键，覆盖率 50% | 全覆盖 + 不可篡改 |
| 备份恢复 | ⚠️ 每日备份，无演练 | 季度演练 |
| MFA | ❌ 未实现 | Admin 强制 |
| 数据导出 | ⚠️ Admin 可，普通用户不可 | 全自助 |
| 数据删除 | ❌ 仅停账号，未真删 | 退出时彻底 |

### 文档能力
| 文档 | 状态 |
|------|------|
| 隐私政策 | ✅ 有 |
| 安全白皮书 | ❌ 无 |
| DPA 模板 | ❌ 无 |
| 子处理者清单 | ❌ 无 |
| 应急响应 SOP | ⚠️ 简单版 |

### 团队能力
- CISO：❌ 无（建议：兼职聘 1 人）
- DPO：❌ 无（建议：法务兼任）
- 合规专员：❌ 无（建议：6 月后招）

## 三、合规优先级（半年内）

### P0（销售必须）
1. **隐私政策 + DPA 模板** ⭐
   - 价值：影响所有 B 端签约
   - 成本：2 周（法务）
2. **安全白皮书**
   - 价值：客户问卷必备
   - 成本：1 月

### P1（合规健康）
3. **MFA + 强化访问控制**
   - 价值：阻止主流安全风险
   - 成本：2 周（工程）
4. **审计日志覆盖 + 不可篡改**
   - 价值：等保 / SOC 2 必备
   - 成本：1 月（工程）

### P2（认证准备）
5. **等保 2 级**
   - 价值：国内 B 端通用
   - 成本：3-6 月 + ¥10-30 万
6. **SOC 2 Type I**（如出海）
   - 价值：海外中型客户
   - 成本：6-9 月 + $30-60K

## 四、6 月路线图

```
M1-M2：合规起步
  - 制度建立（隐私政策 / 应急响应 / 数据保留）
  - DPA + 安全白皮书
  - 选 SaaS 合规平台（Vanta / Drata）

M3-M4：技术整改
  - MFA 强制
  - 审计日志全覆盖 + 不可篡改
  - 备份恢复演练 SOP

M5-M6：等保启动
  - 选定测评机构
  - Gap 分析 + 整改
  - 等保 2 级初评
```

## 五、风险提示

⚠️ 当前最大风险：
- 个保法 / 数安法已生效，无 DPA 出事故承担全责
- 销售层面：5 家金融客户已开始要求合规材料
- 建议：本月启动 P0 项目

⚠️ 出海风险（6 月后）：
- GDPR 罚款上限 4% 全球营收
- 如有欧盟客户必须先 GDPR 合规

→ 用 /compliance-checklist --mode roadmap 看完整 12 月规划
→ 用 /compliance-checklist --mode gap --framework dengbao 详查等保
```

---

## 输出示例（questionnaire 模式）

```markdown
# 客户合规问卷应答模板

## 常见问卷类型 → 应答素材清单

### Q1：你们有哪些合规认证？
**应答**：
- 等保 2 级（计划：2026-Q4）
- SOC 2 Type I（计划：2027-Q2）
- ISO 27001（计划：2027-Q4）

→ 实际有的勾选 ✅，未来计划写"In Progress"

### Q2：数据存储在哪里？
**应答**：
- 中国客户：数据存于阿里云华东 / 华北
- 不跨境（除合规明确允许）
- 备份：异地（华南）

### Q3：有数据加密吗？
**应答**：
- 传输：TLS 1.2+
- 静态：AES-256
- 密钥管理：KMS（HSM 硬件加密）
- 客户管理密钥（CMK）：Enterprise 套餐支持

### Q4：访问控制怎么做的？
**应答**：
- RBAC + 最小权限
- MFA（Admin 强制）
- SSO（SAML 2.0 + OIDC）
- SCIM 自动化用户管理
- 季度访问审议

### Q5：审计日志保留多久？
**应答**：
- Free / Pro：7 天
- Team：30 天
- Enterprise：自定义（默认 1 年）+ S3 归档
- 不可篡改 + Hash 链校验

### Q6：发生数据泄露怎么通知？
**应答**：
- 24 小时内：内部确认
- 72 小时内：通知客户 + 监管（GDPR 标准）
- 30 天内：完整 PIR

### Q7：员工背景调查？
**应答**：
- 入职：背景调查（教育 + 工作）
- 离职：访问立即回收 + 设备回收
- 安全意识：年度培训 + 钓鱼测试

### Q8：第三方依赖（子处理者）？
**应答**：
→ 提供 Subprocessor List
- AWS / 阿里云（数据存储）
- Anthropic / OpenAI（AI 处理）
- Stripe（支付）
- ...

→ 新增 / 变更：30 天前通知

### Q9：BCP / DR 计划？
**应答**：
- RPO ≤ 1 小时
- RTO ≤ 4 小时
- 异地备份（华东 → 华南）
- 季度恢复演练
- 年度桌面演练

→ 完整 BCP 文档：[Trust Center 链接]

## 应答原则
✅ 不夸大（说做不到的合规 = 自爆雷）
✅ 给文档而非话术（Trust Center 链接）
✅ "In Progress" 给时间表
✅ 法务 + 安全 双 review
```

---

## 与其他命令的协同

```
/compliance-checklist（本命令）
  ├── /prd --mode standard / /prd --mode impl → 合规作为非功能需求
  ├── /security-questionnaire → 客户安全问卷应答
  └── /product-bid-params / /product-solution → 合规参数 / 行业方案承载合规承诺

推荐工作流：
  起步合规：
    /compliance-checklist --mode assess
    → /compliance-checklist --mode roadmap
    → P0 项目实施

  申请认证：
    /compliance-checklist --mode gap --framework soc2
    → 整改 → 审计 → 认证

  客户问卷：
    /compliance-checklist --mode questionnaire
    → 套用 Trust Center 资料
```

---

## 使用示例

```bash
# 现状自评 + 优先级（默认）
/compliance-checklist 主产品

# 等保 2 级 Gap 分析
/compliance-checklist --mode gap --framework dengbao

# SOC 2 Type II 路线图
/compliance-checklist --mode roadmap --framework soc2

# 多合规组合规划
/compliance-checklist --mode roadmap --framework fullstack --region global

# 客户合规问卷应答
/compliance-checklist 销售支持 --mode questionnaire

# GDPR 跨境合规
/compliance-checklist --framework gdpr --region eu

# 违约事件响应 SOP
/compliance-checklist --mode incident

# 完整体系（合规起步公司）
/compliance-checklist 全栈合规 --mode fullset --region cn
```
