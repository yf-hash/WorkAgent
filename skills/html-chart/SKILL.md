---
name: html-chart
description: >
  HTML 结构化图表生成知识库。触发词：ASCII草图、HTML图表、流程图截图、架构图截图、
  对比表、步骤图、Playwright截图、零成本配图、1600x900图表。
user-invocable: false
effort: medium
---

# HTML Chart Generator — 结构化图表生成器

## 概述
通过 Claude 生成 ASCII 草图 → 转换为 HTML/CSS → Playwright 截图，零 API 成本生成专业级配图。适合文章中的流程图、架构图、对比表、步骤图。输出标准：1600×900（16:9），PNG 格式。

## 核心能力
- **ASCII 草图** — Claude 先生成文本预览，可快速迭代
- **HTML 渲染** — 将结构数据转换为精美 HTML/CSS 图表
- **Playwright 截图** — 高质量 PNG（1600×900），可直接用于 PPT / 文章
- **4 种风格** — business-blue / tech / warm / minimal
- **4 种图表类型** — 流程图 / 架构图 / 对比表 / 步骤图

## 适用场景
✅ **适合**：流程图、架构图、对比表、步骤图、关系图、层级图
❌ **不适合**：数据可视化（用 Mermaid/ECharts）、创意插画（用 Stable Diffusion）、精确数学图表（用 LaTeX）

---

## Phase 1：ASCII 草图生成

使用标准 ASCII 字符（`─│┌┐└┘├┤┬┴┼`）构建草图，确保结构清晰、易于转换。

### 流程图模板
```
┌──────────────────────────────────────────────────┐
│              [图表标题]                           │
├──────────────────────────────────────────────────┤
│                                                  │
│  [步骤1]  →  [步骤2]  →  [步骤3]  →  [步骤4]    │
│  标签1       标签2       标签3       标签4        │
│                                                  │
└──────────────────────────────────────────────────┘
```

### 架构图模板
```
┌──────────────────────────────────────────────────┐
│              [系统标题]                           │
├──────────────────────────────────────────────────┤
│                                                  │
│  ┌────────────────────────────────────────────┐  │
│  │  层 1：[名称]          [组件A] | [组件B]   │  │
│  └──────────────────────┬─────────────────────┘  │
│                         ↓                        │
│  ┌────────────────────────────────────────────┐  │
│  │  层 2：[名称]          [组件C] | [组件D]   │  │
│  └──────────────────────┬─────────────────────┘  │
│                         ↓                        │
│  ┌────────────────────────────────────────────┐  │
│  │  层 3：[名称]          [组件E]             │  │
│  └────────────────────────────────────────────┘  │
│                                                  │
└──────────────────────────────────────────────────┘
```

### 对比表模板
```
┌──────────────────────────────────────────────────┐
│              [对比标题]                           │
├──────────────────────────────────────────────────┤
│                                                  │
│    [方案A]            VS           [方案B]        │
│    ──────                          ──────         │
│    ✅ 优势1                        ✅ 优势1       │
│    ✅ 优势2                        ✅ 优势2       │
│    ⚠️ 劣势1                        ⚠️ 劣势1      │
│                                                  │
└──────────────────────────────────────────────────┘
```

### 步骤图模板
```
┌──────────────────────────────────────────────────┐
│              [步骤标题]                           │
├──────────────────────────────────────────────────┤
│                                                  │
│  ① [步骤一标题]                                  │
│     说明文字                                      │
│                ↓                                 │
│  ② [步骤二标题]                                  │
│     说明文字                                      │
│                ↓                                 │
│  ③ [步骤三标题]                                  │
│     说明文字                                      │
│                                                  │
└──────────────────────────────────────────────────┘
```

---

## Phase 2：HTML 转换

### ASCII → HTML 映射规则
```
ASCII 元素                  →  HTML 结构
─────────────────────────────────────────────
边框 (┌─┐│└┘)              →  CSS border / box-shadow
标题行                      →  <div class="chart-title">
[数字] / ①②③              →  <div class="step-number">
箭头 (→ ↓)                 →  <div class="arrow"> / CSS ::after
标签文字                    →  <div class="step-label">
分隔线 (├┤)                →  <hr> / border-top
VS 对比                     →  <div class="compare-vs">
✅ ⚠️ 等 emoji              →  直接保留在文本中
```

