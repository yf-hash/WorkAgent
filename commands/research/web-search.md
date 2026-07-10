---
name: web-search
user-invocable: true
allowed-tools: WebSearch, WebFetch, Bash, Read, Write, AskUserQuestion, Skill
description: 基于 open-webSearch 的多引擎免 API Key 联网搜索 — 跨 Bing/百度/CSDN/DuckDuckGo/Brave/掘金/Sogou 并行检索，支持结构化结果聚合与正文抓取
argument-hint: "<query> [--engines <列表>] [--limit <n>] [--mode search|fetch|research] [--fetch] [--url <url>] [--server <地址>] [--proxy <url>] [--lang zh|en|all] [--output <路径>]"
---

# /web-search

基于 [open-webSearch](https://github.com/Aas-ee/open-webSearch) 的多引擎联网搜索命令，无需 API Key，自部署本地 MCP/HTTP 服务后即可跨 9 大搜索引擎并行检索，并支持对常见技术站点（CSDN、掘金、GitHub README、Linux.do）的正文抓取。

加载技能：`skills/open-websearch/SKILL.md`

## 用法

```
/web-search "RAG 检索增强生成 最佳实践"
/web-search "MCP server 开发" --engines bing,duckduckgo,brave --limit 5
/web-search "Claude Code hooks" --mode research --fetch --limit 3
/web-search --mode fetch --url https://juejin.cn/post/7xxxxxxxxx
/web-search "AI Agent 长任务自治" --lang en --output workspace/research/agent.md
/web-search "open-websearch" --server http://localhost:3000 --proxy http://127.0.0.1:7890
```

## 参数说明

### 公共参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `<query>` | 搜索关键词或问题（mode=fetch 时可省略） | — |
| `--mode <模式>` | `search`（仅搜索）/ `fetch`（仅抓取正文）/ `research`（搜索+抓正文聚合） | `search` |
| `--server <url>` | open-webSearch 服务地址（MCP/HTTP 二合一） | `http://localhost:3000` |
| `--output <路径>` | 结果保存到 Markdown 文件 | — |

### 搜索参数（mode=search 或 research）

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--engines <列表>` | 引擎逗号分隔（见下表） | `bing,duckduckgo,brave` |
| `--limit <n>` | 每引擎返回结果数 | `10` |
| `--lang <语言>` | `zh`（中文站为主）/ `en`（英文站为主）/ `all` | `all` |
| `--searchMode <模式>` | `request`（HTTP）/ `auto`（自动回退）/ `playwright`（仅 Bing） | `auto` |

### 抓取参数（mode=fetch 或 research）

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--url <url>` | 指定要抓取的页面 URL（mode=fetch 必填） | — |
| `--fetch` | research 模式下抓取前 N 条结果的正文 | — |
| `--max-chars <n>` | 通用网页抓取最大字符数（1000–200000） | `30000` |

### 网络与代理

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--proxy <url>` | HTTP 代理地址 | — |
| `--insecure-tls` | 跳过 TLS 校验（仅在受信任内网使用） | `false` |

## 支持的搜索引擎（--engines）

| 引擎 ID | 适用场景 | 语言 |
|---------|---------|------|
| `bing` | 通用搜索，综合质量高 | zh/en |
| `duckduckgo` | 隐私优先，英文技术内容 | en 优先 |
| `brave` | 隐私优先，质量稳定 | en 优先 |
| `startpage` | Google 结果代理，无追踪 | en 优先 |
| `baidu` | 中文资讯、政策、本地化 | zh |
| `sogou` | 微信公众号文章入口 | zh |
| `csdn` | 中文技术博客、报错解决方案 | zh |
| `juejin` | 掘金前端/后端技术文章 | zh |
| `exa` | 语义搜索（神经搜索） | en/zh |

> 注：`linux.do` 暂不支持搜索接口（但保留正文抓取）

## 模式说明

### search 模式（默认）— 多引擎检索

```
Step 1: 解析 query / engines / limit
Step 2: 健康检查 → GET {server}/health（若不通则提示用户启动服务）
Step 3: 并行调用 POST {server}/search 或 MCP search 工具
Step 4: 按引擎归并，去重（基于 URL 规范化）
Step 5: 输出结构化列表（标题/URL/摘要/来源/引擎）
```

### fetch 模式 — 单页正文抓取

```
路由规则（按 URL 域名自动选择工具）：
  *.csdn.net          → fetchCsdnArticle
  juejin.cn/post/*    → fetchJuejinArticle
  github.com/*        → fetchGithubReadme（仓库根 URL）
  linux.do/t/*        → fetchLinuxDoArticle
  其他                → fetchWebContent（通用，按 --max-chars 截断）
```

### research 模式 — 搜索+抓正文聚合

```
Step 1: search 模式获取候选列表
Step 2: 取前 --limit 条，按 URL 域名路由到对应 fetch 工具
Step 3: 抽取正文要点（每条 200-400 字摘要 + 关键引用）
Step 4: 输出聚合报告（搜索结果索引 + 各页面深度摘要）
```

## 执行前置：服务可用性检查

命令执行前自动按以下顺序检测：

```
1) GET <server>/health  → 服务存活
2) 若失败，按以下优先级建议启动：
   a. NPX 一键启动：
      npx open-websearch@latest
   b. 已配置 MCP，直接走 stdio
   c. Docker：
      docker run -d --name web-search -p 3000:3000 ghcr.io/aas-ee/open-web-search:latest
   d. 守护进程：
      open-websearch serve
3) 用户确认后再继续
```

## 输出格式

### search 模式

```markdown
# Web Search 结果

**查询**：[原始 query]
**引擎**：bing, duckduckgo, brave
**总数**：N 条（去重前 M 条）
**时间**：YYYY-MM-DD HH:MM

---

## 1. [标题]
- URL：https://example.com/article
- 来源：example.com（bing）
- 摘要：[原始描述]

## 2. ...
```

### research 模式

```markdown
# Web Research：[query]

## 检索概览
- 引擎：[列表]
- 候选：N 条 → 抓取 K 条
- 时间：YYYY-MM-DD HH:MM

## 候选索引
| # | 标题 | 来源 | 引擎 | URL |
|---|------|------|------|-----|

## 深度摘要

### 1. [标题]
- **来源**：[域名]
- **核心观点**：[200-400 字]
- **关键引用**：> "..."
- **原文**：[URL]

---

## 综合洞察
- 共识：...
- 分歧：...
- 待验证：...
```

## 错误处理

| 错误 | 原因 | 处理 |
|------|------|------|
| `ECONNREFUSED` | 服务未启动 | 提示启动命令 |
| `429 Too Many Requests` | 引擎限流 | 切换引擎或加 `--proxy` |
| `403 Forbidden` | 区域限制 | 使用 `--proxy` |
| `Empty results` | 关键词太窄或被引擎拦截 | 切引擎、扩词、回退 `auto`→`playwright` |
| `TLS verify failed` | 自签证书 | 内网可加 `--insecure-tls` |

## 与其他命令的协同

- `/paper-collect`：学术论文（arxiv）专用，本命令补充通用网页面
- `/hv-analysis`：横纵分析，调用本命令做横向竞品/资讯采集
- `/paper-interpret`：单篇深读，与 research 模式的深度摘要互补

## 关联 Skills 与 Agents

- Skill：`open-websearch` — open-webSearch 全部工具与运维知识
- Agent：`web-search-analyst` — 自治多轮检索 + 信息综合
- 上游项目：<https://github.com/Aas-ee/open-webSearch>（Apache-2.0）
