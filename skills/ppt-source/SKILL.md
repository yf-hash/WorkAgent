---
name: ppt-source
description: >
  PPT内容素材获取技能（合并自 ppt-rag + ppt-researcher）。
  支持三种模式：--mode rag（已有材料索引，本地文件/URL向量化检索）、
  --mode research（多源网络研究，官方/媒体/学术/产业/社区五大渠道）、
  --mode combined（RAG打底+联网补充空白章节）。
  输出与 Phase 3-9 直接衔接的结构化素材包（outline + data + quotes + refs）。
  触发词：PPT研究、内容搜集、资料调研、本地文档索引、RAG、已有材料、
  --rag参数、多源搜索、PPT素材、ppt-rag、ppt-researcher
user-invocable: false
effort: high
argument-hint: "[--mode rag|research|combined] [--rag <文件/URL>...] [--rag-dir <目录>] [--rag-index <名称>] [--rag-mode replace|supplement] [--rag-top-k <n>] [--rag-list] [--rag-backend chroma|faiss|bm25|auto]"
---

# PPT Source — 内容素材获取技能

PPT 全流程 Phase 2 内容素材获取模块，支持三种工作模式：

| 模式 | 输入 | 适用场景 |
|------|------|----------|
| `--mode rag` | 本地文件 / 在线URL | 已有内部资料、报告、数据 |
| `--mode research` | PPT主题关键词 | 从零开始，需要联网收集 |
| `--mode combined` | 本地文件 + 联网 | RAG打底，自动补充覆盖薄弱章节 |

两种模式输出**完全相同的素材包格式**，可直接衔接 Phase 3-9 制作 PPT。

---

# 模式一：RAG — 已有材料索引与检索

将用户提供的**本地文件**或**线上URL**构建可检索知识库，
按PPT主题语义检索最相关内容，输出结构化素材包。

## 支持的输入格式

### 本地文件
| 格式 | 解析工具 | 说明 |
|------|---------|------|
| `.pdf` | PyMuPDF / markitdown | 含图表页描述、表格文字提取 |
| `.docx` | python-docx / markitdown | 保留标题层级 |
| `.pptx` | python-pptx | 提取每页文字+备注 |
| `.md` / `.txt` | 直接读取 | 保留Markdown结构 |
| `.html` | BeautifulSoup | 提取正文，去除导航/广告 |
| `.xlsx` / `.csv` | pandas | 表格数据转文字描述 |
| `.epub` | ebooklib | 电子书 |

### 线上URL
| 类型 | 处理方式 |
|------|---------|
| 单页文章 / 博客 | WebFetch抓取正文 |
| 在线PDF | 下载后按本地PDF处理 |
| 文档站点 (`/docs/`) | 递归抓取同域名子页面（深度≤2） |
| GitHub README | 抓取raw内容 |
| 学术论文页 (arXiv/DOI) | 抓取摘要+全文（如可访问） |
| YouTube / 视频 | 抓取字幕/描述文字 |
| 多个URL（换行分隔） | 批量并行抓取 |

### 目录扫描
```
--rag-dir <目录>    递归扫描目录，处理所有支持格式文件
                   自动跳过：.git/ node_modules/ __pycache__/
                   最大文件数：500（超出按修改时间取最新）
```

## RAG 核心流程

### Step 1: 文档摄入

```python
def ingest_sources(sources: list[str]) -> list[Document]:
    documents = []
    for src in sources:
        if src.startswith("http"):
            content = fetch_url(src)
            doc = Document(
                text=extract_main_content(content),
                metadata={"source": src, "type": "url", "title": extract_title(content)}
            )
        elif src.endswith(".pdf"):
            pages = pymupdf.open(src)
            for i, page in enumerate(pages):
                doc = Document(text=page.get_text(),
                               metadata={"source": src, "type": "pdf", "page": i+1})
        elif src.endswith(".pptx"):
            prs = Presentation(src)
            for i, slide in enumerate(prs.slides):
                doc = Document(text=extract_slide_text(slide),
                               metadata={"source": src, "type": "pptx", "slide": i+1})
        documents.append(doc)
    return documents
```

**摄入进度输出**：
```
[RAG摄入进度]
✅ report_2024.pdf        → 42页，已提取 18,234 字
✅ market_analysis.docx   → 23页，已提取 9,876 字
✅ https://example.com/blog/ai-trends → 已抓取，3,421 字
📊 共摄入 3 个来源，总计约 31,531 字
```

