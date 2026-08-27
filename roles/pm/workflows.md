# PM Workflows — 产品经理典型剧本详解（v2.0 精简版）

> `manifest.yaml` 中每个 `workflow.<name>` 的详细展开。
> v2.0 变更：只保留端到端 6 模块流水线相关剧本，其他历史剧本已随资产移除。

---

## 1. end-to-end-pipeline｜端到端 6 模块流水线（核心）

### 场景说明
从一句话原始需求（老板 / 销售 / 客户）走到完整可交付需求包。适用于：
- 客户来了紧急需求，需要产出完整交付物
- PoC / 招投标响应，需要含技术规格书的完整材料
- 立项后正式进入研发，需要 PRD + 技术规格双件套
- 教一个新 PM 走完一遍完整流程

### 执行步骤（6 模块 + 归档）

#### M2 需求澄清 — `/pm-clarify {raw_input}`
- **输入**：一句话原始需求（"客户想批量导入发票"）
- **处理**：
  - Agent 2-1：7 要素歧义识别（业务目标 / 用户 / 场景 / 成功标准 / 边界 / 约束 / 排除）
  - Agent 2-2：分 3 类生成澄清问题（auto 自问自答 / human 交给 PM）
  - Agent 2-3：冲突检测 + 伪需求识别
- **产出**：`01-clarify-report.md`（含假设项、待确认项、冲突清单）
- **Gate**：PM 审阅确认，可驳回重跑

#### M3 业务方案 — `/pm-solution 01-clarify-report.md`
- **输入**：澄清报告
- **处理**：
  - Agent 3-1：主/分支/异常流程 + P0/P1/P2 功能清单 + 角色权限矩阵 + 本次做/不做
  - Agent 3-2：业务依赖、外部第三方依赖、潜在业务风险
- **产出**：`02-business-solution.md`
- **Gate**：可人工调整优先级

#### M4 原型底稿 — `/pm-prototype 02-business-solution.md`
- **输入**：业务方案
- **处理**：
  - Agent 4-1：页面清单 + 组件 + 4 状态设计 + Mermaid 流程图 + 结构化 JSON
  - Agent 4-2：跳转闭环 / 异常态 / 权限一致性 自动校验
- **产出**：`03-prototype/{desc.md, prototype.json, flow.mmd, flow-exception.mmd, validate.md}`
- **Gate**：PM 编辑修改后确认

#### M5 PRD 主文档 — `/prd --mode full --validate --input 01,02,03`
- **输入**：澄清报告 + 业务方案 + 原型底稿
- **处理**：
  - prd-writer skill 生成多功能完整 PRD（每功能 10 项 + 非功能 + 指标 + 发布 + 风险）
  - pm-prd-validate skill 跑四类校验：完整性 / 一致性 / 歧义文本 / 埋点完整性
- **产出**：`04-PRD.md` + `04-PRD-validate.md`
- **Gate**：PM 修改确认

#### M6 技术规格书 — `/pm-tech-spec 04-PRD.md --input 01`
- **输入**：PRD + 澄清报告
- **处理**（**本工具集的核心差异化能力**）：
  - Agent 6-1：产品技术指标梳理，6 大类（性能 / 安全 / 兼容 / 可靠 / 合规 / 外部依赖）
  - Agent 6-2：完整规格书（10 章）
  - Agent 6-3：可量化 / PRD 一致性 / 验收标准完整性 三项校验
- **产出**：`05-tech-metrics.md` + `05-tech-spec.md` + `05-tech-spec-validate.md`
- **Gate**：PM 修改指标数值后确认

#### M7 归档 — `/pm-archive {output-dir}`
- **输入**：6 类产物
- **处理**：完整性检查、交叉引用检查、语义化版本号、可选 freeze 快照
- **产出**：`README.md` + `CHANGELOG.md` + `VERSION` + `archive-report.md`

### 一键调度

```bash
/pm-pipeline "客户想批量导入发票" --mode human --product-type saas-b
```

流水线会自动按 M2 → M3 → M4 → M5 → M6 → M7 顺序执行，每阶段之间自动 gate。

### 断点续跑 / 局部返工

```bash
# 从 M4 继续
/pm-pipeline ./output/pm-pipeline/xxx/ --from M4

# 只跑 M6（PRD 已经在）
/pm-pipeline ./output/pm-pipeline/xxx/ --from M6 --to M6

# 修改优先级后从 M3 重跑到底
/pm-pipeline ./output/pm-pipeline/xxx/ --from M3
```

