---
name: security-questionnaire
description: >
  安全问卷 / VSQ / TPRM 应答工具 — 处理客户发来的 200-500 条安全问卷
  （CAIQ / SIG / VSA / 客户自定义）。含 13 大类问题分类、4 级应答模式、
  合规证据映射、敏感问题红线、应答 KB 复用、年度续答 SOP。
user-invocable: true
argument-hint: "<安全问卷文件或描述> [--mode draft|review|kb-build|annual] [--standard caiq|sig|vsa|custom] [--out path]"
---

# /security-questionnaire — 安全问卷应答

加载技能：`skills/security-questionnaire/SKILL.md`
配套 Skill：`compliance-checklist`（合规证据映射）

## 触发条件
- 客户发来安全问卷（200-500 条问题）
- 大客户每年的供应商风险评估（VSQ）续答
- 建立标准化的安全问卷答案 KB

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `<问卷文件或描述>` | 客户提供的问卷 | — |
| `--mode` | 工作模式 | `draft` |
| `--standard` | 问卷标准 | 自动识别 |
| `--out` | 输出路径 | `./outputs/security-q/` |

### 工作模式

| `--mode` | 输出 |
|----------|------|
| `draft` | 第一轮草稿（KB 复用 + 新增题起草）|
| `review` | 评审已有应答（一致性 / 风险 / 证据完备）|
| `kb-build` | 建立 / 更新 KB（每条题 3 版答案：完整 / 简化 / 拒答）|
| `annual` | 年度续答（与去年版本 diff + 证据更新）|

## 使用示例

```
/security-questionnaire ./Bank_VSQ.xlsx --mode draft --standard custom
/security-questionnaire ./CAIQ.xlsx --mode kb-build --standard caiq
/security-questionnaire 某金融客户 2026 --mode annual
/security-questionnaire ./Draft_v1.xlsx --mode review
```

## 执行流程

```
Step 1: 拆题分类
  → 13 大类自动归类（治理 / 风险 / 合规 / 数据 / 访问 / 物理 / 网络 / 应用 / 运维 / IR / BCP / 第三方 / 隐私）
  → 标记敏感度（普通 / NDA 后披露 / 拒答）

Step 2: KB 检索匹配
  → 标准 CAIQ 答案优先复用（典型复用率 95%+）
  → 客户自定义题走专家分配

Step 3: 应答模式判定
  → ✅ 完全披露（已有公开认证）
  → ⚠️ 部分披露（涉商业机密）
  → ❌ 诚实承认（当前不具备 + 补偿措施 + 时间表）
  → 🔒 NDA 后披露

Step 4: 证据链接
  → 每条至少 1 份证据来源
  → 必备文档清单（SOC 2 / ISO 27001 / 等保 / 渗透报告 / 网安保险等）

Step 5: 红线扫描
  → 数据驻留 / 子处理者 / 跨境 / 历史事件 → 必须诚实披露
  → "100% / 完全 / 永久" → 自动替换

Step 6: 评审
  → 法务（跨境 / 子处理者 / 历史事件）
  → CISO（技术细节准确性）
  → 销售（商业敏感度）

Step 7: 文件打包
  → 命名：[公司]_[客户]_SecurityQuestionnaire_v[版本]_[日期].xlsx
  → 附件清单（证书 / 报告 / 索引页）
```

## 与其他命令的边界

| 选择 | 用前者 | 用后者 |
|------|-------|-------|
| `/security-questionnaire` vs `/compliance-checklist` | 客户问卷应答（被动）| 我方主动建立合规体系 |
| `/security-questionnaire` vs `/rfp-response` | 纯安全维度深度问卷 | 综合 RFP（含部分安全题）|
| `/security-questionnaire` vs `/bid-analyze → /bid-export` 七阶段 | 安全问卷专项 | 招标文件全流程 |
| `/security-questionnaire` vs `/ai-red-team` | 客户对我方安全的评估 | AI 产品红队对抗测试 |
