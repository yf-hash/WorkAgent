# WorkAgent 健康度报告

> 更新于 2026-07-10（v2.7 — 二次裁剪 + 文档漂移修正）
> 范围：`agents/`、`skills/`、`commands/**/`、`templates/`

---

## TL;DR

✅ **零孤立 / 零断链**：所有 Skill 至少被 1 个命令或 Agent 引用，所有引用都指向存在的资产
✅ **严格单一职责**：每个 Skill 只完成一个任务，不再有"4 种模式"、"6 轮流程"等多任务合并
✅ **本轮修复（v2.7）**：删除 4 个低价值 Skill + 1 个能力被覆盖的 Agent + 补录 v2.6 遗漏的 2 个 Agent + 清理根仓库无关文件
✅ **待办**：product-\*-writer 合并、pm-\* 合并、skills 分子目录等结构性优化见 `AUDIT.md`

---

## 一、当前指标

| 类别 | 数量 | 较 v2.6.1 变化 |
|------|------|--------------|
| Agents | 25 | -1（删 `visual-suite`）+2 补录（`web-search-analyst` / `xqy-spec-writer`），净 +1 |
| Skills | 127 | -4（删 `pm-core-framework` / `doc-formatter` / `bid-rewriter` / `pptx-sdk`）+2 补录（`open-websearch` / `prd-xqy`），净 -2 |
| Commands | 114 | +2 补录（`web-search` / `prd-xqy`） |
| Templates | 13 | 持平 |

**命令分布**：

- `commands/product/`：47（含 prd-* 11 个、dashboard-* 7 个、pm-* 5 个、战略决策 + 通用产品方法）
- `commands/presales/`：35（含 bid-* 七阶段、product-* 16 类原子文档、售前 8 类工件）
- `commands/writing/`：11（含 style-* 3 个、humanize-* 3 个）
- `commands/research/`：5（新增 `/web-search`）
- `commands/media/`：16（含 remotion-* 3 个、diagram-* 2 个、md-* 2 个、table-* 2 个）

---

## 二、v2.7 修复明细（本轮）

### A. 裁剪清单

| 类型 | 名称 | 删除原因 | 迁移到 |
|---|---|---|---|
| skill | `pm-core-framework` | 仅 1 处引用（`product-director`），v2.6.1 已改写为"前置思考层"仍是名存实亡 | product-director skills 列表移除；PM 方法论直接引用原子 pm-* Skill |
| skill | `doc-formatter` | 仅 2 处引用，`humanizer-scan/soul` 已覆盖排版 | doc-polisher skills 列表移除 |
| skill | `bid-rewriter` | v2.6 已声明"内嵌于 bid-write" | bid-writer agent skills 列表和路由描述移除 |
| skill | `pptx-sdk` | skill 自身已声明降级，能力已迁移到 `skills/ppt-master/references/pptx-sdk.md` | ppt-generator agent 路由指向 ppt-master |
| agent | `visual-suite` | 能力被 `@diagram-architect`（图表路由）+ `@article-illustrator`（文章配图）+ `/md-poster` / `/md-table-image` 完全覆盖 | article-illustrator 边界说明更新为 `@diagram-architect` |

### B. 补录（v2.6 遗漏）

| 类型 | 名称 | 说明 |
|---|---|---|
| agent | `web-search-analyst` | 多引擎联网研究分析师，v2.6.x 已存在但未列入 README |
| agent | `xqy-spec-writer` | 银行/金融 XQY 需求规格说明书写作 Agent，v2.6.x 已存在但未列入 README |
| skill | `open-websearch` | `web-search-analyst` 的底层引擎 |
| skill | `prd-xqy` | XQY 8 章模板方法论 |
| command | `/web-search` | 触发 web-search-analyst |
| command | `/prd-xqy` | 触发 xqy-spec-writer |

### C. 根仓库清理

- 删除 5 个漏洞挖掘遗留 Python 脚本（`gen_vuln_diff_report.py` / `generate_ai_security_report.py` / `generate_expert_report.py` / `generate_qa_report.py` / `generate_report.py`），与 WorkAgent 项目无关

### D. 引用修复

