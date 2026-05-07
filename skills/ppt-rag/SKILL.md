---
name: ppt-rag
description: >
  PPT专用RAG（检索增强生成）技能。触发词：本地文档/URL索引、RAG、已有材料、
  现成资料、文档库检索、知识库、资料归纳、--rag参数。
  支持PDF/DOCX/PPTX/MD/TXT/HTML/Excel等格式及在线URL批量摄入，
  向量化后按PPT主题检索相关片段，合成输出与ppt-researcher相同格式的素材包，
  可直接衔接Phase 3-9制作PPT。
user-invocable: false
effort: medium
---

# PPT RAG — 已有材料索引与检索技能

## 职责

将用户提供的**本地文件**或**线上URL**构建成可检索的知识库，
按PPT主题和子话题语义检索最相关内容，输出结构化素材包，
完全替代或补充 Phase 2（网络搜索），后续阶段无缝衔接。

---

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

---

## 核心流程

### Step 1: 文档摄入 (Ingestion)

```python
def ingest_sources(sources: list[str]) -> list[Document]:
    """
    sources: 文件路径列表 + URL列表（混合支持）
    返回: Document列表，每个Document含 text + metadata
    """
    documents = []
    
    for src in sources:
        if src.startswith("http"):
            # 线上URL
            content = fetch_url(src)          # WebFetch抓取
            doc = Document(
                text=extract_main_content(content),   # 去除导航/广告
                metadata={"source": src, "type": "url", "title": extract_title(content)}
            )
        elif src.endswith(".pdf"):
            pages = pymupdf.open(src)
            for i, page in enumerate(pages):
                doc = Document(
                    text=page.get_text(),
                    metadata={"source": src, "type": "pdf", "page": i+1}
                )
        elif src.endswith(".pptx"):
            prs = Presentation(src)
            for i, slide in enumerate(prs.slides):
                text = extract_slide_text(slide)    # 含备注
                doc = Document(
                    text=text,
                    metadata={"source": src, "type": "pptx", "slide": i+1}
                )
        # ... 其他格式类似处理
        
        documents.append(doc)
    
    return documents
```

**摄入进度输出**：
```
[RAG摄入进度]
✅ report_2024.pdf        → 42页，已提取 18,234 字
✅ market_analysis.docx   → 23页，已提取 9,876 字
✅ https://example.com/blog/ai-trends → 已抓取，3,421 字
⏳ industry_data.xlsx     → 处理中...
📊 共摄入 4 个来源，总计约 31,531 字
```

---

### Step 2: 规模判断与策略选择

```python
def choose_strategy(documents: list[Document]) -> str:
    total_chars = sum(len(d.text) for d in documents)
    total_docs = len(documents)
    
    if total_chars < 40_000 and total_docs <= 8:
        # 小规模：直接全文放入上下文，LLM直接分析
        return "direct"
    
    elif total_chars < 200_000:
        # 中规模：BM25关键词检索（无需向量化，速度快）
        return "bm25"
    
    else:
        # 大规模：向量化+语义检索（ChromaDB/FAISS）
        return "vector"
```

| 策略 | 触发条件 | 优点 | 工具 |
|------|---------|------|------|
| `direct` | ≤8个文件且≤4万字 | 最准确，无需额外依赖 | 直接LLM处理 |
| `bm25` | ≤20万字 | 快速，无需GPU/API | rank-bm25 |
| `vector` | >20万字 或 需要持久化索引 | 语义检索，支持复用 | ChromaDB/FAISS |

---

### Step 3: 分块 (Chunking)

