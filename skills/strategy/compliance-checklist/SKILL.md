---
name: compliance-checklist
description: >
  合规检查与认证规划知识库。覆盖中国（等保 2.0 / 数据安全法 / 个保法 /
  关基条例 / 网安法）+ 国际（SOC 2 Type I/II / ISO 27001 / GDPR / HIPAA /
  PCI-DSS）+ 行业（医疗 / 金融 / 教育）合规要求。含合规审计流程、
  TPRM（第三方风险管理）、DPIA（数据保护影响评估）、合规材料体系、
  监管沟通模板、合规与产品功能映射表。
  触发词：等保、SOC2、ISO27001、GDPR、HIPAA、PCI-DSS、个保法、数据安全法、
  合规审计、DPIA、TPRM、合规检查、监管、数据驻留、合规认证
user-invocable: false
effort: high
harness:
  execute:
    preset: writing-scoped
  constrain:
    profile: writing-safe
  loop:
    mode: one-shot
  memory:
    scope: project
    reads: [project-context]
  security:
    danger-level: low
---

# Compliance Checklist — 合规检查知识库

把"通过审计"从临时抱佛脚变成持续运营的体系。

---

# 一、合规框架地图

## 1.1 中国合规

```
法律层：
  - 网络安全法（2017）
  - 数据安全法（2021）
  - 个人信息保护法（2021）
  - 关键信息基础设施安全保护条例（2021）

技术标准：
  - 等保 2.0（GB/T 22239-2019）
    - 2 级：一般 SaaS
    - 3 级：重要业务（金融 / 医疗）
    - 4 级：核心业务（央行 / 国家级）

行业要求：
  - 金融：银保监 / 央行
  - 医疗：医院信息化标准
  - 教育：教育部信息化标准
```

## 1.2 国际合规

```
通用框架：
  - SOC 2（Trust Service Criteria）
    - Type I：某时点
    - Type II：某时段（6-12 月）
  - ISO 27001（信息安全管理体系）
  - ISO 27017（云安全扩展）
  - ISO 27018（PII 云保护）

数据保护：
  - GDPR（欧盟，2018）
  - CCPA（加州，2020）
  - LGPD（巴西）
  - PIPL（中国个保法）

行业：
  - HIPAA（美国医疗）
  - PCI-DSS（支付卡）
  - FedRAMP（美国政府）
  - HITRUST（医疗）
```

---

# 二、合规优先级矩阵

```
| 合规 | 客户要求 | 销售影响 | 实施成本 | 推荐时机 |
|------|---------|---------|---------|---------|
| 等保 2 级 | 国内通用 | 中 | 低 | A 轮前 |
| SOC 2 Type I | 海外中型客户 | 高 | 中 | B 轮前 |
| 等保 3 级 | 金融 / 政府 | 高 | 高 | 进金融时 |
| SOC 2 Type II | 海外大客户 | 极高 | 高 | C 轮前 |
| ISO 27001 | 国际企业 | 高 | 高 | 出海时 |
| GDPR | 欧盟客户 | 必须 | 中 | 卖欧盟客户前 |
| HIPAA | 美国医疗 | 必须 | 高 | 进医疗时 |
| PCI-DSS | 处理支付卡 | 必须 | 极高 | 处理卡时 |
```

---

# 三、合规与产品功能映射

## 3.1 通用合规要求 → 产品能力

```
| 要求 | 产品能力 |
|------|---------|
| 数据加密 | TLS 1.2+ 传输 + AES-256 静态 |
| 访问控制 | RBAC + 最小权限 + 季度审议 |
| 审计日志 | 全部敏感操作 + 不可篡改 + 留存 |
| 数据备份 | 每日 + 异地 + 季度演练 |
| 灾备能力 | RPO ≤ 1h / RTO ≤ 4h |
| MFA | Admin 强制 / 普通可选 |
| 数据导出 | 自助 + 客户保留主权 |
| 数据删除 | 退出时彻底删除 + 报告 |
| 漏洞管理 | 季度扫描 / 年度 Pentest |
| 安全意识 | 员工年培 + 钓鱼测试 |
| 合规变更通知 | 法规变更 30 天前通知客户 |
```

## 3.2 GDPR / 个保法 → 产品能力

```
✅ 知情同意（明示 + 撤销）
✅ 数据最小化（不收没用的）
✅ 目的限定（不超约定使用）
✅ 用户权利：
  - 访问权（导出）
  - 更正权
  - 删除权（Right to be Forgotten）
  - 限制处理权
  - 可携带权（机器可读导出）
  - 反对权（拒绝自动决策）
✅ 子处理者管理（DPA + 清单 + 通知变更）
✅ 跨境传输（标准合同条款 SCC）
✅ DPO（数据保护官）
✅ 违约通知（72 小时）
```

## 3.3 等保 2.0 → 产品能力（3 级摘要）

```
物理安全：机房等级 + 出入控制
网络安全：分区分域 + 防火墙 + IDS
主机安全：基线加固 + 防病毒 + 漏洞扫描
应用安全：身份鉴别 + 访问控制 + 安全审计
数据安全：加密 + 备份 + 完整性
管理安全：制度 + 培训 + 应急响应
```

---

# 四、SOC 2 Type II 实施路径

## 4.1 时间表（典型 8-12 个月）