| 文件 | 原引用 | 处理 |
|---|---|---|
| `agents/doc-polisher.md` | skills 列表含 `doc-formatter` | 移除 |
| `agents/product-director.md` | skills 列表含 `pm-core-framework` | 移除 |
| `agents/bid-writer.md` | skills 列表含 `bid-rewriter` + "rewrite → 调用 bid-rewriter skill" 路由 | 移除 |
| `agents/ppt-generator.md` | skills 列表含 `pptx-sdk` + description 提"6 种引擎" + 路由指向 pptx-sdk | 移除，改为"5 种引擎+ ppt-master 内嵌 SDK" |
| `agents/article-illustrator.md` | description + 边界说明引用 `visual-suite` | 改为 `@diagram-architect` |
| `skills/ppt-master/references/pptx-sdk.md` | 说明"原独立技能路径" | 改为"原独立 skill 已删除，能力完全内嵌" |
| `README.md` | 数量表 / agent 表 / skill 表 / 更新日志 | 全量刷新 |

---

## 二·附：v2.6.1 修复历史（2026-06）

### A. 断链修复（25+ 处）

按文件分组列出本轮已修复的对已删除资产的引用：

| 文件 | 原断链 | 替换为 |
|---|---|---|
| `skills/churn-analysis/SKILL.md` | `/data-dashboard --mode customer-health`, `/data-dashboard`, `/user-research --mode interview` | `/dashboard-customer-br`, `/dashboard-revenue`, `/user-research` |
| `skills/omni-captions/SKILL.md` | `remotion-generator`, `/remotion-generate` | `Remotion 系列命令`, `/remotion-native` |
| `skills/pm-core-framework/SKILL.md` | `pm-skills`, `pm-full-cycle`, `/prd-writer`, `/product-spec`, `/sales-guide` 等 7 处 | 重写定位为「前置思考层」+ 链接到 6 个原子 PM 框架 Skill |
| `skills/pm-qa-acceptance/SKILL.md` | `product-spec / prd-writer` | `prd-standard / prd-implementation-draft` |
| `skills/working-backwards/SKILL.md` | `/product-spec` × 2 | `/prd-standard` |
| `skills/user-story-mapping/SKILL.md` | `product-spec` | `prd-standard` |
| `skills/product-strategy/SKILL.md` | `product-spec` | `prd-standard` |
| `skills/compliance-checklist/SKILL.md` | `product-spec` | `prd-standard` |
| `skills/product-sales-faq-writer/SKILL.md` | `/sales-guide` | `sales-guide-writer / /sales-guide` |
| `skills/arch-diagram/SKILL.md` | `diagram-suite` | `mermaid-chart / diagram-plantuml` |
| `skills/visio-builder/SKILL.md` | `diagram-suite` | `diagram-plantuml / arch-diagram` |
| `skills/solution-architecture/SKILL.md` | `diagram-suite` | `mermaid-chart / diagram-plantuml` |
| `skills/impeccable/SKILL.md` | `humanizer skill` | `humanizer-scan / humanizer-soul` |
| `skills/doc-formatter/SKILL.md` | `humanizer` | `humanizer-scan / humanizer-soul` |
| `agents/bid-writer.md` | `/bid <子命令>` | `/bid-analyze / /bid-clarify / ... / /bid-export` |
| `agents/visual-suite.md` | `document-illustrator`, `thesis-figure-skill`, `paper-banana`（不存在的 skill）+ `/mermaid`（不存在的命令） | 改写为 `ai-illustrator` 内部子流程 + `/diagram-uml` |
| `commands/media/caption.md` | `/remotion-generate` | `/remotion-native / /remotion-prompt2video / /remotion-vidosy` |
| `commands/media/videocut.md` | `/remotion-generate` | 同上 |
| `commands/media/pdf2video.md` | `/remotion-generate` | 同上 |
| `commands/media/arch-diagram.md` | `/diagram`, `/prd` | `/diagram-mindmap / /diagram-uml`, `/prd-standard` |
| `commands/media/visio.md` | `/diagram` | `/diagram-uml` |
| `commands/media/ppt.md` | `/diagram`, `/prd` | `/diagram-uml / /diagram-mindmap`, `/prd-standard` |
| `commands/presales/proposal.md` | `/bid` + 失效路径 `commands/writing/bid.md` | `/bid-* 七阶段` |
| `commands/presales/rfp-response.md` | `/bid full` | `/bid-analyze → /bid-export 七阶段` |
| `commands/presales/security-questionnaire.md` | `/bid full` | 同上 |
| `commands/writing/sync.md` | `/humanize` | `/humanize-scan → /humanize-soul` |
| `commands/product/impeccable.md` | `/humanize` | `/humanize-scan → /humanize-soul` |
| `commands/product/pm-discovery.md` | `competitor-analysis`（不存在的 skill 名） | `market-research`（含 `--mode competitive`） |
| `commands/product/gtm-strategy.md` | `/prd --mode gtm` | `/prd-standard` |
| `templates/prd-template.md` | 配套 Skill: `prd-writer`，配套命令: `/prd-writer` | 配套 Agent: `@prd-coach`，配套命令: `/prd-diagnose → /prd-concept → /prd-impl` 或 `/prd-standard` |

