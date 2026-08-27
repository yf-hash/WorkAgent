---
name: content-generate
description: 【模块 3】八大文体专项内容生成 — 输入 ContentRequest + 素材池，按 --style 参数分派到对应文体的模板生成初稿。八大文体：promo / solution-doc / tech-whitepaper / ppt / solution-whitepaper / activity-tweet / pr / tech-popular。生成后自查（章节完整性 + 素材引用比例 + 绝对化用词初筛）。
user-invocable: true
argument-hint: "<00-content-request.json 路径> [<01-material-pool.md 路径>] [--style <id>] [--section <n>] [--out <path>]"
allowed-tools: [Read, Write, Edit, AskUserQuestion, Grep, Glob]
harness:
  execute:
    preset: writing-scoped
  constrain:
    profile: writing-safe
    gates: [before-write]
  loop:
    mode: one-shot
  memory:
    scope: project
    reads: [project-context, content-intake-history, content-materials-history]
    writes: [content-generate-history]
  security:
    danger-level: low
---

# /content-generate — 八大文体专项生成（Module 3）

> **端到端内容创作流水线的第 3 站**
>
> /content-materials →【本命令】→ /content-validate → /content-archive

## 一句话

**根据 ContentRequest.style，调度对应文体的模板 + 语气 + 长度规范，结合素材池生成初稿**。

## 输入

```bash
# 最常见：接 M1 + M2 输出
/content-generate ./output/content-pipeline/xxx/00-content-request.json ./01-material-pool.md

# 无关联项目（无素材池）
/content-generate ./00-content-request.json

# 显式指定文体（覆盖 request 里的 style）
/content-generate ./00-content-request.json ./01-material-pool.md --style tech-whitepaper

# 局部重写（只重写某个章节，其他保留）
/content-generate ./00-content-request.json ./01-material-pool.md --section 3
```

## 八大文体路由

从 `content-request.style.id` 判定，调用 `skills/content/content-templates` 中对应模板：

| Style ID | 内部处理 | 输出主结构 |
|---|---|---|
| `promo` | 商业化语气 + 场景化 | 8 章推广文 |
| `solution-doc` | 专业务实 + 痛点方案映射 | 9 章方案文 |
| `tech-whitepaper` | 严谨技术 + Mermaid + 指标 | 9 章技术白皮书 |
| `ppt` | 页面结构化 JSON + 备注话术 | 15-30 页 PPT JSON + Markdown |
| `solution-whitepaper` | 系统正式 + 案例 + ROI | 9 章解决方案白皮书 |
| `activity-tweet` | 轻量活泼 + emoji + CTA | 推文（短段落） |
| `pr` | 新闻体 + 5W1H + 引用 | 标准 PR 稿 |
| `tech-popular` | 通俗 + 类比 + 示例 | 科普 6 章 |

## 内部处理

### 步骤 1：加载文体规范
- 读 `skills/content/content-templates` 中对应 style 的：
  - 章节结构
  - 语气规范
  - 长度分配
  - 必备要素
  - 禁用词

### 步骤 2：素材筛选
- 从素材池按 style 的"主要素材维度" / "次要素材维度" 筛选可用素材
- 标记 forbidden 项，生成时严禁触碰

### 步骤 3：分章节生成
- 按结构逐章写
- 每章生成时检查：
  - 长度是否在配额内（± 20% 容忍）
  - 是否只引用素材池
  - 是否有绝对化用词（先自查一遍）

### 步骤 4：自查
生成完后逐项检查：
- [ ] 章节完整（无遗漏）
- [ ] 素材引用比例 ≥ 70%（关键事实）
- [ ] 无绝对化用词（最 / 第一 / 100% / 唯一）
- [ ] 篇幅偏差 < 20%
- [ ] Mermaid 图（如需）
- [ ] 案例（如需）

## 输出格式

### 主输出：02-draft.md

```markdown
# {{文体名}}：{{topic}} v0.1

> 上游：00-content-request.json / 01-material-pool.md
> 文体：{{style.name}}
> 生成时间：{{yyyy-mm-dd hh:mm}}
> 篇幅：{{estimated_length}}（目标 {{length.value}}）

## [按文体的章节结构展开]

...

---

## 附：生成自查
- [x] 章节完整
- [x] 素材引用比例：{p}%（关键事实全部来自素材池）
- [x] 绝对化用词初筛：0 处
- [x] 篇幅：{{estimated_length}}（偏差 {δ}%）
- [ ] 待人工核对：{列表}
```

### PPT 类附加输出：02-draft.json

```json
{
  "$schema": "content-ppt-v1",
  "title": "...",
  "total_pages": 20,
  "pages": [...]
}
```

## 局部重写（--section N）

```bash
# 只重写第 3 章
/content-generate ./00-content-request.json ./01-material-pool.md --section 3
```

**行为**：
- 保留其他章节
- 读取现有 02-draft.md 定位章节 N
- 只重写该章节
- 生成 02-draft-v{n+1}.md（不覆盖旧版本）
- 记入 CHANGELOG

## 与其他命令的边界

| 场景 | 用 |
|---|---|
| **request + 素材 → 初稿** | 本命令 |
| 校验（含合规 + 事实） | 下一步 `/content-validate` |
| 一键端到端 | `/content`（编排器） |
| 局部重写 | 本命令 `--section N` |
| 无素材直接生成 | 本命令（跳过 M2） |

## Harness 卡点

**本命令默认无 gate**（生成后立刻交给 M4 校验），gate 由 M4 校验后统一执行。

## 反模式

- ❌ 引用素材池外的具体数字 —— 违规
- ❌ 生成时不看文体规范章节结构 —— 违规
- ❌ 篇幅严重偏差（> 30%）—— 违规
- ❌ 触碰 forbidden 清单 —— 严重违规
- ❌ 未做生成自查 —— 违规
- ❌ PPT 类未输出结构化 JSON —— 违规
