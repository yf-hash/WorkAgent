# WorkAgent 收敛方案（v2.8）

> 本方案配套 AUDIT.md 的 B/C 阶段，聚焦「commands 按主题合并 + skills 分子目录」两个方向。
> **状态**：草案，待用户 review 后执行。
> **产出目标**：114 commands → ~78 commands / 115 skills → 分 13 子目录 / 25 agents → 24 agents。

---

## 1. Context — 为什么做

### 1.1 现状
- **B1/B2/B3 已完成**（commit `12ea3c9` / `d8d7312` / `07bbc13`）
- 但 command 层还有 **37 个 <30 行的 stub**——绝大多数只是「加载 skill」的一层壳
- Skills 全平铺 115 个在 `skills/` 根目录，检索靠肉眼扫
- 1 个死代码 agent：`impeccable-manual-edit-applier`（status: draft，无调用路径）

### 1.2 用户诉求（本轮确认）
1. Commands 按主题合并成 **~6 个主命令**（推荐档）
2. Skills 按 **C1 拆子目录**（中度）
3. **先出方案文件让用户 review**（本文件）

---

## 2. ⚠️ 与 AUDIT.md 已有决策的冲突

AUDIT.md 第 236-249 行「未做事项与理由」中，明确 **主动撤回** 过以下方向：

| 撤回项 | AUDIT 理由 | 本方案是否触碰 |
|---|---|---|
| 参数化 `humanize-*` 回 `--mode` | 与 v2.6 拆原子命令方向相反，会破坏用户习惯 | ⚠️ **Phase 1-B 会做** |
| 参数化 `style-*` 回 `--mode` | 同上 | ✅ 本方案不动 |
| 参数化 `diagram-*` 回 `--type` | 同上 | ⚠️ **Phase 1-B 会做** |
| 合并 `prd-*` 11 个 | 每个适用场景清晰，合并会牺牲精度 | ✅ 本方案不动（保留 11 个 PRD 命令） |

**执行本方案 = 覆盖 AUDIT.md 上述条目**。若用户同意，方案落地时会同步更新 AUDIT.md「未做事项」章节。

### 冲突分级

- **Phase 1-A（无冲突）**：dashboard / bid / md-render / video-gen —— stub 群合并，AUDIT 未反对
- **Phase 1-B（有冲突）**：humanize / diagram —— 与 AUDIT 撤回项直接冲突
- **Phase 2/3（无冲突）**：Skills 分子目录 = AUDIT C1；Agents 索引 = AUDIT C2

---

## 3. Phase 1 — Commands 合并（114 → ~78）

### Phase 1-A：无 AUDIT 冲突的合并（省 21 个命令）

#### 1-A-1 Dashboard 群 7 → 1
**合并前**（`commands/product/`）：
```
dashboard-northstar.md      (11L)
dashboard-aarrr.md          (10L)
dashboard-cohort.md         (10L)
dashboard-revenue.md        (10L)
dashboard-customer-br.md    (11L)
dashboard-ai-monitor.md     (10L)
dashboard-platform-selector.md (10L)
```
**合并后**：`commands/product/dashboard.md`，用 `--metric northstar|aarrr|cohort|revenue|customer-br|ai-monitor` 分派。
- Skills 层 `skills/dashboard-*/` **不动**（能力保留，只收命令入口）
- 保留 `platform-selector` 作为 `--platform` 前置步骤

#### 1-A-2 Bid 群 7 → 1
**合并前**（`commands/presales/`）：
```
bid-analyze.md    (23L, Phase 1 拆解)
bid-clarify.md    (15L, Phase 2 澄清)
bid-outline.md    (11L, Phase 3 大纲)
bid-write.md      (18L, Phase 4 写作)
bid-review.md     (11L, Phase 5 评审)
bid-check.md      (11L, Phase 6 核查)
bid-export.md     (11L, Phase 7 移交)
```
**合并后**：`commands/presales/bid.md`，用 `--phase 1..7` 或 `--phase all` 一键跑完。
- 每个 bid-analyze.md 里已经写着「Phase 1 → 2 → 3 → ... → 7」，本来就是线性流程，合并零违和
- Skills `skills/bid-*/` **不动**
- `@bid-writer` agent 内部编排逻辑不变，只是外部入口收敛

#### 1-A-3 Md-render 群 2 → 1
```
md-poster.md      (23L) + md-table-image.md (17L) → md-render.md --format poster|table
```

#### 1-A-4 Video-gen 群 3 → 1
```
remotion-native.md + prompt2video.md + vidosy.md → video-gen.md --engine <name>
```

**Phase 1-A 小计**：删 19 个命令、新增 4 个命令，净减 **15 个**。

---

### Phase 1-B：与 AUDIT.md 冲突的合并（省 6 个命令，⚠️ 需覆盖 AUDIT）

#### 1-B-1 Humanize 群 3 → 1 ⚠️
```
humanize-scan.md (24L) + humanize-soul.md (23L) + humanize-academic.md (25L)
  → humanize.md --mode scan|soul|academic （或组合 --mode all）
```
**与 AUDIT 冲突**：AUDIT 247 明确「与 v2.6 拆原子命令方向相反」。

