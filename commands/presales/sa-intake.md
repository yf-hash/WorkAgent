---
name: sa-intake
description: 【模块 1】多源客户输入网关 — 接收销售聊天文本、客户访谈转写、RFP/招标 PDF、客户 PPT、Excel 需求清单 等杂乱输入，清洗信息、提取客户元信息（行业/规模/预算/时间/合规/干系人）、标记需求模糊等级，输出标准化项目对象 JSON。流水线起点。
user-invocable: true
argument-hint: "<原始输入：一句话 or 文件路径 or 混合> [--client <名称>] [--industry <行业>] [--source <sales|rfp|interview|ppt|excel>] [--out <path>]"
allowed-tools: [Read, Write, Edit, AskUserQuestion, Grep, Glob, Bash]
model: sonnet  # 轻量：输入清洗 + 元信息抽取，无需 opus
harness:
  execute:
    preset: writing-scoped
    tools: [Bash]  # extend: 从 PDF / PPT / Excel 提取文本
  constrain:
    profile: writing-safe
    gates: [before-write, after-metadata-extract]
  loop:
    mode: pipeline
    stages: [清洗, 元信息抽取, 模糊等级标记, 输出结构化对象]
  memory:
    scope: project
    reads: [project-context]
    writes: [intake-history]
  security:
    danger-level: low
---

# /sa-intake — 多源客户输入网关（Module 1）

> **端到端 7 模块流水线的起点**
>
> 【本命令】→ /sa-clarify → /sa-solution-map → /sa-architect → /sa-poc/impl/rfp → /sa-quote → /sa-archive

## 一句话

**接收销售转述、RFP、访谈录音转写、客户 PPT、Excel 需求等任意杂乱输入 → 输出结构化的《客户项目元数据 JSON》**，供整个流水线共享。

## 输入

```bash
# 一句话客户信息
/sa-intake "某制造业客户，现有老 MES 要替换，私有化 + 国产化，3 个月上线" --client "远大制造"

# 一个 RFP 文件
/sa-intake ./rfp/2026-政务云-RFP.pdf --source rfp

# 混合：一句话 + 补充材料
/sa-intake "客户是某城商行" --with ./ppt/客户现状.pptx,./excel/需求清单.xlsx --client "杭州银行"

# 全部文件放同一目录
/sa-intake ./client-materials/ --client "远大制造" --industry manufacturing
```

## 支持的输入类型

| 类型 | 扩展名 / 特征 | 解析方式 |
|---|---|---|
| 销售转述文本 | 直接一句话 or `.txt` | 文本清洗 |
| 客户访谈录音转写 | `.txt` / `.md`（转写后） | 对话解析 + 说话人分离 |
| RFP / 招标文件 | `.pdf` / `.docx` | PDF 解析 + 条款识别 |
| 客户现状 PPT | `.pptx` | 页面文本提取 + 结构化 |
| Excel 需求清单 | `.xlsx` / `.csv` | 表格解析 |
| 问卷 / 调研 | `.pdf` / `.xlsx` | 表单解析 |

## 内部四个阶段

### 阶段 1：非结构化清洗

- 过滤寒暄客套（"您好、感谢关注、期待合作"等）
- 保留业务现状 / 诉求 / 约束 / 顾虑 的实质表述
- 分类打标签：现状 / 诉求 / 约束 / 疑问 / 竞争 / 预算 / 时间

### 阶段 2：元信息抽取（12 类）

调用 `skills/sa/sa-input-gateway` 提供的实体抽取规则：

| # | 字段 | 来源举例 |
|---|---|---|
| 1 | 客户名称 | "某制造业客户" / RFP 抬头 |
| 2 | 所属行业 | 政企 / 制造 / 金融 / 互联网 / 零售 / 医疗 / 教育 |
| 3 | 客户规模 | 用户数 / 员工数 / 营收 / 城市数 |
| 4 | 项目阶段 | 线索 / 意向 / POC / 投标 / 合同 |
| 5 | 现有 IT 栈 | 老系统名 / 数据库 / 云 / 语言栈 |
| 6 | 显性诉求 | "要替换 X" / "支持 Y" |
| 7 | 已知痛点 | "现在很慢" / "统计口径不一" |
| 8 | 合规约束 | 等保 / 国产化 / 信创 / GDPR / 数据不出域 |
| 9 | 预算线索 | 具体金额 / 档位 / 无线索 |
| 10 | 期望上线时间 | 明确日期 / 相对（3 个月）/ 无 |
| 11 | 关键干系人 | 决策人 / 影响人 / 使用人 + 部门 |
| 12 | 竞争对手 | 客户提及 / 招标邀请名单 |