```
Month 1-2：差距分析（Gap Assessment）
  - 选 Auditor
  - 范围确定（Trust Service Criteria）
  - 现状评估

Month 3-5：差距修复
  - 制度建立
  - 控制措施落地
  - 工具引入（Vanta / Drata / Secureframe）

Month 6：审计准备
  - 证据收集
  - 内审

Month 7-12：观察期（6 月最短）
  - 持续运行
  - 持续证据收集

Month 13：正式审计
  - 上线 Type II 报告
```

## 4.2 Trust Service Criteria（5 项）

```
Security（安全）        必选
Availability（可用性）  推荐
Confidentiality（保密） 推荐
Processing Integrity   按需
Privacy（隐私）         按需
```

## 4.3 Vanta / Drata 等自动化平台

```
价值：
  ✅ 自动证据收集（连接 AWS / GitHub / Okta 等）
  ✅ 持续监控（不再"审计前抱佛脚"）
  ✅ 内置控制清单（Type II 100+ 控制）
  ✅ 文档自动生成
  ✅ 客户信任中心（Trust Center）

成本：年 $10-50K（值，比手动便宜很多）
```

---

# 五、TPRM（第三方风险管理）

## 5.1 子处理者清单

```
所有处理客户数据的第三方都要登记：

- Cloud Provider（AWS / 阿里云）
- 数据分析（PostHog / Mixpanel）
- 客服（Intercom / Zendesk）
- Email（SendGrid）
- 短信（阿里云 / Twilio）
- AI（OpenAI / Anthropic）
- 监控（Datadog / Sentry）
- 支付（Stripe / 支付宝）
```

## 5.2 评估维度

```
| 维度 | 评估项 |
|------|------|
| 合规 | SOC 2 / ISO / 等保 |
| 数据 | 数据驻留 / 加密 / 删除 |
| 安全 | Pentest / 漏洞响应 |
| SLA | 可用性 / RPO / RTO |
| 法务 | DPA / SCC / BAA |
| 财务 | 信用 / 财报 |
```

## 5.3 客户通知

```
新增 / 变更子处理者 → 30 天前通知客户
客户可拒绝（通常导致合同终止）
```

---

# 六、DPIA（数据保护影响评估）

## 6.1 何时必须做 DPIA

```
GDPR Art. 35 强制：
  - 大规模处理特殊类别个人数据
  - 系统性自动化决策
  - 大规模公共空间监控
  - 涉及高风险处理

国内类似要求（个保法）：
  - 处理敏感个人信息
  - 利用个人信息自动化决策
  - 委托或共享个人信息
  - 跨境传输
```

## 6.2 DPIA 模板

```
1. 处理活动描述
   - 目的、范围、数据类型、规模

2. 必要性与适度性
   - 为何处理 / 是否最小化

3. 风险评估
   - 数据主体可能的不利影响
   - 概率 + 影响

4. 应对措施
   - 技术措施
   - 组织措施

5. 残余风险
   - 应对后剩余风险
   - 是否可接受

6. DPO 意见
7. 管理层批准
```

---

# 七、合规材料体系

```
docs/compliance/
├── policies/                       政策
│   ├── security-policy.md
│   ├── privacy-policy.md
│   ├── data-retention.md
│   ├── incident-response.md
│   └── ...
├── procedures/                     程序
│   ├── access-review.md            季度访问审议
│   ├── vulnerability-mgmt.md
│   ├── change-mgmt.md
│   ├── employee-onboarding.md
│   └── ...
├── controls/                       控制清单
│   ├── soc2-controls.md
│   ├── iso27001-controls.md
│   ├── gdpr-controls.md
│   └── ...
├── evidences/                      证据（每季度更新）
│   └── 2026-q2/
├── certifications/                 认证证书
│   ├── soc2-2026.pdf
│   └── iso27001-2026.pdf
├── customer-facing/                对外
│   ├── trust-center.md
│   ├── dpa-template.md
│   ├── subprocessors-list.md
│   └── security-whitepaper.md
└── audits/                         审计记录
    ├── 2026-soc2-typeii.md
    └── ...
```

---

# 八、客户合规问卷应对

## 8.1 问卷常见类型

```
- SIG（Standardized Information Gathering）
- VSAQ（Google Vendor Assessment）
- CSA CAIQ（Cloud Security Alliance）
- 客户自定义（金融 / 政府最常见）
```

## 8.2 应对策略

```
✅ 建立 Trust Center（一次回答多次复用）
✅ 用 Vanta / Drata 自动填问卷
✅ 标准 DPA / Subprocessor List 模板
✅ 安全白皮书（一份解决 80%）
✅ 客户成功 + 法务 + 安全 三方协同
```

---

# 九、违约通知 SOP

```
T+0：发现可能的违约（Incident）
T+1h：内部确认 + 升级到 CISO + 法务
T+24h：事实调查初步报告
T+72h：通知监管 + 受影响客户（GDPR 标准）
T+7 天：详细报告 + 应对措施
T+30 天：完整 PIR + 长期改进
```

---

# 十、与其他知识库的关系

| 知识库 | 协作 |
|--------|------|
| `prd-standard` | 合规作为非功能需求 |
| `security-questionnaire` | 客户安全问卷应答 |
| `product-writer-router` + `templates/product/bid-params.md` / `product-solution-writer` | 合规参数承载 / 行业方案合规承诺 |