```python
def chunk_documents(documents: list[Document], strategy: str) -> list[Chunk]:
    """
    分块策略根据文档类型自动调整
    """
    chunks = []
    
    for doc in documents:
        if doc.metadata["type"] == "pdf":
            # PDF按页分块（保留页码引用）
            chunk_size = 800    # tokens
            overlap = 100
        elif doc.metadata["type"] == "pptx":
            # PPT每页一个chunk（已是自然分界）
            chunk_size = 600
            overlap = 0
        else:
            # 文章/文档：按段落递归分割
            chunk_size = 600
            overlap = 80
        
        doc_chunks = recursive_split(
            text=doc.text,
            chunk_size=chunk_size,
            overlap=overlap,
            separators=["\n\n", "\n", "。", ".", " "]   # 中文优先在句子边界分割
        )
        
        for i, chunk_text in enumerate(doc_chunks):
            chunks.append(Chunk(
                text=chunk_text,
                metadata={**doc.metadata, "chunk_id": i, "char_count": len(chunk_text)}
            ))
    
    return chunks
```

**分块规范**：
- 每块 500-800 tokens（约600-1000中文字符）
- 重叠 10-15%（保留上下文连续性）
- 保留原始来源元数据（文件名/页码/URL/标题）
- 过滤：空块、纯数字块、无意义片段（< 50字）

---

### Step 4: 向量化与索引 (Embedding & Indexing)

```python
# 向量模型选择（按可用性自动降级）
EMBEDDING_MODELS = [
    # 首选：多语言高质量（中英文俱佳）
    ("BAAI/bge-m3", "local", "sentence-transformers"),
    # 次选：OpenAI API（需key，质量优秀）
    ("text-embedding-3-small", "api", "openai"),
    # 兜底：纯本地小模型（速度快，质量一般）
    ("BAAI/bge-small-zh-v1.5", "local", "sentence-transformers"),
    # 最后兜底：BM25关键词（无需向量化）
    ("bm25", "local", "rank-bm25"),
]

def build_index(chunks: list[Chunk], index_name: str = None) -> VectorStore:
    model = auto_select_embedding_model()
    
    if VECTOR_BACKEND == "chroma":
        # ChromaDB：持久化，支持跨session复用
        client = chromadb.PersistentClient(path=f".ppt_rag/{index_name}/")
        collection = client.get_or_create_collection(
            name=index_name,
            embedding_function=model
        )
        collection.upsert(
            documents=[c.text for c in chunks],
            metadatas=[c.metadata for c in chunks],
            ids=[f"chunk_{i}" for i, c in enumerate(chunks)]
        )
    
    elif VECTOR_BACKEND == "faiss":
        # FAISS：纯内存，速度最快，不持久化
        embeddings = model.encode([c.text for c in chunks])
        index = faiss.IndexFlatIP(embeddings.shape[1])  # 内积相似度
        index.add(embeddings)
    
    return store

# 索引持久化（--rag-index 指定名称时）
# 存储位置：.ppt_rag/<index_name>/
#   ├── chroma/          ChromaDB数据
#   ├── metadata.json    索引元信息（来源列表/创建时间/文档数）
#   └── chunks.jsonl     原始分块文本（便于调试）
```

**索引持久化与复用**：
```
首次建立：--rag report.pdf slides.pdf --rag-index my_project
          → 索引保存到 .ppt_rag/my_project/
          → 下次可直接复用：--rag-index my_project（跳过摄入步骤）

增量更新：--rag new_doc.pdf --rag-index my_project
          → 仅对新文件分块并追加到已有索引

查看已有索引：/ppt --rag-list
              → 列出所有持久化索引（名称/文件数/创建时间/大小）
```

---

### Step 5: 主题驱动检索 (Topic-driven Retrieval)

```python
def retrieve_for_ppt(
    store: VectorStore,
    ppt_topic: str,
    outline: list[SlideSpec],    # Phase 1输出的大纲
    top_k: int = 5
) -> dict[str, list[Chunk]]:
    """
    为每个幻灯片章节单独检索，确保每部分都有对应素材
    """
    results = {}
    
    # 为整体主题检索（获取背景/概述材料）
    results["overview"] = store.query(
        query_texts=[ppt_topic, f"{ppt_topic} 综述 overview"],
        n_results=top_k
    )
    
    # 为每个章节/子话题分别检索
    for section in outline:
        queries = generate_section_queries(section, ppt_topic)
        # 例：section="市场规模" → queries=["市场规模 数据", "TAM SAM", "行业规模 亿"]
        
        section_results = store.query(
            query_texts=queries,
            n_results=top_k,
            where=None   # 不过滤来源，跨文档检索
        )
        
        results[section.title] = deduplicate_and_rank(section_results)
    
    return results
```

