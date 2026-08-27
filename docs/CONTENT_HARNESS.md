# Content Harness — 内容创作端到端流水线（八大文体）

> **一句自然语言 → 完整可交付内容物料**：从统一入口输入自然语言描述，经过 5 个 Agent 模块，产出可交付的八大文体内容（PR 稿 / 推广文 / 白皮书 / PPT / 推文 / 科普文 等），可跨流水线复用 PM/SA 项目素材，也可回写为项目附属产物。
>
> 版本：v1.0（2026-08-27）

## 一、为什么需要这套 Harness

内容创作 / 市场 / 品牌人员的日常痛点：

- 每次写稿都要**手工整理产品资料**（PRD / 方案 / 规格书）
- 稿件与**产品实际能力脱节**（销售话术夸大 / 描述过时）
- **绝对化用词、合规风险**难以人工全检
- 白皮书 / PR 稿 / PPT / 推文，**每种文体规范不同**，需要不同模板
- 客户 / 内部反馈后要**局部重写**，全稿重跑成本高
- 生成的物料**难以挂回原项目**追溯

这套 Harness 的核心命题：

> **统一入口 + 素材可追溯 + 校验强制 + 跨流水线协作**

### 相比传统内容创作流程的差异化

| 传统流程 | Content Harness |
|---|---|
| 靠人工翻文档整理素材 | M2：项目素材抽取自动完成，含引用出处 |
| 文案与产品能力对不上 | M4：事实一致性校验对比素材池，冲突即警告 |
| 绝对化用词靠自查 | M4：合规校验含广告法关键词库 + 行业禁语 |
| 八大文体八种规范人工掌握 | M3：`content-templates` 每类内置章节 + 语气 + 长度 |
| 客户反馈后重写全稿 | 支持 `--section N` 局部重写 |
| 内容物料与产品项目脱节 | `--writeback` 挂载回原 PM/SA 项目附属产物 |
| 版本管理靠 Word 另存为 | 语义化版本 + freeze 快照 + 多格式导出 |

## 二、5 模块流水线全景图

```
┌──────────────────────────────────────────────────────────────┐
│ 【输入】一句自然语言 + 可选参数                                  │
│  "基于 VulnHunter 项目，写一份解决方案白皮书..."                │
└──────────────────────────────────────────────────────────────┘
                       │
                       ▼
    ┌──────────────────────────────────────────┐
    │  M1 内容请求网关（统一调用入口）             │
    │  /content-intake                          │
    │  ─────────────────────────                │
    │  · 文体识别（八大文体分类器）                 │
    │  · 项目关联抽取（PM/SA 项目路径）             │
    │  · 需求解析（受众/篇幅/风格/重点/禁止/输出）    │
    │  · ContentRequest JSON 结构化               │
    │                                           │
    │  → 00-content-request.json                │
    └──────────────────────────────────────────┘
                       │
                    🔒 Harness Gate（参数确认）
                       ▼
    ┌──────────────────────────────────────────┐
    │  M2 项目素材抽取（可选）                     │
    │  /content-materials                        │
    │  ─────────────────────────                │
    │  · 从 PM/SA 项目目录读取产物                 │
    │  · 按文体维度抽取（能力/架构/痛点/指标...）     │
    │  · 素材结构化（含引用出处 + 可信度）           │
    │  · 禁止提及清单（forbidden）                 │
    │  · 缺失章节警示                              │
    │                                           │
    │  → 01-material-pool.md                     │
    └──────────────────────────────────────────┘
                       │
                    🔒 Harness Gate（素材确认）
                    （无关联项目时跳过 M2）
                       ▼
    ┌──────────────────────────────────────────┐
    │  M3 八大文体专项生成                         │
    │  /content-generate                         │
    │  ─────────────────────────                │
    │  按 --style 路由到 8 类文体模板：             │
    │  ⓐ promo 产品推广文                         │
    │  ⓑ solution-doc 产品解决方案文               │
    │  ⓒ tech-whitepaper 产品技术白皮书            │
    │  ⓓ ppt 产品 PPT                            │
    │  ⓔ solution-whitepaper 产品解决方案白皮书    │
    │  ⓕ activity-tweet 产品活动推文               │
    │  ⓖ pr 企业 PR 稿                            │
    │  ⓗ tech-popular 产品技术科普文               │
    │                                           │
    │  → 02-draft.md（+ 02-draft.json for PPT）  │
    └──────────────────────────────────────────┘
                       │
                       ▼
    ┌──────────────────────────────────────────┐
    │  M4 五类内容校验                            │
    │  /content-validate                         │
    │  ─────────────────────────                │
    │  · 事实一致性（对比素材池）                   │
    │  · 合规风险（广告法 + 行业禁语 + 未授权披露）    │
    │  · 文体风格（评分制）                        │
    │  · 完整性（必备要素 checklist）              │
    │  · 引用可追溯（Fact → Source 映射）           │
    │                                           │
    │  → 03-validate-report.md                   │
    └──────────────────────────────────────────┘
                       │
                    🔒 Harness Gate（人工审核卡点）
                    编辑 / 驳回重跑 / 局部重写 / 通过
                       ▼
    ┌──────────────────────────────────────────┐
    │  M5 归档 + 多格式导出 + 跨流水线回写           │
    │  /content-archive                          │
    │  ─────────────────────────                │
    │  · 完整性 + 校验状态检查                     │
    │  · README + CHANGELOG + VERSION            │
    │  · 多格式导出（Markdown / Word / PPT JSON）  │
    │  · freeze 只读快照                          │
    │  · --writeback 回写到 PM/SA 项目附属产物      │
    │                                           │
    │  → README + CHANGELOG + _export/*          │
    │  → {project}/_content/{package}/ (可选)     │
    └──────────────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────────┐
│ 【输出】完整可交付内容包 + 可回写到关联项目                       │
│  ./output/content-pipeline/{style}-{topic}-{yyyymmdd}/       │
└──────────────────────────────────────────────────────────────┘
```

