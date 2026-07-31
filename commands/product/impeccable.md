---
name: impeccable
description: >
  Impeccable 设计语言入口 — 让 AI 生成的 UI 不再像 AI。集成 Paul Bakaus 的impeccable.style 设计语言（27 条反 AI slop 反模式 + 7 个领域 reference + 13 个子命令）。
  适用场景：landing page / dashboard / 组件 / 表单 / 品牌站设计与代码生成、AI 味重的 UI 修复、上线前设计审查、风格调整（bolder/quieter/distill）。
user-invocable: true
argument-hint: "<craft|teach|document|extract|shape|critique|audit|polish|bolder|quieter|distill|harden|onboard> [目标] [--register brand|product] [--genre editorial|tech-minimal|luxury|brutalist|consumer-warm] [--stack react|vue|html|tailwind] [--audit-only]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - WebFetch
  - AskUserQuestion
---

# /impeccable — 反 AI Slop 的设计语言入口

> 改编自 [pbakaus/impeccable](https://github.com/pbakaus/impeccable) by Paul Bakaus。完整文档：[impeccable.style](https://impeccable.style/)

加载技能：
- `skills/diagram/impeccable/SKILL.md`（设计语言核心 + 27 条反模式 + 12 条 critique）
- `skills/diagram/impeccable/references/{typography,color,spatial,motion,interaction,responsive,ux-writing}.md`（按需）
- 必要时编排：`@impeccable-designer` Agent

## 触发条件

- 需要从零做一个 landing page / dashboard / 组件 / 品牌站
- 已有 UI 看起来"AI 味重"，想修
- 上线前要过一遍设计 + a11y + 性能审查
- 想调整设计强度（变更大胆 / 变更克制 / 删减元素）
- 想从现有代码反推出 DESIGN.md
- 新项目首次配置设计系统

---

## 子命令矩阵

```bash
# 创作型（writes code）
/impeccable craft <brief>             # 完整闭环：shape → build → audit → polish
/impeccable shape <brief>             # 只规划 UX/UI，不写代码
/impeccable extract                   # 把现有组件 + token 抽到设计系统

# 配置型（writes docs）
/impeccable teach                     # 首次项目设置：访谈 → PRODUCT.md + DESIGN.md
/impeccable document                  # 反向：从代码生成 DESIGN.md

# 评审型（reads code, may write fixes）
/impeccable critique [target]         # UX 主观评判（层级/清晰度/共鸣，LLM 跑 12 条）
/impeccable audit [target]            # 技术确定性检查（a11y/性能/反 slop 27 条）
/impeccable polish [target]           # 上线前最后一次过

# 调整型（writes code）
/impeccable bolder [target]           # 放大对比、加重，让设计更大胆
/impeccable quieter [target]          # 降强度、减饱和，让设计更克制
/impeccable distill [target]          # 删非本质元素，留 20% 最重要
/impeccable harden [target]           # 工程兜底：error handling / i18n / 边界
/impeccable onboard [target]          # 首次使用流 / 空状态 / 激活路径
```

---

## 参数

| 参数 | 说明 | 默认 |
|------|------|------|
| `<subcommand>` | 子命令（必填） | — |
| `[target]` | 文件路径或区块名（"the header" / "checkout form" / `src/Hero.tsx`） | 整个项目 |
| `--register` | 寄存器 | 由 brief 推断 |
| `--genre` | 流派 | 由 register 推断 |
| `--stack` | 技术栈 | 自动检测 |
| `--audit-only` | 只列问题不修 | false |
| `--no-references` | 跳过 reference 加载（节省 token，仅紧急修改） | false |

### Register
| 值 | 适用 | 评判 |
|----|------|------|
| `brand` | marketing 页 / 品牌站 / portfolio / 活动页 | Distinctiveness |
| `product` | App UI / Admin / Dashboard / 工具 | Earned familiarity |

### Genre
| 值 | 调性 |
|----|------|
| `editorial` | 杂志式，serif display + 中性 sans body |
| `tech-minimal` | Linear/Stripe/Vercel 调，grotesque sans only |
| `luxury` | 高对比 serif，深背景，留白多 |
| `brutalist` | mono / 工业感，高饱和原色，反主流 |
| `consumer-warm` | 圆润 humanist，暖色，亲切 |

---

## 快速示例

```bash
# 从零做一个落地页（最常用）
/impeccable craft "AI 安全运营平台 marketing landing"
/impeccable craft "城商行 SOC 产品页" --register brand --genre tech-minimal

# 已有项目调整
/impeccable critique src/components/Hero.tsx
/impeccable audit                                # 整个项目
/impeccable polish "the checkout form" --stack react
/impeccable quieter "the dashboard sidebar"     # 太喧闹了
/impeccable distill "the pricing page"          # 太啰嗦
/impeccable bolder "the marketing hero"         # 太平淡

# 配置阶段
/impeccable teach                                # 新项目首次跑
/impeccable document                             # 已有项目，反推 DESIGN.md
/impeccable extract                              # 抽组件到设计系统

# 上线前
/impeccable harden "the signup flow"            # 加 error / i18n / 边界
/impeccable onboard "first-run experience"      # 设计 onboarding

# 只看不动
/impeccable audit src/ --audit-only             # 出问题清单，不修
```

---

## craft 完整闭环（最常用）

```
Phase 1: Brief Capture（必要时 AskUserQuestion）
  Q1: Register（Brand / Product）
  Q2: Genre 偏好（editorial / tech-minimal / luxury / brutalist / consumer-warm / 让我决定）
  Q3: 已有 DESIGN.md？
  Q4: 技术栈（React+Tailwind / Vue / HTML / 其他）

Phase 2: 按需加载 references
  落地页：typography + color + spatial + motion + ux-writing
  Dashboard：spatial + interaction + responsive + typography
  表单：interaction + ux-writing + responsive

Phase 3: Shape（结构规划）
  - 信息架构
  - 区块顺序
  - 关键 CTA
  - 用真实长内容压力测试

Phase 4: Build（按固定顺序）
  1. Structure
  2. Spacing & Hierarchy（8px grid）
  3. Type & Color（OKLCH + tinted neutrals + One Voice）
  4. States
  5. Motion（ease-out + transform/opacity）
  6. Responsive（mobile-first + container queries）

Phase 5: Anti-Slop 自检（27 条）
  字体 / 颜色 / 间距 / 动效 / 兜底

Phase 6: Polish（设计系统对齐 + ship-ready）
  - DESIGN.md token 同步
  - 真实内容回填
  - 对比度 AA 自查
```

---

## 输出结构

### craft / shape 的输出

```
1. Register 与 Genre 决策摘要（1 段）
2. 信息架构（区块清单）
3. 设计 token（颜色 OKLCH / 字号尺度 / 间距尺度）
4. 完整代码（HTML/JSX/Vue + 样式）
5. Anti-Slop 自检报告（27 条全过 / 例外说明）
6. 后续建议（"建议跑 /impeccable harden"）
```

### audit 的输出

```
## P0（必须修，3）
- [a11y] CTA 对比度 2.8:1（< 4.5:1）
- [slop] 紫蓝渐变 line 42
- [perf] hero img 无 srcset

## P1（强烈建议，5）
- [slop] all-caps eyebrow "OUR FEATURES"
- ...

## P2 / P3 略

## 修复路径建议
- 复杂的进 /impeccable polish
- 工程性的进 /impeccable harden
- 视觉调性的进 /impeccable quieter or bolder
```

### critique 的输出

12 条主观评判，每条 1-2 段，按"维度 → 现状判断 → 建议"。

---

## 反模式速查（27 条 + 12 条总览）

### 27 条 deterministic（不需要 LLM 判断）

字体 8 / 颜色 10 / 间距 5 / 动效 3 / 兜底 1

完整清单见 `skills/diagram/impeccable/SKILL.md`。

### 12 条 LLM critique

Hierarchy / Emotional Resonance / Information Density / Visual Hierarchy via Scale /
Optical Alignment / Whitespace as Composition / Restraint / Specificity /
Genre Awareness / Microcopy Voice / Real Content Stress Test / Reading the Room

---

## 命令对比

| 易混淆对 | 何时用前者 | 何时用后者 |
|---------|----------|----------|
| `quieter` vs `distill` | 元素留着，但音量降低 | 删元素，留 20% 最重要 |
| `critique` vs `audit` | 主观、LLM 判断"感觉对吗" | 客观、grep 检查"硬指标过了吗" |
| `craft` vs `shape` | 要完整代码 | 只要规划，不要代码 |
| `polish` vs `harden` | 视觉对齐 + 设计 token 同步 | 工程性兜底（error / i18n / 边界） |
| `teach` vs `document` | 新项目从访谈出发 | 老项目从代码反推 |
| `bolder` vs 重做 | 现有结构没问题，调强度 | 结构都错了，应该 `shape` 重来 |

---

## 与 WorkAgent 其他命令的协同

```
PRD 阶段：
  /prd --mode standard → /design-proto → /impeccable craft

营销页阶段：
  /marketing-copy → /impeccable craft（用 copy 做页面）

文章阶段：
  /article-writer → /illustrate → 文章本体不走 impeccable

上线前：
  /impeccable audit → /impeccable harden → /launch-checklist

设计系统建立：
  /impeccable teach → /impeccable extract → 沉淀 DESIGN.md

去 AI 味闭环：
  UI 走 /impeccable critique
  文案走 /humanize --mode scan → --mode soul
```

---

## 已知限制

1. **Vocabulary ≠ Taste**：知道术语不等于知道何时用。最终视觉判断还要设计师。
2. **单页优化**：跨多页一致性靠 `teach` 出的 `DESIGN.md` 承载。
3. **Opinion codified**："不要 bounce / 不要纯黑" 是 Paul Bakaus 的审美。如果你的品牌就要 bounce，请在 brief 里显式说明，命令会覆盖。
4. **Token 预算**：完整 craft 约 12k tokens（含 references），dashboard 约 8k。可加 `--no-references` 跳过加载（仅紧急小改用）。

---

## 来源

- 原作者：[Paul Bakaus](https://www.paulbakaus.com/)（jQuery UI 作者、ex-Google AMP DevRel）
- 仓库：[pbakaus/impeccable](https://github.com/pbakaus/impeccable)（MIT-ish）
- 站点：[impeccable.style](https://impeccable.style/)
- 本命令是 WorkAgent 对 Impeccable 设计语言的中文集成与编排，命令前缀 `/impeccable <sub>` 与原项目命名兼容。
