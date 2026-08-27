---
name: content-intake
description: 【模块 1】内容请求网关（统一调用入口的内部第一站）— 输入自然语言描述，输出标准化 ContentRequest JSON。含文体识别（八大文体分类器）、上下文关联（PM/SA 项目 ID 或路径抽取）、需求解析（受众/篇幅/风格/重点/禁止项/输出格式）。
user-invocable: true
argument-hint: "<自然语言描述> [--style <id>] [--project <path>] [--audience <string>] [--length <int>] [--tone <string>] [--format-out markdown|word|ppt-json] [--out <path>]"
allowed-tools: [Read, Write, Edit, AskUserQuestion, Grep, Glob]
model: sonnet  # 轻量：文体分类 + 参数抽取，无需 opus
harness:
  execute:
    preset: writing-scoped
  constrain:
    profile: writing-safe
    gates: [before-write, after-parse]
  loop:
    mode: pipeline
    stages: [文体识别, 项目关联, 需求解析, ContentRequest 结构化]
  memory:
    scope: project
    reads: [project-context]
    writes: [content-intake-history]
  security:
    danger-level: low
---

# /content-intake — 内容请求网关（Module 1）

> **端到端内容创作流水线的第 1 站（统一入口的内部实现）**
>
> 【本命令】→ /content-materials → /content-generate → /content-validate → /content-archive

## 一句话

**把用户一句自然语言描述，加工成标准化的 ContentRequest JSON 对象**，供整条流水线共享。

## 输入

```bash
# 最简：一句话自然语言
/content-intake "写一篇 VulnHunter 新版本 PR 稿"

# 显式指定关键参数（可覆盖自动识别）
/content-intake "写解决方案白皮书" --style solution-whitepaper --length 8000 --audience "政企安全负责人"

# 关联 PM/SA 项目
/content-intake "基于 VulnHunter 项目写白皮书" --project ./output/pm-pipeline/vulnhunter-20260827/

# 关联项目 + 显式所有参数
/content-intake "写 PPT" --style ppt --project ./output/sa-pipeline/xxx/ --audience "客户 CIO" --length 20 --tone 简洁
```

## 内部四阶段

### 阶段 1：文体识别

调用 `skills/content/content-intake` 的分类规则库，对输入做**八分类**：

| 触发关键词 | 文体 | Style ID |
|---|---|---|
| 推广 / 卖点 / 场景化 / 客户价值 / 决策者 | 产品推广文 | `promo` |
| 解决方案文 / 方案文档 / 客户方案 | 产品解决方案文 | `solution-doc` |
| 技术白皮书 / 技术架构说明 / 技术原理 / 技术挑战 | 产品技术白皮书 | `tech-whitepaper` |
| PPT / 演示文稿 / 幻灯片 / 大纲 | 产品 PPT | `ppt` |
| 解决方案白皮书 / 行业白皮书 / 行业方案 | 产品解决方案白皮书 | `solution-whitepaper` |
| 推文 / 公众号 / 新品上线 / 活动 | 产品活动推文 | `activity-tweet` |
| PR 稿 / 新闻稿 / 媒体稿 / 发布稿 | 企业 PR 稿 | `pr` |
| 科普 / 讲清楚 / 通俗 / 由浅入深 / 是什么 | 产品技术科普文 | `tech-popular` |

- 命中一个 → 直接采用
- 命中多个 → 用 AskUserQuestion 让用户选
- 命中零个 → 用 AskUserQuestion 展示八选一

### 阶段 2：项目关联抽取

从输入或参数中抽取关联项目：

- **--project 参数**（显式路径）：优先
- **--project-id 参数**（如 `PM-00126`）：查找项目目录
- **输入中出现路径**：`./output/pm-pipeline/*` 或 `./output/sa-pipeline/*`
- **输入中出现项目 slug**：如 "VulnHunter 项目" → 尝试搜 `./output/*/vulnhunter*`
- **无关联**：`project: null`，M2 会跳过