## 三、八大文体一览

| ID | 名称 | 受众 | 篇幅 | 关键要素 |
|---|---|---|---|---|
| `promo` | 产品推广文 | 决策者 | 800-2000 字 | 价值主张 / 收益 / CTA |
| `solution-doc` | 产品解决方案文 | 客户 IT + 业务 | 2000-5000 字 | 痛点-能力映射 / 部署 / 场景 |
| `tech-whitepaper` | 产品技术白皮书 | 技术受众 | 5000-15000 字 | 架构 / 原理 / 指标 / 局限 |
| `ppt` | 产品 PPT | 会议汇报 | 15-30 页 | title/bullets/visual/note + JSON |
| `solution-whitepaper` | 产品解决方案白皮书 | 客户决策 + 技术 | 8000-20000 字 | Summary / 行业 / 方案 / 案例 / ROI |
| `activity-tweet` | 产品活动推文 | 公众号 / 社群 | 500-1500 字 | 亮点 / 福利 / CTA |
| `pr` | 企业 PR 稿 | 媒体 | 800-1500 字 | 5W1H / 引用 / Boilerplate |
| `tech-popular` | 产品技术科普文 | 开发者 | 2000-5000 字 | 类比 / 举例 / 局限 |

## 四、5 模块产物清单

| 模块 | 命令 | 产物 | Skill 支撑 |
|---|---|---|---|
| M1 | `/content-intake` | 00-content-request.json | content-intake |
| M2 | `/content-materials` | 01-material-pool.md | content-materials |
| M3 | `/content-generate` | 02-draft.md (+ .json for PPT) | content-templates |
| M4 | `/content-validate` | 03-validate-report.md | content-validate |
| M5 | `/content-archive` | README + CHANGELOG + _export/ | content-archive |
| 统一入口 | `/content` | 全部 | 上述全部 |

## 五、目录结构约定

