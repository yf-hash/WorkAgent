# Slidev — 开发者演示框架

## 概述
Slidev 是面向开发者的演示文稿框架，使用 Markdown + Vue 组件构建交互式幻灯片。支持实时代码演示、语法高亮、动画过渡，输出 Web / PDF / PPTX。

## 核心能力
- **Markdown 驱动** — 纯文本写幻灯片，版本可控
- **代码块高亮** — 支持逐行聚焦动画（`{1|2|3}` 语法）
- **Vue 组件嵌入** — 在幻灯片中运行真实的交互 Demo
- **演讲者视图** — 双屏模式，含计时器和备注
- **多主题** — 默认、seriph、bricks、forest、apple-basic 等
- **导出** — HTML SPA、PDF、PPTX（via headless chrome）

## 安装与启动
```bash
# 全局安装 CLI
npm install -g @slidev/cli

# 创建新演示
npm init slidev@latest

# 启动开发服务器
slidev slides.md

# 导出 PDF
slidev export slides.md --format pdf

# 导出 PPTX
slidev export slides.md --format pptx
```

## Markdown 语法

### 基础幻灯片
```markdown
---
theme: default
highlighter: shiki
lineNumbers: false
---

# 演讲标题

副标题或作者信息

---

## 第一张内容幻灯片

- 要点一
- 要点二
- 要点三

---

## 代码演示

```python
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```

---
```

### 代码聚焦动画
```markdown
```python {1|3|5|all}
import torch
import torch.nn as nn

model = nn.Sequential(
    nn.Linear(784, 256),
    nn.ReLU(),
    nn.Linear(256, 10)
)
```
```

### 两栏布局
```markdown
<div class="grid grid-cols-2 gap-4">
<div>

**左侧内容**
- 要点一
- 要点二

</div>
<div>

**右侧内容**
![图片](image.png)

</div>
</div>
```

### 演讲者备注
```markdown
---

## 幻灯片标题

内容…

<!-- 
演讲者备注：
- 重点强调第三点
- 提问环节预留 2 分钟
-->
```

## 主题选择

| 主题 | 风格 | 适用场景 |
|------|------|---------|
| `default` | 简洁白色 | 通用技术演讲 |
| `seriph` | 衬线优雅 | 正式报告 |
| `bricks` | 暗色系 | 开发者大会 |
| `forest` | 绿色自然 | 开源项目 |
| `apple-basic` | Apple 风格 | 产品发布 |
| `geist` | Vercel 风格 | 前端技术 |

## 前端开发专属样式
灵感来源：`zarazhangrui/frontend-slides`

```markdown
---
theme: default
fonts:
  sans: 'Fira Code'
  mono: 'Fira Code'
---

# Frontend Architecture

<style>
.code-demo {
  background: #1a1a2e;
  border-radius: 8px;
  padding: 1rem;
}
</style>

## Component Tree

```jsx
function App() {
  return (
    <Provider store={store}>
      <Router>
        <Header />
        <Main />
      </Router>
    </Provider>
  )
}
```
```

## 最佳实践

1. **技术演讲** — 使用代码聚焦动画逐步展示逻辑
2. **架构介绍** — 嵌入真实运行的 Vue/React Demo
3. **教程演示** — 配合终端录制工具展示 CLI 操作
4. **代码审查** — 用 `{lines}` 语法逐行讲解

## 输出格式

```markdown
## Slidev 演示输出

**演示文件**：`slides.md`
**开发预览**：`http://localhost:3030`
**导出文件**：
- Web: `dist/index.html`（可部署到 Vercel/Netlify）
- PDF: `slides-export.pdf`
- PPTX: `slides-export.pptx`

**演讲者视图**：`http://localhost:3030/presenter`
```

## 相关资源
- 官网: https://sli.dev/
- GitHub: https://github.com/slidevjs/slidev
- 主题库: https://sli.dev/themes/gallery
- 组件库: https://sli.dev/addons/components
- 前端幻灯片参考: https://github.com/zarazhangrui/frontend-slides
