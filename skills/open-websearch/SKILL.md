---
name: open-websearch
description: >
  open-webSearch 多引擎免 API Key 联网搜索技能。覆盖 9 大搜索引擎（Bing/百度/CSDN/DuckDuckGo/
  Brave/掘金/Startpage/Sogou/Exa）、5 个站点正文抓取工具（CSDN/掘金/Linux.do/GitHub README/
  通用网页），含部署模式、MCP/HTTP 调用、引擎选择策略、环境变量、错误兜底、并发与限流最佳实践。
  触发词：web-search、open-websearch、多引擎搜索、免 API 搜索、MCP 搜索、网页抓取、
  fetchWebContent、CSDN 抓取、掘金抓取、GitHub README 抓取
user-invocable: false
effort: medium
---

# open-webSearch — 多引擎联网搜索技能

> 上游：[Aas-ee/open-webSearch](https://github.com/Aas-ee/open-webSearch)（Apache-2.0）
> 单一职责：把 open-webSearch 服务当作搜索/抓取后端，封装调用、路由与结果处理逻辑。
> 不做：本地资料 RAG（→ `ppt-rag-indexer`）、学术论文检索（→ `paper-collector`）、写报告（→ 调用方）。

## 一、部署模式与选择

| 模式 | 命令 | 适用 | 注意 |
|------|------|------|------|
| NPX 一次性 | `npx open-websearch@latest` | 临时联调 | 不持久化 |
| MCP stdio | 客户端配置 stdio + npx | Claude Desktop / Cursor | 仅 MCP 客户端可用 |
| HTTP/SSE | `MODE=http npx open-websearch@latest` | Web/HTTP 调用 | 默认 `:3000` |
| 守护进程 | `open-websearch serve` / `status` | 多客户端共享 | 单实例 |
| Docker | `docker run -d -p 3000:3000 ghcr.io/aas-ee/open-web-search:latest` | 长期运行 | 推荐生产 |
| 本地 build | `npm install && npm run build` | 二开调试 | — |

### MCP 客户端配置（HTTP/SSE）

```json
{
  "mcpServers": {
    "web-search": {
      "type": "streamableHttp",
      "url": "http://localhost:3000/mcp"
    }
  }
}
```

### MCP 客户端配置（stdio）

```json
{
  "mcpServers": {
    "web-search": {
      "command": "npx",
      "args": ["open-websearch@latest"],
      "env": { "MODE": "stdio", "DEFAULT_SEARCH_ENGINE": "bing" }
    }
  }
}
```

## 二、HTTP API 速查

| 方法 | 路径 | 用途 |
|------|------|------|
| GET | `/health` | 健康检查 |
| POST | `/search` | 多引擎搜索 |
| POST | `/fetch-web-content` | 通用网页正文抓取 |
| POST | `/fetch-csdn-article` | CSDN 文章正文 |
| POST | `/fetch-juejin-article` | 掘金文章正文 |
| POST | `/fetch-linuxdo-article` | linux.do 帖子正文 |
| POST | `/fetch-github-readme` | GitHub 仓库 README |

```bash
# 健康检查
curl -s http://localhost:3000/health

# 搜索
curl -s -X POST http://localhost:3000/search \
  -H "Content-Type: application/json" \
  -d '{"query":"MCP server","limit":5,"engines":["bing","duckduckgo"]}'

# 通用网页抓取
curl -s -X POST http://localhost:3000/fetch-web-content \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com/post","maxChars":30000}'
```

## 三、MCP 工具清单

### 1. `search` — 多引擎搜索

```json
{
  "query": "搜索关键词",
  "limit": 10,
  "engines": ["bing", "duckduckgo", "brave"],
  "searchMode": "auto"
}
```

返回数组：`{title, url, description, source, engine}`。

### 2. `fetchWebContent` — 通用网页

```json
{ "url": "https://...", "maxChars": 30000 }
```

返回：`{url, finalUrl, contentType, title, truncated, content}`。

### 3. `fetchCsdnArticle` — CSDN

```json
{ "url": "https://blog.csdn.net/.../article/details/xxxxx" }
```

返回：`{content}`（去除评论区与广告）。

### 4. `fetchJuejinArticle` — 掘金

```json
{ "url": "https://juejin.cn/post/{id}" }
```

### 5. `fetchLinuxDoArticle` — linux.do

```json
{ "url": "https://linux.do/t/topic/xxx" }
```

### 6. `fetchGithubReadme` — GitHub README

```json
{ "url": "https://github.com/owner/repo" }
```

支持 HTTPS、`.git`、SSH、带 query 的 URL。

## 四、引擎选择策略

```
内容类型 → 推荐引擎组合（按优先级）：

通用英文技术 → bing + duckduckgo + brave + startpage
通用中文资讯 → bing + baidu + sogou
中文技术博客 → csdn + juejin + sogou + baidu
微信公众号   → sogou（"微信"标识结果）
开源仓库     → bing + duckduckgo + brave（搜 github.com）
学术论文     → exa（语义） + bing
新闻时效     → bing + duckduckgo + brave（按时间排序）
反审查/隐私   → duckduckgo + brave + startpage
```

### 语言偏好映射

| `--lang` | 推荐引擎 |
|----------|---------|
| `zh` | `bing,baidu,csdn,juejin,sogou` |
| `en` | `bing,duckduckgo,brave,startpage,exa` |
| `all` | `bing,duckduckgo,brave`（再视情况扩展） |

## 五、searchMode 策略

| 模式 | 含义 | 何时用 |
|------|------|--------|
| `request` | 纯 HTTP 抓取 | 速度优先，结果稳定的引擎 |
| `auto` | 失败时回退 | 推荐默认 |
| `playwright` | 浏览器渲染（仅 Bing） | Bing 被反爬 + 已安装 Playwright |

> Playwright 不再随包默认安装，需自备：`PLAYWRIGHT_PACKAGE` / `PLAYWRIGHT_EXECUTABLE_PATH` / `PLAYWRIGHT_CDP_ENDPOINT`。

## 六、环境变量速查

| 变量 | 默认值 | 作用 |
|------|--------|------|
| `MODE` | `both` | `both` / `http` / `stdio` |
| `PORT` | `3000` | HTTP 端口 |
| `DEFAULT_SEARCH_ENGINE` | `bing` | 默认引擎 |
| `ALLOWED_SEARCH_ENGINES` | 空 | 引擎白名单（逗号分隔） |
| `ENABLE_CORS` | `false` | CORS 开关 |
| `CORS_ORIGIN` | `*` | CORS Origin |
| `USE_PROXY` | `false` | 启用 HTTP 代理 |
| `PROXY_URL` | `http://127.0.0.1:7890` | 代理地址 |
| `FAKE_IP_CIDRS` | 空 | Clash fake-IP 段 |
| `FETCH_WEB_INSECURE_TLS` | `false` | 跳过 TLS 校验 |
| `SEARCH_MODE` | `auto` | `request` / `auto` / `playwright` |
| `PLAYWRIGHT_HEADLESS` | `true` | 无头模式 |
| `PLAYWRIGHT_NAVIGATION_TIMEOUT_MS` | `20000` | 导航超时 |
| `MCP_TOOL_*_NAME` | — | 重命名 MCP 工具 |

## 七、调用工作流

### 工作流 A：单次搜索

```
1. 健康检查：GET /health（fail → 提示启动）
2. 调用 search（HTTP 或 MCP）
3. 按 URL 规范化去重（移除 query 跟踪参数）
4. 标注每条来源引擎，输出标准结构
```

### 工作流 B：搜索 + 正文抓取

```
1. search 获取 Top-N 候选
2. 按域名路由抓取工具：
   *.csdn.net          → fetchCsdnArticle
   juejin.cn/post/*    → fetchJuejinArticle
   github.com/owner/repo  → fetchGithubReadme
   linux.do/t/*        → fetchLinuxDoArticle
   其他                → fetchWebContent
3. 并发抓取（建议 ≤ 3 并发，避开引擎限流）
4. 失败重试 1 次后跳过，记录原因
5. 每条正文截断至 30000 字符（默认）
```

### 工作流 C：多轮聚合研究

```
Round 1: 宽口径搜索 → 提取关键概念
Round 2: 围绕关键概念再搜 → 抓取深度内容
Round 3: 跨源交叉验证（同一事实 ≥ 2 来源）
Round 4: 综合输出（共识 / 分歧 / 待验证）
```

## 八、并发与限流

```
并发上限：
  - search 调用：≤ 5 并发（按引擎拆分）
  - fetch* 调用：≤ 3 并发（避免被反爬）

限流回退：
  - 收到 429 → 切换引擎 + 等待 5s
  - 收到 403 → 启用 --proxy
  - 同一域名连续失败 ≥ 3 次 → 降级到通用 fetchWebContent
```

## 九、错误兜底

| 错误码 / 现象 | 根因 | 兜底 |
|---------------|------|------|
| `ECONNREFUSED` | 服务未启动 | 提示 npx/docker/serve 命令 |
| `MODULE_NOT_FOUND playwright` | 未装 Playwright | 改用 `searchMode=request` |
| `Empty results` | 词太窄或被拦截 | 换引擎 / 加同义词 / Playwright 回退 |
| `Captcha required` | 触发验证码 | 切换引擎 + 加代理 |
| `Invalid URL` | 抓取 URL 格式错 | 用通用 `fetchWebContent` |
| `Content truncated` | 超过 `maxChars` | 调大 `maxChars` 至 200000 |

## 十、结果质量基准

```
完整搜索 query（10 条 limit）应满足：
  ├── 引擎覆盖：≥ 2 个不同引擎
  ├── 去重后唯一 URL：≥ 60%
  ├── 标题非空率：100%
  ├── 描述非空率：≥ 80%
  └── 来源域名分布：≥ 4 个不同域名

正文抓取（5 篇）应满足：
  ├── 抓取成功率：≥ 80%
  ├── 平均正文长度：≥ 800 字符
  └── 标题与 URL 一一对应
```

## 十一、典型用法片段（伪代码）

```ts
// 健康检查
const ok = await fetch(`${server}/health`).then(r => r.ok).catch(() => false);
if (!ok) throw new Error('open-websearch service not running');

// 搜索
const results = await fetch(`${server}/search`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ query, limit, engines, searchMode: 'auto' })
}).then(r => r.json());

// 按域名路由抓取
function pickFetcher(url: string): string {
  const u = new URL(url);
  if (u.hostname.endsWith('csdn.net'))   return '/fetch-csdn-article';
  if (u.hostname === 'juejin.cn')        return '/fetch-juejin-article';
  if (u.hostname === 'linux.do')         return '/fetch-linuxdo-article';
  if (u.hostname === 'github.com')       return '/fetch-github-readme';
  return '/fetch-web-content';
}
```

## 十二、与其他技能的边界

| 任务 | 用本技能？ | 替代 |
|------|-----------|------|
| arxiv 论文检索 | 否 | `paper-collector` |
| 本地资料 RAG | 否 | `ppt-rag-indexer` |
| 通用联网搜索 | **是** | — |
| 中文技术博客抓取 | **是** | — |
| GitHub README 抓取 | **是** | — |
| 学术论文 PDF 解读 | 否 | `paper-interpreter` |
| 横纵分析方法论 | 否 | `hv-analysis` |

## 十三、安全与合规

- 默认无 API Key，但仍受目标引擎服务条款约束
- 商业用途请遵守各引擎 ToS
- 代理 / fake-IP 仅用于合法绕过区域限制
- 不要将抓取结果二次分发为公开数据集（版权风险）
- 高频请求务必加 sleep 间隔，避免 IP 被封