```
./output/content-pipeline/{style}-{topic}-{yyyymmdd}/
├── .pipeline-state.json         ← 流水线状态
├── 00-content-request.json      ← M1
├── 00-raw-input.txt              ← M1
├── 00-intake-log.md              ← M1
├── 01-material-pool.md           ← M2（可选）
├── 02-draft.md                   ← M3
├── 02-draft.json                 ← M3（仅 PPT 类）
├── 03-validate-report.md         ← M4
├── review-notes.md               ← 人工审阅（可选）
├── README.md                     ← M7
├── CHANGELOG.md                  ← M7
├── VERSION                       ← M7
├── archive-report.md             ← M7
├── _frozen/                      ← --freeze 生成
│   └── v1.0-发布版/
└── _export/                      ← --export 生成
    ├── {topic}.md
    ├── {topic}.docx
    └── {topic}.pptx.json
```

## 六、如何使用

### 方式 A：单一统一入口（推荐）

```bash
/content "基于 VulnHunter 项目，写一份解决方案白皮书，面向政企安全负责人，8000 字左右" \
  --project ./output/pm-pipeline/vulnhunter-20260827/ \
  --writeback
```

一句话触发，自动 M1 → M5 全流程，每阶段之间 gate 询问。

### 方式 B：通过角色总入口 /content 智能识别

```bash
/content 帮我给 VulnHunter 项目写一份产品发布 PR 稿
```

`/content` agent 识别信号 → 推荐流水线 → 用户确认 → 自动调度。

### 方式 C：手工分步执行

```bash
/content-intake "自然语言"
/content-materials ./00-content-request.json --project ./output/pm-pipeline/xxx/
/content-generate ./00-content-request.json ./01-material-pool.md
/content-validate ./02-draft.md ./01-material-pool.md
/content-archive ./output/content-pipeline/xxx/ --export all --writeback
```

### 方式 D：局部重写 / 驳回回退

```bash
# 只重写第 3 章
/content ./output/content-pipeline/xxx/ --section 3

# 驳回回到素材抽取（补充素材后重跑）
/content ./output/content-pipeline/xxx/ --from M2 --reason "缺少 XX 案例"

# 从校验开始重跑（人工改稿后）
/content ./output/content-pipeline/xxx/ --from M4
```

## 七、Harness 卡点机制

| Gate | 触发时机 | 用户选项 |
|---|---|---|
| after-M1 | 请求解析后 | 通过 / 修改参数 / 中止 |
| after-M2 | 素材抽取后 | 通过 / 补充素材 / 忽略缺失 / 中止 |
| after-M4 | 校验后 | 编辑重跑 / 局部重写 / 全部重跑 / 强制通过 / 中止 |
| before-freeze | freeze 前 | 确认 / 取消 |
| before-writeback | writeback 前 | 确认 / 取消 |

**旁路**：`--skip-gate` 用于快速原型，正式发布严禁使用。M4 有 🔴 项时强制暂停（不可绕过）。

## 八、5 个 Skill 的能力矩阵

| Skill | 位置 | 服务命令 | 核心能力 |
|---|---|---|---|
| content-intake | skills/content/ | /content-intake | 八大文体分类器 + 需求解析 + JSON Schema |
| content-materials | skills/content/ | /content-materials | PM/SA 产物结构 + 按文体的抽取维度 + 禁止提及 |
| content-templates | skills/content/ | /content-generate | 八大文体章节 + 语气 + 长度 + 必备要素 + 禁用词 |
| content-validate | skills/content/ | /content-validate | 5 类校验规则库（含广告法词库 + 行业禁语） |
| content-archive | skills/content/ | /content-archive | 完整性检查 + 多格式导出 + 跨流水线回写 |

## 九、与 PM / SA Harness 的关系

```
                        WorkAgent v3.2
                            │
       ┌────────────────────┼────────────────────┐
       │                    │                    │
      /pm                  /sa                /content
    (内部 PRD)           (对外方案)           (内容传播)
   6 模块 M2-M7        7 模块 M1-M7          5 模块 M1-M5
       │                    │                    │
       └───────素材──────► /content ◄──────素材──┘
                            │
                            ▼
                   产出可回写到 PM/SA 项目
                   _content/{package}/
```

### 跨流水线协作场景

