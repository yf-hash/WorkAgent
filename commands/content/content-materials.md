---
name: content-materials
description: 【模块 2】项目素材抽取 Agent — 从关联的 PM/SA 项目目录，抽取 PRD / 技术规格 / 方案 / 痛点报告等产物，过滤无关内容，整理成结构化素材池（含引用出处）供下游写作 Agent 调用，避免文案与产品实际能力不符。
user-invocable: true
argument-hint: "<00-content-request.json 路径> [--project <path>] [--focus product|solution|pain-points|architecture|metrics|all] [--out <path>]"
allowed-tools: [Read, Write, Edit, AskUserQuestion, Grep, Glob]
harness:
  execute:
    preset: writing-scoped
  constrain:
    profile: writing-safe
    gates: [before-write, after-extract]
  loop:
    mode: pipeline
    stages: [项目产物扫描, 内容过滤与抽取, 素材结构化, 引用回溯建立]
  memory:
    scope: project
    reads: [project-context, content-intake-history]
    writes: [content-materials-history]
  security:
    danger-level: low
---

# /content-materials — 项目素材抽取（Module 2）

> **端到端内容创作流水线的第 2 站**
>
> /content-intake →【本命令】→ /content-generate → /content-validate → /content-archive

## 一句话

**读取关联的 PM/SA 项目产物库，抽取产品能力、架构、优势、客户痛点、技术指标，输出结构化素材池**，供下游生成 Agent 引用，避免"文案与产品实际能力脱节"。

## 触发条件

- ContentRequest.project.linked = true
- 或 --project 参数显式指定

**无关联项目时**：本命令**自动跳过**，由 M3 生成阶段基于用户输入直接创作。

## 输入

```bash
# 最常见：接 M1 输出（其中含 project 关联）
/content-materials ./output/content-pipeline/xxx/00-content-request.json

# 显式覆盖项目路径
/content-materials ./00-content-request.json --project ./output/pm-pipeline/vulnhunter-20260827/

# 只抽取特定维度
/content-materials ./00-content-request.json --focus product
/content-materials ./00-content-request.json --focus pain-points
/content-materials ./00-content-request.json --focus all  # 默认
```

## 内部四阶段

### 阶段 1：项目产物扫描

按项目类型识别可用产物：

**PM 项目**：
- `01-clarify-report.md` → 客户 / 用户 / 痛点 / 假设
- `02-business-solution.md` → 功能 / 流程 / P0/P1/P2 / 权限
- `03-prototype/*.md` → 页面 / 组件
- `04-PRD.md` → 完整产品定义（主素材源）
- `05-tech-metrics.md` → 六大类技术指标
- `05-tech-spec.md` → 完整技术规格书
- `README.md` → 一句话概览 + 版本

**SA 项目**：
- `01-clarify-report.md` → 客户调研痛点
- `02-solution-map.md` → 我方能力映射 + 竞品对比
- `03-overall-solution.md` → 完整方案 + 架构
- `03-architecture.mmd` → 架构图源码
- `04-poc-plan.md` → POC 场景 + 验收
- `04-rfp-response.md` → 应答表（有明确产品承诺）
- `05-config-estimate.md` → 配置估算（谨慎使用）
- `README.md` → 项目概览

**Competitive 项目**（如关联）：
- `02-report-full.md` → 竞品差异化 + 应对话术

### 阶段 2：内容过滤与抽取

依 `content-request.style` 和 `focus` 抽取不同维度：

| 抽取维度 | 用途 | 来源 |
|---|---|---|
| **产品能力**（capabilities） | 推广文 / 解决方案文 / 白皮书 | PRD § 功能描述 + tech-spec § 模块规格 |
| **架构**（architecture） | 技术白皮书 / PPT | overall-solution + arch.mmd + tech-spec |
| **优势**（strengths） | 推广文 / PR 稿 / 推文 | 竞品对比 + PRD § 差异化 |
| **客户痛点**（pain-points） | 解决方案文 / 白皮书 | clarify-report § 痛点 + solution-map |
| **技术指标**（metrics） | 技术白皮书 / 白皮书性能章节 | tech-metrics（六大类 SLA/性能/合规） |
| **典型场景**（scenarios） | 解决方案文 / 白皮书 | business-solution § 主流程 + prototype |
| **客户案例**（cases） | 解决方案白皮书 / 推广文 | archived _frozen 的过往项目 |
| **合规能力**（compliance） | 政企客户白皮书 | tech-spec § 合规 + intake § 合规约束 |
| **禁止提及**（forbidden） | 全部 | intake.forbidden + validate 记录 |

