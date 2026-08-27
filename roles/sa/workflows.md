# SA Workflows — 售前解决方案工程师典型剧本详解（v1.0）

> `manifest.yaml` 中每个 `workflow.<name>` 的详细展开。
> 本 role 服务对外客户售前项目场景，与服务内部 PRD 场景的 `/pm` 互补。

---

## 1. end-to-end-presales｜端到端售前流水线（核心）

### 场景说明

从销售转述的一句话客户信息 / 完整 RFP 招标文件走到完整可交付售前包。适用于：
- 销售给回碎片化模糊客户信息，需要补齐调研缺口
- 拿到 RFP 招标文件，需要产出应答表 + 偏离表 + 报价底稿
- 客户 POC 立项，需要产出 POC 测试方案 + 环境要求
- 项目立项后需要出总体方案 + 架构图给客户汇报

### 执行步骤（7 模块 + 归档）

#### M1 输入网关 — `/sa-intake {raw_input}`
- **输入**：销售一句话 / RFP PDF / 客户访谈录音转写 / 客户 PPT / Excel 需求清单
- **处理**：
  - 非结构化清洗（过滤寒暄、提取业务现状 / 诉求 / 约束 / 顾虑）
  - 元信息抽取（行业 / 规模 / 现有系统 / 痛点 / 预算 / 时间 / 招标约束 / 干系人）
  - 需求模糊等级（高度模糊 / 部分明确 / RFP 明确）
- **产出**：`00-intake.json`（结构化项目对象）
- **Gate**：确认关键字段

#### M2 客户调研澄清 — `/sa-clarify 00-intake.json`
- **输入**：项目对象
- **处理**：
  - Agent 2-1：信息缺口 & 歧义识别（现有 IT / 业务流程 / 痛点 / 合规 / 性能 / 边界 / 禁止项）
  - Agent 2-2：调研问题生成（人机模式：给售前的访谈清单 / 假设补全模式：基于同行业案例补假设）
  - Agent 2-3：痛点收敛（表面诉求 vs 真实痛点 / 业务/技术/合规 分类 / 伪需求 / 冲突）
- **产出**：`01-clarify-report.md`（含客户概况、IT 现状、显性/隐性需求、约束、假设项、待确认项、风险初判）
- **Gate**：售前确认，可驳回

#### M3 方案拆解定位 — `/sa-solution-map 01-clarify-report.md`
- **输入**：调研痛点报告
- **处理**：
  - Agent 3-1：业务-能力映射（客户业务流程 + 痛点→我方能力对照表 + 完全/部分/不支持覆盖 + 定制点）
  - Agent 3-2：竞品对标（识别我方优势 / 劣势 / 规避点 + 客户可能对比的竞品）
  - Agent 3-3：项目风险（外部依赖 / 集成 / 定制 / 合规 / 实施风险）
- **产出**：`02-solution-map.md`
- **Gate**：可人工调整能力匹配 + 标记定制范围

#### M4 总体方案架构 — `/sa-architect 02-solution-map.md`
- **输入**：方案定位
- **处理**：
  - Agent 4-1：总体方案（目标 / 业务架构 / 技术架构 + Mermaid / 模块组成 / 部署模式 / 集成关系）
  - Agent 4-2：方案校验（痛点匹配 / 约束合规 / 可行性 三项自动校验）
- **产出**：`03-overall-solution.md` + `03-architecture.mmd` + `03-solution-validate.md`
- **Gate**：售前确认

#### M5 专项方案（三合一）
可并行生成，也可选择性生成：

##### M5.1 `/sa-poc 03-overall-solution.md`
- **产出**：`04-poc-plan.md`（POC 目标 / 范围 / 环境要求 / 测试用例 / 验收标准 / 周期 / 输出 / 风险）

##### M5.2 `/sa-impl 03-overall-solution.md`
- **产出**：`04-impl-plan.md`（实施阶段划分 / 步骤 / 人员角色 / 上线切换 / 培训计划）

##### M5.3 `/sa-rfp <RFP 原文> 03-overall-solution.md`
- **产出**：`04-rfp-response.md`（逐条应答 + 满足/部分/不满足） + `04-deviation-table.md`（技术偏离表）

#### M6 报价 & 宣讲底稿 — `/sa-quote 03-overall-solution.md 04-poc-plan.md`
- **输入**：总体方案 + 部署模式 + 客户规模指标
- **处理**：
  - Agent 6-1：配置估算（模块选型 + 服务器/存储/许可 + 定制开发工作量初估）
  - Agent 6-2：宣讲材料底稿（PPT 大纲 + 每页文案 + 客户汇报话术）
- **产出**：`05-config-estimate.md` + `05-presentation-draft.md`
- **注意**：估算只是底稿，最终报价由商务人工确认

#### M7 归档 — `/sa-archive {output-dir}`
- **处理**：完整性检查 + 交叉引用 + 语义化版本 + 局部重跑管理 + Markdown/Word 导出
- **产出**：`README.md` + `CHANGELOG.md` + `VERSION` + `archive-report.md`

### 一键调度

```bash
/sa-pipeline "某制造业客户，现有一套老旧 MES，希望替换，需要私有化部署，有国产化要求，大概 3 个月要上线" \
  --industry manufacturing --compliance 等保三级,国产化 --deployment private
```

### 断点续跑 / 局部重跑

```bash
# 客户需求变更了部署模式，只重跑 M4 → M5 → M6
/sa-pipeline ./output/sa-pipeline/xxx/ --from M4

# 只重跑 RFP 应答（新 RFP 版本到了）
/sa-rfp ./new-rfp.pdf ./output/sa-pipeline/xxx/03-overall-solution.md

# 只补一份 POC 方案
/sa-poc ./output/sa-pipeline/xxx/03-overall-solution.md
```

### 何时不用完整流水线

- **只解析一份 RFP** → 单独跑 `/sa-intake ./rfp.pdf`
- **已经有方案，补 POC** → 直接 `/sa-poc {已有方案}`
- **只需要报价估算** → `/sa-quote`（前提是有方案）
- **只需要归档已有产物** → `/sa-archive {已有目录}`

---

## 剧本编写规范

新增 workflow 时的要求：

1. **trigger 关键词 3-8 个**：太少覆盖不到用户表达，太多容易误触发
2. **步骤要有 produces**：产出文件路径明确，方便下一步 --input
3. **说明"何时不用"**：帮助 LLM 判断边界
4. **保持流水线一致性**：不引入已删除的历史命令
5. **售前特有约束**：报价类必须标注"底稿，非最终"
