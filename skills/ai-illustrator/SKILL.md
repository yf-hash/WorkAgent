---
name: ai-illustrator
description: >
  AI 智能插图生成知识库。触发词：文章插图、学术配图、论文图表、文档插图、
  AI插图、自动配图、article-illustrator、thesis-figure、paper-banana、
  document-illustrator、jaaz、插画生成、风格插图、像素风、水墨风、吉卜力风格。
  支持文章自动配图、学术论文图表、文档专业插图、创意画布四大场景。
user-invocable: false
effort: high
---

# AI Illustrator — AI 智能插图生成知识库

> 整合来源：
> - article-illustrator（文章自动配图 MCP Server）
> - document-illustrator-skill（文档专业插图，Claude+Gemini）
> - thesis-figure-skill（学术论文图表，LaTeX/TikZ/draw.io）
> - paper-banana（科学论文插图，Matplotlib，NeurIPS/ICML标准）
> - AI-illustration-generator-demo（Notion风格平面插图）
> - jaaz（多模态创意画布，Midjourney/GPT-4o/Kling）

---

## 一、场景路由

| 场景 | 推荐工具 | 输出风格 |
|------|---------|---------|
| 技术/产品文章配图 | article-illustrator | 像素风/水墨/吉卜力/自定义 |
| 文档专业插图（PPT/报告） | document-illustrator-skill | 渐变玻璃/票据设计/矢量 |
| 学术论文图表 | thesis-figure-skill | LaTeX/TikZ/draw.io |
| 科学论文可视化 | paper-banana | Matplotlib/NeurIPS标准 |
| Notion风格平面插图 | AI-illustration-generator | 扁平简约/品牌一致 |
| 创意多模态画布 | jaaz | 写实/艺术/多角色一致 |

---

## 二、article-illustrator — 文章自动配图

### 核心能力
- 自动分析 Markdown 文章，识别需要配图的段落
- 生成并插入插图（支持自定义风格）
- 保持角色/元素一致性（跨图一致）
- 支持 CLI 和 MCP Server 两种调用方式

### 支持风格
```
pixel-art      像素风格（复古游戏感）
ink-painting   水墨画风格（中国传统）
ghibli         吉卜力动画风格（温暖治愈）
flat-design    扁平设计风格（现代简约）
watercolor     水彩风格（柔和艺术）
custom         自定义风格（提供参考图）
```

### 使用方式
```bash
# CLI 模式
pip install article-illustrator
article-illustrator --input article.md --style pixel-art --output ./imgs/

# MCP Server 模式（Claude Code 集成）
# 在 claude_desktop_config.json 中配置：
{
  "mcpServers": {
    "article-illustrator": {
      "command": "python",
      "args": ["-m", "article_illustrator.server"]
    }
  }
}
```

### 工作流程
```
Step 1: 文章解析
  → 读取 Markdown 文件
  → 识别段落语义（标题/正文/代码/列表）
  → 标记适合配图的位置（通常是概念性段落）

Step 2: 插图规划
  → 为每个配图位置生成图像描述提示词
  → 确保跨图风格一致性
  → 规划图像尺寸（文章内嵌：800×450 / 封面：1200×630）

Step 3: 图像生成
  → 调用图像生成 API（Stable Diffusion / DALL-E / Midjourney）
  → 应用风格参数
  → 质量检验（分辨率/内容相关性）

Step 4: 插入文章
  → 在对应段落后插入 ![描述](路径) 语法
  → 更新文章文件
```

---

## 三、document-illustrator-skill — 文档专业插图

### 核心能力
- 分析文档内容（Markdown/PDF/纯文本）
- 生成三种专业视觉风格的插图
- 支持 16:9 和 3:4 两种比例
- 使用 Claude Sonnet 4.5 + Gemini 3 Pro 双模型

### 三种视觉风格
```
gradient-glass  渐变玻璃风格
  → 半透明玻璃质感，渐变色背景
  → 适合：科技产品文档、SaaS 介绍、现代商务报告

ticket-design   票据设计风格
  → 撕边效果，复古票据感
  → 适合：活动方案、营销材料、创意提案

vector-style    矢量插图风格
  → 简洁线条，扁平化图形
  → 适合：教程文档、说明书、通用商务文档
```

### 使用方式（Claude Skill 调用）
```
# 在 Claude 对话中：
请分析以下文档并生成专业插图：
[粘贴文档内容]

风格：gradient-glass
比例：16:9
数量：3张（封面 + 2张内容图）
```

### 提示词模板
```
你是一位专业的文档插图设计师。请分析以下文档内容，
为其生成 [数量] 张专业插图。

文档内容：
[内容]

要求：
- 风格：[gradient-glass / ticket-design / vector-style]
- 比例：[16:9 / 3:4]
- 每张图需体现文档的核心概念
- 输出：图像生成提示词（英文，适合 Midjourney/DALL-E）
```