### 阶段 3：素材结构化

每条素材含 5 要素：

```markdown
### 素材编号：M-001
- **类别**：产品能力
- **内容**：VulnHunter 支持分布式沙箱调度，可同时运行 100 个隔离沙箱
- **来源**：./output/pm-pipeline/vulnhunter-20260827/04-PRD.md § 3.2 沙箱模块
- **可信度**：🟢 高（一手 PRD）
- **可用于**：推广文（核心卖点）/ 白皮书（技术架构章节）/ PR 稿（新版本亮点）
```

### 阶段 4：引用回溯建立

每条素材都有明确出处（文件路径 + 章节），后续 M4 校验会用这个做引用可追溯性校验。

## Harness 卡点

**抽取后 gate**：AskUserQuestion 展示：
```
【M2 素材抽取完成】共抽取 {n} 条素材：
  产品能力：{p} 条
  架构：{a} 条
  痛点：{q} 条
  技术指标：{m} 条
  客户案例：{c} 条
  合规：{l} 条

发现的问题：
  ⚠️ 缺失章节：{列表}（下游生成可能不完整）
  ⚠️ 素材冲突：{列表}（同一事实不同表述）

请选择：
(1) 通过 → 进入 M3 生成初稿
(2) 补充素材 → 让我补跑或手动加
(3) 忽略缺失继续
(4) 中止
```

## 输出格式

```markdown
# 素材池：{{topic}}

> 生成时间：{{yyyy-mm-dd hh:mm}}
> 关联项目：{{project.path}}
> ContentRequest：./00-content-request.json
> 抽取维度：{{focus}}

## 项目概览
- 项目名：VulnHunter 漏洞猎人
- 版本：v1.0.0
- 项目类型：PM
- 关键人员：{{...}}
- 上次归档时间：{{...}}

## 素材总表
| # | 类别 | 内容摘要 | 来源 | 可信度 |
|---|---|---|---|---|
| M-001 | 产品能力 | 分布式沙箱调度 | PRD § 3.2 | 🟢 |
| M-002 | 技术指标 | 单沙箱 P95 ≤ 500ms | tech-spec § 4.1 P3 | 🟢 |
| ... | ... | ... | ... | ... |

## 分类明细

### 产品能力（{p} 条）
（详细的 M-001, M-002...）

### 架构（{a} 条）
（含 Mermaid 源码引用）

### 痛点（{q} 条）

### 技术指标（{m} 条）

### 客户案例（{c} 条）
（说明：本项目 _frozen/ 中的历史客户可用于素材，需确认是否可对外披露）

### 合规能力（{l} 条）

## 禁止提及清单
从 ContentRequest.forbidden + 项目 assumptions 提取：
- 内部估算数字（如 05-config-estimate 的商务提醒章节）
- 未上线的实验性能力
- 客户名（除非明确授权披露）

## 缺失章节提醒
| 缺失 | 影响 | 建议 |
|---|---|---|
| 项目未跑 tech-spec | 白皮书性能章节将只能定性 | 补跑 /pm-tech-spec |
| 项目无客户案例 | 白皮书案例章节需外部补 | 手工补 or 从其他项目引用 |

## 推荐下一步
- [ ] 认可素材 → `/content-generate ./00-content-request.json ./01-material-pool.md`
- [ ] 需补充 → 本命令 `--refine "补 XX 维度"`
```

## 与其他命令的边界

| 场景 | 用 |
|---|---|
| **PM/SA 项目产物 → 结构化素材池** | 本命令 |
| 无关联项目直接写 | 跳过本命令，M3 基于用户输入直接生成 |
| 生成初稿 | 下一步 `/content-generate` |
| 一键端到端 | `/content`（编排器） |

## 反模式

- ❌ 素材没有 5 要素完整（含来源）—— 违规
- ❌ 可信度栏空缺 —— 违规
- ❌ 未提示"缺失章节" —— 下游 M3 会盲写
- ❌ 未标"禁止提及" —— 会踩合规雷
- ❌ 从其他项目"借"素材未标注 —— 事实错误温床