### 何时不用完整流水线

- **只需要澄清一份报告** → 单独跑 `/pm-clarify`
- **只需要一份 PRD**（已有澄清 / 业务方案在脑子里） → 直接 `/prd --mode full`
- **只需要补技术规格** → `/pm-tech-spec {已有 PRD}`
- **只需要归档** → `/pm-archive {已有目录}`

---

## 2. competitive-analysis｜竞品分析工程化（横向能力）

### 场景说明

主流水线关注"内部产品需求"，竞品分析是**横向输入能力**。适用于：

- 立项前的市场判断（我方要不要做？跟谁竞争？）
- PRD 中的"竞品对比"章节
- 定价前的价格锚定
- 销售培训 / 售前应答话术准备
- 季度 / 半年度竞品情报刷新
- 客户对比投诉后的紧急更新

### 执行步骤（2 阶段）

#### 阶段 1：竞品发现 + 情报采集 — `/pm-competitive-scan {产品定位}`
- **输入**：产品定位 / 客户场景描述
- **处理**：
  - 竞品发现（强制 4 类都覆盖：直接 / 间接 / 替代 / 自建）
  - 多信源采集（🟢 官方一手 → 🟡 三方评测 → 🟠 社区口碑）
  - 情报卡结构化（12 字段 JSON）
  - 可信度分级（🟢 / 🟡 / 🟠 / 🔴）
- **产出**：`01-competitor-list.md` + `01-competitors.json` + 单竞品卡若干
- **Gate**：竞品清单确认 + 采集完成确认

#### 阶段 2：多维对标 + 差异化定位 + 应对策略 — `/pm-competitive-benchmark 01-competitors.json`
- **处理**：
  - 5 维对标（功能矩阵 / 定价矩阵 / 生态 / 口碑雷达 / 技术架构）
  - 5 类洞察产出（绝对优势 / 绝对劣势 / 价值链差距 / 定价错位 / 未满足需求）
  - Blue Ocean 四象限（消除 / 减少 / 提升 / 创造）
  - Positioning 定位矩阵（二维象限）
  - 应对四象限（领先 / 侧翼 / 跟随 / 避战 / 合作）
  - 销售话术 + 竞品 FAQ
- **产出**：`02-benchmark-matrix.md` + `02-insights.md` + `02-positioning.md` + `02-strategy.md` + `02-sales-playbook.md` + `02-report-full.md`
- **Gate**：战略产出确认

### 一键调度

```bash
# 完整两阶段
/pm-competitive "AI 写作助手，面向中小企业内容营销" --depth deep

# 加种子竞品
/pm-competitive "AI 写作助手" --seed "Jasper,Copy.ai,ChatGPT,Notion AI"

# 常态月度轻量刷新
/pm-competitive ./output/competitive/ai-writer-{date}/ --mode monitor

# 季度全量刷新（对比历史版本）
/pm-competitive ./output/competitive/ai-writer-{date}/ --mode refresh

# 只做定价对比（客户临时对比价格用）
/pm-competitive "AI 写作助手" --focus pricing
```

### 与主流水线的组合使用

```
1. 立项前
   /pm-competitive "定位" → 02-report-full.md
   → /pm-clarify "需求" 引用报告作为背景

2. 业务方案定位
   竞品报告 → /pm-solution 引用作为差异化依据

3. PRD 补"竞品对比"章节
   /prd --mode full --input ./01-clarify.md,./competitive/xxx/02-report-full.md

4. 常态跟踪
   每月 /pm-competitive --mode monitor
   每季度 /pm-competitive --mode refresh
```

### 何时不用竞品分析

- **单纯写 PRD** 且不需要外部竞争视角 → 走 `/prd` 单命令
- **客户具体项目的竞争定位**（RFP 应答） → 走 `/sa-solution-map`（SA 场景）
- 只需要"知道有哪些竞品"清单 → 走 `--mode full --depth quick`（30 分钟出结果）

---

## 剧本编写规范


新增 workflow 时的要求：

1. **trigger 关键词 3-8 个**：太少覆盖不到用户表达，太多容易误触发
2. **步骤要有 produces**：产出文件路径明确，方便下一步 --input
3. **说明"何时不用"**：帮助 LLM 判断边界
4. **保持流水线一致性**：不引入已删除的历史命令
