---
name: md-visual
description: >
  Markdown 转视觉图像工具集。触发词：markdown转图片、md转图、mark-pic、Madopic、
  tablesnap、表格截图、markdown海报、md海报、数学公式图片、Mermaid图片导出、
  ECharts图表、KaTeX、markdown可视化、代码卡片、分享图片。
  整合 mark-pic / Madopic / tablesnap / markdown-table-imagifier 四大工具。
user-invocable: false
effort: medium
---

# MD Visual — Markdown 转视觉图像工具集

> 整合来源：
> - mark-pic（Markdown → 样式图片，40+渐变背景）
> - Madopic（Markdown → 精美海报，支持KaTeX/Mermaid/ECharts）
> - tablesnap（Markdown表格 → PNG，Go CLI）
> - markdown-table-imagifier（浏览器端表格 → PNG）
> - markdown-table-to-image（Flask服务，表格 → PNG）

---

## 一、工具选型速查

| 工具 | 最适合 | 特点 | 部署方式 |
|------|--------|------|---------|
| **mark-pic** | 代码卡片、技术分享图 | 40+渐变背景、暗色模式、Mermaid支持 | React/Vite本地 |
| **Madopic** | 完整文章海报、数学内容 | KaTeX+Mermaid+ECharts、多格式导出 | 在线/本地 |
| **tablesnap** | 表格快速截图 | Go CLI、emoji支持、深浅主题 | `go install` |
| **table-imagifier** | 浏览器端表格转图 | 纯客户端、无需服务器 | 静态页面 |
| **table-to-image** | 服务端表格转图 | Flask API、动态尺寸 | Python服务 |

---

## 二、mark-pic — Markdown 样式图片生成

### 核心能力
- Markdown 内容 → 精美样式图片
- 40+ 渐变背景主题
- 支持暗色/亮色模式
- 内嵌 Mermaid 图表渲染
- LaTeX 数学公式支持
- 可拖拽调整编辑器/预览区比例
- 导出：html-to-image → PNG

### 安装与使用
```bash
git clone https://github.com/alterem/mark-pic
cd mark-pic
npm install
npm run dev
# 访问 http://localhost:5173
```

### 适用场景
```
技术分享卡片：代码片段 + 说明文字 → 社交媒体分享图
知识卡片：概念解释 + 示例 → 微信/小红书配图
会议摘要：要点列表 → 可分享的摘要图
代码展示：带语法高亮的代码截图
```

### 背景主题示例
```
渐变系列：sunset（橙红）/ ocean（蓝绿）/ forest（绿色）/ purple（紫色）
商务系列：corporate-blue / professional-gray / executive-dark
创意系列：neon-glow / pastel-dream / aurora
```

---

## 三、Madopic — Markdown 精美海报生成

### 核心能力
- 完整 Markdown 文章 → 精美海报/长图
- KaTeX 数学公式渲染
- Mermaid 图表内嵌
- ECharts 数据可视化
- 实时预览 + 缩放
- 多格式导出：PNG / PDF / HTML

### 使用方式
```
在线版：https://madopic.com（或本地部署）

本地部署：
git clone https://github.com/xiaolinbaba/Madopic
npm install && npm run dev
```

### 支持的特殊语法
```markdown
# 普通 Markdown 内容

## 数学公式（KaTeX）
行内公式：$E = mc^2$
块级公式：
$$\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}$$

## Mermaid 图表
```mermaid
graph LR
    A --> B --> C
```

## ECharts 数据图表
```echarts
{
  "xAxis": {"data": ["Q1","Q2","Q3","Q4"]},
  "yAxis": {},
  "series": [{"type":"bar","data":[120,200,150,80]}]
}
```
```

### 适用场景
```
学术内容分享：含公式的数学/物理/统计内容
技术博客长图：完整文章 → 可分享的长图
数据报告海报：含图表的分析报告 → 精美海报
教学材料：课程内容 → 可打印的学习卡片
```

---

## 四、tablesnap — 表格快速截图（CLI）

### 核心能力
- Markdown 表格 → PNG（命令行管道）
- 深色/浅色主题
- Emoji 支持（Twemoji）
- Go 编写，跨平台，无依赖

### 安装与使用
```bash
# 安装
go install github.com/joargp/tablesnap/cmd/tablesnap@latest

# 基础用法（管道输入）
echo "| 姓名 | 部门 | 薪资 |
|------|------|------|
| 张三 | 研发 | 25k |
| 李四 | 产品 | 22k |" | tablesnap > table.png

# 从文件读取
cat data.md | tablesnap > output.png

# 深色主题
cat data.md | tablesnap --theme dark > output.png

# 指定输出路径
cat data.md | tablesnap -o ./imgs/table.png
```

### 适用场景
```
CI/CD 自动化：在流水线中自动生成表格截图
批量处理：脚本循环处理多个表格文件
报告生成：将数据表格嵌入 PDF/PPT 报告
```

---

## 五、markdown-table-imagifier — 浏览器端表格转图

### 核心能力
- 纯客户端，无需服务器
- Markdown 表格 → PNG
- 实时预览
- 可直接下载

### 使用方式
```
在线版：https://fahdi.github.io/markdown-table-imagifier/

本地部署：
git clone https://github.com/fahdi/markdown-table-imagifier
# 直接用浏览器打开 index.html
```

### 适用场景
```
临时需求：快速将表格转为图片，无需安装任何工具
隐私敏感：数据不离开本地浏览器
简单表格：不需要复杂样式的快速转换
```

---

## 六、markdown-table-to-image — Flask API 服务

### 核心能力
- Flask Web 服务
- 动态尺寸（自适应内容）
- 文字自动换行
- 输出 PNG

### 安装与使用
```bash
git clone https://github.com/fahdi/markdown-table-to-image
pip install flask pillow
python app.py
# 访问 http://127.0.0.1:5000/

# API 调用
curl -X POST http://127.0.0.1:5000/convert \
  -H "Content-Type: application/json" \
  -d '{"table": "| A | B |\n|---|---|\n| 1 | 2 |"}'
```

---

## 七、场景决策树

```
需要将 Markdown 转为图片
  │
  ├── 是表格内容？
  │   ├── 需要 CLI/自动化 → tablesnap
  │   ├── 浏览器快速转换 → markdown-table-imagifier
  │   └── 需要 API 服务  → markdown-table-to-image（Flask）
  │
  ├── 是完整文章/长内容？
  │   ├── 含数学公式/ECharts → Madopic
  │   └── 普通 Markdown 内容 → mark-pic
  │
  ├── 是代码/技术卡片？
  │   → mark-pic（渐变背景 + 代码高亮）
  │
  └── 需要精美海报（社交媒体分享）？
      → Madopic（最丰富的样式选项）
```

---

## 八、提示词模板（Claude 辅助生成内容）

### 生成适合 mark-pic 的 Markdown 卡片
```
请将以下内容整理为适合 mark-pic 生成分享卡片的 Markdown 格式：
- 内容简洁，不超过300字
- 使用标题、要点列表、代码块等结构
- 适合 [技术分享/知识卡片/会议摘要] 场景

内容：[原始内容]
```

### 生成适合 Madopic 的长图内容
```
请将以下内容整理为适合 Madopic 生成海报的 Markdown 格式：
- 可包含数学公式（KaTeX语法）
- 可包含 Mermaid 图表
- 结构清晰，适合长图阅读

内容：[原始内容]
```
