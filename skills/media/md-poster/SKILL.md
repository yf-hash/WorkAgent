---
name: md-poster
description: >
  Markdown 转海报/分享卡片技能。整合 mark-pic（40+ 渐变背景，代码卡片）+ Madopic（KaTeX 公式 / Mermaid /
  ECharts，长图海报）。适合技术分享卡片、知识卡片、含公式的学术内容、社交媒体长图。
  触发词：markdown 转图片、md 转海报、mark-pic、Madopic、代码卡片、分享图片、技术博客长图
user-invocable: false
effort: medium
harness:
  execute:
    preset: media-heavy
  constrain:
    profile: shell-restricted
  loop:
    mode: one-shot
  memory:
    scope: session
    reads: [project-context]
  security:
    danger-level: medium
---

# MD Poster — Markdown 转海报/分享卡片

> 单一职责：把 Markdown 内容渲染成精美海报或分享卡片图片。
> 不做：Markdown 表格转图（→ `md-table-image`）

## 工具选型

| 工具 | 适用 | 特点 |
|---|---|---|
| **mark-pic** | 代码卡片、技术分享图 | 40+ 渐变背景、暗色模式、Mermaid 支持 |
| **Madopic** | 完整文章海报、含公式/数据图 | KaTeX + Mermaid + ECharts、多格式导出 |

## mark-pic — 代码卡片 / 技术分享图

### 核心能力
- Markdown 内容 → 精美样式图片
- 40+ 渐变背景主题
- 支持暗色/亮色模式
- 内嵌 Mermaid 图表渲染
- LaTeX 数学公式支持
- 导出：html-to-image → PNG

### 适用
- 技术分享卡片：代码片段 + 说明文字 → 社交媒体分享图
- 知识卡片：概念解释 + 示例 → 微信/小红书配图
- 会议摘要：要点列表 → 可分享的摘要图
- 代码展示：带语法高亮的代码截图

### 部署

```bash
git clone https://github.com/alterem/mark-pic
cd mark-pic && npm install && npm run dev
# 访问 http://localhost:5173
```

### 背景主题

```
渐变系列：sunset（橙红）/ ocean（蓝绿）/ forest（绿色）/ purple（紫色）
商务系列：corporate-blue / professional-gray / executive-dark
创意系列：neon-glow / pastel-dream / aurora
```

## Madopic — 长图海报

### 核心能力
- 完整 Markdown 文章 → 精美海报/长图
- KaTeX 数学公式渲染
- Mermaid 图表内嵌
- ECharts 数据可视化
- 实时预览 + 缩放
- 多格式导出：PNG / PDF / HTML

### 部署

```bash
# 在线版：https://madopic.com
# 本地部署：
git clone https://github.com/xiaolinbaba/Madopic
npm install && npm run dev
```

### 特殊语法

```markdown
## 数学公式（KaTeX）
行内公式：$E = mc^2$
块级公式：
$$\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}$$

## Mermaid 图表
\`\`\`mermaid
graph LR
    A --> B --> C
\`\`\`

## ECharts 数据图表
\`\`\`echarts
{
  "xAxis": {"data": ["Q1","Q2","Q3","Q4"]},
  "yAxis": {},
  "series": [{"type":"bar","data":[120,200,150,80]}]
}
\`\`\`
```

### 适用

- 学术内容分享：含公式的数学/物理/统计内容
- 技术博客长图：完整文章 → 可分享的长图
- 数据报告海报：含图表的分析报告 → 精美海报
- 教学材料：课程内容 → 可打印的学习卡片

## 选择决策

```
输入内容判断：
  ├── 代码片段 + 简短说明（< 300 字）→ mark-pic
  ├── 完整文章 / 含数学公式 → Madopic
  ├── 含 ECharts 数据图 → Madopic
  └── 需要多种渐变背景选项 → mark-pic
```