### 阶段 3：需求解析

从自然语言 + 参数抽取以下字段：

| 字段 | 解析规则 | 默认值 |
|---|---|---|
| audience | "面向 XX / 目标 XX / 给 XX 看" | "通用" |
| length | 数字 + "字/页" | 依文体默认 |
| tone | "正式 / 专业 / 轻量 / 通俗 / 严谨" | 依文体默认 |
| emphasis | "突出 XX / 重点讲 XX / 强调" | 空 |
| forbidden | "不要 XX / 避免 XX / 禁止 XX" | 空 |
| format_out | --format-out or "输出 XX 格式" | markdown |
| include_mermaid | "架构图 / Mermaid / 流程图" | false（技术类默认 true） |
| include_cases | "案例 / case / 客户故事" | true（白皮书类）|
| language | --lang or 检测 | zh-CN |

### 阶段 4：ContentRequest JSON 结构化

输出标准化 JSON，供 M2-M5 共享：

```json
{
  "$schema": "content-request-v1",
  "id": "cr-20260827-1502",
  "generated_at": "2026-08-27T15:02:00+08:00",
  "raw_input": "基于 VulnHunter 漏洞猎人产品，写一篇面向企业安全负责人的解决方案白皮书，突出沙箱能力，面向中大型政企客户，风格正式专业，8000 字左右",
  "style": {
    "id": "solution-whitepaper",
    "name": "产品解决方案白皮书"
  },
  "topic": "VulnHunter 漏洞猎人产品解决方案",
  "topic_slug": "vulnhunter-solution",
  "project": {
    "linked": false,
    "path": null,
    "id": null,
    "notes": "无关联项目 ID，可考虑关联现有 PM/SA 项目"
  },
  "audience": {
    "primary": "企业安全负责人",
    "secondary": "中大型政企客户"
  },
  "length": {
    "value": 8000,
    "unit": "字"
  },
  "tone": ["正式", "专业"],
  "emphasis": ["沙箱能力"],
  "forbidden": [],
  "format_out": "markdown",
  "include_mermaid": true,
  "include_cases": true,
  "language": "zh-CN",
  "ambiguity": {
    "level": "low",
    "unresolved": []
  },
  "next_step": "如需关联现有项目产物，请补 --project；否则 /content-materials 会自动跳过"
}
```

## Harness 卡点

**解析后 gate**：AskUserQuestion 展示：
```
【M1 网关解析完成】
  文体：{style.name}
  受众：{audience.primary}
  篇幅：{length.value} {length.unit}
  风格：{tone}
  重点：{emphasis}
  项目关联：{project.path 或 "无"}
  输出格式：{format_out}

请选择：
(1) 通过 → 进入 M2 素材抽取（或跳过如无项目关联）
(2) 修改参数 → 我修改后按回车
(3) 中止
```

## 输出目录

```
./output/content-pipeline/{style-id}-{topic-slug}-{yyyymmdd}/
├── 00-content-request.json      ← 【本命令产出】ContentRequest 标准对象
├── 00-raw-input.txt              ← 原始自然语言输入备份
└── 00-intake-log.md              ← 解析日志（哪些字段抽取到，可信度）
```

## 与其他命令的边界

| 场景 | 用 |
|---|---|
| **一句话 → 标准化请求 JSON** | 本命令 |
| 用户直接给完整 JSON | 跳过本命令，直接调 M2 |
| 一键端到端 | `/content`（编排器，本命令是其内部第 1 步） |
| 需要重新解析（改文体或参数） | 本命令 `--refine` |

## 反模式

- ❌ 文体识别失败仍继续 —— 违规，必须明确 style
- ❌ 未标注可信度分级 —— 违规
- ❌ 项目关联时不校验目录存在 —— 会在 M2 崩
- ❌ 输出没写 ambiguity.level —— 违规
- ❌ 用未识别的默认值覆盖用户明确参数 —— 违规