### B. 冗余 Agent 清理

- **删除 `agents/writer-reviewer.md`**（188 行）— 已被 `skills/style-writer-reviewer/SKILL.md`（139 行）完全覆盖。该 Agent 与 Skill 的 Writer-Reviewer 互搏流程一致，无独立编排价值，删除后由 `@content-director` 和 `@style-evolver` 直接调用 Skill。

### C. 单一职责（SR）违规描述修正

| Skill | 原 description 违规点 | 修正 |
|---|---|---|
| `proposal-generator` | "支持三大方案类型：售前解决方案 / 可行性研究报告 / 初步设计方案" | 改述为 `/proposal` 命令通过 `--type` 路由的章节模板库，加上「不做：产品级标准资料 / 招投标全流程 / 纯架构 Blueprint」边界 |
| `ai-illustrator` | "支持文章自动配图、学术论文图表、文档专业插图、创意画布四大场景" | 改述为按场景路由到 article-illustrator / thesis-figure / document-illustrator 子流程，加上「不做：结构化图表 / SD 文生图 / Markdown 海报」边界 |
| `bid-write` | "支持交互模式/批量模式/RAG 增强/配图生成" | 改述为「核心职责始终是按大纲写章节」，调用标志只是控制选项；加上拆解 / 大纲 / 评审 / 核查 / 导出的流转边界 |

---

## 三、v2.6 单一职责重构回顾

> 以下为 v2.6 既有拆分清单，本轮（v2.6.1）未变化。

### A. 必拆类（明确多任务 / 多模式合并）

| 原 Skill | 拆分为 |
|---|---|
| `product-spec` | `prd-lite` / `prd-standard` / `prd-spec-first` / `prd-proto` / `prd-quality-check` |
| `prd-writer` | `prd-diagnose` / `prd-concept-draft` / `prd-implementation-draft` / `prd-incremental-update` / `prd-deep-evaluate` |
| `ppt-source` | `ppt-rag-indexer` / `ppt-web-researcher` |
| `style-evolver` | `style-card-extractor` / `style-writer-reviewer` / `style-refine` |
| `remotion-generator` | `remotion-native` / `remotion-prompt2video` / `remotion-vidosy` |
| `pm-skills` | `pm-discovery-frameworks` / `pm-prioritization-frameworks` / `pm-growth-aarrr` / `pm-north-star` / `pm-upward-management` / `pm-ai-era-evolution` |
| `pm-full-cycle` | 删除 → 改由 `@product-manager` Agent 编排原子命令 |
| `diagram-suite` | `diagram-markmap` / `diagram-plantuml`（`mermaid-chart` 保留独立）|
| `md-visual` | `md-poster` / `md-table-image` |
| `table-toolkit` | `table-from-text` / `table-csv-md` |
| `humanizer` | `humanizer-scan` / `humanizer-soul` / `humanizer-academic` |
| `data-dashboard` | `dashboard-northstar` / `dashboard-aarrr` / `dashboard-cohort` / `dashboard-revenue` / `dashboard-customer-br` / `dashboard-ai-monitor` / `dashboard-platform-selector` |
| `bid-writer` | `bid-analyze` / `bid-clarify` / `bid-outline` / `bid-write` / `bid-review` / `bid-check` / `bid-export` |

### B. 保持不变的"看起来像聚合实则单一职责"Skill