#### 1-B-2 Diagram 群 (≥4) → 1 ⚠️
```
diagram-mindmap.md (17L) + diagram-uml.md (27L) + 其他 diagram-* → diagram.md --type mindmap|uml|...
```
**同上冲突**。

**Phase 1-B 小计**：净减 **6 个**。

---

### Phase 1 汇总

| 分类 | 合并前 | 合并后 | 净减 | 冲突 |
|---|---|---|---|---|
| dashboard | 7 | 1 | -6 | 无 |
| bid | 7 | 1 | -6 | 无 |
| md-render | 2 | 1 | -1 | 无 |
| video-gen | 3 | 1 | -2 | 无 |
| humanize | 3 | 1 | -2 | ⚠️ 有 |
| diagram | ≥4 | 1 | -3 | ⚠️ 有 |
| **合计** | **26+** | **6** | **-20** | — |

**其余 88 个 command 保留原状**（PRD 11 个、pm-* 5 个、style-* 系列、product-* 16 个、以及 mega 命令 ppt.md/illustrate.md 等），因为：
- PRD 11 个 → AUDIT 明确保留
- style-* → AUDIT 撤回过合并
- product-* 16 个 → B1 已经完成配套模板化，命令层刻意保留
- ppt.md / illustrate.md → 已经是聚合命令

---

## 4. Phase 2 — Skills 子目录拆分（C1）

按 AUDIT C1 的映射，把 `skills/` 下 115 个平铺目录分入 13 个子域：

```
skills/
├── writing/     article-writer, humanizer-scan/soul/academic, style-card-extractor,
│                style-writer-reviewer, style-refine, marketing-copy, interview-writer,
│                hv-analysis
├── prd/         prd-lite, prd-standard, prd-spec-first, prd-proto, prd-quality-check,
│                prd-deep-evaluate, prd-diagnose, prd-concept-draft, prd-implementation-draft,
│                prd-incremental, prd-xqy
├── pm/          pm-discovery-frameworks, pm-prioritization-frameworks, pm-metrics-frameworks,
│                pm-ai-era-evolution, pm-ai-security-product, working-backwards, product-strategy
├── product/     product-whitepaper-writer, product-tech-whitepaper-writer,
│                product-solution-writer, product-case-writer
├── presales/    discovery-call, gap-analysis, solution-architecture, business-case,
│                rfp-response, security-questionnaire, battle-card, demo-design, poc-plan,
│                sales-guide-writer, doc-auditor, proposal-generator
├── bid/         bid-analyze, bid-clarify, bid-outline, bid-write, bid-review,
│                bid-check, bid-export
├── dashboard/   dashboard-northstar, dashboard-aarrr, dashboard-cohort, dashboard-revenue,
│                dashboard-customer-br, dashboard-ai-monitor, dashboard-platform-selector
├── ppt/         ppt-rag-indexer, ppt-architect, academic-pptx, slidetailor, slidev, marp
├── media/       remotion-native, prompt2video, vidosy, pdf2video, omni-captions,
│                videocut, content-sync, md-poster, md-table-image
├── diagram/     arch-diagram, diagram-markmap, diagram-plantuml, mermaid-chart,
│                visio-builder, html-chart, ai-illustrator, stable-diffusion, impeccable
├── research/    market-research, user-research, paper-collector, paper-interpreter,
│                taskweaver, chat2db, open-websearch
├── data/        product-analytics, ab-test
└── strategy/    gtm-strategy, build-vs-buy, sunset-plan, win-loss-analysis, churn-analysis,
                 tech-debt, ai-red-team, mvp-canvas, user-story-mapping, launch-checklist,
                 pmf-survey, pricing-strategy, compliance-checklist, product-report,
                 product-roadmap, design-proto, user-feedback, table-*
```

### 引用修复面
- **所有 agents/*.md** 的 skills 列表（25 个文件）
- **所有 commands/**/*.md** 的「加载技能：skills/xxx/SKILL.md」（估算 100+ 处）
- **skills 之间的相互引用**（estimated 50+ 处）

### 执行方式
1. 写 PowerShell 迁移脚本：先复制到新目录，再全仓 grep-replace 引用
2. 迁移完后跑 `grep -r "skills/" agents/ commands/` 校验，若仍有 `skills/<name>` 未加子域前缀则报错
3. 独立分支执行，最后一并 merge

### 验收
- `grep -r "skills/" agents/ commands/ | grep -vE "skills/(writing|prd|pm|product|presales|bid|dashboard|ppt|media|diagram|research|data|strategy)/"` 结果为空

---

## 5. Phase 3 — Agents 收敛（25 → 24）

### 3.1 删除死代码
- **删除** `agents/impeccable-manual-edit-applier.md`（status: draft，无 command 调用路径，依赖不存在的 live-browser 脚本）
- 检查引用：`grep -r "impeccable-manual-edit-applier" .` 应仅命中自身

