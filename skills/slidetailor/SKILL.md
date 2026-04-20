# SlideTailor — AI 学术幻灯片内容生成

## 概述
NUS NLP Lab 出品的学术幻灯片生成工具，基于 NLP 技术从科学论文 PDF 自动提取关键信息，生成结构化的幻灯片内容（标题、要点、图表位置）。用于学术演讲的内容骨架生成，结合 academic-pptx 进行格式化输出。

## 核心能力
- **论文内容提取** — 解析 PDF，识别标题、摘要、贡献、方法、结果、结论
- **关键点提炼** — 自动判断每张幻灯片的核心内容
- **图表定位** — 识别论文中的 Figure/Table 并关联到幻灯片
- **结构推荐** — 按演讲类型推荐幻灯片大纲
- **内容优化** — AI 改写，从论文长句转换为幻灯片 bullet point
- **可读性分析** — 检查 bullet point 长度、复杂度

## 安装

```bash
# 克隆仓库
git clone https://github.com/nusnlp/SlideTailor.git
cd SlideTailor

# 安装依赖
pip install -r requirements.txt

# 下载模型（首次运行自动下载）
python setup.py install
```

## 使用场景
1. **有论文 PDF** → 自动生成幻灯片内容草稿
2. **演讲准备** → 快速整理论文核心贡献为幻灯片要点
3. **内容审查** → 检查现有幻灯片内容的可读性和完整性
4. **多论文整合** → 将多篇相关论文整合为一场演讲

## 核心工作流

### Step 1: 论文内容提取
```python
from slidetailor import PaperParser

parser = PaperParser()
paper = parser.parse("my_paper.pdf")

# 提取的结构
print(paper.title)        # 论文标题
print(paper.abstract)     # 摘要
print(paper.contributions) # 主要贡献（列表）
print(paper.methods)       # 方法描述
print(paper.results)       # 实验结果
print(paper.conclusion)    # 结论
print(paper.figures)       # 图表列表
```

### Step 2: 幻灯片内容生成
```python
from slidetailor import SlideGenerator

generator = SlideGenerator(
    presentation_type="conference",  # conference | defense | seminar
    duration_minutes=15,
    audience="specialist"            # specialist | mixed | general
)

slides_content = generator.generate(paper)

# slides_content 结构示例
# [
#   {"type": "title", "title": "...", "subtitle": "..."},
#   {"type": "motivation", "action_title": "...", "bullets": [...]},
#   {"type": "method", "action_title": "...", "figure": "fig2.png"},
#   {"type": "result", "action_title": "...", "table": "tab1"},
#   ...
# ]
```

### Step 3: 内容优化
```python
from slidetailor import ContentOptimizer

optimizer = ContentOptimizer()

# 改写长句为 bullet points
optimized = optimizer.rewrite_bullets(
    text="Our method achieves state-of-the-art performance...",
    max_words_per_bullet=12
)

# 可读性检查
issues = optimizer.check_readability(slides_content)
# 返回：字数超限、行数过多、缺少行动标题等问题
```

## 与 academic-pptx 集成

SlideTailor 生成内容骨架，academic-pptx 负责格式化输出。

```python
# 完整流程
from slidetailor import PaperParser, SlideGenerator
from academic_pptx import SlideFormatter

# 1. 解析论文
paper = PaperParser().parse("paper.pdf")

# 2. 生成内容
content = SlideGenerator(
    presentation_type="conference",
    duration_minutes=15
).generate(paper)

# 3. 格式化为 PPTX（academic-pptx 标准）
formatter = SlideFormatter(
    template="academic_white",
    citation_style="APA"
)
formatter.export(content, "output.pptx")
```

## 内容优化规则

### Bullet Point 写作规范
```
✅ 好：
- Achieves 3.2% F1 improvement over baseline
- Reduces inference time by 40%
- Generalizes to 5 out-of-domain datasets

❌ 不好：
- Our proposed method demonstrates significantly improved performance 
  across multiple evaluation metrics compared to prior work
```

### 行动标题（Action Title）规则
```
✅ 好：
"Our Method Reduces Training Cost by 60% Without Accuracy Loss"
"Cross-Domain Evaluation Confirms Generalization"

❌ 不好：
"Experiments"
"Results"
"Method Overview"
```

## 输出格式

```markdown
## SlideTailor 内容生成结果

**论文**：`paper.pdf`
**演讲类型**：Conference / Defense / Seminar
**幻灯片数量**：[N] 张（按 [X] 分钟演讲规划）

**生成的幻灯片大纲**：
1. 标题页 — [论文标题]
2. 动机 — [行动标题]（[要点数] 个要点）
3. 方法 — [行动标题]（含 Figure [N]）
4. 实验 — [行动标题]（含 Table [N]）
5. 结论 — [行动标题]（[要点数] 个要点）
6. 参考文献

**内容优化提示**：
- [X] 个 bullet point 超过 12 词，已自动精简
- [Y] 张幻灯片已添加行动标题

**输出**：`slides_content.json`（可导入 academic-pptx）
```

## 常见问题

### PDF 解析效果差
- 确保 PDF 不是扫描件（需要可选中文字）
- 使用 ArXiv 下载的 PDF 效果最佳
- 中文论文支持有限

### 幻灯片数量不合适
- 调整 `duration_minutes` 控制幻灯片密度
- 使用 `max_slides` 参数强制限制数量

## 相关资源
- GitHub: https://github.com/nusnlp/SlideTailor
- NUS NLP Lab: https://nlp.comp.nus.edu.sg/