### 阶段 3：需求模糊等级标记

依据抽取结果的完整度打标：

| 等级 | 判定标准 | 下一步建议 |
|---|---|---|
| 🔴 高度模糊 | 缺失 ≥ 6 个关键字段 / 只有一句话 | 强烈建议 `/sa-clarify --mode human` |
| 🟠 部分明确 | 缺失 3-5 个 / 有基本背景 | `/sa-clarify --mode mixed` |
| 🟢 RFP 明确 | 有完整 RFP + 大部分字段可抽取 | `/sa-clarify --mode auto` |

### 阶段 4：输出结构化 JSON

```json
{
  "$schema": "sa-intake-v1",
  "project_id": "mfg-mes-20260827",
  "generated_at": "2026-08-27T15:00:00+08:00",
  "source": "sales",
  "raw_input_summary": "某制造业客户，现有老 MES 要替换，私有化+国产化，3 个月上线",
  "client": {
    "name": "远大制造",
    "industry": "manufacturing",
    "sub_industry": "机械制造",
    "scale": {
      "users_estimated": null,
      "employees": null,
      "revenue": null,
      "notes": "未提供"
    },
    "existing_it": ["老 MES（品牌未知）"],
    "stakeholders": []
  },
  "project": {
    "stage": "线索",
    "timeline": {
      "target_go_live": "3m",
      "hard_deadline": null
    },
    "budget": null,
    "competitors": []
  },
  "requirements": {
    "explicit": ["替换老 MES"],
    "pain_points": [],
    "constraints": ["私有化部署", "国产化"],
    "compliance": ["国产化"],
    "excluded": []
  },
  "ambiguity": {
    "level": "high",
    "missing_fields": ["用户规模", "预算", "现有系统品牌", "干系人", "具体痛点", "现有集成"],
    "notes": "客户规模、预算、具体痛点全部缺失，强烈建议进入调研澄清"
  },
  "next_step": "推荐执行 /sa-clarify --mode human"
}
```

## Harness 卡点

- **抽取后 gate**：AskUserQuestion 展示：
  ```
  【M1 输入网关完成】客户项目元数据已生成：
    - 客户：{name}
    - 行业：{industry}
    - 模糊等级：{level}（缺失 {n} 个关键字段）
    - 关键约束：{constraints}

  请选择：
  (1) 通过 → 进入 M2 调研澄清
  (2) 补充字段 → 我人工补几个字段再继续
  (3) 重新解析 → 换个 --source 类型或补文件
  ```

## 输出目录约定

```
./output/sa-pipeline/{client}-{project}-{yyyymmdd}/
├── 00-intake.json               ← 【本命令产出】
├── 00-raw-materials/            ← 原始文件的软链接或副本（可选）
│   ├── rfp.pdf
│   ├── 客户现状.pptx
│   └── 需求清单.xlsx
└── 00-intake-log.md              ← 解析日志（哪些字段被抽取到、置信度）
```

## 与其他命令的边界

| 场景 | 用 |
|---|---|
| **杂乱输入 → 结构化项目对象** | 本命令 |
| 结构化后需要出调研报告 | 下一步 `/sa-clarify` |
| 只想读一份 RFP 的目录 | 本命令 `--source rfp` |
| 一句话直接跑到 RFP 应答 | `/sa-pipeline`（一键） |

## 反模式

- ❌ 模糊等级留空 —— 违规，必须打标
- ❌ 假设客户合规要求 —— 违规，必须显式标"未提供 / 假设待确认"
- ❌ 从原始输入编造事实（如"客户预算 200 万"，原文没说） —— 违规
- ❌ 未产出 JSON 只出 Markdown —— 违规，下游依赖 JSON