### HTML 基础结构
```html
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
  /* 使用风格变量 */
  :root {
    --primary: [风格主色];
    --secondary: [风格辅色];
    --bg: [背景色];
    --text: [文字色];
    --radius: 10px;
    --shadow: 0 4px 20px rgba(0,0,0,0.08);
  }

  * { box-sizing: border-box; margin: 0; padding: 0; }

  body {
    width: 1600px;
    height: 900px;
    background: var(--bg);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    font-family: 'Segoe UI', 'PingFang SC', sans-serif;
    overflow: hidden;
  }

  .chart-title {
    font-size: 48px;
    font-weight: 700;
    color: var(--primary);
    margin-bottom: 48px;
    letter-spacing: -0.5px;
  }

  .chart-container {
    width: 1400px;
    padding: 40px;
  }
</style>
</head>
<body>
  <!-- 图表内容 -->
</body>
</html>
```

---

## 4 种风格 CSS 变量

### business-blue（默认）— 商务蓝白
```css
:root {
  --primary: #1E3A8A;        /* 深蓝 */
  --secondary: #3B82F6;      /* 标准蓝 */
  --accent: #DBEAFE;         /* 浅蓝背景 */
  --bg: #FFFFFF;             /* 纯白 */
  --text: #1E293B;           /* 深灰文字 */
  --border: #BFDBFE;         /* 蓝色边框 */
  --shadow: 0 4px 20px rgba(30,58,138,0.08);
}
```
**适用**：商业报告、技术演示、PPT 配图（可直接粘贴）

### tech — 科技感深色
```css
:root {
  --primary: #6366F1;        /* 靛紫 */
  --secondary: #8B5CF6;      /* 紫色 */
  --accent: #1E1B4B;         /* 深紫背景块 */
  --bg: #0F172A;             /* 深色底 */
  --text: #E2E8F0;           /* 浅灰文字 */
  --border: #4338CA;         /* 深紫边框 */
  --shadow: 0 4px 20px rgba(99,102,241,0.15);
}
```
**适用**：AI/编程文章、技术博客、开发者内容

### warm — 温暖亲和
```css
:root {
  --primary: #D97706;        /* 深橙 */
  --secondary: #F59E0B;      /* 琥珀 */
  --accent: #FEF3C7;         /* 浅黄背景 */
  --bg: #FFFBEB;             /* 奶白 */
  --text: #451A03;           /* 深棕文字 */
  --border: #FCD34D;         /* 黄色边框 */
  --shadow: 0 4px 20px rgba(217,119,6,0.10);
}
```
**适用**：个人成长、情感文章、生活方式内容

### minimal — 极简线条
```css
:root {
  --primary: #0F172A;        /* 近黑 */
  --secondary: #475569;      /* 中灰 */
  --accent: #F1F5F9;         /* 浅灰背景 */
  --bg: #FFFFFF;             /* 纯白 */
  --text: #334155;           /* 深灰文字 */
  --border: #CBD5E1;         /* 浅灰边框 */
  --shadow: 0 2px 8px rgba(0,0,0,0.06);
}
```
**适用**：教程文档、说明文档、技术规范

---

## Phase 3：Playwright 截图

```javascript
// 1. 导航到 HTML 文件
mcp__playwright__browser_navigate({
  url: `file:///workspace/.tmp/html/chart-${timestamp}.html`
})

// 2. 等待渲染完成（CSS + 字体加载）
// 等待 networkidle 状态（约 500ms）

// 3. 截图（1600×900 视口，不滚动）
mcp__playwright__browser_take_screenshot({
  filename: `imgs/${articleName}-${index}.png`
})

// 4. 关闭浏览器
mcp__playwright__browser_close()

