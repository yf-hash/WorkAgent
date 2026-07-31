---
name: ppt-rag-indexer
description: >
  PPT 已有材料 RAG 索引与检索技能。将用户提供的本地文件（pdf/docx/pptx/md/html/xlsx/epub）或线上 URL
  构建可检索知识库，按 PPT 主题语义检索最相关内容，输出与 Phase 3-9 直接衔接的结构化素材包。
  支持持久化索引、增量更新、覆盖度报告、多种向量后端（chroma/faiss/bm25/auto）。
  触发词：PPT 已有材料、本地文档索引、RAG、ppt rag、向量检索 PPT、内部资料 PPT
user-invocable: false
effort: high
argument-hint: "[--rag <文件/URL>...] [--rag-dir <目录>] [--rag-index <名称>] [--rag-mode replace|supplement] [--rag-top-k <n>] [--rag-list] [--rag-backend chroma|faiss|bm25|auto]"
---

# PPT RAG Indexer — 已有材料索引与检索

> 单一职责：把用户已有的内部资料 → 可检索向量库 → 主题驱动检索 → 输出素材包。
> 不做：联网研究（→ `ppt-web-researcher`）、写大纲（→ `ppt-architect`）、生成 PPT（→ `ppt-master` 等）

## 支持的输入格式

### 本地文件
| 格式 | 解析工具 | 说明 |
|------|---------|------|
| `.pdf` | PyMuPDF / markitdown | 含图表页描述、表格文字提取 |
| `.docx` | python-docx / markitdown | 保留标题层级 |
| `.pptx` | python-pptx | 提取每页文字+备注 |
| `.md` / `.txt` | 直接读取 | 保留 Markdown 结构 |
| `.html` | BeautifulSoup | 提取正文，去除导航/广告 |
| `.xlsx` / `.csv` | pandas | 表格数据转文字描述 |
| `.epub` | ebooklib | 电子书 |

### 线上 URL
| 类型 | 处理方式 |
|------|---------|
| 单页文章 / 博客 | WebFetch 抓取正文 |
| 在线 PDF | 下载后按本地 PDF 处理 |
| 文档站点 (`/docs/`) | 递归抓取同域名子页面（深度 ≤ 2） |
| GitHub README | 抓取 raw 内容 |
| 学术论文页 (arXiv/DOI) | 抓取摘要+全文（如可访问） |
| YouTube / 视频 | 抓取字幕/描述文字 |
| 多个 URL（换行分隔） | 批量并行抓取 |

### 目录扫描
```
--rag-dir <目录>    递归扫描目录，处理所有支持格式文件
                   自动跳过：.git/ node_modules/ __pycache__/
                   最大文件数：500（超出按修改时间取最新）
```

## 核心流程

### Step 1：文档摄入

```python
def ingest_sources(sources: list[str]) -> list[Document]:
    documents = []
    for src in sources:
        if src.startswith("http"):
            content = fetch_url(src)
            doc = Document(text=extract_main_content(content),
                           metadata={"source": src, "type": "url", "title": extract_title(content)})
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

### Step 2：规模判断与策略选择

```python
def choose_strategy(documents):
    total_chars = sum(len(d.text) for d in documents)
    total_docs = len(documents)
    if total_chars < 40_000 and total_docs <= 8:
        return "direct"       # 直接 LLM 处理（最准确）
    elif total_chars < 200_000:
        return "bm25"         # BM25 关键词检索（快速）
    else:
        return "vector"       # 向量化+语义检索（大规模）
```

### Step 3：分块

每块 500-800 tokens，重叠 10-15%，按文档类型调整：PDF 按页、PPT 每页一块、文章按段落递归分割。

### Step 4：向量化与索引

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
查看索引：--rag-list
```

### Step 5：主题驱动检索

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

**检索质量优化**：余弦相似度 > 0.92 去重、同源最多 3 片段、相似度 < 0.45 丢弃、多源验证标注

### Step 6：内容合成

输出与 `ppt-web-researcher` 完全相同的素材包格式：

```
ppt_assets/
  ├── outline.md        幻灯片大纲（含每页建议内容类型）
  ├── data.md           数据点（来源引用到具体文件+页码/URL）
  ├── quotes.md         精选引语和案例（保留原文+出处）
  ├── refs.md           参考文献列表（APA/IEEE 格式）
  └── rag_report.md     覆盖度+来源统计
```

**覆盖度报告**：

```
[RAG 素材覆盖度]
✅ 第 1 章 背景与现状    → 找到 8 个相关片段
⚠️ 第 3 章 竞争格局      → 仅找到 2 个相关片段（覆盖较薄）
   建议：调用 `ppt-web-researcher` 联网补充
总体覆盖率：82%
```

**data.md 引用格式**：
```markdown
## 市场规模数据
- 全球 AI 市场规模 2024 年达 2,305 亿美元
  来源：`market_report_2024.pdf` 第 12 页 | 可信度：★★★★★
  交叉验证：同一数据出现在 `industry_analysis.docx` 第 8 页
```

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--rag <来源>` | 文件路径或 URL（空格分隔多个）| — |
| `--rag-dir <目录>` | 递归索引整个目录 | — |
| `--rag-index <名称>` | 索引名称（持久化和复用）| 临时索引 |
| `--rag-top-k <n>` | 每章节检索片段数 | `5` |
| `--rag-list` | 列出已保存的持久化索引 | — |
| `--rag-backend chroma\|faiss\|bm25\|auto` | 向量存储后端 | `auto` |

## 依赖

```bash
pip install PyMuPDF python-docx python-pptx markitdown beautifulsoup4 pandas
pip install chromadb           # 持久化向量存储（首选）
pip install faiss-cpu          # 内存向量存储（次选）
pip install rank-bm25          # 关键词检索（轻量）
pip install sentence-transformers  # 本地嵌入模型
```
