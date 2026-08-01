---
name: market-research
description: >
  市场研究与竞争情报分析，支持竞品分析、行业趋势、市场规模估算、亚马逊选品研究。
  
  与相邻命令的边界（防混淆）：
  - vs /user-research：本命令做"市场视角（竞品 + 趋势 + TAM）"；
    /user-research 做"用户视角（行为 + 动机 + JTBD）"。两者互补不重复。
  - vs /product-strategy --mode lean：本命令产出"市场情报数据"；
    /product-strategy 接收数据后做"战略画布"决策。
user-invocable: true
argument-hint: "<研究主题> [--mode competitive|trend|tam|amazon|oss] [--output brief|report|matrix]"
allowed-tools: [Read, Write, Edit, Grep, Glob, AskUserQuestion]
harness:
  execute:
    preset: research
  constrain:
    profile: writing-safe
    gates: [before-write]
  loop:
    mode: parallel
    fanout: 3
  memory:
    scope: project
    reads: [project-context]
  security:
    danger-level: low
---

# /market-research — 竞争情报 & 市场研究

加载技能：`skills/research/market-research/SKILL.md`

## 触发条件
需要进行竞品分析、市场机会评估、行业趋势研究、开源生态分析或亚马逊选品研究时。

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `<研究主题>` | 市场/产品/行业/关键词（必填） | — |
| `--mode` | 研究模式 | `competitive` |
| `--output` | 输出格式 | `report` |

### 研究模式
| `--mode` | 内容 | 适用场景 |
|----------|------|---------|
| `competitive` | 竞品全景：功能矩阵 + 定价 + 优劣势对比 | 立项评估、竞品监测 |
| `trend` | 行业趋势：技术趋势 + 市场信号 + 预测 | 战略规划、融资 BP |
| `tam` | 市场规模：TAM/SAM/SOM 估算 | 融资材料、商业计划书 |
| `amazon` | 亚马逊选品：销量/评分/关键词/竞争度 | 跨境电商选品 |
| `oss` | 开源生态：Star 趋势 + 社区活跃度 + 商业化（powered by ossinsight） | 技术选型、投资研究 |
| `deepresearch` | Deep Research 竞品报告：多源搜索聚合 + PDF（powered by competitor-analysis） | 快速出竞品深度报告 |
| `crawl` | 爬虫竞品分析：官网抓取 + LLM分类 + 词云 + 对比（powered by Comperator） | 深挖竞品官网信息 |

## 参考工具生态

| 工具 | 用途 | GitHub |
|------|------|--------|
| competitive-intelligence-cli | 竞争情报命令行工具 | qb-harshit/competitve-intelligence-cli |
| rag-market-research | RAG 驱动市场研究 | ahmedtrb/rag-solution-for-market-research |
| amazon-sorftime-research | 亚马逊选品 MCP Skill | liangdabiao/amazon-sorftime-research-MCP-skill |
| ossinsight | 开源项目洞察平台（100亿+GitHub事件，AI生态排名+自然语言查询） | pingcap/ossinsight |
| competitor-analysis | Deep Research 竞品报告生成器（Valyu API，实时进度+PDF导出） | unicodeveloper/competitor-analysis |
| Comperator | 爬虫+LLM全流程竞品分析（网站抓取→分类→摘要→词云→对比） | Procycons/Comperator |
| OpenStock | 开放股票数据分析 | Open-Dev-Society/OpenStock |
| founder-discovery | 创始人/公司发现工具 | ORBWEVA/founder-discovery |

### 竞品分析工具选型指南

| 场景 | 推荐工具 | 理由 |
|------|---------|------|
| 快速生成竞品报告（一键PDF） | `competitor-analysis` | Valyu Deep Research API 多源聚合，5分钟出报告，带实时进度条 |
| 深度爬取竞品官网内容 | `Comperator` | 自动爬取→LLM分类→词云可视化→产品特性对比，完全离线可控 |
| 开源项目 Star/贡献者/趋势对比 | `ossinsight` | 100亿+行 GitHub 事件数据，支持自然语言查询生成 SQL，AI agent 生态排名实时更新 |
| 命令行批量竞品情报 | `competitive-intelligence-cli` | CI/CD 友好，可集成到自动化流水线 |

## 执行流程