### Step 2: 规模判断与策略选择

```python
def choose_strategy(documents):
    total_chars = sum(len(d.text) for d in documents)
    total_docs = len(documents)
    if total_chars < 40_000 and total_docs <= 8:
        return "direct"       # 直接LLM处理（最准确）
    elif total_chars < 200_000:
        return "bm25"         # BM25关键词检索（快速）
    else:
        return "vector"       # 向量化+语义检索（大规模）
```

### Step 3: 分块

每块 500-800 tokens，重叠 10-15%，按文档类型调整：PDF按页、PPT每页一块、文章按段落递归分割。

### Step 4: 向量化与索引

```python
EMBEDDING_MODELS = [
    ("BAAI/bge-m3", "local", "sentence-transformers"),       # 首选：多语言
    ("text-embedding-3-small", "api", "openai"),              # 次选：OpenAI API
    ("BAAI/bge-small-zh-v1.5", "local", "sentence-transformers"),  # 兜底
    ("bm25", "local", "rank-bm25"),                          # 最后兜底
]
```

**索引持久化与复用**：
```
首次建立：--rag report.pdf --rag-index my_project
          → 索引保存到 .ppt_rag/my_project/
下次复用：--rag-index my_project（跳过重新摄入）
增量更新：--rag new_doc.pdf --rag-index my_project
查看索引：/ppt --rag-list
```

### Step 5: 主题驱动检索

为每个幻灯片章节单独检索（确保每部分都有对应素材）：

```python
def retrieve_for_ppt(store, ppt_topic, outline, top_k=5):
    results = {}
    results["overview"] = store.query([ppt_topic, f"{ppt_topic} 综述"], n_results=top_k)
    for section in outline:
        queries = generate_section_queries(section, ppt_topic)
        results[section.title] = deduplicate_and_rank(store.query(queries, n_results=top_k))
    return results
```

**检索质量优化**：余弦相似度>0.92去重、同源最多3片段、相似度<0.45丢弃、多源验证标注

### Step 6: 内容合成

将检索结果合成为与 `research` 模式相同格式的素材包，并输出覆盖度报告：

```
[RAG素材覆盖度]
✅ 第1章 背景与现状    → 找到 8 个相关片段
⚠️ 第3章 竞争格局      → 仅找到 2 个相关片段（覆盖较薄）
   建议：补充竞品分析文档，或开启 --rag-mode supplement 联网补充
总体覆盖率：82%
```

## RAG 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--rag <来源>` | 文件路径或URL（空格分隔多个）| — |
| `--rag-dir <目录>` | 递归索引整个目录 | — |
| `--rag-index <名称>` | 索引名称（持久化和复用）| 临时索引 |
| `--rag-mode replace\|supplement` | replace=仅RAG；supplement=RAG+联网补充 | `replace` |
| `--rag-top-k <n>` | 每章节检索片段数 | `5` |
| `--rag-list` | 列出已保存的持久化索引 | — |
| `--rag-backend chroma\|faiss\|bm25\|auto` | 向量存储后端 | `auto` |

## RAG 依赖

```bash
pip install PyMuPDF python-docx python-pptx markitdown beautifulsoup4 pandas
pip install chromadb           # 持久化向量存储（首选）
pip install faiss-cpu          # 内存向量存储（次选）
pip install rank-bm25          # 关键词检索（轻量）
pip install sentence-transformers  # 本地嵌入模型
```

---

# 模式二：Research — 多源网络研究

为 PPT 全流程生成提供高质量内容基础，覆盖官方、媒体、学术、产业实践、社区五大渠道。

## 搜索渠道矩阵

### 渠道1：官方权威来源
```
政府与监管机构
  ├── 中国：国务院、各部委官网、发改委报告、工信部白皮书
  ├── 美国：White House/FTC/FDA/SEC官方报告
  └── 关键词策略：site:gov.cn OR site:gov [主题] report/white paper

国际组织：联合国体系 / WEF / McKinsey Global Institute
企业官方：年报(10-K) / IR页 / 工程师博客 / 技术白皮书
```

### 渠道2：媒体报道
```
财经主流：Reuters / Bloomberg / FT / WSJ / 财新 / 第一财经
科技行业：MIT Technology Review / Wired / TechCrunch / 36氪 / 虎嗅
```

### 渠道3：学术研究
```
搜索引擎：Google Scholar / arXiv / PubMed / CNKI / 万方
顶会/顶刊：NeurIPS / ICML / Nature / Science / HBR
策略：优先高引用综述，检索近2-3年顶会论文
```