| 场景 | 用法 |
|---|---|
| PM 项目上线，出 PR 稿 | `/content "PR 稿" --project {PM path} --writeback` |
| PM 项目上线，出推广文 | `/content "推广文" --project {PM path} --writeback` |
| SA 中标，出客户交付白皮书 | `/content "解决方案白皮书" --project {SA path} --writeback` |
| SA 汇报，出客户 PPT | `/content "PPT" --project {SA path}` |
| 竞品分析报告，出对比推广文 | 参考 /pm-competitive 输出 |
| 季度汇报 | `/content "季度 PPT" --project {PM path}` |

## 十、反模式（禁止）

- ❌ **用 --skip-gate 交付客户版** —— gate 是质量红线
- ❌ **跳过 M2 素材抽取但仍引用具体数字** —— 事实错误温床
- ❌ **M4 校验 🔴 项时强制归档并对外发布** —— 严重违规
- ❌ **写 PR 稿 / 白皮书而不关联任何项目** —— 素材空转，容易失真
- ❌ **忽视 forbidden 清单** —— 会踩合规雷
- ❌ **修改 `_frozen/` 内文件** —— 审计留档不可篡改
- ❌ **回写覆盖原项目主流水线产物** —— 只能创建新子目录

## 十一、演进路线

- ✅ v1.0（2026-08-27）：首版 5 模块流水线上线
- ⏳ v1.1：M3 PPT 类支持直接生成 `.pptx` 文件（python-pptx）
- ⏳ v1.2：M2 增加对 Competitive 项目的素材抽取
- ⏳ v1.3：M4 引入 LLM 自评 + 人工评估对比
- ⏳ v2.0：接入内容分发平台（公众号 / LinkedIn / 微博 API）

## 十二、故障排查

| 症状 | 原因 | 解决 |
|---|---|---|
| M1 文体识别失败 | 输入模糊 | 显式 --style |
| M2 项目路径无效 | project 目录不存在 | 检查路径 |
| M2 素材缺失章节警示 | 项目未完整跑完 | 先补跑 PM/SA 主流水线 |
| M3 生成内容偏短 / 偏长 | 素材不足 / 素材过多 | 调整 --length 或补素材 |
| M4 事实一致性大量 🔴 | 生成时未引用素材池 | 重跑 M3 |
| M4 合规 🔴 | 使用了绝对化用词 | 按 skill 建议改写 |
| M5 pandoc 未安装 | 本机缺 pandoc | 只导 Markdown |
| M5 writeback 失败 | 项目目录不存在 | 检查 project.path |

## 十三、快速上手

**第一次用**：

```bash
# 1. 用简单需求熟悉流水线（无项目关联）
/content "写一篇 500 字的产品活动推文，介绍新版本发布"

# 2. 看看产出目录长啥样
ls ./output/content-pipeline/activity-tweet-*/

# 3. 用关联项目跑正式内容
/content "基于 VulnHunter 项目写解决方案白皮书" \
  --project ./output/pm-pipeline/vulnhunter-20260827/ \
  --writeback
```

**升级你的日常习惯**：

- 每次 PM/SA 项目归档后，立刻跑 `/content --writeback` 出对外物料
- 内容规范全部内嵌到 skill，不用记
- 内容库通过 `_content/` 子目录挂载在项目里，一个项目就是一个完整的"知识包"

---

**相关文档**：

- 顶层 Harness 框架：[`../HARNESS_FRAMEWORK.md`](../HARNESS_FRAMEWORK.md)
- PM Harness 总览：[`PM_HARNESS.md`](PM_HARNESS.md)
- SA Harness 总览：[`SA_HARNESS.md`](SA_HARNESS.md)
- 项目级说明：[`../.claude/CLAUDE.md`](../.claude/CLAUDE.md)
- Content 角色清单：[`../roles/content/manifest.yaml`](../roles/content/manifest.yaml)
- 6 大命令文档：[`../commands/content/*.md`](../commands/content/)
- 5 大 skill 文档：[`../skills/content/*/SKILL.md`](../skills/content/)