// 5. 清理临时文件
// rm workspace/.tmp/html/chart-${timestamp}.html
```

**输出**：`imgs/<article-name>-<index>.png`（1600×900, PNG）

---

## 完整 HTML 模板库

### 流程图 HTML
```html
<div class="chart-title">流程标题</div>
<div class="flow-container">
  <div class="flow-step">
    <div class="step-number">1</div>
    <div class="step-label">步骤名称</div>
  </div>
  <div class="flow-arrow">→</div>
  <div class="flow-step">
    <div class="step-number">2</div>
    <div class="step-label">步骤名称</div>
  </div>
  <!-- 重复 -->
</div>

<style>
.flow-container {
  display: flex;
  align-items: center;
  gap: 24px;
  justify-content: center;
}
.flow-step {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  padding: 32px 40px;
  background: var(--accent);
  border: 2px solid var(--border);
  border-radius: var(--radius);
  min-width: 160px;
  box-shadow: var(--shadow);
}
.step-number {
  width: 48px; height: 48px;
  background: var(--primary);
  color: white;
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 22px; font-weight: 700;
}
.step-label {
  font-size: 22px; font-weight: 600;
  color: var(--text); text-align: center;
}
.flow-arrow {
  font-size: 36px; color: var(--secondary);
  font-weight: 700;
}
</style>
```

### 架构图 HTML
```html
<div class="chart-title">架构标题</div>
<div class="arch-container">
  <div class="arch-layer">
    <span class="layer-name">前端层</span>
    <div class="layer-items">
      <span class="layer-item">React</span>
      <span class="layer-item">Vue</span>
    </div>
  </div>
  <div class="arch-connector">↓</div>
  <!-- 重复层 -->
</div>

<style>
.arch-container {
  display: flex; flex-direction: column;
  gap: 0; width: 900px; align-items: center;
}
.arch-layer {
  width: 100%;
  border: 2px solid var(--border);
  border-radius: var(--radius);
  padding: 24px 40px;
  display: flex; align-items: center; gap: 40px;
  background: var(--accent);
  box-shadow: var(--shadow);
}
.layer-name {
  font-size: 22px; font-weight: 700;
  color: var(--primary); min-width: 100px;
}
.layer-items {
  display: flex; gap: 16px; flex-wrap: wrap;
}
.layer-item {
  padding: 8px 20px;
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 6px;
  font-size: 18px; color: var(--text);
}
.arch-connector {
  font-size: 32px; color: var(--secondary);
  margin: 8px 0; font-weight: 700;
}
</style>
```

### 对比表 HTML
```html
<div class="chart-title">对比标题</div>
<div class="compare-container">
  <div class="compare-card">
    <div class="compare-heading">方案 A</div>
    <ul class="compare-list">
      <li>✅ 优势 1</li>
      <li>✅ 优势 2</li>
      <li>⚠️ 劣势 1</li>
    </ul>
  </div>
  <div class="compare-vs">VS</div>
  <div class="compare-card">
    <div class="compare-heading">方案 B</div>
    <ul class="compare-list">
      <li>✅ 优势 1</li>
      <li>🚀 优势 2</li>
      <li>⚠️ 劣势 1</li>
    </ul>
  </div>
</div>

<style>
.compare-container {
  display: flex; align-items: center; gap: 48px;
}
.compare-card {
  flex: 1; padding: 40px;
  border: 2px solid var(--border);
  border-radius: var(--radius);
  background: var(--accent);
  box-shadow: var(--shadow);
}
.compare-heading {
  font-size: 28px; font-weight: 700;
  color: var(--primary); margin-bottom: 24px;
  padding-bottom: 16px; border-bottom: 2px solid var(--border);
}
.compare-list {
  list-style: none; display: flex; flex-direction: column; gap: 14px;
}
.compare-list li { font-size: 20px; color: var(--text); }
.compare-vs {
  font-size: 36px; font-weight: 900;
  color: var(--secondary); white-space: nowrap;
}
</style>
```

---

## 文件组织
```
imgs/
├── ascii/          # ASCII 草图（.txt）
├── sources/        # HTML 源码（.html，可复用调整）
└── *.png           # 最终截图（插入文章）

workspace/
└── .tmp/html/      # 截图前临时 HTML（自动清理）
```

## 相关资源
- Playwright MCP: Claude Code 内置，调用 `mcp__playwright__browser_*`
- 在线预览中间产物：直接用浏览器打开 `imgs/sources/*.html`
