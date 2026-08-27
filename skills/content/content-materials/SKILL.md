---
name: content-materials
description: 项目素材抽取方法论工具箱 — 供 /content-materials 命令调用。含 PM/SA 项目产物结构清单、按文体的抽取维度映射、素材可信度分级、禁止提及识别。
user-invocable: false
---

# content-materials — 项目素材抽取工具箱

> 本 skill 被 `/content-materials` 命令调用。

## 一、PM/SA 项目产物结构清单

### PM 项目（`./output/pm-pipeline/*/`）

| 文件 | 抽取维度 |
|---|---|
| `01-clarify-report.md` | 客户 / 用户 / 场景 / 痛点 / 假设项 / 待确认项 |
| `02-business-solution.md` | 功能清单（P0/P1/P2）/ 流程 / 权限 / 依赖 |
| `03-prototype/*.md` | 页面清单 / 组件 / 交互 |
| `03-prototype/*.json` | 结构化原型（可用于 PPT 生成） |
| `03-prototype/*.mmd` | Mermaid 流程图 |
| `04-PRD.md` | **主素材源** — 完整产品定义 |
| `04-PRD-validate.md` | 已知问题（可用于 tech-popular 的"限制"章节） |
| `05-tech-metrics.md` | 六大类技术指标（性能 / 安全 / 兼容 / 可靠 / 合规 / 依赖） |
| `05-tech-spec.md` | 技术规格书（**技术白皮书主素材**） |
| `README.md` | 项目一句话 + 版本 + 状态 |
| `CHANGELOG.md` | 迭代历史（可用于 PR 稿的"版本演进"） |

### SA 项目（`./output/sa-pipeline/*/`）

| 文件 | 抽取维度 |
|---|---|
| `00-intake.json` | 客户元信息 |
| `01-clarify-report.md` | 客户调研痛点（**解决方案文主素材**） |
| `02-solution-map.md` | 我方能力映射 / 竞品对比 / 定制点 |
| `03-overall-solution.md` | 完整方案（**解决方案白皮书主素材**）|
| `03-architecture.mmd` | 架构图源码 |
| `03-solution-validate.md` | 校验报告（可警示未回应痛点） |
| `04-poc-plan.md` | POC 场景 / 验收标准 |
| `04-impl-plan.md` | 实施阶段 / RACI / 培训 |
| `04-rfp-response.md` | 应答表（**有明确产品承诺，可作为白皮书具体能力）** |
| `04-deviation-table.md` | 技术偏离（不能对外说的东西） |
| `05-config-estimate.md` | 配置估算（⚠️ § 商务提醒 严禁对外） |
| `05-presentation-outline.md` | PPT 大纲（可复用） |
| `05-pitch-script.md` | 汇报话术（**推文 / PR 稿参考语调**） |
| `README.md` | 项目一句话 |

### Competitive 项目（`./output/competitive/*/`）

| 文件 | 抽取维度 |
|---|---|
| `02-report-full.md` | 差异化 / 应对话术 / 竞品对比（**推广文卖点素材**） |
| `02-sales-playbook.md` | 销售话术（可用于推广文语气） |

## 二、按文体的抽取维度映射

| Style | 主要素材维度 | 次要素材维度 |
|---|---|---|
| `promo` | 优势、痛点、场景、客户案例 | 差异化 |
| `solution-doc` | 痛点、解决方案、部署、能力映射 | 收益、场景 |
| `tech-whitepaper` | 架构、技术原理、技术指标 | 安全、性能、局限 |
| `ppt` | 一句话价值、痛点、方案、差异化 | 案例、下一步 |
| `solution-whitepaper` | 行业背景、痛点、方案、落地路径、案例 | 收益、实施建议 |
| `activity-tweet` | 新亮点、福利、引导行动 | 简短痛点 |
| `pr` | 事件、企业观点、产品亮点、展望 | 引用（客户 / 分析师） |
| `tech-popular` | 是什么、解决什么、怎么工作 | 局限、演进方向 |

