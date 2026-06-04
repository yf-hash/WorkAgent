---
name: product-doc
description: >
  B2B 产品资料体系 — 24 类标准产品文档生成器。覆盖产品白皮书、技术白皮书、
  产品介绍 PPT（商务/技术版）、产品彩页、解决方案、操作手册、部署手册、
  招投标参数、培训材料、成功案例、版本说明、兼容性文档、竞品分析等。
  含命名规范、密级管理、修订记录、14 项自查清单。
  适用于：新产品上市资料套件、版本更新同步、竞标备战、行业化定制。
user-invocable: true
argument-hint: "<产品名称> [--type whitepaper|tech-whitepaper|brochure|solution|manual|deploy|training|case|release-note|compat|bid-params|competitive|fullset] [--industry fintech|gov|healthcare|edu|mfg|retail|saas] [--version v1.0] [--confidential]"
---

# /product-doc — B2B 产品资料体系生成器

加载技能：`skills/product-doc-writer/SKILL.md`
配套核验：`skills/doc-auditor/SKILL.md`（自动调用）
配套编排：`@product-enablement`（多文档批量生产时使用）

## 触发条件
需要编写产品白皮书、技术白皮书、产品彩页、解决方案、操作手册、部署手册、招投标参数、培训材料、成功案例、版本说明、兼容性文档、竞品分析等 B2B 产品资料时。
单文档生成用本命令；多文档批量套件用 `@product-enablement`。

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `<产品名称>` | 产品全称（必填） | — |
| `--type` | 文档类型（见下表，必填） | `whitepaper` |
| `--version` | 当前版本号 | `v1.0` |
| `--industry` | 目标行业（影响内容侧重） | — |
| `--confidential` | 标记为内部保密文档 | `false` |
| `--out` | 输出路径 | `./outputs/` |

### 文档类型

| `--type` | 文档名 | 受众 | 密级 | 篇幅 |
|----------|-------|------|------|------|
| `whitepaper` | 产品白皮书 | 技术负责人 / 方案架构师 | 可公开 | ≥20 页 |
| `tech-whitepaper` | 技术白皮书 | 技术专家 / 架构师 | **内部保密** | ≥30 页 |
| `brochure` | 产品彩页 | 展会 / 客户拜访 | 可公开 | A4 双面或三折页 |
| `intro-business` | 产品介绍-商务版 PPT | 商务决策层 / 采购委员会 | 可公开 | 15-25 页 |
| `intro-tech` | 产品介绍-技术版 PPT | 技术决策层 / IT 负责人 | 可公开 | 20-40 页 |
| `solution` | 产品解决方案 | 行业客户 / 售前对接 | 可公开 | 30-60 页 |
| `manual` | 产品操作手册 | 终端用户 / 运维 | 可公开 | 按功能模块 |
| `deploy` | 部署及配置手册 | 实施工程师 | 可公开 | 按部署模式 |
| `training` | 培训材料套件 | 渠道商 / 客户 / 内部 | 可公开 | 课件 + 实操 |
| `case` | 成功案例 | 销售场景 / 合规验证 | 可公开 | 3-8 页 |
| `release-note` | 版本说明 | 全员 + 客户 | 可公开 | 按变更项 |
| `compat` | 兼容性文档 | 集成商 / 实施 | 可公开 | 按平台矩阵 |
| `bid-params` | 招投标参数 | 标书编写 / 销售 | **内部保密** | 完整版 + 精简版 |
| `competitive` | 竞品分析 | 销售 / 售前 | **内部保密** | 含应对话术 |
| `function-list` | 产品型号及功能清单 | 商务 / 销售 | 可公开 | Excel |
| `sales-faq` | 销售常见问题 | 销售 / 售前 | 可公开 | 5 大类问答 |
| `fullset` | 完整 24 类资料套件 | — | 混合 | 引导转 `@product-enablement` |

### 行业定制

| `--industry` | 内容侧重 |
|--------------|---------|
| `fintech` | 合规审计 / 风险控制 / 数据安全 |
| `gov` | 政策符合性 / 国产化 / 可控性 |
| `healthcare` | 数据合规 / 互联互通 / 稳定性 |
| `edu` | 易用性 / 扩展性 / 性价比 |
| `mfg` | 系统集成 / 工厂部署 / ROI |
| `retail` | 转化率 / 用户体验 / 数据洞察 |
| `saas` | 功能完整性 / 集成生态 / API |

## 使用示例

```
/product-doc 数据安全网关 --type whitepaper --version v2.0
/product-doc 零信任访问控制 --type solution --industry fintech
/product-doc 终端检测响应 --type tech-whitepaper --confidential
/product-doc 智能运维平台 --type bid-params --industry gov
/product-doc API 安全防护 --type case --industry fintech
/product-doc 数据治理平台 --type fullset --industry fintech    # 转 @product-enablement
```

## 执行流程

```
Step 1: 信息采集
  → 必问：一句话定位 / 三大差异化优势 / 目标客户 / 产品形态 / 已有案例
  → 按 type 追问：
    [solution] 行业监管背景？业务痛点排序？
    [bid-params] A/B 级排他性优势？
    [competitive] 主要竞品 3-5 家？各自核心卖点？
    [tech-whitepaper] 技术架构层级？关键算法？性能数据？

Step 2: 结构填充
  → 加载 product-doc-writer 中对应文档的结构模板
  → 将采集到的产品信息填入框架
  → 每章生成 ≥80% 完整草稿（剩余 20% 标注 [需补充：xxx]）

Step 3: 命名规范
  → [产品名]【版本号】[文档类别]_版本号.扩展名
  → 自动判断密级（标记"内部保密"水印）
  → 添加修订记录表 + 法律声明 + 版权信息

Step 4: 14 项自查（doc-auditor 自动调用）
  → F1 命名 / F2 修订记录 / F7 封面对比度
  → C1 产品名 / C2 版本一致性 / C3 截图
  → 输出自查报告（✅ / ⚠️ / ❌）

Step 5: 输出
  → 文档正文 + 自查报告 + 待补充清单
  → 建议下一份配套文档（如白皮书 → 技术白皮书 / 解决方案）
```

## 与其他命令的边界

| 选择 | 用前者 | 用后者 |
|------|-------|-------|
| `/product-doc` vs `@product-enablement` | 单份文档生产 | 多份文档批量编排 |
| `/product-doc --type solution` vs `/proposal` | 产品级标准解决方案（可复用）| 项目型一次性方案（响应特定客户）|
| `/product-doc --type sales-faq` vs `/sales-guide` | 单独的 FAQ 文档 | 完整销售一页禅 |
| `/product-doc` vs `/doc-audit` | 生成新文档 | 审计已有文档库 |
| `/product-doc --type case` vs `/win-loss` | 对外可发布的成功案例 | 内部赢单失单分析 |