### 3.2 新增 agents/README.md（AUDIT C2）
分层索引：
- **战略层**：product-director, solution-architect, gtm-strategist, growth-strategist
- **领域专家**：prd-coach, xqy-spec-writer, qa-acceptance-designer, ai-product-architect, research-analyst, paper-researcher, web-search-analyst, content-director, style-evolver, doc-polisher, impeccable-designer, diagram-architect, article-illustrator
- **全栈执行**：product-manager, product-enablement, proposal-writer, bid-writer, ppt-generator, video-maker, data-analyst

### 3.3 补 AGENT_ROUTING.md（补 AUDIT 未覆盖的边界说明）
明确 5 组高频混淆的路由规则：
- `@product-manager` vs `@gtm-strategist`：内部产品逻辑 vs B2B 走市场旅程
- `@research-analyst` vs `@web-search-analyst`：研究方法论 vs 搜索执行层
- `@content-director` vs `@style-evolver`：通用文章 vs 有独立风格进化流程的文章
- `@article-illustrator` vs `@diagram-architect` vs `@ppt-generator`：内联配图 vs 独立图表 vs 幻灯片嵌入
- `@product-manager` vs `@growth-strategist`：产品全流程 vs 增长实验

---

## 6. 执行顺序（4 个 commit）

| Commit | 内容 | 风险 | 预计影响面 |
|---|---|---|---|
| **C1** | Phase 3（删死码 + agents/README.md + AGENT_ROUTING.md） | 低 | 3 文件 |
| **C2** | Phase 1-A（4 组无冲突合并：dashboard/bid/md-render/video-gen） | 中 | ~25 文件 |
| **C3** | Phase 1-B（humanize + diagram 合并，⚠️ 需你确认覆盖 AUDIT） | 中 | ~10 文件；**默认跳过除非你明确同意** |
| **C4** | Phase 2（skills 分子目录 + 引用重写） | 高 | ~200+ 处引用 |

每个 commit 都独立可回退（`git revert <hash>`）。

---

## 7. 验收标准

```powershell
# 命令数从 114 → ≤ 95（若含 1-B）或 ≤ 100（若不含 1-B）
(Get-ChildItem commands -Recurse -Filter *.md).Count

# skill 分子目录后，根目录不应有平铺 SKILL.md
(Get-ChildItem skills -Filter SKILL.md).Count -eq 0

# 无孤儿 skill 引用
Select-String -Path "agents\*.md","commands\**\*.md" -Pattern "skills/[a-z-]+/SKILL\.md" `
  | Where-Object { $_.Line -notmatch "skills/(writing|prd|pm|product|presales|bid|dashboard|ppt|media|diagram|research|data|strategy)/" }
# 应无输出

# 无死链
Select-String -Path "**\*.md" -Pattern "@impeccable-manual-edit-applier"
# 应无输出

# 每个合并后的命令能加载至少一个 skill
grep -l "加载技能" commands/product/dashboard.md commands/presales/bid.md
```

---

## 8. 关键决策点（需用户回答）

1. **是否覆盖 AUDIT.md 撤回项，执行 Phase 1-B（humanize + diagram 合并）？**
   - 是 → 4 个 commit 全跑
   - 否 → 只跑 C1/C2/C4，跳过 C3（推荐给"保守派"）

2. **Phase 2（skills 分子目录）是否需要保留旧路径 shim？**
   - 是 → 在 `skills/<oldname>/SKILL.md` 留一层重定向说明，兼容外部引用（若有）
   - 否 → 硬迁移（推荐，仓库外无引用）

3. **合并后的命令是否保留原命令名做 alias？**
   - 是 → `commands/product/dashboard-northstar.md` 保留 3 行「已合并到 /dashboard --metric northstar」的迁移提示
   - 否 → 硬删（推荐）

---

## 9. 回退方案

任何 commit 出问题：
```powershell
git revert <hash>       # 单个 commit 回退
git reset --hard HEAD~4 # 全部回退到方案执行前
```

Phase 2（skills 分子目录）风险最大，会先跑在 `refactor/c1-skills-subdir` 分支，PR 前手工核验。

---

## 10. 不做事项（本方案主动排除）

沿用 AUDIT.md 236-249 「未做事项」：
- ✅ 不删 content-sync（driver/adapter 模式必要）
- ✅ 不删 sunset-plan（`/sunset` 直接依赖）
- ✅ 不删 chat2db（data-analyst 依赖）
- ✅ 不删 pm-ai-security-product（15+ 处依赖）
- ✅ 不删 ppt-architect（ppt-generator 核心）
- ✅ 不合并 prd-* 11 个（AUDIT 明确保留）
- ✅ 不合并 style-* 系列（AUDIT 明确保留）
- ✅ 不拆 product-manager agent（一站式价值）

**新增本轮的不做事项**：
- 不合并 ppt.md / illustrate.md（已是聚合命令）
- 不动 mega 命令 gtm-strategy.md（356L）、compliance-checklist.md（333L）、poc-plan.md（323L）——它们不是 stub
