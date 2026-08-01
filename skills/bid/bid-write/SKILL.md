---
name: bid-write
description: >
  标书第 4 阶段：分模块撰写与内容填充。9 个模块的写作规范（understanding/solution/implementation/management/
  quality/service/performance/team/commercial）。可通过 --interactive / --batch / --kb / --figures 调用标志
  控制交互模式、RAG 知识库引用与配图引用，但本 Skill 的核心职责始终是「按大纲写章节」。
  触发词：标书撰写、技术方案写作、分章节写、bid write。
  不做：拆解（→ bid-analyze）/ 大纲（→ bid-outline）/ 评审（→ bid-review）/ 核查（→ bid-check）/ 导出（→ bid-export）。
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
    danger-level: medium
---

# Bid Write — 标书 Phase 4 分模块撰写

> 单一职责：标书七阶段第 4 阶段（分模块写作）。
> 上游：`bid-outline` 的大纲与字数配比。
> 下游：`bid-review` 双轮评审。

## 写作模式

- **交互模式**（默认）：逐章确认后继续，支持即时修改
- **批量模式**：一键生成全部章节，自动检查点保存
- **RAG 增强**：基于知识库真实资料生成，避免幻觉
- **配图生成**：调用 `mermaid-chart` / `html-chart` skill 生成架构图、流程图、拓扑图

## 各模块写作规范

| section | 内容 | 核心写作逻辑 |
|---------|------|-------------|
| `understanding` | 项目理解与需求分析 | 痛点 → 影响 → 解决方案（业务视角升华，非照搬招标文件） |
| `solution` | 技术解决方案（核心） | 每功能点对应招标要求，明确实现方式；多图表少大段文字 |
| `implementation` | 项目实施方案 | 甘特图、里程碑、资源投入；响应实施周期和人员要求 |
| `management` | 项目管理与组织 | 团队成员及资质；沟通机制、汇报频率 |
| `quality` | 质量保障体系 | 测试方案、验收标准、质量度量指标 |
| `service` | 售后服务承诺 | 分级 SLA、驻场/远程比例、服务内容清单 |
| `performance` | 业绩证明与案例 | 同行业/同规模/同类型优先；含项目名称、规模、效果、证明材料 |
| `team` | 团队资质介绍 | 成员简历、证书（须在有效期内）、同类经验 |
| `commercial` | 商务文件套装 | 投标函、授权书、报价单；与技术标承诺保持一致 |

## 写作铁律

- ❗ 案例需提供合同关键页或验收报告作为证明
- ❗ 资质文件须在有效期内（过期证书禁止引用）
- ❗ 每章完成后每日同步进度
- ❗ 所有内容必须与「最终技术要求清单.xlsx」+「技术偏离表」完全一致

## 配图调用

```
架构图    → 调用 plantuml / arch-diagram
流程图    → 调用 mermaid-chart
甘特图    → 调用 mermaid-chart（gantt 语法）
拓扑图    → 调用 arch-diagram
数据流图  → 调用 mermaid-chart 或 plantuml
```

## RAG 检索建议

```
写作前检索企业知识库：
- 历史标书（同行业 / 同类型）
- 企业资质证书（核查有效期）
- 业绩案例（含合同金额 / 规模 / 成果）
- 技术白皮书（最新版）
- 团队简历库（核查在职状态）

引用必须可追溯：
- 案例：标注合同号 / 验收报告页码
- 数据：标注来源文档 + 出版日期
- 资质：标注证书编号 + 有效期
```

## 输出物

- `bid-draft-[章节名].md` — 单章节草稿
- `bid-draft-full.md` — 全标书合并版

## 写作质量自检（每章完成后）

- [ ] 所有评分要点是否覆盖（看大纲权重标注）
- [ ] 字数是否在配比范围内
- [ ] 是否引用真实案例 / 数据（带来源标注）
- [ ] 是否与偏离表一致
- [ ] 配图是否清晰可读
