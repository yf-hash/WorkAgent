# WorkAgent 结构优化 AUDIT

> v2.7 二次裁剪已完成 A 阶段（删 4 skill + 1 agent + 清根仓库）。
> 本文件是 **B 阶段（合并同质化资产）** 和 **C 阶段（目录结构调整）** 的可执行 checklist。
> 每一步都独立可回退，建议按顺序执行，每完成一步先 `git commit` 再进入下一步。

**当前基线**：25 Agents / 127 Skills / 114 Commands / 13 Templates
**目标基线**：22 Agents / ~108 Skills / ~110 Commands / ~25 Templates

---

## B 阶段：合并同质化资产

### B1. 16 个 `product-*-writer` skill 合并（省 ~9 个）

**问题**：16 个 skill 各自 100-200 行，实际差异只在章节模板 30%，剩下 70% 是重复的"客户视角/量化/边界"逻辑。

**改造方案**：
1. 保留 4 个"多章节复合"型 skill：
   - `product-whitepaper-writer`（8-15 章白皮书）
   - `product-tech-whitepaper-writer`（技术架构侧重）
   - `product-solution-writer`（客户场景侧重）
   - `product-case-writer`（客户故事结构独特）
2. 其余 12 个改造为 **`templates/product/*.md`** 模板文件，由一个新的 `product-writer-router` skill + `/product` 命令统一路由
3. 保留 16 个 `commands/presales/product-*.md` 命令（用户熟悉），但底层实现改为读模板 + 复用 `product-whitepaper-writer` 的通用写作规范

**待删 12 个 skill**（能力迁移到 templates）：
- `product-brochure-writer` → `templates/product/brochure.md`
- `product-intro-business-writer` → `templates/product/intro-business.md`
- `product-intro-tech-writer` → `templates/product/intro-tech.md`
- `product-function-list-writer` → `templates/product/function-list.md`
- `product-sales-faq-writer` → `templates/product/sales-faq.md`
- `product-competitive-writer` → `templates/product/competitive.md`
- `product-bid-params-writer` → `templates/product/bid-params.md`
- `product-manual-writer` → `templates/product/manual.md`
- `product-deploy-writer` → `templates/product/deploy.md`
- `product-compat-writer` → `templates/product/compat.md`
- `product-release-note-writer` → `templates/product/release-note.md`
- `product-training-writer` → `templates/product/training.md`

**引用修复**（每个待删 skill 都要扫描引用）：
- `agents/product-enablement.md` skills 列表
- `agents/solution-architect.md` skills 列表
- `commands/presales/product-*.md` 加载指令
- `templates/sales-enablement-template.md`
- `README.md` §产品资料段落
- `HEALTH_REPORT.md` 相关表格

**验收标准**：`/product-brochure X 产品` 命令仍可用，输出质量不下降；skill 计数从 127 → 115。

---

### B2. 9 个 `pm-*` skill 精简（省 ~4 个）

**现状引用度**（v2.7 已删 pm-core-framework）：
- 高频：`pm-discovery-frameworks`(12)、`pm-prioritization-frameworks`(12)
- 中频：`pm-growth-aarrr`(8)、`pm-north-star`(6)、`pm-ai-era-evolution`(5)
- 低频：`pm-upward-management`(4)、`pm-qa-acceptance`(3)
- 大依赖：`pm-ai-security-product`（15+ 处依赖，保留不动）

**改造方案**：
1. **`pm-upward-management`** 内容并入 `pm-prioritization-frameworks`（都属于"决策与沟通"域）
2. **`pm-qa-acceptance`** 降级为 `templates/pm-qa-acceptance-template.md`，能力被 `@qa-acceptance-designer` agent 覆盖
3. **`pm-growth-aarrr`** 和 **`pm-north-star`** 内容合并入一个新 `pm-metrics-frameworks`（都是指标框架）
4. 保留：`pm-discovery-frameworks` / `pm-prioritization-frameworks` / `pm-metrics-frameworks`（新）/ `pm-ai-era-evolution` / `pm-ai-security-product`