**查询扩展策略**：
```python
def generate_section_queries(section: str, topic: str) -> list[str]:
    """为单个章节生成多个检索query，提高召回率"""
    queries = [
        section,                          # 直接匹配
        f"{topic} {section}",             # 加主题上下文
        f"{section} 数据 案例 实践",       # 搜索具体内容
        translate_to_english(section),    # 英文版本（跨语言检索）
    ]
    return [q for q in queries if q]     # 去空
```

**检索质量优化**：
- **去重**：余弦相似度>0.92的片段只保留评分最高的一个
- **多样性**：同一来源文件最多贡献3个片段（避免单一来源主导）
- **相关性过滤**：相似度<0.45的片段丢弃（噪声过滤）
- **交叉引用**：同一事实在多个来源出现→标注"多源验证"

---

### Step 6: 内容合成 (Synthesis)

```python
def synthesize_to_ppt_materials(
    retrieved: dict[str, list[Chunk]],
    topic: str,
    audience: str,
    purpose: str
) -> PPTMaterials:
    """
    将检索结果合成为与ppt-researcher输出格式一致的素材包
    每个合成步骤均保留来源引用
    """
    
    # 1. 提取数据点（量化信息优先）
    data_points = extract_data_points(retrieved)
    # 示例：[{"value": "市场规模达2300亿元", "source": "report.pdf:p12", "year": "2024"}]
    
    # 2. 提取关键引语
    quotes = extract_quotes(retrieved)
    
    # 3. 提取案例（STAR格式识别）
    cases = extract_cases(retrieved)
    
    # 4. 生成大纲（基于检索内容的覆盖度）
    outline = generate_outline_from_retrieval(retrieved, topic, audience, purpose)
    
    # 5. 整理参考文献（来源去重+格式化）
    refs = format_references(retrieved)
    
    return PPTMaterials(
        outline=outline,    # → outline.md
        data=data_points,   # → data.md
        quotes=quotes,      # → quotes.md
        refs=refs,          # → refs.md
        rag_coverage=compute_coverage(retrieved, outline)  # 覆盖度报告
    )
```

**覆盖度报告**（合成完成后展示）：
```
[RAG素材覆盖度]
✅ 第1章 背景与现状    → 找到 8 个相关片段（来自 3 个文件）
✅ 第2章 市场规模      → 找到 6 个相关片段（含 4 个量化数据点）
⚠️ 第3章 竞争格局      → 仅找到 2 个相关片段（覆盖较薄）
   建议：补充 --rag 竞品分析文档，或开启 --rag-mode supplement 联网补充
✅ 第4章 案例分析      → 找到 5 个案例（2个有完整STAR数据）
✅ 第5章 未来展望      → 找到 4 个相关片段

总体覆盖率：82%  ⚠️ 建议补充"竞争格局"相关资料
```

---

## 输出格式

与 `ppt-researcher` 完全一致，可直接进入 Phase 3：

```
ppt_assets/
  ├── outline.md        幻灯片大纲（含每页建议内容类型）
  ├── data.md           数据点（来源引用到具体文件+页码/URL+段落）
  ├── quotes.md         精选引语和案例（保留原文+出处）
  ├── refs.md           参考文献列表（APA/IEEE格式）
  └── rag_report.md     RAG检索报告（覆盖度+来源统计+建议）
```

**data.md 引用格式示例**（精确到文件+位置）：
```markdown
## 市场规模数据
- 全球AI市场规模2024年达2,305亿美元，预计2030年增至8,272亿美元
  来源：`market_report_2024.pdf` 第12页 | 可信度：★★★★★

- 中国AI核心产业规模超过5,000亿元（2023年）
  来源：`中国信通院白皮书.pdf` 第3页 | 可信度：★★★★★
  交叉验证：同一数据出现在 `industry_analysis.docx` 第8页
```