| Skill | 为何不拆 |
|---|---|
| `mermaid-chart` | 同一种语法的多种图表类型，单一任务"生成 Mermaid 代码" |
| `content-sync` | 同一任务"发布到平台"的不同 driver/adapter，类似数据库驱动 |
| `md-poster` / `md-table-image` / `table-csv-md` | "整合 N 个工具"指 driver/adapter，不是多任务 |

---

## 四、命令拆分（v2.6 既有）

| 原命令 | 拆分为 |
|---|---|
| `/product-spec --mode {prd, spec, proto, lite}` | `/prd-standard` `/prd-spec-first` `/prd-proto` `/prd-lite` |
| `/prd-writer` | `/prd-diagnose` `/prd-concept` `/prd-impl` `/prd-update` `/prd-quality` `/prd-deep-evaluate` |
| `/self-evolve` | `/style-extract` `/style-create` `/style-refine` |
| `/humanize` | v2.6 拆分：`/humanize-scan` `/humanize-soul` `/humanize-academic` → v2.8 重新合并入口：`/humanize --mode scan\|soul\|academic\|all`（skills 保留） |
| `/remotion-generate` | v2.6 拆分：`/remotion-native` `/remotion-prompt2video` `/remotion-vidosy` → v2.8 重新合并入口：`/video-gen --engine <name>`（skills 保留） |
| `/diagram` | v2.6 拆分：`/diagram-mindmap` `/diagram-uml` → v2.8 重新合并入口：`/diagram --type mindmap\|uml\|json`（skills 保留，mermaid/arch/visio 保持独立命令） |
| `/md-visual` | v2.6 拆分：`/md-poster` `/md-table-image` → v2.8 重新合并入口：`/md-render --format poster\|table`（skills 保留） |
| `/table` | `/table-from-text` `/table-csv` |
| `/data-dashboard` | v2.6 拆分：`/dashboard-northstar` 等 7 个 → v2.8 重新合并入口：`/dashboard --metric <name>`（skills 保留） |
| `/bid` | v2.6 拆分：`/bid-analyze` `/bid-clarify` `/bid-outline` `/bid-write` `/bid-review` `/bid-check` `/bid-export` → v2.8 恢复统一入口：`/bid --phase <name>`（skills 保留） |
| `/product-doc` | `/product-whitepaper` 等 16 个原子命令 |

---

## 五、单一职责验证标准

每个 Skill 的 description 必须满足：

```
✅ 一句话能讲清"这个 Skill 做什么"
✅ 不出现"支持 N 种模式"、"M 轮流程"、"合并自 X+Y"等暗示多任务的措辞
✅ 在文档中明确写出"不做什么 → 流转到哪个 Skill / 命令"
✅ 一次调用消耗的上下文 ≤ 单一任务所需，不会拉满
```

> **例外**：driver/adapter 模式 Skill（`mermaid-chart` / `content-sync` / `md-poster` / `table-csv-md`）允许在 description 中列出底层引擎，但核心职责必须是单一任务。

---

## 六、当前文件结构

```
WorkAgent/
├── agents/             # 24
├── skills/             # 129（严格单一职责）
├── commands/
│   ├── writing/        # 11（含 style-*/humanize-* 拆分）
│   ├── product/        # 46（含 prd-*/dashboard-*/pm-* 拆分）
│   ├── presales/       # 35（含 bid-* 七阶段 + product-* 16 类）
│   ├── research/       # 4
│   └── media/          # 16（含 remotion-*/diagram-*/md-*/table-* 拆分）
├── templates/          # 13
├── HEALTH_REPORT.md（本文件）
└── README.md
```

---

## 七、易混命令边界

### PRD 系列（10 个命令）

| 场景 | 命令 |
|---|---|
| 1 页对齐方向 | `/prd-lite` |
| 标准 8 章 PRD | `/prd-standard` |
| Spec-First 四件套 | `/prd-spec-first` |
| 含 ASCII 线框图 | `/prd-proto` |
| B 端严格 12 章 | `/pm-prd-enterprise` |
| 通用 5 维度评分 | `/prd-quality` |
| 23 节模板差距分析 | `/prd-deep-evaluate` |
| 对话式渐进生成（想法模糊）| `/prd-diagnose` → `/prd-concept` → `/prd-impl` |
| 已有 PRD 增量变更 | `/prd-update` |

