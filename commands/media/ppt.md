---
name: ppt
description: 生成演示文稿，覆盖 6 种输出引擎：学术演讲、商务通用、技术/代码演示、Markdown快速出片、论文自动生成、编程式生成
user-invocable: true
argument-hint: "<任务描述> [--backend academic|ppt-master|slidev|marp|slidetailor|sdk] [--format ppt169|4:3] [--style <风格>] [--source <文件路径>] [--output <文件名>]"
---

# /ppt — 演示文稿生成

智能选择最合适的 PPT 引擎，或手动指定 `--backend` 精确控制。

---

## 快速示例

```
# 学术演讲（无论文PDF）
/ppt 帮我做论文答辩 PPT，主题"深度学习在医学图像分���中的应用"

# 学术演讲（有论文PDF，自动提取内容）
/ppt --backend slidetailor --source paper.pdf --duration 15

# 商务通用 PPT
/ppt 做一个年度总结 PPT --style mckinsey --pages 12

# 技术/代码演示（Slidev）
/ppt 做一个 React Hooks 技术分享 PPT --backend slidev

# Markdown 快速出片（Marp）
/ppt 把 README.md 转成幻灯片 --backend marp --source README.md

# 编程式生成（批量报表）
/ppt 根据 data.csv 批量生成月度销售报告 PPT --backend sdk
```

---

## 引擎选择指南

| `--backend` | 引擎 | 最适合 | 输出格式 |
|-------------|------|-------|---------|
| `academic` | academic-pptx | 学术演讲（无论文PDF） | .pptx |
| `slidetailor` | SlideTailor + academic-pptx | 学术演讲（有论文PDF） | .pptx |
| `ppt-master` | ppt-master | 商务通用、设计优先 | .pptx |
| `slidev` | Slidev | 技术/代码演示、前端展示 | .html / .pdf / .pptx |
| `marp` | Marp | Markdown快速出片 | .html / .pdf / .pptx |
| `sdk` | python-pptx / PptxGenJS | 编程式、数据驱动、批量生成 | .pptx |

---

## 自动场景检测

未指定 `--backend` 时，按以下规则自动路由：

```
IF --source *.pdf AND 学术关键词:
    → slidetailor（论文PDF → 学术幻灯片）

ELIF 学术关键词（论文答辩/会议演讲/研究报告）:
    → academic

ELIF 代码/技术/开发者关键词（React/Vue/API/架构/技术分享）:
    → slidev

ELIF --source *.md OR Markdown关键词（markdown/md文件/README）:
    → marp

ELIF 数据/批量/CSV/报表/编程关键词:
    → sdk

ELSE（商务/产品/汇报/通用）:
    → ppt-master
```

### 学术演讲关键词
`论文答辩` `thesis defense` `seminar` `conference talk` `学术报告` `研究演讲` `academic presentation` `grant briefing`

### 技术/代码关键词
`技术分享` `代码演示` `tech talk` `developer` `前端` `frontend` `开发者` `架构图` `API 介绍` `框架介绍`

### Markdown 关键词
`markdown` `md文件` `README` `文档转幻灯片` `quick slides` `快速出片`

### 数据/编程关键词
`批量生成` `数据报告` `CSV` `Excel` `自动化` `编程生成` `programmatic`

---

## 参数说明

### 通用参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--backend` | 指定引擎 | 自动检测 |
| `--source <路径>` | 源文档（PDF/DOCX/MD/URL/CSV） | — |
| `--output <文件名>` | 输出文件名（无扩展名） | 自动生成 |
| `--lang zh\|en` | 幻灯片语言 | `zh` |

### 学术演讲参数（`academic` / `slidetailor`）

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--type conference\|seminar\|defense\|grant` | 演讲类型 | `conference` |
| `--duration <分钟>` | 演讲时长（控制幻灯片数量） | `15` |
| `--audience specialist\|mixed\|general` | 受众类型 | `specialist` |
| `--citation apa\|ieee\|chicago` | 引用格式 | `ieee` |

### 商务通用参数（`ppt-master`）

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--style google\|mckinsey\|zen\|pixel\|academic` | 设计风格 | 自动 |
| `--format ppt169\|ppt43\|xiaohongshu\|moments` | 画布格式 | `ppt169` |
| `--pages <数量>` | 目标页数 | 自动 |
| `--image-backend gemini\|openai\|qwen\|zhipu` | 图片生成后端 | `gemini` |

### 技术演示参数（`slidev`）

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--theme default\|seriph\|bricks\|forest\|geist\|apple-basic` | 主题 | `default` |
| `--export html\|pdf\|pptx` | 导出格式 | `html` |
| `--highlighter shiki\|prism` | 代码高亮引擎 | `shiki` |

### Markdown 快速出片参数（`marp`）

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--theme default\|gaia\|uncover` | 主题 | `default` |
| `--export html\|pdf\|pptx` | 导出格式 | `pdf` |
| `--size 16:9\|4:3` | 幻灯片比例 | `16:9` |

