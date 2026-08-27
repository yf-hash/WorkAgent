---
name: content
description: 内容创作端到端统一入口 — **单一调用入口**（对外只暴露这一个）。一句自然语言 → 自动流转文体识别 → 素材抽取（可选关联 PM/SA 项目）→ 八大文体专项生成 → 五类校验 → 人工审核 → 归档 + 多格式导出。支持从任意 stage 起跑、局部重写指定章节、驳回回退。
user-invocable: true
argument-hint: "<自然语言描述> or <已有 content-pipeline 目录> [--style <id>] [--project <path>] [--audience <string>] [--length <int>] [--tone <string>] [--format-out markdown|word|ppt-json|all] [--from M1|M2|M3|M4|M5] [--to Mx] [--section N] [--writeback] [--skip-gate]"
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob, AskUserQuestion]
harness:
  execute:
    preset: agent-orchestrator
  constrain:
    profile: writing-safe
    gates: [before-stage, after-stage, before-writeback]
  loop:
    mode: pipeline
    stages: [M1, M2, M3, M4, M5]
    gate-between: true
  memory:
    scope: project
    reads: [project-context, content-intake-history, content-materials-history, content-generate-history, content-validate-history]
    writes: [pipeline-state]
  security:
    danger-level: low
---

# /content — 内容创作统一入口编排器（单一调用入口）

> **对外只暴露这一个入口**。上层应用、界面、脚本都调用它，用户不需要理解内部 Agent、流水线细节。
>
> M1 网关 → M2 素材（可选）→ M3 生成 → M4 校验 → M5 归档 全流程编排。

## 一句话

**给一句自然语言，本命令自动跑完整 5 模块流水线，产出可交付的内容物料**（八大文体皆可）。

## 用法

### 场景 1：从零开始一句话触发

```bash
# 最简
/content "写一篇 VulnHunter 新版本 PR 稿"

# 关联 PM 项目（自动拉素材）
/content "基于项目 PM-00126 写一份产品解决方案白皮书，面向政企安全负责人，重点讲 POC 沙箱调度能力，5000 字左右" \
  --project ./output/pm-pipeline/vulnhunter-20260827/

# 关联 SA 项目
/content "基于本次投标方案，写一篇宣讲 PPT" \
  --project ./output/sa-pipeline/vulnhunter-mfg-20260830/

# 显式指定所有参数（跳过 AskUserQuestion）
/content "写解决方案白皮书" \
  --style solution-whitepaper \
  --project ./output/pm-pipeline/xxx/ \
  --audience "政企安全运维负责人" \
  --length 8000 \
  --tone "正式,专业" \
  --format-out word \
  --writeback
```

### 场景 2：断点续跑

```bash
# 已经跑到 M3，从 M4 校验开始
/content ./output/content-pipeline/xxx/ --from M4

# 只重跑归档
/content ./output/content-pipeline/xxx/ --from M5
```

### 场景 3：局部重写

```bash
# 只重写第 3 章
/content ./output/content-pipeline/xxx/ --section 3

# 驳回回到素材抽取（补充素材后重新流转）
/content ./output/content-pipeline/xxx/ --from M2 --reason "素材池缺少 XX 案例"

# 驳回回到生成（保留素材，重跑生成）
/content ./output/content-pipeline/xxx/ --from M3
```

### 场景 4：跨流水线（内容挂载到项目）

```bash
# 完整跑 + 挂载回原 PM 项目
/content "写发布 PR 稿" --project ./output/pm-pipeline/xxx/ --writeback

# 生成的 PR 稿会同时归档到：
#   ./output/content-pipeline/pr-xxx-{date}/  （content 主目录）
#   ./output/pm-pipeline/xxx/_content/pr-xxx-{date}/  （项目附属产物）
```

## 编排逻辑

### 阶段 0：初始化

**若输入是自然语言**：
1. 从输入提取 `{style}-{topic-slug}` 组合
2. 创建目录 `./output/content-pipeline/{style}-{topic-slug}-{yyyymmdd}/`
3. 初始化 `.pipeline-state.json`

**若输入是已存在目录**：
1. 读取 `.pipeline-state.json` 获取当前进度
2. 依据 --from 判定重跑起点

### 5 阶段调度

```
M1 → gate → M2（如关联项目）or skip → gate → M3 → M4 → gate → M5
     ↑                                          ↓
     └─── 用户驳回 → 回到指定 stage ←─────────┘
```

### STAGE_COMMANDS 映射

| Stage | Command | 输入依赖 |
|---|---|---|
| M1 | `/content-intake {raw_input} --out {dir}/00-content-request.json` | raw_input + 参数 |
| M2 | `/content-materials {dir}/00-content-request.json --out {dir}/01-material-pool.md` | M1（有项目关联） |
| M3 | `/content-generate {dir}/00-content-request.json [{dir}/01-material-pool.md] --out {dir}/02-draft.md` | M1 + M2 |
| M4 | `/content-validate {dir}/02-draft.md [{dir}/01-material-pool.md] --out {dir}/03-validate-report.md` | M3 |
| M5 | `/content-archive {dir}/ [--export all] [--writeback]` | 全部 |

## Harness 卡点

### 每阶段之后的 gate 交互

```
【M{n} 完成】{产物名} 已生成：
  {文件路径}

关键内容速览：
  {关键统计}

请选择：
  (1) 通过 → 继续 M{n+1}
  (2) 驳回 → 回到上游 stage
  (3) 局部重写 → --section N（仅 M3 后可用）
  (4) 编辑后继续 → 我手工改文件，改完按 Enter
  (5) 中止 → 停止流水线，保留当前进度
```

### M4 校验 gate（关键红线）

M4 校验后必须显示详细结果 + 阻断 🔴 项：