### Style / Humanizer 系列

| 场景 | 命令 |
|---|---|
| 提炼风格卡片 | `/style-extract` |
| 风格驱动从零创作 | `/style-create` |
| 已有文章风格优化 | `/style-refine` |
| AI 痕迹扫描去除 | `/humanize --mode scan` |
| 灵魂注入 | `/humanize --mode soul` |
| 学术深度强化 | `/humanize --mode academic` |

### Dashboard 系列

> v2.8 起命令入口统一为 `/dashboard --metric <name>`。Skills 层拆分保留。

| 看板类型 | 命令 |
|---|---|
| 北极星 | `/dashboard --metric northstar` |
| AARRR 漏斗 | `/dashboard --metric aarrr` |
| Cohort 留存 | `/dashboard --metric cohort` |
| 收入（MRR/ARR/NRR）| `/dashboard --metric revenue` |
| 客户 BR / QBR | `/dashboard --metric customer-br` |
| AI 功能监控 | `/dashboard --metric ai-monitor` |
| 平台选型决策 | `/dashboard --metric platform-selector` |

### Bid 系列（七阶段串行）

> v2.8 起命令入口统一为 `/bid --phase <name>`。Skills 层 7 阶段拆分保留。

```
/bid --phase analyze → clarify → outline → write → review → check → export
# 或一键：
/bid RFP.pdf --phase all
```

### Diagram 系列

| 引擎 | 命令 |
|---|---|
| Mermaid（流程/甘特/状态/ER 等）| `/illustrate --backend mermaid` |
| PlantUML（全系 UML）| `/diagram --type uml` |
| Markmap（思维导图）| `/diagram --type mindmap` |
| 云架构图（diagrams 库）| `/arch-diagram` |
| Visio 创建 / 格式互转 | `/visio` |

---

## 八、合规与质量基线

所有 Skill / Agent / Command 须遵守：

1. **单一职责**：一个 Skill 只做一件事（v2.6 起核心）
2. **Frontmatter 规范**：name / description / 关键字段齐全
3. **写作四层自检**：活人感 / 情感 / 信息 / 结构
4. **量化驱动**：商业输出（Business Case / RFP / Demo）数字可查证
5. **客户视角**：售前文档不用我方产品行话，用客户行业术语
6. **诚实承诺**：做不到的明说 + 替代方案 + 时间表

---

## 九、本轮验证结果

- ✅ 检查所有 `commands/` 和 `agents/` 中对 `skills/*` 的路径引用：**零断链**
- ✅ 检查所有 agent frontmatter 中 `skills:` 列表：**零无效引用**
- ✅ 修复 v2.6 后残留的 25+ 处对已删命令 / Skill / Agent 的纯文本引用
- ✅ 删除被 Skill 完全覆盖的冗余 `@writer-reviewer` Agent
- ✅ 3 处 SR 违规描述已修正（`proposal-generator` / `ai-illustrator` / `bid-write`）

---

## 十、可选的进一步优化

1. **README 中保留的 `--mode` 示例审计**：当前 README 已尽量改用原子命令，但部分命令（如 `/discovery-call --mode prep`、`/ab-test --mode design`）的 `--mode` 是命令内部行为开关而非 v2.6 路由 flag，保留合理。如未来全部改为 flag-free 调用，需再次扫描清理。
2. **Agent 维度的拆分**：`@product-manager` 现在的 `skills:` 列表已含 40+ 项，未来可按子领域拆为 PRD 专精 / 增长专精 / B 端专精等轻量版。
3. **PPT Agent 的引擎归并**：`@ppt-generator` skills 列表也较长，可考虑引入"引擎注册中心" Skill 减少直接引用。
4. **跨域同名 Skill**：`pm-ai-security-product` 和新增的 `pm-ai-era-evolution` 与 `@ai-product-architect` 三者职责需要持续观察，必要时合并或进一步细化边界。
5. **重型 Agent 减肥**：`@ppt-generator`（693 行）、`@bid-writer`（323 行）等 Agent 内嵌大量本应在 Skill 中的伪代码/模板，可在下一轮重构中迁移至对应 Skill，让 Agent 退化为纯路由层。