---

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--rag <来源>` | 文件路径或URL（空格分隔多个）| — |
| `--rag-dir <目录>` | 递归索引整个目录 | — |
| `--rag-index <名称>` | 索引名称（用于持久化和复用）| 临时索引 |
| `--rag-mode replace\|supplement` | replace=仅RAG；supplement=RAG+网络搜索 | `replace` |
| `--rag-top-k <n>` | 每个章节检索的片段数 | `5` |
| `--rag-list` | 列出所有已保存的持久化索引 | — |
| `--rag-backend chroma\|faiss\|bm25\|auto` | 向量存储后端 | `auto` |

---

## 工具链依赖

```bash
# 文档解析（必须）
pip install PyMuPDF python-docx python-pptx markitdown beautifulsoup4 pandas

# 向量检索（按需选择一种）
pip install chromadb                          # 首选：持久化，跨session复用
pip install faiss-cpu                         # 次选：速度最快，内存中运行
pip install rank-bm25                         # 最轻量：关键词检索（无需向量化）

# 向量嵌入（按需选择一种）
pip install sentence-transformers             # 本地嵌入（推荐BGE-M3多语言模型）
pip install openai                            # OpenAI Embeddings API

# 可选增强
pip install langdetect                        # 自动语言检测
pip install ebooklib                          # EPUB格式支持
pip install openpyxl                          # Excel支持
```

**自动降级链**（按可用性自动选择，无需手动配置）：
```
BGE-M3（本地） → text-embedding-3-small（OpenAI API）→ BGE-small-zh（本地轻量）→ BM25（无向量）
ChromaDB（持久化）→ FAISS（内存）→ BM25（关键词）→ 直接LLM处理（超小规模）
```

---

## 使用场景示例

```bash
# 场景1：公司内部报告 → PPT
/ppt Q4业绩汇报 --rag quarterly_report.pdf kpi_data.xlsx --style mckinsey

# 场景2：多份研究报告 → 行业分析PPT
/ppt AI医疗行业分析 --rag-dir ./research_papers/ --mode full --pages 25

# 场景3：在线文章 + 本地文档混合
/ppt 碳中和政策解读 --rag policy_doc.pdf https://gov.cn/policy/2024/carbon https://news.cn/env

# 场景4：建立持久化知识库，多次复用
/ppt 产品发布会PPT --rag product_spec.pdf user_research.pdf --rag-index product_launch_2025
# 下次同项目复用（跳过重复摄入）：
/ppt 销售培训PPT --rag-index product_launch_2025 --mode make

# 场景5：RAG+网络搜索联合（用已有材料打底，联网补充最新进展）
/ppt 新能源汽车战略报告 --rag internal_analysis.docx --rag-mode supplement --mode full

# 场景6：查看已保存的索引
/ppt --rag-list
```

---

## 错误处理

### 文件无法解析
```
⚠️ report_scan.pdf 解析失败（可能是扫描版PDF，无文字层）
自动处理：跳过该文件，继续处理其他来源
建议：使用OCR工具（tesseract/Adobe Acrobat）转换后重试
```

### URL无法访问
```
⚠️ https://example.com/report 访问失败（403/超时）
自动处理：记录失败URL，继续处理其他来源
可选：--rag-retry 重试失败URL（最多3次）
```

### 覆盖度不足（< 60%）
```
⚠️ RAG检索覆盖率仅 54%，以下章节素材不足：
  - 竞争格局（找到0个相关片段）
  - 未来预测（找到1个片段，可能不充分）

建议选项：
  1. 补充相关文件：--rag competitor_report.pdf future_outlook.pdf
  2. 开启联网补充：--rag-mode supplement
  3. 继续制作（覆盖不足的章节用通用内容填充）
```

### 索引过大（> 10万个chunk）
```
⚠️ 文档库过大（预计生成 120,000 个chunk）
建议：
  1. 使用 --rag-dir 过滤子目录（只索引最相关的文件夹）
  2. 使用 --rag 精确指定关键文件（而非整个目录）
  3. 强制继续：--rag-force（可能较慢，约需15-30分钟建立索引）
```