```
【M4 五类校验完成】

事实一致性：{n1}/{total1}
  🔴 冲突：{c1} 处（阻断）
  🟡 部分：{p1} 处
  ⚠️ 未在素材：{u1} 处

合规风险：{c} 处高风险
  🔴 绝对化词：{列表}（阻断）

文体风格：{s}/10（低于 7 阻断）

完整性：{✅/❌}（必备要素缺失阻断）

引用可追溯率：{p}%

--------------------------------
总体：{通过 / 有修改建议 / 需重写}

如有 🔴，必须选择：
(1) 局部重写受影响章节
(2) 全部重跑生成
(3) 编辑修复后重跑校验
(4) 强制归档（写入 known-issues.md，仅用于内部试稿）
```

### `--skip-gate` 模式

- 用于快速原型（不推荐正式产出）
- 每阶段完成后打印摘要，不问用户
- M4 有 🔴 项仍会强制暂停（不可绕过）

## `.pipeline-state.json` 结构

```json
{
  "style": "solution-whitepaper",
  "topic": "VulnHunter 漏洞猎人产品解决方案",
  "topic_slug": "vulnhunter-solution",
  "created_at": "2026-08-27T15:00:00+08:00",
  "raw_input": "...",
  "params": {
    "audience": "政企安全负责人",
    "length": 8000,
    "tone": ["正式", "专业"],
    "format_out": "word",
    "writeback": true
  },
  "project": {
    "linked": true,
    "path": "./output/pm-pipeline/vulnhunter-20260827/",
    "type": "PM"
  },
  "stages": {
    "M1": { "status": "done", "at": "..." },
    "M2": { "status": "done", "at": "..." },
    "M3": { "status": "done", "at": "..." },
    "M4": { "status": "in-progress" },
    "M5": { "status": "pending" }
  },
  "gates": {
    "after-M1": { "reviewed": true },
    "after-M2": { "reviewed": true },
    "after-M4": { "reviewed": false }
  },
  "version": "1.0.0"
}
```

## 输出结构

```
./output/content-pipeline/{style}-{topic-slug}-{yyyymmdd}/
├── .pipeline-state.json         ← 流水线状态
├── 00-content-request.json      ← M1
├── 00-raw-input.txt              ← M1
├── 00-intake-log.md              ← M1
├── 01-material-pool.md           ← M2（可选）
├── 02-draft.md                   ← M3
├── 02-draft.json                 ← M3（仅 PPT 类）
├── 03-validate-report.md         ← M4
├── review-notes.md               ← M5 人工审阅（可选）
├── README.md                     ← M5
├── CHANGELOG.md                  ← M5
├── VERSION                       ← M5
├── archive-report.md             ← M5
├── _frozen/                      ← M5 冻结
│   └── v1.0-发布版/
└── _export/                      ← M5 导出
    ├── {topic}.md
    ├── {topic}.docx
    └── {topic}.pptx.json
```

## 常见剧本

### 剧本 A：产品发布 PR 稿（20 分钟）

```bash
/content "VulnHunter 完成新版本发布，新增分布式沙箱调度，写一份 PR 稿" \
  --project ./output/pm-pipeline/vulnhunter-20260827/ \
  --writeback

# 自动识别文体 = pr
# 拉 PM 项目产物 → 素材池
# 生成 1000 字 PR 稿
# 校验 + 归档 + 挂载到 PM 项目
```

### 剧本 B：客户方案白皮书（1-2 小时）

```bash
/content "基于本次投标方案写一份客户交付白皮书" \
  --project ./output/sa-pipeline/vulnhunter-mfg-20260830/ \
  --style solution-whitepaper \
  --length 12000 \
  --writeback
```

### 剧本 C：技术布道科普文（1 小时）

```bash
/content "写一篇讲清楚分布式沙箱调度原理的科普文" \
  --project ./output/pm-pipeline/vulnhunter-20260827/ \
  --style tech-popular \
  --audience "开发者" \
  --length 3000
```

### 剧本 D：季度汇报 PPT（30-60 分钟）

```bash
/content "把 VulnHunter 项目做成季度汇报 PPT" \
  --project ./output/pm-pipeline/vulnhunter-20260827/ \
  --style ppt \
  --audience "董事会" \
  --length 20 \
  --format-out ppt-json
```

### 剧本 E：客户反馈后局部重写

```bash
# 客户看了初稿后要求换一个案例
/content ./output/content-pipeline/xxx/ --section 6
```

## 与 /pm、/sa 的关系

```
                        WorkAgent
                            │
       ┌────────────────────┼────────────────────┐
       │                    │                    │
      /pm                  /sa                /content
    (内部 PRD)           (对外方案)           (内容传播)
       │                    │                    │
      /pm-pipeline         /sa-pipeline         /content
       │                    │                    │
       └───────素材──────► /content ◄──────素材──┘
                            │
                    产出可回写到 PM/SA
```

### 跨流水线协作场景
1. **PM 项目归档 → Content 出 PR 稿**：写发布通稿
2. **PM 项目归档 → Content 出推广文**：市场传播
3. **SA 项目中标 → Content 出解决方案白皮书**：客户交付
4. **SA 项目 → Content 出 PPT**：客户汇报
5. **Competitive 报告 → Content 出对比推广文**：差异化传播

## 反模式

- ❌ 用 `--skip-gate` 交付客户版 —— gate 是质量红线
- ❌ 手动改 `.pipeline-state.json` —— 状态会不一致
- ❌ 跳过 M2 素材抽取但仍引用具体数字 —— 事实错误温床
- ❌ M4 校验 🔴 项时强制归档并对外发布 —— 严重违规
- ❌ 写 PR 稿 / 白皮书 而不关联任何项目 —— 素材空转，容易失真
- ❌ 修改 `_frozen/` 内文件 —— 违规
