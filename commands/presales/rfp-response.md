---
name: rfp-response
description: >
  RFP / RFI 应答生成器 — 把客户的招标问询文件（Excel / Word）逐条结构化应答，
  含 4 级应答模式（满足 / 部分 / 替代 / 不满足）、Winning Themes 植入、
  分工矩阵、应答 KB 复用、风险措辞红线、提交前评审清单。
user-invocable: true
argument-hint: "<RFP 文件路径或描述> [--mode draft|review|kb-build] [--industry fintech|gov|healthcare|saas] [--themes <核心讯息1,讯息2,讯息3>] [--out path]"
---

# /rfp-response — RFP / RFI 应答生成器

加载技能：`skills/presales/rfp-response/SKILL.md`
配套 Skill：`skills/presales/security-questionnaire/SKILL.md`（含安全题时自动联动）

## 触发条件
客户给了一份结构化问题清单（Excel / Word / 在线问卷）需要逐条应答。

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `<RFP 文件路径或描述>` | RFP 文件 / 问题清单 | — |
| `--mode` | 工作模式 | `draft` |
| `--industry` | 客户行业（影响话术）| — |
| `--themes` | 自定义 Winning Themes | 默认 5 套 |
| `--out` | 输出路径 | `./outputs/rfp-response/` |

### 工作模式

| `--mode` | 说明 |
|----------|------|
| `draft` | 第一轮草稿生成（80% 完成度，标注待补充项）|
| `review` | 评审已有应答（一致性 / 完整性 / 风险 / 客户化 / 格式）|
| `kb-build` | 把已完成的 RFP 应答归档到 KB，标准化未来复用 |

## 使用示例

```
/rfp-response ./CustomerX_RFP.xlsx --industry fintech --themes "国产化,等保三级,本地化服务"
/rfp-response ./Bank_Tender.docx --mode draft --industry fintech
/rfp-response ./Old_RFP_Done.xlsx --mode kb-build
/rfp-response ./Draft_v1.xlsx --mode review --industry gov
```

## 执行流程

```
Step 1: 拆解 + 分类
  → 把 RFP 问题按 8 大类分（功能 / 安全 / 性能 / 集成 / 合规 / 部署 / 服务 / 商务）
  → 每条标记敏感度（普通 / 法务 review / 高管 review）

Step 2: 应答模式判定
  → 我方完全做到 → ✅ 满足
  → 80%+ 做到 → ⚠️ 部分（明确边界）
  → 业务效果可达 → 🔄 替代方案
  → 当前做不到 → ❌ 不满足（roadmap 时间表）

Step 3: 应答正文生成
  → 每条问题：结论 + 1-3 条证据 + 风险说明
  → 客户化语言（客户行业术语，避免我方产品行话）
  → Winning Themes 植入（每 5-10 条问题穿插一次）

Step 4: 风险措辞扫描
  → 自动替换"100% / 完全 / 永久 / 唯一"等绝对化表述
  → 标记需法务 / 高管 review 项

Step 5: 评审清单
  → 一致性 / 完整性 / 风险 / 客户化 / 格式 五维度
  → 输出待补充项清单（哪些需要 PoC 验证 / 法务确认）

Step 6: 文件打包
  → 命名规范：[公司]_[客户]_[项目]_应答_v[版本]_[日期].xlsx
  → 附件清单（资质证书 / 案例 / 报告）
```

## 与其他命令的边界

| 选择 | 用前者 | 用后者 |
|------|-------|-------|
| `/rfp-response` vs `/bid --phase 1..7` 七阶段 | 问题清单逐条应答 | 招标文件全流程编制 |
| `/rfp-response` vs `/proposal` | 问答风格 | 大块叙述方案 |
| `/rfp-response` vs `/security-questionnaire` | 综合 RFP（部分含安全题）| 纯安全问卷（200+ 条 VSQ）|
| `/rfp-response` vs `/gap-analysis` | 客户问 → 我方答 | 客户需求 vs 产品能力主动映射 |