---

## 四、thesis-figure-skill — 学术论文图表

### 核心能力
- 将学术文本/图像转换为出版级图表
- 支持 LaTeX/TikZ 和 draw.io 两种格式
- 内嵌数据可视化（热力图/柱状图/波形图）
- 14种图表类型，自动质量保证

### 支持的14种图表类型
```
1.  系统架构图（System Architecture）
2.  算法流程图（Algorithm Flowchart）
3.  神经网络结构图（Neural Network）
4.  实验对比图（Experiment Comparison）
5.  数据流图（Data Flow）
6.  时序图（Sequence Diagram）
7.  热力图（Heatmap）
8.  柱状图/折线图（Bar/Line Chart）
9.  散点图（Scatter Plot）
10. 消融实验图（Ablation Study）
11. 注意力可视化（Attention Visualization）
12. 框架对比图（Framework Comparison）
13. 概念示意图（Conceptual Diagram）
14. 结果展示图（Results Visualization）
```

### LaTeX/TikZ 输出示例
```latex
\begin{figure}[htbp]
\centering
\begin{tikzpicture}[
  node distance=1.5cm,
  box/.style={rectangle, draw, rounded corners, minimum width=2cm}
]
  \node[box] (input) {输入层};
  \node[box, below of=input] (hidden) {隐藏层};
  \node[box, below of=hidden] (output) {输出层};
  \draw[->] (input) -- (hidden);
  \draw[->] (hidden) -- (output);
\end{tikzpicture}
\caption{模型架构示意图}
\label{fig:architecture}
\end{figure}
```

### 使用方式
```
# Claude Skill 调用
请将以下论文段落转换为出版级图表：

[论文段落内容]

图表类型：系统架构图
输出格式：LaTeX/TikZ
目标期刊：NeurIPS / ICML / ACL（影响排版标准）
```

---

## 五、paper-banana — 科学论文可视化

### 核心能力
- 多 Agent 系统，专为科学论文设计
- 生成 Matplotlib 代码（可复现）
- 支持方法论图、统计图、美学优化
- 目标标准：NeurIPS/ICML 出版质量

### 工作流程
```
Agent 1: 内容分析
  → 解析论文文本，识别需要可视化的数据/概念

Agent 2: 图表规划
  → 选择最合适的图表类型
  → 规划布局和配色方案

Agent 3: 代码生成
  → 生成 Matplotlib/Seaborn Python 代码
  → 确保代码可直接运行

Agent 4: 美学优化
  → 应用学术期刊配色规范
  → 调整字体、间距、图例
  → 输出 PDF/EPS 格式（矢量，适合印刷）
```

### Matplotlib 代码模板
```python
import matplotlib.pyplot as plt
import numpy as np

# 学术风格配置
plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 12,
    'axes.linewidth': 1.5,
    'figure.dpi': 300,
})

fig, ax = plt.subplots(figsize=(6, 4))
# [生成的图表代码]
plt.tight_layout()
plt.savefig('figure.pdf', bbox_inches='tight')
```

---

## 六、jaaz — 多模态创意画布

### 核心能力
- 开源 Canva 替代品，本地优先
- 无限画布，多角色一致性生成
- 支持 GPT-4o / Midjourney / VEO3 / Kling
- Electron 桌面应用，数据本地存储

### 适用场景
```
创意内容：品牌视觉、营销素材、社交媒体配图
多角色场景：故事板、漫画、产品展示（保持角色一致）
视频生成：VEO3/Kling 视频片段生成
草图生成：手绘草图 → AI 精细化
```

### 安装与使用
```bash
# 克隆并运行
git clone https://github.com/11cafe/jaaz
cd jaaz && npm install && npm run dev

# 或下载桌面版
# https://github.com/11cafe/jaaz/releases
```

---

## 七、提示词工程指南

### 文章配图提示词结构
```
[风格关键词], [主题描述], [构图], [色调], [质量标准]

示例：
"pixel art style, developer coding at computer with AI assistant floating nearby,
isometric view, warm orange and blue tones, 16-bit retro game aesthetic,
high detail, clean background"
```

### 学术图表提示词结构
```
[图表类型] showing [核心概念], [数据特征], [视觉风格],
publication quality, [目标期刊] style, vector graphics

示例：
"System architecture diagram showing three-layer microservice structure,
with data flow arrows, clean minimal style, NeurIPS publication quality,
vector graphics, blue and gray color scheme"
```

### 文档插图提示词结构
```
[风格] illustration for [文档主题], [关键视觉元素],
professional business style, [比例] aspect ratio,
[色调] color palette, high quality

示例：
"Gradient glass style illustration for SaaS product launch document,
featuring dashboard interface and growth metrics,
professional business style, 16:9 aspect ratio,
blue-purple gradient, high quality"
```