### 编程式生成参数（`sdk`）

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--engine python-pptx\|pptxgenjs` | SDK 引擎 | `python-pptx` |
| `--template <模板路径>` | 基础模板 .pptx | — |
| `--data <数据路径>` | 数据源（CSV/JSON/Excel） | — |

---

## 各引擎执行流程

### academic — 学术演讲（无论文PDF）

```
Step 1: 识别演讲类型（conference / seminar / defense / grant）
Step 2: 规划幻灯片大纲
  → 标题 → 动机/背景 → 研究问题 → 方法 → 结果 → 结论 → 参考文献
Step 3: 生成行动标题（每张幻灯片标题为完整句子）
Step 4: 应用学术设计标准（白色背景/单一字体/≤3色）
Step 5: 学术 QA 检查：
  □ 幽灵甲板测试（仅读标题能还原完整论证）
  □ 每个结果幻灯片有"那又怎样"注释
  □ 所有数据有引用
  □ 字体 ≥ 20pt
Step 6: 输出 .pptx
```

### slidetailor — 论文PDF → 学术幻灯片

```
Step 1: SlideTailor 解析论文 PDF
  → 提取：标题、贡献、方法、结果、结论、图表
Step 2: AI 将长句改写为 bullet points（≤12词/条）
Step 3: 生成行动标题
Step 4: 定位论文图表，关联到对应幻灯片
Step 5: academic-pptx 格式化，应用学术设计标准
Step 6: QA 检查 + 输出 .pptx
```

### ppt-master — 商务通用

```
Step 1: 初始化项目（project_manager.py init）
Step 2: 导入源文档（PDF/DOCX/URL → Markdown）
Step 3: Strategist 生成设计规范（风格/颜色/布局）
Step 4: [可选] Image_Generator 生成配图
Step 5: Executor 生成 SVG
Step 6: 后处理（total_md_split → finalize_svg）
Step 7: SVG → PPTX（svg_to_pptx.py）
Step 8: 输出 exports/[项目名]_<timestamp>.pptx
```

### slidev — 技术/代码演示

```
Step 1: 确认技术主题和代码演示内容
Step 2: 选择��题（default / seriph / bricks / geist）
Step 3: 生成 slides.md（Markdown + Vue 语法）
  → 代码块使用 {行号} 语法添加聚焦动画
  → 复杂布局使用 grid 分栏
  → 演讲者备注写入 <!-- --> 注释
Step 4: 导出（html / pdf / pptx）
Step 5: 输出 slides.md + 导出文件
```

### marp — Markdown 快速出片

```
Step 1: 检查源文档格式
  → 已有 .md 文件：在开头注入 marp 指令
  → 无源文档：根据主题生成 Markdown
Step 2: 添加 Marp 指令（theme / size / paginate）
Step 3: 处理分页（--- 分隔符）
Step 4: 运行 marp-cli 导出
Step 5: 输出 .html / .pdf / .pptx
```

### sdk — 编程式生成

```
Step 1: 确认数据源和模板
Step 2: 选择引擎（python-pptx / PptxGenJS）
Step 3: 生成完整代码（含数据读取 + 幻灯片生���逻辑）
Step 4: 用户确认代码后执行（或直接输出代码）
Step 5: 输出 .pptx + 生成脚本（供复用）
```

---

## 输出格式汇总

```
academic / slidetailor → [名称]_academic.pptx
ppt-master            → exports/[名称]_<timestamp>.pptx
slidev                → slides.md + dist/index.html（或 .pdf/.pptx）
marp                  → slides.md + slides.pdf（或 .html/.pptx）
sdk                   → [名称].pptx + generate_ppt.py（或 .js）
```

---

## 依赖速查

### academic / slidetailor
```bash
pip install "markitdown[pptx]" python-pptx
npm install -g pptxgenjs
# SlideTailor 额外依赖：
pip install transformers torch PyMuPDF
```

### ppt-master
```bash
pip install python-pptx PyMuPDF mammoth svglib reportlab Pillow
npm install -g pptxgenjs
# 系统工具：LibreOffice, Poppler
```

### slidev
```bash
npm install -g @slidev/cli
# 导出 PDF/PPTX 需要：
npx playwright install chromium
```

### marp
```bash
npm install -g @marp-team/marp-cli
# 导出 PDF 需要：Chrome/Chromium
```

### sdk (python-pptx)
```bash
pip install python-pptx Pillow pandas openpyxl
```

### sdk (PptxGenJS)
```bash
npm install pptxgenjs
```

---

## 综合比较

| 维度 | academic | slidetailor | ppt-master | slidev | marp | sdk |
|------|---------|------------|----------|--------|------|-----|
| 上手速度 | 快 | 中（需PDF） | 中 | 中 | 极快 | 慢（需编程） |
| 设计质量 | 标准 | 标准 | 高 | 中-高 | 简洁 | 自定义 |
| 内容自动化 | 中 | 高（从论文） | 中 | 低 | 低 | 高（数据驱动） |
| 输出可编辑性 | ✅ PPTX | ✅ PPTX | ✅ PPTX | ⚠️ HTML优先 | ⚠️ PDF优先 | ✅ PPTX |
| 代码展示 | ❌ | ❌ | ❌ | ✅ 最佳 | ✅ 良好 | ❌ |
| 引用/参考文献 | ✅ 强制 | ✅ 自动提取 | ❌ | ❌ | ❌ | ⚠️ 手动 |
| 批量生成 | ❌ | ❌ | ❌ | ❌ | ⚠️ 有限 | ✅ 最佳 |