```
Step 1: 研究范围界定
  → 确认研究对象（产品/市场/行业/地区）
  → 识别关键竞争维度
  → 选择数据来源策略

Step 2: 竞品收集（competitive 模式）
  → 直接竞品（同类产品）
  → 间接竞品（替代方案）
  → 潜在竞品（进入者）

Step 3: 维度分析
  → 产品功能矩阵对比
  → 定价策略分析
  → 目标客户 & 市场定位
  → 增长策略 & 渠道

Step 4: 洞察提炼
  → 市场空白点识别
  → 差异化机会
  → 威胁与风险

Step 5: 战略建议
  → 竞争应对策略
  → 机会优先级排序
  → 监测指标推荐
```

## 输出结构（report 模式）

```markdown
# [主题] 市场研究报告

## 执行摘要
- 核心发现（3-5条）
- 战略建议

## 市场概览
- 市场规模与增速
- 关键驱动因素
- 主要玩家格局

## 竞品分析矩阵
| 竞品 | 核心功能 | 定价 | 目标客户 | 优势 | 劣势 |
|------|---------|------|---------|------|------|

## 差异化机会
- 未被满足的需求
- 可切入的细分市场

## 威胁与风险
- 竞争态势变化
- 技术替代风险

## 监测建议
- 关键信号清单
- 下次更新时间点
```

## OSS 生态分析（ossinsight）

使用 [ossinsight.io](https://ossinsight.io) 进行开源项目竞品分析：

```
分析维度：
- Star 增速趋势（日/周/月粒度）
- 贡献者数量 & 地域分布 & 公司构成
- Fork / Issue / PR 活跃度对比
- AI 生态专项排名：Agent Frameworks / Coding Agents / MCP Tools
- 自然语言查询 → SQL → 可视化（Data Explorer）

查询示例（ossinsight Data Explorer）：
  "Compare star growth of langchain vs llamaindex in 2025"
  "Which companies contribute most to kubernetes?"
  "Show monthly PR merge rate for pytorch vs tensorflow"

重点集合：
  collections/ai-agent-frameworks  → LangChain/CrewAI/AutoGen 等50+框架排名
  collections/ai-coding-assistant  → Claude Code/Copilot/Cursor/Aider 趋势
  collections/model-context-protocol → MCP 生态追踪
```

## Deep Research 竞品报告（competitor-analysis）

基于 Valyu Deep Research API 的全自动竞品深度报告，适合快速出报告：

```
输入：竞品官网 URL + 背景描述
输出：Markdown 报告 + PDF（可选 fast/standard/heavy 三档深度）

报告结构：
  - 公司概览（规模/融资/发展历程）
  - 核心产品与功能矩阵
  - 市场定位与差异化优势
  - 近期动态（新功能/公告/舆情）
  - 可验证来源引用

深度档位：
  fast    → ~5分钟，日常监测
  standard → 10-20分钟，立项评估
  heavy   → 最长90分钟，战略决策

实时进度：步骤追踪 + 进度条 + 即时结果流式输出
```

## 爬虫竞品分析（Comperator）

基于 Python/Streamlit 的本地化全流程竞品分析管道：

```
Pipeline：
  Step 1: 爬取竞品官网（BeautifulSoup，多域名多起始URL）
  Step 2: LLM内容分类（按预定义类别：功能/定价/目标用户等）
  Step 3: LLM摘要生成（压缩提炼核心内容）
  Step 4: 词云可视化（高频词直观呈现竞品侧重）
  Step 5: 对比分析（你的产品 vs 竞品，LLM生成差异洞察）

配置示例（config.yaml）：
  competitors:
    - name: "CompetitorA"
      allowed_domains: ["competitora.com"]
      start_urls: ["https://competitora.com"]
  product:
    name: "我们的产品"
    description: "产品核心价值描述"

适用场景：对竞品官网有深度爬取需求、需离线分析、或需定制分类维度时
```

## 使用示例

```
/market-research AI 写作工具市场
/market-research Notion 竞品分析 --mode competitive
/market-research 中国 SaaS 市场 2025 趋势 --mode trend
/market-research 降噪耳机亚马逊选品 --mode amazon
/market-research vercel vs netlify --mode competitive --output matrix
/market-research GitHub Copilot 开源生态 --mode oss
/market-research langchain vs crewai star趋势对比 --mode oss
/market-research Figma 竞品深度报告 --mode deepresearch
/market-research 爬取分析 linear.app 产品内容 --mode crawl
```