### 渠道4：产业实践与报告
```
咨询机构：McKinsey / BCG / Gartner / IDC / 艾瑞 / 易观
数据来源：CB Insights / Crunchbase / PitchBook
案例库：Harvard Business School Cases / MIT Sloan
```

### 渠道5：社区与用户声音
```
技术社区：GitHub / Stack Overflow / Hacker News / Reddit
专业社交：LinkedIn / X(Twitter) / 知乎
视频平台：TED Talks / YouTube / B站
```

## Research 执行工作流

### Step 1: 任务拆解
```
主题类型 → 主力渠道映射：
  技术/AI类    → 学术(arXiv) + 媒体(TechCrunch) + 社区(GitHub/HN)
  商业/战略类  → 咨询报告(McKinsey/BCG) + 媒体(FT/WSJ) + 案例(HBS)
  政策/监管类  → 官方(gov.cn) + 媒体(Reuters) + 智库
  医疗/科学类  → 学术(PubMed/Nature) + 官方(WHO/FDA)
  市场/行业类  → 咨询(IDC/Gartner) + 数据(CB Insights) + 媒体
```

### Step 2: 并行多源搜索
```
Thread A: 官方渠道（政府+国际组织+企业官方）
Thread B: 媒体渠道（主流+科技+行业媒体）
Thread C: 学术搜索（综述+顶会+近期论文）
Thread D: 产业报告（咨询机构+行业协会）
Thread E: 社区信号（GitHub+社交+视频）

每渠道收集：标题 / 来源 / 时间 / 摘要（50-100字）/ URL / 核心数据点 / 代表性引语
```

### Step 3: 内容过滤与验证
```
过滤标准：时效性（优先2年内）/ 权威性（官方>学术>咨询>媒体）/ 相关性 / 唯一性
数据验证：重要数据点需至少2个独立来源交叉验证
```

### Step 4: 内容分类整理

按子主题归组（与PPT大纲对应），每章节包含：数据点列表（含来源）/ 代表性案例 / 权威引语

## Research 质量标准

```
数量基准（20页PPT对应）：
  ├── 数据点：≥ 20个量化数据
  ├── 学术来源：≥ 5篇论文/报告
  ├── 官方来源：≥ 3个权威机构
  ├── 案例：≥ 3个具体实践案例
  └── 代表性引语：≥ 5条可引用观点
```

---

# 模式三：Combined — RAG + 联网补充

等同于 `--mode rag --rag-mode supplement`：

1. 执行 RAG 流程，建立本地素材检索
2. 计算覆盖度报告
3. 对覆盖率 < 70% 的章节，自动触发 Research 模式补充
4. 合并两路素材，去重后输出

---

# 统一输出格式

两种模式输出完全相同的素材包，直接衔接 Phase 3-9：

```
ppt_assets/
  ├── outline.md        幻灯片大纲（含每页建议内容类型）
  ├── data.md           数据点（来源引用到具体文件+页码/URL）
  ├── quotes.md         精选引语和案例（保留原文+出处）
  └── refs.md           参考文献列表（APA/IEEE格式）
  └── rag_report.md     （仅RAG模式）覆盖度+来源统计
```

**data.md 引用格式**（精确到文件+位置）：
```markdown
## 市场规模数据
- 全球AI市场规模2024年达2,305亿美元
  来源：`market_report_2024.pdf` 第12页 | 可信度：★★★★★
  交叉验证：同一数据出现在 `industry_analysis.docx` 第8页
```

---

# 使用场景示例

```bash
# RAG 模式：已有材料 → PPT
/ppt Q4业绩汇报 --rag quarterly_report.pdf kpi_data.xlsx --style mckinsey
/ppt AI医疗分析 --rag-dir ./research_papers/ --pages 25

# RAG + 在线URL
/ppt 政策解读 --rag policy_doc.pdf https://gov.cn/policy/2024

# 持久化索引（多次复用）
/ppt 产品发布会 --rag product_spec.pdf --rag-index product_launch_2025
/ppt 销售培训  --rag-index product_launch_2025  # 复用已有索引

# Research 模式：纯网络研究
/ppt 人工智能行业分析 --mode research --pages 30

# Combined 模式：内部资料+联网补充
/ppt 新能源汽车战略 --rag internal_analysis.docx --rag-mode supplement

# 查看已保存索引
/ppt --rag-list
```