**待删 4 个 skill**：`pm-upward-management` / `pm-qa-acceptance` / `pm-growth-aarrr` / `pm-north-star`
**新增 1 个 skill**：`pm-metrics-frameworks`

**引用修复**：
- `agents/product-manager.md` / `product-director.md` / `growth-strategist.md` 的 skills 列表
- `commands/product/pm-review.md` / `pm-discovery.md` 中的加载指令
- `templates/pm-discovery-template.md` 中的配套 Skill 说明

**验收标准**：skill 计数 115 → 112；PM 方法论仍完整可用。

---

### B3. `market-intelligence` agent 降级

**问题**：与 `research-analyst` 职责重叠 80%（都是市场研究），只是侧重竞品/TAM。

**改造方案**：
1. `market-intelligence` agent 删除
2. 能力吸收进 `research-analyst`，在其 description 补一句"含市场情报 / 竞品矩阵 / TAM / OSS 生态"
3. `commands/product/market-research.md` 保留，改为直接触发 `research-analyst`

**引用修复**：所有 `@market-intelligence` 改为 `@research-analyst --focus market`

**验收标准**：agent 计数 25 → 24；市场研究能力不下降。

---

### B4. `proposal-writer` agent 是否合并（**决策点**）

**分析**：
- 优点：与 `solution-architect` + `proposal-generator` skill 有 60% 重叠
- 缺点：被 5 处引用（`solution-architect` / `product-director` / `product-enablement` / `templates/sales-enablement-template` / `commands/presales/proposal.md`），且它承担"多轮问答 + 完整方案生成"的独立编排逻辑

**建议**：**保留**。删除代价大于收益。若一定要合并，改造成 `solution-architect` 的一个 phase（不推荐）。

---

## C 阶段：目录结构调整

### C1. `skills/` 分子目录（改动最大，需慎重）

**现状**：131 个 skill 全平铺在 `skills/`，检索困难。

**改造方案**：按 command 分类映射，把 skills 分入子目录：

```
skills/
├── writing/           # article-writer, hv-analysis, interview-writer, marketing-copy, humanizer-*, style-*
├── prd/               # prd-* 11 个
├── pm/                # pm-* 剩余 5 个 + product-strategy / working-backwards 等
├── product/           # 16 个 product-*-writer（若 B1 未做）或 4 个（若 B1 已做）
├── presales/          # discovery-call, gap-analysis, solution-architecture, business-case, rfp-response, security-questionnaire, battle-card, demo-design, poc-plan, sales-guide-writer, doc-auditor, proposal-generator
├── bid/               # bid-* 7 个
├── dashboard/         # dashboard-* 7 个
├── ppt/               # ppt-*, academic-pptx, slidetailor, slidev, marp
├── media/             # remotion-*, pdf2video, omni-captions, videocut, content-sync
├── diagram/           # arch-diagram, diagram-*, mermaid-chart, visio-builder, html-chart, ai-illustrator, stable-diffusion, impeccable, md-poster, md-table-image
├── research/          # market-research, user-research, paper-*, taskweaver, chat2db, open-websearch, hv-analysis
├── data/              # product-analytics, ab-test
└── strategy/          # gtm-strategy, build-vs-buy, sunset-plan, win-loss-analysis, churn-analysis, tech-debt, ai-red-team, mvp-canvas, user-story-mapping, launch-checklist, pmf-survey, pricing-strategy, compliance-checklist, product-report, product-roadmap, design-proto, user-feedback, table-*
```

**影响面**：
- 所有 agent 的 `skills:` 列表需要更新为新路径（若使用相对路径 `skills/xxx` 需要改成 `skills/domain/xxx`）
- 所有 command `加载技能：skills/xxx/SKILL.md` 需要更新
- 所有 skill 之间的 `[[link]]` 需要检查

**验收标准**：`grep -r "skills/" agents/ commands/ | grep -v "skills/[a-z]*/[a-z]"` 结果为空（都指向新子目录）。

**风险**：改动量估计 200+ 处引用。建议单独用一个分支执行，先做迁移脚本再手工核验。