## 三、素材抽取规则

### 抽取流程（按维度）

```
产品能力（capabilities）
  ├── 从 PRD § 功能描述 提取功能名 + 输入 + 输出
  └── 从 tech-spec § 各模块规格 补技术细节

架构（architecture）
  ├── overall-solution § 技术架构（文字）
  └── architecture.mmd（图源码）

优势（strengths）
  ├── 从 solution-map § 竞品对比 提取
  ├── 从 competitive/02-report-full.md 提取 Blue Ocean § 创造
  └── 兜底：从 tech-spec 的严重度=高指标推断

痛点（pain-points）
  ├── SA clarify-report § 3 业务痛点列表
  └── PM clarify-report § 用户痛点

技术指标（metrics）
  ├── tech-metrics 六大类
  └── 只抽严重度=高的对外披露

场景（scenarios）
  ├── business-solution § 主流程 / 分支流程
  └── prototype 页面清单

案例（cases）
  ├── 项目 _frozen 目录的历史归档版本
  └── 引用时必须匿名 or 已授权

合规（compliance）
  ├── tech-spec § 合规指标
  └── intake § 合规约束

禁止提及（forbidden）
  ├── ContentRequest.forbidden
  ├── clarify-report § 假设项
  ├── 05-config-estimate § 商务提醒
  ├── 04-deviation-table（技术偏离）
  └── 未上线功能
```

## 四、素材可信度分级

| 级别 | 判定 | 处理 |
|---|---|---|
| 🟢 高 | 来自 PRD / tech-spec 主文件 | 直接引用 |
| 🟡 中 | 来自 solution 或 rfp-response（已承诺客户） | 引用 + 保留出处 |
| 🟠 低 | 假设项 / 待确认项 | ⚠️ 加"当前设计" or "预计"限定 |
| 🔴 极低 | 商务提醒 / 内部策略 / 偏离表 | **严禁对外**，加入 forbidden |

## 五、禁止提及识别规则

### 必扫内容
| 位置 | 禁止对外 |
|---|---|
| `01-clarify-report § 7 假设项` | 未确认的产品承诺 |
| `05-config-estimate § 商务提醒` | 内部估算 / 竞品价格 / 报价策略 |
| `04-deviation-table` | 技术偏离（不能对外说不满足） |
| `03-solution-validate` | 校验失败项（未回应的痛点） |
| `review-notes.md` | 内部评审意见 |
| `_frozen/*/` 除非授权 | 具体客户名 |

### 自动添加到 forbidden
- 未上线的探索性功能
- 内部代号 / 项目代号
- 客户真名（除非授权披露）
- 具体报价数字
- 竞品负面评价

## 六、缺失章节警示

如果关联项目缺失某些产物，主动警示下游影响：

| 缺失 | 影响文体 | 建议 |
|---|---|---|
| tech-metrics.md | 技术白皮书 / 白皮书性能章节 | 补跑 /pm-tech-spec |
| architecture.mmd | 技术白皮书 / PPT 架构页 | 补跑 /sa-architect |
| 客户案例 | 解决方案白皮书 § 案例 | 手工补 or 引用其他项目 |
| business-solution | 解决方案文 § 应用场景 | 补跑 /pm-solution |

## 七、素材冲突处理

同一事实在不同产物中表述不一致时：

| 冲突 | 优先级 |
|---|---|
| PRD vs tech-spec | tech-spec（更具体） |
| clarify-report vs PRD | PRD（更成熟） |
| solution-map vs overall-solution | overall-solution（更完整） |
| _frozen vs 主文件 | 主文件（更新） |

**记录**：所有冲突需要在素材池 § 素材冲突 章节列出。

## 八、反模式

- ❌ 抽取的素材不带来源 —— 违规
- ❌ 可信度栏空 —— 违规
- ❌ 把 🔴 的商务提醒抽出来 —— 严重违规
- ❌ 抽取时不看 forbidden 清单 —— 会踩合规雷
- ❌ 缺失章节静默处理 —— 违规，必须显式警示