---

### C2. `agents/` 分层索引

**现状**：25 个 agent 平铺，用户难以选择。

**改造方案**：不动文件，只在 `agents/README.md` 加索引：

```markdown
# Agents 索引

## 战略层（策略/决策）
- product-director, solution-architect, gtm-strategist, growth-strategist

## 领域专家（有独立方法论）
- prd-coach, xqy-spec-writer, qa-acceptance-designer, ai-product-architect
- research-analyst, paper-researcher, web-search-analyst
- content-director, style-evolver, doc-polisher
- impeccable-designer, diagram-architect, article-illustrator

## 全栈执行（编排大量命令）
- product-manager, product-enablement, proposal-writer, bid-writer
- ppt-generator, video-maker, data-analyst
```

**影响面**：仅新增 1 个 `agents/README.md`，无破坏性变更。

---

### C3. 根仓库 templates/ 扩容（配合 B1）

若执行 B1，需要新增 `templates/product/` 子目录 + 12 个模板文件。

模板文件的结构应包含：
- 章节大纲（H2/H3）
- 每章节的写作要点（bullet）
- 客户视角检查表
- 量化数字要求
- 示例段落（可选）

---

### C4. `commands/product/` 拆分

**现状**：47 个命令，最大的一个目录，分类杂。

**改造方案**：拆成两个子目录：
- `commands/product/` 保留 PRD + 产品方法（prd-* 11 + pm-* 5 + 战略决策 15）
- `commands/dashboard/` 单独出 7 个 dashboard-* 命令

**验收标准**：`commands/product/` 从 47 → 40，新增 `commands/dashboard/` 7 个。

---

## 执行顺序建议

**Sprint 1（低风险，1-2 小时）**：
- B3（market-intelligence 降级）
- C2（agents/README.md 索引）
- C4（commands 拆分 dashboard 子目录）

**Sprint 2（中风险，半天）**：
- B2（pm-* 合并 4 → 3）
- 期间同步修改所有引用

**Sprint 3（高风险，需一整天）**：
- B1（product-*-writer 16 → 4 + 12 模板）
- 需要在独立分支执行，全量 CI 验证

**Sprint 4（结构性，需一整天）**：
- C1（skills 分子目录）
- 建议先写迁移脚本，再手工核验 100+ 引用

---

## 完成后目标态

```
WorkAgent/
├── agents/                    # 22 个（-3：删 visual-suite / market-intelligence / proposal-writer 可选）
│   └── README.md              # 分层索引
├── skills/                    # ~108 个（分子目录）
│   ├── writing/  prd/  pm/  product/
│   ├── presales/  bid/
│   ├── dashboard/  ppt/  media/  diagram/
│   ├── research/  data/  strategy/
├── commands/                  # ~110 个
│   ├── writing/  product/  dashboard/  presales/
│   ├── research/  media/
├── templates/                 # ~25 个（product/ 子目录扩容）
│   └── product/
├── AUDIT.md（本文件）
├── HEALTH_REPORT.md
└── README.md
```

---

## 未做事项与理由

以下几个 explore 代理提议的裁剪已经 **主动撤回**：

| 提议 | 撤回理由 |
|---|---|
| 删 `content-sync` | v2.6 HEALTH_REPORT §五 明确保留为 driver/adapter 模式 |
| 删 `sunset-plan` | `/sunset` 命令直接加载它，无法拆离 |
| 删 `chat2db` | `@data-analyst` agent 依赖它作为 SQL backend |
| 删 `pm-ai-security-product` | 15+ 处依赖，含 templates 和多 agent，删除代价过大 |
| 删 `ppt-architect` | `@ppt-generator` 的核心调度层，多处引用 |
| 参数化 `humanize-*/style-*/diagram-*` 回 --mode | 与 v2.6 拆原子命令的方向相反，会破坏用户习惯 |
| 拆 `product-manager` agent | 主管全栈是它的价值所在，拆分会破坏"一站式" |
| 合 `prd-*` 11 个 | 每个适用场景清晰，合并会牺牲精度 |
